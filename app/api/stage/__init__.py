from flask_restx import Namespace, Resource, fields
from app.data.stage import Stage
from app.util import Util

api = Namespace("stage", description="")

stage_model = api.model('stage', {
    'id': fields.String,
    'stage_display_name': fields.String,
    'stage_sub_display_name': fields.String,
    'stage_area_id': fields.String,
    'stage_list_order': fields.Integer,
    'stage_difficulty': fields.Integer,
    'stage_recommended_cp': fields.Integer,
    'stage_stamina_cost': fields.Integer,
    'stage_talent_point_gain': fields.Integer,
    'stage_is_boss_stage': fields.Boolean,
    'stage_is_story_stage':  fields.Boolean,
    'stage_is_auto_only':  fields.Boolean,
    'stage_is_limited_total_weight':  fields.Boolean,
    'stage_limited_total_weight': fields.Integer,
    'stage_is_organization_limit_num':  fields.Boolean,
    'stage_organization_limit_num': fields.Integer,
    'stage_is_send_feed_when_first_cleared':  fields.Boolean,
    'stage_enable_score_challenge':  fields.Boolean,
    'stage_banner_path': fields.String,
    'stage_drops': fields.List(fields.Raw),
    'stage_missions': fields.List(fields.Raw),
    'stage_enemies': fields.List(fields.Raw),
    'stage_random_enemies': fields.List(fields.Raw),
    'stage_reinforcement_enemies': fields.List(fields.Raw),
})

api.param("path", "Path")
@api.route("/")
@api.route("/<path>")
class Asset(Resource):

    util: Util
    stage_parser: Stage
    stages: list
    cache_key: str

    @api.marshal_list_with(stage_model)
    def get(self, path = None):
        '''Fetch a given Stage'''
        self.util = Util()
        self.stage_parser = Stage(util=self.util)
        self.stages = []

        if path is not None:
            self.stages.append(self.stage_parser.get_data(path=path))

            return self.stages

        self.cache_key = 'stage_parsed_asset'
        cached_asset = self.util.get_redis_asset(cache_key=self.cache_key)

        if cached_asset is not None:
            return cached_asset

        asset_list: list = self.util.get_asset_list('Stage')
        failure: bool = False

        for path in asset_list:
            try:
                stage = self.stage_parser.get_data(path)
            except Exception as ex:
                print(f'Failed to process {path}.')
                failure = True
                #raise ex

            self.stages.append(stage)

        assert failure is False, 'Failed to process stages.'
        self.util.save_redis_asset(cache_key=self.cache_key, data=sorted(self.stages, key=lambda d: d['stage_display_name']))

        return sorted(self.stages, key=lambda d: d['stage_display_name'])
