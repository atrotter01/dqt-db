from app.assetmap import get_asset_map_from_file, save_assets_to_db

root_path: str = '/mnt/d/DQT'
asset_map: dict = get_asset_map_from_file(root_path=root_path)

save_assets_to_db(root_path=root_path, asset_map=asset_map)
