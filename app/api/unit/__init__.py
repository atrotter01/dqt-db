from flask_restx import Namespace, Resource, fields
from app.util import Util
from app.data.unit import Unit

api = Namespace("unit", description="")

unit_model = api.model('unit', {
    'id': fields.Integer,
    'display_name': fields.String,
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
    'blossoms': fields.List(fields.Raw),
    'character_builder_blossoms': fields.List(fields.Raw)
})

@api.param("path", "Path")
@api.route("/")
@api.route("/<path>")
class Asset(Resource):

    util: Util
    unit_parser: Unit
    units: list

    @api.marshal_list_with(unit_model)
    def get(self, path = None):
        '''Fetch a given Unit'''
        self.util = Util()
        self.unit_parser = Unit(util=self.util)
        self.units = []

        if path is not None:
            self.units.append(self.unit_parser.get_data(path=path))

            return self.units

        asset_list: list = self.util.get_asset_list('AllyMonster')

        for path in asset_list:
            unit = self.unit_parser.get_data(path=path)
            self.units.append(unit)

        return sorted(self.units, key=lambda d: d['almanac_number'])
