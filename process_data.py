import cProfile

from app.util import Util
from app.data.translation import Translation

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
translation = Translation(util)

allymonster = AllyMonster(_util=util, _translation=translation)
arena_ghost_npc = ArenaGhostNPC(_util=util, _translation=translation)
area = Area(_util=util, _translation=translation)
enemy_monster = EnemyMonster(_util=util, _translation=translation)
generic_asset = GenericAsset(_util=util, _translation=translation)
item = Item(_util=util, _translation=translation)
loot = Loot(_util=util, _translation=translation)
skill = Skill(_util=util, _translation=translation)
stage = Stage(_util=util, _translation=translation)

generic_asset.process_assets()

allymonster.process_assets()
arena_ghost_npc.process_assets()
area.process_assets()
enemy_monster.process_assets()
item.process_assets()
loot.process_assets()
skill.process_assets()
stage.process_assets()
