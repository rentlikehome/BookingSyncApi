import pathlib
import argparse
import dotenv
import logging
from bookingsyncapi.factory import YAMLApiFactory
from bookingsyncapi.export import export_endpoint


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simple commandline interface for exporting from BSync.",
        epilog="Example usage (exporting hosts): python3 cmd_export.py --account 14030 --endpoint '/hosts' --out hosts.xlsx",
    )

    parser.add_argument("--config", help="YAML config file", type=pathlib.Path)
    parser.add_argument("--account", help="Account ID from config file", required=True)
    parser.add_argument(
        "--out",
        help="Output file with .xlsx extension",
        type=pathlib.Path,
        required=True,
    )
    parser.add_argument(
        "--endpoint", help="BookingSync API endpoint e.g. '/rentals'", required=True
    )

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    config = args.config
    if not config:
        config = dotenv.dotenv_values()["BOOKINGSYNCAPI_CONFIG_FILE"]

    api = YAMLApiFactory(config).get_api(args.account)

    df = export_endpoint(api, args.endpoint)

    df.to_excel(args.out)
