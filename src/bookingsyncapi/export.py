import pandas
import urllib.parse
import logging

logger = logging.getLogger(__name__)


def paginate_endpoint(endpoint, pages):
    endpoint_parts = urllib.parse.urlparse(endpoint)._asdict()
    endpoint_query = urllib.parse.parse_qs(endpoint_parts["query"])

    for page in range(1, pages + 1):
        page_query = {"page": page}

        full_query = endpoint_query | page_query
        endpoint_parts["query"] = urllib.parse.urlencode(full_query)

        paginated_endpoint = urllib.parse.urlunparse(endpoint_parts.values())

        yield paginated_endpoint


def export_endpoint(api, endpoint, cutoff_page=float("inf"), max_level=3):
    """
    Args:
        pages_cutoff (int): Number of page after which the export will stop.
            Defaults to inf meaning all pages.
        max_level (int): Max number of levels(depth of dict) to normalize.
            If None, normalizes all levels.
    """

    response = api.get(endpoint).json()
    data_key = list(response.keys())[1]

    pages = int(response["meta"]["X-Total-Pages"])
    pages = cutoff_page if pages > cutoff_page else pages

    logger.info(f"Exporting {pages} pages from {endpoint}.")

    df = pandas.DataFrame()
    for endpoint in paginate_endpoint(endpoint, pages):
        response = api.get(endpoint).json()
        data = response[data_key]
        page_df = pandas.json_normalize(data, max_level=max_level)
        df = df.append(page_df, ignore_index=True)

    return df
