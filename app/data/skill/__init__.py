from app.translation import Translation
from app.util import Util
from app.data import DataProcessor

class Skill:

    assets: list
    util: Util
    translation: Translation
    data_processor: DataProcessor

    def __init__(self, _util: Util, _translation: Translation):
        self.util = _util
        self.translation = _translation
        self.data_processor = DataProcessor()

        self.assets = []
        self.assets.extend(self.util.get_asset_list('ActiveSkill'))
        self.assets.extend(self.util.get_asset_list('EnemySkill'))
        self.assets.extend(self.util.get_asset_list('GuestSkill'))
        self.assets.extend(self.util.get_asset_list('NotUsePassiveSkill'))
        self.assets.extend(self.util.get_asset_list('NotUseSkill'))
        self.assets.extend(self.util.get_asset_list('PassiveSkill'))
        self.assets.extend(self.util.get_asset_list('ReactionPassiveSkill'))
        self.assets.extend(self.util.get_asset_list('ReactionSkill'))

    def process_assets(self):
        for path in self.assets:
            try:
                asset = self.util.get_asset_by_path(path)

                if asset.get('processed_document') is not None:
                    continue

                print(f'Processing {path}')

                document: dict = self.data_processor.parse_asset(path=path)
                assert type(document) is dict, document

                translated_document: dict = self.translation.translate_dict(document)
                assert type(translated_document) is dict, translated_document

                display_name: str = translated_document.get('displayName')

                if display_name == '':
                    display_name = translated_document.get('m_Name')

                assert type(display_name) is str, translated_document
                assert display_name != '', translated_document

                print(f'Saving {display_name}')
                self.util.save_processed_document(path=path, processed_document=translated_document, display_name=display_name)
            except TypeError as ex:
                print(f'Failed to process with type error {path} {ex}')
                continue
            except AssertionError as ex:
                print(f'Failed to process with assertion error {path} {ex}')
                continue
