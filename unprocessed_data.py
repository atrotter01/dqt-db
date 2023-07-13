from app.util import Util
from pprint import pprint

util = Util()

unprocessed_asset_counts: dict = util.get_unprocessed_assets(skip_cache=True)

for asset_type in sorted(unprocessed_asset_counts):
    unprocessed_count = unprocessed_asset_counts.get(asset_type)

    if unprocessed_count > 0:
        print(f'{asset_type}: {unprocessed_count}')
