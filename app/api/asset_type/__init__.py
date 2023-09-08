from flask import request
from flask_restx import Namespace, Resource, fields
from app.util import Util

api = Namespace("asset_type", description="")

asset_model = api.model('asset_type', {
    'asset_type': fields.List(fields.String)
})

@api.route("/")
class AssetType(Resource):
    util: Util

    @api.marshal_with(asset_model)
    def get(self):
        self.util = Util(lang=request.args.get('lang'))
        asset_type_list = self.util.get_asset_by_path(path='asset_types', deflate_data=False)

        return {
            'asset_type': sorted(asset_type_list)
        }
