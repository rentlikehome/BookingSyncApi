from BookingSyncApi.api import API
import json
import pandas as pd

def modify_table():
    api = API()

    df = pd.read_excel('rules.xlsx', index_col='id')

    pages = int(api.get(f'/rates_tables?include=rates_rules').json()['meta']['X-Total-Pages'])
    for page in range(1, pages + 1):
        response = api.get(f'/rates_tables?include=rates_rules&page={page}').json()
        for table in response['rates_tables']:
            rentals = table['links']['rentals']
            if rentals and rentals[0] in df.index:
                for rule in table['rates_rules']:
                    if rule['kind'] == "late_booking" and rule['percentage'] == '-10.0':
                        api.delete(f'/rates_rules/{rule["id"]}')
                df.at[rentals[0], 'processed'] = 1

    df.to_excel('rules_update.xlsx')

modify_table()
