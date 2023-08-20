import requests
import json
from app.util import Util
util: Util = Util()

#requests.get(f'http://localhost:5000/api/unit')
#requests.get(f'http://localhost:5000/api/skill/active_skill')
#requests.get(f'http://localhost:5000/api/skill/passive_skill')
#requests.get(f'http://localhost:5000/api/skill/reaction_skill')
#requests.get(f'http://localhost:5000/api/skill/enemy_skill')
#requests.get(f'http://localhost:5000/api/equipment')
#requests.get(f'http://localhost:5000/api/enemy_monster')

area_response = requests.get(f'http://localhost:5000/api/area')
area_group_response = requests.get(f'http://localhost:5000/api/area_group')
stage_response = requests.get('http://localhost:5000/api/stage')

area_data = area_response.json()
area_group_data = area_group_response.json()
stage_data = stage_response.json()

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
    associated_area_group_id = area.get('area_group')

    if stage_structure.get(area_id) is None:
        stage_structure[area_id] = {}

    stage_structure[area_id]['area_group_id'] = associated_area_group_id
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
    area_group_parent_id = area_group.get('area_group_parent')
    area_group_children = area_group.get('area_group_children')

    has_event_portal: bool = False

    for area in stage_structure:
        if stage_structure[area]['area_group_id'] == str(area_group_id):
            stage_structure[area]['area_group_name'] = area_group_name
            stage_structure[area]['area_group_parent_id'] = area_group_parent_id
            stage_structure[area]['area_group_children'].extend(area_group_children)

            if stage_structure[area]['has_event_portal'] is True:
                has_event_portal = True
    
    if has_event_portal is False and area_group_parent_id is None:
        print(area_group_name)

for stage in stage_data:
    stage_id = stage.get('id')
    stage_name = stage.get('stage_display_name')
    stage_area_id = stage.get('stage_area_id')
    stage_structure[stage_area_id]['stages'].append(stage_id)
    stage_structure[stage_area_id]['stage_names'].append(stage_name)

#print(json.dumps(stage_structure))
