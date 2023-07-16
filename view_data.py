from app.util import Util
from pprint import pprint

util = Util()
asset_list: list = util.get_asset_list(asset_type='LootItemGroup')

for path in asset_list:
    asset = util.get_asset_by_path(path)
    path: int = asset.get('path')
    document = asset.get('document')

    print(document)
    print(document.get('displayName'))