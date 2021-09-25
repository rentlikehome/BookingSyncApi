from BookingSyncApi.api import API
import json, csv
import pandas as pd
from datetime import datetime

def export_fees():
    api = API()

    columns = ['fee_id', 'booking_id', 'fee_name', 'city', 'price', 'booking_start_at', 'booking_end_at', 'num_of_guests']
    endpoint = "/bookings?include=bookings_fees,rental&from=20201231"

    pages = int(api.get(endpoint).json()['meta']['X-Total-Pages'])
    print(pages)

    rows = []
    for page in range(1, pages + 1):
        print(page)
        response = api.get(endpoint + f'&page={page}').json()
        for booking in response['bookings']:
            parsedStartDate = datetime.strptime(booking['start_at'], "%Y-%m-%dT%H:%M:%SZ")
            parsedEndDate = datetime.strptime(booking['end_at'], "%Y-%m-%dT%H:%M:%SZ")
            for fee in booking['bookings_fees']:
                row = []
                row.append(fee['id'])
                row.append(booking['id'])
                row.append(fee['name']['en'])
                row.append(booking['rental']['city'])
                row.append(float(fee['price']))
                row.append(parsedStartDate)
                row.append(parsedEndDate)
                num_of_guests = 0

                try:
                    num_of_guests += int(booking['adults'])
                except TypeError:
                    pass

                try:
                    num_of_guests += int(booking['children'])
                except TypeError:
                    pass

                row.append(num_of_guests)

                rows.append(row)

    df = pd.DataFrame(rows, columns=columns,)
    df.to_excel("fees_export.xlsx", engine='xlsxwriter')


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
    export_fees()
