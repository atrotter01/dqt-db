from flask_restx import Namespace, Resource, fields
from app.util import Util
from app.data.skill import Skill

api = Namespace("active_skill", description="")

skill_model = api.model('unit', {
    'id': fields.String,
    'level_learned': fields.Integer,
    'skill_name': fields.String,
    'skill_description': fields.String,
    'skill_button_icon': fields.String,
    'skill_rank': fields.String,
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

@api.param("path", "Path")
@api.route("/")
@api.route("/<path>")
class Asset(Resource):

    util: Util
    skill_parser: Skill
    skills: list

    @api.marshal_list_with(skill_model)
    def get(self, path = None):
        '''Fetch a given Skill'''
        self.util = Util()
        self.skill_parser = Skill(util=self.util)
        self.skills = []

        if path is not None:
            self.skills.append(self.skill_parser.get_active_skill(path=path))

            return self.skills

        asset_list: list = self.util.get_asset_list('ActiveSkill')

        for path in asset_list:
            skill = self.skill_parser.get_active_skill(path=path)
            self.skills.append(skill)

        return sorted(self.skills, key=lambda d: d['skill_name'])
