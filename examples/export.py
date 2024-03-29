from BookingSyncApi.api import API
import requests, json, csv
import pandas

from datetime import datetime


def getRentals(api, page=1):
    url = f"https://www.bookingsync.com/api/v3/rentals"

    params = {
        "page": page,
        "include": "rentals_tags",
    }
    headers = api.getDefaultHeaders()

    return requests.get(url, params=params, headers=headers)


def export(outputFile):
    api = API()
    pages = int(
        api.get("/rentals?include=rentals_tags").json()["meta"]["X-Total-Pages"]
    )
    columns = ["id", "name", "city", "rentals_tags"]

    rows = []
    for page in range(1, pages + 1):
        data = api.get(f"/rentals?include=rentals_tags&page={page}").json()
        for rental in data["rentals"]:
            row = []
            tags = ";".join([tag["name"]["en"] for tag in rental["rentals_tags"]])

            row.append(rental["id"])
            row.append(rental["name"])
            row.append(rental["city"])
            row.append(tags)

            rows.append(row)
    df = pandas.DataFrame(
        rows,
        columns=columns,
    )
    df.to_excel(outputFile, engine="xlsxwriter")


def export_fees_from_rental():
    api = API()
    json = getRentals(api).json()
    csvFields = ["id", "name", "city", ""]

    with open("export.csv", "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csvFields, extrasaction="ignore")
        writer.writeheader()
        for page in range(1, int(json["meta"]["X-Total-Pages"]) + 1):
            data = getRentals(api, page).json()
            for row in data["rentals"]:
                row["rentals_tags"] = ";".join(
                    [tag["name"]["en"] for tag in row["rentals_tags"]]
                )
                writer.writerow(row)


def getBookingsStartingToday():
    api = API()

    with open("export_bookings.csv", "w") as outputfile:
        csvFields = [
            "bookingID",
            "city",
            "address",
            "startDate",
            "endDate",
            "price",
            "nazwisko",
        ]
        writer = csv.DictWriter(outputfile, fieldnames=csvFields, extrasaction="ignore")
        writer.writeheader()
        r = api.get("/bookings").json()
        pages = r["meta"]["X-Total-Pages"]

        for page in range(1, int(pages) + 1):
            json = api.get(f"/bookings?page={page}").json()
            for booking in json["bookings"]:

                parsedStartDate = datetime.strptime(
                    booking["start_at"], "%Y-%m-%dT%H:%M:%SZ"
                )
                if parsedStartDate >= datetime.today():
                    row = {}
                    row["bookingID"] = booking["id"]
                    row["startDate"] = booking["start_at"]
                    row["endDate"] = booking["end_at"]
                    row["price"] = booking["final_price"]

                    if booking["links"]["rental"]:
                        rental_response = api.get(
                            f'/rentals/{booking["links"]["rental"]}'
                        )
                        if rental_response.status_code == 200:
                            rental = rental_response.json()
                            try:
                                row["city"] = rental["rentals"][0]["city"]
                                row["address"] = rental["rentals"][0]["address1"]
                            except:
                                pass

                    if booking["links"]["client"]:
                        client_response = api.get(
                            f'/clients/{booking["links"]["client"]}'
                        )
                        if client_response.status_code == 200:
                            try:
                                client = client_response.json()
                                row["nazwisko"] = client["clients"][0]["fullname"]
                            except:
                                pass
                    writer.writerow(row)


if __name__ == "__main__":
    export("rentals.xlsx")
