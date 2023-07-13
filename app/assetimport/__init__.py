import os
import json
import xmltodict
from pathlib import Path
from app.util import Util

class AssetImport:

    util: Util
    root_path: str
    asset_map: dict

    def __init__(self, util, root_path):
        self.util = util
        self.root_path = root_path
        self.asset_map = self.build_asset_map_from_file()

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

    def map_path_to_file(self, path: int, asset_map: dict):
        asset: dict = asset_map.get(path)

        assert asset is not None, path

        asset_name: str = asset.get('Name')
        asset_container: str = asset.get('Container')

        if asset_container is None:
            return None

        container_path: Path = Path(asset_container).parent
        filepath: str = os.path.join(self.root_path, container_path, asset_name) + '.json'

        return filepath

    def save_assets_to_db(self, file_type_to_process = None):
        for path in self.asset_map:
            filepath = self.map_path_to_file(path=path, asset_map=self.asset_map)

            if not filepath:
                print(f'Failed to map {self.asset_map.get(path)} to a file.')
                continue

            filetype = Path(filepath).name.split('_')[0]

            if file_type_to_process is not None and not filetype.lower() == str(file_type_to_process).lower():
                continue

            container = str(Path(filepath).parent).replace(self.root_path + '/', '')

            if os.path.exists(filepath):
                with open(filepath) as fh:
                    document = json.load(fh)
                    
                    if self.util.save_asset(path=path, filepath=filepath, container=container, filetype=filetype, document=document):
                        print(f'Saved {path}')
                        os.unlink(filepath)
