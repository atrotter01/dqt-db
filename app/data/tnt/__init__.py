import concurrent
from app.util import Util
from app.data.lootgroup import LootGroup
from app.data.stage import Stage

data_class_instance = None

class TnT:

    util: Util
    loot_group_parser: LootGroup
    stage_parser: Stage

    def __init__(self, util):
        self.util = util
        self.loot_group_parser = LootGroup(util=util)
        self.stage_parser = Stage(util=util)
        globals()['data_class_instance'] = self

        return

    def parse_tnt_zone(self, zone_data: dict):
        tnt_routes: list = zone_data.get('routes')
        tnt_treasure_chest_squares: list = zone_data.get('treasureChestSquareCodes')
        tnt_shortest_path_length: int = zone_data.get('shortestPathLength')
        tnt_zone_squares: list = []

        for square in zone_data.get('squares'):
            square_number: int = square.get('code')
            square_events: list = []
            square_connections: list = []
            square_has_treasure_chest: bool = False

            for event in square.get('squareEventSetting').get('squareEvents'):
                event_type: int = event.get('eventType')
                
                square_event_type: str = None
                square_event: dict = {}
                square_event_probability: int = event.get('probabilityPerMil') / 10

                if event_type == 0:
                    square_event_type = 'Arrow'

                elif event_type == 1:
                    square_event_type = 'Start'

                elif event_type == 2:
                    square_event_type = 'Goal'

                elif event_type == 3:
                    square_event_type = 'Warp'
                    square_event.update({
                        'warp_to_square': event.get('warpSettingData').get('warpTo'),
                        'warp_is_selectable': bool(event.get('warpSettingData').get('isSelectable')),
                        'warp_dice_quantity_change': event.get('warpSettingData').get('diceQuantityChange')
                    })

                elif event_type == 4:
                    square_event_type = 'Move'
                    square_event.update({
                        'step_count': event.get('moveSettingData').get('stepCount')
                    })

                elif event_type == 5:
                    square_event_type = 'Dice Quantity Change'
                    square_event.update({
                        'dice_quantity': event.get('diceQuantityChangeSettingData').get('diceQuantityChange')
                    })

                elif event_type == 6:
                    square_event_type = 'Trap Square'

                elif event_type == 7:
                    square_event_type = 'Loot'
                    formatted_loot_groups: dict = {}
                    loot_asset = self.util.get_asset_by_path(path=event.get('lootSettingData').get('lootLotteryMasterData').get('m_PathID'), deflate_data=True)

                    for drop_candidate in loot_asset.get('processed_document').get('dropCandidates'):
                        loot_drop_percent: int = drop_candidate.get('weight')
                        loot_group: dict = self.loot_group_parser.get_data(drop_candidate.get('lootGroup').get('linked_asset_id'))

                        for loot in loot_group.get('loot'):
                            loot_quantity = loot.get('quantity')
                            loot_type = loot.get('loot_type')
                            loot_display_name = loot.get('display_name')
                            loot_icon = loot.get('icon')
                            loot_path = loot.get('path')

                            if formatted_loot_groups.get(loot_display_name) is None:
                                formatted_loot_groups[loot_display_name] = {}

                            if formatted_loot_groups[loot_display_name].get('sources') is None:
                                formatted_loot_groups[loot_display_name]['sources'] = []

                            if formatted_loot_groups[loot_display_name].get('average') is None:
                                formatted_loot_groups[loot_display_name]['average'] = 0

                            formatted_loot_groups[loot_display_name]['sources'].append({
                                'loot_quantity': loot_quantity,
                                'loot_type': loot_type,
                                'loot_display_name': loot_display_name,
                                'loot_icon': loot_icon,
                                'loot_path': loot_path,
                                'loot_drop_percent': loot_drop_percent,
                            })

                            formatted_loot_groups[loot_display_name]['average'] = formatted_loot_groups[loot_display_name]['average'] + (loot_quantity * (loot_drop_percent / 100))

                    square_event.update({
                        'loot': formatted_loot_groups
                    })

                elif event_type == 8:
                    square_event_type = 'Battle'
                    stage: dict = self.stage_parser.get_data(path=event.get('battleSettingData').get('stageMasterData').get('m_PathID'))

                    square_event.update({
                        'stage_id': stage.get('id'),
                        'stage_display_name': stage.get('stage_display_name'),
                        'stage_area_name': stage.get('stage_area_name'),
                        'stage_area_group_name': stage.get('stage_area_group_name'),
                    })

                elif event_type == 9:
                    square_event_type = 'Roulette'
                    formatted_loot_groups: dict = {}

                    roulette_lottery_path = event.get('rouletteSettingData').get('sugorokuRouletteLotteryMasterData').get('m_PathID')
                    roulette_data = self.util.get_asset_by_path(path=roulette_lottery_path, deflate_data=True)
                    roulette_document = roulette_data.get('processed_document')

                    for loot_lottery_master_data in roulette_document.get('lootLotteryMasterDatas'):
                        loot_lottery_path = loot_lottery_master_data.get('m_PathID')
                        loot_lottery_asset = self.util.get_asset_by_path(path=loot_lottery_path, deflate_data=True)

                        for drop_candidate in loot_lottery_asset.get('processed_document').get('dropCandidates'):
                            loot_drop_percent: int = drop_candidate.get('weight')
                            loot_group: dict = self.loot_group_parser.get_data(drop_candidate.get('lootGroup').get('linked_asset_id'))

                            for loot in loot_group.get('loot'):
                                loot_quantity = loot.get('quantity')
                                loot_type = loot.get('loot_type')
                                loot_display_name = loot.get('display_name')
                                loot_icon = loot.get('icon')
                                loot_path = loot.get('path')

                                if formatted_loot_groups.get(loot_display_name) is None:
                                    formatted_loot_groups[loot_display_name] = {}

                                if formatted_loot_groups[loot_display_name].get('sources') is None:
                                    formatted_loot_groups[loot_display_name]['sources'] = []

                                if formatted_loot_groups[loot_display_name].get('average') is None:
                                    formatted_loot_groups[loot_display_name]['average'] = 0

                                formatted_loot_groups[loot_display_name]['sources'].append({
                                    'loot_quantity': loot_quantity,
                                    'loot_type': loot_type,
                                    'loot_display_name': loot_display_name,
                                    'loot_icon': loot_icon,
                                    'loot_path': loot_path,
                                    'loot_drop_percent': loot_drop_percent,
                                })

                                formatted_loot_groups[loot_display_name]['average'] = formatted_loot_groups[loot_display_name]['average'] + (loot_quantity * (loot_drop_percent / 100))

                    square_event.update({
                        'loot': formatted_loot_groups
                    })

                else:
                    print(zone_data)
                    raise NotImplementedError(event_type)
                
                square_events.append({
                    'square_event_type': square_event_type,
                    'square_event_probability': square_event_probability,
                    'square_event': square_event
                })

            for route in tnt_routes:
                if route.get('from') == square_number:
                    square_connections.append(route.get('to'))

            if square_number in tnt_treasure_chest_squares:
                square_has_treasure_chest = True

            tnt_zone_squares.append({
                'square_number': square_number,
                'square_events': square_events,
                'square_connections': square_connections,
                'square_has_treasure_chest': square_has_treasure_chest
            })

        tnt_zone: dict = {
            'tnt_shortest_path_length': tnt_shortest_path_length,
            'tnt_zone_squares': tnt_zone_squares,
        }

        return tnt_zone

    def parse_tnt_board(self, path):
        asset = self.util.get_asset_by_path(path=path, deflate_data=True)
        data: dict = asset.get('processed_document')

        tnt_display_name: str = self.util.get_localized_string(data=data, key='displayName_translation', path=path)
        tnt_recommended_cp: int = data.get('recommendedPowerLevel')
        tnt_initial_dice_quantity: int = data.get('initialDiceQuantity')
        tnt_obtainable_normal_zone_dice_limit: int = data.get('obtainableNormalZoneDiceLimit')
        tnt_obtainable_bonus_zone_dice_limit: int = data.get('obtainableBonusZoneDiceLimit')
        tnt_normal_zone: dict = self.parse_tnt_zone(data.get('normalZone'))
        tnt_bonus_zones: list = []

        for zone in data.get('bonusZones'):
            tnt_bonus_zones.append(self.parse_tnt_zone(zone))

        tnt_rewards: list = []

        for main_reward in data.get('mainRewards'):
            loot_type: int = main_reward.get('lootType')
            reward_type: str = None

            if loot_type == 1:
                reward_type = 'consumable_item'
                reward_id: str = main_reward.get('consumableItem').get('linked_asset_id')
                reward_name: str = self.util.get_localized_string(data=main_reward.get('consumableItem'), key='displayName_translation', path=path)
                reward_description: str = self.util.get_localized_string(data=main_reward.get('consumableItem'), key='description_translation', path=path)
                reward_icon: str = self.util.get_image_path(main_reward.get('consumableItem').get('iconPath'))

                tnt_rewards.append({
                    'reward_type': reward_type,
                    'reward_id': reward_id,
                    'reward_name': reward_name,
                    'reward_description': reward_description,
                    'reward_icon': reward_icon
                })

                continue

            elif loot_type == 3:
                reward_type = 'equipment'
                reward_id: str = main_reward.get('equipment').get('linked_asset_id')
                reward_name: str = self.util.get_localized_string(data=main_reward.get('equipment').get('profile'), key='displayName_translation', path=path)
                reward_description: str = self.util.get_localized_string(data=main_reward.get('equipment').get('profile'), key='description_translation', path=path)
                reward_icon: str = self.util.get_image_path(main_reward.get('equipment').get('profile').get('iconPath'))

                tnt_rewards.append({
                    'reward_type': reward_type,
                    'reward_id': reward_id,
                    'reward_name': reward_name,
                    'reward_description': reward_description,
                    'reward_icon': reward_icon
                })

                continue

            else:
                raise NotImplementedError(loot_type)

        tntboard: dict = {
            'id': path,
            'tnt_display_name': tnt_display_name,
            'tnt_recommended_cp': tnt_recommended_cp,
            'tnt_initial_dice_quantity': tnt_initial_dice_quantity,
            'tnt_obtainable_normal_zone_dice_limit': tnt_obtainable_normal_zone_dice_limit,
            'tnt_obtainable_bonus_zone_dice_limit': tnt_obtainable_bonus_zone_dice_limit,
            'tnt_rewards': tnt_rewards,
            'tnt_normal_zone': tnt_normal_zone,
            'tnt_bonus_zones': tnt_bonus_zones
        }

        return tntboard

    def get_data(self, path):
        cache_key: str = f'{self.util.get_language_setting()}_{path}_parsed_asset'
        cached_asset: dict = self.util.get_redis_asset(cache_key=cache_key)

        if cached_asset is not None:
            return cached_asset

        asset: dict = self.parse_tnt_board(path)
        self.util.save_redis_asset(cache_key=cache_key, data=asset)

        return asset

    def seed_cache(self):
        executor = concurrent.futures.ProcessPoolExecutor(16)
        futures = [executor.submit(process_and_save_asset, path) for path in self.util.get_asset_list('SugorokuStage')]
        concurrent.futures.wait(futures)

def process_and_save_asset(path):
    data_class_instance.get_data(path=path)
