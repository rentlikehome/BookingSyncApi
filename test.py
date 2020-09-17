from BookingSyncApi.api import API
import json

api = API()

print(json.dumps(api.get('/bookings?include=bookings_fees,rental').json()['bookings'][0], indent=4))
