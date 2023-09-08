from flask import request
from flask_restx import Namespace, Resource, fields
from app.util import Util

api = Namespace("asset_list", description="")

asset_model = api.model('asset_list', {
    'id': fields.String(),
    'display_name': fields.String()
})

@api.route("/<asset_type>")
@api.param("asset_type", "Asset Type")
class Asset(Resource):
    util: Util

    @api.marshal_with(asset_model)
    def get(self, asset_type):
        '''Fetch a list of assets of a given type'''
        self.util = Util(lang=request.args.get('lang'))
        asset_list = []
        asset_map: dict = self.util.get_asset_by_path(path='asset_path_map', deflate_data=False).get(asset_type).get('assets')

        for asset in asset_map:
            asset_list.append({
                'id': asset.get('path'),
                'display_name': asset.get('display_name')
            })

        return asset_list
        #return sorted(asset_list, key=lambda d: d['display_name'])
