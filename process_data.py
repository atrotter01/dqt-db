from app.util import Util
from app.data import DataProcessor
from app.data.assetprocessor import AssetProcessor

util = Util()
data_processor = DataProcessor(_util=util)
asset_processor = AssetProcessor(_util=util, _data_processor=data_processor)
asset_processor.process_assets()
