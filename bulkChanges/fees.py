from BookingSyncApi.api import API
import json
import csv

# LINK: https://www.bookingsync.com/en/admin/v2/14030/preferences/fees

def add_fees():
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

def get_fees():
    api = API()

    # print(json.dumps(api.get('/rentals/128538?include=rentals_fees').json(), indent=4))
    print(json.dumps(api.get('/fees').json(), indent=4))


if __name__ == '__main__':
    get_fees()


