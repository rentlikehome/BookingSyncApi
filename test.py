import json
from BookingSyncApi.api import API
import pandas as pd

api = API()

print(json.dumps(api.get('/booking_comments?page=112').json(), indent=4))



