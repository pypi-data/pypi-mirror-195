import json
import os

schema_paths = []
for root, dirs, files in os.walk('chattr_event_bus/schemas'):
    schema_paths += [
        f'{root}/{file}'
        for file in files
        if file.endswith('.schema.json')
    ]


def format_json_file(file_path):
    with open(file_path, 'r+') as f:
        unformatted_schema = json.load(f)
        f.seek(0)
        json.dump(unformatted_schema, f, indent=4)
        f.write('\n')
        f.truncate()


for schema_path in schema_paths:
    format_json_file(schema_path)
