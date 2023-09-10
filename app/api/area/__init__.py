from flask import request
from flask_restx import Namespace, Resource, fields
from app.data.area import Area
from app.util import Util

api = Namespace("area", description="")

area_model = api.model('area', {
    'id': fields.String,
    'area_group': fields.String,
    'area_display_name': fields.String,
    'area_sub_display_name': fields.String,
    'area_group_name': fields.String,
    'area_category': fields.Integer,
    'area_sub_category': fields.Integer,
    'area_stage_display_type': fields.Integer,
    'area_list_order': fields.Integer,
    'area_banner_path': fields.String,
    'area_show_display_name_at_banner': fields.Boolean,
    'area_achievement_target_name': fields.String,
    'area_has_schedule': fields.Boolean,
    'area_is_condition_clear_visible': fields.Boolean,
    'area_skip_ticket_unusable': fields.Boolean,
    'area_is_demons_tower': fields.Boolean,
    'area_hide_when_completed': fields.Boolean,
    'area_is_notification_displayable': fields.Boolean,
    'area_reset_type': fields.Integer,
    'area_number_of_stages_back': fields.Integer,
    'area_available_monster_families': fields.List(fields.Raw),
    'area_available_monsters': fields.List(fields.Raw),
})

api.param("path", "Path")
@api.route("/")
@api.route("/<path>")
class Asset(Resource):

    util: Util
    area_parser: Area
    areas: list
    cache_key: str

    @api.marshal_list_with(area_model)
    def get(self, path = None):
        '''Fetch a given Area'''
        self.util = Util(lang=request.args.get('lang'))
        self.area_parser = Area(util=self.util)
        self.areas = []

        if path is not None:
            self.areas.append(self.area_parser.get_data(path=path))

            return self.areas

        self.cache_key = f'{self.util.get_language_setting()}_area_parsed_asset'
        cached_asset = self.util.get_redis_asset(cache_key=self.cache_key)

        if cached_asset is not None:
            return cached_asset

        asset_list: list = self.util.get_asset_list('Area')

        for path in asset_list:
            area = self.area_parser.get_data(path=path)

            self.areas.append(area)

        self.util.save_redis_asset(cache_key=self.cache_key, data=sorted(self.areas, key=lambda d: d['area_display_name']))

        return sorted(self.areas, key=lambda d: d['area_display_name'])
