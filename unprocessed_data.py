from app.util import Util

util = Util()

unprocessed_containers: dict = util.get_uncached_assets_by_container(processed_filter=False)

for container in sorted(unprocessed_containers):
    if 'aiming' not in container:
        continue

    if 'prefab' in container:
        continue

    if 'masterdata' not in container:
        continue

    asset_types = unprocessed_containers.get(container)

    for asset_type in sorted(asset_types):
        if 'MasterData' in asset_type:
            continue

        print(f'{container}: {asset_type}: {len(unprocessed_containers.get(container).get(asset_type))}')
