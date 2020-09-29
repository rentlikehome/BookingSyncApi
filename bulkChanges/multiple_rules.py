from BookingSyncApi.api import API
import json
import pandas as pd

rule1 = {
  "rates_rules": [
    {
      "always_applied": True,
      "kind": "departure_only",
      "fixed_amount" : None,
      "period_name" : None,
      "variables": {
        "days": [
          0,
          1,
          2,
          3,
          4,
          5,
          6
        ]
      }
    }
  ]
}

rule2 = {
  "rates_rules": [
    {
      "always_applied": True,
      "kind": "additional_person_fixed_per_night",
      "fixed_amount" : '25.0',
      "period_name" : None,
      "variables": {
          "occupation_greater_than": "2",
      }
    }
  ]
}


rule3 = {
  "rates_rules": [
    {
      "always_applied": True,
      "kind": "stay_at_least",
      "percentage" : '-10.0',
      "period_name" : None,
      "variables": {
          "length": 7,
          "unit": "days"
      }
    }
  ]
}

rule4 = {
  "rates_rules": [
    {
      "always_applied": True,
      "kind": "stay_shorter_than",
      "percentage" : '200.0',
      "period_name" : None,
      "variables": {
          "length": 2,
          "unit": "days"
      }
    }
  ]
}

def modify_table():
    api = API()

    df = pd.read_excel('rules.xlsx', index_col='id')
    rule1 = {
    "rates_rules": [
        {
        "always_applied": True,
        "kind": "stay_at_least",
        "percentage" : '-10.0',
        "period_name" : None,
        "variables": {
            "length": 7,
            "unit": "days"
        }
        }
    ]
    }

    rule2 = {
    "rates_rules": [
        {
        "always_applied": True,
        "kind": "stay_at_least",
        "percentage" : '-10.0',
        "period_name" : None,
        "variables": {
            "length": 14,
            "unit": "days"
        }
        }
    ]
    }

    for page in range(1, 7):
        response = api.get(f'/rates_tables?include=rates_rules&page={page}').json()
        for table in response['rates_tables']:
            rentals = table['links']['rentals']
            if rentals and rentals[0] in df.index:
                print(f'Deleting {len(table["rates_rules"])} rules.')
                for rule in table['rates_rules']:
                    api.delete(f'/rates_rules/{rule["id"]}')
                print(rentals[0])
                api.post(f'/rates_tables/{table["id"]}/rates_rules', rule1)
                print("Rule1 added.")
                api.post(f'/rates_tables/{table["id"]}/rates_rules', rule2)
                print("Rule2 added.")

    df.to_excel('rules_update.xlsx')

def new_table():
    api = API()

    df = pd.read_excel('rules.xlsx', index_col='id')

    for page in range(1, 7):
        response = api.get(f'/rates_tables?include=rates_rules&page={page}').json()
        for table in response['rates_tables']:
            rentals = table['links']['rentals']
            if rentals and rentals[0] in df.index:
                for rule in table['rates_rules']:
                    api.delete(f'/rates_rules/{rule["id"]}')
                print(rentals[0])
                api.post(f'/rates_tables/{table["id"]}/rates_rules', rule1)
                print("Rule1 added.")
                api.post(f'/rates_tables/{table["id"]}/rates_rules', rule2)
                print("Rule2 added.")
                print(api.post(f'/rates_tables/{table["id"]}/rates_rules', rule3).text)
                print("Rule3 added.")
                api.post(f'/rates_tables/{table["id"]}/rates_rules', rule4)
                print("Rule4 added.")
                df.at[rentals[0], 'processed'] = 1

    df.to_excel('rules_update.xlsx')

# new_table()

modify_table()
