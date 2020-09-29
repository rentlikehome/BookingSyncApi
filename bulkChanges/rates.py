from BookingSyncApi.api import API
import json
import pandas as pd
import traceback

def update_rules():
    api = API()

    df = pd.read_excel('rates.xlsx', index_col='id')

    for page in range(1, 7):
        response = api.get(f'/rates_tables?include=rates_rules&page={page}').json()
        for table in response['rates_tables']:
            rentals = table['links']['rentals']
            if rentals and rentals[0] in df.index:
                for rule in table['rates_rules']:
                    if rule['kind'] == 'stay_at_least':
                        if rule['variables']['length'] == 14:
                            rule['percentage'] = '-15.0'
                            payload = {
                                    'rates_rules' : [rule,]
                                    }
                            r = api.put(f'/rates_rules/{rule["id"]}', payload)
                            print(r.text)
                            df.at[rentals[0], 'processed'] = 1
                        elif rule['variables']['length'] == 28:
                            rule['percentage'] = '-20.0'
                            payload = {
                                    'rates_rules' : [rule,]
                                    }
                            r = api.put(f'/rates_rules/{rule["id"]}', payload)
                            print(r.text)
                            df.at[rentals[0], 'processed'] = 1
    df.to_excel('rates_update.xlsx')

def single_rule_addition():
    api = API()
    df = pd.read_excel('rules.xlsx')

    for index, row in df.iterrows():
        try:
            table_id = api.get(f'/rentals/{row["id"]}').json()['rentals'][0]['links']['rates_table']
        except:
            print(f'No rental with ID: {row["id"]}')
            continue
        
        
        payload = {
            'rates_rules' : [
                {
            "always_applied": True,
            "percentage": "-10.0",
            "fixed_amount": None,
            "period_name": None,
            "kind": "late_booking",
            "variables": {
                "length": 60,
                "unit": "days"
            },
            "start_date": None,
            "end_date": None,
            "canceled_at": None 
            }]
        }

        r = api.post(f'/rates_tables/{table_id}/rates_rules', payload)
        print(r.text)

        try:
            response_headers = dict(r.headers)
            if int(response_headers['x-ratelimit-remaining']) < 10:
                resetTime = datetime.fromtimestamp(int(response_headers['x-ratelimit-reset']))
                print(f'Waiting until {resetTime} ...')
                while datetime.now() < resetTime:
                    time.sleep(10)
        except:
            traceback.print_exc()

single_rule_addition()
# api = API()
# print(json.dumps(api.get('/rates_tables/348244').json(), indent=4))
