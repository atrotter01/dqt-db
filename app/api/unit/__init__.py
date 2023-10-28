from flask import request
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
    'small_family_icon': fields.String,
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

majellan_bot_model = api.model('unit', {
    'id': fields.String,
    'display_name': fields.String,
    'weight': fields.String,
    'unit_rank': fields.String,
    'unit_rank_icon': fields.String,
    'family': fields.String,
    'family_icon': fields.String,
    'small_family_icon': fields.String,
    'role': fields.String,
    'role_icon': fields.String,
    'unit_icon': fields.String,
    'has_battleroad': fields.Boolean,
    'has_blossom': fields.Boolean,
    'has_character_builder': fields.Boolean,
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
    master_rank: int = 1
    awakening: int = 0
    single_unit: bool = False

    @api.marshal_list_with(unit_model)
    def get(self, path = None):
        '''Fetch a given Unit'''
        self.util = Util(lang=request.args.get('lang'))
        self.unit_parser = Unit(util=self.util)
        self.units = []

        if request.args.get('master_rank') is not None:
            self.master_rank = int(request.args.get('master_rank'))

        if request.args.get('awakening') is not None:
            self.awakening = int(request.args.get('awakening'))

        if path is not None:
            profile_map: dict = self.util.get_redis_asset(f'{self.util.get_language_setting()}_profile_unit_map_parsed_asset')
            self.single_unit = True

            if profile_map is not None:
                if profile_map.get(path) is not None:
                    path = profile_map.get(path)

            self.units.append(self.unit_parser.get_data(path=path))

        else:
            self.cache_key = f'{self.util.get_language_setting()}_unit_parsed_asset'
            cached_asset = self.util.get_redis_asset(cache_key=self.cache_key)

            if cached_asset is not None:
                self.units = cached_asset
            else:
                asset_list: list = self.util.get_asset_list('AllyMonster')

                for path in asset_list:
                    unit = self.unit_parser.get_data(path=path)
                    self.units.append(unit)

                self.util.save_redis_asset(cache_key=self.cache_key, data=sorted(self.units, key=lambda d: d['almanac_number']))

        stat_increase_table = self.util.get_asset_by_path(path='-5945447399125289372', deflate_data=True, build_processed_asset=True)
        stat_increase_table_document = stat_increase_table.get('processed_document')
        master_rank: int = 1
        global_stat_multipliers: list = []
        global_stat_additives: list = []

        for item in stat_increase_table_document.get('items'):
            if master_rank == self.master_rank:
                passive_skill = item.get('passiveSkill')
                stat_increase_path = passive_skill.get('passiveSkillStatusMulEffectMasterData').get('m_PathID')
                stat_increase_asset = self.util.get_asset_by_path(path=stat_increase_path, deflate_data=True, build_processed_asset=True)
                stat_increase_document = stat_increase_asset.get('processed_document')
                stat_increase = stat_increase_document.get('statusIncrease')
                global_stat_multipliers.append(stat_increase)

                break
            else:
                master_rank = master_rank + 1
                continue

        for unit in self.units:
            start_index: int = -1

            if self.single_unit is True:
                start_index = 0

            for level in unit.get('stats_by_level')[start_index:]:
                level_number = level.get('level')

                for key in level.keys():
                    if key == 'level':
                        continue

                    multiplier: int = 1
                    stat_key = key

                    if key == 'defense':
                        stat_key = 'defence'

                    for rank in unit.get('rank_up_table'):
                        if level_number > rank.get('rank_level_cap'):
                            level.update({ key: level.get(key) + rank.get('stats_increase').get(key) })

                    for panel in unit.get('blossoms'):
                        if panel.get('panel_stat_additives') is not None:
                            level.update({ key: level.get(key) + panel.get('panel_stat_additives').get(stat_key) })

                        if panel.get('type') == 'Passive Skill':
                            if panel.get('data').get('skill_stat_additives') is not None:
                                level.update({ key: level.get(key) + panel.get('data').get('skill_stat_additives').get(stat_key) })

                    for panel in unit.get('character_builder_blossoms'):
                        if panel.get('panel_stat_additives') is not None:
                            level.update({ key: level.get(key) + panel.get('panel_stat_additives').get(stat_key) })

                        if panel.get('type') == 'Passive Skill':
                            if panel.get('data').get('skill_stat_additives') is not None:
                                level.update({ key: level.get(key) + panel.get('data').get('skill_stat_additives').get(stat_key) })

                    for passive_skill in unit.get('passive_skills'):
                        if passive_skill.get('skill_stat_additives') is not None:
                            if passive_skill.get('skill_stat_additives').get(stat_key) is not None:
                                level.update({ key: level.get(key) + passive_skill.get('skill_stat_additives').get(stat_key) })

                    for passive_skill in unit.get('awakening_passive_skills'):
                        if int(passive_skill.get('awakening_level'))  > self.awakening:
                            continue

                        if passive_skill.get('skill_stat_additives') is not None:
                            if passive_skill.get('skill_stat_additives').get(stat_key) is not None:
                                level.update({ key: level.get(key) + passive_skill.get('skill_stat_additives').get(stat_key) })

                    for passive_skill in unit.get('awakening_passive_skills'):
                        if int(passive_skill.get('awakening_level'))  > self.awakening:
                            continue

                        if passive_skill.get('skill_stat_multipliers') is not None:
                            if passive_skill.get('skill_stat_multipliers').get(stat_key) is not None:
                                multiplier = multiplier + (passive_skill.get('skill_stat_multipliers').get(stat_key) / 100)

                    for passive_skill in unit.get('passive_skills'):
                        if passive_skill.get('skill_stat_multipliers') is not None:
                            if passive_skill.get('skill_stat_multipliers').get(stat_key) is not None:
                                multiplier = multiplier + (passive_skill.get('skill_stat_multipliers').get(stat_key) / 100)

                    for stat_increase in global_stat_multipliers:
                        multiplier = multiplier + (stat_increase.get(stat_key) / 100)

                    level.update({ key: level.get(key) * multiplier })
                    level.update({ key: int(level.get(key)) })

        return sorted(self.units, key=lambda d: d['almanac_number'])

@api.route("/majellan_bot")
class Majellan(Resource):

    util: Util
    unit_parser: Unit
    units: list
    cache_key: str

    @api.marshal_list_with(majellan_bot_model)
    def get(self, path = None):
        '''Fetch a given Unit'''
        self.util = Util(lang=request.args.get('lang'))
        self.unit_parser = Unit(util=self.util)
        self.units = []

        self.cache_key = f'{self.util.get_language_setting()}_unit_parsed_asset'
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
        self.util = Util(lang=request.args.get('lang'))
        self.unit_parser = Unit(util=self.util)
        self.units = []

        self.cache_key = f'{self.util.get_language_setting()}_rankup_calculator_parsed_asset'
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
        self.util = Util(lang=request.args.get('lang'))
        self.unit_parser = Unit(util=self.util)
        self.units = []

        self.cache_key = f'{self.util.get_language_setting()}_unit_resist_filter_parsed_asset'
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
