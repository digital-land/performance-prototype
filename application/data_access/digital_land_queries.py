import logging
import urllib.parse

from application.caching import get
from application.utils import create_dict, yesterday, index_by
from application.data_access.sql_helpers import (
    generate_sql_where_str,
    prepare_query_str,
)

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
        query_lines.append("WHERE dataset.dataset = '{}'".format(dataset))
    query_lines.append("GROUP BY dataset.dataset")
    query_str = " ".join(query_lines)
    query = urllib.parse.quote(query_str)
    url = f"{DATASETTE_URL}/{DATABASE_NAME}.json?sql={query}"
    # logger.info("get_datasets: %s", url)
    print("get_datasets: {}".format(url))
    result = get(url, format="json")

    if dataset:
        return create_dict(result["columns"], result["rows"][0])
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


def fetch_sources(limit=100, filter=None, include_blanks=False, concat_pipelines=True):
    params = ""
    limit_str = ""
    where_clause = ""

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

    # handle concat of pipelines for each source
    group_pipeline_strs = "source_pipeline.pipeline"
    group_by = ""
    if concat_pipelines:
        group_pipeline_strs = (
            "GROUP_CONCAT(DISTINCT source_pipeline.pipeline) AS pipeline"
        )
        group_by = ("GROUP BY source.source",)

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
        group_pipeline_strs,
        "FROM",
        "source",
        "INNER JOIN source_pipeline ON source.source = source_pipeline.source",
        "INNER JOIN organisation ON source.organisation = organisation.organisation",
        "INNER JOIN endpoint ON source.endpoint = endpoint.endpoint"
        if filter and "endpoint_" in filter.keys()
        else "",
        where_clause,
        group_by,
        "ORDER BY source.start_date DESC",
        limit_str,
    ]
    query_str = " ".join(query_lines)
    query = urllib.parse.quote(query_str)
    url = f"{DATASETTE_URL}/digital-land.json?sql={query}{params}"

    print(url)
    result = get(url, format="json")
    return [create_dict(result["columns"], row) for row in result["rows"]], url.replace(
        "digital-land.json?sql", "digital-land?sql"
    )


# def fetch_sources_by_organisation(organisation):
#     query_lines = [
#         "SELECT",
#         "source.source,",
#         "source.organisation,",
#         "organisation.name,",
#         "source.endpoint,",
#         "source.documentation_url,",
#         "source.entry_date,",
#         "source.start_date," "source.end_date,",
#         "source_pipeline.pipeline",
#         "FROM",
#         "source",
#         "INNER JOIN source_pipeline ON source.source = source_pipeline.source",
#         "INNER JOIN organisation ON source.organisation = organisation.organisation",
#         "WHERE",
#         f"source.organisation = '{organisation}'",
#         "ORDER BY",
#         "source.start_date DESC",
#     ]
#     query_str = " ".join(query_lines)
#     query = urllib.parse.quote(query_str)
#     url = f"{DATASETTE_URL}/{DATABASE_NAME}.json?sql={query}"
#     logger.info(f"get_sources_by_organisation: {url}")
#     print(f"get_sources_by_organisation: {url}")
#     result = get(url, format="json")
#     return [create_dict(result["columns"], row) for row in result["rows"]]


def fetch_organisation_stats():
    """
    Returns a list of organisations with:
    - end_date if applicable
    - number of resources
    - number of resource without an end-date
    - number of endpoints
    - number of dataset resources are for
    """
    query_lines = [
        "SELECT",
        "organisation.name,",
        "source.organisation,",
        "organisation.end_date AS organisation_end_date,",
        "COUNT(DISTINCT resource.resource) AS resources,",
        "COUNT(",
        "DISTINCT CASE",
        "WHEN resource.end_date == '' THEN resource.resource",
        "WHEN strftime('%Y%m%d', resource.end_date) >= strftime('%Y%m%d', 'now') THEN resource.resource",
        "END",
        ") AS active,",
        "COUNT(DISTINCT resource_endpoint.endpoint) AS endpoints,",
        "COUNT(DISTINCT source_pipeline.pipeline) AS pipelines",
        "FROM",
        "resource",
        "INNER JOIN resource_endpoint ON resource.resource = resource_endpoint.resource",
        "INNER JOIN endpoint ON resource_endpoint.endpoint = endpoint.endpoint",
        "INNER JOIN source ON resource_endpoint.endpoint = source.endpoint",
        "INNER JOIN source_pipeline ON source.source = source_pipeline.source",
        "INNER JOIN organisation ON source.organisation = organisation.organisation",
        "GROUP BY",
        "source.organisation",
    ]
    query = prepare_query_str(query_lines)
    url = f"{DATASETTE_URL}/{DATABASE_NAME}.json?sql={query}"
    print(f"get_organisation_stats: {url}")
    result = get(url, format="json")
    organisations = [create_dict(result["columns"], row) for row in result["rows"]]
    return index_by("organisation", organisations)


def fetch_resources(organisation):
    query_lines = [
        "SELECT",
        "resource.resource,",
        "resource.end_date,",
        "source.source,",
        "resource_endpoint.endpoint,",
        "endpoint.endpoint_url,",
        "source.organisation,",
        "source_pipeline.pipeline",
        "FROM",
        "resource",
        "INNER JOIN resource_endpoint ON resource.resource = resource_endpoint.resource",
        "INNER JOIN endpoint ON resource_endpoint.endpoint = endpoint.endpoint",
        "INNER JOIN source ON resource_endpoint.endpoint = source.endpoint",
        "INNER JOIN source_pipeline ON source.source = source_pipeline.source",
        "WHERE",
        f"source.organisation = '{organisation}'",
    ]
    query = prepare_query_str(query_lines)
    url = f"{DATASETTE_URL}/{DATABASE_NAME}.json?sql={query}"
    print(f"get_resources ({organisation}): {url}")
    return get(url, format="json")


def fetch_resource_count_per_dataset(organisation):
    query_lines = [
        "SELECT",
        "COUNT(DISTINCT resource.resource) AS resources,",
        "COUNT(DISTINCT CASE ",
        "WHEN resource.end_date == '' THEN resource.resource",
        "WHEN strftime('%Y%m%d', resource.end_date) >= strftime('%Y%m%d', 'now') THEN resource.resource",
        "END) AS active_resources,",
        "COUNT(DISTINCT resource_endpoint.endpoint) AS endpoints,",
        "source_pipeline.pipeline AS pipeline",
        "FROM",
        "resource",
        "INNER JOIN resource_endpoint ON resource.resource = resource_endpoint.resource",
        "INNER JOIN endpoint ON resource_endpoint.endpoint = endpoint.endpoint",
        "INNER JOIN source ON resource_endpoint.endpoint = source.endpoint",
        "INNER JOIN source_pipeline ON source.source = source_pipeline.source",
        "INNER JOIN organisation ON source.organisation = organisation.organisation",
        "WHERE",
        f"organisation.organisation = '{organisation}'",
        "GROUP BY",
        "source.organisation,",
        "source_pipeline.pipeline",
    ]
    query = prepare_query_str(query_lines)
    url = f"{DATASETTE_URL}/{DATABASE_NAME}.json?sql={query}"
    print(f"get_resource_count_per_dataset ({organisation}): {url}")
    result = get(url, format="json")
    return [create_dict(result["columns"], row) for row in result["rows"]]


def fetch_organisation_sources(organisation):
    sources, url = fetch_sources(
        filter={"organisation": organisation},
        include_blanks=True,
        concat_pipelines=False,
    )
    return sources


def fetch_source_counts(organisation):
    query_lines = [
        "SELECT",
        "source_pipeline.pipeline AS pipeline,",
        "COUNT(DISTINCT source.source) AS sources,",
        "SUM(CASE WHEN (source.endpoint) is not null and (source.endpoint) != ''",
        " THEN 1 ELSE 0 END)  AS sources_with_endpoint",
        "FROM",
        "source",
        "INNER JOIN source_pipeline ON source.source = source_pipeline.source",
        "WHERE",
        f"source.organisation = '{organisation}'",
        "GROUP BY",
        "source_pipeline.pipeline",
    ]
    query = prepare_query_str(query_lines)
    url = f"{DATASETTE_URL}/{DATABASE_NAME}.json?sql={query}"
    print(f"get_source_counts ({organisation}): {url}")
    result = get(url, format="json")
    return [create_dict(result["columns"], row) for row in result["rows"]]
