import math
from app.util import Util
from app.data.resistance import Resistance
from app.data.skill import Skill

class Blossom:

    util: Util
    skill_parser: Skill
    resistance_parser: Resistance

    def __init__(self, util):
        self.util = util
        self.skill_parser = Skill(util=util)
        self.resistance_parser = Resistance(util=util)

        return

    def parse_skill_board(self, blossom_board):
        blossoms: list = []

        for blossom_panel in blossom_board.get('panels'):
            panel_code = blossom_panel.get('panelCode')
            panel_contents = blossom_panel.get('panelContents')
            panel_unlock_costs = blossom_panel.get('unlockCosts')
            panel_display_name = None
            panel_description = None
            
            if panel_contents.get('displayName_translation'):
                panel_display_name = panel_contents.get('displayName_translation').get('gbl') or panel_contents.get('displayName_translation').get('ja')
            else:
                panel_display_name = panel_contents.get('displayName')
            
            if panel_contents.get('description_translation'):
                panel_description = panel_contents.get('description_translation').get('gbl') or panel_contents.get('description_translation').get('ja')
            else:
                panel_description = panel_contents.get('description')

            panel_effects = panel_contents.get('effects')
            panel_type = panel_effects[0].get('type')
            panel_unlock_items: list = []

            for consumption_item in panel_unlock_costs.get('consumptionItems'):
                consumption_item_quantity = consumption_item.get('quantity')
                consumption_item_display_name = consumption_item.get('consumableItem').get('displayName_translation').get('gbl') or consumption_item.get('consumableItem').get('displayName_translation').get('ja')
                consumption_item_icon_path = self.util.get_image_path(consumption_item.get('consumableItem').get('iconPath'))
                panel_unlock_items.append({
                    'consumption_item_display_name': consumption_item_display_name,
                    'consumption_item_icon_path': consumption_item_icon_path,
                    'consumption_item_quantity': consumption_item_quantity
                })

            if panel_type == 0:
                skill = panel_effects[0].get('activeSkill')
                active_skill = self.skill_parser.parse_active_skill(skill=skill, level_learned='0')
                blossoms.append({
                    'panel_code': panel_code,
                    'panel_display_name': panel_display_name,
                    'panel_description': panel_description,
                    'type': 'Active Skill',
                    'data': active_skill,
                    'unlock_costs': panel_unlock_items
                })

            elif panel_type == 1:
                skill = panel_effects[len(panel_effects)-1].get('passiveSkill')
                passive_skill = self.skill_parser.parse_passive_skill(skill=skill, level_learned='0')
                blossoms.append({
                    'panel_code': panel_code,
                    'panel_display_name': panel_display_name,
                    'panel_description': panel_description,
                    'type': 'Passive Skill',
                    'data': passive_skill,
                    'unlock_costs': panel_unlock_items
                })

            elif panel_type == 3:
                status_add_effect: dict = panel_effects[len(panel_effects)-1].get('statusAddEffect')
                status_add_dffect_data: dict = self.resistance_parser.parse_status_increase_data(status_increase_data=status_add_effect, display_name=panel_display_name, description=panel_description)
                panel_display_name = status_add_dffect_data.get('display_name')
                panel_description = status_add_dffect_data.get('description')

                blossoms.append({
                    'panel_code': panel_code,
                    'panel_display_name': panel_display_name,
                    'panel_description': panel_description,
                    'type': 'Stats Increase',
                    'unlock_costs': panel_unlock_items
                })

            elif panel_type == 4:
                element_resistance = panel_effects[len(panel_effects)-1].get('statusElementResistance')
                element_resistance_table: dict = self.resistance_parser.parse_elemental_resistance_table(element_resistance_data=element_resistance)
                element_resistance_strings: dict = self.resistance_parser.parse_element_resistance(element_resistance_table=element_resistance_table, display_name=panel_display_name, description=panel_description)
                panel_display_name = element_resistance_strings.get('display_name')
                panel_description = element_resistance_strings.get('description')

                blossoms.append({
                    'panel_code': panel_code,
                    'panel_display_name': panel_display_name,
                    'panel_description': panel_description,
                    'type': 'Elemental Resistance',
                    'unlock_costs': panel_unlock_items
                })

            elif panel_type == 5:
                abnormity_resistance_data = panel_effects[len(panel_effects)-1].get('statusAbnormityResistance')
                abnormity_resistance_table = self.resistance_parser.parse_abnormity_resistance_table(abnormity_resistance_data=abnormity_resistance_data)
                abnormity_resistance_strings: dict = self.resistance_parser.parse_abnormity_resistance(abnormity_resistance_table=abnormity_resistance_table, display_name=panel_display_name, description=panel_description)
                panel_display_name = abnormity_resistance_strings.get('display_name')
                panel_description = abnormity_resistance_strings.get('description')

                blossoms.append({
                    'panel_code': panel_code,
                    'panel_display_name': panel_display_name,
                    'panel_description': panel_description,
                    'type': 'Abnormity Resistance',
                    'unlock_costs': panel_unlock_items
                })

        return blossoms
