import json
import requests
from flask import Flask, Blueprint, render_template, Response
from flask_restx import Api
from flask_autoindex import AutoIndex
from werkzeug.middleware.proxy_fix import ProxyFix
from app.api.asset import api as asset_api
from app.api.asset_list import api as asset_list_api
from app.api.asset_type import api as asset_type_api
from app.api.item import api as item_api
from app.api.skill import api as skill_api
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

api.add_namespace(asset_api)
api.add_namespace(asset_list_api)
api.add_namespace(asset_type_api)
api.add_namespace(item_api)
api.add_namespace(skill_api)
api.add_namespace(unit_api)

app.register_blueprint(blueprint=blueprint)

files_index = AutoIndex(app, browse_root='static/dqt_images', add_url_rules=False)
util: Util = Util()

@app.route('/')
def index():
    events: list = []

    if util.redis_client.get('event_portal_cache'):
        events = util.get_asset_by_path('event_portal_cache', deflate_data=False)
    else:
        asset_list: list = util.get_asset_list('EventPortal')

        for path in asset_list:
            asset = util.get_asset_by_path(path, deflate_data=True)
            banner_path: str = asset.get('document').get('bannerPath')
            image_path: str = util.get_image_path(banner_path, lang='en')
            display_name: str = asset.get('display_name')
            events.append({'display_name': display_name, 'banner_path': image_path})

        util.redis_client.set('event_portal_cache', json.dumps(events))

    return render_template('index.html', events=sorted(events, key=lambda d: d['display_name']))

@app.route('/unit')
def unit():
    api_response = requests.get(url='http://localhost:5000/api/unit/')
    units = []

    if api_response.status_code == 200:
        units = api_response.json()

    return render_template('unit_list.html', units=units)

@app.route('/skill')
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

@app.route('/item')
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

@app.route('/asset_type')
def asset_type():
    api_response = requests.get(url='http://localhost:5000/api/asset_type')
    asset_types = {}

    if api_response.status_code == 200:
        asset_types = api_response.json().get('asset_type')

    return render_template('asset_type.html', asset_types=asset_types)

@app.route('/asset_list/<asset_type>')
def asset_list(asset_type):
    api_response = requests.get(url=f'http://localhost:5000/api/asset_list/{asset_type}')
    assets = []

    if api_response.status_code == 200:
        assets = api_response.json()

    sorted_assets = list = []
    
    try:
        sorted_assets = sorted(assets, key=lambda d: d['display_name'])
    except TypeError:
        sorted_assets = assets

    return render_template('asset_list.html', assets=sorted_assets)

@app.route('/asset/<path_id>')
def asset(path_id):
    api_response = requests.get(url=f'http://localhost:5000/api/asset/{path_id}')
    asset = {}

    if api_response.status_code == 200:
        asset = api_response.json()[0]

    return Response(json.dumps(asset, indent=2), mimetype='text/json')

@app.route('/imagebrowser')
@app.route('/imagebrowser/')
@app.route('/imagebrowser/<path:path>')
def autoindex(path='.'):
    return files_index.render_autoindex(path)

@app.route('/rankup_calculator')
def rankup_calculator():
    api_response = requests.get(url=f'http://localhost:5000/api/unit')
    units = []

    if api_response.status_code == 200:
        units = api_response.json()

    return render_template('rankup_calculator.html', units=units)

if __name__ == '__main__':
    app.run(debug=True)
