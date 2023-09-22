import datetime
import json
import requests
from flask import Flask, Blueprint, render_template, request, Response, session
from flask_restx import Api
from flask_autoindex import AutoIndex
from werkzeug.middleware.proxy_fix import ProxyFix
#from werkzeug.middleware.profiler import ProfilerMiddleware
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
app.secret_key = 'REo!NtU6Wr2g#nPpGll116@uXuEqTBJHyOqVG$Stfv8Wo^cJbBiqsNsQwyEG&wEfI6tb6ZXbQdhn2*eBtEwa-bcwY3ot2vQJfldR8wL=v3iJx=9rsGzbUIJr3q!rnmONavS'
app.wsgi_app = ProxyFix(app.wsgi_app)
#app.wsgi_app = ProfilerMiddleware(app.wsgi_app)

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

@app.before_request
def check_session_vars():
    if request.args.get('lang') is not None:
        session['lang'] = request.args.get('lang')

    if session.get('lang') is None:
        session['lang'] = 'en'

@app.route('/')
def index_route():
    return render_template('index.html')

@app.route('/unit/')
def unit_route():
    api_response = requests.get(url='http://localhost:5000/api/unit/', timeout=300, params=dict(lang=session['lang']))
    units = []

    if api_response.status_code == 200:
        units = api_response.json()

    return render_template('unit_list.html', units=units)

@app.route('/skill/active_skill/')
def active_skill_route():
    active_skill_api_response = requests.get(url='http://localhost:5000/api/skill/active_skill', timeout=300, params=dict(lang=session['lang']))
    active_skills = []

    if active_skill_api_response.status_code == 200:
        active_skills = active_skill_api_response.json()

    return render_template('active_skill.html', active_skills=active_skills)

@app.route('/skill/enemy_skill/')
def enemy_skill_route():
    enemy_skill_api_response = requests.get(url='http://localhost:5000/api/skill/enemy_skill', timeout=300, params=dict(lang=session['lang']))
    enemy_skills = []

    if enemy_skill_api_response.status_code == 200:
        enemy_skills = enemy_skill_api_response.json()

    return render_template('enemy_skill.html', enemy_skills=enemy_skills)

@app.route('/skill/passive_skill/')
def passive_skill_route():
    passive_skill_api_response = requests.get(url='http://localhost:5000/api/skill/passive_skill', timeout=300, params=dict(lang=session['lang']))
    passive_skills = []

    if passive_skill_api_response.status_code == 200:
        passive_skills = passive_skill_api_response.json()

    return render_template('passive_skill.html', passive_skills=passive_skills)

@app.route('/skill/reaction_skill/')
def reaction_skill_route():
    reaction_skill_api_response = requests.get(url='http://localhost:5000/api/skill/reaction_skill', timeout=300, params=dict(lang=session['lang']))
    reaction_skills = []

    if reaction_skill_api_response.status_code == 200:
        reaction_skills = reaction_skill_api_response.json()

    return render_template('reaction_skill.html', reaction_skills=reaction_skills)

@app.route('/skill/<type_of_skill>/<skill_id>')
def skill_detail_route(type_of_skill, skill_id):
    util: Util = Util(lang=session['lang'])
    api_response = requests.get(url=f'http://localhost:5000/api/skill/{type_of_skill}/{skill_id}', timeout=300, params=dict(lang=session['lang']))
    skill_data = []
    skill_learned_by = []
    skill_equipment_cache = []

    if util.get_redis_asset(f'{util.get_language_setting()}_skill_equipment_parsed_asset').get(skill_id) is not None:
        skill_equipment_cache = util.get_redis_asset(f'{util.get_language_setting()}_skill_equipment_parsed_asset').get(skill_id)

    if util.get_redis_asset(f'{util.get_language_setting()}_skill_unit_table_parsed_asset').get(skill_id) is not None:
        skill_learned_by.extend(util.get_redis_asset(f'{util.get_language_setting()}_skill_unit_table_parsed_asset').get(skill_id))

    if api_response.status_code == 200:
        skill_data = api_response.json()

    return render_template('skill_detail.html', skill=skill_data[0], skill_learned_by=skill_learned_by, skill_equipment_cache=skill_equipment_cache)

@app.route('/item/')
def item_route():
    consumable_items = []

    item_api_response = requests.get(url='http://localhost:5000/api/item/consumableitem', timeout=300, params=dict(lang=session['lang']))
    if item_api_response.status_code == 200:
        consumable_items = item_api_response.json()

    return render_template('item.html', items=consumable_items)

@app.route('/item/<consumable_item_id>')
def item_detail_route(consumable_item_id):
    util: Util = Util(lang=session['lang'])
    api_response = requests.get(url=f'http://localhost:5000/api/item/consumableitem/{consumable_item_id}', timeout=300, params=dict(lang=session['lang']))
    item_data = []
    location_table = []

    if api_response.status_code == 200:
        item_data = api_response.json()

    if util.get_redis_asset(f'{util.get_language_setting()}_item_location_parsed_asset').get(consumable_item_id) is not None:
        location_table = util.get_redis_asset(f'{util.get_language_setting()}_item_location_parsed_asset').get(consumable_item_id)

    return render_template('item_detail.html', item=item_data[0], location_table=location_table)

@app.route('/icon/')
def icon_route():
    profile_icons = []

    profile_icon_api_response = requests.get(url='http://localhost:5000/api/item/profileicon', timeout=300, params=dict(lang=session['lang']))
    if profile_icon_api_response.status_code == 200:
        profile_icons = profile_icon_api_response.json()

    return render_template('icon.html', icons=profile_icons)

@app.route('/icon/<profile_icon_id>')
def icon_detail_route(profile_icon_id):
    util: Util = Util(lang=session['lang'])
    api_response = requests.get(url=f'http://localhost:5000/api/item/profileicon/{profile_icon_id}', timeout=300, params=dict(lang=session['lang']))
    icon_data = []
    location_table = []

    if api_response.status_code == 200:
        icon_data = api_response.json()

    if util.get_redis_asset(f'{util.get_language_setting()}_item_location_parsed_asset').get(profile_icon_id) is not None:
        location_table = util.get_redis_asset(f'{util.get_language_setting()}_item_location_parsed_asset').get(profile_icon_id)

    return render_template('icon_detail.html', icon=icon_data[0], location_table=location_table)

@app.route('/package/')
def package_route():
    packages = []

    package_api_response = requests.get(url='http://localhost:5000/api/item/package', timeout=300, params=dict(lang=session['lang']))
    if package_api_response.status_code == 200:
        packages = package_api_response.json()

    return render_template('package.html', packages=packages)

@app.route('/unit/<unit_id>')
def unit_detail_route(unit_id):
    api_response = requests.get(url=f'http://localhost:5000/api/unit/{unit_id}', timeout=300, params=dict(lang=session['lang']))
    farmable_api_response = requests.get(url='http://localhost:5000/api/farmable/', timeout=300, params=dict(lang=session['lang']))
    area_api_response = requests.get(url='http://localhost:5000/api/area', timeout=300, params=dict(lang=session['lang']))

    unit = []
    farmables = []
    area_data = []
    battleroads = []

    if api_response.status_code == 200:
        unit = api_response.json()

    if farmable_api_response.status_code == 200:
        farmables = farmable_api_response.json()

    if area_api_response.status_code == 200:
        area_data = area_api_response.json()

    for area in area_data:
        if area.get('area_category') == 4:
            for monster in area.get('area_available_monsters'):
                if monster.get('monster_path') == unit_id:
                    battleroads.append(area)
                    break

    return render_template('unit_detail.html', unit=unit[0], farmables=farmables, battleroads=battleroads)

@app.route('/equipment/')
def equipment_route():
    api_response = requests.get(url='http://localhost:5000/api/equipment', timeout=300, params=dict(lang=session['lang']))
    equipments = []

    if api_response.status_code == 200:
        equipments = api_response.json()

    return render_template('equipment_list.html', equipments=equipments)

@app.route('/equipment/<equipment_id>')
def equipment_detail_route(equipment_id):
    util: Util = Util(lang=session['lang'])
    api_response = requests.get(url=f'http://localhost:5000/api/equipment/{equipment_id}', timeout=300, params=dict(lang=session['lang']))
    equipment_data = []
    location_table = []

    if api_response.status_code == 200:
        equipment_data = api_response.json()

    if util.get_redis_asset(f'{util.get_language_setting()}_item_location_parsed_asset').get(equipment_id) is not None:
        location_table = util.get_redis_asset(f'{util.get_language_setting()}_item_location_parsed_asset').get(equipment_id)

    return render_template('equipment_detail.html', equipment=equipment_data[0], location_table=location_table)

@app.route('/accolade/')
def accolade_route():
    api_response = requests.get(url='http://localhost:5000/api/accolade/', timeout=300, params=dict(lang=session['lang']))
    accolades = []

    if api_response.status_code == 200:
        accolades = api_response.json()

    return render_template('accolade.html', accolades=accolades)

@app.route('/asset_container/')
def asset_container_route():
    api_response = requests.get(url='http://localhost:5000/api/asset_container', timeout=300, params=dict(lang=session['lang']))
    asset_container_response: dict = {}
    asset_containers: list = []

    if api_response.status_code == 200:
        asset_container_response = api_response.json().get('asset_containers')

    for container in asset_container_response:
        if container.startswith('/mnt/'):
            continue

        asset_containers.append(container)

    return render_template('asset_container.html', asset_containers=asset_containers)

@app.route('/asset_container/<container_id>')
def asset_type_route(container_id):
    api_response = requests.get(url='http://localhost:5000/api/asset_container', timeout=300, params=dict(lang=session['lang']))
    asset_container_response: dict = {}
    asset_types: list = []

    if api_response.status_code == 200:
        asset_container_response = api_response.json().get('asset_containers')

    for asset_container in asset_container_response.keys():
        if asset_container.replace('/', '___') != container_id:
            continue

        for asset_type in asset_container_response.get(asset_container):
            asset_types.append({ 'container': container_id, 'asset_type': asset_type })

    return render_template('asset_type.html', asset_types=asset_types)

@app.route('/asset_container/<container>/<container_asset_type>')
def asset_list_route(container, container_asset_type):
    api_response = requests.get(url='http://localhost:5000/api/asset_container', timeout=300, params=dict(lang=session['lang']))
    asset_container_response: dict = {}
    container_key: str = container.replace('___', '/')
    assets: list = []

    if api_response.status_code == 200:
        asset_container_response = api_response.json().get('asset_containers')
        assets.extend(asset_container_response.get(container_key).get(container_asset_type))

    return render_template('asset_list.html', assets=assets)

@app.route('/asset/<path_id>')
def asset_route(path_id):
    api_response = requests.get(url=f'http://localhost:5000/api/asset/{path_id}', timeout=300, params=dict(lang=session['lang']))
    asset = {}

    if api_response.status_code == 200:
        asset = api_response.json()[0]

    return Response(json.dumps(asset, indent=2), mimetype='text/plain')

@app.route('/shop/')
def shop_route():
    api_response = requests.get(url='http://localhost:5000/api/shop', timeout=300, params=dict(lang=session['lang']))
    shops = []

    if api_response.status_code == 200:
        shops = api_response.json()

    return render_template('shop.html', shops=shops)

@app.route('/shop/<shop_id>')
def shop_goods_route(shop_id):
    api_response = requests.get(url=f'http://localhost:5000/api/shop/{shop_id}', timeout=300, params=dict(lang=session['lang']))
    shop_goods = []

    if api_response.status_code == 200:
        shop_goods = api_response.json()

    return render_template('shop_goods.html', shop_goods=shop_goods)

@app.route('/imagebrowser/')
@app.route('/imagebrowser/<path:path>')
def autoindex(path='.'):
    return files_index.render_autoindex(path)

@app.route('/rankup_calculator/')
def rankup_calculator_route():
    api_response = requests.get(url='http://localhost:5000/api/unit', timeout=300, params=dict(lang=session['lang']))
    units = []

    if api_response.status_code == 200:
        units = api_response.json()

    return render_template('rankup_calculator.html', units=units)

@app.route('/enemy_monster/<monster_id>')
def enemy_monster_route(monster_id):
    util: Util = Util(lang=session['lang'])
    api_response = requests.get(url=f'http://localhost:5000/api/enemy_monster/{monster_id}', timeout=300, params=dict(lang=session['lang']))
    enemy_monster_data = []
    stages: list = util.get_redis_asset(f'{util.get_language_setting()}_stage_monster_lookup_parsed_asset').get(monster_id)

    if api_response.status_code == 200:
        enemy_monster_data = api_response.json()

    return render_template('enemy_monster.html', enemy_monster=enemy_monster_data[0], stages=stages)

@app.route('/stage/<stage_id>')
def stage_route(stage_id):
    api_response = requests.get(url=f'http://localhost:5000/api/stage/{stage_id}', timeout=300, params=dict(lang=session['lang']))
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

@app.route('/stage/category/<stage_category>')
def stage_category_route(stage_category):
    util: Util = Util(lang=session['lang'])
    stage_structure = util.get_redis_asset(f'{util.get_language_setting()}_stage_structure_parsed_asset')

    return render_template('stage_list.html', stage_structure=stage_structure, stage_category=int(stage_category))

@app.route('/battleroad/')
def battleroad_route():
    api_response = requests.get(url='http://localhost:5000/api/area', timeout=300, params=dict(lang=session['lang']))
    area_data = []
    battleroads = []

    if api_response.status_code == 200:
        area_data = api_response.json()

    for area in area_data:
        if area.get('area_category') == 4:
            battleroads.append(area)

    return render_template('battleroad.html', battleroads=battleroads)

@app.route('/farmable/')
def farmable_route():
    api_response = requests.get(url='http://localhost:5000/api/farmable', timeout=300, params=dict(lang=session['lang']))
    farmable_data = []

    if api_response.status_code == 200:
        farmable_data = api_response.json()

    return render_template('farmable.html', farmables=farmable_data)

@app.route('/lawson/')
def lawson_route():
    util: Util = Util(lang=session['lang'])
    condolences = util.get_redis_asset('user_data_lawson')

    if condolences is None:
        condolences = []

    return render_template('lawson.html', condolences=condolences)

@app.route('/lawson/save', methods=['POST'])
def lawson_save_route():
    util: Util = Util(lang=session['lang'])
    user = request.form.get('name')
    message = request.form.get('message')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    condolences = util.get_redis_asset('user_data_lawson')

    if condolences is None:
        condolences = []

    if user == '':
        return render_template('lawson.html', condolences=condolences)

    if message == '':
        return render_template('lawson.html', condolences=condolences)

    condolences.append({
        'user': user,
        'message': message,
        'timestamp': timestamp,
    })

    util.save_redis_asset(cache_key='user_data_lawson', data=condolences)

    return render_template('lawson.html', condolences=condolences)

@app.route('/translate')
def translate_route():
    util: Util = Util(lang=session['lang'])
    untranslated_asset_list = util.get_redis_asset('sys_untranslated_strings')
    untranslated_assets: list = []
    seen_assets: list = []

    for asset_key in untranslated_asset_list:
        key: str = untranslated_asset_list.get(asset_key).get('key')
        path: str = untranslated_asset_list.get(asset_key).get('path')
        asset_id: str = untranslated_asset_list.get(asset_key).get('asset_id')

        if asset_id in seen_assets:
            continue

        seen_assets.append(asset_id)
        asset: dict = util.get_asset_by_path(asset_id, deflate_data=True)
        data: dict = asset.get('processed_document')
        filetype: str = asset.get('filetype')
        string = data.get(key).get('ja')

        untranslated_assets.append({
            'key': key,
            'path': path,
            'filetype': filetype,
            'asset_id': asset_id,
            'string': string
        })

    return render_template('translate.html', untranslated_assets=untranslated_assets)

if __name__ == '__main__':
    app.run(debug=True)
