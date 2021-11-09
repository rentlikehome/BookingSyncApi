from bookingsyncapi.factory import YAMLApiFactory

import datetime
import logging
import dotenv

import sentry_sdk

sentry_sdk.init(
    "https://1c57587ee7da41599b79b3669b6e6dda@o1026489.ingest.sentry.io/5992847",
    environment="PROD",
)

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(fmt="%(levelname)s %(asctime)s %(module)s %(name)s.%(funcName)s:%(lineno)s- %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)


BOOKINGSYNC_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def create_booking(start_hour):
    today = datetime.datetime.today()
    tomorrow = today + datetime.timedelta(hours=24)

    today = today.replace(hour=start_hour)
    # Hardcoded 11:00 a.m.
    tomorrow = tomorrow.replace(hour=11)

    start_at = today.strftime(BOOKINGSYNC_DATE_FORMAT)
    end_at = tomorrow.strftime(BOOKINGSYNC_DATE_FORMAT)

    expiry = tomorrow.replace(hour=2).strftime(BOOKINGSYNC_DATE_FORMAT)

    booking = {
        "start_at": start_at,
        "end_at": end_at,
        "tentative_expires_at": expiry,
        "bookings_tag_ids": [5264],
    }

    return booking


def block_rental(api, rental_id, start_hour):
    payload = {
        "bookings": [
            create_booking(start_hour),
        ]
    }
    response = api.post(f"/rentals/{rental_id}/bookings", payload)

    if response.status_code == 503:
        response = api.post(f"/rentals/{rental_id}/bookings", payload)

    if response.status_code == 503:
        logger.warning(f"Got 503 twice in a row. Skipping {rental_id}.")

    """
    Status codes:
    - 201 - tentative booking created
    - 422 - tentative booking not created because rental already booked during this period
    """
    if response.status_code not in [201, 422]:
        logger.warning(
            f"Unrecognized status code [{response.status_code}]: {response.text}"
        )


def retry_at_error(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Got exception {e}. Retrying..")
            func(*args, **kwargs)

    return wrapper


"""
Assumptions:
- city_code is taken from first 3 chars of rental name
- we always create a tentative booking and we rely on bookingsync to check if apartment is available


This function will consume about 10 + the number of rentals with given city code requests to API which means
that if the number of rentals exceeds the request limit of 1000 we need to change this code
to take this into account.
"""


@retry_at_error
def block_rentals(account_id, city_code, start_hour):
    logger.info(f"Starting blocking for {city_code}.")
    config_file = dotenv.dotenv_values()["BOOKINGSYNCAPI_CONFIG_FILE"]

    api = YAMLApiFactory(config_file).get_api(account_id)

    response = api.get("/rentals?include=rentals_tags")
    pages = int(response.json()["meta"]["X-Total-Pages"])

    for page in range(1, pages + 1):
        data = api.get(f"/rentals?include=rentals_tags&page={page}").json()
        for rental in data["rentals"]:
            if rental["name"][:3] == city_code:
                block_rental(api, rental["id"], start_hour)


if __name__ == "__main__":
    # block_rentals("14030", "POZ", 18)
    pass
