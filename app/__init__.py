import json
import requests
from flask import Flask, Blueprint, render_template, Response
from flask_restx import Api
from flask_autoindex import AutoIndex
from werkzeug.middleware.proxy_fix import ProxyFix
from app.api.accolade import api as accolade_api
from app.api.area import api as area_api
from app.api.area_group import api as area_group_api
from app.api.asset import api as asset_api
from app.api.asset_container import api as asset_container_api
from app.api.asset_list import api as asset_list_api
from app.api.asset_type import api as asset_type_api
from app.api.enemy_monster import api as enemy_monster_api
from app.api.equipment import api as equipment_api
from app.api.farmable import api as farmable_api
from app.api.item import api as item_api
from app.api.shop import api as shop_api
from app.api.skill import api as skill_api
from app.api.stage import api as stage_api
from app.api.unit import api as unit_api
from app.util import Util

app = Flask(__name__, static_folder='../static', template_folder='../templates')
app.wsgi_app = ProxyFix(app.wsgi_app)

blueprint: Blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(
    blueprint,
    version='1.0',
    title='DQT API',
    doc=False
)

api.add_namespace(accolade_api)
api.add_namespace(area_api)
api.add_namespace(area_group_api)
api.add_namespace(asset_api)
api.add_namespace(asset_container_api)
api.add_namespace(asset_list_api)
api.add_namespace(asset_type_api)
api.add_namespace(enemy_monster_api)
api.add_namespace(equipment_api)
api.add_namespace(farmable_api)
api.add_namespace(item_api)
api.add_namespace(shop_api)
api.add_namespace(skill_api)
api.add_namespace(stage_api)
api.add_namespace(unit_api)

app.register_blueprint(blueprint=blueprint)

files_index = AutoIndex(app, browse_root='static/dqt_images', add_url_rules=False)
util: Util = Util()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/unit/')
def unit():
    api_response = requests.get(url='http://localhost:5000/api/unit/')
    units = []

    if api_response.status_code == 200:
        units = api_response.json()

    return render_template('unit_list.html', units=units)

@app.route('/skill/')
def skill():
    active_skill_api_response = requests.get(url='http://localhost:5000/api/skill/active_skill')
    active_skills = []

    if active_skill_api_response.status_code == 200:
        active_skills = active_skill_api_response.json()

    enemy_skill_api_response = requests.get(url='http://localhost:5000/api/skill/enemy_skill')
    enemy_skills = []

    if enemy_skill_api_response.status_code == 200:
        enemy_skills = enemy_skill_api_response.json()

    passive_skill_api_response = requests.get(url='http://localhost:5000/api/skill/passive_skill')
    passive_skills = []

    if passive_skill_api_response.status_code == 200:
        passive_skills = passive_skill_api_response.json()

    reaction_skill_api_response = requests.get(url='http://localhost:5000/api/skill/reaction_skill')
    reaction_skills = []

    if reaction_skill_api_response.status_code == 200:
        reaction_skills = reaction_skill_api_response.json()

    return render_template('skill_list.html', active_skills=active_skills, enemy_skills=enemy_skills, passive_skills=passive_skills, reaction_skills=reaction_skills)

@app.route('/skill/<type_of_skill>/<skill>')
def skill_detail(type_of_skill, skill):
    api_response = requests.get(url=f'http://localhost:5000/api/skill/{type_of_skill}/{skill}')
    skill_data = []
    skill_learned_by = []
    
    if util.get_redis_asset('skill_unit_table_parsed_asset').get(skill) is not None:
        skill_learned_by.extend(util.get_redis_asset('skill_unit_table_parsed_asset').get(skill))

    if api_response.status_code == 200:
        skill_data = api_response.json()

    return render_template('skill_detail.html', skill=skill_data[0], skill_learned_by=skill_learned_by)

@app.route('/item/')
def item():
    consumable_items = []
    profile_icons = []
    packages = []

    item_api_response = requests.get(url='http://localhost:5000/api/item/consumableitem')
    if item_api_response.status_code == 200:
        consumable_items = item_api_response.json()

    profile_icon_api_response = requests.get(url='http://localhost:5000/api/item/profileicon')
    if profile_icon_api_response.status_code == 200:
        profile_icons = profile_icon_api_response.json()

    package_api_response = requests.get(url='http://localhost:5000/api/item/package')
    if package_api_response.status_code == 200:
        packages = package_api_response.json()

    return render_template('item.html', items=consumable_items, icons=profile_icons, packages=packages)

@app.route('/unit/<unit>')
def unit_detail(unit):
    api_response = requests.get(url=f'http://localhost:5000/api/unit/{unit}')
    unit = []

    if api_response.status_code == 200:
        unit = api_response.json()

    return render_template('unit_detail.html', unit=unit[0])

@app.route('/equipment/')
def equipment():
    api_response = requests.get(url=f'http://localhost:5000/api/equipment')
    equipments = []

    if api_response.status_code == 200:
        equipments = api_response.json()

    return render_template('equipment_list.html', equipments=equipments)

@app.route('/equipment/<equipment>')
def equipment_detail(equipment):
    api_response = requests.get(url=f'http://localhost:5000/api/equipment/{equipment}')
    equipment = []

    if api_response.status_code == 200:
        equipment = api_response.json()

    return render_template('equipment_detail.html', equipment=equipment[0])

@app.route('/accolade/')
def accolade():
    api_response = requests.get(url='http://localhost:5000/api/accolade/')
    accolades = []

    if api_response.status_code == 200:
        accolades = api_response.json()

    return render_template('accolade.html', accolades=accolades)

@app.route('/asset_container/')
def asset_container():
    api_response = requests.get(url='http://localhost:5000/api/asset_container')
    asset_container_response: dict = {}
    asset_containers: list = []

    if api_response.status_code == 200:
        asset_container_response = api_response.json().get('asset_containers')

    for container in asset_container_response:
        if container.startswith('/mnt/'):
            continue

        asset_containers.append(container)

    return render_template('asset_container.html', asset_containers=asset_containers)

@app.route('/asset_container/<container>')
def asset_type(container):
    api_response = requests.get(url='http://localhost:5000/api/asset_container')
    asset_container_response: dict = {}
    asset_types: list = []

    if api_response.status_code == 200:
        asset_container_response = api_response.json().get('asset_containers')

    for asset_container in asset_container_response.keys():
        if asset_container.replace('/', '___') != container:
            continue

        for asset_type in asset_container_response.get(asset_container):
            asset_types.append({ 'container': container, 'asset_type': asset_type })

    return render_template('asset_type.html', asset_types=asset_types)

@app.route('/asset_container/<container>/<container_asset_type>')
def asset_list(container, container_asset_type):
    api_response = requests.get(url='http://localhost:5000/api/asset_container')
    asset_container_response: dict = {}
    container_key: str = container.replace('___', '/')
    assets: list = []

    if api_response.status_code == 200:
        asset_container_response = api_response.json().get('asset_containers')
        assets.extend(asset_container_response.get(container_key).get(container_asset_type))

    return render_template('asset_list.html', assets=assets)

@app.route('/asset/<path_id>')
def asset(path_id):
    api_response = requests.get(url=f'http://localhost:5000/api/asset/{path_id}')
    asset = {}

    if api_response.status_code == 200:
        asset = api_response.json()[0]

    return Response(json.dumps(asset, indent=2), mimetype='text/json')

@app.route('/shop/')
def shop():
    api_response = requests.get(url='http://localhost:5000/api/shop')
    shops = []

    if api_response.status_code == 200:
        shops = api_response.json()

    return render_template('shop.html', shops=shops)

@app.route('/shop/<shop_id>')
def shop_goods(shop_id):
    api_response = requests.get(url=f'http://localhost:5000/api/shop/{shop_id}')
    shop_goods = []

    if api_response.status_code == 200:
        shop_goods = api_response.json()

    return render_template('shop_goods.html', shop_goods=shop_goods)

@app.route('/imagebrowser/')
@app.route('/imagebrowser/<path:path>')
def autoindex(path='.'):
    return files_index.render_autoindex(path)

@app.route('/rankup_calculator/')
def rankup_calculator():
    api_response = requests.get(url=f'http://localhost:5000/api/unit')
    units = []

    if api_response.status_code == 200:
        units = api_response.json()

    return render_template('rankup_calculator.html', units=units)

@app.route('/enemy_monster/<monster_id>')
def enemy_monster(monster_id):
    api_response = requests.get(url=f'http://localhost:5000/api/enemy_monster/{monster_id}')
    enemy_monster_data = []
    stages: list = util.get_redis_asset('stage_monster_lookup_parsed_asset').get(monster_id)

    if api_response.status_code == 200:
        enemy_monster_data = api_response.json()

    return render_template('enemy_monster.html', enemy_monster=enemy_monster_data[0], stages=stages)

@app.route('/stage/<stage_id>')
def stage(stage_id):
    api_response = requests.get(url=f'http://localhost:5000/api/stage/{stage_id}')
    stage_data = []

    if api_response.status_code == 200:
        stage_data = api_response.json()

    return render_template('stage_detail.html', stage=stage_data[0])

    # 1: Story
    # 2: Event
    # 4: Battle Road
    # 5: Daily
    # 6: All Out Battle
    # 7: Hero Quest
    # 8: Anniversary Battle
    # 9: Bloom Door
    # 10: Large Battle
    # 11: Guild Co-op Battle
    # 12: TnT Board

@app.route('/stage/')
def area():
    stage_structure = util.get_redis_asset('stage_structure_parsed_asset')

    return render_template('stage_list.html', stage_structure=stage_structure)

@app.route('/battleroad/')
def battleroad():
    api_response = requests.get(url=f'http://localhost:5000/api/area')
    area_data = []
    battleroads = []

    if api_response.status_code == 200:
        area_data = api_response.json()

    for area in area_data:
        if area.get('area_category') == 4:
            battleroads.append(area)

    return render_template('battleroad.html', battleroads=battleroads)

@app.route('/farmable/')
def farmable():
    api_response = requests.get(url=f'http://localhost:5000/api/farmable')
    farmable_data = []

    if api_response.status_code == 200:
        farmable_data = api_response.json()

    return render_template('farmable.html', farmables=farmable_data)

if __name__ == '__main__':
    app.run(debug=True)
