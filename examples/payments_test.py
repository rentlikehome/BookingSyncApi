import json
from BookingSyncApi.api import API
import pandas as pd
import datetime

api = API()
api.print_json(api.get('/payments/9383752?include=bookings').json())
exit()

pages = int(api.get('/payments').json()['meta']['X-Total-Pages'])


payment_fields = ['id', 'paid_at', 'amount_in_cents', 'kind', 'created_at', 'canceled_at']
booking_fields = ['id', 'start_at', 'end_at', 'final_price', 'paid_amount']

fields = payment_fields + ['booking_' + fieldname for fieldname in booking_fields]

rows = []
for page in range(50, pages + 1):
    print(page)
    data = api.get(f'/payments?include=bookings&page={page}').json()
    for payment in data['payments']:
        parsedStartDate = datetime.datetime.strptime(payment['bookings'][0]['start_at'], "%Y-%m-%dT%H:%M:%SZ").date()
        if parsedStartDate <= datetime.date(2021, 7, 31) and parsedStartDate >= datetime.date(2021, 7, 1):
            row = []
            for field in payment_fields:
                row.append(payment[field])

            for field in booking_fields:
                row.append(payment['bookings'][0][field])

            print(row)
            rows.append(row)

    if page % 10 == 0:
        df = pd.DataFrame(rows, columns=fields)
        df.to_excel('export_payments.xlsx')

df = pd.DataFrame(rows, columns=fields)
df.to_excel('export_payments.xlsx')




