from flask_restx import Namespace, Resource, fields
from app.util import Util

api = Namespace("asset_type", description="")

asset_model = api.model('asset_type', {
    'asset_type': fields.List(fields.String)
})

util = Util()

@api.route("/")
class AssetType(Resource):
    @api.marshal_with(asset_model)
    def get(self):
        asset_type_list = util.get_asset_by_path(path='asset_types', deflate_data=False)

        return {
            'asset_type': sorted(asset_type_list)
        }
