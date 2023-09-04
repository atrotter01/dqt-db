from flask_restx import Namespace, Resource, fields
from app.util import Util
from app.data.skill import Skill

api = Namespace("skill", description="")

active_skill_model = api.model('active_skill', {
    'id': fields.String,
    'level_learned': fields.Integer,
    'skill_name': fields.String,
    'skill_description': fields.String,
    'skill_button_icon': fields.String,
    'skill_rank': fields.String,
    'skill_rank_icon': fields.String,
    'skill_range_icon': fields.String,
    'skill_reach': fields.String,
    'skill_element': fields.String,
    'skill_element_icon': fields.String,
    'skill_wave_immune': fields.Boolean,
    'skill_ignore_reflect': fields.Boolean,
    'skill_ignore_death_endurance': fields.Boolean,
    'skill_ignores_damage_reduction': fields.Boolean,
    'skill_surehit': fields.Boolean,
    'skill_ignore_spell_invalid': fields.Boolean,
    'skill_threshold_of_intelligence': fields.Integer,
    'skill_threshold_of_attack': fields.Integer,
    'skill_mp_cost': fields.Integer,
    'skill_is_swap_skill': fields.Boolean,
    'skill_is_special': fields.Boolean,
    'skill_times_available': fields.Integer,
    'skill_turns_needed': fields.Integer,
    'skill_num_attacks': fields.Integer,
    'skill_is_random_target': fields.Boolean,
    'skill_base_damage': fields.Integer,
    'skill_min_damage': fields.Integer,
    'skill_max_damage': fields.Integer,
    'skill_multiplier': fields.Float,
    'skill_action_type': fields.Integer,
    'skill_type': fields.String, 
    'skill_target_type': fields.Integer,
    'skill_status_effect_parameter_name': fields.String,
    'skill_damage_calculation_type': fields.Integer,
    'skill_enhancements': fields.List(fields.Raw),
    'type_of_skill': fields.String
})

passive_skill_model = api.model('passive_skill', {
    'id': fields.String,
    'level_learned': fields.Integer,
    'skill_name': fields.String,
    'skill_description': fields.String,
    'skill_is_invisible': fields.Boolean,
    'skill_is_pve_only': fields.Boolean,
    'ally_skill_icon': fields.String,
    'enemy_skill_icon': fields.String,
    'type_of_skill': fields.String
})

reaction_skill_model = api.model('reaction_skill', {
    'id': fields.String,
    'level_learned': fields.Integer,
    'skill_name': fields.String,
    'skill_description': fields.String,
    'skill_is_invisible': fields.Boolean,
    'skill_is_pve_only': fields.Boolean,
    'skill_times_available': fields.Integer,
    'skill_accuracy': fields.Integer,
    'skill_attacker_is_enemy': fields.Boolean,
    'skill_attacker_is_self': fields.Boolean,
    'skill_attacker_is_ally': fields.Boolean,
    'skill_receiver_is_enemy': fields.Boolean,
    'skill_receiver_is_self': fields.Boolean,
    'skill_receiver_is_ally': fields.Boolean,
    'skill_is_activated_by_damage': fields.Boolean,
    'skill_is_activated_by_recovery': fields.Boolean,
    'skill_is_activated_by_abnormity': fields.Boolean,
    'skill_is_activated_by_death': fields.Boolean,
    'skill_reaction_target': fields.String,
    'skill_multiple_activation_to_same_target': fields.Boolean,
    'skill_is_re_reactionable': fields.Boolean,
    'skill_applicable_abnormity_types': fields.List(fields.Raw),
    'skill_related_active_skill_name': fields.String,
    'skill_related_active_skill_id': fields.String,
    'type_of_skill': fields.String
})

@api.param("path", "Path")
@api.route("/active_skill")
@api.route("/active_skill/<path>")
class ActiveSkill(Resource):

    util: Util
    skill_parser: Skill
    skills: list
    cache_key: str

    @api.marshal_list_with(active_skill_model)
    def get(self, path = None):
        '''Fetch a given Skill'''
        self.util = Util()
        self.skill_parser = Skill(util=self.util)
        self.skills = []

        if path is not None:
            self.skills.append(self.skill_parser.get_active_skill(path=path))

            return self.skills

        self.cache_key = 'active_skills_parsed_asset'
        cached_asset = self.util.get_redis_asset(cache_key=self.cache_key)

        if cached_asset is not None:
            return cached_asset

        asset_list: list = []
        asset_list.extend(self.util.get_asset_list('ActiveSkill'))
        asset_list.extend(self.util.get_asset_list('GuestSkill'))
        asset_list.extend(self.util.get_asset_list('NotUseSkill'))

        for path in asset_list:
            skill = self.skill_parser.get_active_skill(path=path)

            if skill.get('skill_name') is not None and skill.get('skill_name') != '':
                self.skills.append(skill)

        self.util.save_redis_asset(cache_key=self.cache_key, data=sorted(self.skills, key=lambda d: d['skill_name']))

        return sorted(self.skills, key=lambda d: d['skill_name'])

@api.param("path", "Path")
@api.route("/passive_skill")
@api.route("/passive_skill/<path>")
class PassiveSkill(Resource):

    util: Util
    skill_parser: Skill
    skills: list
    cache_key: str

    @api.marshal_list_with(passive_skill_model)
    def get(self, path = None):
        '''Fetch a given Skill'''
        self.util = Util()
        self.skill_parser = Skill(util=self.util)
        self.skills = []

        if path is not None:
            self.skills.append(self.skill_parser.get_passive_skill(path=path))

            return self.skills

        self.cache_key = 'passive_skills_parsed_asset'
        cached_asset = self.util.get_redis_asset(cache_key=self.cache_key)

        if cached_asset is not None:
            return cached_asset

        asset_list: list = []
        asset_list.extend(self.util.get_asset_list('LeaderPassive'))
        asset_list.extend(self.util.get_asset_list('ReactionPassive'))
        asset_list.extend(self.util.get_asset_list('NotUsePassiveSkill'))
        asset_list.extend(self.util.get_asset_list('PassiveSkill'))

        for path in self.util.get_asset_list('PS'):
            asset = self.util.get_asset_by_path(path)

            if asset.get('processed_document').get('passiveSkillName') is not None:
                asset_list.append(path)

        for path in self.util.get_asset_list('EquipmentPassive'):
            asset = self.util.get_asset_by_path(path)

            if asset.get('processed_document').get('passiveSkillName') is not None:
                asset_list.append(path)

        for path in self.util.get_asset_list('MS'):
            asset = self.util.get_asset_by_path(path)

            if asset.get('processed_document').get('passiveSkillName') is not None:
                asset_list.append(path)

        for path in asset_list:
            skill = self.skill_parser.get_passive_skill(path=path)

            if skill.get('skill_name') is not None and skill.get('skill_name') != '':
                self.skills.append(skill)

        self.util.save_redis_asset(cache_key=self.cache_key, data=sorted(self.skills, key=lambda d: d['skill_name']))

        return sorted(self.skills, key=lambda d: d['skill_name'])

@api.param("path", "Path")
@api.route("/reaction_skill")
@api.route("/reaction_skill/<path>")
class ReactionSkill(Resource):

    util: Util
    skill_parser: Skill
    skills: list
    cache_key: str

    @api.marshal_list_with(reaction_skill_model)
    def get(self, path = None):
        '''Fetch a given Skill'''
        self.util = Util()
        self.skill_parser = Skill(util=self.util)
        self.skills = []

        if path is not None:
            self.skills.append(self.skill_parser.get_reaction_skill(path=path))

            return self.skills

        self.cache_key = 'reaction_skills_parsed_asset'
        cached_asset = self.util.get_redis_asset(cache_key=self.cache_key)

        if cached_asset is not None:
            return cached_asset

        asset_list: list = []
        asset_list.extend(self.util.get_asset_list('ReactionPassiveSkill'))

        for path in asset_list:
            skill = self.skill_parser.get_reaction_skill(path=path)

            if skill.get('skill_name') is not None and skill.get('skill_name') != '':
                self.skills.append(skill)

        self.util.save_redis_asset(cache_key=self.cache_key, data=sorted(self.skills, key=lambda d: d['skill_name']))

        return sorted(self.skills, key=lambda d: d['skill_name'])

@api.param("path", "Path")
@api.route("/enemy_skill")
@api.route("/enemy_skill/<path>")
class EnemySkill(Resource):

    util: Util
    skill_parser: Skill
    skills: list
    cache_key: str

    @api.marshal_list_with(active_skill_model)
    def get(self, path = None):
        '''Fetch a given Skill'''
        self.util = Util()
        self.skill_parser = Skill(util=self.util)
        self.skills = []

        if path is not None:
            self.skills.append(self.skill_parser.get_active_skill(path=path))

            return self.skills

        self.cache_key = 'enemy_skills_parsed_asset'
        cached_asset = self.util.get_redis_asset(cache_key=self.cache_key)

        if cached_asset is not None:
            return cached_asset

        asset_list: list = []
        asset_list.extend(self.util.get_asset_list('EnemySkill'))

        for path in asset_list:
            skill = self.skill_parser.get_active_skill(path=path)

            if skill.get('skill_name') is not None and skill.get('skill_name') != '':
                self.skills.append(skill)

        self.util.save_redis_asset(cache_key=self.cache_key, data=sorted(self.skills, key=lambda d: d['skill_name']))

        return sorted(self.skills, key=lambda d: d['skill_name'])
