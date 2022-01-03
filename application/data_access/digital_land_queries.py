import logging
import urllib.parse

from application.caching import get
from application.utils import create_dict, yesterday

logger = logging.getLogger(__name__)

DATASETTE_URL = "https://datasette.digital-land.info"
DATABASE_NAME = "digital-land"


def fetch_datasets(dataset=None):
    query_lines = [
        "SELECT",
        "dataset.*,",
        "GROUP_CONCAT(dataset_theme.theme, ';') AS themes",
        "FROM dataset",
        "INNER JOIN dataset_theme ON dataset.dataset = dataset_theme.dataset",
    ]
    if dataset:
        query_lines.append("WHERE dataset.dataset = '{dataset}'")
    query_lines.append("GROUP BY dataset.dataset")
    query_str = " ".join(query_lines)
    query = urllib.parse.quote(query_str)
    url = f"{DATASETTE_URL}/{DATABASE_NAME}.json?sql={query}"
    logger.info("get_datasets: %s", url)
    result = get(url, format="json")
    return [create_dict(result["columns"], row) for row in result["rows"]]


def fetch_log_summary(date=yesterday(string=True)):
    query_lines = [
        "SELECT",
        "entry_date,",
        "status,",
        "COUNT(DISTINCT endpoint) AS count",
        "FROM",
        "log",
        "WHERE",
        f"entry_date = '{date}'",
        "GROUP BY",
        "status",
    ]
    query_str = " ".join(query_lines)
    query = urllib.parse.quote(query_str)
    url = f"{DATASETTE_URL}/{DATABASE_NAME}.json?sql={query}"
    logger.info("get_log_summary: %s", url)
    result = get(url, format="json")
    return [create_dict(result["columns"], row) for row in result["rows"]]
