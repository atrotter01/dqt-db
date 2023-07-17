import json
import redis
import brotli
from pathlib import Path

class Util:
    asset_list: list = []
    cache_keys: list = ['asset_path_map', 'asset_types', 'lookup_cache', 'metadata_cache']
    redis_client: redis
    lookup_cache: dict = {}
    possible_circular_references: list = []

    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=False)
        self.asset_list = self.build_asset_list()
        self.lookup_cache = self.cache_lookup_table()

    def build_asset_list(self):
        return [key.decode() for key in self.redis_client.keys()]

    def get_asset_list(self, asset_type: str = None):

        if asset_type is None:
            asset_list: list = []

            for key in self.lookup_cache.keys():
                asset_list.extend(self.lookup_cache.get(key))

            return asset_list
        else:
            return self.lookup_cache.get(asset_type)

    def get_asset_by_path(self, path: int):
        asset = self.redis_client.get(path)
        
        if asset is None:
            return None
        
        return self.inflate_asset(asset)

    def inflate_asset(self, asset):
        return json.loads(brotli.decompress(asset).decode())

    def deflate_asset(self, asset):
        return brotli.compress(json.dumps(asset).encode())

    def save_processed_document(self, path: int, processed_document: dict, display_name: str):
        asset: dict = self.get_asset_by_path(path)
        asset.update({'processed_document': processed_document, 'display_name': display_name, 'processed': True})
        self.redis_client.set(path, self.deflate_asset(asset))

    def save_asset(self, path: int, filepath: str, container: str, filetype: str, document: dict):
        asset: dict = {
            'path': path,
            'filepath': filepath,
            'container': container,
            'filetype': filetype,
            'document': document,
            'display_name': None,
            'processed_document': None,
            'processed': False
        }

        return self.redis_client.set(path, self.deflate_asset(asset))

    def get_unprocessed_assets(self):
        unprocessed_asset_counts: dict = {}
        asset_list: list = self.get_asset_by_path('metadata_cache')

        for asset in asset_list:
            type = asset.get('filetype')

            if unprocessed_asset_counts.get(type) is None:
                unprocessed_asset_counts.update({type: 0})

            count = unprocessed_asset_counts.get(type)

            if asset.get('processed') is False:
                unprocessed_asset_counts.update({type: count+1})

        return unprocessed_asset_counts

    def cache_api_tables(self):
        self.cache_metadata()

    def cache_metadata(self):
        asset_list: list = self.asset_list
        metadata_cache: list = []
        asset_types: list = []
        asset_path_map: dict = {}
        lookup_cache: dict = {}
        total_assets: int = len(self.asset_list)
        processed_assets: int = 0

        if self.redis_client.get('metadata_cache') is None\
        or self.redis_client.get('asset_types') is None\
        or self.redis_client.get('asset_path_map') is None\
        or self.redis_client.get('lookup_cache') is None:
            for path in asset_list:
                if path in self.cache_keys:
                    continue

                asset = self.get_asset_by_path(path)
                filepath = asset.get('filepath')
                container = asset.get('container')
                filetype = asset.get('filetype')
                display_name = asset.get('display_name')
                processed = asset.get('processed')

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

                processed_assets = processed_assets + 1
                print(f'Added {path} to metadata caches. ({processed_assets} of {total_assets})')

            print('Saving metadata cache.')
            deflated_metadata_cache = self.deflate_asset(metadata_cache)
            self.redis_client.set('metadata_cache', deflated_metadata_cache)

            print('Saving asset type cache.')
            deflated_asset_types = self.deflate_asset(asset_types)
            self.redis_client.set('asset_types', deflated_asset_types)

            print('Saving asset path map cache.')
            deflated_asset_path_map = self.deflate_asset(asset_path_map)
            self.redis_client.set('asset_path_map', deflated_asset_path_map)

            print('Saving lookup cache.')
            deflated_lookup_cache = self.deflate_asset(lookup_cache)
            self.redis_client.set('lookup_cache', deflated_lookup_cache)

    def cache_lookup_table(self):
        if self.redis_client.get('lookup_cache') is None:
            self.cache_metadata()

        return self.get_asset_by_path('lookup_cache')

    def map_asset_file_to_path(self, asset_file):
        asset_cache: dict = self.get_asset_by_path('metadata_cache')
        
        for asset in asset_cache:
            filepath: str = asset.get('filepath')
            path_object: Path = Path(filepath)
            filename = path_object.stem

            if filename == asset_file:
                return asset.get('path')

    def reset_processed_document(self, path: int):
        asset: dict = self.get_asset_by_path(path)
        asset.update({'processed_document': None, 'display_name': None, 'processed': False})
        self.redis_client.set(path, self.deflate_asset(asset))

    def reset_processed_data(self, asset_type_to_reset = None):
        metadata_cache: dict = self.get_asset_by_path('metadata_cache')
        total_assets: int = len(metadata_cache)
        processed_assets: int = 0

        for asset in metadata_cache:
            path: int = asset.get('path')
            processed_assets = processed_assets + 1

            if asset.get('processed') is True:
                if asset_type_to_reset is not None and asset_type_to_reset != asset.get('filetype'):
                    continue
                
                self.reset_processed_document(path=path)
                print(f'Reset {path} ({processed_assets} of {total_assets})')

    def clear_caches(self):

        for key in self.cache_keys:
            self.redis_client.delete(key)
