from aiohttp import web

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