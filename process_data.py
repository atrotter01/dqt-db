import cProfile

from app.util import Util
from app.translation import Translation

from app.allymonster import AllyMonster
from app.arenaghostnpc import ArenaGhostNPC
from app.area import Area
from app.enemymonster import EnemyMonster
from app.genericasset import GenericAsset
from app.item import Item
from app.loot import Loot
from app.skill import Skill
from app.stage import Stage

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

#allymonster.process_assets()
arena_ghost_npc.process_assets()
#area.process_assets()
#enemy_monster.process_assets()
#generic_asset.process_assets()
#item.process_assets()
#loot.process_assets()
#skill.process_assets()
#stage.process_assets()