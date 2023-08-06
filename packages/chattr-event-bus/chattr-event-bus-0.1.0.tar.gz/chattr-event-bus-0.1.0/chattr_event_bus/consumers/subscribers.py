import os
import datetime
import functools
import inspect
import json
import logging
import pytz
import time
import re
from typing import List
from uuid import uuid4
from chattr_config.monitoring.context import Context
from chattr_config.monitoring.service.monitoring_service import MonitoringService
from chattr_config.utils.system_utils import get_machine_info

ENV = os.getenv("ENV", "local")
DEDUPLICATION_INTERVAL = 60 * 60 * 24 * 2  # 2 days

monitoring_service = MonitoringService()

# Regular logs
logger = logging.getLogger(__name__)

# Logs to EventBus logger, but doesn't have "Event_log: " prefix, so wouldn't be shipped to S3
eventbus_logger = logging.getLogger("eventbus_events")


class JsonEventError(Exception):
    pass


class EmptyEventError(Exception):
    pass


class MissingContextError(Exception):
    pass


class DuplicateEventError(Exception):
    pass


class Event:
    def __init__(self):
        self.start = time.time()
        self.log = {}
        self.valid = False
        self.payload = None
        self.context = None
        self.func = None
        self.duplication_key = None
        self.tags = None

    def finish(self):
        self.log["ended_on"] = datetime.datetime.now(tz=pytz.utc)
        self.log["total_process_time"] = time.time() - self.start
        eventbus_logger.info(
            "Eventbus Consumer log", extra={"eventbus_message": self.log}
        )

    def is_duplicate(self, cacher, deduplication_interval=DEDUPLICATION_INTERVAL):
        """
        Sets a key in redis with expiration and checks if it does not exist already

        Returns:
            bool: False is this is a first time triggered event (Good). True is repeated event (Bad).
        """
        try:
            key = self.duplication_key
            if key is None:
                return False
            res = cacher.set(name=key, value="1", nx=True, ex=deduplication_interval)
            if res:
                # not processed yet
                return False
            else:
                # processed - key does exist in redis
                logging.warning(f"Repeated processing found with key: {key}.")
                monitoring_service.increment_metric(
                    "faust_consumer_duplicate_message", self.tags
                )
                return True
        except:
            logging.exception("Unable to retrieve the double processing value")
            return False

    @classmethod
    def _parse_and_validate(cls, raw_message):
        try:
            contents = json.loads(raw_message)
        except Exception as e:
            raise JsonEventError("JSON error") from e
        if not isinstance(contents, dict):
            raise JsonEventError("Event contents are not a dict")
        payload = contents.get("payload")
        if isinstance(payload, (str, bytes)):
            payload = json.loads(payload)
        if not isinstance(payload, dict):
            raise JsonEventError("Event payload is not a dict")
        if not payload:
            raise EmptyEventError
        contents["payload"] = payload
        return contents

    @classmethod
    def _context_from_contents(cls, contents):
        try:
            context = Context.acquire_from_dict(
                context_dict=contents.get("context", {}), set_context=False
            )
            return context.to_dict() if context else None
        except Exception as e:
            raise MissingContextError from e

    @classmethod
    def from_message(cls, func, raw_message, consumer_group_key: str = ''):
        try:
            now = datetime.datetime.now(tz=pytz.utc)
            subscriber_name = func.__name__
            subscriber_file = inspect.getfile(func)

            event = Event()
            event.log = {
                **event.log,
                **get_machine_info(),
                "type": "consumer",
                "consumer": f"{subscriber_file}#{subscriber_name}",
                "started_on": str(now),
            }
            event.tags = monitoring_service.get_tags(
                consumer=subscriber_name, environment=ENV
            )

            contents = None
            contents = Event._parse_and_validate(raw_message)
            event.log.update(message=contents, **contents)
            event.payload = contents.get("payload")
            event_name = contents.get("name")
            event_uuid = contents.get("event_uuid")
            event.tags = monitoring_service.get_tags(
                consumer=subscriber_name, environment=ENV, topic=event_name
            )

            context = Event._context_from_contents(contents)
            event.context = context
            event.payload["context"] = context
            event.log["context"] = context

            if event_name and event_uuid:
                event.duplication_key = f"{consumer_group_key}-{event_name}-{subscriber_name}-{event_uuid}"

            event.func = func
            event.valid = True

        except JsonEventError:
            event.log["error"] = "Error deserializing message"
            logger.exception(f"Error deserializing message")
            logger.info(event.log)
            eventbus_logger.error(
                "Error retrieving payload", extra={"eventbus_message": event.log}
            )
            monitoring_service.increment_metric(
                "faust_consumer_deserialization_error", event.tags
            )

        except EmptyEventError:
            eventbus_logger.error(
                "Empty payload", extra={"eventbus_message": event.log}
            )
            monitoring_service.increment_metric(
                "faust_consumer_empty_payload", event.tags
            )

        except MissingContextError:
            logger.warning("Missing context from producer")

        except Exception as err:
            event.log["exception"] = str(err)
            eventbus_logger.error("Error", extra={"eventbus_message": event.log})

        finally:
            eventbus_logger.info(
                f"Faust worker {subscriber_name} received message on {str(now)}.",
                extra={
                    "message_body": contents,
                    "topic": contents.get("name") if contents else None,
                    "consumer": {"name": subscriber_name, "path": subscriber_file},
                },
            )
            monitoring_service.increment_metric(
                "faust_consumer_message_received", event.tags
            )
            return event


class Batch:
    def __init__(self, func):
        self.id = f"{func.__name__}-{uuid4()}"
        self.start = time.time()
        self.valid = False
        self.events = []
        self.log = {"batch_id": self.id, "correlation_ids": []}
        self.func = func
        self.tags = None

    def finish(self):
        self.log["ended_on"] = datetime.datetime.now(tz=pytz.utc)
        self.log["total_process_time"] = time.time() - self.start
        eventbus_logger.info("Batch done", extra={"eventbus_message": self.log})

    def filter_duplicates(self, cacher, deduplication_interval=DEDUPLICATION_INTERVAL):
        self.events = filter(
            lambda e: not e.is_duplicate(cacher, deduplication_interval), self.events
        )

    def from_messages(cacher, func, raw_messages, consumer_group_key: str = ''):
        try:
            now = datetime.datetime.now(tz=pytz.utc)
            subscriber_name = func.__name__
            subscriber_file = inspect.getfile(func)

            batch = Batch(func)
            batch.log = {
                **batch.log,
                **get_machine_info(),
                "type": "consumer",
                "consumer": f"{subscriber_file}#{subscriber_name}",
                "started_on": str(now),
                "batch_size": len(raw_messages),
            }
            batch.tags = monitoring_service.get_tags(
                consumer=subscriber_name, environment=ENV
            )

            for m in raw_messages:
                event = Event.from_message(func, m)
                if event.valid:
                    batch.events.append(event)

            if len(batch.events) > 0:
                batch.valid = True
                batch.log["topic"] = batch.events[0]["name"]

            eventbus_logger.info(
                f"Faust worker {subscriber_name} received batch on {str(now)}.",
                extra={
                    "batch_size": len(raw_messages),
                    "valid_events": len(batch.events),  # some may be duplicated
                    "topic": batch.log.get("topic"),
                    "consumer": {"name": subscriber_name, "path": subscriber_file},
                    "eventbus_batch_message": batch.log,
                },
            )
            event.tags = monitoring_service.get_tags(
                consumer=subscriber_name, environment=ENV, topic=subscriber_name
            )
            monitoring_service.increment_metric(
                "faust_batch_consumer_message_received", event.tags
            )

        except Exception as e:
            batch.log["exception"] = str(e)
            eventbus_logger.error(
                "Batch error", extra={"eventbus_batch_message": batch.log}
            )

        finally:
            return batch


async def process_event(event, *args, **kwargs):
    if not event.valid:
        return
    try:
        start = time.time()
        result = await event.func(event.tags, event.payload, *args, **kwargs)
        end = time.time()
        run_time = end - start
        event.log["result"] = str(result)
        event.log["run_time"] = run_time
        monitoring_service.send_metric("faust_execution_time", run_time, event.tags)
        monitoring_service.increment_metric(
            "faust_consumer_processing_success", event.tags
        )

    except Exception as e:
        event.log["error"] = e
        logger.warning(f"Error when processing {event.func.__name__}: {e}")
        monitoring_service.increment_metric(
            "faust_consumer_processing_error", event.tags
        )

    finally:
        event.finish()


async def process_batch(batch, *args, **kwargs):
    if not batch.valid:
        return
    try:
        event = Event()
        start = time.time()
        events = []
        for e in batch.events:
            events.append(e.payload)
            batch.log["correlation_ids"].append(e.context.get("correlation_id"))
        result = await batch.func(batch.tags, events, *args, **kwargs)
        end = time.time()
        run_time = end - start
        batch.log["result"] = str(result)
        batch.log["run_time"] = run_time
        batch.log["processed_events"] = len(events)
        monitoring_service.send_metric(
            "faust_batch_execution_time", run_time, batch.tags
        )
        monitoring_service.increment_metric(
            "faust_batch_processing_success", event.tags
        )

    except Exception as e:
        batch.log["error"] = e
        for event in batch.events:
            event.log["batch_exception_id"] = batch.id
        logger.warning(f"Error when processing batch {batch.func.__name__}: {e}")
        monitoring_service.increment_metric("faust_batch_processing_error", batch.tags)

    finally:
        for e in batch.events:
            e.finish()
        batch.finish()


def kafka_topics(app, *topics, prefix=None):
    _topics: List[str] = []
    for topic in topics:
        if not bool(re.fullmatch("[a-zA-Z0-9\\._\\-]*", topic)):
            raise ValueError(f"Invalid kafka topic name '{topic}' supplied")
        _topics.append(f"{prefix}.{topic}" if prefix is not None else topic)
    logger.info(f"Subscribed to {_topics} topic(s).")
    return app.topic(*_topics)


async def dummy_sink(_):
    pass


def subscribe_single(
    app,
    cacher,
    *topics: str,
    prefix: str = None,
    deduplication_interval: int = DEDUPLICATION_INTERVAL,
    consumer_group_key: str = ''
):
    def decorator(func):
        @functools.wraps(func)
        @app.agent(kafka_topics(app, *topics, prefix=prefix), sinks=[dummy_sink])
        async def wrapper(stream):
            async for message in stream:
                try:
                    event = Event.from_message(func, message, consumer_group_key=consumer_group_key)
                    if not event.valid:
                        continue
                    if event.is_duplicate(cacher, deduplication_interval):
                        continue
                    await process_event(event)

                finally:
                    # Keep dummy sink happy
                    yield None

        return wrapper

    return decorator


def subscribe_batch(
    app,
    cacher,
    *topics: str,
    batch_size: int = 1,
    timeout: int = 10,
    prefix: str = None,
    deduplication_interval: int = DEDUPLICATION_INTERVAL,
    consumer_group_key: str = ''
):
    def decorator(func):
        @functools.wraps(func)
        @app.agent(kafka_topics(app, prefix=prefix, *topics), sinks=[dummy_sink])
        async def wrapper(stream):
            async for messages in stream.take(batch_size, within=timeout):
                batch = Batch.from_messages(cacher, func, messages, consumer_group_key=consumer_group_key)
                batch.filter_duplicates(cacher, deduplication_interval)
                await process_batch(batch)

                # Keep dummy sink happy
                yield None

        return wrapper

    return decorator
