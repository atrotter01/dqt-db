import requests
import json
from app.util import Util

def cache_stage_structure():
    event_portal_list = util.get_asset_list('EventPortal')
    event_portals: dict = {}

    for event_portal_path in event_portal_list:
        event_portal = util.get_asset_by_path(event_portal_path).get('processed_document')
        event_portal_id = event_portal.get('linked_asset_id')
        event_portal_name = event_portal.get('m_Name')

        event_portals[event_portal_id] = {}
        event_portals[event_portal_id]['areas'] = []
        event_portals[event_portal_id]['name'] = event_portal_name

        for area in event_portal.get('eventAreaList'):
            event_portals[event_portal_id]['areas'].append(area.get('linked_asset_id'))

        for area in event_portal.get('eventBattleRoadAreaList'):
            event_portals[event_portal_id]['areas'].append(area.get('linked_asset_id'))

        if event_portal.get('eventAreaContainingMegaMonsterStage').get('m_PathID') is None:
            event_portals[event_portal_id]['areas'].append(event_portal.get('eventAreaContainingMegaMonsterStage').get('linked_asset_id'))

        if event_portal.get('scoreChallengeAreaGroup').get('m_PathID') is None:
            event_portals[event_portal_id]['areas'].append(event_portal.get('scoreChallengeAreaGroup').get('linked_asset_id'))

    stage_structure: dict = {}

    for area in area_data:
        area_id = area.get('id')
        area_name = area.get('area_display_name')
        area_banner_path = area.get('area_banner_path')
        area_category = area.get('area_category')
        associated_area_group_id = area.get('area_group')

        if stage_structure.get(area_id) is None:
            stage_structure[area_id] = {}

        stage_structure[area_id]['area_group_id'] = associated_area_group_id
        stage_structure[area_id]['area_banner_path'] = area_banner_path
        stage_structure[area_id]['area_category'] = area_category
        stage_structure[area_id]['area_name'] = area_name
        stage_structure[area_id]['stages'] = []
        stage_structure[area_id]['stage_names'] = []
        stage_structure[area_id]['area_group_children'] = []

    for area_id in stage_structure:
        has_event_portal: bool = False

        for event_portal in event_portals:
            if area_id in event_portals[event_portal]['areas']:
                has_event_portal = True

        stage_structure[area_id]['has_event_portal'] = has_event_portal

    for area_group in area_group_data:
        area_group_id = area_group.get('id')
        area_group_name = area_group.get('area_group_display_name')
        area_group_banner_path = area_group.get('area_group_banner_path')
        area_group_parent_id = area_group.get('area_group_parent')
        area_group_children = area_group.get('area_group_children')

        for area in stage_structure:
            if stage_structure[area]['area_group_id'] == str(area_group_id):
                stage_structure[area]['area_group_name'] = area_group_name
                stage_structure[area]['area_group_parent_id'] = area_group_parent_id
                stage_structure[area]['area_group_banner_path'] = area_group_banner_path
                stage_structure[area]['area_group_children'].extend(area_group_children)

    for stage in stage_data:
        stage_id = stage.get('id')
        stage_name = stage.get('stage_display_name')
        stage_area_id = stage.get('stage_area_id')
        stage_structure[stage_area_id]['stages'].append({
            'stage_id': stage_id,
            'stage_name': stage_name
        })

    util.save_redis_asset(cache_key='stage_structure_parsed_asset', data=stage_structure)

def cache_stage_monster_lookup_table():
    stage_monster_lookup_parsed_asset: dict = {}

    for stage in stage_data:
        stage_id = stage.get('id')
        stage_name = stage.get('stage_display_name')
        stage_area_id = stage.get('stage_area_id')

        for enemy in stage.get('stage_enemies'):
            monster_id: str = enemy.get('monster').get('id')

            if stage_monster_lookup_parsed_asset.get(monster_id) is None:
                stage_monster_lookup_parsed_asset[monster_id] = []

            stage_monster_lookup_parsed_asset[monster_id].append({
                'stage_id': stage_id,
                'stage_name': stage_name
            })

        for enemy in stage.get('stage_random_enemies'):
            monster_id: str = enemy.get('monster').get('id')

            if stage_monster_lookup_parsed_asset.get(monster_id) is None:
                stage_monster_lookup_parsed_asset[monster_id] = []

            stage_monster_lookup_parsed_asset[monster_id].append({
                'stage_id': stage_id,
                'stage_name': stage_name
            })

        for enemy in stage.get('stage_reinforcement_enemies'):
            monster_id: str = enemy.get('monster').get('id')

            if stage_monster_lookup_parsed_asset.get(monster_id) is None:
                stage_monster_lookup_parsed_asset[monster_id] = []

            stage_monster_lookup_parsed_asset[monster_id].append({
                'stage_id': stage_id,
                'stage_name': stage_name
            })

    util.save_redis_asset(cache_key='stage_monster_lookup_parsed_asset', data=stage_monster_lookup_parsed_asset)

def cache_skill_unit_table():
    unit_data = unit_response.json()
    enemy_monster_data = enemy_monster_response.json()

    skill_unit_table: dict = {}

    for unit in unit_data:
        unit_id: str = unit.get('id')
        unit_name: str = unit.get('display_name')
        unit_icon: str = unit.get('unit_icon')

        for skill in unit.get('active_skills'):
            skill_id = skill.get('id')

            if skill_unit_table.get(skill_id) is None:
                skill_unit_table[skill_id] = []
            
            skill_unit_table[skill_id].append({
                'unit_id': unit_id,
                'unit_name': unit_name,
                'unit_icon': unit_icon,
                'unit_type': 'Unit'
            })

        for skill in unit.get('passive_skills'):
            skill_id = skill.get('id')

            if skill_unit_table.get(skill_id) is None:
                skill_unit_table[skill_id] = []
            
            skill_unit_table[skill_id].append({
                'unit_id': unit_id,
                'unit_name': unit_name,
                'unit_icon': unit_icon,
                'unit_type': 'Unit'
            })

        for skill in unit.get('awakening_passive_skills'):
            skill_id = skill.get('id')

            if skill_unit_table.get(skill_id) is None:
                skill_unit_table[skill_id] = []
            
            skill_unit_table[skill_id].append({
                'unit_id': unit_id,
                'unit_name': unit_name,
                'unit_icon': unit_icon,
                'unit_type': 'Unit'
            })

        for skill in unit.get('reaction_passive_skills'):
            skill_id = skill.get('id')

            if skill_unit_table.get(skill_id) is None:
                skill_unit_table[skill_id] = []
            
            skill_unit_table[skill_id].append({
                'unit_id': unit_id,
                'unit_name': unit_name,
                'unit_icon': unit_icon,
                'unit_type': 'Unit'
            })

        for skill in unit.get('awakening_reaction_passive_skills'):
            skill_id = skill.get('id')

            if skill_unit_table.get(skill_id) is None:
                skill_unit_table[skill_id] = []
            
            skill_unit_table[skill_id].append({
                'unit_id': unit_id,
                'unit_name': unit_name,
                'unit_icon': unit_icon,
                'unit_type': 'Unit'
            })

        for panel in unit.get('blossoms'):
            if panel.get('type') == 'Passive Skill' or panel.get('type') == 'Active Skill':
                skill = panel.get('data')
                skill_id = skill.get('id')

                if skill_unit_table.get(skill_id) is None:
                    skill_unit_table[skill_id] = []
            
                skill_unit_table[skill_id].append({
                    'unit_id': unit_id,
                    'unit_name': unit_name,
                    'unit_icon': unit_icon,
                    'unit_type': 'Unit'
                })

        for panel in unit.get('character_builder_blossoms'):
            if panel.get('type') == 'Passive Skill' or panel.get('type') == 'Active Skill':
                skill = panel.get('data')
                skill_id = skill.get('id')

                if skill_unit_table.get(skill_id) is None:
                    skill_unit_table[skill_id] = []
            
                skill_unit_table[skill_id].append({
                    'unit_id': unit_id,
                    'unit_name': unit_name,
                    'unit_icon': unit_icon,
                    'unit_type': 'Unit'
                })

    for enemy_monster in enemy_monster_data:
        enemy_monster_id: str = enemy_monster.get('id')
        enemy_monster_name: str = enemy_monster.get('enemy_display_name')
        enemy_monster_icon: str = enemy_monster.get('enemy_unit_icon')

        for skill in enemy_monster.get('enemy_active_skills'):
            skill_id = skill.get('id')

            if skill_unit_table.get(skill_id) is None:
                skill_unit_table[skill_id] = []
            
            skill_unit_table[skill_id].append({
                'unit_id': enemy_monster_id,
                'unit_name': enemy_monster_name,
                'unit_icon': enemy_monster_icon,
                'unit_type': 'Enemy Monster'
            })

        for skill in enemy_monster.get('enemy_passive_skills'):
            skill_id = skill.get('id')

            if skill_unit_table.get(skill_id) is None:
                skill_unit_table[skill_id] = []
            
            skill_unit_table[skill_id].append({
                'unit_id': enemy_monster_id,
                'unit_name': enemy_monster_name,
                'unit_icon': enemy_monster_icon,
                'unit_type': 'Enemy Monster'
            })

        for skill in enemy_monster.get('enemy_reaction_skills'):
            skill_id = skill.get('id')

            if skill_unit_table.get(skill_id) is None:
                skill_unit_table[skill_id] = []
            
            skill_unit_table[skill_id].append({
                'unit_id': enemy_monster_id,
                'unit_name': enemy_monster_name,
                'unit_icon': enemy_monster_icon,
                'unit_type': 'Enemy Monster'
            })

    util.save_redis_asset(cache_key='skill_unit_table_parsed_asset', data=skill_unit_table)

def cache_equipment_skill_table():
    skill_equipment_cache: dict = {}

    for equipment in equipment_response.json():
        equipment_id = equipment.get('id')
        equipment_icon = equipment.get('equipment_icon')
        equipment_name = equipment.get('equipment_display_name')
        seen_skills: list = []

        if equipment.get('equipment_passive_skill') is not None:
            skill_id = equipment.get('equipment_passive_skill').get('id')

            if skill_equipment_cache.get(skill_id) is None:
                skill_equipment_cache[skill_id] = []

            if not skill_id in seen_skills:
                seen_skills.append(skill_id)
                skill_equipment_cache[skill_id].append({
                    'equipment_id': equipment_id,
                    'equipment_icon': equipment_icon,
                    'equipment_name': equipment_name,
                })

        if equipment.get('equipment_reaction_skill') is not None:
            skill_id = equipment.get('equipment_reaction_skill').get('id')

            if skill_equipment_cache.get(skill_id) is None:
                skill_equipment_cache[skill_id] = []

            if not skill_id in seen_skills:
                seen_skills.append(skill_id)
                skill_equipment_cache[skill_id].append({
                    'equipment_id': equipment_id,
                    'equipment_icon': equipment_icon,
                    'equipment_name': equipment_name,
                })

        for slot in equipment.get('equipment_alchemy_slots').get('slot_1'):
            skill_id = slot.get('passive_skill').get('id')

            if skill_equipment_cache.get(skill_id) is None:
                skill_equipment_cache[skill_id] = []

            if not skill_id in seen_skills:
                seen_skills.append(skill_id)
                skill_equipment_cache[skill_id].append({
                    'equipment_id': equipment_id,
                    'equipment_icon': equipment_icon,
                    'equipment_name': equipment_name,
                })

        for slot in equipment.get('equipment_alchemy_slots').get('slot_2'):
            skill_id = slot.get('passive_skill').get('id')

            if skill_equipment_cache.get(skill_id) is None:
                skill_equipment_cache[skill_id] = []

            if not skill_id in seen_skills:
                seen_skills.append(skill_id)
                skill_equipment_cache[skill_id].append({
                    'equipment_id': equipment_id,
                    'equipment_icon': equipment_icon,
                    'equipment_name': equipment_name,
                })

        if equipment.get('equipment_alchemy_slots').get('slot_3') is not None:
            for slot in equipment.get('equipment_alchemy_slots').get('slot_3'):
                skill_id = slot.get('passive_skill').get('id')

                if skill_equipment_cache.get(skill_id) is None:
                    skill_equipment_cache[skill_id] = []

                if not skill_id in seen_skills:
                    seen_skills.append(skill_id)
                    skill_equipment_cache[skill_id].append({
                        'equipment_id': equipment_id,
                        'equipment_icon': equipment_icon,
                        'equipment_name': equipment_name,
                    })

    util.save_redis_asset('skill_equipment_parsed_asset', skill_equipment_cache)

def cache_item_location_table():
    item_location_table: dict = {}

    for stage in stage_data:
        location_id = stage.get('id')
        location_name = stage.get('stage_display_name')

        for drop in stage.get('stage_drops'):
            for loot in drop.get('loot_group').get('loot'):
                item_id = loot.get('path')

                if item_location_table.get(item_id) is None:
                    item_location_table[item_id] = []

                item_location_table[item_id].append({
                    'location_id': location_id,
                    'location_name': location_name,
                    'location_type': 'Stage'
                })

        for mission in stage.get('stage_missions'):
            item_id = mission.get('reward_id')

            if item_location_table.get(item_id) is None:
                item_location_table[item_id] = []

            item_location_table[item_id].append({
                'location_id': location_id,
                'location_name': location_name,
                'location_type': 'Stage'
            })

    for shop in shop_data:
        location_id = shop.get('id')
        location_name = shop.get('display_name')

        seen_items: list = []

        for good in shop.get('shop_goods'):
            item_id = good.get('goods_path')

            if item_id in seen_items:
                continue

            seen_items.append(item_id)

            if item_location_table.get(item_id) is None:
                item_location_table[item_id] = []

            item_location_table[item_id].append({
                'location_id': location_id,
                'location_name': location_name,
                'location_type': 'Shop'
            })

    util.save_redis_asset('item_location_parsed_asset', item_location_table)

def cache_unit_profile_map():
    profile_unit_map: dict = {}

    for path in util.get_asset_list('AllyMonster'):
        asset = util.get_asset_by_path(path=path, deflate_data=True)

        processed_document = asset.get('processed_document')
        profile_id = processed_document.get('profile').get('linked_asset_id')

        profile_unit_map[profile_id] = path

    util.save_redis_asset('profile_unit_map_parsed_asset', profile_unit_map)

if __name__ == '__main__':
    util: Util = Util()

    #unit_response = requests.get(f'http://localhost:5000/api/unit')
    #active_skill_response = requests.get(f'http://localhost:5000/api/skill/active_skill')
    #passive_skill_response = requests.get(f'http://localhost:5000/api/skill/passive_skill')
    #reaction_skill_response = requests.get(f'http://localhost:5000/api/skill/reaction_skill')
    #enemy_skill_response = requests.get(f'http://localhost:5000/api/skill/enemy_skill')
    #accolade_response = requests.get(f'http://localhost:5000/api/accolade')
    #equipment_response = requests.get(f'http://localhost:5000/api/equipment')
    #enemy_monster_response = requests.get(f'http://localhost:5000/api/enemy_monster')

    #consumable_item_response = requests.get(f'http://localhost:5000/api/item/consumableitem')
    #profile_icon_response = requests.get(f'http://localhost:5000/api/item/profileicon')
    #package_response = requests.get(f'http://localhost:5000/api/item/package')
    #shop_response = requests.get(f'http://localhost:5000/api/shop')

    #area_response = requests.get(f'http://localhost:5000/api/area')
    #area_group_response = requests.get(f'http://localhost:5000/api/area_group')
    #stage_response = requests.get('http://localhost:5000/api/stage')

    #area_data = area_response.json()
    #area_group_data = area_group_response.json()
    #stage_data = stage_response.json()
    #shop_data = shop_response.json()
    #unit_data = unit_response.json()

    #cache_stage_structure()
    #cache_skill_unit_table()
    #cache_stage_monster_lookup_table()
    #cache_equipment_skill_table()
    #cache_item_location_table()
    #cache_unit_profile_map()
