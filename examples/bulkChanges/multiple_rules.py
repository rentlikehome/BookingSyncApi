from BookingSyncApi.api import API
import json
import pandas as pd

newRule = {
    "rates_rules": [
        {
            "always_applied": True,
            "percentage": None,
            "fixed_amount": None,
            "period_name": None,
            "kind": "prevent_if_booked_less_than",
            "variables": {"length": 1, "unit": "days"},
        }
    ]
}

newRule2 = {
    "rates_rules": [
        {
            "always_applied": False,
            "percentage": None,
            "fixed_amount": None,
            "period_name": "Wielkanoc",
            "kind": "departure_only",
            "variables": {"days": [3, 5]},
            "start_date": "2021-03-31",
            "end_date": "2021-04-02",
        }
    ]
}


def get_rules(rental_id):
    api = API()
    rental = api.get(f"/rentals/{rental_id}").json()["rentals"][0]
    table_id = rental["links"]["rates_table"]
    print(
        json.dumps(
            api.get(f"/rates_tables/{table_id}?include=rates_rules").json(), indent=4
        )
    )


def modify_table():
    api = API()
    df = pd.read_excel("rules.xlsx", index_col="id")

    # Filter for Zakopane
    cityFilter = df["name"].str[:3] != "MDZ"
    df = df[cityFilter]

    pages = int(
        api.get(f"/rates_tables?include=rates_rules").json()["meta"]["X-Total-Pages"]
    )
    for page in range(1, pages + 1):
        response = api.get(f"/rates_tables?include=rates_rules&page={page}").json()

        for table in response["rates_tables"]:
            rentals = table["links"]["rentals"]
            if rentals and rentals[0] in df.index:
                # print(rentals[0], api.delete(f'/rates_rules/{rule["id"]}').text)

                print(
                    api.post(f'/rates_tables/{table["id"]}/rates_rules', newRule).text
                )
                # print(api.post(f'/rates_tables/{table["id"]}/rates_rules', newRule2).text)

                for rental in rentals:
                    df.at[rental, "processed"] = 1

    df.to_excel("rules_update.xlsx")


modify_table()
# get_rules(128585)
