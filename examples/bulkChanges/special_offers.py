from BookingSyncApi.api import API
import json
import pandas as pd

api = API()


def createPayload():
    payload = {
        "special_offers": [
            {
                "discount": 20.0,
                "start_date": "2021-02-16",
                "end_date": "2021-03-31",
                "name_en": "Winter at the Baltic Sea",
                "name_pl": "Zima nad Bałtykiem",
                "name_de": "Winter an der Ostsee",
            }
        ]
    }

    return payload


pages = int(api.get(f"/rentals").json()["meta"]["X-Total-Pages"])

for page in range(1, pages + 1):
    response = api.get(f"/rentals?page={page}").json()

    for rental in response["rentals"]:
        if rental["name"][:3] in [
            "MIE",
        ]:
            print(rental["name"][:3], rental["id"])
            print(
                api.post(
                    f'/rentals/{rental["id"]}/special_offers', createPayload()
                ).status_code
            )
