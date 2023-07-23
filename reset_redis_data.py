from app.util import Util

util = Util()
#util.reset_processed_data(asset_type_to_reset='AreaExtraReward')

util.cache_metadata(force_rebuild=True)
