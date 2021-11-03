import dotenv
import argparse
import pathlib
from bookingsyncapi.factory import YAMLApiFactory


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help="YAML config file", type=pathlib.Path)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--account', help="Account ID from config file")
    group.add_argument('--all', help="Authorize all accounts in config file", action="store_true")

    args = parser.parse_args()

    config = args.config
    if not config:
        config = dotenv.dotenv_values()["BOOKINGSYNCAPI_CONFIG_FILE"]

    if args.all:
        YAMLApiFactory(config).authorize_all()
    else:
        YAMLApiFactory(config).authorize_api(args.account)
