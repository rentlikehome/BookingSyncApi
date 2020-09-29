from BookingSyncApi.api import API
import json, csv
import pandas as pd
from datetime import datetime

##
def export_fees():
    api = API()

    with open('fees.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        fieldnames = ['name', 'city', 'price']
        writer.writerow(fieldnames)

        for page in range(1, 32):
            response = api.get(f'/bookings?include=bookings_fees,rental&from=20200731&page={page}').json()
            for booking in response['bookings']:

                parsedStartDate = datetime.strptime(booking['start_at'], "%Y-%m-%dT%H:%M:%SZ")
                if parsedStartDate.month == 8:
                    for fee in booking['bookings_fees']:
                        writer.writerow([fee['name']['en'], booking['rental']['city'], fee['price']])
##


if __name__ == '__main__':
    # export_fees()
    print('text')
