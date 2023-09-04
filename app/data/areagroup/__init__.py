from app.util import Util

class AreaGroup:

    util: Util

    def __init__(self, util):
        self.util = util

        return

    def parse_area_group(self, path):
        asset = self.util.get_asset_by_path(path=path, deflate_data=True)
        data: dict = asset.get('processed_document')

        area_group_name = data.get('displayName_translation').get('gbl') or data.get('displayName_translation').get('ja')
        area_group_banner_path = self.util.get_image_path(data.get('bannerPath'))
        area_group_score_reward = data.get('enableScoreRanking')
        area_group_show_display_name_at_banner = data.get('showDisplayNameAtBanner')
        area_group_category = data.get('category')
        area_group_subcategory = data.get('subCategory')
        area_group_parent = data.get('parentAreaGroup').get('linked_asset_id')
        area_group_children: list = []

        all_area_group_asset_list: list = []
        all_area_group_asset_list.extend(self.util.get_asset_list('AreaGroup'))
        all_area_group_asset_list.extend(self.util.get_asset_list('MemoryAreaGroup'))
        all_area_group_asset_list.extend(self.util.get_asset_list('MemoryAreaGroupCategory'))

        for area_group_path in all_area_group_asset_list:
            area_asset = self.util.get_asset_by_path(area_group_path)
            area_data: dict = area_asset.get('processed_document')

            if area_data.get('parentAreaGroup').get('linked_asset_id') == path:
                area_group_children.append(area_group_path)

        area_group: dict = {
            'id': path,
            'area_group_display_name': area_group_name,
            'area_group_banner_path': area_group_banner_path,
            'area_group_score_reward': area_group_score_reward,
            'area_group_show_display_name_at_banner': area_group_show_display_name_at_banner,
            'area_group_category': area_group_category,
            'area_group_subcategory': area_group_subcategory,
            'area_group_parent': area_group_parent,
            'area_group_children': area_group_children
        }

        return area_group

    def get_data(self, path):
        cache_key: str = f'{path}_parsed_asset'
        cached_asset: dict = self.util.get_redis_asset(cache_key=cache_key)

        if cached_asset is not None:
            return cached_asset

        asset: dict = self.parse_area_group(path)
        self.util.save_redis_asset(cache_key=cache_key, data=asset)

        return asset
