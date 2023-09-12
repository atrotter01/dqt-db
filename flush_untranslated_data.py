from app.util import Util
from app.data.assetprocessor import AssetProcessor
from app.data import DataProcessor

util: Util = Util()
data_processor: DataProcessor = DataProcessor(_util=util)
asset_processor: AssetProcessor = AssetProcessor(_util=util, _data_processor=data_processor)
untranslated_assets = util.get_redis_asset('sys_untranslated_strings')
final_untranslated_assets: dict = {}
seen_paths: list = []

for asset in untranslated_assets:
    asset_id = untranslated_assets.get(asset).get('asset_id')
    path = untranslated_assets.get(asset).get('path')

    if not asset_id in seen_paths:
        seen_paths.append(asset_id)
        [util.redis_client.delete(key) for key in util.asset_list if key.startswith(f'en_{asset_id}')]

    if not path in seen_paths:
        seen_paths.append(path)
        [util.redis_client.delete(key) for key in util.asset_list if key.startswith(f'en_{path}')]

seen_paths.clear()

for asset in untranslated_assets:
    asset_id = untranslated_assets.get(asset).get('asset_id')
    path = untranslated_assets.get(asset).get('path')
    
    if not asset_id in seen_paths:
        seen_paths.append(asset_id)
        asset_processor.process_asset(path=asset_id, force_rebuild=True)

    if not path in seen_paths:
        seen_paths.append(path)
        asset_processor.process_asset(path=path, force_rebuild=True)

util.redis_client.delete('en_exchange_shop_parsed_asset')
util.redis_client.delete('en_stage_parsed_asset')
util.redis_client.delete('en_farmable_parsed_asset')
util.redis_client.delete('en_area_group_parsed_asset')
util.redis_client.delete('en_enemy_monster_parsed_asset')
util.redis_client.delete('en_consumable_item_parsed_asset')
util.redis_client.delete('en_profile_icon_parsed_asset')
util.redis_client.delete('en_package_parsed_asset')
util.redis_client.delete('en_unit_parsed_asset')
util.redis_client.delete('en_rankup_calculator_parsed_asset')
util.redis_client.delete('en_unit_resist_filter_parsed_asset')
util.redis_client.delete('en_active_skills_parsed_asset')
util.redis_client.delete('en_passive_skills_parsed_asset')
util.redis_client.delete('en_reaction_skills_parsed_asset')
util.redis_client.delete('en_enemy_skills_parsed_asset')
util.redis_client.delete('en_area_parsed_asset')
util.redis_client.delete('en_equipment_parsed_asset')

for asset_key in untranslated_assets:
    key: str = untranslated_assets.get(asset_key).get('key')
    path: str = untranslated_assets.get(asset_key).get('path')
    asset_id: str = untranslated_assets.get(asset_key).get('asset_id')
    translate_key: str = f'{path}_{asset_id}_{key}'

    asset: dict = util.get_asset_by_path(asset_id, deflate_data=True)
    data: dict = asset.get('processed_document')

    if data.get(key).get('gbl') is not None:
        continue

    final_untranslated_assets[translate_key] = {
        'key': key,
        'path': path,
        'asset_id': asset_id
    }

util.save_redis_asset('sys_untranslated_strings', final_untranslated_assets)
