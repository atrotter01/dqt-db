from app.util import Util
from app.data.stage import Stage

data_class_instance = None

class Farmable:

    util: Util
    stage_parser: Stage

    def __init__(self, util):
        self.util = util
        self.stage_parser = Stage(util=self.util)
        globals()['data_class_instance'] = self

        return

    def build_farmable_list(self):
        farmables: list = []

        asset_list: list = self.util.get_asset_list('Stage')
        best_drop_rate_per_unit: dict = {}

        for path in asset_list:
            stage = self.stage_parser.get_data(path)
            stage_id: str = stage.get('id')
            stage_area_id: str = stage.get('stage_area_id')
            stage_area_name: str = stage.get('stage_area_name')
            stage_area_group_name: str = stage.get('stage_area_group_name')
            stage_display_name: str = stage.get('stage_display_name')
            stage_stamina_cost: int = stage.get('stage_stamina_cost')
            seen_units: list = []

            for enemy in stage.get('stage_enemies'):
                enemy_id: str = enemy.get('monster').get('id')
                enemy_display_name: str = enemy.get('monster').get('enemy_display_name')
                enemy_icon: str = enemy.get('monster').get('enemy_unit_icon')
                enemy_family: str = enemy.get('monster').get('enemy_family')
                enemy_family_icon: str = enemy.get('monster').get('enemy_family_icon')
                enemy_role: str = enemy.get('monster').get('enemy_role')
                enemy_role_icon: str = enemy.get('monster').get('enemy_role_icon')
                scout_probability: float = float(enemy.get('monster').get('enemy_scout_probability'))

                unit_key: str = f'{stage_id}_{enemy_id}'

                if unit_key in seen_units:
                    continue

                seen_units.append(unit_key)

                if scout_probability > 0:
                    stamina_per_drop: float = round((100 / scout_probability) * stage_stamina_cost, 2)
                    stamina_per_double_drop_rate: float = round((100 / (scout_probability * 2)) * stage_stamina_cost, 2)

                    if best_drop_rate_per_unit.get(enemy_display_name) is None:
                        best_drop_rate_per_unit[enemy_display_name] = stamina_per_drop

                    if stamina_per_drop < best_drop_rate_per_unit[enemy_display_name]:
                        best_drop_rate_per_unit[enemy_display_name] = stamina_per_drop

                    farmables.append({
                        'stage_id': stage_id,
                        'stage_area_id': stage_area_id,
                        'stage_area_name': stage_area_name,
                        'stage_area_group_name': stage_area_group_name,
                        'stage_display_name': stage_display_name,
                        'stage_stamina_cost': stage_stamina_cost,
                        'enemy_id': enemy_id,
                        'enemy_display_name': enemy_display_name,
                        'enemy_icon': enemy_icon,
                        'enemy_family': enemy_family,
                        'enemy_family_icon': enemy_family_icon,
                        'enemy_role': enemy_role,
                        'enemy_role_icon': enemy_role_icon,
                        'scout_probability': scout_probability,
                        'stamina_per_drop': stamina_per_drop,
                        'stamina_per_drop_double_drop_rate': stamina_per_double_drop_rate,
                    })

            for enemy in stage.get('stage_random_enemies'):
                enemy_id: str = enemy.get('monster').get('id')
                enemy_display_name: str = enemy.get('monster').get('enemy_display_name')
                enemy_icon: str = enemy.get('monster').get('enemy_unit_icon')
                enemy_family: str = enemy.get('monster').get('enemy_family')
                enemy_family_icon: str = enemy.get('monster').get('enemy_family_icon')
                enemy_role: str = enemy.get('monster').get('enemy_role')
                enemy_role_icon: str = enemy.get('monster').get('enemy_role_icon')
                scout_probability: float = float(enemy.get('monster').get('enemy_scout_probability'))

                unit_key: str = f'{stage_id}_{enemy_id}'

                if unit_key in seen_units:
                    continue

                seen_units.append(unit_key)

                if scout_probability > 0:
                    stamina_per_drop: float = round((100 / scout_probability) * stage_stamina_cost, 2)
                    stamina_per_double_drop_rate: float = round((100 / (scout_probability * 2)) * stage_stamina_cost, 2)

                    if best_drop_rate_per_unit.get(enemy_display_name) is None:
                        best_drop_rate_per_unit[enemy_display_name] = stamina_per_drop

                    if stamina_per_drop < best_drop_rate_per_unit[enemy_display_name]:
                        best_drop_rate_per_unit[enemy_display_name] = stamina_per_drop

                    farmables.append({
                        'stage_id': stage_id,
                        'stage_area_id': stage_area_id,
                        'stage_area_name': stage_area_name,
                        'stage_area_group_name': stage_area_group_name,
                        'stage_display_name': stage_display_name,
                        'stage_stamina_cost': stage_stamina_cost,
                        'enemy_id': enemy_id,
                        'enemy_display_name': enemy_display_name,
                        'enemy_icon': enemy_icon,
                        'enemy_family': enemy_family,
                        'enemy_family_icon': enemy_family_icon,
                        'enemy_role': enemy_role,
                        'enemy_role_icon': enemy_role_icon,
                        'scout_probability': scout_probability,
                        'stamina_per_drop': stamina_per_drop,
                        'stamina_per_drop_double_drop_rate': stamina_per_double_drop_rate,
                    })

            for enemy in stage.get('stage_reinforcement_enemies'):
                enemy_id: str = enemy.get('monster').get('id')
                enemy_display_name: str = enemy.get('monster').get('enemy_display_name')
                enemy_icon: str = enemy.get('monster').get('enemy_unit_icon')
                enemy_family: str = enemy.get('monster').get('enemy_family')
                enemy_family_icon: str = enemy.get('monster').get('enemy_family_icon')
                enemy_role: str = enemy.get('monster').get('enemy_role')
                enemy_role_icon: str = enemy.get('monster').get('enemy_role_icon')
                scout_probability: float = float(enemy.get('monster').get('enemy_scout_probability'))

                unit_key: str = f'{stage_id}_{enemy_id}'

                if unit_key in seen_units:
                    continue

                seen_units.append(unit_key)

                if scout_probability > 0:
                    stamina_per_drop: float = round((100 / scout_probability) * stage_stamina_cost, 2)
                    stamina_per_double_drop_rate: float = round((100 / (scout_probability * 2)) * stage_stamina_cost, 2)

                    if best_drop_rate_per_unit.get(enemy_display_name) is None:
                        best_drop_rate_per_unit[enemy_display_name] = stamina_per_drop

                    if stamina_per_drop < best_drop_rate_per_unit[enemy_display_name]:
                        best_drop_rate_per_unit[enemy_display_name] = stamina_per_drop

                    farmables.append({
                        'stage_id': stage_id,
                        'stage_area_id': stage_area_id,
                        'stage_area_name': stage_area_name,
                        'stage_area_group_name': stage_area_group_name,
                        'stage_display_name': stage_display_name,
                        'stage_stamina_cost': stage_stamina_cost,
                        'enemy_id': enemy_id,
                        'enemy_display_name': enemy_display_name,
                        'enemy_icon': enemy_icon,
                        'enemy_family': enemy_family,
                        'enemy_family_icon': enemy_family_icon,
                        'enemy_role': enemy_role,
                        'enemy_role_icon': enemy_role_icon,
                        'scout_probability': scout_probability,
                        'stamina_per_drop': stamina_per_drop,
                        'stamina_per_drop_double_drop_rate': stamina_per_double_drop_rate,
                    })

        for farmable in farmables:
            enemy_display_name = farmable.get('enemy_display_name')
            stamina_per_drop = farmable.get('stamina_per_drop')

            if stamina_per_drop == best_drop_rate_per_unit[enemy_display_name]:
                farmable.update({ 'is_best_drop_rate': True })
            else:
                farmable.update({ 'is_best_drop_rate': False })

        return farmables

    def get_data(self):
        cache_key = f'{self.util.get_language_setting()}_farmable_parsed_asset'
        cached_asset = self.util.get_redis_asset(cache_key=cache_key)

        if cached_asset is not None:
            return cached_asset

        farmables = self.build_farmable_list()

        self.util.save_redis_asset(cache_key=cache_key, data=sorted(farmables, key=lambda d: d['enemy_display_name']))

        return farmables