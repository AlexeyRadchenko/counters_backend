import sys
import argparse
import aiohttp_cors
import asyncio
import sqlalchemy as sa
import jwt

from aiohttp import web
from aiohttp_jwt import JWTMiddleware
from aiopg.sa import create_engine

from handlers.auth_handlers import login, secret, get_account_counters, put_counter_data
from db import init_db_engine, close_db_engine, create_tables, drop_tables, insert_values
from models.users import users, users_groups

tables_list = [users_groups, users]

async def get_token(request):
    res = jwt.encode({
        'account': '100001001',
    }, secret)
    print(res)
    if not isinstance('', bytes):
        token = ''.encode()
        print(token)
    return ''

app = web.Application(
    middlewares=[
        JWTMiddleware(
            secret_or_pub_key=secret,
            #token_getter=get_token,
            #request_property='user',
            whitelist=[
                r'/login'
            ]
        ),
    ]
)

app.add_routes([web.post('/login', login),
                web.get('/accounts/{account_id__company_id}/counters', get_account_counters),
                web.put('/accounts/{account_id__company_id}/counters/{counter_id}', put_counter_data)])

cors = aiohttp_cors.setup(app, defaults={
    'http://localhost:8080': aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*"
    )
})

for route in list(app.router.routes()):
    cors.add(route)
app.on_startup.append(init_db_engine)
app.on_cleanup.append(close_db_engine)   


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--create_tables', action='store_true', help='Create tables in DB')
    parser.add_argument('-d', '--drop_tables', action='store_true', help='Drop tables in DB')
    parser.add_argument('-s', '--start', action='store_true', help='Start application')
    parser.add_argument('-i', '--iu', action='store_true', help='Insert default values to users table')

    args = parser.parse_args()

    if args.create_tables:
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        loop = asyncio.get_event_loop()
        eng = loop.run_until_complete(init_db_engine(in_app=False))
        loop.run_until_complete(create_tables(eng, tables_list))
        loop.run_until_complete(close_db_engine(engine=eng, in_app=False))

    if args.drop_tables:
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        loop = asyncio.get_event_loop()
        eng = loop.run_until_complete(init_db_engine(in_app=False))
        loop.run_until_complete(drop_tables(eng, tables_list))
        loop.run_until_complete(close_db_engine(engine=eng, in_app=False))

    if args.iu:
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        loop = asyncio.get_event_loop()
        eng = loop.run_until_complete(init_db_engine(in_app=False))
        loop.run_until_complete(insert_values(eng, users, 
                account='100001001', 
                password='any',
                street='Володина',
                house='12',
                appartment='29',
                company=1
        ))
        loop.run_until_complete(insert_values(eng, users_groups, name='superadmin'))
        loop.run_until_complete(close_db_engine(engine=eng, in_app=False))

    if args.start:
        web.run_app(app, port=3000)