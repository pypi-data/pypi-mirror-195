import os

import chattr_event_bus.constants.schema as schema_constants
from chattr_event_bus.validators.json import validate
from chattr_event_bus.serializers.json import serialize, deserialize
from chattr_event_bus.services.schema import get_schema

schemas = []
for root, dirs, files in os.walk(schema_constants.SCHEMA_FOLDER):
    schemas += [
        (
            f'{root}/{file}'
            .replace(schema_constants.FILE_EXTENSION, '')
            .replace(schema_constants.SCHEMA_FOLDER, '')
            .lstrip('/')
        )
        for file in files
        if file.endswith(schema_constants.FILE_EXTENSION)
    ]
