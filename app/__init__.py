from flask import Flask, Blueprint
from flask_restx import Api
from flask_autoindex import AutoIndex
from werkzeug.middleware.proxy_fix import ProxyFix
from app.api.asset import api as asset_api
from app.api.asset_list import api as asset_list_api
from app.api.asset_type import api as asset_type_api
from app.util import Util

app = Flask(__name__, static_folder='static', template_folder='templates')
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

@app.route('/imagebrowser')
@app.route('/imagebrowser/')
@app.route('/imagebrowser/<path:path>')
def autoindex(path='.'):
    return files_index.render_autoindex(path)

if __name__ == '__main__':
    util = Util()
    util.cache_api_tables()

    app.run(debug=True)