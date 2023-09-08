from flask import request
from flask_restx import Namespace, Resource, fields
from app.util import Util
from app.data.equipment import Equipment

api = Namespace("equipment", description="")

equipment_model = api.model('equipment', {
    'id': fields.String,
    'equipment_display_name': fields.String,
    'equipment_description': fields.String,
    'equipment_icon': fields.String,
    'equipment_rank_icon': fields.String,
    'equipment_rank': fields.String,
    'equipment_alchemy_cost': fields.String,
    'equipment_type_icon': fields.String,
    'equipment_type': fields.String,
    'equipment_category_icon': fields.String,
    'equipment_category': fields.String,
    'equipment_is_free_alchemy': fields.Boolean,
    'equipment_equipable_roles': fields.List(fields.String),
    'equipment_status_increase': fields.Raw,
    'equipment_passive_skill': fields.Raw,
    'equipment_reaction_skill': fields.Raw,
    'equipment_alchemy_slots': fields.Raw,
})

@api.param("path", "Path")
@api.route("/")
@api.route("/<path>")
class Asset(Resource):

    util: Util
    equipments: list
    cache_key: str
    equipment_parser: Equipment

    @api.marshal_list_with(equipment_model)
    def get(self, path = None):
        '''Fetch a given Equipment'''
        self.util = Util(lang=request.args.get('lang'))
        self.equipment_parser = Equipment(util=self.util)
        self.equipments = []

        if path is not None:
            self.equipments.append(self.equipment_parser.get_data(path=path))

            return self.equipments

        self.cache_key = f'{self.util.get_language_setting()}_equipment_parsed_asset'
        cached_asset = self.util.get_redis_asset(cache_key=self.cache_key)

        if cached_asset is not None:
            return cached_asset

        asset_list: list = self.util.get_asset_list('Equipment')

        for path in asset_list:
            equipment = self.equipment_parser.get_data(path=path)
            self.equipments.append(equipment)

        self.util.save_redis_asset(cache_key=self.cache_key, data=sorted(self.equipments, key=lambda d: d['equipment_display_name']))

        return sorted(self.equipments, key=lambda d: d['equipment_display_name'])
