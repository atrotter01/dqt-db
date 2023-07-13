from app.util import Util
from app.translation import Translation
from app.data import DataProcessor

from app.data.allymonster import AllyMonster
from app.data.arenaghostnpc import ArenaGhostNPC
from app.data.area import Area
from app.data.enemymonster import EnemyMonster
from app.data.genericasset import GenericAsset
from app.data.item import Item
from app.data.loot import Loot
from app.data.skill import Skill
from app.data.stage import Stage

util = Util()
data_processor = DataProcessor(_util=util)
translation = Translation(_util=util)

allymonster = AllyMonster(_util=util, _translation=translation, _data_processor=data_processor)
arena_ghost_npc = ArenaGhostNPC(_util=util, _translation=translation, _data_processor=data_processor)
area = Area(_util=util, _translation=translation, _data_processor=data_processor)
enemy_monster = EnemyMonster(_util=util, _translation=translation, _data_processor=data_processor)
generic_asset = GenericAsset(_util=util, _translation=translation, _data_processor=data_processor)
item = Item(_util=util, _translation=translation, _data_processor=data_processor)
loot = Loot(_util=util, _translation=translation, _data_processor=data_processor)
skill = Skill(_util=util, _translation=translation, _data_processor=data_processor)
stage = Stage(_util=util, _translation=translation, _data_processor=data_processor)

generic_asset.process_assets()

allymonster.process_assets()
arena_ghost_npc.process_assets()
area.process_assets()
enemy_monster.process_assets()
item.process_assets()
loot.process_assets()
skill.process_assets()
stage.process_assets()
