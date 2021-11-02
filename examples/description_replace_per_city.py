import json
from bookingsyncapi.api import API
import pandas as pd
import re

api = API()

pages = int(api.get("/rentals").json()["meta"]["X-Total-Pages"])

df = pd.read_excel("desc_replace_per_city.xlsx", index_col=0)

backup_rows = []
status_rows = []
for page in range(1, pages + 1):
    data = api.get(f"/rentals?page={page}").json()
    for rental in data["rentals"]:
        print(rental["name"][:3], rental["id"])

        description_en = rental["description"].get("en", "")
        description_pl = rental["description"].get("pl", "").replace("\r\n", "\n")

        try:
            row = df.loc[rental["name"][:3]]
        except KeyError:
            print("No city in file. Skipping...")
            continue

        payload = {"rentals": [{}]}

        pattern = row["original_pl"].replace(" ", r"\s*").replace("\n", r"\s*\n")
        if re.search(pattern, description_pl):
            description_pl = re.sub(pattern, row["new_pl"], description_pl)
            payload["rentals"][0]["description_pl"] = description_pl

        pattern = row["original_en"].replace(" ", r"\s*").replace("\n", r"\s*")
        if re.search(pattern, description_en):
            description_en = re.sub(pattern, row["new_en"], description_en)
            payload["rentals"][0]["description_en"] = description_en

        backup_row = [rental["id"], description_pl, description_en]
        backup_rows.append(backup_row)

        
        status_row = [
            rental["id"],
            rental["name"][:3],
            bool(payload["rentals"][0].get("description_pl", False)),
            bool(payload["rentals"][0].get("description_en", False)),
        ]
        print(status_row)
        if payload["rentals"][0].get("description_en", False) or payload["rentals"][0].get("description_pl", False):
            print(api.put(f'/rentals/{rental["id"]}', payload).status_code)

        status_rows.append(status_row)

columns = ["id", "pl", "en"]
df = pd.DataFrame(backup_rows, columns=columns)
df.to_excel("desc_backup.xlsx")

columns = ["id", "city", "changed_pl", "changed_en"]
df = pd.DataFrame(status_rows, columns=columns)
df.to_excel("desc_status.xlsx")
