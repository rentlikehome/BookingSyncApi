import json
from BookingSyncApi.api import API
import pandas as pd

api = API()

pages = int(api.get('/rentals').json()['meta']['X-Total-Pages'])

df = pd.read_excel("desc_replace.xlsx")

rows = []
for page in range(1, pages + 1):
    data = api.get(f'/rentals?page={page}').json()
    for rental in data['rentals']:
        if rental['name'][:3] == "KOŁ":
            print(rental['name'][:3], rental['id'])
            try:
                description_en = rental['description']['en'] 
            except:
                description_en = ''

            try:
                description_pl = rental['description']['pl'] 
            except:
                description_pl = ''

            if description_pl:
                for idx, row in df.iterrows():
                    description_pl = description_pl.replace(row['original_pl'], row['new_pl'])

                new_pl = description_pl
            else:
                new_pl = ''


            if description_en:
                for idx, row in df.iterrows():
                    description_en = description_en.replace(row['original_en'], row['new_en'])

                new_en = description_en
            else:
                new_en =''


            if description_en or description_pl:
                payload = {
                    "rentals" : [
                        {
                            "description_en" : new_en,
                            "description_pl" : new_pl,

                        }
                    ]
                }

                print(api.put(f'/rentals/{rental["id"]}', payload).status_code)
                new_row = [rental['id'], description_pl, description_en]
                rows.append(new_row)
            else:
                print("empty desc")

columns = ['id', 'pl', 'en']
df = pd.DataFrame(rows, columns=columns)
df.to_excel('desc_backup.xlsx')
