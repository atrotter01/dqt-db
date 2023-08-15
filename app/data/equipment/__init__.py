from app.util import Util
from app.data.skill import Skill

class Equipment:

    util: Util
    skill_parser: Skill

    def __init__(self, util):
        self.util = util
        self.skill_parser = Skill(util=util)

        return

    def parse_equipment(self, path):
        asset = self.util.get_asset_by_path(path=path, deflate_data=True)
        data: dict = asset.get('processed_document')

        equipment_display_name = data.get('profile').get('displayName_translation').get('gbl') or data.get('profile').get('displayName_translation').get('ja')
        equipment_description = data.get('profile').get('description_translation').get('gbl') or data.get('profile').get('description_translation').get('ja')
        equipment_icon = self.util.get_image_path(data.get('profile').get('iconPath'))
        equipment_rank_icon = self.util.get_image_path(data.get('rank').get('rankIconPath'))
        equipment_rank = data.get('rank').get('displayName_translation').get('gbl') or data.get('rank').get('displayName_translation').get('ja')
        equipment_alchemy_cost = data.get('rank').get('alchemyCost')
        equipment_type_icon = self.util.get_image_path(data.get('category').get('typeMaster').get('iconPath'))
        equipment_type = data.get('category').get('typeMaster').get('displayName_translation').get('gbl') or data.get('category').get('typeMaster').get('displayName_translation').get('ja')
        equipment_category_icon = self.util.get_image_path(data.get('category').get('iconPath'))
        equipment_category = data.get('category').get('displayName_translation').get('gbl') or data.get('category').get('displayName_translation').get('ja')
        equipment_is_free_alchemy = data.get('isFreeAlchemyCost')
        equipment_equipable_roles = []

        for role in data.get('limitation').get('limitedMonsterRoles'):
            equipment_equipable_roles.append(role.get('abbrevDisplayName_translation').get('gbl') or role.get('abbrevDisplayName_translation').get('ja'))

        base_passive_skill = data.get('basePassiveSkill')
        stat_increase_path = base_passive_skill.get('passiveSkillStatusAddEffectMasterData').get('m_PathID')
        stat_increase_document = self.util.get_asset_by_path(stat_increase_path).get('processed_document')
        equipment_status_increase = stat_increase_document.get('statusIncrease')
        equipment_passive_skill: dict = None
        equipment_reaction_skill: dict = None

        if data.get('uniquePassiveSkill').get('m_PathID') is None:
            equipment_passive_skill = self.skill_parser.get_passive_skill(data.get('uniquePassiveSkill').get('linked_asset_id'))

        if data.get('uniqueReactionPassiveSkill').get('m_PathID') is None:
            equipment_reaction_skill = self.skill_parser.get_reaction_skill(data.get('uniqueReactionPassiveSkill').get('linked_asset_id'))

        equipment_alchemy_slots: dict = {}
        equipment_alchemy_slot_counter: int = 1

        for alchemy_slot in data.get('alchemyPassiveSkillLotteries'):
            equipment_alchemy_slots[f'slot_{equipment_alchemy_slot_counter}'] = []

            for passive_skill_candidate in alchemy_slot.get('passiveSkillCandidates'):
                weight = passive_skill_candidate.get('weight')
                passive_skill = self.skill_parser.get_passive_skill(passive_skill_candidate.get('passiveSkill').get('linked_asset_id'))

                equipment_alchemy_slots[f'slot_{equipment_alchemy_slot_counter}'].append({
                    'roll_probability': weight / 1000,
                    'passive_skill': passive_skill
                })
            
            equipment_alchemy_slot_counter = equipment_alchemy_slot_counter + 1

        equipment: dict = {
            'id': path,
            'equipment_display_name': equipment_display_name,
            'equipment_description': equipment_description,
            'equipment_icon': equipment_icon,
            'equipment_rank_icon': equipment_rank_icon,
            'equipment_rank': equipment_rank,
            'equipment_alchemy_cost': equipment_alchemy_cost,
            'equipment_type_icon': equipment_type_icon,
            'equipment_type': equipment_type,
            'equipment_category_icon': equipment_category_icon,
            'equipment_category': equipment_category,
            'equipment_is_free_alchemy': equipment_is_free_alchemy,
            'equipment_equipable_roles': equipment_equipable_roles,
            'equipment_status_increase': equipment_status_increase,
            'equipment_passive_skill': equipment_passive_skill,
            'equipment_reaction_skill': equipment_reaction_skill,
            'equipment_alchemy_slots': equipment_alchemy_slots
        }

        return equipment

    def get_data(self, path):
        cache_key: str = f'{path}_parsed_asset'
        cached_asset: dict = self.util.get_redis_asset(cache_key=cache_key)

        #if cached_asset is not None:
        #    return cached_asset
        
        asset: dict = self.parse_equipment(path)
        self.util.save_redis_asset(cache_key=cache_key, data=asset)
        
        return asset
