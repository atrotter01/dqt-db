import os
import concurrent
from pathlib import Path
import json
import xmltodict
from app.util import Util

asset_importer_instance = None

class AssetImport:

    util: Util
    root_path: str
    asset_map: dict

    def __init__(self, util, root_path):
        self.util = util
        self.root_path = root_path
        self.asset_map = self.build_asset_map_from_file()
        globals()['asset_importer_instance'] = self

    def build_asset_map_from_file(self):
        path = os.path.join(self.root_path, 'assets.xml')
        asset_map: dict = {}

        with open(path) as fh:
            xml = fh.read()
            xmldict = xmltodict.parse(xml, process_namespaces=True)
            assets = xmldict.get('Assets').get('Asset')

            for asset in assets:
                key = asset.get('PathID')
                asset_map.update({key: asset})

            return asset_map

    def map_path_to_file(self, path: str):
        asset: dict = self.asset_map.get(path)

        assert asset is not None, path

        asset_container: str = asset.get('Container')

        if asset_container is None:
            return None

        container_path: Path = Path(asset_container).parent
        filepath: str = os.path.join(self.root_path, container_path, path) + '.json'

        return filepath

    def save_assets_to_db(self):
        executor = concurrent.futures.ProcessPoolExecutor(16)
        futures = [executor.submit(process_and_save_asset, path) for path in self.asset_map]
        concurrent.futures.wait(futures)

def process_and_save_asset(path):
    try:
        filepath = asset_importer_instance.map_path_to_file(path=path)
        asset_name = asset_importer_instance.asset_map.get(path).get('Name')

        if path in asset_importer_instance.util.asset_list:
            return True

        if filepath is None:
            filepath = os.path.join(asset_importer_instance.root_path, f'{path}.json')

        #print(f'{asset_name}\t{path}\t{filepath}')

        if not os.path.exists(filepath):
            print(f'Could not find {path}')

        filetype = Path(asset_name).name.split('_')[0].replace('.json', '')
        container = str(Path(filepath).parent).replace(asset_importer_instance.root_path + '/', '')

        if os.path.exists(filepath):
            with open(filepath) as fh:
                document = json.load(fh)

                if asset_importer_instance.util.save_asset(path=path, filepath=filepath, container=container, filetype=filetype, document=document, display_name=asset_name):
                    print(f'Saved {path}')
                    #os.unlink(filepath)
                    return True
                else:
                    return False
        else:
            print(f'{filepath} does not exist.')
            return False
    except Exception as ex:
        print(ex)
        return False
