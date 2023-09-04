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

resistance_model = api.model('resistance_model', {
    'display_name': fields.String,
    'Frizz': fields.Integer,
    'Sizz': fields.Integer,
    'Crack': fields.Integer,
    'Woosh': fields.Integer,
    'Bang': fields.Integer,
    'Zap': fields.Integer,
    'Zam': fields.Integer,
    'Sleep': fields.Integer,
    'Stun': fields.Integer,
    'Paralysis': fields.Integer,
    'Poison': fields.Integer,
    'Hobble': fields.Integer,
    'Curse': fields.Integer,
    'Blind': fields.Integer,
    'Physical Lock': fields.Integer,
    'Martial Lock': fields.Integer,
    'Spell Lock': fields.Integer,
    'Breath Lock': fields.Integer,
    'Confusion': fields.Integer,
    'Charm': fields.Integer,
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
    cache_key: str

    @api.marshal_list_with(rank_up_calculator_model)
    def get(self, path = None):
        '''Fetch a given Unit'''
        self.util = Util()
        self.unit_parser = Unit(util=self.util)
        self.units = []

        self.cache_key = f'rankup_calculator_parsed_asset'
        cached_asset = self.util.get_redis_asset(cache_key=self.cache_key)

        if cached_asset is not None:
            return cached_asset

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

@api.route("/resist_table")
class UnitResistFilter(Resource):

    util: Util
    unit_parser: Unit
    units: list
    cache_key: str

    @api.marshal_list_with(resistance_model)
    def get(self, path = None):
        '''Fetch a given Unit'''
        self.util = Util()
        self.unit_parser = Unit(util=self.util)
        self.units = []

        self.cache_key = f'unit_resist_filter_parsed_asset'
        cached_asset = self.util.get_redis_asset(cache_key=self.cache_key)

        if cached_asset is not None:
            return cached_asset

        asset_list: list = self.util.get_asset_list('AllyMonster')

        for path in asset_list:
            unit = self.unit_parser.get_data(path=path)
            self.units.append({
                'display_name': unit.get('display_name'),
                'Frizz': unit.get('element_resistances').get('1').get('rate'),
                'Sizz': unit.get('element_resistances').get('2').get('rate'),
                'Crack': unit.get('element_resistances').get('3').get('rate'),
                'Woosh': unit.get('element_resistances').get('4').get('rate'),
                'Bang': unit.get('element_resistances').get('5').get('rate'),
                'Zap': unit.get('element_resistances').get('6').get('rate'),
                'Zam': unit.get('element_resistances').get('7').get('rate'),
                'Sleep': unit.get('abnormity_resistances').get('1').get('rate'),
                'Stun': unit.get('abnormity_resistances').get('2').get('rate'),
                'Paralysis': unit.get('abnormity_resistances').get('3').get('rate'),
                'Poison': unit.get('abnormity_resistances').get('4').get('rate'),
                'Hobble': unit.get('abnormity_resistances').get('5').get('rate'),
                'Curse': unit.get('abnormity_resistances').get('6').get('rate'),
                'Blind': unit.get('abnormity_resistances').get('7').get('rate'),
                'Physical Lock': unit.get('abnormity_resistances').get('8').get('rate'),
                'Martial Lock': unit.get('abnormity_resistances').get('9').get('rate'),
                'Spell Lock': unit.get('abnormity_resistances').get('10').get('rate'),
                'Breath Lock': unit.get('abnormity_resistances').get('11').get('rate'),
                'Confusion': unit.get('abnormity_resistances').get('12').get('rate'),
                'Charm': unit.get('abnormity_resistances').get('13').get('rate'),
            })

        return sorted(self.units, key=lambda d: d['display_name'])
