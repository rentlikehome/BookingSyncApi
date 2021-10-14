import json
from BookingSyncApi.api import API
import pandas as pd

api = API()

AMENITY_ID = 58

pages = int(api.get("/rentals").json()["meta"]["X-Total-Pages"])
columns = ["id", "name", "city", "address", "zip", "has_washing_machine"]

rows = []
for page in range(1, pages + 1):
    data = api.get(f"/rentals?page={page}&include=rentals_amenities").json()
    for rental in data["rentals"]:
        row = []
        row.append(rental["id"])
        row.append(rental["name"])
        row.append(rental["city"])
        row.append(rental["address1"])
        row.append(rental["zip"])

        # Check if it has amenity: 1 if has, 0 if doesn't
        has_amenity = 0
        for amenity in rental["rentals_amenities"]:
            if amenity["links"]["amenity"] == AMENITY_ID:
                has_amenity = 1
                break

        row.append(has_amenity)

        rows.append(row)

df = pd.DataFrame(rows, columns=columns)
df.to_excel("rentals_w_am.xlsx")


def rental_w_fee():

    AMENITY_ID = 58

    pages = int(api.get("/rentals").json()["meta"]["X-Total-Pages"])
    columns = ["id", "name", "sleeps_max", "cleaning_fee"]

    rows = []
    for page in range(1, pages + 1):
        data = api.get(f"/rentals?page={page}&include=rentals_fees").json()
        for rental in data["rentals"]:
            row = []
            row.append(rental["id"])
            row.append(rental["name"])
            row.append(rental["sleeps_max"])

            cleaning_fee = ""
            for fee in rental["rentals_fees"]:
                if "Cleaning" in fee["name"]["en"]:
                    cleaning_fee = fee["rate"]
            row.append(cleaning_fee)

            rows.append(row)

    df = pd.DataFrame(rows, columns=columns)
    df.to_excel("rentals_export_w_fee.xlsx")
