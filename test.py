from BookingSyncApi.api import API
import json

api = API()

print(json.dumps(api.get('/rentals?include=rentals_tags').json(), indent=4))

