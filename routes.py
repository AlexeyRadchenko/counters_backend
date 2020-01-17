import aiohttp_cors
from handlers.auth_handlers import user_login
from handlers.data_handlers import get_account_counters, put_counter_data
from settings import config
from aiohttp_jwt import check_permissions, match_any
from settings import config

root_url = config['api']['root_url']
version_1 = config['api']['versions'][1]

def setup_routes(app, web):
    app.add_routes([
        web.post(f'{root_url}{version_1}/login', user_login),
        #web.post('/api/v1/login', user_login),
        web.get('/accounts/{account_id__company_id}/counters', 
            check_permissions(config['permissions']['groups']['account_data'], comparison=match_any)(get_account_counters)),
        web.put('/accounts/{account_id__company_id}/counters/{counter_id}', put_counter_data)
    ])


def setup_cors(app):
    cors = aiohttp_cors.setup(app, defaults={
    config['cors']['site']: aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*"
        )
    })

    for route in list(app.router.routes()):
        cors.add(route)