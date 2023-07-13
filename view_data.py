from app.util import Util
from app.translation import Translation
from pprint import pprint

util = Util(filetype='ArenaGhostNPC')
#translation = Translation()
asset_list: list = util.get_asset_list()
asset_list: list = [-1564704183638881606]

for path in asset_list:
    asset = util.get_asset_by_path(path)
    path: int = asset.get('path')
    document = asset.get('document')
    #print(translation.translation.get(document.get('npcName')))
    pprint(document)
    #print(document_dict.get('processed_document'))
