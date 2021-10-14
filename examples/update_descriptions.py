import json
from BookingSyncApi.api import API
import pandas as pd

api = API()

en = """---"""

pl = """---"""

pages = int(api.get("/rentals").json()["meta"]["X-Total-Pages"])

rows = []
for page in range(1, pages + 1):
    data = api.get(f"/rentals?page={page}").json()
    for rental in data["rentals"]:
        # Only the rest
        # if rental['name'][:3] in ['WRO', 'POZ', 'MIE', 'ZAK',  'WAW']:
        # Only for KOŁ and GDA
        if rental["name"][:3] in [
            "GDA",
        ]:
            # ALL
            # if True:
            print(rental["name"][:3], rental["id"])
            try:
                description_en = rental["description"]["en"]
            except:
                description_en = ""

            try:
                description_pl = rental["description"]["pl"]
            except:
                description_pl = ""

            if description_pl and "---" in description_pl:
                split = description_pl.split("---")
                split[0] = pl
                new_pl = "".join(split)
            elif description_pl:
                new_pl = pl + "\n\n" + description_pl
            else:
                new_pl = ""

            if description_en and "---" in description_en:
                split = description_en.split("---")
                split[0] = en
                new_en = "".join(split)
            elif description_en:
                new_en = en + "\n\n" + description_en
            else:
                new_en = ""

            payload = {
                "rentals": [
                    {
                        "description_en": new_en,
                        "description_pl": new_pl,
                    }
                ]
            }

            print(api.put(f'/rentals/{rental["id"]}', payload).status_code)
            new_row = [rental["id"], description_pl, description_en]
            rows.append(new_row)

columns = ["id", "pl", "en"]
df = pd.DataFrame(rows, columns=columns)
df.to_excel("desc_backup.xlsx")
