import math
from app.util import Util

class Resistance:

    def __init__(self, util):
        self.util = util

        return

    def map_rate_to_image(self, rate: int):
        icon: str = None

        if int(rate) == 100:
            icon = self.util.get_image_path('Assets/Aiming/Textures/GUI/en/Icon/MonsterIcon/MonsterIconParts/ResistanceLevel_Mukou.png')
        elif int(rate) == 75:
            icon = self.util.get_image_path('Assets/Aiming/Textures/GUI/en/Icon/MonsterIcon/MonsterIconParts/ResistanceLevel_Gekigen.png')
        elif int(rate) == 50:
            icon = self.util.get_image_path('Assets/Aiming/Textures/GUI/en/Icon/MonsterIcon/MonsterIconParts/ResistanceLevel_Hangen.png')
        elif int(rate) == 25:
            icon = self.util.get_image_path('Assets/Aiming/Textures/GUI/en/Icon/MonsterIcon/MonsterIconParts/ResistanceLevel_Keigen.png')
        elif int(rate) == 0:
            icon = self.util.get_image_path('Assets/Aiming/Textures/GUI/en/Icon/MonsterIcon/MonsterIconParts/ResistanceLevel_Hutuu.png')
        elif int(rate) == -25:
            icon = self.util.get_image_path('Assets/Aiming/Textures/GUI/en/Icon/MonsterIcon/MonsterIconParts/ResistanceLevel_Zyakuten.png')
        elif int(rate) == -50:
            icon = self.util.get_image_path('Assets/Aiming/Textures/GUI/en/Icon/MonsterIcon/MonsterIconParts/ResistanceLevel_DaiZyakuten.png')
        elif int(rate) == -100:
            icon = self.util.get_image_path('Assets/Aiming/Textures/GUI/en/Icon/MonsterIcon/MonsterIconParts/ResistanceLevel_ChouZyakuten.png')

        return icon

    def parse_elemental_resistance_table(self, element_resistance_data: dict):
        elements: dict = self.build_element_table()
        element_resistance_table: dict = {}

        for element_resistance in element_resistance_data.get('elementResistances'):
            element_type = element_resistance.get('type')
            element_name = elements.get(element_type).get('name')
            element_icon = elements.get(element_type).get('icon')
            element_resistance_rate = str(math.trunc(element_resistance.get('rate') / 100))
            element_resistance_rate_icon = self.map_rate_to_image(element_resistance_rate)

            element_resistance_table.update({
                element_type: {
                    'name': element_name,
                    'icon': element_icon,
                    'rate': element_resistance_rate,
                    'rate_icon': element_resistance_rate_icon
                }
            })

        return element_resistance_table

    def parse_status_increase_data(self, status_increase_data: dict, display_name: str, description: str):
        status_add_table: dict = status_increase_data.get('statusIncrease')
        status_increase_value: str = None
        status_keys: dict = {
            'statusAddMP': 'mp',
            'statusAddAtk': 'attack',
            'statusAddSpd': 'agility',
            'statusAddInt': 'intelligence',
            'statusAddDef': 'defence',
            'statusAddHP': 'hp',
            'statusMulMP': 'mp',
            'statusMulAtk': 'attack',
            'statusMulSpd': 'agility',
            'statusMulInt': 'intelligence',
            'statusMulDef': 'defence',
            'statusMulHP': 'hp'
        }

        for key in status_keys.keys():
            if key in display_name or key in description:
                status_increase_value = str(status_add_table.get(status_keys.get(key)))
                display_name = self.util.clean_text_string(str_to_clean=self.util.replace_string_variable(str_to_clean=display_name, key=key, value=status_increase_value), unit='%')
                description = self.util.clean_text_string(str_to_clean=self.util.replace_string_variable(str_to_clean=description, key=key, value=status_increase_value), unit='%')

        return {
            'display_name': display_name,
            'description': description
        }

    def parse_abnormity_resistance_table(self, abnormity_resistance_data: dict):
        abnormity_status_effects: dict = self.build_abnormity_resistance_table()
        abnormity_resistance_table: dict = {}

        for abnormity_resistance in abnormity_resistance_data.get('abnormityResistances'):
            abnormity_resistance_type = abnormity_resistance.get('type')

            if abnormity_status_effects.get(abnormity_resistance_type) is None:
                continue

            abnormity_resistance_name = abnormity_status_effects.get(abnormity_resistance_type).get('name')
            abnormity_resistance_icon = abnormity_status_effects.get(abnormity_resistance_type).get('icon')
            abnormity_resistance_rate = str(math.trunc(abnormity_resistance.get('rate') / 100))
            abnormity_resistance_rate_icon = self.map_rate_to_image(abnormity_resistance_rate)

            abnormity_resistance_table.update({
                abnormity_resistance_type: {
                    'name': abnormity_resistance_name,
                    'icon': abnormity_resistance_icon,
                    'rate': abnormity_resistance_rate,
                    'rate_icon': abnormity_resistance_rate_icon
                }
            })

        return abnormity_resistance_table

    def get_abnormity_resistance_keys(self):
        abnormity_resistance_keys: dict = {
            'abnormityResistanceSleep': 1,
            'abnormityResistanceSkip': 2,
            'abnormityResistanceParalysis': 3,
            'abnormityResistancePoison': 4,
            'abnormityResistanceMobility': 5,
            'abnormityResistanceCurse': 6,
            'abnormityResistanceBlindness': 7,
            'abnormityResistanceSealPhysics': 8,
            'abnormityResistanceSealTechnique': 9,
            'abnormityResistanceSealSpell': 10,
            'abnormityResistanceSealBreath': 11,
            'abnormityResistanceConfuse': 12,
            'abnormityResistanceCharm': 13
        }

        return abnormity_resistance_keys

    def parse_abnormity_resistance(self, abnormity_resistance_table: dict, display_name: str, description: str):
        abnormity_resistance_keys: dict = self.get_abnormity_resistance_keys()

        for key in abnormity_resistance_keys.keys():
            if key in display_name:
                abnormity_resistance_type = abnormity_resistance_keys.get(key)
                abnormity_resistance_increase_value = abnormity_resistance_table.get(abnormity_resistance_type).get('rate')
                display_name = self.util.clean_text_string(str_to_clean=self.util.replace_string_variable(str_to_clean=display_name, key=key, value=abnormity_resistance_increase_value), unit='%')
                description = self.util.clean_text_string(str_to_clean=self.util.replace_string_variable(str_to_clean=description, key=key, value=abnormity_resistance_increase_value), unit='%')

        return {
            'display_name': display_name,
            'description': description
        }

    def get_element_resistance_keys(self):
        element_resistance_keys: dict = {
            'elementResistanceMera': 1,
            'elementResistanceGira': 2,
            'elementResistanceHyado': 3,
            'elementResistanceBagi': 4,
            'elementResistanceIo': 5,
            'elementResistanceDein': 6,
            'elementResistanceDoruma': 7,
        }

        return element_resistance_keys

    def parse_element_resistance(self, element_resistance_table: dict, display_name: str, description: str):
        element_resistance_keys: dict = self.get_element_resistance_keys()

        for key in element_resistance_keys.keys():
            if key in display_name:
                element_resistance_type = element_resistance_keys.get(key)
                element_resistance_increase_value = self.util.float_to_str(int(element_resistance_table.get(element_resistance_type).get('rate')) / 10)
                display_name = self.util.clean_text_string(str_to_clean=self.util.replace_string_variable(str_to_clean=display_name, key=key, value=element_resistance_increase_value), unit='%')
                description = self.util.clean_text_string(str_to_clean=self.util.replace_string_variable(str_to_clean=description, key=key, value=element_resistance_increase_value), unit='%')

        return {
            'display_name': display_name,
            'description': description
        }

    def build_element_table(self):
        elements: dict = {}

        for path in self.util.get_asset_list('Element'):
            asset = self.util.get_asset_by_path(path)
            document = asset.get('processed_document')
            code = document.get('code')
            display_name = self.util.get_localized_string(document, key='displayName_translation', path=path)
            icon = self.util.get_image_path(document.get('iconPath'))

            elements.update({code: {
                'name': display_name,
                'icon': icon
            }})

        return elements

    def build_abnormity_status_table(self):
        abnormity_status: dict = {}

        for path in self.util.get_asset_list('AbnormityStatus'):
            asset = self.util.get_asset_by_path(path)
            document = asset.get('processed_document')
            code = document.get('targetType')
            display_name = self.util.get_localized_string(document, key='effectStatusName_translation', path=path)
            icon = self.util.get_image_path(document.get('effectIconPath'))

            abnormity_status.update({code: {
                'name': display_name,
                'icon': icon,
            }})

        return abnormity_status

    def build_abnormity_resistance_table(self):
        abnormity_status: dict = {}

        for path in self.util.get_asset_list('AbnormityStatus'):
            asset = self.util.get_asset_by_path(path)
            document = asset.get('processed_document')
            code = document.get('resistanceAbnormityStatus').get('resistanceType')
            display_name = self.util.get_localized_string(document, key='effectStatusName_translation', path=path)
            icon = self.util.get_image_path(document.get('effectIconPath'))

            if display_name == 'Envenom' or display_name == 'Deep Sleep':
                continue

            if code is None:
                continue

            abnormity_status.update({code: {
                'name': display_name,
                'icon': icon,
            }})

        return abnormity_status
