from BookingSyncApi.api import API
import json
import csv
import pandas

# LINK: https://www.bookingsync.com/en/admin/v2/14030/preferences/fees

def add_fee(api, rental_id, fee_id):
    payload = {
    "rentals_fees": [
        {
        "always_applied": True,
        "fee_id": fee_id,
        "status": "private"
        }
    ]
    }
    print(api.post(f'/rentals/{rental_id}/rentals_fees', payload).status_code)



def add_fees():
    api = API()
    df = pandas.read_excel('fees.xlsx')

    wawFilter = df['name'].str[:3] == 'WAW'
    df = df[wawFilter]

    fees = [35050, 35049, 35048, 35047, 35046]

    for _, row in df.iterrows():
        print(row['id'])
        for fee_id in fees:
            add_fee(api, row['id'], fee_id)

def get_fees():
    api = API()

    # print(json.dumps(api.get('/rentals/128538?include=rentals_fees').json(), indent=4))
    print(json.dumps(api.get('/fees').json(), indent=4))


if __name__ == '__main__':
    add_fees()


