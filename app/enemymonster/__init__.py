from app.translation import Translation
from app.util import Util

class EnemyMonster:

    assets: list
    util: Util
    translation: Translation

    def __init__(self, _util: Util, _translation: Translation):
        self.util = _util
        self.translation = _translation

        self.assets = []
        self.assets.extend(self.util.get_asset_list('EnemyMonster'))

    def process_assets(self):
        for path in self.assets:
            asset = self.util.get_asset_by_path(path)

            if asset.get('processed_document') is not None:
                continue

            print(f'Processing {path}')

            document: dict = self.util.parse_asset(path=path)
            assert type(document) is dict, document

            translated_document: dict = self.translation.translate_dict(document)
            assert type(translated_document) is dict, translated_document

            display_name: str = translated_document.get('profile').get('displayName')

            assert type(display_name) is str, translated_document
            assert display_name != '', translated_document

            print(f'Saving {display_name}')
            self.util.save_processed_document(path=path, processed_document=translated_document, display_name=display_name)
