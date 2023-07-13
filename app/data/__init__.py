from copy import deepcopy
import networkx as nx
from app.util import Util

class DataProcessor:

    graph: nx.Graph
    util: Util

    def __init__(self, _util: Util):
        self.graph = nx.Graph()
        self.util = _util

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
            or key_stack.startswith('root.area.areaExpansion.difficultySettings.area')\
            or key_stack.startswith('root.area.areaExpansion.stageSettings.stage.area')\
            or key_stack.startswith('root.areaExpansion.difficultySettings.area.areaExpansion')\
            or key_stack.startswith('root.areaExpansion.stageSettings.stage.area.areaExpansion')\
            or key_stack.startswith('root.difficultySettings.area.areaExpansion.difficultySettings')\
            or key_stack.startswith('root.difficultySettings.area.areaExpansion.stageSettings')\
            or key_stack.startswith('root.stageSettings.stage.area.areaExpansion.difficultySettings')\
            or key_stack.startswith('root.stageSettings.stage.area.areaExpansion.stageSettings'):
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

        asset: dict = self.util.get_asset_by_path(path)
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
