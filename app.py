import sys
import argparse
import asyncio
import uvloop

from aiohttp import web
from aiohttp_jwt import JWTMiddleware
from aiopg.sa import create_engine

from db import init_db_engine, close_db_engine, create_tables, drop_tables, insert_values
from models.users import user_tables
from settings import config
from routes import setup_routes, setup_cors
#from aiohttp_swagger import setup_swagger
from aiohttp_swagger3 import SwaggerDocs, SwaggerUiSettings


app = web.Application(
    middlewares=[
        JWTMiddleware(
            secret_or_pub_key=config['jwt']['secret'],
            #token_getter=get_token,
            #request_property='user',
            whitelist=[
                r'/api/v1/login',
                r'/api/doc'
            ]
        ),
    ]
)

setup_routes(app, web)
setup_cors(app)
#setup_swagger(app, swagger_from_file="docs/sw_docs.yaml")

app['config'] = config
app.on_startup.append(init_db_engine)
app.on_cleanup.append(close_db_engine)   


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--create_tables', action='store_true', help='Create tables in DB')
    parser.add_argument('-d', '--drop_tables', nargs='+', default=[], help='Drop tables in DB')
    parser.add_argument('-s', '--start', action='store_true', help='Start application')
    parser.add_argument('--cu', action='store_true', help='Insert test values to users table')

    args = parser.parse_args()

    if args.create_tables:
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        loop = asyncio.get_event_loop()
        eng = loop.run_until_complete(init_db_engine(in_app=False))
        loop.run_until_complete(create_tables(eng, user_tables.values()))
        loop.run_until_complete(close_db_engine(engine=eng, in_app=False))

    if args.drop_tables:
        drop_list = []
        for k in args.drop_tables:
            drop_list.append(user_tables[k])
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        loop = asyncio.get_event_loop()
        eng = loop.run_until_complete(init_db_engine(in_app=False))
        loop.run_until_complete(drop_tables(eng, drop_list))
        loop.run_until_complete(close_db_engine(engine=eng, in_app=False))

    if args.cu:
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        loop = asyncio.get_event_loop()
        eng = loop.run_until_complete(init_db_engine(in_app=False))
        loop.run_until_complete(insert_values(eng, user_tables['users'], 
            street='Володина',
            house='12',
            appartment='29',
        ))
        loop.run_until_complete(insert_values(eng, user_tables['groups'], name='users'))
        loop.run_until_complete(insert_values(eng, user_tables['companies'], name='Комфорт'))
        loop.run_until_complete(insert_values(eng, user_tables['logins'],
            username='100001001',
            password='any',
            user_profile=1
        ))
        loop.run_until_complete(insert_values(eng, user_tables['roles'], name='user'))
        loop.run_until_complete(insert_values(eng, user_tables['accounts'],
            account='100001001',
            company=1,
            user=1
        ))
        loop.run_until_complete(insert_values(eng, user_tables['memberships'],
            user=1,
            group=1,
            role=1,
            company=1
        ))
        loop.run_until_complete(close_db_engine(engine=eng, in_app=False))

    s = SwaggerDocs(
        app,
        swagger_ui_settings=SwaggerUiSettings(path="/docs/"),
        title="Swagger Petstore",
        version="1.0.0",
        components="docs/sw_docs.yaml"
    )  

    if args.start:
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        web.run_app(app, port=3000)