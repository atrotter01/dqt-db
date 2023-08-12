from app.util import Util

util: Util = Util()

keys = [x for x in util.redis_client.keys() if x.decode().endswith('_parsed_data')]

for key in keys:
    print(f'Deleting {key}.')
    util.redis_client.delete(key)

