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
    'skill_ignore_reflect': fields.Boolean,
    'skill_ignore_death_endurance': fields.Boolean,
    'skill_surehit': fields.Boolean,
    'skill_ignore_spell_invalid': fields.Boolean,
    'skill_threshold_of_intelligence': fields.Integer,
    'skill_threshold_of_attack': fields.Integer,
    'skill_mp_cost': fields.Integer,
    'skill_is_swap_skill': fields.Boolean,
    'skill_potency': fields.Float,
    'skill_is_special': fields.Boolean,
    'skill_times_available': fields.Integer,
    'skill_turns_needed': fields.Integer,
    'skill_num_attacks': fields.Integer,
    'skill_is_random_target': fields.Boolean,
    'skill_min_damage': fields.Integer,
    'skill_max_damage': fields.Integer,
    'skill_action_type': fields.Integer,
    'skill_type': fields.String, 
    'skill_target_type': fields.Integer,
    'skill_damage_calculation_type': fields.Integer,
    'skill_enhancements': fields.List(fields.Raw)
})

passive_skill_model = api.model('passive_skill', {
    'id': fields.String,
    'level_learned': fields.Integer,
    'skill_name': fields.String,
    'skill_description': fields.String,
    'skill_is_invisible': fields.Boolean,
    'skill_is_pve_only': fields.Boolean,
    'ally_skill_icon': fields.String,
    'enemy_skill_icon': fields.String
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
    'skill_applicable_abnormity_types': fields.List(fields.Raw)
})

@api.param("path", "Path")
@api.route("/active_skill")
@api.route("/active_skill/<path>")
class ActiveSkill(Resource):

    util: Util
    skill_parser: Skill
    skills: list

    @api.marshal_list_with(active_skill_model)
    def get(self, path = None):
        '''Fetch a given Skill'''
        self.util = Util()
        self.skill_parser = Skill(util=self.util)
        self.skills = []

        if path is not None:
            self.skills.append(self.skill_parser.get_active_skill(path=path))

            return self.skills

        asset_list: list = []
        asset_list.extend(self.util.get_asset_list('ActiveSkill'))
        asset_list.extend(self.util.get_asset_list('GuestSkill'))
        asset_list.extend(self.util.get_asset_list('NotUseSkill'))

        for path in asset_list:
            skill = self.skill_parser.get_active_skill(path=path)

            if skill.get('skill_name') is not None and skill.get('skill_name') != '':
                self.skills.append(skill)

        return sorted(self.skills, key=lambda d: d['skill_name'])

@api.param("path", "Path")
@api.route("/passive_skill")
@api.route("/passive_skill/<path>")
class PassiveSkill(Resource):

    util: Util
    skill_parser: Skill
    skills: list

    @api.marshal_list_with(passive_skill_model)
    def get(self, path = None):
        '''Fetch a given Skill'''
        self.util = Util()
        self.skill_parser = Skill(util=self.util)
        self.skills = []

        if path is not None:
            self.skills.append(self.skill_parser.get_passive_skill(path=path))

            return self.skills

        asset_list: list = []
        asset_list.extend(self.util.get_asset_list('LeaderPassive'))
        asset_list.extend(self.util.get_asset_list('ReactionPassive'))
        asset_list.extend(self.util.get_asset_list('NotUsePassiveSkill'))
        asset_list.extend(self.util.get_asset_list('PassiveSkill'))

        for path in asset_list:
            skill = self.skill_parser.get_passive_skill(path=path)

            if skill.get('skill_name') is not None and skill.get('skill_name') != '':
                self.skills.append(skill)

        return sorted(self.skills, key=lambda d: d['skill_name'])

@api.param("path", "Path")
@api.route("/reaction_skill")
@api.route("/reaction_skill/<path>")
class ReactionSkill(Resource):

    util: Util
    skill_parser: Skill
    skills: list

    @api.marshal_list_with(reaction_skill_model)
    def get(self, path = None):
        '''Fetch a given Skill'''
        self.util = Util()
        self.skill_parser = Skill(util=self.util)
        self.skills = []

        if path is not None:
            self.skills.append(self.skill_parser.get_reaction_skill(path=path))

            return self.skills

        asset_list: list = []
        asset_list.extend(self.util.get_asset_list('ReactionPassiveSkill'))

        for path in asset_list:
            skill = self.skill_parser.get_reaction_skill(path=path)

            if skill.get('skill_name') is not None and skill.get('skill_name') != '':
                self.skills.append(skill)

        return sorted(self.skills, key=lambda d: d['skill_name'])

@api.param("path", "Path")
@api.route("/enemy_skill")
@api.route("/enemy_skill/<path>")
class EnemySkill(Resource):

    util: Util
    skill_parser: Skill
    skills: list

    @api.marshal_list_with(active_skill_model)
    def get(self, path = None):
        '''Fetch a given Skill'''
        self.util = Util()
        self.skill_parser = Skill(util=self.util)
        self.skills = []

        if path is not None:
            self.skills.append(self.skill_parser.get_active_skill(path=path))

            return self.skills

        asset_list: list = []
        asset_list.extend(self.util.get_asset_list('EnemySkill'))

        for path in asset_list:
            skill = self.skill_parser.get_active_skill(path=path)

            if skill.get('skill_name') is not None and skill.get('skill_name') != '':
                self.skills.append(skill)

        return sorted(self.skills, key=lambda d: d['skill_name'])
