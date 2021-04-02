from BookingSyncApi.api import API

import json
import pandas as pd

api = API()

df = pd.read_excel('downpayment.xlsx')

cityFilter = df['name'].str[:3] == 'MIE'
df = df[cityFilter]

for index, row in df.iterrows():
    payload = {
    "rentals": [
        {
            'balance_due' : 3,
        }
    ]
    }
    print(row["id"], api.put(f'/rentals/{row["id"]}', payload).status_code)
