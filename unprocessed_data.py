from app.util import Util
from pprint import pprint

util = Util()

asset_list: list = util.get_asset_list()
counts: dict = {}

for path in asset_list:
    asset = util.get_asset_by_path(path)
    type = asset.get('filetype')

    if counts.get(type) is None:
        counts.update({type: 0})

    count = counts.get(type)

    if asset.get('processed') is False:
        counts.update({type: count+1})

pprint(counts)
