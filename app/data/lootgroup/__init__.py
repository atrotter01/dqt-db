import concurrent
from app.util import Util

data_class_instance = None

class LootGroup:

    util: Util

    def __init__(self, util):
        self.util = util
        globals()['data_class_instance'] = self

        return

    def parse_loot_group(self, path):
        asset = self.util.get_asset_by_path(path=path, deflate_data=True)
        data: dict = asset.get('processed_document')
        loots: list = []

        for loot in data.get('equipmentLoots'):
            quantity = loot.get('quantity')
            loot_type = 'equipment'
            display_name = self.util.get_localized_string(loot.get('drop').get('profile'), key='displayName_translation', path=path)
            icon = self.util.get_image_path(loot.get('drop').get('profile').get('iconPath'))
            loot_path = loot.get('drop').get('linked_asset_id')

            loot: dict = {
                'quantity': quantity,
                'loot_type': loot_type,
                'display_name': display_name,
                'icon': icon,
                'path': loot_path
            }

            loots.append(loot)

        for loot in data.get('consumableItemLoots'):
            quantity = loot.get('quantity')
            loot_type = 'consumable_item'
            display_name = self.util.get_localized_string(loot.get('drop'), key='displayName_translation', path=path)
            icon = self.util.get_image_path(loot.get('drop').get('iconPath'))
            loot_path = loot.get('drop').get('linked_asset_id')

            loot: dict = {
                'quantity': quantity,
                'loot_type': loot_type,
                'display_name': display_name,
                'icon': icon,
                'path': loot_path
            }

            loots.append(loot)

        for loot in data.get('monsterLoots'):
            quantity = loot.get('quantity')
            loot_type = 'monster'
            display_name = self.util.get_localized_string(loot.get('drop').get('profile'), key='displayName_translation', path=path)
            icon = self.util.get_image_path(loot.get('drop').get('profile').get('iconPath'))
            loot_path = loot.get('drop').get('linked_asset_id')

            loot: dict = {
                'quantity': quantity,
                'loot_type': loot_type,
                'display_name': display_name,
                'icon': icon,
                'path': loot_path
            }

            loots.append(loot)

        for loot in data.get('profileIconLoots'):
            quantity = loot.get('quantity')
            loot_type = 'profile_icon'
            display_name = self.util.get_localized_string(loot.get('drop'), key='displayName_translation', path=path)
            icon = self.util.get_image_path(loot.get('drop').get('iconPath'))
            loot_path = loot.get('drop').get('linked_asset_id')

            loot: dict = {
                'quantity': quantity,
                'loot_type': loot_type,
                'display_name': display_name,
                'icon': icon,
                'path': loot_path
            }

            loots.append(loot)

        for loot in data.get('monsterExperiences'):
            quantity = loot.get('quantity')
            loot_type = 'experience'
            display_name = 'Experience'
            icon = None
            loot_path = None

            loot: dict = {
                'quantity': quantity,
                'loot_type': loot_type,
                'display_name': display_name,
                'icon': icon,
                'path': loot_path
            }

            loots.append(loot)

        loot_group: dict = {
            'id': path,
            'loot': loots,
        }

        return loot_group

    def get_data(self, path):
        cache_key: str = f'{self.util.get_language_setting()}_{path}_parsed_asset'
        cached_asset: dict = self.util.get_redis_asset(cache_key=cache_key)

        if cached_asset is not None:
            return cached_asset

        asset: dict = self.parse_loot_group(path)
        self.util.save_redis_asset(cache_key=cache_key, data=asset)

        return asset

    def seed_cache(self):
        executor = concurrent.futures.ProcessPoolExecutor(16)
        futures = [executor.submit(process_and_save_asset, path) for path in self.util.get_asset_list('LootItemGroup')]
        concurrent.futures.wait(futures)

def process_and_save_asset(path):
    data_class_instance.get_data(path=path)
