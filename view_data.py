from app.util import Util
from pprint import pprint

util = Util()
asset_list: list = util.get_asset_list(asset_type='MonsterProfile')
asset_list = [2374582551451606286]

for path in asset_list:
    asset = util.get_asset_by_path(path)
    path: int = asset.get('path')
    document = asset.get('processed_document')

    print(document)
    print(type(document))
