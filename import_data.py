from app.assetimport import AssetImport
from app.util import Util

root_path: str = '/mnt/d/DQT'
util: Util = Util()
assetimport: AssetImport = AssetImport(util=util, root_path=root_path)

assetimport.save_assets_to_db()