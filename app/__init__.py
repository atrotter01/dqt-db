import json
import requests
from flask import Flask, Blueprint, render_template, Response
from flask_restx import Api
from flask_autoindex import AutoIndex
from werkzeug.middleware.proxy_fix import ProxyFix
from app.api.asset import api as asset_api
from app.api.asset_list import api as asset_list_api
from app.api.asset_type import api as asset_type_api

app = Flask(__name__, static_folder='../static', template_folder='../templates')
app.wsgi_app = ProxyFix(app.wsgi_app)

blueprint: Blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(
    blueprint,
    version='1.0',
    title='DQT API'
)
api.add_namespace(asset_api)
api.add_namespace(asset_list_api)
api.add_namespace(asset_type_api)

app.register_blueprint(blueprint=blueprint)

files_index = AutoIndex(app, browse_root='static/images', add_url_rules=False)

@app.route('/')
def index():
    api_response = requests.get(url='http://localhost:5000/api/asset_type')
    asset_types = {}

    if api_response.status_code == 200:
        asset_types = api_response.json().get('asset_type')

    return render_template('index.html', asset_types=asset_types)

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

if __name__ == '__main__':
    app.run(debug=True)
