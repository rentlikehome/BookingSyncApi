import json
from BookingSyncApi.api import API
import pandas as pd

api = API()

print(json.dumps(api.get('/payments?page=90').json(), indent=4))

print(json.dumps(api.get('/bookings_payments/8830406').json(), indent=4))
