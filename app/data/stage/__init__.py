from app.util import Util
from app.data.enemymonster import EnemyMonster
from app.data.lootgroup import LootGroup

class Stage:

    util: Util
    enemy_monster_parser: EnemyMonster
    loot_group_parser: LootGroup

    def __init__(self, util):
        self.util = util
        self.enemy_monster_parser = EnemyMonster(util=util)
        self.loot_group_parser = LootGroup(util=util)

        return

    def parse_stage(self, path):
        asset = self.util.get_asset_by_path(path=path, deflate_data=True)
        data: dict = asset.get('processed_document')

        stage_name = data.get('displayName_translation').get('gbl') or data.get('displayName_translation').get('ja')
        stage_area_id = data.get('area').get('linked_asset_id')
        stage_list_order = data.get('listOrder')
        stage_difficulty = data.get('difficulty')
        stage_recommended_cp = data.get('recommendedAveragePowerLevel')
        stage_stamina_cost = data.get('consumptionStamina')
        stage_talent_point_gain = data.get('acquisitionTrainingBoardPoint')
        stage_is_boss_stage = data.get('isBossStage')
        stage_is_story_stage = data.get('isStoryStage')
        stage_is_auto_only = data.get('disableManualOperation')
        stage_is_limited_total_weight = data.get('useLimitedTotalWeight')
        stage_limited_total_weight = data.get('limitedTotalWeight')
        stage_is_organization_limit_num = data.get('useOrganizationLimitNum')
        stage_organization_limit_num = data.get('organizationLimitNum')
        stage_is_send_feed_when_first_cleared = data.get('isSendFeedWhenFirstCleared')
        stage_enable_score_challenge = data.get('enableScoreChallenge')
        stage_banner_path = self.util.get_image_path(data.get('bannerImagePath'))
        stage_sub_display_name = None
        stage_enemies: list = []
        stage_random_enemies: list = []
        stage_reinforcement_enemies: list = []
        stage_drops: list = []
        stage_missions: list = []

        # Todo
        #randomStageGeneration - TnT Board Enemies
        #consumptionItems - Required Stage Items
        #onlyConsumeItemsWhenClear
        #treasureChests
        #openingScenarioPath
        #endingScenarioPath
        #preBattleScenarioPath
        #postBattleScenarioPath
        #imageIconPath
        #pickupIcons
        #stagePlayCountRestriction
        #stageEffect
        #turnLimit
        #extraGuestMonsters
        #clearCountRestriction
        #elementWeaknesses
        #abnormityStatusWeaknesses

        if data.get('subDisplayName_translation') is not None:
            stage_sub_display_name = data.get('subDisplayName_translation').get('gbl') or data.get('subDisplayName_translation').get('ja')

        for enemy in data.get('enemies'):
            enemy_monster: dict = self.enemy_monster_parser.get_data(enemy.get('monster').get('linked_asset_id'))
            monster: dict = {
                'id': enemy_monster.get('id'),
                'enemy_display_name': enemy_monster.get('enemy_display_name'),
                'enemy_level': enemy_monster.get('enemy_level'),
                'enemy_hp': enemy_monster.get('enemy_hp'),
                'enemy_mp': enemy_monster.get('enemy_mp'),
                'enemy_attack': enemy_monster.get('enemy_attack'),
                'enemy_defense': enemy_monster.get('enemy_defense'),
                'enemy_intelligence': enemy_monster.get('enemy_intelligence'),
                'enemy_agility': enemy_monster.get('enemy_agility'),
                'enemy_mobility': enemy_monster.get('enemy_mobility'),
                'enemy_weight': enemy_monster.get('enemy_weight'),
                'enemy_is_unique_monster': enemy_monster.get('enemy_is_unique_monster'),
                'enemy_is_strong_enemy': enemy_monster.get('enemy_is_strong_enemy'),
                'enemy_scout_probability': enemy_monster.get('enemy_scout_probability'),
                'enemy_is_rare_scout': enemy_monster.get('enemy_is_rare_scout'),
                'enemy_flavor_text': enemy_monster.get('enemy_flavor_text'),
                'enemy_family': enemy_monster.get('enemy_family'),
                'enemy_family_icon': enemy_monster.get('enemy_family_icon'),
                'enemy_role': enemy_monster.get('enemy_role'),
                'enemy_role_icon': enemy_monster.get('enemy_role_icon'),
                'enemy_unit_icon': enemy_monster.get('enemy_unit_icon'),
                'enemy_transformed_unit_icon': enemy_monster.get('enemy_transformed_unit_icon'),
                'enemy_drops': enemy_monster.get('enemy_drops')
            }

            stage_enemies.append({
                'is_one_time_enemy': enemy.get('isOneTime'),
                'monster': monster
            })

        for enemy_reinforcement in data.get('enemyReinforcements'):
            enemy_monster: dict = self.enemy_monster_parser.get_data(enemy_reinforcement.get('enemy').get('monster').get('linked_asset_id'))
            monster: dict = {
                'id': enemy_monster.get('id'),
                'enemy_display_name': enemy_monster.get('enemy_display_name'),
                'enemy_level': enemy_monster.get('enemy_level'),
                'enemy_hp': enemy_monster.get('enemy_hp'),
                'enemy_mp': enemy_monster.get('enemy_mp'),
                'enemy_attack': enemy_monster.get('enemy_attack'),
                'enemy_defense': enemy_monster.get('enemy_defense'),
                'enemy_intelligence': enemy_monster.get('enemy_intelligence'),
                'enemy_agility': enemy_monster.get('enemy_agility'),
                'enemy_mobility': enemy_monster.get('enemy_mobility'),
                'enemy_weight': enemy_monster.get('enemy_weight'),
                'enemy_is_unique_monster': enemy_monster.get('enemy_is_unique_monster'),
                'enemy_is_strong_enemy': enemy_monster.get('enemy_is_strong_enemy'),
                'enemy_scout_probability': enemy_monster.get('enemy_scout_probability'),
                'enemy_is_rare_scout': enemy_monster.get('enemy_is_rare_scout'),
                'enemy_flavor_text': enemy_monster.get('enemy_flavor_text'),
                'enemy_family': enemy_monster.get('enemy_family'),
                'enemy_family_icon': enemy_monster.get('enemy_family_icon'),
                'enemy_role': enemy_monster.get('enemy_role'),
                'enemy_role_icon': enemy_monster.get('enemy_role_icon'),
                'enemy_unit_icon': enemy_monster.get('enemy_unit_icon'),
                'enemy_transformed_unit_icon': enemy_monster.get('enemy_transformed_unit_icon'),
                'enemy_drops': enemy_monster.get('enemy_drops')
            }

            stage_reinforcement_enemies.append({
                'is_one_time_enemy': enemy_reinforcement.get('enemy').get('isOneTime'),
                'monster': monster
            })

        for random_pop_enemy in data.get('randomPopEnemies'):
            for candidate in random_pop_enemy.get('enemyGroup').get('candidates'):
                enemy_monster: dict = self.enemy_monster_parser.get_data(candidate.get('monster').get('linked_asset_id'))
                monster: dict = {
                    'id': enemy_monster.get('id'),
                    'enemy_display_name': enemy_monster.get('enemy_display_name'),
                    'enemy_level': enemy_monster.get('enemy_level'),
                    'enemy_hp': enemy_monster.get('enemy_hp'),
                    'enemy_mp': enemy_monster.get('enemy_mp'),
                    'enemy_attack': enemy_monster.get('enemy_attack'),
                    'enemy_defense': enemy_monster.get('enemy_defense'),
                    'enemy_intelligence': enemy_monster.get('enemy_intelligence'),
                    'enemy_agility': enemy_monster.get('enemy_agility'),
                    'enemy_mobility': enemy_monster.get('enemy_mobility'),
                    'enemy_weight': enemy_monster.get('enemy_weight'),
                    'enemy_is_unique_monster': enemy_monster.get('enemy_is_unique_monster'),
                    'enemy_is_strong_enemy': enemy_monster.get('enemy_is_strong_enemy'),
                    'enemy_scout_probability': enemy_monster.get('enemy_scout_probability'),
                    'enemy_is_rare_scout': enemy_monster.get('enemy_is_rare_scout'),
                    'enemy_flavor_text': enemy_monster.get('enemy_flavor_text'),
                    'enemy_family': enemy_monster.get('enemy_family'),
                    'enemy_family_icon': enemy_monster.get('enemy_family_icon'),
                    'enemy_role': enemy_monster.get('enemy_role'),
                    'enemy_role_icon': enemy_monster.get('enemy_role_icon'),
                    'enemy_unit_icon': enemy_monster.get('enemy_unit_icon'),
                    'enemy_transformed_unit_icon': enemy_monster.get('enemy_transformed_unit_icon'),
                    'enemy_drops': enemy_monster.get('enemy_drops')
                }

                stage_random_enemies.append({
                    'is_rare_pop': candidate.get('isRarePopCandidate'),
                    'pop_percentage': candidate.get('probabilityPercentage'),
                    'monster': monster
                })

        monster_drop_rates: dict = {}
        seen_monsters: list = []
        monster_counts: dict = {
            0: 0,
            1: 0
        }

        for enemy in stage_enemies:
            enemy_id = enemy.get('monster').get('id')
            enemy_name = enemy.get('monster').get('enemy_display_name')
            scout_probability = enemy.get('monster').get('enemy_scout_probability')
            is_rare_scout = enemy.get('monster').get('enemy_is_rare_scout')

            if not enemy_name in seen_monsters:
                monster_counts[is_rare_scout] = monster_counts[is_rare_scout] + 1
                seen_monsters.append(enemy_name)

            if monster_drop_rates.get(enemy_id) is None:
                monster_drop_rates[enemy_id] = {}
                monster_drop_rates[enemy_id]['is_rare_scout'] = is_rare_scout
                monster_drop_rates[enemy_id]['base_drop_rate'] = scout_probability
                monster_drop_rates[enemy_id]['count'] = 1
            else:
                monster_drop_rates[enemy_id]['count'] = monster_drop_rates[enemy_id]['count'] + 1

        for enemy in stage_reinforcement_enemies:
            enemy_id = enemy.get('monster').get('id')
            enemy_name = enemy.get('monster').get('enemy_display_name')
            scout_probability = enemy.get('monster').get('enemy_scout_probability')
            is_rare_scout = enemy.get('monster').get('enemy_is_rare_scout')

            if not enemy_name in seen_monsters:
                monster_counts[is_rare_scout] = monster_counts[is_rare_scout] + 1
                seen_monsters.append(enemy_name)

            if monster_drop_rates.get(enemy_id) is None:
                monster_drop_rates[enemy_id] = {}
                monster_drop_rates[enemy_id]['is_rare_scout'] = is_rare_scout
                monster_drop_rates[enemy_id]['base_drop_rate'] = scout_probability
                monster_drop_rates[enemy_id]['count'] = 1
            else:
                monster_drop_rates[enemy_id]['count'] = monster_drop_rates[enemy_id]['count'] + 1

            monster_counts[is_rare_scout] = monster_counts[is_rare_scout] + 1

        for enemy in stage_random_enemies:
            enemy_id = enemy.get('monster').get('id')
            enemy_name = enemy.get('monster').get('enemy_display_name')
            scout_probability = enemy.get('monster').get('enemy_scout_probability')
            is_rare_scout = enemy.get('monster').get('enemy_is_rare_scout')

            if not enemy_name in seen_monsters:
                monster_counts[is_rare_scout] = monster_counts[is_rare_scout] + 1
                seen_monsters.append(enemy_name)

            if monster_drop_rates.get(enemy_id) is None:
                monster_drop_rates[enemy_id] = {}
                monster_drop_rates[enemy_id]['is_rare_scout'] = is_rare_scout
                monster_drop_rates[enemy_id]['base_drop_rate'] = scout_probability
                monster_drop_rates[enemy_id]['count'] = 1
            else:
                monster_drop_rates[enemy_id]['count'] = monster_drop_rates[enemy_id]['count'] + 1

            monster_counts[is_rare_scout] = monster_counts[is_rare_scout] + 1

        for monster in monster_drop_rates:
            is_rare_scout = monster_drop_rates.get(monster).get('is_rare_scout')
            base_drop_rate = monster_drop_rates.get(monster).get('base_drop_rate')
            monster_count = monster_drop_rates.get(monster).get('count')
            total_scouts = monster_counts.get(is_rare_scout)

            if base_drop_rate == 0:
                continue

            calculated_drop_rate = self.util.float_to_str(((base_drop_rate * monster_count) / total_scouts) / 100)

            for enemy in stage_enemies:
                enemy_id = enemy.get('monster').get('id')

                if enemy_id == monster:
                    enemy.get('monster').update({'enemy_scout_probability': calculated_drop_rate})

            for enemy in stage_reinforcement_enemies:
                enemy_id = enemy.get('monster').get('id')

                if enemy_id == monster:
                    enemy.get('monster').update({'enemy_scout_probability': calculated_drop_rate})

            for enemy in stage_random_enemies:
                enemy_id = enemy.get('monster').get('id')

                if enemy_id == monster:
                    enemy.get('monster').update({'enemy_scout_probability': calculated_drop_rate})


        for drop_candidate in data.get('fixedReward').get('dropCandidates'):
            drop_percent: int = drop_candidate.get('weight')
            loot_group: dict = self.loot_group_parser.get_data(drop_candidate.get('lootGroup').get('linked_asset_id'))

            stage_drops.append({
                'loot_group': loot_group,
                'drop_percent': drop_percent,
                'first_clear_only': False,
                'clear_count': None,
            })

        for random_reward in data.get('randomRewards'):
            for drop_candidate in random_reward.get('dropCandidates'):
                drop_percent: int = drop_candidate.get('weight')
                loot_group: dict = self.loot_group_parser.get_data(drop_candidate.get('lootGroup').get('linked_asset_id'))

                stage_drops.append({
                    'loot_group': loot_group,
                    'drop_percent': drop_percent,
                    'first_clear_only': False,
                    'clear_count': None,
                })

        for fixed_reward in data.get('stageRewardByClearCounts'):
            clear_count = fixed_reward.get('clearCount')

            for drop_candidate in fixed_reward.get('lootLottery').get('dropCandidates'):
                drop_percent: int = drop_candidate.get('weight')
                loot_group: dict = self.loot_group_parser.get_data(drop_candidate.get('lootGroup').get('linked_asset_id'))

                stage_drops.append({
                    'loot_group': loot_group,
                    'drop_percent': drop_percent,
                    'first_clear_only': True,
                    'clear_count': clear_count,
                })

        for stage_mission_key in data.get('stageMissionList').get('stageMissions'):
                stage_mission_conditions: list = []
                
                for condition in stage_mission_key.get('conditions'):
                    condition_code = '0'#condition.get('code')
                    condition_amount = str(condition.get('amount'))
                    condition_description: str = None

                    if stage_mission_key.get('description_translation') is not None:
                        condition_description = stage_mission_key.get('description_translation').get('gbl') or stage_mission_key.get('description_translation').get('ja')
                    else:
                        condition_description = condition.get('typeMaster').get('description_translation').get('gbl') or condition.get('typeMaster').get('description_translation').get('ja')

                    condition_description = self.util.clean_text_string(str_to_clean=self.util.replace_string_variable(str_to_clean=condition_description, key=condition_code, value=condition_amount), unit='+')

                    stage_mission_conditions.append(condition_description)

                reward_quantity = stage_mission_key.get('reward').get('quantity')
                reward_display_name = None
                reward_icon = None

                if stage_mission_key.get('reward').get('item').get('m_PathID') is None:
                    reward_icon = self.util.get_image_path(stage_mission_key.get('reward').get('item').get('iconPath'))
                    reward_display_name = stage_mission_key.get('reward').get('item').get('displayName_translation').get('gbl') or stage_mission_key.get('reward').get('item').get('displayName_translation').get('ja')
                elif stage_mission_key.get('reward').get('profileIcon').get('m_PathID') is None:
                    reward_icon = self.util.get_image_path(stage_mission_key.get('reward').get('profileIcon').get('iconPath'))
                    reward_display_name = stage_mission_key.get('reward').get('profileIcon').get('displayName_translation').get('gbl') or stage_mission_key.get('reward').get('profileIcon').get('displayName_translation').get('ja')

                stage_missions.append({
                    'stage_mission_conditions': stage_mission_conditions,
                    'reward_quantity': reward_quantity,
                    'reward_display_name': reward_display_name,
                    'reward_icon': reward_icon
                })

        stage: dict = {
            'id': path,
            'stage_display_name': stage_name,
            'stage_sub_display_name': stage_sub_display_name,
            'stage_area_id': stage_area_id,
            'stage_list_order': stage_list_order,
            'stage_difficulty': stage_difficulty,
            'stage_recommended_cp': stage_recommended_cp,
            'stage_stamina_cost': stage_stamina_cost,
            'stage_talent_point_gain': stage_talent_point_gain,
            'stage_is_boss_stage': stage_is_boss_stage,
            'stage_is_story_stage': stage_is_story_stage,
            'stage_is_auto_only': stage_is_auto_only,
            'stage_is_limited_total_weight': stage_is_limited_total_weight,
            'stage_limited_total_weight': stage_limited_total_weight,
            'stage_is_organization_limit_num': stage_is_organization_limit_num,
            'stage_organization_limit_num': stage_organization_limit_num,
            'stage_is_send_feed_when_first_cleared': stage_is_send_feed_when_first_cleared,
            'stage_enable_score_challenge': stage_enable_score_challenge,
            'stage_banner_path': stage_banner_path,
            'stage_enemies': stage_enemies,
            'stage_random_enemies': stage_random_enemies,
            'stage_reinforcement_enemies': stage_reinforcement_enemies,
            'stage_drops': stage_drops,
            'stage_missions': stage_missions,
        }

        return stage

    def get_data(self, path):
        cache_key: str = f'{path}_parsed_asset'
        cached_asset: dict = self.util.get_redis_asset(cache_key=cache_key)

        if cached_asset is not None:
            return cached_asset
        
        asset: dict = self.parse_stage(path)
        self.util.save_redis_asset(cache_key=cache_key, data=asset)
        
        return asset
