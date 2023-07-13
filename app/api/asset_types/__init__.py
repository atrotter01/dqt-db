from flask_restx import Namespace, Resource, fields
from app.util import Util

api = Namespace("Asset Type", description="")

asset_model = api.model('asset_type', {
    'asset_type': fields.List()
})

util = Util()

@api.route("/")
class AssetType(Resource):
    @api.marshal_with(asset_model)
    def get(self, id):
        asset_type_list = util.get_asset_by_path('asset_types')

        return sorted(asset_type_list)