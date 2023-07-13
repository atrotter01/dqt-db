from app.translation import Translation
from app.util import Util

class GenericAsset:

    assets: list
    asset_types_to_process: list
    util: Util
    translation: Translation

    def __init__(self, _util: Util, _translation: Translation):
        self.util = _util
        self.translation = _translation

        self.assets = []
        self.asset_types_to_process = []
        self.asset_types_to_process.append('MonsterProfile')

        self.asset_types_to_process.append('ActiveSkillRange')
        self.asset_types_to_process.append('ActiveSkillEnhance')
        self.asset_types_to_process.append('ActiveSkillReach')
        self.asset_types_to_process.append('AccuracyIncrease')
        self.asset_types_to_process.append('AchievementGroup')
        self.asset_types_to_process.append('Armor')
        self.asset_types_to_process.append('ArenaGhostPartyMember')
        self.asset_types_to_process.append('ASO')
        self.asset_types_to_process.append('AST')
        self.asset_types_to_process.append('Board')
        self.asset_types_to_process.append('Campaign')
        self.asset_types_to_process.append('eq')
        self.asset_types_to_process.append('HonoraryTitle')
        self.asset_types_to_process.append('ItemGroup')
        self.asset_types_to_process.append('LeaderPassive')
        self.asset_types_to_process.append('LevelParameterTable')
        self.asset_types_to_process.append('LoadingTip')
        self.asset_types_to_process.append('LS')
        self.asset_types_to_process.append('LSTree')
        self.asset_types_to_process.append('MM')
        self.asset_types_to_process.append('MS')
        self.asset_types_to_process.append('MonsterPlacement')
        self.asset_types_to_process.append('MonsterRank')
        self.asset_types_to_process.append('Operation')
        self.asset_types_to_process.append('PS')
        self.asset_types_to_process.append('PSTree')
        self.asset_types_to_process.append('ProfileIcon')
        self.asset_types_to_process.append('RandomEnemyGroup')
        self.asset_types_to_process.append('RankUpRecipe')
        self.asset_types_to_process.append('RankUpTable')
        self.asset_types_to_process.append('SkillEnhancement')
        self.asset_types_to_process.append('SkillPanel')
        self.asset_types_to_process.append('StageEffect')

    def process_assets(self):
        for asset_type_to_process in self.asset_types_to_process:
            print(f'Processing asset type {asset_type_to_process}')

            for path in self.util.get_asset_list(asset_type=asset_type_to_process):
                asset: dict = self.util.get_asset_by_path(path)

                if asset.get('processed_document') is not None:
                    continue

                path: int = asset.get('path')

                document: dict = self.util.parse_asset(path=path)
                assert type(document) is dict, document

                translated_document: dict = self.translation.translate_dict(document)
                assert type(translated_document) is dict, translated_document

                display_name: str = translated_document.get('displayName')

                if display_name is None or display_name == '':
                    display_name = translated_document.get('m_Name')

                assert type(display_name) is str, translated_document
                assert display_name != '', translated_document

                print(f'Saving {display_name}')
                self.util.save_processed_document(path=path, processed_document=translated_document, display_name=display_name)
