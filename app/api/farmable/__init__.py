from flask import request
from flask_restx import Namespace, Resource, fields
from app.data.stage import Stage
from app.util import Util

api = Namespace("farmable", description="")

farmable_model = api.model('farmable', {
    'stage_id': fields.String,
    'stage_area_id': fields.String,
    'stage_area_name': fields.String,
    'stage_area_group_name': fields.String,
    'stage_display_name': fields.String,
    'stage_stamina_cost': fields.Integer,
    'enemy_id': fields.String,
    'enemy_display_name': fields.String,
    'enemy_icon': fields.String,
    'enemy_family': fields.String,
    'enemy_family_icon': fields.String,
    'enemy_role': fields.String,
    'enemy_role_icon': fields.String,
    'scout_probability': fields.Float,
    'stamina_per_drop': fields.Float,
    'stamina_per_drop_double_drop_rate': fields.Float,
    'is_best_drop_rate': fields.Boolean
})

@api.route("/")
class Asset(Resource):

    util: Util
    stage_parser: Stage
    farmables: list
    cache_key: str

    @api.marshal_list_with(farmable_model)
    def get(self, path = None):
        '''Fetch farmable units'''
        self.util = Util(lang=request.args.get('lang'))
        self.stage_parser = Stage(util=self.util)
        self.farmables = []

        self.cache_key = f'{self.util.get_language_setting()}_farmable_parsed_asset'
        cached_asset = self.util.get_redis_asset(cache_key=self.cache_key)

        if cached_asset is not None:
            return cached_asset

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

                    self.farmables.append({
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

                    self.farmables.append({
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

                    self.farmables.append({
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

        for farmable in self.farmables:
            enemy_display_name = farmable.get('enemy_display_name')
            stamina_per_drop = farmable.get('stamina_per_drop')

            if stamina_per_drop == best_drop_rate_per_unit[enemy_display_name]:
                farmable.update({ 'is_best_drop_rate': True })
            else:
                farmable.update({ 'is_best_drop_rate': False })

        self.util.save_redis_asset(cache_key=self.cache_key, data=sorted(self.farmables, key=lambda d: d['enemy_display_name']))

        return sorted(self.farmables, key=lambda d: d['enemy_display_name'])
