import json
from BookingSyncApi.api import API
import pandas as pd

api = API()

# print(json.dumps(api.get('/inbox/messages/10421894?include=sender,hosts').json(), indent=4))
print(json.dumps(api.get('/hosts').json(), indent=4))
# print(json.dumps(api.get('/inbox/participants/3110823?include=member').json(), indent=4))
# print(json.dumps(api.get('/bookings/14824069?include=payments').json(), indent=4))
# print(json.dumps(api.get('/accounts/14030').json(), indent=4))
# print(json.dumps(api.get('/inbox/conversations/1196394').json(), indent=4))


            




