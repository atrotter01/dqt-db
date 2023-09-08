from flask import request
from flask_restx import Namespace, Resource, fields
from app.data.areagroup import AreaGroup
from app.util import Util

api = Namespace("area_group", description="")

area_group_model = api.model('area_group', {
    'id': fields.String,
    'area_group_display_name': fields.String,
    'area_group_banner_path': fields.String,
    'area_group_score_reward': fields.Boolean,
    'area_group_show_display_name_at_banner': fields.Boolean,
    'area_group_category': fields.Integer,
    'area_group_subcategory': fields.Integer,
    'area_group_parent': fields.String,
    'area_group_children': fields.List(fields.String)
})

api.param("path", "Path")
@api.route("/")
@api.route("/<path>")
class Asset(Resource):

    util: Util
    area_group_parser: AreaGroup
    area_groups: list
    cache_key: str

    @api.marshal_list_with(area_group_model)
    def get(self, path = None):
        '''Fetch a given Area Group'''
        self.util = Util(lang=request.args.get('lang'))
        self.area_group_parser = AreaGroup(util=self.util)
        self.area_groups = []

        if path is not None:
            self.area_groups.append(self.area_group_parser.get_data(path=path))

            return self.area_groups

        self.cache_key = f'{self.util.get_language_setting()}_area_group_parsed_asset'
        cached_asset = self.util.get_redis_asset(cache_key=self.cache_key)

        if cached_asset is not None:
            return cached_asset

        asset_list: list = []
        asset_list.extend(self.util.get_asset_list('AreaGroup'))
        asset_list.extend(self.util.get_asset_list('MemoryAreaGroup'))
        asset_list.extend(self.util.get_asset_list('MemoryAreaGroupCategory'))

        for path in asset_list:
            area_group = self.area_group_parser.get_data(path=path)

            self.area_groups.append(area_group)

        self.util.save_redis_asset(cache_key=self.cache_key, data=sorted(self.area_groups, key=lambda d: d['area_group_display_name']))

        return sorted(self.area_groups, key=lambda d: d['area_group_display_name'])
