from flask_restx import Namespace, Resource, fields
from app.util import Util
from app.data.unit import Unit

api = Namespace("unit", description="")

unit_model = api.model('unit', {
    'id': fields.String,
    'display_name': fields.String,
    'flavor_text': fields.String,
    'weight': fields.String,
    'move': fields.Integer,
    'unit_rank': fields.String,
    'unit_rank_icon': fields.String,
    'allow_nicknaming': fields.Boolean,
    'almanac_visible': fields.Boolean,
    'almanac_number': fields.Integer,
    'max_cp': fields.Integer,
    'is_quest_reward': fields.Boolean,
    'is_gacha_unit': fields.Boolean,
    'rank_up_table': fields.List(fields.Raw),
    'element_resistances': fields.Raw,
    'abnormity_resistances': fields.Raw,
    'stats_by_level': fields.List(fields.Raw),
    'family': fields.String,
    'family_icon': fields.String,
    'role': fields.String,
    'role_icon': fields.String,
    'unit_icon': fields.String,
    'transformed_unit_icon': fields.String,
    'active_skills': fields.List(fields.Raw),
    'passive_skills': fields.List(fields.Raw),
    'awakening_passive_skills': fields.List(fields.Raw),
    'reaction_passive_skills': fields.List(fields.Raw),
    'awakening_reaction_passive_skills': fields.List(fields.Raw),
    'has_battleroad': fields.Boolean,
    'has_blossom': fields.Boolean,
    'has_character_builder': fields.Boolean,
    'blossoms': fields.List(fields.Raw),
    'character_builder_blossoms': fields.List(fields.Raw)
})

rank_up_calculator_model = api.model('rank_up_calculator', {
    'id': fields.String,
    'display_name': fields.String,
    'unit_icon': fields.String,
    'almanac_number': fields.Integer,
    'rank_up_table': fields.List(fields.Raw),
})

@api.param("path", "Path")
@api.route("/")
@api.route("/<path>")
class Asset(Resource):

    util: Util
    unit_parser: Unit
    units: list
    cache_key: str

    @api.marshal_list_with(unit_model)
    def get(self, path = None):
        '''Fetch a given Unit'''
        self.util = Util()
        self.unit_parser = Unit(util=self.util)
        self.units = []

        if path is not None:
            profile_map: dict = self.util.get_redis_asset('profile_unit_map_parsed_asset')

            if profile_map.get(path) is not None:
                path = profile_map.get(path)

            self.units.append(self.unit_parser.get_data(path=path))

            return self.units

        self.cache_key = f'unit_parsed_asset'
        cached_asset = self.util.get_redis_asset(cache_key=self.cache_key)

        if cached_asset is not None:
            return cached_asset

        asset_list: list = self.util.get_asset_list('AllyMonster')

        for path in asset_list:
            unit = self.unit_parser.get_data(path=path)
            self.units.append(unit)

        self.util.save_redis_asset(cache_key=self.cache_key, data=sorted(self.units, key=lambda d: d['almanac_number']))

        return sorted(self.units, key=lambda d: d['almanac_number'])

@api.route("/rankup_calculator")
class RankUpCalculator(Resource):

    util: Util
    unit_parser: Unit
    units: list

    @api.marshal_list_with(rank_up_calculator_model)
    def get(self, path = None):
        '''Fetch a given Unit'''
        self.util = Util()
        self.unit_parser = Unit(util=self.util)
        self.units = []

        asset_list: list = self.util.get_asset_list('AllyMonster')

        for path in asset_list:
            unit = self.unit_parser.get_data(path=path)
            self.units.append({
                'id': unit.get('id'),
                'display_name': unit.get('display_name'),
                'almanac_number': unit.get('almanac_number'),
                'unit_icon': unit.get('unit_icon'),
                'rank_up_table': unit.get('rank_up_table')
            })

        return sorted(self.units, key=lambda d: d['almanac_number'])
