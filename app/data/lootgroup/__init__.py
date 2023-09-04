from app.util import Util

class LootGroup:

    util: Util

    def __init__(self, util):
        self.util = util

        return

    def parse_loot_group(self, path):
        asset = self.util.get_asset_by_path(path=path, deflate_data=True)
        data: dict = asset.get('processed_document')
        loots: list = []

        for loot in data.get('equipmentLoots'):
            quantity = loot.get('quantity')
            loot_type = 'equipment'
            display_name = loot.get('drop').get('profile').get('displayName_translation').get('gbl') or loot.get('drop').get('profile').get('displayName_translation').get('ja')
            icon = self.util.get_image_path(loot.get('drop').get('profile').get('iconPath'))
            path = loot.get('drop').get('linked_asset_id')

            loot: dict = {
                'quantity': quantity,
                'loot_type': loot_type,
                'display_name': display_name,
                'icon': icon,
                'path': path
            }

            loots.append(loot)

        for loot in data.get('consumableItemLoots'):
            quantity = loot.get('quantity')
            loot_type = 'consumable_item'
            display_name = loot.get('drop').get('displayName_translation').get('gbl') or loot.get('drop').get('displayName_translation').get('ja')
            icon = self.util.get_image_path(loot.get('drop').get('iconPath'))
            path = loot.get('drop').get('linked_asset_id')

            loot: dict = {
                'quantity': quantity,
                'loot_type': loot_type,
                'display_name': display_name,
                'icon': icon,
                'path': path
            }

            loots.append(loot)

        for loot in data.get('monsterLoots'):
            quantity = loot.get('quantity')
            loot_type = 'monster'
            display_name = loot.get('drop').get('profile').get('displayName_translation').get('gbl') or loot.get('drop').get('profile').get('displayName_translation').get('ja')
            icon = self.util.get_image_path(loot.get('drop').get('profile').get('iconPath'))
            path = loot.get('drop').get('linked_asset_id')

            loot: dict = {
                'quantity': quantity,
                'loot_type': loot_type,
                'display_name': display_name,
                'icon': icon,
                'path': path
            }

            loots.append(loot)

        for loot in data.get('profileIconLoots'):
            quantity = loot.get('quantity')
            loot_type = 'profile_icon'
            display_name = loot.get('drop').get('displayName_translation').get('gbl') or loot.get('drop').get('displayName_translation').get('ja')
            icon = self.util.get_image_path(loot.get('drop').get('iconPath'))
            path = loot.get('drop').get('linked_asset_id')

            loot: dict = {
                'quantity': quantity,
                'loot_type': loot_type,
                'display_name': display_name,
                'icon': icon,
                'path': path
            }

            loots.append(loot)

        for loot in data.get('monsterExperiences'):
            quantity = loot.get('quantity')
            loot_type = 'experience'
            display_name = 'Experience'
            icon = None
            path = None

            loot: dict = {
                'quantity': quantity,
                'loot_type': loot_type,
                'display_name': display_name,
                'icon': icon,
                'path': path
            }

            loots.append(loot)

        loot_group: dict = {
            'id': path,
            'loot': loots,
        }

        return loot_group

    def get_data(self, path):
        cache_key: str = f'{path}_parsed_asset'
        cached_asset: dict = self.util.get_redis_asset(cache_key=cache_key)

        if cached_asset is not None:
            return cached_asset

        asset: dict = self.parse_loot_group(path)
        self.util.save_redis_asset(cache_key=cache_key, data=asset)

        return asset
