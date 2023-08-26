from flask_restx import Namespace, Resource, fields
from app.data.enemymonster import EnemyMonster
from app.util import Util

api = Namespace("enemy_monster", description="")

enemy_monster_model = api.model('enemy_monster', {
    'id': fields.String,
    'enemy_display_name': fields.String,
    'enemy_level': fields.Integer,
    'enemy_hp': fields.Integer,
    'enemy_mp': fields.Integer,
    'enemy_attack': fields.Integer,
    'enemy_defense': fields.Integer,
    'enemy_intelligence': fields.Integer,
    'enemy_agility': fields.Integer,
    'enemy_mobility': fields.Integer,
    'enemy_weight': fields.Integer,
    'enemy_is_strong_enemy': fields.Boolean,
    'enemy_is_unique_monster': fields.Integer,
    'enemy_scout_probability': fields.Integer,
    'enemy_is_rare_scout': fields.Integer,
    'enemy_flavor_text': fields.String,
    'enemy_family': fields.String,
    'enemy_family_icon': fields.String,
    'enemy_role': fields.String,
    'enemy_role_icon': fields.String,
    'enemy_unit_icon': fields.String,
    'enemy_transformed_unit_icon': fields.String,
    'enemy_active_skills': fields.List(fields.Raw),
    'enemy_passive_skills': fields.List(fields.Raw),
    'enemy_reaction_skills': fields.List(fields.Raw),
    'enemy_element_resistance': fields.Raw,
    'enemy_abnormity_resistance': fields.Raw,
    'enemy_drops': fields.List(fields.Raw)
})

api.param("path", "Path")
@api.route("/")
@api.route("/<path>")
class Asset(Resource):

    util: Util
    enemy_monster_parser: EnemyMonster
    enemy_monsters: list
    cache_key: str

    @api.marshal_list_with(enemy_monster_model)
    def get(self, path = None):
        '''Fetch a given Enemy Monster'''
        self.util = Util()
        self.enemy_monster_parser = EnemyMonster(util=self.util)
        self.enemy_monsters = []

        if path is not None:
            self.enemy_monsters.append(self.enemy_monster_parser.get_data(path=path))

            return self.enemy_monsters

        self.cache_key = f'enemy_monster_parsed_asset'
        cached_asset = self.util.get_redis_asset(cache_key=self.cache_key)

        if cached_asset is not None:
            return cached_asset

        asset_list: list = self.util.get_asset_list('EnemyMonster')

        for path in asset_list:
            enemy_monster = self.enemy_monster_parser.get_data(path=path)
            self.enemy_monsters.append(enemy_monster)

        self.util.save_redis_asset(cache_key=self.cache_key, data=sorted(self.enemy_monsters, key=lambda d: d['enemy_display_name']))

        return sorted(self.enemy_monsters, key=lambda d: d['enemy_display_name'])
