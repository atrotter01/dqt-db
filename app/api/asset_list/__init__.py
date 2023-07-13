from flask_restx import Namespace, Resource, fields
from app.util import Util

api = Namespace("asset_list", description="")

asset_model = api.model('asset_list', {
    'id': fields.String(),
    'display_name': fields.String()
})

util = Util()

@api.route("/<asset_type>")
@api.param("asset_type", "Asset Type")
class Asset(Resource):
    @api.marshal_with(asset_model)
    def get(self, asset_type):
        '''Fetch a list of assets of a given type'''
        asset_list = []
        asset_map: dict = util.get_asset_by_path('asset_path_map').get(asset_type).get('assets')

        for asset in asset_map:
            asset_list.append({
                'id': asset.get('path'),
                'display_name': asset.get('display_name')
            })
        
        return asset_list
        #return sorted(asset_list, key=lambda d: d['display_name']) 
