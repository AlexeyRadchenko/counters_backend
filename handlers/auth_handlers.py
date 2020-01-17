import jwt
import json
import sqlalchemy as sa
from aiohttp import web
from datetime import datetime, timedelta
from models.users import logins, users, memberships, companies, groups, accounts
from collections import OrderedDict
import psycopg2.extras
from passlib.hash import pbkdf2_sha512


async def check_address(street, house, appartment, db_result, request):
    if street != db_result.Users_street:
        return False, request.app['config']['errors']['messages']['street-error']['mess'], request.app['config']['errors']['messages']['street-error']['hint']
    if house != db_result.Users_house:
        return False, request.app['config']['errors']['messages']['house-error']['mess'], request.app['config']['errors']['messages']['house-error']['hint']
    if appartment != db_result.Users_appartment:
        return False, request.app['config']['errors']['messages']['appartment-error']['mess'], request.app['config']['errors']['messages']['appartment-error']['hint']
    return True, '', ''

async def get_login_info_from_db(conn, post_data):
    login_query = logins.select().where(logins.c.username == post_data['account'])
    db_result = await conn.execute(login_query)
    return await db_result.fetchone()

async def validate_login(login_result, post_data):
    if not login_result:
        return False
    if login_result.blocked:
        return False
    valid_pass = pbkdf2_sha512.verify(post_data['defpass'], login_result.password.hash)
    if not valid_pass:
        return False
    return True

async def get_user_data_from_login(conn, login_result):
    join_membership = users.join(memberships, memberships.c.user == users.c.id)
    join_group = join_membership.join(groups, groups.c.id == memberships.c.group)
    join_company = join_group.join(companies, companies.c.id == memberships.c.company)
    join_account = join_company.join(accounts, accounts.c.company == memberships.c.company)
    user_query = sa.select([memberships, users, groups, companies, accounts], use_labels=True).select_from(join_account).where(users.c.id == login_result.user_profile)
    db_result = await conn.execute(user_query)
    return await db_result.fetchone()

async def create_payload(user_json_data, user, request):
    user_json_data['user']['account'] = user.Accounts_account
    pl = {
        'user': user_json_data,
        'exp': datetime.utcnow() + timedelta(seconds=request.app['config']['jwt']['exp_delta_seconds']),
        'scopes': [user_json_data['group']['name']]
    }
    return pl

async def user_login(request):
    post_data = await request.json()
    db = request.app['db']
    login_valid = None
    user = None
    async with db.acquire() as conn:
        login_result = await get_login_info_from_db(conn, post_data)
        login_valid = await validate_login(login_result, post_data)
        if login_valid:
            user = await get_user_data_from_login(conn, login_result)

    if not user:
        json_response = {
            'error_message': request.app['config']['errors']['messages']['username-error']['mess'], 
            'error_recomend': request.app['config']['errors']['messages']['username-error']['hint']
        }
        return web.json_response(json_response, status=401)

    if user.Groups_name == request.app['config']['permissions']['groups']['users']:
        address_check, error, recomend = await check_address(post_data['street'], post_data['house'], post_data['appartment'], user, request)
        if not address_check:
            return web.json_response({'error_message': error, 'error_recomend': recomend}, status=401)
    user_json = memberships.db_result_to_json(user, key_values=['user', 'company', 'group'])
    payload = await create_payload(user_json, user, request)
    token = jwt.encode(payload, request.app['config']['jwt']['secret'], request.app['config']['jwt']['algorithm'])
    return web.json_response({'token': token.decode('utf-8')})
   