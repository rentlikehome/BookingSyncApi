import requests, json, csv
from datetime import datetime

class API:

    def __init__(self, auth_code):
        access_token = self.auth(auth_code)
        self.default_headers = {
            'Authorization' : f'Bearer {access_token}',
        }

    def auth(self, auth_code):
        client_id = 'f4954a04b5987e96e9fb99b4ab04f8c2b47d7902c32feb63a63a220d04727d64'
        client_secret = '995da035eb74a397ed4dfae342303686626367e1cc84f6a29c646e390aac5c35'
        # Taken from here
# https://www.bookingsync.com/oauth/authorize?client_id=f4954a04b5987e96e9fb99b4ab04f8c2b47d7902c32feb63a63a220d04727d64&scope=bookings_read%20rentals_read%20bookings_write%20rentals_write%20clients_write%20inbox_write&response_type=code&redirect_uri=urn:ietf:wg:oauth:2.0:oob

        token_url = 'https://www.bookingsync.com/oauth/token'

        data = {
            'code' : auth_code,
            'grant_type' : 'authorization_code',
            'redirect_uri' : 'urn:ietf:wg:oauth:2.0:oob'
        }

        access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))

        if access_token_response.status_code == 401:
            raise Exception('Failed to authorize.')

        tokens = json.loads(access_token_response.text)

        with open('refresh_token.txt', 'w') as f:
            f.write(tokens['refresh_token'])

        return tokens['access_token']

    def refresh():
        pass

    def get(self, endpoint):
        url = f'https://www.bookingsync.com/api/v3{endpoint}'
        return requests.get(url, headers=self.default_headers)

    def post(self, endpoint, json):
        url = f'https://www.bookingsync.com/api/v3{endpoint}'
        return requests.post(url, headers=self.default_headers, json=json)

    def getHosts(self, page=1):
        url = 'https://www.bookingsync.com/api/v3/hosts'

        params = {
            'page' : page,
        }
        headers = self.default_headers

        return requests.get(url, params=params, headers=headers)

    def getAccounts(self, page=1):
        url = 'https://www.bookingsync.com/api/v3/accounts'

        params = {
            'page' : page,
        }
        headers = self.default_headers

        return requests.get(url, params=params, headers=headers)

    def getAmenities(self, page=1):
        url = 'https://www.bookingsync.com/api/v3/amenities'
        params = {
            'page' : page,
        }
        headers = self.default_headers

        return requests.get(url, params=params, headers=headers)

    def getRentals(self, page=1):
        url = 'https://www.bookingsync.com/api/v3/rentals'

        params = {
            'page' : page,
        }
        # params['fields'] = 'id,name,headline,description,website_url,city'
        headers = self.default_headers

        return requests.get(url, params=params, headers=headers)

    def getRental(self, rental_id):
        url = f'https://www.bookingsync.com/api/v3/rentals'

        params = {
            'id' : rental_id,
        }
        headers = self.default_headers

        return requests.get(url, params=params, headers=headers)

    def getClients(self, page=1):
        url = 'https://www.bookingsync.com/api/v3/clients'

        params = {
            'page' : page,
        }
        headers = self.default_headers

        return requests.get(url, params=params, headers=headers)

    def getBookings(self, page=1):
        url = 'https://www.bookingsync.com/api/v3/bookings'

        params = {
            'page' : page,
        }
        headers = self.default_headers

        return requests.get(url, params=params, headers=headers)

    def getBookingsFromRental(self, rental_id):
        url = f'https://www.bookingsync.com/api/v3/bookings'

        params = {
            'rental_id' : rental_id,
        }
        headers = self.default_headers

        return requests.get(url, params=params, headers=headers)

    
    def createBooking(self, rentalID, json):
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
        headers = self.default_headers
        return requests.post(url, headers=headers, json=json)

    def createClient(self, fullname, email, phone, country_code):
        url = f'https://www.bookingsync.com/api/v3/clients'

        json = {
            "clients" : [
                {
                    "fullname" : fullname,
                }
            ]
        }

        headers = self.default_headers

        client_id = requests.post(url, headers=headers, json=json).json()['clients'][0]['id']

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

    def deleteBooking(self, bookingID):
        url = f'https://www.bookingsync.com/api/v3/bookings/{bookingID}'
        headers = self.default_headers
        return requests.delete(url, headers=headers)

    def export(self):
        json = self.getRentals().json()
        csvFields = ['id', 'name', 'city', 'headline', 'description', 'website_url']
        with open('export.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csvFields, extrasaction='ignore')
            writer.writeheader()
            for page in range(1, int(json['meta']['X-Total-Pages']) + 1):
                data = self.getRentals(page).json()
                for row in data['rentals']:
                    writer.writerow(row)

    def importBookings(self):
        with open('import_POZ-1.csv', encoding='utf-8-sig') as inputfile, open('import_status.csv', 'w') as outputfile:
            reader = csv.DictReader(inputfile, delimiter=';')
            writer = csv.DictWriter(outputfile, fieldnames=reader.fieldnames + ['bookingID',], delimiter=';')
            writer.writeheader()
            for row in reader:
                client_id = self.createClient(row['Nazwisko'], row['Email'], row['Telefon'], row['country'])
                parsedStartDate = datetime.strptime(row['startDate'], '%d.%m.%Y %H:%M')
                parsedStartDate.replace(hour=16)
                parsedEndDate = datetime.strptime(row['endDate'], '%d.%m.%Y %H:%M')
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

                response = self.createBooking(row['BSYNC RENTAL ID'], json)
                print(response.status_code)
                print(response.text)
                try:
                    row['bookingID'] = response.json()['bookings'][0]['id']
                except:
                    row['bookingID'] = ''

                writer.writerow(row)

if __name__ == '__main__':
    api = API('abe6eec7aa51a5d7b59b4ad411ecb6e2f0777244d4b07f043e809b09d5e0d140')
    # print(api.createBooking(128429, json).text)



