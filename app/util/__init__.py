import json
import re
import redis
import brotli
import math
from pathlib import Path

class Util:
    asset_list: list = []
    cache_keys: list = ['asset_path_map', 'asset_types', 'lookup_cache', 'metadata_cache', 'unprocessed_asset_counts']
    redis_client: redis
    lookup_cache: dict = {}
    possible_circular_references: list = []

    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=False)
        self.asset_list = self.build_asset_list()
        self.lookup_cache = self.cache_lookup_table()

    def build_asset_list(self):
        valid_keys: list = [key.decode() for key in self.redis_client.keys() if not key.decode().endswith('_data')]

        return valid_keys

    def get_asset_list(self, asset_type: str = None):

        if asset_type is None:
            asset_list: list = []

            for key in self.lookup_cache.keys():
                asset_list.extend(self.lookup_cache.get(key))

            return asset_list
        else:
            return self.lookup_cache.get(asset_type)

    def get_asset_by_path(self, path: int, deflate_data: bool = True):
        asset: dict = None

        #if path in self.cache_keys:
        #    asset = self.inflate_asset(self.redis_client.get(path))
        #else:
        redis_data = self.redis_client.get(path)

        if redis_data is None:
            return None

        asset = json.loads(redis_data)

        if path not in self.cache_keys and not str(path).endswith('_cache'):
            assert isinstance(asset, dict), type(asset)

        if deflate_data == True and self.redis_client.get(f'{path}_data') is not None:
            asset.update({'document': self.inflate_asset(self.redis_client.get(f'{path}_data'))})

        if deflate_data == True and self.redis_client.get(f'{path}_processed_data') is not None:
            asset.update({'processed_document': self.inflate_asset(self.redis_client.get(f'{path}_processed_data'))})

        return asset

    def inflate_asset(self, asset):
        return json.loads(brotli.decompress(asset).decode())

    def deflate_asset(self, asset):
        return brotli.compress(json.dumps(asset).encode())

    def save_processed_document(self, path: int, processed_document: dict, display_name: str):
        asset: dict = self.get_asset_by_path(path=path, deflate_data=False)
        asset.update({'processed': True})
    
        if display_name is not None:
            asset.update({'display_name': display_name})

        self.redis_client.set(path, json.dumps(asset))
        self.redis_client.set(f'{path}_processed_data', self.deflate_asset(processed_document))

    def save_asset(self, path: int, filepath: str, container: str, filetype: str, document: dict, display_name: str):
        asset: dict = {
            'path': path,
            'filepath': filepath,
            'container': container,
            'filetype': filetype,
            'display_name': display_name,
            'processed': False
        }

        data_saved: bool = self.redis_client.set(f'{path}_data', self.deflate_asset(document))
        
        if data_saved is True:
            return self.redis_client.set(path, json.dumps(asset))
        else:
            return False

    def get_unprocessed_assets(self):
        return self.get_asset_by_path('unprocessed_asset_counts', deflate_data=False)

    def cache_metadata(self, force_rebuild: bool = False):
        asset_list: list = self.asset_list
        metadata_cache: list = []
        asset_types: list = []
        asset_path_map: dict = {}
        lookup_cache: dict = {}
        total_assets: int = len(self.asset_list)
        processed_assets: int = 0
        unprocessed_asset_counts: dict = {}

        if self.redis_client.get('metadata_cache') is None\
        or self.redis_client.get('asset_types') is None\
        or self.redis_client.get('asset_path_map') is None\
        or self.redis_client.get('lookup_cache') is None\
        or force_rebuild is True:
            for path in asset_list:
                if path in self.cache_keys:
                    continue

                asset = self.get_asset_by_path(path=path, deflate_data=False)
                filepath = asset.get('filepath')
                container = asset.get('container')
                filetype = asset.get('filetype')
                display_name = asset.get('display_name')
                processed = asset.get('processed')

                assert filetype is not None, f'{path}: {asset}'

                if filetype not in asset_types:
                    asset_types.append(filetype)

                if asset_path_map.get(filetype) is None:
                    asset_path_map.update(
                        {
                            filetype: {
                                'assets': []
                            }
                        }
                    )

                asset_path_map.get(filetype).get('assets').append(
                    {
                        'display_name': display_name,
                        'path': path
                    }
                )

                metadata_cache.append(
                    {
                        'path': path,
                        'filepath': filepath,
                        'container': container,
                        'filetype': filetype,
                        'display_name': display_name,
                        'processed': processed,
                    }
                )

                if lookup_cache.get(filetype) is None:
                    lookup_cache.update({filetype: []})

                lookup_cache[filetype].append(path)

                if unprocessed_asset_counts.get(filetype) is None:
                    unprocessed_asset_counts.update({filetype: 0})

                if processed is False:
                    count = unprocessed_asset_counts.get(filetype)
                    unprocessed_asset_counts.update({filetype: count+1})

                processed_assets = processed_assets + 1
                print(f'Added {path} to metadata caches. ({processed_assets} of {total_assets})')

            print('Saving metadata cache.')
            #deflated_metadata_cache = self.deflate_asset(metadata_cache)
            #self.redis_client.set('metadata_cache', deflated_metadata_cache)
            self.redis_client.set('metadata_cache', json.dumps(metadata_cache))

            print('Saving asset type cache.')
            #deflated_asset_types = self.deflate_asset(asset_types)
            #self.redis_client.set('asset_types', deflated_asset_types)
            self.redis_client.set('asset_types', json.dumps(asset_types))

            print('Saving asset path map cache.')
            #deflated_asset_path_map = self.deflate_asset(asset_path_map)
            #self.redis_client.set('asset_path_map', deflated_asset_path_map)
            self.redis_client.set('asset_path_map', json.dumps(asset_path_map))

            print('Saving lookup cache.')
            #deflated_lookup_cache = self.deflate_asset(lookup_cache)
            #self.redis_client.set('lookup_cache', deflated_lookup_cache)
            self.redis_client.set('lookup_cache', json.dumps(lookup_cache))
            
            print('Saving unprocessed counts.')
            self.redis_client.set('unprocessed_asset_counts', json.dumps(unprocessed_asset_counts))

    def cache_lookup_table(self):
        if self.redis_client.get('lookup_cache') is None:
            self.cache_metadata()

        return self.get_asset_by_path(path='lookup_cache', deflate_data=False)

    def map_asset_file_to_path(self, asset_file):
        asset_cache: dict = self.get_asset_by_path(path='metadata_cache', deflate_data=False)
        
        for asset in asset_cache:
            if asset.get('display_name') == asset_file:
                return asset.get('path')

    def reset_processed_data(self, asset_type_to_reset = None):
        asset_list: list = self.get_asset_list(asset_type_to_reset)
        total_assets: int = len(asset_list)
        processed_assets: int = 0

        for path in asset_list:
            asset = self.get_asset_by_path(path=path, deflate_data=False)
            path: int = asset.get('path')
            processed_assets = processed_assets + 1

            if asset.get('processed') is True:
                if asset_type_to_reset is not None and asset_type_to_reset != asset.get('filetype'):
                    continue
            elif asset.get('processed') is False:
                continue

            self.redis_client.delete(f'{path}_processed_data')
            asset.update({'processed': False})
            self.redis_client.set(path, json.dumps(asset))
            print(f'Reset {path} ({processed_assets} of {total_assets})')

    def get_image_path(self, image_path, lang='en'):
        if image_path == '' or image_path is None:
            return None

        path: Path = Path(image_path)
        filepath_en: list = ['static', 'dqt_images']
        filepath_ja: list = ['static', 'dqt_images']

        for part in path.parts:
            if part in ['en', 'ja']:
                if 'lawson' in path.name.lower():
                    filepath_en.append('ja')
                else:
                    filepath_en.append('en')
                filepath_ja.append('ja')
            elif part == f'{path.stem}{path.suffix}':
                filepath_en.append(part)
                filepath_ja.append(part)
            else:
                filepath_en.append(part.lower())
                filepath_ja.append(part.lower())

        if lang == 'en':
            if Path(*filepath_en).absolute().exists():
                return str(Path(*filepath_en))
        
        return str(Path(*filepath_ja))

    def clean_text_string(self, str_to_clean: str, unit: str):
        str_to_clean = str_to_clean.replace('<unit>', unit)
        str_to_clean = str_to_clean.replace('<addSign>', '+')

        while '<IfSing_' in str_to_clean:
            start_pos: int = str_to_clean.find('<IfSing_')+8
            end_pos: int = str_to_clean.find('(', start_pos)
            data: str = str_to_clean[start_pos:end_pos]
            num = int(re.sub('[a-z]|[A-Z]', '', data))
            choices: list = str_to_clean[end_pos+1:str_to_clean.find(')', end_pos)].split(',')

            if num == 1:
                str_to_clean = str_to_clean.replace(f'<IfSing_{data}({choices[0]},{choices[1]})>', choices[0])
            else:
                str_to_clean = str_to_clean.replace(f'<IfSing_{data}({choices[0]},{choices[1]})>', choices[1])

        return str_to_clean

    def replace_string_variable(self, str_to_clean: str, key: str, value: str):
        str_to_clean = str_to_clean.replace(f'<{key}>', value)

        return str_to_clean
    
    def float_to_str(self, value):
        return str(math.trunc(value)).replace('-', '')