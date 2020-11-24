import json
from BookingSyncApi.api import API
import pandas as pd

api = API()

print(json.dumps(api.get('/payments/8861993').json(), indent=4))



