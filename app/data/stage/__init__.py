from app.translation import Translation
from app.util import Util
from app.data import DataProcessor

class Stage:

    assets: list
    util: Util
    translation: Translation
    data_processor: DataProcessor

    def __init__(self, _util: Util, _translation: Translation, _data_processor: DataProcessor):
        self.util = _util
        self.translation = _translation
        self.data_processor = _data_processor
        self.assets = []
        self.assets.extend(self.util.get_asset_list('Stage'))

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

                achievement_target_name: str = translated_document.get('area').get('achievementTarget').get('displayName')
                area_group_name: str = translated_document.get('area').get('areaGroup').get('displayName')
                area_name: str = translated_document.get('area').get('displayName')
                stage_name: str = translated_document.get('displayName')

                display_name: str = None

                if achievement_target_name is not None and area_group_name is not None:
                    display_name = f'{achievement_target_name} - {area_group_name} - {area_name} - {stage_name}'
                elif area_group_name is not None:
                    display_name = f'{area_group_name} - {area_name} - {stage_name}'
                elif achievement_target_name is not None:
                    display_name = f'{achievement_target_name} - {area_name} - {stage_name}'
                else:
                    display_name = f'{area_name} - {stage_name}'

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
