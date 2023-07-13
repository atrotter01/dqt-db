import os
import xmltodict
import psycopg
from pathlib import Path
from app.util import map_path_to_file, get_database_connection_string, get_processed_keys

def get_asset_map_from_file(root_path):
    path = os.path.join(root_path, 'assets.xml')
    asset_data: dict = {}

    with open(path) as fh:
        xml = fh.read()
        xmldict = xmltodict.parse(xml, process_namespaces=True)
        assets = xmldict.get('Assets').get('Asset')
        
        for asset in assets:
            key = asset.get('PathID')
            asset_data.update({key: asset})

        return asset_data

def save_assets_to_db(root_path, asset_map, file_type_to_process = None):
    connection_string = get_database_connection_string()
    assets: list = []
    existing_assets = get_processed_keys(file_type_to_process)

    for path in asset_map:
        filepath = map_path_to_file(path=path, root_path=root_path, asset_map=asset_map)
        filetype = Path(filepath).name.split('_')[0]

        if file_type_to_process is not None and not filetype.lower() == str(file_type_to_process).lower():
            continue

        if path in existing_assets:
            continue

        container = str(Path(filepath).parent).replace(root_path + '/', '')

        if os.path.exists(filepath):
            with open(filepath) as fh:
                document = fh.read()
                assets.append((path, filepath, container, filetype, document))
        else:
            print(f'{filepath} does not exist.')

    if len(assets) > 0:
        with psycopg.connect(conninfo=connection_string) as conn:
            query: str = 'insert into public.assets(path, filepath, container, filetype, document) values (%s, %s, %s, %s, %s)'
            cursor: object = conn.cursor()
            cursor.executemany(query, assets)
