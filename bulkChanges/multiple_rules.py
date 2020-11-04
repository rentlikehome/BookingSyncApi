from BookingSyncApi.api import API
import json
import pandas as pd

newRule = {
    "rates_rules": [{
    "always_applied": True,
    "percentage": None,
    "fixed_amount": "10.0",
    "period_name": None,
    "kind": "additional_person_fixed_per_night",
    "variables": {
        "occupation_greater_than": "1"
    },
    "start_date": None,
    "end_date": None,
    "canceled_at": None
    }]
}
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
                    if rule['kind'] == "additional_person_fixed_per_night":
                        print("Deleting ", rule['variables']['occupation_greater_than'])
                        api.delete(f'/rates_rules/{rule["id"]}')
                print(api.post(f'/rates_tables/{table["id"]}/rates_rules', newRule).text)
                df.at[rentals[0], 'processed'] = 1

    df.to_excel('rules_update.xlsx')

modify_table()

