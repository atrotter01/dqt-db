import json
import redis
import zlib

class Util:
    asset_list: list = []
    translation: object
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
        return self.inflate_asset(self.redis_client.get(path))

    def inflate_asset(self, asset):
        return json.loads(zlib.decompress(asset).decode())

    def deflate_asset(self, asset):
        return zlib.compress(json.dumps(asset).encode())

    def save_processed_document(self, path: int, processed_document: dict, display_name: str):
        asset: dict = self.get_asset_by_path(path)
        asset.update({'processed_document': processed_document, 'display_name': display_name, 'processed': True})
        self.redis_client.set(path, self.deflate_asset(asset))

    def save_document(self, path: int, document: dict):
        asset: dict = self.get_asset_by_path(path)
        asset.update({'document': document, 'updated': True})
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

        deflated_asset = self.deflate_asset(unprocessed_asset_counts)
        self.redis_client.set('unprocessed_asset_counts', deflated_asset)

        return unprocessed_asset_counts

    def cache_api_tables(self):
        self.cache_asset_lookup_data()
        self.cache_metadata()

    def cache_metadata(self):
        asset_list: list = self.get_asset_list()
        asset_cache: list = []

        if self.redis_client.get('metadata_cache') is None:
            for path in asset_list:
                asset = self.get_asset_by_path(path)
                filepath = asset.get('filepath')
                container = asset.get('container')
                filetype = asset.get('filetype')
                display_name = asset.get('display_name')
                processed = asset.get('processed')

                print(display_name)

                asset_cache.append(
                    {
                        'path': path,
                        'filepath': filepath,
                        'container': container,
                        'filetype': filetype,
                        'display_name': display_name,
                        'processed': processed,
                    }
                )

            deflated_asset = self.deflate_asset(asset_cache)
            self.redis_client.set('metadata_cache', deflated_asset)

    def cache_asset_lookup_data(self):
        asset_list: list = self.get_asset_list()
        asset_types: list = []
        asset_path_map: dict = {}

        if self.redis_client.get('asset_types') is None\
        or self.redis_client.get('asset_path_map') is None:
            for path in asset_list:
                asset = self.get_asset_by_path(path)
                type = asset.get('filetype')
                display_name = asset.get('display_name')
                print(display_name)

                if type not in asset_types:
                    asset_types.append(type)

                if asset_path_map.get(type) is None:
                    asset_path_map.update(
                        {
                            type: {
                                'assets': []
                            }
                        }
                    )

                asset_path_map.get(type).get('assets').append(
                    {
                        'display_name': display_name,
                        'path': path
                    }
                )

            deflated_asset_types = self.deflate_asset(asset_types)
            self.redis_client.set('asset_types', deflated_asset_types)

            deflated_asset_path_map = self.deflate_asset(asset_path_map)
            self.redis_client.set('asset_path_map', deflated_asset_path_map)

    def cache_lookup_table(self):
        if self.redis_client.get('lookup_cache'):
            return self.get_asset_by_path('lookup_cache')

        lookup_cache: dict = {}

        for path in self.asset_list:
            asset: dict = self.get_asset_by_path(path)
            assert type(asset) is dict, asset

            filetype: str = asset.get('filetype')

            if lookup_cache.get(filetype) is None:
                lookup_cache.update({filetype: []})

            lookup_cache[filetype].append(path)

        deflated_asset = self.deflate_asset(lookup_cache)
        self.redis_client.set('lookup_cache', deflated_asset)

        return lookup_cache
