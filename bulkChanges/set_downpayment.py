from BookingSyncApi.api import API

import json
import pandas as pd

api = API()

df = pd.read_excel('downpayment.xlsx')

for index, row in df.iterrows():
    payload = {
    "rentals": [
        {
            'downpayment' : 30,
            'balance_due' : row["Balance"]
        }
    ]
    }
    print(row["ID"], api.put(f'/rentals/{row["ID"]}', payload).status_code)
