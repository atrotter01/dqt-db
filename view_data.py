import sys
import json
import zlib
from app.util import Util
from pprint import pprint

util = Util()
#asset_list: list = util.get_asset_list('Stage')
asset: dict = util.get_asset_by_path('5891531898241754695', deflate_data=True)
#print(asset.keys())
print(asset.get('document'))
#print(asset.get('processed_document'))
#total_assets: int = len(asset_list)
#asset_count: int = 0

#for path in asset_list:
    #asset = util.get_asset_by_path(path, deflate_data=True)
    #path: int = asset.get('path')
    #pprint(asset)
    #asset_count = asset_count + 1
    #document = asset.get('processed_document')

    #print(document)
    #print(document.get('displayName'))

    #print(f'{path}: ({asset_count} of {total_assets})')