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
        self.util = Util()
        self.accolades = []

        asset_list: list = self.util.get_asset_list('HonoraryTitle')

        for path in asset_list:
            asset = self.util.get_asset_by_path(path, deflate_data=True)
            document = asset.get('processed_document')
            banner_path: str = self.util.get_image_path(document.get('bannerIconPath'), lang='en')
            display_name: str = document.get('displayName_translation').get('gbl') or document.get('displayName_translation').get('ja')
            content: str = document.get('content_translation').get('gbl') or document.get('content_translation').get('ja')
            self.accolades.append(
                {
                    'display_name': display_name,
                    'banner_path': banner_path,
                    'content': content
                }
            )

        return sorted(self.accolades, key=lambda d: d['display_name'])
