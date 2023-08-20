from copy import deepcopy
from app.util import Util
from pathlib import Path

class DataProcessor:

    translation_ja: dict
    translation_noun_ja: dict
    translation_gbl: dict
    translation_noun_gbl: dict
    util: Util

    def __init__(self, _util: Util):
        self.util = _util
        self.translation_ja = self.build_translation('Translation')
        self.translation_noun_ja = self.build_translation_noun('TranslationNoun')
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
        translations: dict = {}

        gbl: str = self.translation_gbl.get(key)
        ja: str = self.translation_ja.get(key)

        if gbl is None and ja is None:
            return None

        translations.update({
            'gbl': gbl,
            'ja': ja
        })

        return translations

    def get_translation_noun(self, key: str):
        translations: dict = {}

        gbl: str = self.translation_noun_gbl.get(key)
        ja: str = self.translation_noun_ja.get(key)

        if gbl is None and ja is None:
            return None

        translations.update({
            'gbl': gbl,
            'ja': ja
        })

        return translations

    def get_translated_string(self, key: str):
        if self.get_translation(key) is not None:
            return self.get_translation(key)
        elif self.get_translation_noun(key) is not None:
            return self.get_translation_noun(key)

        return None

    def process_dict(self, dictionary: dict, parent_path: str, path_stack: list, key_stack: str = ''):
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
            or 'MasterData' in key_stack\
            or ('instructionSet' in key_stack and key == 'operationData'):

                #dictionary_copy.update({key: {'Omitted': True}})
                #print(f'Skipping {key} in stack {key_stack}')
                continue

            if type(item) is dict:
                if 'm_PathID' in item.keys():
                    path: str = str(item.get('m_PathID'))
                    assert isinstance(path, str), path

                    if path != '0' and key != 'm_Script':
                        try:
                            stack_copy: list = deepcopy(path_stack)
                            stack_copy.append(path)

                            if self.test_cycle(stack_copy):
                                continue

                            recursive_document: dict = self.get_document(path=path, parent_path=parent_path, key_stack=f'{key_stack}.{key}', path_stack=stack_copy)
                            assert isinstance(recursive_document, dict), recursive_document

                            dictionary_copy.update({key: recursive_document})
                        except RecursionError as ex:
                            print(f'Recursion Error 1: {path}')
                            print(key_stack)
                            raise ex
                    else:
                        continue
                else:
                    processed_dict: dict = self.process_dict(dictionary=item, parent_path=parent_path, key_stack=f'{key_stack}.{key}', path_stack=path_stack)
                    assert isinstance(processed_dict, dict), type(processed_dict)

                    dictionary_copy.update({key: processed_dict})

            elif type(item) is list:
                exploded_list: list = []

                for element in item:
                    if type(element) is dict:
                        if 'm_PathID' in element.keys():
                            element_path: str = str(element.get('m_PathID'))
                            assert isinstance(element_path, str), element_path

                            if element_path != '0':
                                try:
                                    stack_copy: list = deepcopy(path_stack)
                                    stack_copy.append(element_path)

                                    if self.test_cycle(stack_copy):
                                        continue

                                    recursive_document: dict = self.get_document(path=element_path, parent_path=parent_path, key_stack=f'{key_stack}.{key}', path_stack=stack_copy)
                                    assert isinstance(recursive_document, dict), type(recursive_document)

                                    exploded_list.append(recursive_document)
                                except RecursionError as ex:
                                    print(f'Recursion Error 2: {element_path}')
                                    raise ex
                            else:
                                exploded_list.append(element)
                        else:
                            try:
                                processed_dict: dict = self.process_dict(dictionary=element, parent_path=parent_path, key_stack=f'{key_stack}.{key}', path_stack=path_stack)
                                assert isinstance(processed_dict, dict), type(processed_dict)

                                exploded_list.append(processed_dict)
                            except RecursionError as ex:
                                print(f'Recursion Error 3: {path}')
                                raise ex
                    else:
                        exploded_list.append(element)

                dictionary_copy.update({key: exploded_list})

            elif type(item) is str:
                translations: dict = self.get_translated_string(item)

                if translations is not None:
                    dictionary_copy.update({f'{key}_translation': translations})

                if item.lower().endswith('.asset'):
                    asset_path_object = Path(item)
                    asset_filename: str = asset_path_object.name.replace('.asset', '')

                    asset_path = self.util.map_asset_file_to_path(asset_filename)
                    recursive_document: dict = self.get_document(path=asset_path, parent_path=parent_path, key_stack=f'{key_stack}.{key}')

                    dictionary_copy.update({key: recursive_document})

        return dictionary_copy

    def get_document(self, path: str, parent_path: str = None, key_stack: str = None, path_stack: list = [], force_rebuild: bool = False):
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
                if force_rebuild is False:
                    return asset.get('processed_document')

            processed_dict: dict = self.process_dict(dictionary=document, parent_path=path, key_stack=key_stack, path_stack=path_stack)
            processed_dict.update({'linked_asset_id': str(path)})
            assert isinstance(processed_dict, dict), f'Processed Dict Error: {path}'

            if parent_path is not None:
                print(f'Saving processed document for {path}.')
                self.util.save_processed_document(path=path, processed_document=processed_dict, display_name=None, set_processed_flag=True)

            return processed_dict
        except TypeError as ex:
            print(f'Failed to fetch a document for path {path} via {parent_path} {ex}')
            raise ex

    def parse_asset(self, path: str, force_rebuild: bool = False):
        document: dict = self.get_document(path=path, key_stack='root', path_stack=[path], force_rebuild=force_rebuild)
        assert isinstance(document, dict), document

        return document

    def test_cycle(self, assets: list):
        linked_list: LinkedList = LinkedList()

        for asset in assets:
            linked_list.push(asset)

        return linked_list.detectLoop()

class Node:
    data: str
    next: str

    def __init__(self, data: str):
        self.data = data
        self.next = None
  
class LinkedList:
    head: Node

    def __init__(self):
        self.head = None
 
    def push(self, new_data: str):
        new_node: Node = Node(new_data)
        new_node.next = self.head
        self.head = new_node

    def detectLoop(self):
        slow_p: Node = self.head
        fast_p: Node = self.head

        while(slow_p and fast_p and fast_p.next):
            slow_p: Node = slow_p.next
            fast_p: Node = fast_p.next.next

            if slow_p is not None and fast_p is not None:
                if slow_p.data == fast_p.data:
                    return True

        return False
