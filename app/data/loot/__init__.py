from app.util import Util
from app.data import DataProcessor

class Loot:

    assets: list
    util: Util
    data_processor: DataProcessor

    def __init__(self, _util: Util, _data_processor: DataProcessor):
        self.util = _util
        self.data_processor = _data_processor

        self.assets = []
        self.assets.extend(self.util.get_asset_list('LootItemGroup'))
        self.assets.extend(self.util.get_asset_list('LootitemGroup'))
        self.assets.extend(self.util.get_asset_list('LootLottery'))

    def process_assets(self):
        for path in self.assets:
            try:
                asset = self.util.get_asset_by_path(path=path, deflate_data=True)

                if asset.get('processed_document') is not None:
                    continue

                print(f'Processing {path}')

                document: dict = self.data_processor.parse_asset(path=path)
                assert type(document) is dict, document

                display_name: str = document.get('m_Name')

                assert type(display_name) is str, document
                assert display_name != '', document

                print(f'Saving {display_name}')
                self.util.save_processed_document(path=path, processed_document=document, display_name=display_name)
            except TypeError as ex:
                print(f'Failed to process with type error {path} {ex}')
                continue
            except AssertionError as ex:
                print(f'Failed to process with assertion error {path} {ex}')
                continue