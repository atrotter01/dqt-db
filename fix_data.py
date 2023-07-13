import json
from app.util import Util
from app.translation import Translation
from pprint import pprint

util = Util(filetype='ArenaGhostNPC')
#translation = Translation()
asset_list: list = util.get_asset_list()
#asset_list = [-2014534983663632832]
for path in asset_list:
    asset = util.get_asset_by_path(path)
    path: int = asset.get('path')
    document = asset.get('processed_document')
    display_name = asset.get('display_name')

    if document is None:
        continue
    #print(translation.translation.get(document.get('npcName')))

    #util.save_document(path=path, document=json.loads(document))

    if type(document) is str:
        print(path)
        #util.save_document(path=path, document=json.loads(document))
        util.save_processed_document(path=path, processed_document=json.loads(document), display_name=display_name)
        #print(document_dict.get('processed_document'))
