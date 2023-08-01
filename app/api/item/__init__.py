from flask_restx import Namespace, Resource, fields
from app.util import Util

api = Namespace("item", description="")

item_model = api.model('item', {
    'id': fields.String,
    'display_name': fields.String,
    'description': fields.String,
    'rank_icon_path': fields.String,
    'icon_path': fields.String,
    'possession_limit': fields.Integer
})

@api.param("path", "Path")
@api.route("/")
@api.route("/<path>")
class Asset(Resource):

    util: Util
    items: list

    @api.marshal_list_with(item_model)
    def get(self, path = None):
        '''Fetch a given Item'''
        self.util = Util()
        self.items = []

        if path is not None:
            asset = self.util.get_asset_by_path(path)
            processed_document = asset.get('processed_document')

            item = {
                'id': path,
                'display_name': processed_document.get('displayName'),
                'description': processed_document.get('description'),
                'rank_icon_path': self.util.get_image_path(processed_document.get('consumableItemRank').get('iconPath')),
                'icon_path': self.util.get_image_path(processed_document.get('iconPath')),
                'posession_limit': processed_document.get('possessionLimit')
            }

            self.items.append(item)

            return self.items

        asset_list: list = self.util.get_asset_list('ConsumableItem')

        for path in asset_list:
            asset = self.util.get_asset_by_path(path)
            processed_document = asset.get('processed_document')

            item = {
                'id': path,
                'display_name': processed_document.get('displayName'),
                'description': processed_document.get('description'),
                'rank_icon_path': self.util.get_image_path(processed_document.get('consumableItemRank').get('iconPath')),
                'icon_path': self.util.get_image_path(processed_document.get('iconPath')),
                'possession_limit': processed_document.get('possessionLimit')
            }

            self.items.append(item)

        return sorted(self.items, key=lambda d: d['display_name'])
