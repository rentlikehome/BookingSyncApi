import json
from BookingSyncApi.api import API
import pandas as pd

api = API()

pages = int(api.get('/bookings?include=rental').json()['meta']['X-Total-Pages'])


for page in range(1, pages + 1):
    data = api.get(f'/bookings?include=payments,rental&page={page}').json()
    for booking in data['bookings']:
        print(json.dumps(booking, indent=4))
        # count = 0
        # for payment in booking['payments']:
        #     if payment['paid_at']:
        #         # Create payment

