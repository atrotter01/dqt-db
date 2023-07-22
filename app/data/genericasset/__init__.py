from app.util import Util
from app.data import DataProcessor

class GenericAsset:

    assets: list
    asset_types_to_process: list
    util: Util
    data_processor: DataProcessor

    def __init__(self, _util: Util, _data_processor: DataProcessor):
        self.util = _util
        self.data_processor = _data_processor

        self.assets = []
        self.asset_types_to_process = []

        self.asset_types_to_process.append('MonsterProfile')
        self.asset_types_to_process.append('Monsterprofile')
        self.asset_types_to_process.append('AbnormityResistance')
        self.asset_types_to_process.append('Achievement')
        self.asset_types_to_process.append('AchievementTarget')
        self.asset_types_to_process.append('ActiveSkillRange')
        self.asset_types_to_process.append('ActiveSkillEnhance')
        self.asset_types_to_process.append('ActiveSkillReach')
        self.asset_types_to_process.append('AccuracyIncrease')
        self.asset_types_to_process.append('AchievementGroup')
        self.asset_types_to_process.append('ArenaStage')
        self.asset_types_to_process.append('Armor')
        self.asset_types_to_process.append('ASO')
        self.asset_types_to_process.append('AST')
        self.asset_types_to_process.append('Board')
        self.asset_types_to_process.append('Campaign')
        self.asset_types_to_process.append('el')
        self.asset_types_to_process.append('eq')
        self.asset_types_to_process.append('Equipment')
        self.asset_types_to_process.append('EquipmentPassive')
        self.asset_types_to_process.append('EquipmentProfile')
        self.asset_types_to_process.append('EventPortal')
        self.asset_types_to_process.append('ExchangeShop')
        self.asset_types_to_process.append('ExchangeShopGoods')
        self.asset_types_to_process.append('ExchangeShopSub')
        self.asset_types_to_process.append('Expansion')
        self.asset_types_to_process.append('ExpansionSetting')
        self.asset_types_to_process.append('GeneralAlchemyMaterial')
        self.asset_types_to_process.append('Global')
        self.asset_types_to_process.append('GuestMonster')
        self.asset_types_to_process.append('HonoraryTitle')
        self.asset_types_to_process.append('ItemGroup')
        self.asset_types_to_process.append('LandingScenario')
        self.asset_types_to_process.append('LeaderPassive')
        self.asset_types_to_process.append('LevelParameterTable')
        self.asset_types_to_process.append('LoadingTip')
        self.asset_types_to_process.append('LoadingTipText')
        self.asset_types_to_process.append('LoginBonus')
        self.asset_types_to_process.append('LoginBonusTemplateMessage')
        self.asset_types_to_process.append('LS')
        self.asset_types_to_process.append('LSTree')
        self.asset_types_to_process.append('MM')
        self.asset_types_to_process.append('MonsterFamily')
        self.asset_types_to_process.append('MonsterPlacement')
        self.asset_types_to_process.append('MonsterRank')
        self.asset_types_to_process.append('MonsterRankRarity')
        self.asset_types_to_process.append('MS')
        self.asset_types_to_process.append('OnProcAbnormityStatus')
        self.asset_types_to_process.append('OnProcHeal')
        self.asset_types_to_process.append('OnProcStatusChange')
        self.asset_types_to_process.append('Operation')
        self.asset_types_to_process.append('Package')
        self.asset_types_to_process.append('PassiveSkillTrigger')
        self.asset_types_to_process.append('PCPP')
        self.asset_types_to_process.append('PS')
        self.asset_types_to_process.append('PSTree')
        self.asset_types_to_process.append('ProfileIcon')
        self.asset_types_to_process.append('RandomEnemyGroup')
        self.asset_types_to_process.append('RankUpRecipe')
        self.asset_types_to_process.append('RankUpTable')
        self.asset_types_to_process.append('ReactionPassive')
        self.asset_types_to_process.append('ReactionPassiveSkillParameterCondition')
        self.asset_types_to_process.append('ReactionPassiveTree')
        self.asset_types_to_process.append('ScoutStamp')
        self.asset_types_to_process.append('SCE')
        self.asset_types_to_process.append('SkillEnhancement')
        self.asset_types_to_process.append('SkillPanel')
        self.asset_types_to_process.append('SkillPanelBackground')
        self.asset_types_to_process.append('SkillPanelUnlockCosts')
        self.asset_types_to_process.append('StageEffect')
        self.asset_types_to_process.append('StageMission')
        self.asset_types_to_process.append('StageMissionList')
        self.asset_types_to_process.append('StagePassive')
        self.asset_types_to_process.append('StagePassiveTree')
        self.asset_types_to_process.append('StatusAbnormityResistance')
        self.asset_types_to_process.append('StatusActiveSkillTypeResistance')
        self.asset_types_to_process.append('StatusAddEffect')
        self.asset_types_to_process.append('StatusChange')
        self.asset_types_to_process.append('StatusChangeGroup')
        self.asset_types_to_process.append('StatusChangeLevel')
        self.asset_types_to_process.append('StatusElement')
        self.asset_types_to_process.append('TrainingBoard')
        self.asset_types_to_process.append('TrainingBoardPanelBackground')
        self.asset_types_to_process.append('TrainingBoardUnlockCosts')
        self.asset_types_to_process.append('TreasureChest')
        self.asset_types_to_process.append('WorldMapAreaSetting')
        self.asset_types_to_process.append('WorldMapStageSetting')

        self.find_small_asset_groups(asset_limit=5)

    def find_small_asset_groups(self, asset_limit):
        unprocessed_assets: dict = self.util.get_unprocessed_assets()

        for asset_type in unprocessed_assets.keys():
            if asset_type.endswith('MasterDataStoreSource')\
            or asset_type.startswith('AreaExtraReward')\
            or asset_type.startswith('GuildArenaGhost')\
            or asset_type.startswith('LargeBattleAreaSetting')\
            or asset_type.startswith('Track Group'):
                continue

            unprocessed_count: int = unprocessed_assets.get(asset_type)

            if unprocessed_count > 0 and unprocessed_count < asset_limit:
                self.asset_types_to_process.append(asset_type)

    def process_assets(self):
        for asset_type_to_process in self.asset_types_to_process:
            print(f'Processing asset type {asset_type_to_process}')

            for path in self.util.get_asset_list(asset_type=asset_type_to_process):
                asset: dict = self.util.get_asset_by_path(path=path, deflate_data=True)

                if asset.get('processed') is True:
                    continue

                path: int = asset.get('path')
                print(f'Processing {path}')

                try:
                    document: dict = None

                    if asset_type_to_process.strip().endswith('CanvasView'):
                        document = asset.get('document')
                    else:
                        document = self.data_processor.parse_asset(path=path)

                    assert type(document) is dict, document

                    display_name: str = None
                    
                    if asset_type_to_process == 'LoginBonus':
                        display_name = document.get('loginBonusName')
                    elif asset_type_to_process == 'PCPP':
                        display_name = document.get('itemName')
                    else:
                        display_name = document.get('displayName')

                        if display_name is None or display_name == '':
                            display_name = document.get('m_Name')

                        if display_name is None or display_name == '':
                            display_name = f'{asset_type_to_process}: {path}'

                    assert type(display_name) is str, document
                    assert display_name != '', document

                    print(f'Saving {display_name}')
                    self.util.save_processed_document(path=path, processed_document=document, display_name=display_name)
                except TypeError as ex:
                    print(f'Failed to process with type error {path} {ex}')
                    continue
                except AssertionError as ex:
                    print(f'Failed to process with assertion error {path} {ex}')
                    continue
