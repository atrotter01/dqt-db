from app.util import Util
util: Util = Util()

asset_list = util.asset_list
files: list = []

for path in asset_list:
    try:
        path = int(path)
        files.append(path)
    except Exception:
        pass

new_data: dict = {}

for path in files:
    data: dict = util.get_redis_asset(cache_key=path)
    date_imported = data.get('date_imported')
    filetype = data.get('filetype')
    valid_filetypes: list = [
        #'ActiveSkill',
        'AllyMonster',
        'ConsumableItem',
        #'EnemySkill',
        'Equipment',
        'ExchangeShop',
        #'Stage'
    ]

    if not filetype in valid_filetypes:
        continue

    if date_imported != '2023-09-25':
        asset = util.get_asset_by_path(path=path, deflate_data=True, build_processed_asset=True)
        document = asset.get('processed_document')
        display_name: str = None
        icon_path: str = None

        if document.get('displayName_translation') is not None:
            display_name = util.get_localized_string(data=document, key='displayName_translation', path=path)
        elif document.get('profile') is not None:
            display_name = util.get_localized_string(data=document.get('profile'), key='displayName_translation', path=path)
        elif document.get('passiveSkillName_translation') is not None:
            display_name = util.get_localized_string(data=document, key='passiveSkillName_translation', path=path)
        else:
            print(filetype)
            print(document)

        if document.get('iconPath') is not None:
            icon_path = util.get_image_path(image_path=document.get('iconPath'))
        elif document.get('profile') is not None:
            icon_path = util.get_image_path(image_path=document.get('profile').get('iconPath'))
        elif filetype == 'ActiveSkill' or filetype == 'EnemySkill':
            skill_rank = util.get_localized_string(data=document.get('originRarity'), key='displayName_translation', path=path)
            icon_path = util.get_image_path(image_path=f'Assets/Aiming/Textures/GUI/General/Icon/MonsterIcon/MonsterIconParts/MonsterRankIcon_{skill_rank}.png')
        elif filetype == 'Stage':
            icon_path = util.get_image_path(image_path=document.get('area').get('bannerPath'))
        elif filetype == 'ExchangeShop':
            icon_path = util.get_image_path(image_path=document.get('bannerPath'))
        else:
            print(filetype)
            print(document)

        if display_name == '':
            continue

        if new_data.get(date_imported) is None:
            new_data[date_imported] = {}
            new_data[date_imported]['assets'] = []

        new_data[date_imported]['assets'].append({
            'path': path,
            'display_name': display_name,
            'filetype': filetype,
            'icon_path': icon_path
        })

util.save_redis_asset(cache_key='sys_db_updates', data=new_data)
