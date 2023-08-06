import json
import os

import chattr_event_bus.constants.schema as schema_constants



def get_schema(schema_name: str) -> dict:
    ''' If schema_name is valid this returns schema metadata otherwise raises ValueError.
    Arguments:
        schema_name

    Returns:
        schema (dict): the request schema loaded from .schema.json file.

    Raises:
        ValueError: raised when schema_name is not a defined schema.
    '''

    schema_path = os.path.join(schema_constants.SCHEMA_FOLDER, f'{schema_name}{schema_constants.FILE_EXTENSION}')

    if not os.path.exists(schema_path):
        raise ValueError(f'Invalid schema_name: {schema_name}')

    with open(schema_path, 'r') as f:
        schema = json.load(f)

    return schema
