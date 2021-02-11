from BookingSyncApi.api import API
import json
import pandas as pd
import traceback

api = API()

def createPayload(amenity_id):
    payload = {
        "rentals_amenities": [
            {
                "amenity_id": amenity_id,
                "details_en": None 
            }
        ]
    }

    return payload

pages = int(api.get(f'/rentals').json()['meta']['X-Total-Pages'])

cutoff_id = 134383
cutoff = False

for page in range(1, pages + 1):
    response = api.get(f'/rentals?page={page}').json()

    for rental in response['rentals']:
        if cutoff:
            print(rental['id'])
            print(api.post(f'/rentals/{rental["id"]}/rentals_amenities', createPayload(348)).status_code)
            print(api.post(f'/rentals/{rental["id"]}/rentals_amenities', createPayload(349)).status_code)
        else:
            if rental['id'] != cutoff_id:
                print('Skipping...')
            else:
                print('Found cutoff')
                cutoff = True

