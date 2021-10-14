from BookingSyncApi.api import API

import json
import pandas as pd

api = API()

df = pd.read_excel("downpayment.xlsx")

# cityFilter = df['name'].str[:3].isin(['WAW', 'WRO', 'POZ', 'GDA'])
# df = df[cityFilter]

for index, row in df.iterrows():
    payload = {
        "rentals": [
            {
                "downpayment": 30,
            }
        ]
    }
    print(row["id"], api.put(f'/rentals/{row["id"]}', payload).status_code)
