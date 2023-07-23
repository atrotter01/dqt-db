from app.util import Util

util = Util()

unprocessed_asset_counts: dict = util.get_unprocessed_assets()

for asset_type in sorted(unprocessed_asset_counts):
    unprocessed_count = unprocessed_asset_counts.get(asset_type)

    if unprocessed_count > 0:
        if not asset_type.endswith('MasterDataStoreSource'):
            print(f'{asset_type}: {unprocessed_count}')
