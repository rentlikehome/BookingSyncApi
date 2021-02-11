import json
from BookingSyncApi.api import API
import pandas as pd

api = API()

# print(json.dumps(api.get('/payments?include=bookings').json(), indent=4))
print(json.dumps(api.get('/bookings/14696025?include=payments&from=20140324').json(), indent=4))

            




