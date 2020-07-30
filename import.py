import requests, json, csv

from datetime import datetime, timedelta

from BookingSyncApi.api import API

def createClient(api, fullname, email, phone, country_code):
    url = f'https://www.bookingsync.com/api/v3/clients'

    json = {
        "clients" : [
            {
                "fullname" : fullname,
            }
        ]
    }

    headers = api.getDefaultHeaders()

    response = requests.post(url, headers=headers, json=json).json()
    # print(response)
    client_id = response['clients'][0]['id']

    url += f'/{client_id}'

    json = {
        "clients" : [
            {
                "phones": [
                    {
                        "client_id": client_id,
                        "label": "phone",
                        "number": phone,
                        "country_code": country_code,
                        "primary": True,
                    }
                ],
                "emails": [
                        {
                            "client_id": 1,
                            "label": "default",
                            "email": email,
                            "primary": True,
                        }
                ],
            }
        ]
    }

    return client_id 

def createBooking(api, rentalID, json):
    """
    Example json:
    json = {
        "bookings": [
            {
            "adults": 1,
            "booked": True,
            "currency": "USD",
            "final_price": "2700.0",
            "start_at": "2020-08-16T16:00:00Z",
            "end_at": "2020-08-17T11:00:00Z",
            }
        ]
    }
    """
    url = f'https://www.bookingsync.com/api/v3/rentals/{rentalID}/bookings'
    headers = api.getDefaultHeaders()
    return requests.post(url, headers=headers, json=json)

def importBookings():
    api = API()
    with open('import_WAW-1.csv', encoding='utf-8-sig') as inputfile, open('import_status.csv', 'w') as outputfile:
        reader = csv.DictReader(inputfile, delimiter=';')
        writer = csv.DictWriter(outputfile, fieldnames=reader.fieldnames + ['bookingID',], delimiter=';')
        writer.writeheader()
        for row in reader:
            client_id = createClient(api, row['Nazwisko'], row['Email'], row['Telefon'], row['country'])
            parsedStartDate = datetime.strptime(row['startDate'], '%d.%m.%Y %H:%M')
            parsedStartDate.replace(hour=16)
            parsedEndDate = datetime.strptime(row['endDate'], '%d.%m.%Y %H:%M') + timedelta(days=1)
            parsedEndDate.replace(hour=11)
            json = {
                "bookings": [
                    {
                        "adults": row['persons'],
                        "booked": True,
                        "currency": "PLN",
                        "final_price": row['price'],
                        "start_at": parsedStartDate.isoformat(),
                        "end_at": parsedEndDate.isoformat(),
                        "client_id" : client_id,
                        "links": {
                            "source": 12303
                        }
                    }
                ]
            }

            response = createBooking(api, row['BSYNC RENTAL ID'], json)
            print(20*'-')
            print(f'ADDING BOOKING: {row["BSYNC RENTAL ID"]}')
            print(response.status_code)
            print(response.text)
            print(20*'-')
            try:
                row['bookingID'] = response.json()['bookings'][0]['id']
            except:
                row['bookingID'] = ''

            writer.writerow(row)

importBookings()
