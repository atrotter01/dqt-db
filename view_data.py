import sys
import json
import zlib
from app.util import Util
from pprint import pprint

util = Util()
asset_list: list = util.get_asset_list(asset_type='Stage')

for path in asset_list:
    asset = util.get_asset_by_path(path)
    path: int = asset.get('path')
    document = asset.get('processed_document')

    #print(document)
    #print(document.get('displayName'))
    print('---------------------')
    print(path)
    print('---------------------')
    print(sys.getsizeof(str(document)))
    print(sys.getsizeof(zlib.compress(json.dumps(document).encode())))
    print(sys.getsizeof(zlib.compress(json.dumps(document).encode(), level=9)))
    print('')