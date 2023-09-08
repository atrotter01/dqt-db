from flask import request
from flask_restx import Namespace, Resource, fields
from app.util import Util

api = Namespace("asset_container", description="")

asset_model = api.model('asset_container', {
    'asset_containers': fields.Raw
})

@api.route("/")
class AssetContainer(Resource):
    util: Util

    @api.marshal_with(asset_model)
    def get(self):
        self.util = Util(lang=request.args.get('lang'))
        containers: list = self.util.get_assets_by_container()

        return {
            'asset_containers': containers
        }
