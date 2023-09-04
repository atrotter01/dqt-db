import math
from app.util import Util
from app.data.resistance import Resistance

class Skill:

    util: Util
    resistance_parser: Resistance

    def __init__(self, util):
        self.util = util
        self.resistance_parser = Resistance(util=util)

        return

    def parse_active_skill(self, skill: dict, level_learned: str = None, path = None):
        skill_id = path
        skill_name = None
        skill_description = None

        if skill.get('displayName_translation'):
            skill_name = skill.get('displayName_translation').get('gbl') or skill.get('displayName_translation').get('ja')
        else:
            skill_name = skill.get('displayName')

        if skill.get('description_translation') is not None:
            skill_description = skill.get('description_translation').get('gbl') or skill.get('description_translation').get('ja')
        else:
            skill_description = skill.get('description')

        skill_button_icon = self.util.get_image_path(skill.get('buttonBasePath'))
        skill_rank = skill.get('originRarity').get('displayName_translation').get('gbl') or skill.get('originRarity').get('displayName_translation').get('ja')
        skill_rank_icon = self.util.get_image_path(f'Assets/Aiming/Textures/GUI/General/Icon/MonsterIcon/MonsterIconParts/MonsterRankIcon_{skill_rank}.png')
        skill_range_icon = self.util.get_image_path(skill.get('rangeShape').get('iconPath'))
        skill_reach = skill.get('reachShape').get('description_translation').get('gbl') or skill.get('reachShape').get('description_translation').get('ja')
        skill_element = 'Typeless'

        if skill.get('element').get('displayName_translation'):
            skill_element = skill.get('element').get('displayName_translation').get('gbl') or skill.get('element').get('displayName_translation').get('ja')

        skill_element_icon = self.util.get_image_path(skill.get('element').get('iconPath'))
        if skill_element_icon is None:
            skill_element_icon = self.util.get_image_path('Assets/Aiming/Textures/GUI/General/Battle/CommandPanel/SkillSelectionPanel/ElementIcon/SpellIcon_Mu.png')

        skill_ignore_reflect = skill.get('ignoreSkillReflection')
        skill_ignore_death_endurance = skill.get('ignoreDeathEndurance')
        skill_surehit = skill.get('absolutelyHit')
        skill_ignore_spell_invalid = skill.get('ignoreSpellInvalid')
        skill_threshold_of_intelligence = skill.get('thresholdOfIntelligence')
        skill_threshold_of_attack = skill.get('thresholdOfAttack')
        skill_mp_cost = skill.get('requiredMp')
        skill_is_swap_skill = skill.get('isSwapSkill')
        skill_is_special = skill.get('isSpecial')
        skill_turns_needed = self.util.float_to_str(skill.get('specialCoolTurnCount'))
        skill_times_available = self.util.float_to_str(skill.get('specialAvailableTimes'))
        skill_mp_ratio = self.util.float_to_str(skill.get('remainingMpRatio'))
        skill_num_attacks = self.util.float_to_str(skill.get('numberOfAttacks'))
        skill_is_random_target = self.util.float_to_str(skill.get('isRandomTarget'))
        skill_multiplier = self.util.float_to_str(skill.get('attackMagnificationPermil') / 10)
        skill_base_damage = self.util.float_to_str(skill.get('baseDamage'))
        skill_min_damage = self.util.float_to_str(skill.get('minDamage'))
        skill_max_damage = self.util.float_to_str(skill.get('maxDamage'))
        skill_action_type = self.util.float_to_str(skill.get('activeSkillActionType'))
        skill_type = self.util.float_to_str(skill.get('activeSkillType'))
        skill_target_type = self.util.float_to_str(skill.get('activeSkillTargetType'))
        skill_damage_calculation_type = self.util.float_to_str(skill.get('damageCalculationType'))
        skill_ignores_damage_reduction = skill.get('ignoreDamageScaleEffect')
        skill_wave_immune: bool = False
        skill_enhancements: list = []

        for enhancement in skill.get('enhancements'):
            enhancement_level = enhancement.get('enhancementLevel')
            enhancement_max_accumulation = enhancement.get('maxAccumulation')
            enhancement_required_mp_reduction = enhancement.get('requiredMpReduction')
            enhancement_damage_increase_multiplier = enhancement.get('damageIncrease').get('multiplier')
            enhancement_damage_increase_static_addition = enhancement.get('damageIncrease').get('addition')
            enhancement_healing_increase_multiplier = enhancement.get('healingIncrease').get('multiplier')
            enhancement_healing_increase_static_addition = enhancement.get('healingIncrease').get('addition')
            enhancement_mp_damage_increase_multiplier = enhancement.get('mpDamageIncrease').get('multiplier')
            enhancement_mp_damage_increase_static_addition = enhancement.get('mpDamageIncrease').get('addition')
            enhancement_mp_healing_increase_multiplier = enhancement.get('mpHealingIncrease').get('multiplier')
            enhancement_mp_healing_increase_static_addition = enhancement.get('mpHealingIncrease').get('addition')
            enhancement_accuracy_increase = enhancement.get('accuracyIncrease')
            enhancement_abnormity_accuracy_increase = enhancement.get('abnormityAccuracyIncrease')
            enhancement_status_change_accuracy_increase = enhancement.get('statusChangeAccuracyIncrease')
            enhancement_abnormity_duration_increase = enhancement.get('abnormityDurationIncrease')
            enhancement_status_change_duration_increase = enhancement.get('statusChangeDurationIncrease')

            skill_enhancements.append({
                'enhancement_level': enhancement_level,
                'enhancement_max_accumulation': enhancement_max_accumulation,
                'enhancement_required_mp_reduction': enhancement_required_mp_reduction,
                'enhancement_damage_increase_multiplier': enhancement_damage_increase_multiplier,
                'enhancement_damage_increase_static_addition': enhancement_damage_increase_static_addition,
                'enhancement_healing_increase_multiplier': enhancement_healing_increase_multiplier,
                'enhancement_healing_increase_static_addition': enhancement_healing_increase_static_addition,
                'enhancement_mp_damage_increase_multiplier': enhancement_mp_damage_increase_multiplier,
                'enhancement_mp_damage_increase_static_addition': enhancement_mp_damage_increase_static_addition,
                'enhancement_mp_healing_increase_multiplier': enhancement_mp_healing_increase_multiplier,
                'enhancement_mp_healing_increase_static_addition': enhancement_mp_healing_increase_static_addition,
                'enhancement_accuracy_increase': enhancement_accuracy_increase,
                'enhancement_abnormity_accuracy_increase': enhancement_abnormity_accuracy_increase,
                'enhancement_status_change_accuracy_increase': enhancement_status_change_accuracy_increase,
                'enhancement_abnormity_duration_increase': enhancement_abnormity_duration_increase,
                'enhancement_status_change_duration_increase': enhancement_status_change_duration_increase
            })

        skill_description = self.util.replace_string_variable(skill_description, 'damagePhysics', skill_multiplier)
        skill_description = self.util.replace_string_variable(skill_description, 'specialCoolTurn', skill_turns_needed)
        skill_description = self.util.replace_string_variable(skill_description, 'consumeMPRatio', skill_mp_ratio)
        skill_status_effect_parameter_name: str = None
        change_parameter_counter = 0

        for change_parameter in skill.get('changeParameters'):
            change_parameter_counter = change_parameter_counter + 1
            duration = self.util.float_to_str(change_parameter.get('duration'))
            skill_wave_immune = change_parameter.get('effect').get('disruptiveWaveImmune')
            skill_status_effect_parameter_name = change_parameter.get('effect').get('effectStatusName_translation').get('gbl') or change_parameter.get('effect').get('effectStatusName_translation').get('ja')

            skill_description = self.util.replace_string_variable(skill_description, f'Turn{change_parameter_counter}', duration)

        skill_description = self.util.clean_text_string(str_to_clean=skill_description, unit='%')

        skill: dict = {
            'id': skill_id,
            'level_learned': level_learned,
            'skill_name': skill_name,
            'skill_description': skill_description,
            'skill_button_icon': skill_button_icon,
            'skill_rank': skill_rank,
            'skill_rank_icon': skill_rank_icon,
            'skill_range_icon': skill_range_icon,
            'skill_reach': skill_reach,
            'skill_element': skill_element,
            'skill_element_icon': skill_element_icon,
            'skill_ignore_reflect': skill_ignore_reflect,
            'skill_ignore_death_endurance': skill_ignore_death_endurance,
            'skill_surehit': skill_surehit,
            'skill_ignore_spell_invalid': skill_ignore_spell_invalid,
            'skill_threshold_of_intelligence': skill_threshold_of_intelligence,
            'skill_threshold_of_attack': skill_threshold_of_attack,
            'skill_mp_cost': skill_mp_cost,
            'skill_is_swap_skill': skill_is_swap_skill,
            'skill_multiplier': skill_multiplier,
            'skill_is_special': skill_is_special,
            'skill_times_available': skill_times_available,
            'skill_turns_needed': skill_turns_needed,
            'skill_num_attacks': skill_num_attacks,
            'skill_is_random_target': skill_is_random_target,
            'skill_base_damage': skill_base_damage,
            'skill_min_damage': skill_min_damage,
            'skill_max_damage': skill_max_damage,
            'skill_action_type': skill_action_type,
            'skill_type': skill_type, 
            'skill_target_type': skill_target_type, 
            'skill_damage_calculation_type': skill_damage_calculation_type,
            'skill_ignores_damage_reduction': skill_ignores_damage_reduction,
            'skill_status_effect_parameter_name': skill_status_effect_parameter_name,
            'skill_wave_immune': skill_wave_immune,
            'skill_enhancements': skill_enhancements,
            'type_of_skill': 'active_skill'
        }

        return skill

    def parse_passive_skill(self, skill: dict, level_learned: str = None, path = None):
        skill_id = path
        skill_name = None
        skill_description = None

        if skill.get('passiveSkillName_translation'):
            skill_name = skill.get('passiveSkillName_translation').get('gbl') or skill.get('passiveSkillName_translation').get('ja')
        else:
            skill_name = skill.get('passiveSkillName')

        if skill.get('description_translation') is not None:
            skill_description = skill.get('description_translation').get('gbl') or skill.get('description_translation').get('ja')
        else:
            skill_description = skill.get('description')

        skill_is_invisible = skill.get('isInvisible')
        skill_is_pve_only = skill.get('isOnlyPve')
        skill_icon = self.util.get_image_path(skill.get('iconPath'))
        ally_skill_icon = self.util.get_image_path(skill.get('allySideEffectIconPath'))
        enemy_skill_icon = self.util.get_image_path(skill.get('enemySideEffectIconPath'))

        skill_name = self.util.clean_text_string(str_to_clean=skill_name, unit='%')
        skill_description = self.util.clean_text_string(str_to_clean=skill_description, unit='%')

        skill_text: dict = self.parse_skill_variables(skill=skill, skill_name=skill_name, skill_description=skill_description)
        skill_name = skill_text.get('skill_name')
        skill_description = skill_text.get('skill_description')

        passive_skill: dict = {
            'id': skill_id,
            'level_learned': level_learned,
            'skill_name': skill_name,
            'skill_description': skill_description,
            'skill_is_invisible': skill_is_invisible,
            'skill_is_pve_only': skill_is_pve_only,
            'skill_icon': skill_icon,
            'ally_skill_icon': ally_skill_icon,
            'enemy_skill_icon': enemy_skill_icon,
            'type_of_skill': 'passive_skill'
        }

        return passive_skill

    def parse_reaction_passive_skill(self, skill: dict, level_learned: str = None, path = None):
        abnormity_status_table = self.resistance_parser.build_abnormity_status_table()

        skill_id = path
        skill_name = None
        skill_description = None

        if skill.get('displayName_translation'):
            skill_name = skill.get('displayName_translation').get('gbl') or skill.get('displayName_translation').get('ja')
        else:
            skill_name = skill.get('displayName')

        if skill.get('description_translation') is not None:
            skill_description = skill.get('description_translation').get('gbl') or skill.get('description_translation').get('ja')
        else:
            skill_description = skill.get('description')

        skill_is_invisible: bool = skill.get('isInvisible')
        skill_is_pve_only: bool = skill.get('isOnlyPve')
        skill_times_available = skill.get('availableCount')
        skill_accuracy = skill.get('accuracy')
        skill_attacker_is_enemy: bool = skill.get('attackerIsEnemy')
        skill_attacker_is_self: bool = skill.get('attackerIsSelf')
        skill_attacker_is_ally: bool = skill.get('attackerIsAlly')
        skill_receiver_is_enemy: bool = skill.get('receiverIsEnemy')
        skill_receiver_is_self: bool = skill.get('receiverIsSelf')
        skill_receiver_is_ally: bool = skill.get('receiverIsAlly')
        skill_is_activated_by_damage: bool = skill.get('isDamagedAction')
        skill_is_activated_by_recovery: bool = skill.get('isRecoveredActon')
        skill_is_activated_by_abnormity: bool = skill.get('isAbnormityAction')
        skill_is_activated_by_death: bool = skill.get('isDeadAction')
        skill_reaction_target: bool = skill.get('reactionTarget')
        skill_multiple_activation_to_same_target: bool = skill.get('isMultipleInvokableToSameReactionTarget')
        skill_is_re_reactionable: bool = skill.get('isReReactionable')
        skill_applicable_abnormity_types: list = []
        skill_related_active_skill: dict = None
        skill_related_active_skill_id: str = None
        skill_related_active_skill_name: str = None

        if skill.get('activeSkill').get('linked_asset_id') is not None:
            skill_related_active_skill = self.get_active_skill(path=skill.get('activeSkill').get('linked_asset_id'))
            skill_related_active_skill_name = skill_related_active_skill.get('skill_name')
            skill_related_active_skill_id = skill_related_active_skill.get('id')

        for abnormity in skill.get('refineAbnormityTypes'):
            skill_applicable_abnormity_types.append(abnormity_status_table.get(abnormity))

        skill_name = self.util.clean_text_string(str_to_clean=skill_name, unit='%')
        skill_description = self.util.clean_text_string(str_to_clean=skill_description, unit='%')

        skill_text: dict = self.parse_skill_variables(skill=skill, skill_name=skill_name, skill_description=skill_description)
        skill_name = skill_text.get('skill_name')
        skill_description = skill_text.get('skill_description')

        reaction_passive_skill: dict = {
            'id': skill_id,
            'level_learned': level_learned,
            'skill_name': skill_name,
            'skill_description': skill_description,
            'skill_is_invisible': skill_is_invisible,
            'skill_is_pve_only': skill_is_pve_only,
            'skill_times_available': skill_times_available,
            'skill_accuracy': skill_accuracy,
            'skill_attacker_is_enemy': skill_attacker_is_enemy,
            'skill_attacker_is_self': skill_attacker_is_self,
            'skill_attacker_is_ally': skill_attacker_is_ally,
            'skill_receiver_is_enemy': skill_receiver_is_enemy,
            'skill_receiver_is_self': skill_receiver_is_self,
            'skill_receiver_is_ally': skill_receiver_is_ally,
            'skill_is_activated_by_damage': skill_is_activated_by_damage,
            'skill_is_activated_by_recovery': skill_is_activated_by_recovery,
            'skill_is_activated_by_abnormity': skill_is_activated_by_abnormity,
            'skill_is_activated_by_death': skill_is_activated_by_death,
            'skill_reaction_target': skill_reaction_target,
            'skill_multiple_activation_to_same_target': skill_multiple_activation_to_same_target,
            'skill_is_re_reactionable': skill_is_re_reactionable,
            'skill_applicable_abnormity_types': sorted(skill_applicable_abnormity_types),
            'skill_related_active_skill_name': skill_related_active_skill_name,
            'skill_related_active_skill_id': skill_related_active_skill_id,
            'type_of_skill': 'reaction_skill'
        }

        return reaction_passive_skill

    def parse_awakening_passive_skill(self, skill: dict, awakening_level: str, path: str = None):
        if awakening_level > 0:
            awakening_level = self.util.float_to_str(awakening_level / 10)

        awakening_passive_skill = self.parse_passive_skill(skill=skill, level_learned='0', path=path)
        awakening_passive_skill.update({'awakening_level': awakening_level})

        return awakening_passive_skill

    def parse_awakening_reaction_passive_skill(self, skill: dict, awakening_level: str, path: str = None):
        if awakening_level > 0:
            awakening_level = self.util.float_to_str(awakening_level / 10)

        awakening_reaction_passive_skill = self.parse_reaction_passive_skill(skill=skill, level_learned='0', path=path)
        awakening_reaction_passive_skill.update({'awakening_level': awakening_level})

        return awakening_reaction_passive_skill

    def parse_skill_variables(self, skill: dict, skill_name: str, skill_description: str):
        if skill.get('passiveSkillActiveSkillEnhancementMasterData') is not None:
            passive_skill_enhancement_keys: list = ['damageMultiplier', 'requiredMPReduction','healMultiplier']
            passive_skill_enhancement_path = skill.get('passiveSkillActiveSkillEnhancementMasterData').get('m_PathID')
            passive_skill_enhancement_asset = None

            if passive_skill_enhancement_path != 0:
                passive_skill_enhancement_asset = self.util.get_asset_by_path(passive_skill_enhancement_path)
                passive_skill_enhancement_document = passive_skill_enhancement_asset.get('processed_document')

                for key in passive_skill_enhancement_keys:
                    value: str = None

                    if key == 'damageMultiplier':
                        value = self.util.float_to_str(passive_skill_enhancement_document.get('damageIncrease').get('multiplier') / 100)
                    elif key == 'requiredMPReduction':
                        value = self.util.float_to_str(passive_skill_enhancement_document.get('requiredMpReduction') / 100)
                    elif key == 'healMultiplier':
                        value = self.util.float_to_str(passive_skill_enhancement_document.get('healingIncrease').get('multiplier') / 100)

                    skill_name = self.util.replace_string_variable(str_to_clean=skill_name, key=key, value=value)
                    skill_description = self.util.replace_string_variable(str_to_clean=skill_description, key=key, value=value)

        if skill.get('passiveSkillStatusAddEffectMasterData') is not None:
            passive_skill_status_effect_path = skill.get('passiveSkillStatusAddEffectMasterData').get('m_PathID')
            passive_skill_status_effect_asset = None

            if passive_skill_status_effect_path != 0:
                passive_skill_status_effect_asset = self.util.get_asset_by_path(passive_skill_status_effect_path)
                passive_skill_status_effect_document = passive_skill_status_effect_asset.get('processed_document')

                status_increase_data = self.resistance_parser.parse_status_increase_data(status_increase_data=passive_skill_status_effect_document, display_name=skill_name, description=skill_description)
                skill_name = status_increase_data.get('display_name')
                skill_description = status_increase_data.get('description')

        if skill.get('passiveSkillIncreaseAbnormityAccuracyMasterData') is not None:
            abnormity_accuracy_keys: list = ['abnormityAccuracy']
            abnormity_accuracy_path = skill.get('passiveSkillIncreaseAbnormityAccuracyMasterData').get('m_PathID')
            abnormity_accuracy_asset = None

            if abnormity_accuracy_path != 0:
                abnormity_accuracy_asset = self.util.get_asset_by_path(abnormity_accuracy_path)
                abnormity_accuracy_document = abnormity_accuracy_asset.get('processed_document')

                for key in abnormity_accuracy_keys:
                    value: str = None

                    if key == 'abnormityAccuracy':
                        value = self.util.float_to_str(abnormity_accuracy_document.get('accuracyIncrease'))

                    skill_name = self.util.replace_string_variable(str_to_clean=skill_name, key=key, value=value)
                    skill_description = self.util.replace_string_variable(str_to_clean=skill_description, key=key, value=value)

        if skill.get('passiveSkillCriticalCorrectionMasterData') is not None:
            critical_correction_keys: list = ['criticalCorrection']
            critical_correction_path = skill.get('passiveSkillCriticalCorrectionMasterData').get('m_PathID')
            critical_correction_asset = None

            if critical_correction_path != 0:
                critical_correction_asset = self.util.get_asset_by_path(critical_correction_path)
                critical_correction_document = critical_correction_asset.get('processed_document')

                for key in critical_correction_keys:
                    value: str = None

                    if key == 'criticalCorrection':
                        value = self.util.float_to_str(critical_correction_document.get('value') / 100)

                    skill_name = self.util.replace_string_variable(str_to_clean=skill_name, key=key, value=value)
                    skill_description = self.util.replace_string_variable(str_to_clean=skill_description, key=key, value=value)

        if skill.get('passiveSkillStatusElementResistanceMasterData') is not None:
            element_resistances: dict = {}
            element_resistance_keys: dict = self.resistance_parser.get_element_resistance_keys()
            element_resistance_path = skill.get('passiveSkillStatusElementResistanceMasterData').get('m_PathID')
            element_resistance_asset = None

            if element_resistance_path != 0:
                element_resistance_asset = self.util.get_asset_by_path(element_resistance_path)
                element_resistance_document = element_resistance_asset.get('processed_document')

                for element_resistance in element_resistance_document.get('elementResistances'):
                    element_type = element_resistance.get('type')
                    resistance_rate = str(math.trunc(element_resistance.get('rate') / 100))

                    element_resistances.update({
                        element_type: resistance_rate
                    })

                for key in element_resistance_keys.keys():
                    key_id: int = element_resistance_keys.get(key)

                    if element_resistances.get(key_id) is None:
                        continue

                    skill_name = self.util.replace_string_variable(str_to_clean=skill_name, key=key, value=element_resistances.get(key_id))
                    skill_description = self.util.replace_string_variable(str_to_clean=skill_description, key=key, value=element_resistances.get(key_id))

        if skill.get('passiveSkillStatusAbnormityResistanceMasterData') is not None:
            abnormity_resistances: dict = {}
            abnormity_resistance_keys: dict = self.resistance_parser.get_abnormity_resistance_keys()
            abnormity_resistance_path = skill.get('passiveSkillStatusAbnormityResistanceMasterData').get('m_PathID')
            abnormity_resistance_asset = None

            if abnormity_resistance_path != 0:
                abnormity_resistance_asset = self.util.get_asset_by_path(abnormity_resistance_path)
                abnormity_resistance_document = abnormity_resistance_asset.get('processed_document')

                for abnormity_resistance in abnormity_resistance_document.get('abnormityResistances'):
                    abnormity_type = abnormity_resistance.get('type')
                    resistance_rate = str(math.trunc(abnormity_resistance.get('rate') / 100))

                    abnormity_resistances.update({
                        abnormity_type: resistance_rate
                    })

                for key in abnormity_resistance_keys.keys():
                    key_id: int = abnormity_resistance_keys.get(key)

                    skill_name = self.util.replace_string_variable(str_to_clean=skill_name, key=key, value=abnormity_resistances.get(key_id))
                    skill_description = self.util.replace_string_variable(str_to_clean=skill_description, key=key, value=abnormity_resistances.get(key_id))

        if 'damageEnhancement' in skill_name or 'damageEnhancement' in skill_description:
            skill_damage_increase = self.util.float_to_str(skill.get('passiveSkillExcellentDamageEnhancementEffect').get('damageIncrease') / 100)
            skill_name = self.util.replace_string_variable(str_to_clean=skill_name, key='damageEnhancement', value=skill_damage_increase)
            skill_description = self.util.replace_string_variable(str_to_clean=skill_description, key='damageEnhancement', value=skill_damage_increase)

        if 'damageTakenDecrease' in skill_name or 'damageTakenDecrease' in skill_description:
            skill_damage_decrease_asset = self.util.get_asset_by_path(path=skill.get('passiveSkillDecreaseDamageTakenMasterData').get('m_PathID'), deflate_data=True)
            skill_damage_decrease_document = skill_damage_decrease_asset.get('processed_document')
            skill_damage_decrease = self.util.float_to_str(100 - (skill_damage_decrease_document.get('rate') / 100))
            skill_name = self.util.replace_string_variable(str_to_clean=skill_name, key='damageTakenDecrease', value=skill_damage_decrease)
            skill_description = self.util.replace_string_variable(str_to_clean=skill_description, key='damageTakenDecrease', value=skill_damage_decrease)

        if skill.get('passiveSkillStatusMulEffectMasterData') is not None:
            skill_increase_path = skill.get('passiveSkillStatusMulEffectMasterData').get('m_PathID')

            if skill_increase_path != 0:
                status_multiplier_asset = self.util.get_asset_by_path(path=skill.get('passiveSkillStatusMulEffectMasterData').get('m_PathID'), deflate_data=True)
                status_multiplier_document = status_multiplier_asset.get('processed_document')
                skill_increase_data: dict = self.resistance_parser.parse_status_increase_data(status_increase_data=status_multiplier_document, display_name=skill_name, description=skill_description)
                skill_name = skill_increase_data.get('display_name')
                skill_description = skill_increase_data.get('description')

        if skill.get('activeSkillTypeResistance') is not None:
            if skill.get('activeSkillTypeResistance').get('activeSkillTypeResistances') is not None:
                active_skill_resistance_table: list = skill.get('activeSkillTypeResistance').get('activeSkillTypeResistances')
                active_skill_resistance_strings: dict = self.parse_active_skill_resistance(active_skill_resistance_table=active_skill_resistance_table, display_name=skill_name, description=skill_description)
                skill_name = active_skill_resistance_strings.get('display_name')
                skill_description = active_skill_resistance_strings.get('description')

        return {
            'skill_name': skill_name,
            'skill_description': skill_description
        }

    def parse_active_skill_resistance(self, active_skill_resistance_table: dict, display_name: str, description: str):
        active_skill_resistance_keys: dict = {
            'activeSkillTypeResistanceBreathNone': 0,
            'activeSkillTypeResistancePhysicsNone': 0,
            'activeSkillTypeResistanceSpellNone': 0,
            'activeSkillTypeResistanceTechniqueNone': 0,
            'activeSkillTypeResistanceBreathMera': 1,
            'activeSkillTypeResistancePhysicsMera': 1,
            'activeSkillTypeResistanceSpellMera': 1,
            'activeSkillTypeResistanceTechniqueMera': 1,
            'activeSkillTypeResistanceBreathGira': 2,
            'activeSkillTypeResistancePhysicsGira': 2,
            'activeSkillTypeResistanceSpellGira': 2,
            'activeSkillTypeResistanceTechniqueGira': 2,
            'activeSkillTypeResistanceBreathHyado': 3,
            'activeSkillTypeResistancePhysicsHyado': 3,
            'activeSkillTypeResistanceSpellHyado': 3,
            'activeSkillTypeResistanceTechniqueHyado': 3,
            'activeSkillTypeResistanceBreathBagi': 4,
            'activeSkillTypeResistancePhysicsBagi': 4,
            'activeSkillTypeResistanceSpellBagi': 4,
            'activeSkillTypeResistanceTechniqueBagi': 4,
            'activeSkillTypeResistanceBreathIo': 5,
            'activeSkillTypeResistancePhysicsIo': 5,
            'activeSkillTypeResistanceSpellIo': 5,
            'activeSkillTypeResistanceTechniqueIo': 5,
            'activeSkillTypeResistancePhysicsDein': 6,
            'activeSkillTypeResistanceBreathDein': 6,
            'activeSkillTypeResistanceSpellDein': 6,
            'activeSkillTypeResistanceTechniqueDein': 6,
            'activeSkillTypeResistanceBreathDoruma': 7,
            'activeSkillTypeResistancePhysicsDoruma': 7,
            'activeSkillTypeResistanceSpellDoruma': 7,
            'activeSkillTypeResistanceTechniqueDoruma': 7
        }

        for key in active_skill_resistance_keys.keys():
            if key in display_name:
                active_skill_resistance_type = active_skill_resistance_keys.get(key)

                for active_skill_resistance in active_skill_resistance_table:
                    if active_skill_resistance.get('element') == active_skill_resistance_type:
                        active_skill_resistance_increase_value = self.util.float_to_str(int(active_skill_resistance.get('rate')) / 100)
                        display_name = self.util.clean_text_string(str_to_clean=self.util.replace_string_variable(str_to_clean=display_name, key=key, value=active_skill_resistance_increase_value), unit='%')
                        description = self.util.clean_text_string(str_to_clean=self.util.replace_string_variable(str_to_clean=description, key=key, value=active_skill_resistance_increase_value), unit='%')

        return {
            'display_name': display_name,
            'description': description
        }

    def get_active_skill(self, path):
        cache_key: str = f'{path}_parsed_asset'
        cached_asset: dict = self.util.get_redis_asset(cache_key=cache_key)

        if cached_asset is not None:
            return cached_asset

        asset: dict = self.util.get_asset_by_path(path=path, deflate_data=True)
        skill: dict = self.parse_active_skill(skill=asset.get('processed_document'), level_learned=None, path=path)
        self.util.save_redis_asset(cache_key=cache_key, data=skill)

        return skill

    def get_passive_skill(self, path):
        cache_key: str = f'{path}_parsed_asset'
        cached_asset: dict = self.util.get_redis_asset(cache_key=cache_key)

        if cached_asset is not None:
            return cached_asset

        asset: dict = self.util.get_asset_by_path(path=path, deflate_data=True)
        skill: dict = self.parse_passive_skill(skill=asset.get('processed_document'), level_learned=None, path=path)
        self.util.save_redis_asset(cache_key=cache_key, data=skill)

        return skill

    def get_reaction_skill(self, path):
        cache_key: str = f'{path}_parsed_asset'
        cached_asset: dict = self.util.get_redis_asset(cache_key=cache_key)

        if cached_asset is not None:
            return cached_asset

        asset: dict = self.util.get_asset_by_path(path=path, deflate_data=True)
        skill: dict = self.parse_reaction_passive_skill(skill=asset.get('processed_document'), level_learned=None, path=path)
        self.util.save_redis_asset(cache_key=cache_key, data=skill)

        return skill
