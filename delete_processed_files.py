import os
from app.util import get_asset_list

processed_files: list = get_asset_list()

for file in processed_files:
    filepath: str = file.get('filepath')

    if os.path.exists(filepath):
        print(f'Deleting {filepath}')
        os.unlink(filepath)