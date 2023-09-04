from app.data.assetimport import AssetImport
from app.util import Util

root_path: str = '/mnt/d/DQT/ja/data'
util: Util = Util()
assetimport: AssetImport = AssetImport(util=util, root_path=root_path)

assetimport.save_assets_to_db()
