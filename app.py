from app import app
from app.util import Util

if __name__ == '__main__':
    util = Util()
    util.cache_api_tables()

    app.run(debug=True)
