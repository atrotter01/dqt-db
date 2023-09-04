import requests
from flask_restx import Namespace, Resource, fields
from app.util import Util

api = Namespace("shop", description="")

shop_model = api.model('shop', {
    'id': fields.String,
    'display_name': fields.String,
    'available_in_reminiscene': fields.Boolean,
    'banner_path': fields.String,
    'category_banner_path': fields.String,
    'parent_category_banner_path': fields.String,
    'shop_goods': fields.Raw,
})

shop_goods_model = api.model('shop_goods', {
    'shop_id': fields.String,
    'shop_name': fields.String,
    'list_order': fields.Integer,
    'purchasable_count': fields.Integer,
    'quantity': fields.Integer,
    'goods_path': fields.String,
    'goods_cost': fields.Integer,
    'goods_name': fields.String,
    'goods_image': fields.String,
    'goods_description': fields.String,
    'goods_category': fields.String,
})

@api.route("/")
class Shop(Resource):

    util: Util
    shops: list
    sub_shops: list
    cache_key: str

    @api.marshal_list_with(shop_model)
    def get(self, path = None):
        '''Fetch a given Shop'''
        self.util = Util()
        self.shops = []
        self.sub_shops = {}

        self.cache_key = 'exchange_shop_parsed_asset'
        cached_asset = self.util.get_redis_asset(cache_key=self.cache_key)

        if cached_asset is not None:
            return cached_asset

        sub_shop_asset_list: list = self.util.get_asset_list('ExchangeShopSub')

        for path in sub_shop_asset_list:
            asset = self.util.get_asset_by_path(path)
            document = asset.get('processed_document')
            banner_path = self.util.get_image_path(document.get('bannerPath'))
            parent_banner_path = self.util.get_image_path(document.get('parent').get('bannerPath'))

            for shop in document.get('exchangeShops'):
                shop_id = shop.get('linked_asset_id')

                self.sub_shops.update({
                    shop_id: {
                        'banner_path': banner_path,
                        'parent_banner_path': parent_banner_path
                    }
                })

        asset_list: list = self.util.get_asset_list('ExchangeShop')

        for path in asset_list:
            asset = self.util.get_asset_by_path(path, deflate_data=True)
            document = asset.get('processed_document')

            # Bad Fygg Shop Data
            if 'Megaminokazitu' in asset.get('display_name'):
                continue

            # Dummy Passport Shop
            if not document.get('displayName_translation'):
                continue

            shop_id = document.get('linked_asset_id')
            shop_name = document.get('displayName_translation').get('gbl') or document.get('displayName_translation').get('ja')
            shop_banner = self.util.get_image_path(document.get('bannerPath'))
            category_banner: str = None
            parent_category_banner: str = None
            available_in_reminiscene: bool = False

            if self.sub_shops.get(shop_id) is not None:
                category_banner = self.sub_shops.get(shop_id).get('banner_path')
                parent_category_banner = self.sub_shops.get(shop_id).get('parent_banner_path')

                if parent_category_banner is not None:
                    available_in_reminiscene = True

            shop_goods = requests.get(f'http://localhost:5000/api/shop/{shop_id}', timeout=300).json()

            self.shops.append({
                'id': shop_id,
                'display_name': shop_name,
                'available_in_reminiscene': available_in_reminiscene,
                'banner_path': shop_banner,
                'category_banner_path': category_banner,
                'parent_category_banner_path': parent_category_banner,
                'shop_goods': shop_goods,
            })

        self.util.save_redis_asset(cache_key=self.cache_key, data=sorted(self.shops, key=lambda d: d['display_name']))

        return sorted(self.shops, key=lambda d: d['display_name'])

@api.param("shop_path", "Path")
@api.route("/<shop_path>")
class ShopGoods(Resource):

    util: Util
    goods: list
    cache_key: str

    @api.marshal_list_with(shop_goods_model)
    def get(self, shop_path):
        '''Fetch a given Shop'''
        self.util = Util()
        self.goods = []
        self.cache_key = f'{shop_path}_shop_goods_parsed_asset'
        cached_asset = self.util.get_redis_asset(cache_key=self.cache_key)

        if cached_asset is not None:
            return cached_asset

        asset_list: list = []
        codelist: dict = self.util.get_codelist_path_map()

        shop_asset = self.util.get_asset_by_path(shop_path, deflate_data=True)
        shop_document = shop_asset.get('processed_document')

        if shop_document.get('m_Name') == 'ExchangeShop_Megaminokazitu':
            shop_asset_list = self.util.get_asset_list('ExchangeShop')

            for path in shop_asset_list:
                temp_shop_asset = self.util.get_asset_by_path(path)

                if 'Megaminokazitu' in temp_shop_asset.get('document').get('m_Name') and temp_shop_asset.get('document').get('shop') is not None:
                    asset_list.append(path)

        else:
            asset_list.extend(self.util.get_asset_list('ExchangeShopGoods'))

        for path in asset_list:
            asset = self.util.get_asset_by_path(path)
            document = asset.get('processed_document')

            if document.get('shop').get('linked_asset_id') != shop_path:
                continue

            code: str = str(document.get('goodsCode'))
            list_order: int = document.get('listOrder')
            purchasable_count: int = document.get('purchasableCount')
            quantity: int = document.get('goodsQuantity')
            goods_type = document.get('goodsType')
            goods_cost = document.get('consumptionQuantity')
            goods_name: str = None
            goods_image: str = None
            goods_description: str = None
            goods_category: str = None

            if goods_type == 1:
                goods_path = codelist.get('ConsumableItemMasterDataStoreSource').get(code)[0]
                goods_asset = self.util.get_asset_by_path(goods_path)
                goods_name = goods_asset.get('display_name')
                goods_description = goods_asset.get('processed_document').get('description_translation').get('gbl') or goods_asset.get('processed_document').get('description_translation').get('ja')
                goods_image = self.util.get_image_path(goods_asset.get('processed_document').get('iconPath'))
                goods_category = 'item'

            elif goods_type == 2:
                goods_path = codelist.get('MonsterProfileMasterDataStoreSource').get(code)[0]
                goods_asset = self.util.get_asset_by_path(goods_path)
                goods_name = goods_asset.get('processed_document').get('displayName_translation').get('gbl') or goods_asset.get('processed_document').get('displayName_translation').get('ja')
                goods_description = ''
                goods_image = self.util.get_image_path(goods_asset.get('processed_document').get('iconPath'))
                goods_category = 'monster'

            elif goods_type == 3:
                goods_path = codelist.get('EquipmentMasterDataStoreSource').get(code)[0]
                goods_asset = self.util.get_asset_by_path(goods_path)
                goods_name = goods_asset.get('processed_document').get('profile').get('displayName_translation').get('gbl') or goods_asset.get('processed_document').get('profile').get('displayName_translation').get('ja')
                goods_description = goods_asset.get('processed_document').get('profile').get('description_translation').get('gbl') or goods_asset.get('processed_document').get('profile').get('description_translation').get('ja')
                goods_image = self.util.get_image_path(goods_asset.get('processed_document').get('profile').get('iconPath'))
                goods_category = 'equipment'

            elif goods_type == 6:
                goods_path = codelist.get('PackageMasterDataStoreSource').get(code)[0]
                goods_asset = self.util.get_asset_by_path(goods_path)
                goods_name = goods_asset.get('display_name')
                goods_description = ''
                goods_image = self.util.get_image_path(goods_asset.get('processed_document').get('iconPath'))
                goods_category = 'package'

            elif goods_type == 7:
                goods_path = codelist.get('ProfileItemMasterDataStoreSource').get(code)[0]
                goods_asset = self.util.get_asset_by_path(goods_path)
                goods_name = goods_asset.get('processed_document').get('displayName_translation').get('gbl') or goods_asset.get('processed_document').get('displayName_translation').get('ja')
                goods_description = goods_asset.get('processed_document').get('shortDisplayName_translation').get('gbl') or goods_asset.get('processed_document').get('shortDisplayName_translation').get('ja')
                goods_image = self.util.get_image_path(goods_asset.get('processed_document').get('iconPath'))
                goods_category = 'profile_icon'

            else:
                for gtype in codelist.keys():
                    if codelist.get(gtype).get(code) is not None:
                        raise AttributeError(f'{gtype}: {goods_type}')

            self.goods.append({
                'shop_id': shop_document.get('linked_asset_id'),
                'shop_name': shop_document.get('displayName_translation').get('gbl') or shop_document.get('displayName_translation').get('ja'),
                'list_order': list_order,
                'purchasable_count': purchasable_count,
                'quantity': quantity,
                'goods_path': goods_path,
                'goods_cost': goods_cost,
                'goods_name': goods_name,
                'goods_image': goods_image,
                'goods_description': goods_description,
                'goods_category': goods_category
            })

        self.util.save_redis_asset(cache_key=self.cache_key, data=sorted(self.goods, key=lambda d: d['list_order']))

        return sorted(self.goods, key=lambda d: d['list_order'])
