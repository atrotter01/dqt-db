import requests
from app.util import Util
util: Util = Util()

for path in util.get_asset_list('AllyMonster'):
    requests.get(f'http://localhost:5000/api/unit/{path}')

requests.get(f'http://localhost:5000/api/unit')
requests.get(f'http://localhost:5000/api/skill/active_skill')
requests.get(f'http://localhost:5000/api/skill/passive_skill')
requests.get(f'http://localhost:5000/api/skill/reaction_skill')
requests.get(f'http://localhost:5000/api/skill/enemy_skill')
requests.get(f'http://localhost:5000/api/equipment')
