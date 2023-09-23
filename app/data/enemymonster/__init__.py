import concurrent
from app.util import Util
from app.data.lootgroup import LootGroup
from app.data.resistance import Resistance
from app.data.skill import Skill

data_class_instance = None

class EnemyMonster:

    util: Util
    loot_group_parser: LootGroup
    resistance_parser: Resistance
    skill_parser: Skill

    def __init__(self, util):
        self.util = util
        self.loot_group_parser = LootGroup(util=util)
        self.resistance_parser = Resistance(util=util)
        self.skill_parser = Skill(util=util)
        globals()['data_class_instance'] = self

        return

    def parse_enemy_monster(self, path):
        asset = self.util.get_asset_by_path(path=path, deflate_data=True)
        data: dict = asset.get('processed_document')

        enemy_display_name: str = self.util.get_localized_string(data.get('profile'), key='displayName_translation', path=path)
        enemy_level = data.get('level')
        enemy_hp = data.get('hp')
        enemy_mp = data.get('mp')
        enemy_attack = data.get('attack')
        enemy_defense = data.get('defense')
        enemy_intelligence = data.get('intelligence')
        enemy_agility = data.get('agility')
        enemy_mobility = data.get('mobility')
        enemy_weight = data.get('weight')
        enemy_is_unique_monster = data.get('profile').get('uniqueType')
        enemy_is_strong_enemy = data.get('isStrongEnemy')
        enemy_scout_probability = data.get('scoutProbabilityPermyriad')
        enemy_is_rare_scout = data.get('isRareScout')
        enemy_flavor_text: str = None
        enemy_family = self.util.get_localized_string(data.get('profile').get('family'), key='abbrevDisplayName_translation', path=path)
        enemy_family_icon = self.util.get_image_path(data.get('profile').get('family').get('largeIconPath'))
        enemy_role = self.util.get_localized_string(data.get('profile').get('role'), key='abbrevDisplayName_translation', path=path)
        enemy_role_icon = self.util.get_image_path(data.get('profile').get('role').get('iconPath'))
        enemy_unit_icon = self.util.get_image_path(data.get('profile').get('iconPath'))
        enemy_transformed_unit_icon = self.util.get_image_path(data.get('profile').get('transformedIconPath'))

        if data.get('profile').get('flavorText_translation') is not None:
            enemy_flavor_text = self.util.get_localized_string(data.get('profile'), key='flavorText_translation', path=path)

        enemy_active_skills: list = []
        enemy_passive_skills: list = []
        enemy_reaction_skills: list = []
        enemy_drops: list = []

        enemy_element_resistance = self.resistance_parser.parse_elemental_resistance_table(data.get('elementResistance'))
        enemy_abnormity_resistance = self.resistance_parser.parse_abnormity_resistance_table(data.get('abnormityResistance'))

        for skill in data.get('activeSkills'):
            enemy_active_skills.append(self.skill_parser.parse_active_skill(skill, path=skill.get('linked_asset_id')))

        for skill in data.get('passiveSkills'):
            enemy_passive_skills.append(self.skill_parser.parse_passive_skill(skill, path=skill.get('linked_asset_id')))

        for skill in data.get('reactionPassiveSkills'):
            enemy_reaction_skills.append(self.skill_parser.parse_reaction_passive_skill(skill, path=skill.get('linked_asset_id')))

        for drop_candidate in data.get('fixedReward').get('dropCandidates'):
            drop_percent: int = drop_candidate.get('weight')
            loot_group: dict = self.loot_group_parser.get_data(drop_candidate.get('lootGroup').get('linked_asset_id'))

            enemy_drops.append({
                'loot_group': loot_group,
                'drop_percent': drop_percent
            })

        for drop_candidate in data.get('randomReward').get('dropCandidates'):
            drop_percent: int = drop_candidate.get('weight')
            loot_group: dict = self.loot_group_parser.get_data(drop_candidate.get('lootGroup').get('linked_asset_id'))

            enemy_drops.append({
                'loot_group': loot_group,
                'drop_percent': drop_percent
            })

        enemy_monster: dict = {
            'id': path,
            'enemy_display_name': enemy_display_name,
            'enemy_level': enemy_level,
            'enemy_hp': enemy_hp,
            'enemy_mp': enemy_mp,
            'enemy_attack': enemy_attack,
            'enemy_defense': enemy_defense,
            'enemy_intelligence': enemy_intelligence,
            'enemy_agility': enemy_agility,
            'enemy_mobility': enemy_mobility,
            'enemy_weight': enemy_weight,
            'enemy_is_unique_monster': enemy_is_unique_monster,
            'enemy_is_strong_enemy': enemy_is_strong_enemy,
            'enemy_scout_probability': enemy_scout_probability,
            'enemy_is_rare_scout': enemy_is_rare_scout,
            'enemy_flavor_text': enemy_flavor_text,
            'enemy_family': enemy_family,
            'enemy_family_icon': enemy_family_icon,
            'enemy_role': enemy_role,
            'enemy_role_icon': enemy_role_icon,
            'enemy_unit_icon': enemy_unit_icon,
            'enemy_transformed_unit_icon': enemy_transformed_unit_icon,
            'enemy_active_skills': enemy_active_skills,
            'enemy_passive_skills': enemy_passive_skills,
            'enemy_reaction_skills': enemy_reaction_skills,
            'enemy_element_resistance': enemy_element_resistance,
            'enemy_abnormity_resistance': enemy_abnormity_resistance,
            'enemy_drops': enemy_drops
        }

        return enemy_monster

    def get_data(self, path):
        cache_key: str = f'{self.util.get_language_setting()}_{path}_parsed_asset'
        cached_asset: dict = self.util.get_redis_asset(cache_key=cache_key)

        if cached_asset is not None:
            return cached_asset

        asset: dict = self.parse_enemy_monster(path)
        self.util.save_redis_asset(cache_key=cache_key, data=asset)

        return asset

    def seed_cache(self):
        executor = concurrent.futures.ProcessPoolExecutor(16)
        futures = [executor.submit(process_and_save_asset, path) for path in self.util.get_asset_list('EnemyMonster')]
        concurrent.futures.wait(futures)

def process_and_save_asset(path):
    data_class_instance.get_data(path=path)
