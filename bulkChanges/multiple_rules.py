from BookingSyncApi.api import API
import json
import pandas as pd

newRule = {
    "rates_rules": [{
            "always_applied": False,
            "percentage": None,
            "fixed_amount": None,
            "period_name": "Sezon",
            "kind": "charge_at_least_if_available",
            "variables": {
                "length": 4,
                "unit": "days"
            },
            "start_date": "2021-01-04",
            "end_date": "2021-02-28",
    }]
}
newRule2 = {
    "rates_rules": [{
            "always_applied": False,
            "percentage": None,
            "fixed_amount": None,
            "period_name": "Sezon",
            "kind": "charge_at_least_if_available",
            "variables": {
                "length": 5,
                "unit": "days"
            },
            "start_date": "2020-12-23",
            "end_date": "2022-01-03",
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
                    if rule['kind'] == "charge_at_least_if_available" and rule['variables']['length'] == 5 and rule['start_date'] == '2020-12-23':
                        print("Deleting rule1")
                        api.delete(f'/rates_rules/{rule["id"]}')
                    if rule['kind'] == "charge_at_least_if_available" and rule['variables']['length'] == 4 and rule['start_date'] == '2021-01-04':
                        print("Deleting rule2")
                        api.delete(f'/rates_rules/{rule["id"]}')
                print(api.post(f'/rates_tables/{table["id"]}/rates_rules', newRule).text)
                print(api.post(f'/rates_tables/{table["id"]}/rates_rules', newRule2).text)
                for rental in rentals:
                    df.at[rental, 'processed'] = 1

    df.to_excel('rules_update.xlsx')

modify_table()

