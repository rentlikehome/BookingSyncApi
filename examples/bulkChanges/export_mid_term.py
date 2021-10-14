import json
import datetime
import pandas as pd
from BookingSyncApi.api import API

from itertools import groupby


def export_mid_term_rates():
    api = API()

    columns = ["id", "name", "city", "start_date", "end_date", "price"]

    # print(json.dumps(api.get('/rentals?include=mid_term_rate_map').json(), indent=4))
    response = api.get("/rentals?include=mid_term_rate_map").json()

    rows = []
    for page in range(1, int(response["meta"]["X-Total-Pages"]) + 1):
        data = api.get(f"/rentals?include=mid_term_rate_map&page={page}").json()
        for rental in data["rentals"]:
            rate_map = rental["mid_term_rate_map"]["map"].split(",")
            start_date = rental["mid_term_rate_map"]["start_date"]
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            for price, grouper in groupby(rate_map):
                new_row = []
                new_row.append(rental["id"])
                new_row.append(rental["name"])
                new_row.append(rental["city"])
                new_row.append(start_date.date())
                end_date = start_date + datetime.timedelta(days=len(list(grouper)))
                new_row.append(end_date.date())
                new_row.append(price)
                if price != "0":
                    rows.append(new_row)

                start_date = end_date

    df = pd.DataFrame(rows, columns=columns)
    df.to_excel("mid_term_maps.xlsx")


if __name__ == "__main__":
    export_mid_term_rates()
