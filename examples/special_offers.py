import json
from BookingSyncApi.api import API
import pandas as pd

api = API()

payload = {
    "special_offers": [
            {
                "name_en": "Special offer",
                "name_pl": "Oferta specjalna",
                "name_de": "Sonderangebot",
                "start_date": "2021-02-28",
                "end_date": "2021-06-30",
                "discount": 15.0,
            }
        ]
}

df = pd.read_excel('rentals.xlsx')

cityFilter = df['name'].str[:3] == 'KOŁ'
df = df[cityFilter]

for index, row in df.iterrows():
    print(api.post(f'/rentals/{row["id"]}/special_offers', payload).json())
