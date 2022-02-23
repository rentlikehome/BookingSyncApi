import time
import requests, json, csv
from datetime import datetime, timedelta
import base64
import hashlib
import hmac
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
        self.URL = "https://www.bookingsync.com/api/v3"
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
        self.refresh_token = creds.get("refresh_token", None)

        if not self.access_token or not self.refresh_token:
            raise AuthorizationError(f"Creds file {creds_path} is missing tokens")

        expires_in = creds.get("expires_in", None)
        created_at = creds.get("created_at", None)

        if not expires_in or not created_at:
            raise AuthorizationError(f"Creds file {creds_path} is missing tokens")

        self.expires_at = created_at + expires_in

        self.refresh_if_expired()

    def __del__(self):
        self.session.close()

    def get_default_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
        }

    def is_expired(self):
        return self.expires_at < int(time.time()) + 1

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
            raise Exception(
                f"Creds file {creds_path} already exists. Aborting manual authorization..."
            )

        base_url = "https://www.bookingsync.com/oauth/authorize"
        params = {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
            "scope": " ".join(scope),
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

    def refresh_access_token(self):
        data = {
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token",
            "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        }
        auth = (self.client_id, self.client_secret)
        self.access_token = self.authorize(auth, data, self.creds_path)

    def refresh_if_expired(self):
        if self.is_expired():
            self.refresh_access_token()

    """
    Below are convienient wrappers for requests lib that automatically
    include auth token in request.
    """

    def get(self, endpoint):
        self.refresh_if_expired()
        return self.session.get(self.URL + endpoint, headers=self.get_default_headers())

    def delete(self, endpoint):
        self.refresh_if_expired()
        return self.session.delete(
            self.URL + endpoint, headers=self.get_default_headers()
        )

    def post(self, endpoint, json):
        self.refresh_if_expired()
        return self.session.post(
            self.URL + endpoint, headers=self.get_default_headers(), json=json
        )

    def put(self, endpoint, json):
        self.refresh_if_expired()
        return self.session.put(
            self.URL + endpoint, headers=self.get_default_headers(), json=json
        )

    def get_remaining_requests(self):
        headers = self.get("/rentals").headers
        return headers["x-ratelimit-remaining"]

    @staticmethod
    def print_json(data):
        print(json.dumps(data, indent=4))

    @staticmethod
    def check_xcontentsig(client_secret, sig, request_body):
        """
        Checks if signature matches the received body.
        This doesn't require being authenticated so we avoid
        making unnecessery requests by making this a static method.

        The signature is calculated accroding to BSync documentation:
        https://developers.bookingsync.com/guides/webhook-subscriptions/

        Args:
            client_secret (str, bytes): client secret indentyfing app. If str is passed
                it is converted to bytes using default encoding.
            sig: signature received in headers, usually "X-Content-Signature" field
            request_body (bytes): request body before serialization to json

        Returns:
            bool: True if signature match, False otherwise.
        """

        if isinstance(client_secret, str):
            client_secret = client_secret.encode()

        encoded_body = list(base64.b64encode(request_body))

        # We have to pad encoded body with newlines every 60 chars
        # and at the end since this is how Ruby, which is used to calculate
        # original sig, does it by default.
        padding_spacing = 60
        new_encoded = b""
        for pos in range(0, len(encoded_body), padding_spacing):
            new_encoded += bytes(encoded_body[pos : pos + padding_spacing]) + b"\n"

        body_sig = hmac.new(
            client_secret, new_encoded, digestmod=hashlib.sha1
        ).hexdigest()

        return hmac.compare_digest(sig, body_sig)


if __name__ == "__main__":
    pass
