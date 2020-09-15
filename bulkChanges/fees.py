from BookingSyncApi.api import API
import json
import csv


api = API()

with open('export.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    payload = {
    "rentals_fees": [
        {
        "always_applied": True,
        "fee_id": 29578,
        "status": "private"
        }
    ]
    }
    for row in reader:
        print(json.dumps(api.post(f'/rentals/{row["id"]}/rentals_fees', payload).json(), indent=4))
        # print(f'/rentals/row["id"]/rentals_fees')

