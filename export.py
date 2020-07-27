from BookingSync.api import API
import requests, json, csv

def getRentals(api, page=1):
    url = f'https://www.bookingsync.com/api/v3/rentals'

    params = {
        'page' : page,
    }
    headers = api.getDefaultHeaders()

    return requests.get(url, params=params, headers=headers)

def export():
    api = API()
    json = getRentals(api).json()
    csvFields = ['id', 'name', 'city', 'headline', 'description', 'website_url']
    with open('export.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csvFields, extrasaction='ignore')
        writer.writeheader()
        for page in range(1, int(json['meta']['X-Total-Pages']) + 1):
            data = getRentals(api, page).json()
            for row in data['rentals']:
                writer.writerow(row)

export()
