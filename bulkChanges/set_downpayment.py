from BookingSyncApi.api import API

import json
import pandas as pd

api = API()

df = pd.read_csv('export.csv')
filter_city = df['city'] == 'Gdańsk'
df = df[filter_city]

for index, row in df.iterrows():
    payload = {
    "rentals": [
        {
            'downpayment' : 0
        }
    ]
    }
    print(api.put(f'/rentals/{row["id"]}', payload).text)
