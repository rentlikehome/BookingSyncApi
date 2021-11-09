import requests, json, csv
from datetime import datetime, timedelta


import pathlib
import json

import logging

logger = logging.getLogger(__name__)

class AuthorizationError(Exception):
    pass

class API:
    def __init__(self, client_id, client_secret, creds_path):
        """
        client_id and client_secret are taken from here:
        https://www.bookingsync.com/en/partners/applications/1011/edit
        """
        self.session = requests.Session()

        self.client_id = client_id
        self.client_secret = client_secret
        self.creds_path = creds_path

        try:
            with open(creds_path, "r") as f:
                creds = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            raise AuthorizationError(f"Couldn't load creds from {creds_path}")

        self.access_token = creds.get("access_token", None)
        refresh_token = creds.get("refresh_token", None)

        if not self.access_token or not refresh_token:
            raise AuthorizationError(f"Creds file {creds_path} is missing tokens")

        if not self.is_authorized():
            self.access_token = self.refresh_access_token(refresh_token)

    def __del__(self):
        self.session.close()

    def get_default_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
        }

    def is_authorized(self):
        response = self.get("/bookings")
        return response.status_code != 401

    @staticmethod
    def authorize(auth, data, creds_path):
        token_url = "https://www.bookingsync.com/oauth/token"

        response = requests.post(
            token_url,
            data=data,
            verify=False,
            allow_redirects=False,
            auth=auth,
        )
        # print(response.text)

        if response.status_code == 401:
            raise AuthorizationError(f"Failed to authorize: {response.text}")

        tokens = response.json() 

        with open(creds_path, "w") as f:
            json.dump(tokens, f, indent=4)

        return tokens["access_token"]

    @classmethod
    def manual_authorization(cls, client_id, client_secret, creds_path, scope):
        """
        Auth code has to be taken by visting this long url in browser each time we have to manually authorize meaning we don't have a refresh token.
        'https://www.bookingsync.com/oauth/authorize?client_id=f4954a04b5987e96e9fb99b4ab04f8c2b47d7902c32feb63a63a220d04727d64&scope=bookings_read%20rates_write%20rentals_read%20bookings_write%20rentals_write%20clients_write%20payments_read%20inbox_write&response_type=code&redirect_uri=urn:ietf:wg:oauth:2.0:oob'
        Subseqent authorizations don't require auth code because they use refresh token.
        """
        
        if pathlib.Path(creds_path).is_file():
            raise Exception(f"Creds file {creds_path} already exists. Aborting manual authorization...")


        base_url = "https://www.bookingsync.com/oauth/authorize"
        params = {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
            "scope": " ".join(scope)
        }

        import urllib
        url = base_url + "?" + urllib.parse.urlencode(params)
        
        print("Please visit following URL to obtain authorization code:")
        print(url)
        print("Input authorization code:")
        auth_code = input()

        data = {
            "code": auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        }

        auth = (client_id, client_secret)

        return cls.authorize(auth, data, creds_path)

    def refresh_access_token(self, refresh_token):
        data = {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
            "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        }
        auth = (self.client_id, self.client_secret)
        return self.authorize(auth, data, self.creds_path)

    """
    Below are convienient wrappers for requests lib that automatically
    include auth token in request.
    """

    def get(self, endpoint):
        url = f"https://www.bookingsync.com/api/v3{endpoint}"
        return self.session.get(url, headers=self.get_default_headers())

    def delete(self, endpoint):
        url = f"https://www.bookingsync.com/api/v3{endpoint}"
        return self.session.delete(url, headers=self.get_default_headers())

    def post(self, endpoint, json):
        url = f"https://www.bookingsync.com/api/v3{endpoint}"
        return self.session.post(url, headers=self.get_default_headers(), json=json)

    def put(self, endpoint, json):
        url = f"https://www.bookingsync.com/api/v3{endpoint}"
        return self.session.put(url, headers=self.get_default_headers(), json=json)

    def get_remaining_requests(self):
        headers = self.get("/rentals").headers
        return headers["x-ratelimit-remaining"]

    @staticmethod
    def print_json(data):
        print(json.dumps(data, indent=4))


if __name__ == "__main__":
    # api = API("135b7da8ae141031fead790513828f29cee8410e97d430cd9fdf2aedaf349743")
    API.manual_authorization("client_id_11", "", "creds", ["write", "read"])
