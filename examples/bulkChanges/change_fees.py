from BookingSyncApi.api import API

def change_fees():
    api = API()
    endpoint = "/rentals?include=rentals_fees"


    pages = int(api.get(endpoint).json()['meta']['X-Total-Pages'])
    print(pages)

    for page in range(1, pages + 1):
        data = api.get(endpoint + f"&page={page}").json()

        for rental in data["rentals"]:
            if rental["name"][:3] == "KOŁ":
                print(rental["name"], rental["id"])
                for fee in rental["rentals_fees"]:
                    if fee["links"]["fee"] in [29314, 41614] and fee["end_date"] != "2021-09-30":
                        print(fee["name"]["en"])

    
    # payload = {"rentals_fees" : [{"end_date" : "2021-09-30"}]}
    # print(api.put("/rentals_fees/206734", payload))

change_fees()

