from BookingSyncApi.api import API
import json
import csv
import pandas
import re

# LINK: https://www.bookingsync.com/en/admin/v2/14030/preferences/fees


def add_fee(api, rental_id, fee_id):
    payload = {
        "rentals_fees": [
            {"always_applied": True, "fee_id": fee_id, "status": "private"}
        ]
    }
    print(api.post(f"/rentals/{rental_id}/rentals_fees", payload).text)


"""
reg_string example:
    ZAK|GDA|WAW
"""


def add_fees(rentals_filename, reg_string, fee_id, dry_run=False):
    api = API()
    df = pandas.read_excel(rentals_filename)

    cityFilter = df["name"].str.contains(reg_string, regex=True)
    parkingFilter = df["name"].str.contains("parking", case=False)
    df = df[cityFilter & (~parkingFilter)]

    fees = [fee_id]

    for _, row in df.iterrows():
        print(row["id"], row["name"])
        for fee_id in fees:
            if not dry_run:
                add_fee(api, row["id"], fee_id)


def add_fees_from_xlsx(fees_filename, rentals_filename, dry_run=False):
    df = pandas.read_excel(fees_filename)

    for _, row in df.iterrows():
        reg_string = "|".join(
            [re.escape(string) for string in row["Rentals"].split(",")]
        )
        print(f'Adding fee {row["fee_id"]} for {reg_string}.')
        add_fees(rentals_filename, reg_string, row["fee_id"], dry_run=dry_run)


def remove_fees():
    fees = [
        39939,
    ]

    api = API()
    df = pandas.read_excel("fees.xlsx")

    cityFilter = df["name"].str[:3] == "MIE"
    df = df[cityFilter]

    for _, row in df.iterrows():
        print(row["id"])
        rental = api.get(f'/rentals/{row["id"]}?include=rentals_fees').json()[
            "rentals"
        ][0]

        for fee in rental["rentals_fees"]:
            if fee["links"]["fee"] in fees:
                print(api.delete(f'/rentals_fees/{fee["id"]}').text)


def get_fees():
    api = API()

    print(json.dumps(api.get("/rentals/129345?include=rentals_fees").json(), indent=4))
    # print(json.dumps(api.get('/fees?page=2').json(), indent=4))


if __name__ == "__main__":
    add_fees_from_xlsx("fees_by_cities.xlsx", "fees.xlsx", dry_run=False)
