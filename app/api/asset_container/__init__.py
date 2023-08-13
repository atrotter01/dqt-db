from flask_restx import Namespace, Resource, fields
from app.util import Util

api = Namespace("asset_container", description="")

asset_model = api.model('asset_container', {
    'asset_containers': fields.Raw
})

util = Util()

@api.route("/")
class AssetContainer(Resource):
    @api.marshal_with(asset_model)
    def get(self):
        containers: list = util.get_assets_by_container()

        return {
            'asset_containers': containers
        }
