from flask import request
from flask_restx import Namespace, Resource, fields
from app.util import Util

api = Namespace("accolade", description="")

accolade_model = api.model('accolade', {
    'id': fields.String,
    'display_name': fields.String,
    'banner_path': fields.String,
    'content': fields.String
})

@api.param("path", "Path")
@api.route("/")
@api.route("/<path>")
class Asset(Resource):

    util: Util
    accolades: list

    @api.marshal_list_with(accolade_model)
    def get(self, path = None):
        '''Fetch a given Accolade'''
        self.util = Util(lang=request.args.get('lang'))
        self.accolades = []

        asset_list: list = self.util.get_asset_list('HonoraryTitle')

        for path in asset_list:
            asset = self.util.get_asset_by_path(path, deflate_data=True)
            document = asset.get('processed_document')
            banner_path: str = self.util.get_image_path(document.get('bannerIconPath'))
            display_name: str = self.util.get_localized_string(data=document, key='displayName_translation', path=path)
            content: str = self.util.get_localized_string(data=document, key='content_translation', path=path)
            self.accolades.append(
                {
                    'id': path,
                    'display_name': display_name,
                    'banner_path': banner_path,
                    'content': content
                }
            )

        return sorted(self.accolades, key=lambda d: d['display_name'])
