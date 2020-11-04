import json
from BookingSyncApi.api import API
import pandas as pd

api = API()

payload = {
    "special_offers": [
            {
                "name_en": "Early booker",
                "name_pl": "Wczesna rezerwacja",
                "name_de": "Early Booker",
                "start_date": "2021-04-01",
                "end_date": "2021-06-30",
                "discount": 15.0,
            }
        ]
}

df = pd.read_excel('GDA.xlsx')

for index, row in df.iterrows():
    print(json.dumps(api.post(f'/rentals/{row["id"]}/special_offers', payload).json(), indent=4))
