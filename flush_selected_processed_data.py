import argparse
from app.util import Util

#parser = argparse.ArgumentParser()
#parser.add_argument('--type')
#args = parser.parse_args()

util = Util()
#util.reset_processed_data(asset_type_to_reset=args.type)

# Guild Boss
#util.reset_processed_data(path='-1400780540462253343')
#util.reset_processed_data(path='-3705990144588386043')
#util.reset_processed_data(path='3994089815843366607')
#util.reset_processed_data(path='-4487386723366926342')
#util.reset_processed_data(path='5522849216505113038')
#util.reset_processed_data(path='-965203371287503015')
#util.reset_processed_data(path='92518006644669279')
#util.reset_processed_data(path='-8474284891530091249')
#util.reset_processed_data(path='-47780007596032169')
#util.reset_processed_data(path='-1025597186424606358')
#util.reset_processed_data(path='8320362531917023264')
#util.reset_processed_data(path='-8406799384074751569')
#util.reset_processed_data(path='-2265763625158480142')
#util.reset_processed_data(path='-3218834564771449912')
#util.reset_processed_data(path='7265874941785494478')
#util.reset_processed_data(path='-7208022388038415233')
#util.reset_processed_data(path='5968556107722251117')
#util.reset_processed_data(path='8296386512021214169')

# Translation
util.redis_client.delete('-2375090901635097832000')
util.redis_client.delete('-2375090901635097832000_data')
util.redis_client.delete('-2375090901635097832000_processed_data')
util.redis_client.delete('5894932678760388815000')
util.redis_client.delete('5894932678760388815000_data')
util.redis_client.delete('5894932678760388815000_processed_data')
util.redis_client.delete('7681253118616506923000')
util.redis_client.delete('7681253118616506923000_data')
util.redis_client.delete('7681253118616506923000_processed_data')
