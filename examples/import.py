import requests, json, csv, traceback, time

from datetime import datetime, timedelta

from BookingSyncApi.api import API


def createClient(api, fullname, email, phone, country_code):
    url = f"https://www.bookingsync.com/api/v3/clients"

    if not fullname:
        return None

    json = {
        "clients": [
            {
                "fullname": fullname,
            }
        ]
    }

    headers = api.getDefaultHeaders()

    try:
        int(phone)
    except:
        phone = ""

    response = requests.post(url, headers=headers, json=json)
    client_id = response.json()["clients"][0]["id"]

    url += f"/{client_id}"

    json = {
        "clients": [
            {
                "phones": [
                    {
                        "client_id": client_id,
                        "label": "phone",
                        "number": phone,
                        "country_code": country_code,
                        "primary": True,
                    }
                ],
                "emails": [
                    {
                        "client_id": 1,
                        "label": "default",
                        "email": email,
                        "primary": True,
                    }
                ],
            }
        ]
    }

    response = requests.put(url, headers=headers, json=json)

    return client_id


def createBooking(api, rentalID, json):
    """
    Example json:
    json = {
        "bookings": [
            {
            "adults": 1,
            "booked": True,
            "currency": "USD",
            "final_price": "2700.0",
            "start_at": "2020-08-16T16:00:00Z",
            "end_at": "2020-08-17T11:00:00Z",
            }
        ]
    }
    """
    url = f"https://www.bookingsync.com/api/v3/rentals/{rentalID}/bookings"
    headers = api.getDefaultHeaders()
    return requests.post(url, headers=headers, json=json)


def importBookings():
    api = API()
    with open(
        "1910_IMPORT_MIE+GDA+ZAK.csv", encoding="utf-8-sig", newline=""
    ) as inputfile, open("import_status.csv", "w") as outputfile:
        reader = csv.DictReader(inputfile, delimiter=";")
        writer = csv.DictWriter(
            outputfile,
            fieldnames=reader.fieldnames
            + [
                "bookingID",
            ],
            delimiter=";",
        )
        writer.writeheader()

        for row in reader:
            if row["BSYNC ID"] == "":
                print(f'SKIPPING BOOKING: {row["id"]}')
                continue

            client_id = createClient(
                api, row["Nazwisko"], row["Email"], row["Telefon"], "PL"
            )
            parsedStartDate = datetime.strptime(row["startDate"], "%d.%m.%Y %H:%M")
            parsedStartDate = parsedStartDate.replace(hour=16)
            parsedEndDate = datetime.strptime(
                row["endDate"], "%d.%m.%Y %H:%M"
            ) + timedelta(days=1)
            parsedEndDate = parsedEndDate.replace(hour=11)
            json = {
                "bookings": [
                    {
                        "adults": row["persons"],
                        "booked": True,
                        "currency": "PLN",
                        "channel_price": row["price"],
                        "final_price": row["price"],
                        "start_at": parsedStartDate.isoformat(),
                        "end_at": parsedEndDate.isoformat(),
                        "client_id": client_id,
                        "source_id": 12303,
                        "notes": row["Uwagi"],
                    }
                ]
            }

            response = createBooking(api, row["BSYNC ID"], json)
            print(
                f'ADDING BOOKING: {row["BSYNC ID"]}\n\tStatus(201=GOOD): {response.status_code}'
            )
            try:
                row["bookingID"] = response.json()["bookings"][0]["id"]
            except:
                row["bookingID"] = ""

            writer.writerow(row)

            try:
                response_headers = dict(response.headers)
                if int(response_headers["x-ratelimit-remaining"]) < 10:
                    resetTime = datetime.fromtimestamp(
                        int(response_headers["x-ratelimit-reset"])
                    )
                    print(f"Waiting until {resetTime} ...")
                    while datetime.now() < resetTime:
                        time.sleep(10)
            except:
                traceback.print_exc()


def updateBookings():
    api = API()
    with open("import_status_WAW-1.csv", encoding="utf-8-sig") as inputfile:
        reader = csv.DictReader(inputfile, delimiter=";")
        for row in reversed(list(reader)):
            parsedStartDate = datetime.strptime(row["startDate"], "%d.%m.%Y %H:%M")
            parsedStartDate = parsedStartDate.replace(hour=16)
            parsedEndDate = datetime.strptime(
                row["endDate"], "%d.%m.%Y %H:%M"
            ) + timedelta(days=1)
            parsedEndDate = parsedEndDate.replace(hour=11)
            json = {
                "bookings": [
                    {
                        "start_at": parsedStartDate.isoformat(),
                        "end_at": parsedEndDate.isoformat(),
                    }
                ]
            }
            if row["bookingID"]:
                endpoint = f'/bookings/{row["bookingID"]}'
                response = api.put(endpoint, json)

                print(20 * "-")
                print(f'UPDATING BOOKING: {row["BSYNC RENTAL ID"]}')
                print(response.status_code)
                print(response.text)
                print(20 * "-")


importBookings()
