from app.util import Util
from app.data import DataProcessor

class AssetProcessor:

    assets: list
    asset_types_to_process: list
    util: Util
    data_processor: DataProcessor

    def __init__(self, _util: Util, _data_processor: DataProcessor):
        self.util = _util
        self.data_processor = _data_processor

        self.assets = []
        self.asset_types_to_process = []

        self.find_small_asset_groups(asset_limit=25)
        self.asset_types_to_process.append('MonsterProfile')
        self.asset_types_to_process.append('Monsterprofile')
        self.asset_types_to_process.append('AbnormityResistance')
        self.asset_types_to_process.append('AbnormityStatus')
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
        self.asset_types_to_process.append('el')
        self.asset_types_to_process.append('eq')
        self.asset_types_to_process.append('Equipment')
        self.asset_types_to_process.append('EquipmentPassive')
        self.asset_types_to_process.append('EquipmentProfile')
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
        self.asset_types_to_process.append('EventPortal')

        self.asset_types_to_process.append('ActiveSkill')
        self.asset_types_to_process.append('EnemySkill')
        self.asset_types_to_process.append('GuestSkill')
        self.asset_types_to_process.append('NotUsePassiveSkill')
        self.asset_types_to_process.append('NotUseSkill')
        self.asset_types_to_process.append('PassiveSkill')
        self.asset_types_to_process.append('ReactionPassiveSkill')
        self.asset_types_to_process.append('ReactionSkill')

        self.asset_types_to_process.append('ConsumableItem')

        self.asset_types_to_process.append('LootItemGroup')
        self.asset_types_to_process.append('LootitemGroup')
        self.asset_types_to_process.append('LootLottery')

        self.asset_types_to_process.append('AllyMonster')
        self.asset_types_to_process.append('EnemyMonster')

        self.asset_types_to_process.append('Area')
        self.asset_types_to_process.append('AreaGroup')

        self.asset_types_to_process.append('Campaign')

        self.asset_types_to_process.append('ButtonScaler')
        self.asset_types_to_process.append('ButtonSoundPlayer')
        self.asset_types_to_process.append('ContentSizeFitter')
        self.asset_types_to_process.append('CriAtomSource')
        self.asset_types_to_process.append('EnableRendererTrigger')
        self.asset_types_to_process.append('GradationMap')
        self.asset_types_to_process.append('Grid')
        self.asset_types_to_process.append('HorizontalLayoutGroup')
        self.asset_types_to_process.append('Image')
        self.asset_types_to_process.append('InvisibleGraphic')
        self.asset_types_to_process.append('LayoutElement')
        self.asset_types_to_process.append('MultiTransitionTargetButton')
        self.asset_types_to_process.append('ObservablePointerDownTrigger')
        self.asset_types_to_process.append('ObservablePointerUpTrigger')
        self.asset_types_to_process.append('RawImage')
        self.asset_types_to_process.append('SimpleAnimation')

        #self.asset_types_to_process.append('TextMeshProUGUI')
        #self.asset_types_to_process.append('UITermsInjector')

        self.asset_types_to_process.append('LargeBattleAreaSetting')
        self.asset_types_to_process.append('Track Group')

        self.asset_types_to_process.append('Stage')

    def find_small_asset_groups(self, asset_limit):
        unprocessed_assets: dict = self.util.get_unprocessed_assets()

        for asset_type in unprocessed_assets.keys():
            if asset_type.endswith('MasterDataStoreSource')\
            or asset_type.startswith('ArenaGhost')\
            or asset_type.startswith('GuildArenaGhost')\
            or asset_type.startswith('GuildArena')\
            or asset_type.startswith('AreaExtraReward')\
            or asset_type.startswith('LargeBattleAreaSetting')\
            or asset_type.startswith('Track Group'):
                continue

            #if asset_type.endswith('View'):
            #    self.asset_types_to_process.append(asset_type)
            #    continue

            unprocessed_count: int = unprocessed_assets.get(asset_type)

            if unprocessed_count > 0 and unprocessed_count <= asset_limit:
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

                    assert isinstance(document, dict), document

                    display_name: str = self.get_asset_name(document=document, asset_type=asset_type_to_process)

                    print(f'Saving {display_name}')
                    self.util.save_processed_document(path=path, processed_document=document, display_name=display_name)
                except TypeError as ex:
                    print(f'Failed to process with type error {path} {ex}')
                    continue
                except AssertionError as ex:
                    print(f'Failed to process with assertion error {path} {ex}')
                    raise ex
                    continue

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
            display_path: int = display_name.get('m_PathID')
            
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
