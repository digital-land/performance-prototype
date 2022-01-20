import logging
import urllib.parse

from application.caching import get
from application.utils import create_dict, yesterday
from application.data_access.sql_helpers import generate_sql_where_str

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


def fetch_sources(limit=100, filter=None, include_blanks=False):
    params = ""
    limit_str = ""
    where_clauses = ""

    # handle limit
    if limit:
        limit_str = "limit {}".format(limit)

    # handle any filters
    if filter:
        where_clause, params = generate_sql_where_str(
            filter,
            {
                "organisation": "source.organisation",
                "endpoint_": "endpoint.endpoint",
                "source": "source.source",
            },
        )

    # handle case where blanks also included
    if not include_blanks:
        where_clause = (
            where_clause
            + ("WHERE " if where_clause == "" else " AND ")
            + 'source.endpoint != ""'
        )

    query_lines = [
        "SELECT",
        "source.source,",
        "source.organisation,",
        "organisation.name,",
        "source.endpoint,",
        "source.documentation_url,",
        "source.entry_date,",
        "source.start_date,",
        "source.end_date,",
        "GROUP_CONCAT(DISTINCT source_pipeline.pipeline) AS pipeline",
        "FROM",
        "source",
        "INNER JOIN source_pipeline ON source.source = source_pipeline.source",
        "INNER JOIN organisation ON source.organisation = organisation.organisation",
        "INNER JOIN endpoint ON source.endpoint = endpoint.endpoint"
        if "endpoint_" in filter.keys()
        else "",
        where_clause,
        "GROUP BY",
        "source.source",
        "ORDER BY source.start_date DESC",
        limit_str,
    ]
    query_str = " ".join(query_lines)
    query = urllib.parse.quote(query_str)
    url = f"{DATASETTE_URL}/digital-land.json?sql={query}{params}"

    print(url)
    result = get(url, format="json")
    return [create_dict(result["columns"], row) for row in result["rows"]]
