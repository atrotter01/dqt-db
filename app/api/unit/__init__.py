from flask_restx import Namespace, Resource, fields
from app.util import Util

api = Namespace("unit", description="")

unit_model = api.model('unit', {
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
    'stats_by_level': fields.List(fields.Raw),
    'family': fields.String,
    'family_icon': fields.String,
    'role': fields.String,
    'role_icon': fields.String,
    'unit_icon': fields.String,
    'transformed_unit_icon': fields.String,
    'active_skills': fields.List(fields.Raw),
    'awakening_passive_skills': fields.List(fields.Raw)
})

util = Util()

@api.param("unit_name", "Unit Name")
@api.route("/")
@api.route("/<unit_name>")
class Asset(Resource):
    @api.marshal_list_with(unit_model)
    def get(self, unit_name = None):
        '''Fetch a given Unit'''
        units: list = []

        #if util.redis_client.get('event_portal_cache'):
        #    events = util.get_asset_by_path('event_portal_cache', deflate_data=False)
        #else:
        asset_list: list = util.get_asset_list('AllyMonster')
        units: list = []

        for path in asset_list:
            if unit_name is not None:
                asset = util.get_asset_by_path(path, deflate_data=False)
                display_name: str = asset.get('display_name')

                if display_name != unit_name:
                    continue

            asset = util.get_asset_by_path(path, deflate_data=True)
            data: dict = asset.get('processed_document')
            display_name: str = asset.get('display_name')
            allow_nicknaming = data.get('allowedNicknaming')
            almanac_visible = data.get('monsterCollectionDisplayed')
            almanac_number = data.get('monsterCollectionNumber')
            max_cp = data.get('maxTotalPower')
            is_quest_reward = data.get('questReward')
            is_gacha_unit = data.get('scoutable')
            rank_up_table_list: list = []
            unit_rank = data.get('originRankRarity').get('displayName')
            unit_rank_icon = data.get('originRankRarity').get('iconPath')
            movement = data.get('mobility')
            weight = data.get('weight')
            family = data.get('profile').get('family').get('abbrevDisplayName')
            family_icon = data.get('profile').get('family').get('largeIconPath')
            role = data.get('profile').get('role').get('abbrevDisplayName')
            role_icon = data.get('profile').get('role').get('iconPath')
            unit_icon = data.get('profile').get('iconPath')
            transformed_unit_icon = data.get('profile').get('transformedIconPath')
            stats_by_level: list = data.get('levelParameterTable').get('monsterLevelParamList')
            active_skills: list = []
            awakening_passive_skills: list = []

            for rank_up_table in data.get('rankUpTable').get('monsterRankUpList'):
                rank: dict = rank_up_table.get('rank')
                recipe: dict = rank_up_table.get('recipe')

                rank_number = rank.get('number') + 1
                rank_level_cap: str = rank.get('levelCap')
                rank_gold_cost: str = rank.get('rankUpCost')
                rank_up_items: list = []

                for slot in recipe.get('slots'):
                    item = slot.get('item')
                    item_name: str = item.get('displayName')
                    item_icon: str = item.get('iconPath')
                    quantity: str = slot.get('quantity')

                    rank_up_items.append({
                        'item_name': item_name,
                        'item_icon': util.get_image_path(item_icon),
                        'quantity': quantity
                    })

                rank_up_table_list.append({
                    'rank_number': rank_number,
                    'rank_level_cap': rank_level_cap,
                    'rank_gold_cost': rank_gold_cost,
                    'rank_up_items': rank_up_items
                })

            for skill_learning in data.get('activeSkillLearnings'):
                level_learned = skill_learning.get('level')
                skill = skill_learning.get('activeSkill')
                skill_potency = util.float_to_str(skill.get('attackMagnificationPermil') / 10)
                skill_name = skill.get('displayName')
                skill_description = skill.get('description')
                skill_button_icon = util.get_image_path(skill.get('buttonBasePath'))
                skill_rank = skill.get('originRarity').get('displayName')
                skill_range_icon = util.get_image_path(skill.get('rangeShape').get('iconPath'))
                skill_reach = skill.get('reachShape').get('description')
                skill_element = skill.get('element').get('displayName')
                skill_element_icon = util.get_image_path(skill.get('element').get('iconPath'))
                skill_ignore_reflect = skill.get('ignoreSkillReflection')
                skill_ignore_death_endurance = skill.get('ignoreDeathEndurance')
                skill_surehit = skill.get('absolutelyHit')
                skill_ignore_spell_invalid = skill.get('ignoreSpellInvalid')
                skill_wisdom_cap = skill.get('thresholdOfIntelligence')
                skill_attack_cap = skill.get('thresholdOfAttack')
                skill_mp_cost = skill.get('requiredMp')
                skill_is_swap_skill = skill.get('isSwapSkill')
                skill_is_special = skill.get('isSpecial')
                skill_turns_needed = util.float_to_str(skill.get('specialCoolTurnCount'))
                skill_times_available = util.float_to_str(skill.get('specialAvailableTimes'))
                skill_mp_ratio = util.float_to_str(skill.get('remainingMpRatio'))

                skill_description = util.replace_string_variable(skill_description, 'damagePhysics', skill_potency)
                skill_description = util.replace_string_variable(skill_description, 'specialCoolTurn', skill_turns_needed)
                skill_description = util.replace_string_variable(skill_description, 'consumeMPRatio', skill_mp_ratio)
                change_parameter_counter = 0

                for change_parameter in skill.get('changeParameters'):
                    change_parameter_counter = change_parameter_counter + 1
                    duration = util.float_to_str(change_parameter.get('duration'))

                    skill_description = util.replace_string_variable(skill_description, f'Turn{change_parameter_counter}', duration)

                skill_description = util.clean_text_string(str_to_clean=skill_description, unit='%')

                skill: dict = {
                    'level_learned': level_learned,
                    'skill_name': skill_name,
                    'skill_description': skill_description,
                    'skill_button_icon': skill_button_icon,
                    'skill_rank': skill_rank,
                    'skill_range_icon': skill_range_icon,
                    'skill_reach': skill_reach,
                    'skill_element': skill_element,
                    'skill_element_icon': skill_element_icon,
                    'skill_ignore_reflect': skill_ignore_reflect,
                    'skill_ignore_death_endurance': skill_ignore_death_endurance,
                    'skill_surehit': skill_surehit,
                    'skill_ignore_spell_invalid': skill_ignore_spell_invalid,
                    'skill_wisdom_cap': skill_wisdom_cap,
                    'skill_attack_cap': skill_attack_cap,
                    'skill_mp_cost': skill_mp_cost,
                    'skill_is_swap_skill': skill_is_swap_skill,
                    'skill_potency': skill_potency,
                    'skill_is_special': skill_is_special,
                    'skill_times_available': skill_times_available,
                    'skill_turns_needed': skill_turns_needed
                }

                active_skills.append(skill)

            for skill_learning in data.get('awakeningPassiveSkillLearnings'):
                awakening_level = skill_learning.get('point')
                skill = skill_learning.get('passiveSkill')
                
                if awakening_level > 0:
                    awakening_level = util.float_to_str(awakening_level / 10)

                skill_name = util.clean_text_string(str_to_clean=skill.get('passiveSkillName'), unit='%')
                skill_description = util.clean_text_string(str_to_clean=skill.get('description'), unit='%')
                ally_skill_icon = util.get_image_path(skill.get('allySideEffectIconPath'))
                enemy_skill_icon = util.get_image_path(skill.get('enemySideEffectIconPath'))
                skill_is_invisible = skill.get('isInvisible')
                skill_is_pve_only = skill.get('isOnlyPve')

                passive_skill_enhancement_keys: list = ['damageMultiplier', 'requiredMPReduction','healMultiplier']
                passive_skill_enhancement_path = skill.get('passiveSkillActiveSkillEnhancementMasterData').get('m_PathID')
                passive_skill_enhancement_asset = None

                if passive_skill_enhancement_path != 0:
                    passive_skill_enhancement_asset = util.get_asset_by_path(passive_skill_enhancement_path)
                    passive_skill_enhancement_document = passive_skill_enhancement_asset.get('processed_document')
                    #print(passive_skill_enhancement_document)

                    for key in passive_skill_enhancement_keys:
                        value: str = None

                        if key == 'damageMultiplier':
                            value = util.float_to_str(passive_skill_enhancement_document.get('damageIncrease').get('multiplier') / 100)
                        elif key == 'requiredMPReduction':
                            value = util.float_to_str(passive_skill_enhancement_document.get('requiredMpReduction') / 100)
                        elif key == 'healMultiplier':
                            value = util.float_to_str(passive_skill_enhancement_document.get('healingIncrease').get('multiplier') / 100)

                        skill_name = util.replace_string_variable(str_to_clean=skill_name, key=key, value=value)
                        skill_description = util.replace_string_variable(str_to_clean=skill_description, key=key, value=value)

                passive_skill_status_effect_keys: list = ['statusAddHP','statusAddDef','statusAddAtk','statusAddMP']
                passive_skill_status_effect_path = skill.get('passiveSkillStatusAddEffectMasterData').get('m_PathID')
                passive_skill_status_effect_asset = None

                if passive_skill_status_effect_path != 0:
                    passive_skill_status_effect_asset = util.get_asset_by_path(passive_skill_status_effect_path)
                    passive_skill_status_effect_document = passive_skill_status_effect_asset.get('processed_document')
                    #print(passive_skill_status_effect_document)

                    for key in passive_skill_status_effect_keys:
                        value: str = None

                        if key == 'statusAddHP':
                            value = util.float_to_str(passive_skill_status_effect_document.get('statusIncrease').get('hp'))
                        elif key == 'statusAddMP':
                            value = util.float_to_str(passive_skill_status_effect_document.get('statusIncrease').get('mp'))
                        elif key == 'statusAddDef':
                            value = util.float_to_str(passive_skill_status_effect_document.get('statusIncrease').get('defence'))
                        elif key == 'statusAddAtk':
                            value = util.float_to_str(passive_skill_status_effect_document.get('statusIncrease').get('attack'))

                        skill_name = util.replace_string_variable(str_to_clean=skill_name, key=key, value=value)
                        skill_description = util.replace_string_variable(str_to_clean=skill_description, key=key, value=value)

                abnormity_accuracy_keys: list = ['abnormityAccuracy']
                abnormity_accuracy_path = skill.get('passiveSkillIncreaseAbnormityAccuracyMasterData').get('m_PathID')
                abnormity_accuracy_asset = None

                if abnormity_accuracy_path != 0:
                    abnormity_accuracy_asset = util.get_asset_by_path(abnormity_accuracy_path)
                    abnormity_accuracy_document = abnormity_accuracy_asset.get('processed_document')
                    #print(abnormity_accuracy_document)

                    for key in abnormity_accuracy_keys:
                        value: str = None

                        if key == 'abnormityAccuracy':
                            value = util.float_to_str(abnormity_accuracy_document.get('accuracyIncrease'))

                        skill_name = util.replace_string_variable(str_to_clean=skill_name, key=key, value=value)
                        skill_description = util.replace_string_variable(str_to_clean=skill_description, key=key, value=value)

                critical_correction_keys: list = ['criticalCorrection']
                critical_correction_path = skill.get('passiveSkillCriticalCorrectionMasterData').get('m_PathID')
                critical_correction_asset = None

                if critical_correction_path != 0:
                    critical_correction_asset = util.get_asset_by_path(critical_correction_path)
                    critical_correction_document = critical_correction_asset.get('processed_document')
                    #print(critical_correction_document)

                    for key in critical_correction_keys:
                        value: str = None

                        if key == 'criticalCorrection':
                            value = util.float_to_str(critical_correction_document.get('value') / 100)

                        skill_name = util.replace_string_variable(str_to_clean=skill_name, key=key, value=value)
                        skill_description = util.replace_string_variable(str_to_clean=skill_description, key=key, value=value)

                '''
                element_resistance_keys: list = ['elementResistanceHyado','elementResistanceMera']
                element_resistance_path = skill.get('passiveSkillStatusElementResistanceMasterData').get('m_PathID')
                element_resistance_asset = None

                if element_resistance_path != 0:
                    element_resistance_asset = util.get_asset_by_path(element_resistance_path)
                    element_resistance_document = element_resistance_asset.get('processed_document')
                    print(element_resistance_document)

                    for key in element_resistance_keys:
                        value: str = None

                        if key == 'criticalCorrection':
                            value = util.float_to_str(element_resistance_document.get('value') / 100)

                        skill_name = util.replace_string_variable(str_to_clean=skill_name, key=key, value=value)
                        skill_description = util.replace_string_variable(str_to_clean=skill_description, key=key, value=value)
                '''

                awakening_passive_skill = {
                    'awakening_level': awakening_level,
                    'skill_name': skill_name,
                    'skill_description': skill_description,
                    'ally_skill_icon': ally_skill_icon,
                    'enemy_skill_icon': enemy_skill_icon,
                    'skill_is_invisible': skill_is_invisible,
                    'skill_is_pve_only': skill_is_pve_only
                }

                awakening_passive_skills.append(awakening_passive_skill)

            unit: dict = {
                'display_name': display_name,
                'weight': weight,
                'move': movement,
                'unit_rank': unit_rank,
                'unit_rank_icon': util.get_image_path(unit_rank_icon),
                'allow_nicknaming': allow_nicknaming,
                'almanac_visible': almanac_visible,
                'almanac_number': almanac_number,
                'max_cp': max_cp,
                'is_quest_reward': is_quest_reward,
                'is_gacha_unit': is_gacha_unit,
                'family': family,
                'family_icon': util.get_image_path(family_icon),
                'role': role,
                'role_icon': util.get_image_path(role_icon),
                'unit_icon': util.get_image_path(unit_icon),
                'transformed_unit_icon': util.get_image_path(transformed_unit_icon),
                'active_skills': active_skills,
                'awakening_passive_skills': awakening_passive_skills
            }

            if unit_name is not None:
                unit.update({'rank_up_table': rank_up_table_list})
                unit.update({'stats_by_level': stats_by_level})

            units.append(unit)
            
        return sorted(units, key=lambda d: d['display_name'])

    #util.redis_client.set('event_portal_cache', json.dumps(events))

    #return render_template('index.html', events=sorted(events, key=lambda d: d['display_name']))
