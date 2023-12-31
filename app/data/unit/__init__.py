import concurrent
import requests
from app.util import Util
from app.data.resistance import Resistance
from app.data.skill import Skill
from app.data.blossom import Blossom

data_class_instance = None

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
        globals()['data_class_instance'] = self

        return

    def parse_unit(self, path, skip_area_enumeration: bool = False):
        asset = self.util.get_asset_by_path(path=path, deflate_data=True)
        data: dict = asset.get('processed_document')
        display_name: str = self.util.get_localized_string(data=data.get('profile'), key='displayName_translation', path=path)
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
        unit_rank = self.util.get_localized_string(data=data.get('originRankRarity'), key='displayName_translation', path=path)
        unit_rank_icon = data.get('originRankRarity').get('iconPath')
        movement = data.get('mobility')
        weight = data.get('weight')
        family = self.util.get_localized_string(data=data.get('profile').get('family'), key='abbrevDisplayName_translation', path=path)
        family_icon = data.get('profile').get('family').get('largeIconPath')
        small_family_icon = data.get('profile').get('family').get('smallIconPath')
        role = self.util.get_localized_string(data=data.get('profile').get('role'), key='abbrevDisplayName_translation', path=path)
        role_icon = data.get('profile').get('role').get('iconPath')
        unit_icon = data.get('profile').get('iconPath')
        transformed_unit_icon = data.get('profile').get('transformedIconPath')
        stats_by_level: list = data.get('levelParameterTable').get('monsterLevelParamList')
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
            flavor_text = self.util.get_localized_string(data=data.get('profile'), key='flavorText_translation', path=path)

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
                item_name: str = self.util.get_localized_string(data=item, key='displayName_translation', path=path)
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
            awakening_level = int(skill_learning.get('point'))
            awakening_level = int(awakening_level / 10)

            if bool(is_gacha_unit) is False:
                if awakening_level == 4:
                    awakening_level = 2
                elif awakening_level == 10:
                    awakening_level = 3
                elif awakening_level == 20:
                    awakening_level = 4
                elif awakening_level == 40:
                    awakening_level = 5

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
            awakening_level = int(awakening_level / 10)

            if bool(is_gacha_unit) is False:
                if awakening_level == 4:
                    awakening_level = 2
                elif awakening_level == 10:
                    awakening_level = 3
                elif awakening_level == 20:
                    awakening_level = 4
                elif awakening_level == 40:
                    awakening_level = 5

            skill = skill_learning.get('reactionPassiveSkill')
            skill_id = skill.get('linked_asset_id')
            awakening_reaction_passive_skill = self.skill_parser.parse_awakening_reaction_passive_skill(skill=skill, awakening_level=awakening_level, path=skill_id)
            awakening_reaction_passive_skills.append(awakening_reaction_passive_skill)

        training_board_unit_map: dict = self.util.get_redis_asset(f'{self.util.get_language_setting()}_training_board_map_parsed_asset')

        if training_board_unit_map.get(path) is not None:
            for training_board_path in training_board_unit_map.get(path):
                training_board = self.util.get_asset_by_path(training_board_path, deflate_data=True)
                training_board_document = training_board.get('processed_document')
                training_board_type = training_board_document.get('type')

                if training_board_type == 0:
                    has_blossom = True
                    blossoms = self.blossom_parser.parse_skill_board(blossom_board=training_board_document)

                if training_board_type == 1:
                    has_character_builder = True
                    character_builder_blossoms = self.blossom_parser.parse_skill_board(blossom_board=training_board_document)

        if skip_area_enumeration is False:
            area_api_response = requests.get(url='http://localhost:5000/api/area', params=dict(lang=self.util.get_language_setting()))
            area_data = []

            if area_api_response.status_code == 200:
                area_data = area_api_response.json()

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
            'small_family_icon': self.util.get_image_path(small_family_icon),
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

    def get_data(self, path, skip_area_enumeration: bool = False):
        cache_key: str = f'{self.util.get_language_setting()}_{path}_parsed_asset'
        cached_asset: dict = self.util.get_redis_asset(cache_key=cache_key)

        if cached_asset is not None:
            return cached_asset

        asset: dict = self.parse_unit(path, skip_area_enumeration)

        if skip_area_enumeration is False:
            self.util.save_redis_asset(cache_key=cache_key, data=asset)

        return asset

    def seed_cache(self):
        executor = concurrent.futures.ProcessPoolExecutor(16)
        futures = [executor.submit(process_and_save_asset, path) for path in self.util.get_asset_list('AllyMonster')]
        concurrent.futures.wait(futures)

def process_and_save_asset(path):
    data_class_instance.get_data(path=path)
