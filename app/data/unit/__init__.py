import requests
from app.util import Util
from app.data.resistance import Resistance
from app.data.skill import Skill
from app.data.blossom import Blossom

class Unit:

    util: Util
    skill_parser: Skill
    resistance_parser: Resistance
    blossom_parser: Blossom

    def __init__(self, util):
        self.util = util
        self.skill_parser = Skill(util=util)
        self.resistance_parser = Resistance(util=util)
        self.blossom_parser = Blossom(util=util)

        return

    def parse_unit(self, path):
        asset = self.util.get_asset_by_path(path=path, deflate_data=True)
        data: dict = asset.get('processed_document')
        display_name: str = data.get('profile').get('displayName_translation').get('gbl') or data.get('profile').get('displayName_translation').get('ja')
        flavor_text: str = None
        allow_nicknaming = data.get('allowedNicknaming')
        almanac_visible = data.get('monsterCollectionDisplayed')
        almanac_number = data.get('monsterCollectionNumber')
        max_cp = data.get('maxTotalPower')
        is_quest_reward = data.get('questReward')
        is_gacha_unit = data.get('scoutable')
        rank_up_table_list: list = []
        abnormity_resistance_table: dict = self.resistance_parser.parse_abnormity_resistance_table(abnormity_resistance_data=data.get('abnormityResistance'))
        element_resistance_table: dict = self.resistance_parser.parse_elemental_resistance_table(element_resistance_data=data.get('elementResistance'))
        unit_rank = data.get('originRankRarity').get('displayName_translation').get('gbl') or data.get('originRankRarity').get('displayName_translation').get('ja')
        unit_rank_icon = data.get('originRankRarity').get('iconPath')
        movement = data.get('mobility')
        weight = data.get('weight')
        family = data.get('profile').get('family').get('abbrevDisplayName_translation').get('gbl') or data.get('profile').get('family').get('abbrevDisplayName_translation').get('ja')
        family_icon = data.get('profile').get('family').get('largeIconPath')
        role = data.get('profile').get('role').get('abbrevDisplayName_translation').get('gbl') or data.get('profile').get('role').get('abbrevDisplayName_translation').get('ja')
        role_icon = data.get('profile').get('role').get('iconPath')
        unit_icon = data.get('profile').get('iconPath')
        transformed_unit_icon = data.get('profile').get('transformedIconPath')
        stats_by_level: list = data.get('levelParameterTable').get('monsterLevelParamList')
        blossom_board: dict = data.get('trainingBoard')
        character_builder_board: dict = data.get('skillBoard')
        active_skills: list = []
        passive_skills: list = []
        reaction_passive_skills: list = []
        awakening_passive_skills: list = []
        awakening_reaction_passive_skills: list = []
        has_battleroad: bool = False
        has_blossom: bool = False
        has_character_builder: bool = False
        blossoms: list = []
        character_builder_blossoms: list = []

        if data.get('profile').get('flavorText_translation') is not None:
            flavor_text = data.get('profile').get('flavorText_translation').get('gbl') or data.get('profile').get('flavorText_translation').get('ja')

        for rank_up_table in data.get('rankUpTable').get('monsterRankUpList'):
            rank: dict = rank_up_table.get('rank')
            recipe: dict = rank_up_table.get('recipe')
            stats: dict = {
                 'hp': rank_up_table.get('hp'),
                 'mp': rank_up_table.get('mp'),
                 'attack': rank_up_table.get('attack'),
                 'defense': rank_up_table.get('defense'),
                 'intelligence': rank_up_table.get('intelligence'),
                 'agility': rank_up_table.get('agility')
            }

            rank_number = rank.get('number') + 1
            rank_level_cap: str = rank.get('levelCap')
            rank_gold_cost: str = rank.get('rankUpCost')
            rank_up_items: list = []

            for slot in recipe.get('slots'):
                item = slot.get('item')
                item_name: str = item.get('displayName_translation').get('gbl') or item.get('displayName_translation').get('ja')
                item_icon: str = item.get('iconPath')
                quantity: str = slot.get('quantity')

                rank_up_items.append({
                    'item_name': item_name,
                    'item_icon': self.util.get_image_path(item_icon),
                    'quantity': quantity
                })

            rank_up_table_list.append({
                'rank_number': rank_number,
                'rank_level_cap': rank_level_cap,
                'rank_gold_cost': rank_gold_cost,
                'rank_up_items': rank_up_items,
                'stats_increase': stats
            })

        for skill_learning in data.get('activeSkillLearnings'):
            level_learned = skill_learning.get('level')
            skill = skill_learning.get('activeSkill')
            skill_id = skill.get('linked_asset_id')
            active_skill = self.skill_parser.parse_active_skill(skill=skill, level_learned=level_learned, path=skill_id)
            active_skills.append(active_skill)

        for skill_learning in data.get('awakeningPassiveSkillLearnings'):
            awakening_level = skill_learning.get('point')
            skill = skill_learning.get('passiveSkill')
            skill_id = skill.get('linked_asset_id')
            awakening_passive_skill = self.skill_parser.parse_awakening_passive_skill(skill=skill, awakening_level=awakening_level, path=skill_id)
            awakening_passive_skills.append(awakening_passive_skill)

        for skill_learning in data.get('passiveSkillLearnings'):
            level_learned = skill_learning.get('requiredLevel')
            skill = skill_learning.get('passiveSkill')
            skill_id = skill.get('linked_asset_id')
            passive_skill = self.skill_parser.parse_passive_skill(skill=skill, level_learned=level_learned, path=skill_id)
            passive_skills.append(passive_skill)

        for skill_learning in data.get('reactionPassiveSkillLearnings'):
            level_learned = skill_learning.get('requiredLevel')
            skill = skill_learning.get('reactionPassiveSkill')
            skill_id = skill.get('linked_asset_id')
            reaction_passive_skill = self.skill_parser.parse_reaction_passive_skill(skill=skill, level_learned=level_learned, path=skill_id)
            reaction_passive_skills.append(reaction_passive_skill)

        for skill_learning in data.get('awakeningReactionPassiveSkillLearnings'):
            awakening_level = skill_learning.get('point')
            skill = skill_learning.get('reactionPassiveSkill')
            skill_id = skill.get('linked_asset_id')
            awakening_reaction_passive_skill = self.skill_parser.parse_awakening_reaction_passive_skill(skill=skill, awakening_level=awakening_level, path=skill_id)
            awakening_reaction_passive_skills.append(awakening_reaction_passive_skill)

        if blossom_board.get('panels') is not None:
            has_blossom = True
            blossoms = self.blossom_parser.parse_skill_board(blossom_board=blossom_board)

        if character_builder_board.get('panels') is not None:
            has_character_builder = True
            character_builder_blossoms = self.blossom_parser.parse_skill_board(blossom_board=character_builder_board)

        api_response = requests.get(url=f'http://localhost:5000/api/area')
        area_data = []

        if api_response.status_code == 200:
            area_data = api_response.json()

        for area in area_data:
            if area.get('area_category') == 4:
                for available_monster in area.get('area_available_monsters'):
                    if available_monster.get('monster_name') == display_name:
                        has_battleroad = True
                        break

        unit: dict = {
            'id': path,
            'display_name': display_name,
            'flavor_text': flavor_text,
            'weight': weight,
            'move': movement,
            'unit_rank': unit_rank,
            'unit_rank_icon': self.util.get_image_path(unit_rank_icon),
            'allow_nicknaming': allow_nicknaming,
            'almanac_visible': almanac_visible,
            'almanac_number': almanac_number,
            'max_cp': max_cp,
            'is_quest_reward': is_quest_reward,
            'is_gacha_unit': is_gacha_unit,
            'family': family,
            'family_icon': self.util.get_image_path(family_icon),
            'role': role,
            'role_icon': self.util.get_image_path(role_icon),
            'unit_icon': self.util.get_image_path(unit_icon),
            'transformed_unit_icon': self.util.get_image_path(transformed_unit_icon),
            'active_skills': active_skills,
            'passive_skills': passive_skills,
            'awakening_passive_skills': awakening_passive_skills,
            'reaction_passive_skills': reaction_passive_skills,
            'awakening_reaction_passive_skills': awakening_reaction_passive_skills,
            'has_battleroad': has_battleroad,
            'has_blossom': has_blossom,
            'has_character_builder': has_character_builder,
            'blossoms': blossoms,
            'character_builder_blossoms': character_builder_blossoms
        }

        unit.update({'abnormity_resistances': abnormity_resistance_table})
        unit.update({'element_resistances': element_resistance_table})
        unit.update({'rank_up_table': rank_up_table_list})
        unit.update({'stats_by_level': stats_by_level})

        return unit

    def get_data(self, path):
        cache_key: str = f'{path}_parsed_asset'
        cached_asset: dict = self.util.get_redis_asset(cache_key=cache_key)

        if cached_asset is not None:
            return cached_asset
        
        asset: dict = self.parse_unit(path)
        self.util.save_redis_asset(cache_key=cache_key, data=asset)
        
        return asset
