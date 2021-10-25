import requests, json, csv
from datetime import datetime, timedelta

import os
import json

import logging

logger = logging.getLogger(__name__)


class API:
    def __init__(self, auth_code=None):

        """
        client_id and client_secret are taken from here:
        https://www.bookingsync.com/en/partners/applications/1011/edit
        """
        self.session = requests.Session()

        self.client_id = (
            "f4954a04b5987e96e9fb99b4ab04f8c2b47d7902c32feb63a63a220d04727d64"
        )
        self.client_secret = (
            "995da035eb74a397ed4dfae342303686626367e1cc84f6a29c646e390aac5c35"
        )

        self.credsPath = os.path.dirname(os.path.abspath(__file__)) + "/creds.json"
        try:
            with open(self.credsPath, "r") as f:
                creds = json.load(f)
        except:
            print("Couldn't load credentials from file. Using manual authorization.")
            creds = {}

        refresh_token = creds.get("refresh_token", None)
        self.access_token = creds.get("access_token", None)

        if not self.isAuthorized():
            if not refresh_token:
                self.access_token = self.manualAuth(auth_code)
            else:
                self.access_token = self.refreshAuth(refresh_token)

    def __del__(self):
        self.session.close()

    def getDefaultHeaders(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
        }

    def isAuthorized(self):
        response = self.get("/bookings")
        return response.status_code != 401

    def authorize(self, data):

        token_url = "https://www.bookingsync.com/oauth/token"

        access_token_response = requests.post(
            token_url,
            data=data,
            verify=False,
            allow_redirects=False,
            auth=(self.client_id, self.client_secret),
        )
        # print(access_token_response.text)

        if access_token_response.status_code == 401:
            raise Exception("Failed to authorize.")

        tokens = json.loads(access_token_response.text)

        with open(self.credsPath, "w") as f:
            json.dump(tokens, f, indent=4)

        return tokens["access_token"]

    def manualAuth(self, auth_code):
        """
        Auth code has to be taken by visting this long url in browser each time we have to manually authorize meaning we don't have a refresh token.
        'https://www.bookingsync.com/oauth/authorize?client_id=f4954a04b5987e96e9fb99b4ab04f8c2b47d7902c32feb63a63a220d04727d64&scope=bookings_read%20rates_write%20rentals_read%20bookings_write%20rentals_write%20clients_write%20payments_read%20inbox_write&response_type=code&redirect_uri=urn:ietf:wg:oauth:2.0:oob'
        Subseqent authorizations don't require auth code because they use refresh token.
        """
        data = {
            "code": auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        }

        return self.authorize(data)

    def refreshAuth(self, refresh_token):
        data = {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
            "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        }

        return self.authorize(data)

    """
    Below are convienient wrappers for requests lib that automatically
    include auth token in request.
    """

    def get(self, endpoint):
        url = f"https://www.bookingsync.com/api/v3{endpoint}"
        return self.session.get(url, headers=self.getDefaultHeaders())

    def delete(self, endpoint):
        url = f"https://www.bookingsync.com/api/v3{endpoint}"
        return self.session.delete(url, headers=self.getDefaultHeaders())

    def post(self, endpoint, json):
        url = f"https://www.bookingsync.com/api/v3{endpoint}"
        return self.session.post(url, headers=self.getDefaultHeaders(), json=json)

    def put(self, endpoint, json):
        url = f"https://www.bookingsync.com/api/v3{endpoint}"
        return self.session.put(url, headers=self.getDefaultHeaders(), json=json)

    @staticmethod
    def print_json(data):
        print(json.dumps(data, indent=4))


if __name__ == "__main__":
    api = API("135b7da8ae141031fead790513828f29cee8410e97d430cd9fdf2aedaf349743")
    """
    Prints the number of requests that can be made. Resets each hour up to 1000.
    """
    headers = api.get("/rentals").headers
    print(headers["x-ratelimit-remaining"])
