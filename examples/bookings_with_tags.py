from BookingSyncApi.api import API
import requests, json, csv
import pandas

from datetime import datetime

api = API()
endpoint = '/bookings?include_canceled=True&from=20201231'
pages = int(api.get(endpoint).json()['meta']['X-Total-Pages'])
columns = ['id', 'end_at', 'has_receipt_tag']

rows = []
for page in range(1, pages + 1):
    data = api.get(endpoint + f'&page={page}').json()
    # print(json.dumps(data, indent=4))
    for booking in data['bookings']:
        row = []

        row.append(booking['id'])
        row.append(booking['end_at'])
        row.append(4593 in booking['links']['bookings_tags'])

        parsedEndDate = datetime.strptime(booking['end_at'], "%Y-%m-%dT%H:%M:%SZ")
        if parsedEndDate.month < 4:
            rows.append(row)

df = pandas.DataFrame(rows, columns=columns,)
df.to_excel('bookings_with_tags.xlsx', engine='xlsxwriter')
