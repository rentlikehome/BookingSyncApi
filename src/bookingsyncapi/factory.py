import yaml
import pathlib
import traceback

from bookingsyncapi.api import API


class YAMLApiFactory:
    def __init__(self, config_filepath):
        self.config_filepath = config_filepath

        with open(config_filepath, "r") as f:
            self.config = yaml.safe_load(f)

    def get_creds_path(self, account_id):
        account = self.config["accounts"][account_id]

        if not account["creds_dir"]:
            creds_path = (
                pathlib.Path(self.config_filepath).parent.resolve()
                / f"{account_id}.json"
            )
        else:
            creds_path = pathlib.Path(account["creds_dir"]) / f"{account_id}.json"

        return creds_path

    def get_api(self, account_id):
        account = self.config["accounts"][account_id]

        return API(
            account["client_id"],
            account["client_secret"],
            self.get_creds_path(account_id),
        )

    def authorize_api(self, account_id):
        account = self.config["accounts"][account_id]

        print(f"Manual authorization for account {account.get('name', account_id)}")

        API.manual_authorization(
            account["client_id"],
            account["client_secret"],
            self.get_creds_path(account_id),
            account["scope"],
        )

    def authorize_all(self):
        for account_id in self.config["accounts"].keys():
            try:
                self.authorize_api(account_id)
            except Exception:
                traceback.print_exc()


if __name__ == "__main__":
    pass
