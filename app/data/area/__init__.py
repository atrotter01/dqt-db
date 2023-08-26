from app.util import Util
from app.data.unit import Unit

class Area:

    util: Util
    unit_parser: Unit

    def __init__(self, util):
        self.util = util
        self.unit_parser = Unit(util=util)

        return

    def parse_area(self, path):
        asset = self.util.get_asset_by_path(path=path, deflate_data=True)
        data: dict = asset.get('processed_document')

        area_display_name = data.get('displayName_translation').get('gbl') or data.get('displayName_translation').get('ja')
        area_sub_display_name = None
        area_group = data.get('areaGroup').get('linked_asset_id')
        area_category = data.get('category')
        area_sub_category = data.get('subCategory')
        area_stage_display_type = data.get('stageDisplayType')
        area_list_order = data.get('listOrder')
        area_banner_path = self.util.get_image_path(data.get('bannerPath'))
        area_show_display_name_at_banner = data.get('showDisplayNameAtBanner')
        area_achievement_target_name = None
        area_has_schedule = data.get('hasSchedule')
        area_is_condition_clear_visible = data.get('isConditionClearVisible')
        area_skip_ticket_unusable = data.get('unusableClearTicket')
        area_is_demons_tower = data.get('isDemonsTower')
        area_hide_when_completed = data.get('hideWhenCompleted')
        area_is_notification_displayable = data.get('isNotificationDisplayable')
        area_reset_type = data.get('resetType')
        area_number_of_stages_back = data.get('numberOfStagesToBack')
        area_available_monster_families: list = []
        area_available_monsters: list = []

        if data.get('subDisplayName_translation') is not None:
            area_sub_display_name = data.get('subDisplayName_translation').get('gbl') or data.get('subDisplayName_translation').get('ja')

        if data.get('achievementTarget').get('displayName_translation') is not None:
            area_achievement_target_name = data.get('achievementTarget').get('displayName_translation').get('gbl') or data.get('achievementTarget').get('displayName_translation').get('ja')

        for available_monster_family in data.get('availableMonsterFamilies'):
            monster_family_name = available_monster_family.get('displayName_translation').get('gbl') or available_monster_family.get('displayName_translation').get('ja')
            area_available_monster_families.append(monster_family_name)

        for available_monster in data.get('availableMonsters'):
            monster_is_required = available_monster.get('isRequired')
            monster_path = available_monster.get('monster').get('linked_asset_id')
            unit = self.unit_parser.get_data(monster_path)
            monster_name = unit.get('display_name')
            monster_icon = unit.get('unit_icon')

            area_available_monsters.append({
                'monster_name': monster_name,
                'monster_path': monster_path,
                'monster_icon': monster_icon,
                'is_required': monster_is_required,
            })

        # Todo Parse Guild Battle Rewards
        #if data.get('guildRaidRankingGroup').get('m_PathID') is None:
        #    raise Exception(path)

        area: dict = {
            'id': path,
            'area_group': area_group,
            'area_display_name': area_display_name,
            'area_sub_display_name': area_sub_display_name,
            'area_category': area_category,
            'area_sub_category': area_sub_category,
            'area_stage_display_type': area_stage_display_type,
            'area_list_order': area_list_order,
            'area_banner_path': area_banner_path,
            'area_show_display_name_at_banner': area_show_display_name_at_banner,
            'area_achievement_target_name': area_achievement_target_name,
            'area_has_schedule': area_has_schedule,
            'area_is_condition_clear_visible': area_is_condition_clear_visible,
            'area_skip_ticket_unusable': area_skip_ticket_unusable,
            'area_is_demons_tower': area_is_demons_tower,
            'area_hide_when_completed': area_hide_when_completed,
            'area_is_notification_displayable': area_is_notification_displayable,
            'area_reset_type': area_reset_type,
            'area_number_of_stages_back': area_number_of_stages_back,
            'area_available_monster_families': area_available_monster_families,
            'area_available_monsters': area_available_monsters,
        }

        return area

    def get_data(self, path):
        cache_key: str = f'{path}_parsed_asset'
        cached_asset: dict = self.util.get_redis_asset(cache_key=cache_key)

        if cached_asset is not None:
            return cached_asset
        
        asset: dict = self.parse_area(path)
        self.util.save_redis_asset(cache_key=cache_key, data=asset)
        
        return asset