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
