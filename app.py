from flask import Flask, Blueprint
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
from app.api.asset import api as asset_api
from app.api.asset_list import api as asset_list_api
from app.api.asset_type import api as asset_type_api
from app.util import Util

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='DQT API')
api.add_namespace(asset_api)
api.add_namespace(asset_list_api)
api.add_namespace(asset_type_api)

util = Util()

if __name__ == '__main__':
    util.cache_api_tables()

    app.run(debug=True)