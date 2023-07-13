from flask import Flask
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
from app.util import Util

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='DQT API')
ns = api.namespace('assets', description='')
util = Util()

asset_model = api.model('asset', {
    'display_name': fields.String(),
    'item_key': fields.String(),
})

@ns.route('/')
class Asset(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.marshal_with(asset_model)
    def get(self):
        '''Fetch a given resource'''
        assets = util.get_asset_list('Stage')
        asset_list = []

        for path in assets:
            asset = util.get_asset_by_path(path)
            asset_list.append({
                'display_name': asset.get('display_name'),
                'item_key': asset.get('path')
            })
        
        return sorted(asset_list, key=lambda d: d['display_name']) 





if __name__ == '__main__':
    app.run(debug=True)