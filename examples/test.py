import json
import dotenv
from bookingsyncapi.factory import YAMLApiFactory
import pandas as pd

config_file = dotenv.dotenv_values()["BOOKINGSYNCAPI_CONFIG_FILE"]

api = YAMLApiFactory(config_file).get_api("14030")

# print(json.dumps(api.get('/inbox/messages/10421894?include=sender,hosts').json(), indent=4))
# print(json.dumps(api.get('/bookings/14752894?include_canceled=true').json(), indent=4))
# print(json.dumps(api.get("/reviews").json(), indent=4))
print(json.dumps(api.get("/hosts").json(), indent=4))
# print(json.dumps(api.get('/inbox/participants/3110823?include=member').json(), indent=4))
# print(json.dumps(api.get('/bookings/14824069?include=payments').json(), indent=4))
# print(json.dumps(api.get('/accounts/14030').json(), indent=4))
# print(json.dumps(api.get('/inbox/conversations/1196394').json(), indent=4))
