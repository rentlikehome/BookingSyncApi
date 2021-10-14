from BookingSyncApi.api import API
import json
import pandas as pd
import traceback

api = API()


def createPayload(amenity_id):
    payload = {"rentals_amenities": [{"amenity_id": amenity_id, "details_en": None}]}

    return payload


pages = int(api.get(f"/rentals").json()["meta"]["X-Total-Pages"])


for page in range(1, pages + 1):
    response = api.get(f"/rentals?page={page}").json()

    for rental in response["rentals"]:
        print(rental["id"])
        print(
            api.post(
                f'/rentals/{rental["id"]}/rentals_amenities', createPayload(93)
            ).status_code
        )
