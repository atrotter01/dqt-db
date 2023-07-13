from flask_restx import Namespace, Resource, fields
from app.util import Util

api = Namespace("asset", description="")

asset_model = api.model('asset', {
    'display_name': fields.String(),
    'data': fields.Raw(),
    'expanded_data': fields.Raw()
})

util = Util()

@api.route("/<id>")
@api.param("id", "Asset ID")
class Asset(Resource):
    @api.marshal_with(asset_model)
    def get(self, id):
        '''Fetch a given Asset'''
        asset_list = []

        asset = util.get_asset_by_path(id)
        asset_list.append({
            'display_name': asset.get('display_name'),
            'data': asset.get('document'),
            'expanded_data': asset.get('processed_document')
        })
        
        return sorted(asset_list, key=lambda d: d['display_name']) 
