from flask import request
from flask_restx import Namespace, Resource, fields
from app.util import Util
from app.data.farmable import Farmable

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

majellan_bot_model = api.model('farmable', {
    'stage_area_name': fields.String,
    'stage_area_group_name': fields.String,
    'stage_display_name': fields.String,
    'enemy_display_name': fields.String,
    'scout_probability': fields.Float,
    'stamina_per_drop': fields.Float,
    'is_best_drop_rate': fields.Boolean
})

@api.route("/")
class FarmableApi(Resource):

    util: Util
    cache_key: str
    farmables: list

    @api.marshal_list_with(farmable_model)
    def get(self):
        self.util = Util(lang=request.args.get('lang'))
        self.cache_key = f'{self.util.get_language_setting()}_farmable_parsed_asset'

        cached_asset = self.util.get_redis_asset(cache_key=self.cache_key)

        if cached_asset is not None:
            return cached_asset

        farmable: Farmable = Farmable(util=self.util)
        self.farmables = farmable.get_data()

        self.util.save_redis_asset(cache_key=self.cache_key, data=sorted(self.farmables, key=lambda d: d['enemy_display_name']))

        return sorted(self.farmables, key=lambda d: d['almanac_number'])

@api.route("/majellan_bot")
class Majellan(Resource):

    util: Util
    cache_key: str
    farmables: list

    @api.marshal_list_with(majellan_bot_model)
    def get(self):
        self.util = Util(lang=request.args.get('lang'))
        self.cache_key = f'{self.util.get_language_setting()}_farmable_parsed_asset'

        cached_asset = self.util.get_redis_asset(cache_key=self.cache_key)

        if cached_asset is not None:
            return cached_asset

        farmable: Farmable = Farmable(util=self.util)
        self.farmables = farmable.get_data()

        self.util.save_redis_asset(cache_key=self.cache_key, data=sorted(self.farmables, key=lambda d: d['enemy_display_name']))

        return sorted(self.farmables, key=lambda d: d['almanac_number'])
