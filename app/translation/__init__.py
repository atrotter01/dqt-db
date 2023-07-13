from app.util import Util

class Translation():

    translation: dict
    translation_noun: dict
    util: Util
    translation_cache: dict = {}

    def __init__(self, util: Util):
        self.util = util
        self.translation = self.build_translation()
        self.translation_noun = self.build_translation_noun()

    def build_translation(self):
        translation_data: dict = {}

        asset: dict = self.util.get_asset_by_path(self.util.get_asset_list('Translation')[0])
        document: dict = asset.get('document')
        assert type(document) is dict, document

        for record in document.get('rawData'):
            key: str = record.get('key')
            value: str = record.get('value')
            assert type(key) is str, key
            assert type(value) is str, value

            translation_data.update({key: value})

        return translation_data

    def build_translation_noun(self):
        translation_noun_data: dict = {}

        asset: dict = self.util.get_asset_by_path(self.util.get_asset_list('TranslationNoun')[0])
        document: dict = asset.get('document')
        assert type(document) is dict, document

        for record in document.get('nouns'):
            key: str = record.get('key')
            assert type(key) is str, key
            assert type(record) is dict, record

            translation_noun_data.update({key: record})

        return translation_noun_data

    def get_translation(self, key: str):
        translated_string: str = self.translation.get(key)
        assert type(translated_string) is str, translated_string
        return translated_string

    def get_translation_noun(self, key: str):
        translated_noun: str = self.translation_noun.get(key)
        assert type(translated_noun) is str, translated_noun
        return translated_noun

    def translate_dict(self, dictionary: dict):
        for key in dictionary.keys():
            item = dictionary.get(key)

            if type(item) is dict:
                try:
                    translated_dict: dict = self.translate_dict(dictionary=item)
                    assert type(translated_dict) is dict, translated_dict
                    dictionary.update({key: translated_dict})
                except RecursionError as ex:
                    raise ex

            elif type(item) is list:
                exploded_list: list = []

                for element in item:
                    if type(element) is dict:
                        translated_dict = self.translate_dict(dictionary=element)
                        assert type(translated_dict) is dict, translated_dict
                        exploded_list.append(translated_dict)
                    else:
                        if element in self.translation:
                            translated_string: str = self.translation.get(element)
                            assert type(translated_string) is str, translated_string
                            exploded_list.append(translated_string)

                        elif element in self.translation_noun:
                            translated_noun: str = self.translation_noun.get(element)
                            assert type(translated_noun) is str, translated_noun
                            exploded_list.append(translated_noun)

                        else:
                            exploded_list.append(element)

                dictionary.update({key: exploded_list})

            else:
                if item in self.translation:
                    translated_string: str = self.translation.get(item)
                    assert type(translated_string) is str, translated_string
                    dictionary.update({key: translated_string})

                elif item in self.translation_noun:
                    translated_noun: str = self.translation_noun.get(item)
                    assert type(translated_noun) is str, translated_noun
                    dictionary.update({key: translated_noun})

        assert type(dictionary) is dict, dictionary
        return dictionary
