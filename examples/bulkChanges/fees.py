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
        "status": "required"
        }
    ]
    }
    print(api.post(f'/rentals/{rental_id}/rentals_fees', payload).text)



def add_fees():
    api = API()
    df = pandas.read_excel('fees.xlsx')

    cityFilter = df['name'].str[:3] == 'MIE'
    df = df[cityFilter]

    fees = [39949]

    for _, row in df.iterrows():
        print(row['id'])
        for fee_id in fees:
            add_fee(api, row['id'], fee_id)

def remove_fees():
    fees = [39939,]

    api = API()
    df = pandas.read_excel('fees.xlsx')

    cityFilter = df['name'].str[:3] == 'MIE'
    df = df[cityFilter]

    for _, row in df.iterrows():
        print(row['id'])
        rental = api.get(f'/rentals/{row["id"]}?include=rentals_fees').json()['rentals'][0]

        for fee in rental['rentals_fees']:
            if fee['links']['fee'] in fees:
                print(api.delete(f'/rentals_fees/{fee["id"]}').text)



def get_fees():
    api = API()

    print(json.dumps(api.get('/rentals/129345?include=rentals_fees').json(), indent=4))
    # print(json.dumps(api.get('/fees?page=2').json(), indent=4))


if __name__ == '__main__':
    get_fees()


