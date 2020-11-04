import json
from BookingSyncApi.api import API
import pandas as pd

api = API()

url = '/bookings?from=20000101&include=bookings_fees,rental'
pages = int(api.get(url).json()['meta']['X-Total-Pages'])

columns = ['bookingID', 'rentalID', 'rentalName', 'start_at', 'end_at', 'sourceID', 'initial_price', 'final_price', 'final_rental_price', 'downpayment', 'fee_price']

rows = []
for page in range(1, pages + 1):
    data = api.get(url + f'&page={page}').json()

    for booking in data['bookings']:
        for fee in booking['bookings_fees']:
            if 'VAT' in fee['name']['en']:
                newRow = []
                newRow.append(booking['id'])
                newRow.append(booking['rental']['id'])
                newRow.append(booking['rental']['name'])
                newRow.append(booking['start_at'])
                newRow.append(booking['end_at'])
                newRow.append(booking['links']['source'])
                newRow.append(booking['initial_price'])
                newRow.append(booking['final_price'])
                newRow.append(booking['final_rental_price'])
                newRow.append(booking['downpayment'])
                newRow.append(fee['price'])
                rows.append(newRow)

df = pd.DataFrame(rows, columns=columns)
df.to_excel('vat_fees.xlsx')


