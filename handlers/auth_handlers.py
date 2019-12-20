import jwt
import json
import sqlalchemy as sa
from aiohttp import web
from datetime import datetime, timedelta
from models.users import users, companies, users_groups
from collections import OrderedDict
import psycopg2.extras
from passlib.hash import pbkdf2_sha512

JWT_EXP_DELTA_SECONDS = 60
JWT_ALGORITHM = 'HS256'
secret = 'secret'

async def get_account_counters(request):
    account_id, company_id = request.match_info['account_id__company_id'].split('__')
    #print(account_id, company_id)
    date = datetime.now().strftime("%d.%m.%Y")
    user_counters_data = {
        'counters': {
            'electric_counters': [{
                'id': '51231234',
                'serial_number': '333213',
                'replaced': True,
                'company': 1,
                'type_src': 'Электрэнергия',
                'type_counter': 'simple',
                'data_simple': 32312,
                'data_day': None,
                'data_night': None,
                'date_modify': date,
                'data_previous_simple': 32000,
                'data_previous_day': None,
                'data_previous_night': None,
                'data_delta_simple': 312,
                'data_delta_day': None,
                'data_delta_night': None
            },
            {
                'id': '514',
                'serial_number': '333213',
                'type_src': 'Электрэнергия',
                'type_counter': 'simple',
                'data_simple': 32312,
                'data_day': None,
                'data_night': None,
                'date_modify': date,
                'data_previous_simple': 32000,
                'data_previous_day': None,
                'data_previous_night': None,
                'data_delta_simple': 312,
                'data_delta_day': None,
                'data_delta_night': None  
            }],
            'water_counters': [{
                'id': '1313131',
                'serial_number': '3212',
                'type_src': 'Холодная вода',
                'type_counter': 'simple',
                'data_cold': 123.000,
                'data_hot': None,
                'date_modify': date,
                'data_previous_cold': 123.321,
                'data_previous_hot': None,
                'data_delta_cold': 0.321,
                'data_delta_hot': None
            },
            {
                'id': '4123123',
                'serial_number': '0123',
                'type_src': 'Горячая вода',
                'type_counter': 'simple',
                'data_cold': None,
                'data_hot': 231.332,
                'date_modify': date,
                'data_previous_cold': 232.123,
                'data_previous_hot': None,
                'data_delta_cold': None,
                'data_delta_hot': 0.791
            }],
            'gas_counters':[]
        }
    }
    return web.json_response(user_counters_data)

async def put_counter_data(request):
    put_data = await request.post()
    print(put_data.keys())
    print(put_data['input-counter-id'])
    return web.Response(status=200)

async def check_address(street, house, appartment, db_result):
    if street != db_result.Users_street:
        return False, 'Улица не соответствует лицевому счету !', 'Убедитесь, что Вы вводите верный лицевой счет и адрес'
    if house != db_result.Users_house:
        return False, 'Номер дома не соответствует лицевому счету!', 'Убедитесь, что Вы вводите верный лицевой счет и адрес'
    if appartment != db_result.Users_appartment:
        return False, 'Номер квартиры не соответствует лицевому счету!', 'Убедитесь, что Вы вводите верный лицевой счет и адрес'
    return True, '', ''

async def login(request):
    post_data = await request.json()
    db = request.app['db']
    async with db.acquire() as conn:        
        join_company = sa.join(users, companies, companies.c.id == users.c.company)
        join = join_company.join(users_groups, users_groups.c.id == users.c.group)
        query = sa.select([users, companies, users_groups], use_labels=True).select_from(join).where(users.c.account == post_data['account'])
        db_result = await conn.execute(query)
        result = await db_result.fetchone()
    if result and pbkdf2_sha512.verify(post_data['defpass'], result[2].hash):
        address_check, error, recomend = await check_address(post_data['street'], post_data['house'], post_data['appartment'], result)
        if not address_check:
            return web.json_response({'error_message': error, 'error_recomend': recomend}, status=401)
        json_response = users.db_result_to_json(result, key_values=['account', 'street', 'house', 'appartment', 'company', 'group'])
        payload = {
            'user': json_response,
            'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
        }
        token = jwt.encode(payload, secret, JWT_ALGORITHM)
        del json_response['group']
        return web.json_response({'token': token.decode('utf-8'), 'user': json_response})
    elif not result:
        json_response = {'error_message': 'Лицевой счет не найден !', 'error_recomend': 'Убедитесь что вы ввели верный лицевой счет'}
        return web.json_response(json_response, status=401)
    """    
    user = {
        'account': post_data['account'],
        'street': post_data['street'],
        'house': post_data['house'],
        'appartment': post_data['appartment'],
        'company': {
            'company_id': 1,
            'company_name': 'Комфортный дом'
        },
        'attention_message': '',
    }"""
    


    