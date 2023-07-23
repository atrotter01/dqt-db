import sys
import json
import zlib
from app.util import Util
from pprint import pprint

util = Util()
asset_list: list = util.get_asset_list('EventPortal')

for path in asset_list:
    asset = util.get_asset_by_path(path, deflate_data=True)
    banner_path: str = asset.get('document').get('bannerPath')
    display_name: str = asset.get('display_name')
    print(display_name)
    #path: int = asset.get('path')
    #pprint(asset)
    #asset_count = asset_count + 1
    #document = asset.get('processed_document')

    #print(document)
    #print(document.get('displayName'))

    #print(f'{path}: ({asset_count} of {total_assets})')