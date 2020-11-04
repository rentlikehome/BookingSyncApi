from BookingSyncApi.api import API

import json
import pandas as pd

api = API()

df = pd.read_excel('rentals.xlsx')

for index, row in df.iterrows():
    payload = {
    "rentals": [
        {
            'downpayment' : 30,
            'balance_due' : 1
        }
    ]
    }
    print(row["id"], api.put(f'/rentals/{row["id"]}', payload).status_code)
