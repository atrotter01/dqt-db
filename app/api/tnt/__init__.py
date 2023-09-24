from flask import request
from flask_restx import Namespace, Resource, fields
from app.data.tnt import TnT
from app.util import Util

api = Namespace("tnt", description="")

tnt_model = api.model('tnt', {
    'id': fields.String,
    'tnt_display_name': fields.String,
    'tnt_recommended_cp': fields.Integer,
    'tnt_initial_dice_quantity': fields.Integer,
    'tnt_obtainable_normal_zone_dice_limit': fields.Integer,
    'tnt_obtainable_bonus_zone_dice_limit': fields.Integer,
    'tnt_rewards': fields.List(fields.Raw),
    'tnt_normal_zone': fields.Raw,
    'tnt_bonus_zones': fields.List(fields.Raw)
})

api.param("path", "Path")
@api.route("/")
@api.route("/<path>")
class Asset(Resource):

    util: Util
    tnt_parser: TnT
    tnt_boards: list
    cache_key: str

    @api.marshal_list_with(tnt_model)
    def get(self, path = None):
        '''Fetch a given TnT Board'''
        self.util = Util(lang=request.args.get('lang'))
        self.tnt_parser = TnT(util=self.util)
        self.tnt_boards = []

        if path is not None:
            self.tnt_boards.append(self.tnt_parser.get_data(path=path))

            return self.tnt_boards

        self.cache_key = f'{self.util.get_language_setting()}_tnt_parsed_asset'
        cached_asset = self.util.get_redis_asset(cache_key=self.cache_key)

        if cached_asset is not None:
            return cached_asset

        asset_list: list = self.util.get_asset_list('SugorokuStage')
        
        for path in asset_list:
            tnt_board: dict = self.tnt_parser.get_data(path)

            self.tnt_boards.append(tnt_board)

        self.util.save_redis_asset(cache_key=self.cache_key, data=sorted(self.tnt_boards, key=lambda d: d['tnt_display_name']))

        return sorted(self.tnt_boards, key=lambda d: d['tnt_display_name'])
