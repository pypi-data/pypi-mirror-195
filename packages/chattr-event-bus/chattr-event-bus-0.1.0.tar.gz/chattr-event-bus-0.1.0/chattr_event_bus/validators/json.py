import jsonschema

import chattr_event_bus.services.schema as schema_service


def validate(schema_name: str, payload: dict):
    ''' If payload is valid this returns schema metadata otherwise raises.

    Args:
        schema_name (str): name of schema to validate against
        payload (dict): the payload to validate

    Returns:
        metadata dict of schema

    raises:
        ValueError when schema_name is not a defined schema.
        jsonschema.exceptions.ValidationError for invalid payload.
    '''

    schema = schema_service.get_schema(schema_name)
    jsonschema.validate(instance=payload, schema=schema['schema'])
    return schema['meta']
