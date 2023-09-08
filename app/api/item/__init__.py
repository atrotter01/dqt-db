from flask import request
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

profile_icon_model = api.model('profile_icon', {
    'id': fields.String,
    'display_name': fields.String,
    'short_display_name': fields.String,
    'icon_path': fields.String
})

package_model = api.model('package', {
    'id': fields.String,
    'display_name': fields.String,
    'icon_path': fields.String
})

@api.param("path", "Path")
@api.route("/consumableitem/")
@api.route("/consumableitem/<path>")
class ConsumableItem(Resource):

    util: Util
    items: list
    cache_key: str

    @api.marshal_list_with(item_model)
    def get(self, path = None):
        '''Fetch a given Item'''
        self.util = Util(lang=request.args.get('lang'))
        self.items = []

        if path is not None:
            asset = self.util.get_asset_by_path(path)
            processed_document = asset.get('processed_document')

            display_name: str = None
            description: str = None

            if processed_document.get('displayName_translation') is not None:
                display_name = self.util.get_localized_string(data=processed_document, key='displayName_translation', path=path)
            else:
                display_name = processed_document.get('displayName')

            if processed_document.get('description_translation') is not None:
                description = self.util.get_localized_string(data=processed_document, key='description', path=path)
            else:
                description = processed_document.get('description')

            item = {
                'id': path,
                'display_name': display_name,
                'description': description,
                'rank_icon_path': self.util.get_image_path(processed_document.get('consumableItemRank').get('iconPath')),
                'icon_path': self.util.get_image_path(processed_document.get('iconPath')),
                'possession_limit': processed_document.get('possessionLimit')
            }

            self.items.append(item)

            return self.items

        self.cache_key = f'{self.util.get_language_setting()}_consumable_item_parsed_asset'
        cached_asset = self.util.get_redis_asset(cache_key=self.cache_key)

        if cached_asset is not None:
            return cached_asset

        asset_list: list = []
        asset_list.extend(self.util.get_asset_list('ConsumableItem'))
        asset_list.extend(self.util.get_asset_list('GeneralAlchemyMaterial'))

        for path in asset_list:
            asset = self.util.get_asset_by_path(path)
            processed_document = asset.get('processed_document')

            display_name: str = None
            description: str = None

            if processed_document.get('displayName_translation') is not None:
                display_name = self.util.get_localized_string(data=processed_document, key='displayName_translation', path=path)
            else:
                display_name = processed_document.get('displayName')

            if processed_document.get('description_translation') is not None:
                description = self.util.get_localized_string(data=processed_document, key='description_translation', path=path)
            else:
                description = processed_document.get('description')

            item = {
                'id': path,
                'display_name': display_name,
                'description': description,
                'rank_icon_path': self.util.get_image_path(processed_document.get('consumableItemRank').get('iconPath')),
                'icon_path': self.util.get_image_path(processed_document.get('iconPath')),
                'possession_limit': processed_document.get('possessionLimit')
            }

            self.items.append(item)

        self.util.save_redis_asset(cache_key=self.cache_key, data=sorted(self.items, key=lambda d: d['display_name']))

        return sorted(self.items, key=lambda d: d['display_name'])

@api.param("path", "Path")
@api.route("/profileicon/")
@api.route("/profileicon/<path>")
class ProfileIcon(Resource):

    util: Util
    profile_icons: list
    cache_key: str

    @api.marshal_list_with(profile_icon_model)
    def get(self, path = None):
        '''Fetch a given Profile Icon'''
        self.util = Util(lang=request.args.get('lang'))
        self.profile_icons = []

        if path is not None:
            asset = self.util.get_asset_by_path(path)
            processed_document = asset.get('processed_document')

            display_name: str = None
            short_display_name: str = None

            if processed_document.get('displayName_translation') is not None:
                display_name = self.util.get_localized_string(data=processed_document, key='displayName_translation', path=path)
            else:
                display_name = processed_document.get('displayName')

            if processed_document.get('shortDisplayName_translation') is not None:
                short_display_name = self.util.get_localized_string(data=processed_document, key='shortDisplayName_translation', path=path)
            else:
                short_display_name = processed_document.get('shortDisplayName')

            profile_icon = {
                'id': path,
                'display_name': display_name,
                'short_display_name': short_display_name,
                'icon_path': self.util.get_image_path(processed_document.get('iconPath'))
            }

            self.profile_icons.append(profile_icon)

            return self.profile_icons

        self.cache_key = f'{self.util.get_language_setting()}_profile_icon_parsed_asset'
        cached_asset = self.util.get_redis_asset(cache_key=self.cache_key)

        if cached_asset is not None:
            return cached_asset

        asset_list: list = self.util.get_asset_list('ProfileIcon')

        for path in asset_list:
            asset = self.util.get_asset_by_path(path)
            processed_document = asset.get('processed_document')

            display_name: str = None
            short_display_name: str = None

            if processed_document.get('displayName_translation') is not None:
                display_name = self.util.get_localized_string(data=processed_document, key='displayName_translation', path=path)
            else:
                display_name = processed_document.get('displayName')

            if processed_document.get('shortDisplayName_translation') is not None:
                short_display_name = self.util.get_localized_string(data=processed_document, key='shortDisplayName_translation', path=path)
            else:
                short_display_name = processed_document.get('shortDisplayName')

            profile_icon = {
                'id': path,
                'display_name': display_name,
                'short_display_name': short_display_name,
                'icon_path': self.util.get_image_path(processed_document.get('iconPath'))
            }

            self.profile_icons.append(profile_icon)

        self.util.save_redis_asset(cache_key=self.cache_key, data=sorted(self.profile_icons, key=lambda d: d['display_name']))

        return sorted(self.profile_icons, key=lambda d: d['display_name'])

@api.param("path", "Path")
@api.route("/package/")
@api.route("/package/<path>")
class Package(Resource):

    util: Util
    packages: list
    cache_key: str

    @api.marshal_list_with(package_model)
    def get(self, path = None):
        '''Fetch a given Profile Icon'''
        self.util = Util(lang=request.args.get('lang'))
        self.packages = []

        if path is not None:
            asset = self.util.get_asset_by_path(path)
            processed_document = asset.get('processed_document')

            display_name: str = None

            if processed_document.get('displayName_translation') is not None:
                display_name = self.util.get_localized_string(data=processed_document, key='displayName_translation', path=path)
            else:
                display_name = processed_document.get('displayName')

            icon_path = self.util.get_image_path(processed_document.get('iconPath'))

            if icon_path is None:
                if processed_document.get('consumableItems') is not None:
                    icon_path = self.util.get_image_path(processed_document.get('consumableItems')[0].get('drop').get('iconPath'))

            package = {
                'id': path,
                'display_name': display_name,
                'icon_path': icon_path
            }

            self.packages.append(package)

            return self.packages

        self.cache_key = f'{self.util.get_language_setting()}_package_parsed_asset'
        cached_asset = self.util.get_redis_asset(cache_key=self.cache_key)

        if cached_asset is not None:
            return cached_asset

        asset_list: list = self.util.get_asset_list('Package')

        for path in asset_list:
            asset = self.util.get_asset_by_path(path)
            processed_document = asset.get('processed_document')

            display_name: str = None

            if processed_document.get('displayName_translation') is not None:
                display_name = self.util.get_localized_string(data=processed_document, key='displayName_translation', path=path)
            else:
                display_name = processed_document.get('displayName')

            icon_path = self.util.get_image_path(processed_document.get('iconPath'))

            if icon_path is None:
                if processed_document.get('consumableItems') is not None:
                    icon_path = self.util.get_image_path(processed_document.get('consumableItems')[0].get('drop').get('iconPath'))

            package = {
                'id': path,
                'display_name': display_name,
                'icon_path': icon_path
            }

            self.packages.append(package)

        self.util.save_redis_asset(cache_key=self.cache_key, data=sorted(self.packages, key=lambda d: d['display_name']))

        return sorted(self.packages, key=lambda d: d['display_name'])
