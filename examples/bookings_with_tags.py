from BookingSyncApi.api import API
import requests, json, csv
import pandas

from datetime import datetime

api = API()
endpoint = '/bookings?from=20201231&include=rental'
pages = int(api.get(endpoint).json()['meta']['X-Total-Pages'])
print(pages)
columns = ['id', 'start_at', 'end_at', 'has_breakfast_tag', 'city', 'name', 'num_of_guests']

rows = []
for page in range(1, pages + 1):
    print(page)
    data = api.get(endpoint + f'&page={page}').json()
    for booking in data['bookings']:
        # print(json.dumps(booking, indent=4))
        row = []
        row.append(booking['id'])
        row.append(datetime.strptime(booking['start_at'], "%Y-%m-%dT%H:%M:%SZ"))
        row.append(datetime.strptime(booking['end_at'], "%Y-%m-%dT%H:%M:%SZ"))
        row.append(4657 in booking['links']['bookings_tags'])
        row.append(booking['rental']['city'])
        row.append(booking['rental']['name'])
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

df = pandas.DataFrame(rows, columns=columns,)
df.to_excel('bookings_with_tags.xlsx', engine='xlsxwriter')
