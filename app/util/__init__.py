import os
import json
from pathlib import Path
import networkx as nx
import redis
import zlib
from copy import deepcopy

class Util:
    asset_list: list = []
    translation: object
    graph: nx.Graph
    redis_client: redis
    lookup_cache: dict = {}
    possible_circular_references: list = []

    def __init__(self):
        self.graph = nx.Graph()
        self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=False)
        self.asset_list = self.build_asset_list()
        self.lookup_cache = self.build_lookup_cache()

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

    def build_lookup_cache(self):
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

    def inflate_asset(self, asset):
        return json.loads(zlib.decompress(asset).decode())

    def deflate_asset(self, asset):
        return zlib.compress(json.dumps(asset).encode())

    def get_asset_by_path(self, path: int):
        return self.inflate_asset(self.redis_client.get(path))

#    def get_processed_keys(self, asset_type: str = None):
#        connection_string = self.get_database_connection_string()
#        path_list: list = []

#        with psycopg.connect(conninfo=connection_string, row_factory=dict_row) as conn:
#            query: str = None
#            cursor: object = conn.cursor()
            
#            if asset_type is None:
#                query = 'select path from public.assets'
#                cursor.execute(query)
#            else:
#                query = 'select path from public.assets where filetype = %s'
#                cursor.execute(query, (asset_type,))

#            for row in cursor.fetchall():
#                path_list.append(row.get('path'))

#        return path_list

    def process_dict(self, dictionary: dict, parent_path: int, key_stack: str = ''):
        dictionary_copy: dict = deepcopy(dictionary)
        #print(key_stack)

        for key in dictionary.keys():
            item = dictionary.get(key)

            if key == 'timelineOverrideMasterData'\
            or key == 'timeline'\
            or key == 'affectionTimeline'\
            or key == 'curseUnbindingTimeline'\
            or key == 'givingTimeline'\
            or key == 'removingTimeline'\
            or key == 'resistTimeline'\
            or key == 'removeTimeline'\
            or key == 'shortTimeline'\
            or key == 'prerequisiteStages'\
            or key_stack == 'root.area.areaExpansion.difficultySettings.area'\
            or key_stack == 'root.area.areaExpansion.stageSettings.stage.area'\
            or key_stack == 'root.areaExpansion.difficultySettings.area.areaExpansion'\
            or key_stack == 'root.areaExpansion.stageSettings.stage.area.areaExpansion':
                #dictionary_copy.update({key: {'Omitted': True}})
                continue

            if type(item) is dict:
                if 'm_PathID' in item.keys():
                    path: int = item.get('m_PathID')
                    assert type(path) is int, path

                    if path != 0 and key != 'm_Script':
                        try:
                            recursive_document: dict = self.get_document(path=path, parent_path=parent_path, key_stack=f'{key_stack}.{key}')
                            assert type(recursive_document) is dict, recursive_document

                            dictionary_copy.update({key: recursive_document})
                        except RecursionError as ex:
                            print(f'Recursion Error 1: {path}')
                            print(key_stack)
                            raise ex
                    else:
                        continue
                else:
                    continue

            elif type(item) is list:
                exploded_list: list = []

                for element in item:
                    if type(element) is dict:
                        if 'm_PathID' in element.keys():
                            element_path: int = element.get('m_PathID')
                            assert type(element_path) is int, element_path

                            if element_path != 0:
                                try:
                                    recursive_document: dict = self.get_document(path=element_path, parent_path=parent_path, key_stack=f'{key_stack}.{key}')
                                    assert type(recursive_document) is dict, type(recursive_document)

                                    exploded_list.append(recursive_document)
                                except RecursionError as ex:
                                    print(f'Recursion Error 2: {path}')
                                    raise ex
                            else:
                                exploded_list.append(element)
                        else:
                            try:
                                processed_dict: dict = self.process_dict(dictionary=element, parent_path=parent_path, key_stack=f'{key_stack}.{key}')
                                assert type(processed_dict) is dict, type(processed_dict)

                                exploded_list.append(processed_dict)
                            except RecursionError as ex:
                                print(f'Recursion Error 3: {path}')
                                raise ex
                    else:
                        exploded_list.append(element)

                dictionary_copy.update({key: exploded_list})

        return dictionary_copy

    def get_document(self, path: int, parent_path: int = None, key_stack: str = None):
        circular_reference_check: dict = self.check_circular_references(path=path, parent_path=parent_path)

        if circular_reference_check is not None:
            return circular_reference_check

        asset: dict = self.get_asset_by_path(path)
        assert type(asset) is dict, path

        document: dict = asset.get('document')
        assert type(document) is dict, document

        if asset.get('processed_document') is not None:
            return asset.get('processed_document')

        processed_dict: dict = self.process_dict(dictionary=document, parent_path=path, key_stack=key_stack)
        assert type(processed_dict) is dict, path

        return processed_dict

    def parse_asset(self, path: int):
        self.graph.clear()
        self.possible_circular_references = []

        document: dict = self.get_document(path=path, key_stack='root')
        assert type(document) is dict, document

        return document

    def check_circular_references(self, path: int, parent_path: int):
        if parent_path is not None:
            connected_edge_sets = list(nx.connected_components(self.graph))

            for connected_edge in connected_edge_sets:
                if path in connected_edge and parent_path in connected_edge:
                    combination_key: str = f'{path}:{parent_path}'
                    opposing_combination_key: str = f'{parent_path}:{path}'

                    if combination_key in self.possible_circular_references or opposing_combination_key in self.possible_circular_references:
                        if opposing_combination_key in self.possible_circular_references:
                            return {'CircularReference': True}
                    else:
                        self.possible_circular_references.append(combination_key)

        self.graph.add_node(path)

        if parent_path is not None:
            self.graph.add_edge(path, parent_path)

        return

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

#    def save_document(self, asset_id: int, document: dict):
#        connection_string = self.get_database_connection_string()

#        with psycopg.connect(conninfo=connection_string) as conn:
#            query: str = 'update public.assets set document=%s where id=%s'
#            cursor: object = conn.cursor()
#            cursor.execute(query, (json.dumps(document), asset_id))
