from flask import request
from flask_restx import Namespace, Resource, fields
from app.util import Util

api = Namespace("asset", description="")

asset_model = api.model('asset', {
    'display_name': fields.String(),
    'data': fields.Raw(),
})

@api.route("/<path>")
@api.param("path", "Asset ID")
class Asset(Resource):

    util: Util

    @api.marshal_with(asset_model)
    def get(self, path):
        '''Fetch a given Asset'''
        self.util = Util(lang=request.args.get('lang'))
        asset_list = []
        asset = self.util.get_asset_by_path(path=path, deflate_data=True)

        display_name: str = asset.get('display_name')
        document: dict = asset.get('processed_document')

        if document is None:
            document = asset.get('document')

        asset_list.append({
            'display_name': display_name,
            'data': document,
        })

        return sorted(asset_list, key=lambda d: d['display_name'])
