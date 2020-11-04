from BookingSyncApi.api import API
import json, csv
import pandas as pd
from datetime import datetime

def export_fees():
    api = API()

    with open('fees.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        fieldnames = ['name', 'city', 'price']
        writer.writerow(fieldnames)

        ## !! Hardcoded pages
        for page in range(1, 32):
            response = api.get(f'/bookings?include=bookings_fees,rental&from=20200731&page={page}').json()
            for booking in response['bookings']:

                parsedStartDate = datetime.strptime(booking['start_at'], "%Y-%m-%dT%H:%M:%SZ")
                if parsedStartDate.month == 8:
                    for fee in booking['bookings_fees']:
                        writer.writerow([fee['name']['en'], booking['rental']['city'], fee['price']])

def export_fees_from_rental():
    api = API()
    response = api.get('/rentals').json()
    csvFields = ['rental_id', 'rental_name', 'city', 'id', 'always_applied', 'end_date', 'maximum_bookable', 'public', 'required', 'start_date', 'created_at', 'name', 'rate', 'rate_kind', 'archived_at']

    with open('export.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csvFields, extrasaction='ignore')
        writer.writeheader()
        for page in range(1, int(response['meta']['X-Total-Pages']) + 1):
            data = api.get(f'/rentals?include=rentals_fees&page={page}').json()
            for row in data['rentals']:
                for fee in row['rentals_fees']:
                    fee['name'] = fee['name']['pl']
                    fee['rental_id'] = row['id']
                    fee['rental_name'] = row['name']
                    fee['city'] = row['city']
                    writer.writerow(fee)

def export_cleaning_fees():
    api = API()
    response = api.get('/rentals').json()

    csvFields = ['rental_id', 'rental_name', 'city', 'sleeps_max', 'surface', 'rate', 'name', ]

    with open('export.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csvFields, extrasaction='ignore')
        writer.writeheader()
        for page in range(1, int(response['meta']['X-Total-Pages']) + 1):
            data = api.get(f'/rentals?include=rentals_fees&page={page}').json()
            for row in data['rentals']:
                for fee in row['rentals_fees']:
                    fee['name'] = fee['name']['en']
                    fee['rental_id'] = row['id']
                    fee['rental_name'] = row['name']
                    fee['city'] = row['city']
                    fee['sleeps_max'] = row['sleeps_max']
                    fee['surface'] = row['surface']

                    if 'Cleaning' in fee['name']:
                        writer.writerow(fee)

if __name__ == '__main__':
    export_cleaning_fees()
