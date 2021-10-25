import json
from BookingSyncApi.api import API

api = API()

payload = {"conversations": [{"closed": True}]}

pages = int(api.get("/inbox/conversations").json()["meta"]["X-Total-Pages"])
count = 0

for page in range(1, pages + 1):
    data = api.get(f"/inbox/conversations?page={page}").json()

    for conv in data["conversations"]:
        if not conv["closed_at"]:
            print(api.put(f'/inbox/conversations/{conv["id"]}', payload).status_code)
