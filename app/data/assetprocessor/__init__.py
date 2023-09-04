from app.util import Util
from app.data import DataProcessor

class AssetProcessor:

    util: Util
    data_processor: DataProcessor

    def __init__(self, _util: Util, _data_processor: DataProcessor):
        self.util = _util
        self.data_processor = _data_processor

    def process_assets(self):
        unprocessed_containers: dict = self.util.get_assets_by_container(processed_filter=False)

        for container in sorted(unprocessed_containers):
            if 'scriptabledata' not in container:
                continue

            asset_types = unprocessed_containers.get(container)

            for asset_type in sorted(asset_types):
                if 'MasterData' in asset_type\
                or asset_type.startswith('AreaExtraReward')\
                or asset_type.startswith('ArenaGhost')\
                or asset_type.startswith('GuildArenaCompetition')\
                or asset_type.startswith('GuildArenaGhost'):
                    continue

                assets: list = unprocessed_containers.get(container).get(asset_type)

                print(f'Processing asset type {asset_type}')

                for asset in assets:
                    path = asset.get('path')
                    print(f'Processing {path}')

                    self.process_asset(path=path, asset_type=asset_type)

    def process_asset(self, path, asset_type):
        try:
            document: dict = self.data_processor.parse_asset(path=str(path))

            assert isinstance(document, dict), document

            display_name: str = self.get_asset_name(document=document, asset_type=asset_type)

            print(f'Saving {display_name}')
            self.util.save_processed_document(path=path, processed_document=document, display_name=display_name)
        except TypeError as ex:
            print(f'Failed to process with type error {path} {ex}')
            raise ex
        except AssertionError as ex:
            print(f'Failed to process with assertion error {path} {ex}')
            raise ex

    def get_asset_name(self, document, asset_type):
        if asset_type == 'LoginBonus':
            return document.get('loginBonusName_translation').get('gbl') or document.get('loginBonusName_translation').get('ja')

        if asset_type == 'PCPP':
            return document.get('itemName_translation').get('gbl') or document.get('itemName_translation').get('ja')

        if asset_type == 'EnemyMonster':
            return document.get('profile').get('displayName_translation').get('gbl') or document.get('profile').get('displayName_translation').get('ja')

        if asset_type == 'AllyMonster':
            return document.get('profile').get('displayName_translation').get('gbl') or document.get('profile').get('displayName_translation').get('ja')

        if asset_type == 'Stage':
            achievement_target_name: str = None
            area_group_name: str = None

            if document.get('area').get('achievementTarget') is not None:
                if document.get('area').get('achievementTarget').get('displayName_translation') is not None:
                    achievement_target_name = document.get('area').get('achievementTarget').get('displayName_translation').get('gbl') or document.get('area').get('achievementTarget').get('displayName_translation').get('ja')

            if document.get('area').get('areaGroup') is not None:
                if document.get('area').get('areaGroup').get('displayName_translation') is not None:
                    area_group_name: str = document.get('area').get('areaGroup').get('displayName_translation').get('gbl') or document.get('area').get('areaGroup').get('displayName_translation').get('ja')

            area_name: str = document.get('area').get('displayName_translation').get('gbl') or document.get('area').get('displayName_translation').get('ja')
            stage_name: str = document.get('displayName_translation').get('gbl') or document.get('displayName_translation').get('ja')

            display_name: str = None

            if achievement_target_name is not None and area_group_name is not None:
                display_name = f'{achievement_target_name} - {area_group_name} - {area_name} - {stage_name}'
            elif area_group_name is not None:
                display_name = f'{area_group_name} - {area_name} - {stage_name}'
            elif achievement_target_name is not None:
                display_name = f'{achievement_target_name} - {area_name} - {stage_name}'
            else:
                display_name = f'{area_name} - {stage_name}'

            return display_name

        display_name: str = None

        if document.get('displayName_translation') is not None:
            display_name = document.get('displayName_translation').get('gbl') or document.get('displayName_translation').get('ja')
        else:
            display_name = document.get('displayName')

        if isinstance(display_name, dict):
            display_path: str = display_name.get('m_PathID')

            if display_path is not None:
                display_asset = self.util.get_asset_by_path(display_path)

                if display_asset.get('display_name_translation'):
                    display_name = display_asset.get('display_name_translation').get('gbl') or display_asset.get('display_name_translation').get('ja')
                else:
                    display_name = display_asset.get('display_name')
            else:
                display_name = None

        if display_name is None or display_name == '':
            display_name = document.get('m_Name')

        if display_name == '':
            display_name = None

        return display_name
