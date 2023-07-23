from copy import deepcopy
import networkx as nx
from app.util import Util
from pathlib import Path

class DataProcessor:

    graph: nx.Graph
    translation_jp: dict
    translation_noun_jp: dict
    translation_gbl: dict
    translation_noun_gbl: dict
    util: Util

    def __init__(self, _util: Util):
        self.graph = nx.Graph()
        self.util = _util
        self.translation_jp = self.build_translation('Translation')
        self.translation_noun_jp = self.build_translation_noun('TranslationNoun')
        self.translation_gbl = self.build_translation('TranslationGbl')
        self.translation_noun_gbl = self.build_translation_noun('TranslationNounGbl')

    def build_translation(self, key):
        translation_data: dict = {}

        asset: dict = self.util.get_asset_by_path(path=self.util.get_asset_list(key)[0], deflate_data=True)
        document: dict = asset.get('document')
        assert isinstance(document, dict), document

        for record in document.get('rawData'):
            key: str = record.get('key')
            value: str = record.get('value')
            assert isinstance(key, str), key
            assert isinstance(value, str), value

            translation_data.update({key: value})

        return translation_data

    def build_translation_noun(self, key):
        translation_noun_data: dict = {}

        asset: dict = self.util.get_asset_by_path(self.util.get_asset_list(key)[0], deflate_data=True)
        document: dict = asset.get('document')
        assert isinstance(document, dict), document

        for record in document.get('nouns'):
            key: str = record.get('key')
            assert isinstance(key, str), key
            assert isinstance(record, dict), record

            translation_noun_data.update({key: record})

        return translation_noun_data

    def get_translation(self, key: str):
        if self.translation_gbl.get(key) is not None:
            return self.translation_gbl.get(key)

        return self.translation_jp.get(key)

    def get_translation_noun(self, key: str):
        if self.translation_noun_gbl.get(key) is not None:
            return self.translation_noun_gbl.get(key)

        return self.translation_noun_jp.get(key)

    def get_translated_string(self, key: str):
        translated_string: str = None

        if self.get_translation(key) is not None:
            translated_string = self.get_translation(key)
        elif self.get_translation_noun(key) is not None:
            translated_string = self.get_translation_noun(key)
        else:
            translated_string = key

        return translated_string

    def process_dict(self, dictionary: dict, parent_path: int, key_stack: str = ''):
        dictionary_copy: dict = deepcopy(dictionary)
        #print(key_stack)

        for key in dictionary.keys():
            item = dictionary.get(key)

            if key == 'timeline'\
            or key == 'affectionTimeline'\
            or key == 'curseUnbindingTimeline'\
            or key == 'givingTimeline'\
            or key == 'removingTimeline'\
            or key == 'resistTimeline'\
            or key == 'removeTimeline'\
            or key == 'shortTimeline'\
            or key == 'prerequisiteStages'\
            or key == 'ghostNpcList'\
            or 'MasterData' in key\
            or 'root.m_Parent' in key_stack\
            or 'MasterData' in key_stack\
            or ('areaExpansion.difficultySettings' in key_stack and key == 'area')\
            or ('areaExpansion.stageSettings' in key_stack and key == 'area')\
            or ('root.difficultySettings' in key_stack and key == 'area')\
            or ('root.stageSettings' in key_stack and key == 'area')\
            or ('instructionSet.action.operationData' in key_stack and key == 'instructionSet')\
            or ('m_Children' in key_stack and key == 'm_Parent')\
            or ('m_Children.m_Clips' in key_stack and key == 'm_ParentTrack')\
            or ('root.m_Clips' in key_stack and key == 'm_ParentTrack')\
            or ('root.friendlyGestures' in key_stack and key == 'friendlyGestures'):

                #dictionary_copy.update({key: {'Omitted': True}})
                #print(f'Skipping {key} in stack {key_stack}')
                continue

            if type(item) is dict:
                if 'm_PathID' in item.keys():
                    path: int = item.get('m_PathID')
                    assert isinstance(path, int), path

                    if path != 0 and key != 'm_Script':
                        try:
                            recursive_document: dict = self.get_document(path=path, parent_path=parent_path, key_stack=f'{key_stack}.{key}')
                            assert isinstance(recursive_document, dict), recursive_document

                            dictionary_copy.update({key: recursive_document})
                        except RecursionError as ex:
                            print(f'Recursion Error 1: {path}')
                            print(key_stack)
                            raise ex
                    else:
                        continue
                else:
                    processed_dict: dict = self.process_dict(dictionary=item, parent_path=parent_path, key_stack=f'{key_stack}.{key}')
                    assert isinstance(processed_dict, dict), type(processed_dict)

                    dictionary_copy.update({key: processed_dict})

            elif type(item) is list:
                exploded_list: list = []

                for element in item:
                    if type(element) is dict:
                        if 'm_PathID' in element.keys():
                            element_path: int = element.get('m_PathID')
                            assert isinstance(element_path, int), element_path

                            if element_path != 0:
                                try:
                                    recursive_document: dict = self.get_document(path=element_path, parent_path=parent_path, key_stack=f'{key_stack}.{key}')
                                    assert isinstance(recursive_document, dict), type(recursive_document)

                                    exploded_list.append(recursive_document)
                                except RecursionError as ex:
                                    print(f'Recursion Error 2: {element_path}')
                                    raise ex
                            else:
                                exploded_list.append(element)
                        else:
                            try:
                                processed_dict: dict = self.process_dict(dictionary=element, parent_path=parent_path, key_stack=f'{key_stack}.{key}')
                                assert isinstance(processed_dict, dict), type(processed_dict)

                                exploded_list.append(processed_dict)
                            except RecursionError as ex:
                                print(f'Recursion Error 3: {path}')
                                raise ex
                    else:
                        exploded_list.append(element)

                dictionary_copy.update({key: exploded_list})

            elif type(item) is str:
                translated_string: str = self.get_translated_string(item)

                if item != translated_string and item is not None:
                    dictionary_copy.update({key: translated_string})
                elif item.lower().endswith('.asset'):
                    asset_path_object = Path(item)
                    asset_filename: str = asset_path_object.name.replace('.asset', '')

                    asset_path = self.util.map_asset_file_to_path(asset_filename)
                    recursive_document: dict = self.get_document(path=asset_path, parent_path=parent_path, key_stack=f'{key_stack}.{key}')

                    dictionary_copy.update({key: recursive_document})

        return dictionary_copy

    def get_document(self, path: int, parent_path: int = None, key_stack: str = None):
        circular_reference_check: dict = self.check_circular_references(path=path, parent_path=parent_path)

        if circular_reference_check is not None:
            return circular_reference_check

        try:
            asset: dict = self.util.get_asset_by_path(path=path, deflate_data=True)

            if asset is None:
                return {
                    'MissingData': True
                }

            assert isinstance(asset, dict), f'Path: {path}, Parent Path: {parent_path}'

            document: dict = asset.get('document')
            assert isinstance(document, dict), f'Document Error: {document}'

            if asset.get('processed_document') is not None:
                return asset.get('processed_document')

            processed_dict: dict = self.process_dict(dictionary=document, parent_path=path, key_stack=key_stack)
            assert isinstance(processed_dict, dict), f'Processed Dict Error: {path}'

            return processed_dict
        except TypeError as ex:
            print(f'Failed to fetch a document for path {path} via {parent_path} {ex}')
            raise ex

    def parse_asset(self, path: int):
        self.graph.clear()
        self.possible_circular_references = []

        document: dict = self.get_document(path=path, key_stack='root')
        assert isinstance(document, dict), document

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
