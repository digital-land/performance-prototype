import logging
from application.data_access.db import Database
from application.factory import digital_land_db_path
from application.utils import create_dict, yesterday, index_by
from application.data_access.sql_helpers import (
    generate_sql_where_str,
)

logger = logging.getLogger(__name__)

#
# DATASETTE_URL = "https://datasette.digital-land.info"
# DATABASE_NAME = "digital-land"


def fetch_datasets(filter=None):
    where_clause = ""
    if filter:
        where_clause = generate_sql_where_str(
            filter,
            {
                "active": "dataset_active",  # not currently available
                "dataset": "dataset.dataset",
                "theme": "dataset_theme.theme",
            },
        )
    query_lines = [
        "SELECT",
        "dataset.*,",
        "GROUP_CONCAT(dataset_theme.theme, ';') AS themes",
        "FROM dataset",
        "INNER JOIN dataset_theme ON dataset.dataset = dataset_theme.dataset",
        where_clause,
        "GROUP BY dataset.dataset",
    ]

    query_str = " ".join(query_lines)

    with Database(digital_land_db_path) as db:
        if filter:
            rows = db.execute(query_str, filter).fetchall()
        else:
            rows = db.execute(query_str).fetchall()

    columns = rows[0].keys() if rows else []
    return [create_dict(columns, row) for row in rows]


def fetch_sources(
    limit=100,
    filter=None,
    include_blanks=False,
    only_blanks=False,
    concat_pipelines=True,
):
    limit_str = ""
    where_clause = ""

    # handle limit
    if limit:
        limit_str = "limit {}".format(limit)

    # handle any filters
    if filter:
        where_clause = generate_sql_where_str(
            filter,
            {
                "organisation": "source.organisation",
                "endpoint_": "endpoint.endpoint",
                "source": "source.source",
            },
        )

    if only_blanks:
        where_clause = (
            where_clause
            + ("WHERE " if where_clause == "" else " AND ")
            + 'source.endpoint == ""'
        )
    else:
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
        group_by = "GROUP BY source.source"

    query_lines = [
        "SELECT",
        "source.source,",
        "source.organisation,",
        "organisation.name,",
        "source.endpoint,",
        "" if only_blanks or include_blanks else "endpoint.endpoint_url,",
        "source.documentation_url,",
        "source.entry_date,",
        "source.start_date,",
        "source.end_date,",
        group_pipeline_strs,
        "FROM",
        "source",
        "INNER JOIN source_pipeline ON source.source = source_pipeline.source",
        "INNER JOIN organisation ON source.organisation = organisation.organisation",
        ""
        if only_blanks or include_blanks
        else "INNER JOIN endpoint ON source.endpoint = endpoint.endpoint",
        where_clause,
        group_by,
        "ORDER BY source.start_date DESC",
        limit_str,
    ]
    query_str = " ".join(query_lines)

    with Database(digital_land_db_path) as db:
        if filter:
            rows = db.execute(query_str, filter).fetchall()
        else:
            rows = db.execute(query_str).fetchall()

    columns = rows[0].keys() if rows else []

    # return empty query_url - not sure where used?
    query_url = ""

    return [create_dict(columns, row) for row in rows], query_url


def fetch_publishers():
    query_lines = [
        "SELECT",
        "source.organisation,",
        "organisation.name,",
        "organisation.end_date AS organisation_end_date,",
        "SUM(CASE WHEN (source.endpoint) is not null and (source.endpoint) != '' THEN 1 ELSE 0 END)  AS sources_with_endpoint",  # noqa
        "FROM",
        "source",
        "INNER JOIN organisation ON source.organisation = organisation.organisation",
        "GROUP BY",
        "source.organisation",
    ]
    sql = " ".join(query_lines)
    with Database(digital_land_db_path) as db:
        rows = db.execute(sql).fetchall()
    columns = rows[0].keys() if rows else []
    organisations = [create_dict(columns, row) for row in rows]
    return index_by("organisation", organisations)


def fetch_publisher_coverage(dataset=None):
    query_lines = [
        "SELECT",
        "count(DISTINCT source.organisation) AS total,",
        "COUNT(",
        "DISTINCT CASE",
        "WHEN source.endpoint != '' THEN source.organisation",
        "END",
        ") AS active",
        "FROM",
        "source",
        "INNER JOIN source_pipeline on source.source = source_pipeline.source",
        "WHERE",
        "source.organisation != ''",
        f" AND source_pipeline.pipeline = '{dataset}'" if dataset else "",
        "ORDER BY",
        "source.source",
    ]
    sql = " ".join(query_lines)
    with Database(digital_land_db_path) as db:
        rows = db.execute(sql).fetchall()
    columns = rows[0].keys() if rows else []
    return [create_dict(columns, row) for row in rows]


# def f_orgs():
#     query = urllib.parse.quote(
#         "select name, organisation from organisation order by organisation"
#     )
#     url = f"{DATASETTE_URL}/{DATABASE_NAME}.json?sql={query}"
#     result = get(url, format="json")
#     sql = "SELECT name, organisation FROM organisation ORDER BY organisation"
#     with Database(sqlite_db_path) as db:
#         rows = db.execute(sql).fetchall()
#     columns = rows[0].keys() if rows else []
#     # return [create_dict(columns, row) for row in rows]
#     return [{"text": o[0], "value": o[1]} for o in result["rows"]]


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
    sql = " ".join(query_lines)
    with Database(digital_land_db_path) as db:
        rows = db.execute(sql).fetchall()
    columns = rows[0].keys() if rows else []
    organisations = [create_dict(columns, row) for row in rows]
    return index_by("organisation", organisations)


# should replace fetch_organisation_stats
def fetch_publisher_stats(dataset):
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
        ") AS active_resources,",
        "COUNT(DISTINCT resource_endpoint.endpoint) AS endpoints,",
        "COUNT(DISTINCT source.source) AS sources,",
        "COUNT(",
        "DISTINCT CASE",
        "WHEN source.end_date == '' THEN source.source",
        "WHEN strftime('%Y%m%d', source.end_date) >= strftime('%Y%m%d', 'now') THEN source.source",
        "END",
        ") AS active_sources,",
        "MAX(resource.start_date),",
        "Cast (",
        "(",
        "julianday('now') - julianday(MAX(resource.start_date))",
        ") AS INTEGER",
        ") as days_since_update",
        "FROM",
        "resource",
        "INNER JOIN resource_endpoint ON resource.resource = resource_endpoint.resource",
        "INNER JOIN endpoint ON resource_endpoint.endpoint = endpoint.endpoint",
        "INNER JOIN source ON resource_endpoint.endpoint = source.endpoint",
        "INNER JOIN source_pipeline ON source.source = source_pipeline.source",
        "INNER JOIN organisation ON source.organisation = organisation.organisation",
        "WHERE",
        f"source_pipeline.pipeline = '{dataset}'",
        "GROUP BY",
        "source.organisation",
    ]
    sql = " ".join(query_lines)
    with Database(digital_land_db_path) as db:
        rows = db.execute(sql).fetchall()
    columns = rows[0].keys() if rows else []
    organisations = [create_dict(columns, row) for row in rows]
    return index_by("organisation", organisations)


def fetch_resources(filters=None, limit=None):
    limit_str = ""
    if limit:
        limit_str = f"LIMIT {limit}"

    where_clause = ""
    if filters:
        where_clause = generate_sql_where_str(
            filters,
            {
                "organisation": "source.organisation",
                "dataset": "source_pipeline.pipeline",
                "resource": "resource.resource",
                "source": "source.source",
            },
        )

    query_lines = [
        "SELECT",
        "DISTINCT resource.resource,",
        "resource.entry_date,",
        "resource.start_date,",
        "resource.end_date,",
        "source.source,",
        "resource_endpoint.endpoint,",
        "endpoint.endpoint_url,",
        "source.organisation,",
        "source_pipeline.pipeline,",
        "REPLACE(",
        "GROUP_CONCAT(DISTINCT log.content_type),",
        "',',",
        "';'",
        ") AS content_type",
        "FROM",
        "resource",
        "INNER JOIN resource_endpoint ON resource.resource = resource_endpoint.resource",
        "INNER JOIN endpoint ON resource_endpoint.endpoint = endpoint.endpoint",
        "INNER JOIN log ON resource.resource = log.resource",
        "INNER JOIN source ON resource_endpoint.endpoint = source.endpoint",
        "INNER JOIN source_pipeline ON source.source = source_pipeline.source",
        where_clause,
        "GROUP BY",
        "resource.resource",
        "ORDER BY",
        "resource.start_date DESC",
        limit_str,
    ]

    query_str = " ".join(query_lines)
    with Database(digital_land_db_path) as db:
        if filters:
            rows = db.execute(query_str, filters).fetchall()
        else:
            rows = db.execute(query_str).fetchall()
    return rows


def fetch_resource(resource_hash):
    # seems like overkill...
    query_lines = [
        "SELECT",
        "DISTINCT resource.resource,",
        "resource.entry_date,",
        "resource.start_date,",
        "resource.end_date,",
        "resource_organisation.organisation,",
        "organisation.name,",
        "endpoint.endpoint,",
        "endpoint.endpoint_url,",
        "REPLACE(GROUP_CONCAT(DISTINCT log.content_type), ',', ';') AS content_type,",
        "REPLACE(GROUP_CONCAT(DISTINCT source_pipeline.pipeline), ',', ';') AS pipeline",
        "FROM",
        "resource",
        "INNER JOIN resource_organisation ON resource.resource = resource_organisation.resource",
        "INNER JOIN organisation ON resource_organisation.organisation = organisation.organisation",
        "INNER JOIN resource_endpoint ON resource.resource = resource_endpoint.resource",
        "INNER JOIN endpoint ON resource_endpoint.endpoint = endpoint.endpoint",
        "INNER JOIN log ON resource.resource = log.resource",
        "INNER JOIN source ON source.endpoint = resource_endpoint.endpoint",
        "INNER JOIN source_pipeline ON source.source = source_pipeline.source",
        "WHERE resource.resource = :resource_hash",
        "GROUP BY",
        "endpoint.endpoint",
    ]

    sql = " ".join(query_lines)
    with Database(digital_land_db_path) as db:
        rows = db.execute(sql, {"resource_hash": resource_hash}).fetchall()

    columns = rows[0].keys() if rows else []

    return [create_dict(columns, row) for row in rows]


def fetch_active_resources(pipeline):
    # probably doesn't need to be it's own query but it was causing a headache
    query_lines = [
        "SELECT",
        "resource.resource,",
        "resource_organisation.organisation,",
        "resource.end_date,",
        "resource.entry_date,",
        "resource.start_date,",
        "source_pipeline.pipeline",
        "FROM",
        "resource",
        "INNER JOIN resource_endpoint ON resource.resource = resource_endpoint.resource",
        "INNER JOIN resource_organisation ON resource.resource = resource_organisation.resource",
        "INNER JOIN source ON resource_endpoint.endpoint = source.endpoint",
        "INNER JOIN source_pipeline ON source.source = source_pipeline.source",
        "WHERE",
        "source_pipeline.pipeline = :pipeline",
        "AND (resource.end_date == '' OR strftime('%Y%m%d', resource.end_date) >= strftime('%Y%m%d', 'now'))",
        "ORDER BY",
        "resource.end_date ASC",
    ]
    sql = " ".join(query_lines)
    with Database(digital_land_db_path) as db:
        rows = db.execute(sql, {"pipeline": pipeline}).fetchall()

    columns = rows[0].keys() if rows else []
    return [create_dict(columns, row) for row in rows]


def fetch_total_resource_count():
    sql = "select count(distinct resource) from resource"
    with Database(digital_land_db_path) as db:
        result = db.execute(sql).fetchone()
    return result[0] if result else 0


def fetch_latest_resource(dataset=None):
    try:
        if dataset:
            results = fetch_resources(filters={"dataset": dataset}, limit=1)
        else:
            results = fetch_resources(limit=1)

        if len(results["rows"]):
            return create_dict(results["columns"], results["rows"][0])

        return None
    except Exception as e:
        print(e)
        return {"error": "Problem retrieving data from datasette"}


def fetch_resource_count_per_dataset(organisation=None):
    query_lines = [
        "SELECT",
        "COUNT(DISTINCT resource.resource) AS resources,",
        "COUNT(DISTINCT CASE ",
        "WHEN resource.end_date == '' THEN resource.resource",
        "WHEN strftime('%Y%m%d', resource.end_date) >= strftime('%Y%m%d', 'now') THEN resource.resource",
        "END) AS active_resources,",
        "COUNT(DISTINCT CASE",
        "WHEN resource.end_date != ''",
        "AND strftime('%Y%m%d', resource.end_date) <= strftime('%Y%m%d', 'now') THEN resource.resource",
        "END",
        ") AS ended_resources,",
        "COUNT(DISTINCT resource_endpoint.endpoint) AS endpoints,",
        "source_pipeline.pipeline AS pipeline",
        "FROM",
        "resource",
        "INNER JOIN resource_endpoint ON resource.resource = resource_endpoint.resource",
        "INNER JOIN endpoint ON resource_endpoint.endpoint = endpoint.endpoint",
        "INNER JOIN source ON resource_endpoint.endpoint = source.endpoint",
        "INNER JOIN source_pipeline ON source.source = source_pipeline.source",
        "INNER JOIN organisation ON source.organisation = organisation.organisation",
        f"WHERE organisation.organisation = '{organisation}'" if organisation else "",
        "GROUP BY",
        "source.organisation," if organisation else "",
        "source_pipeline.pipeline",
    ]
    sql = " ".join(query_lines)
    with Database(digital_land_db_path) as db:
        rows = db.execute(sql).fetchall()
    columns = rows[0].keys() if rows else []
    return [create_dict(columns, row) for row in rows]


def fetch_organisation_sources(organisation):
    sources, url = fetch_sources(
        filter={"organisation": organisation},
        include_blanks=True,
        concat_pipelines=False,
    )
    return sources


def fetch_overall_source_counts(groupby=None):
    groupby_options = {
        "organisation": "organisation.organisation",
        "dataset": "source_pipeline.pipeline",
    }
    query_lines = [
        "SELECT",
        "source_pipeline.pipeline,",
        "organisation.organisation, organisation.name, organisation.end_date,"
        if groupby == "organisation"
        else "",
        "COUNT(DISTINCT source.source) AS sources,",
        "SUM(",
        "CASE",
        "WHEN (source.endpoint) is not null",
        "and (source.endpoint) != '' THEN 1",
        "ELSE 0",
        "END",
        ") AS sources_with_endpoint,",
        "SUM(",
        "CASE",
        "WHEN (source.endpoint) is not null",
        "and (source.endpoint) != '' and ((source.documentation_url) is null",
        "or (source.documentation_url) == '') THEN 1",
        "ELSE 0",
        "END",
        ") AS sources_missing_document_url",
        "FROM",
        "source",
        "INNER JOIN source_pipeline on source.source = source_pipeline.source",
        "INNER JOIN organisation on source.organisation = organisation.organisation",
        f"GROUP BY {groupby_options.get(groupby)}"
        if groupby and groupby_options.get(groupby)
        else "",
    ]
    sql = " ".join(query_lines)
    with Database(digital_land_db_path) as db:
        rows = db.execute(sql).fetchall()
    columns = rows[0].keys() if rows else []
    return [create_dict(columns, row) for row in rows]


def fetch_organisation_source_counts(organisation, by_dataset=True):
    query_lines = [
        "SELECT",
        "source_pipeline.pipeline AS pipeline,",
        "organisation.organisation,",
        "organisation.name,",
        "COUNT(DISTINCT source.source) AS sources,",
        "SUM(CASE WHEN (source.endpoint) is not null and (source.endpoint) != ''",
        " THEN 1 ELSE 0 END)  AS sources_with_endpoint",
        "FROM",
        "source",
        "INNER JOIN source_pipeline ON source.source = source_pipeline.source",
        "INNER JOIN organisation ON source.organisation = organisation.organisation",
        "WHERE",
        f"source.organisation = '{organisation}'",
        "GROUP BY source_pipeline.pipeline" if by_dataset else "",
    ]
    sql = " ".join(query_lines)
    with Database(digital_land_db_path) as db:
        rows = db.execute(sql).fetchall()
    columns = rows[0].keys() if rows else []
    return [create_dict(columns, row) for row in rows]


def fetch_source_counts(organisation=None, **kwargs):
    if organisation:
        return fetch_organisation_source_counts(organisation, **kwargs)
    return fetch_overall_source_counts(**kwargs)


def fetch_latest_collector_run_date(dataset=None):
    where_clause = ""
    if dataset:
        where_clause = f"WHERE source_pipeline.pipeline = '{dataset}'"
    query_lines = [
        "SELECT",
        "source_pipeline.pipeline,",
        "MAX(log.entry_date) AS latest_attempt",
        "FROM",
        "source",
        "INNER JOIN source_pipeline ON source.source = source_pipeline.source",
        "INNER JOIN log ON source.endpoint = log.endpoint",
        where_clause,
        "GROUP BY",
        "source_pipeline.pipeline",
    ]
    sql = " ".join(query_lines)
    with Database(digital_land_db_path) as db:
        rows = db.execute(sql).fetchall()
    columns = rows[0].keys() if rows else []
    return index_by("pipeline", [create_dict(columns, row) for row in rows])


def fetch_table(tablename):
    sql = f"SELECT * FROM {tablename}"
    with Database(digital_land_db_path) as db:
        rows = db.execute(sql).fetchall()
    columns = rows[0].keys() if rows else []
    return [create_dict(columns, row) for row in rows]


def fetch_themes():
    return fetch_table("theme")


def fetch_typologies():
    return fetch_table("typology")


##########################################
# Queries using log table as primary table
##########################################


def fetch_logs(filters=None, group_by=None):
    where_str = ""
    if filters:
        where_str = "WHERE " + " AND ".join(
            [f"log.{fil} = '{val}'" for fil, val in filters.items()]
        )

    group_by_str = ""
    if group_by:
        group_by_str = f"GROUP BY log.{group_by}"

    query_lines = ["SELECT", "log.*", "FROM", "log", where_str, group_by_str]

    sql = " ".join(query_lines)
    with Database(digital_land_db_path) as db:
        rows = db.execute(sql).fetchall()
    columns = rows[0].keys() if rows else []
    return [create_dict(columns, row) for row in rows]


def fetch_log_summary(date=yesterday(string=True)):
    query_lines = [
        "SELECT",
        "entry_date,",
        "status,",
        "COUNT(DISTINCT endpoint) AS count",
        "FROM",
        "log",
        "WHERE",
        "entry_date = :date",
        "GROUP BY",
        "status",
    ]
    sql = " ".join(query_lines)
    with Database(digital_land_db_path) as db:
        rows = db.execute(sql, {"date": date}).fetchall()
    columns = rows[0].keys() if rows else []
    return [create_dict(columns, row) for row in rows]


def fetch_content_type_counts(dataset=None):
    joins = []
    where_str = None
    if dataset:
        joins = [
            "INNER JOIN source ON log.endpoint = source.endpoint",
            "INNER JOIN source_pipeline on source.source = source_pipeline.source",
        ]
        where_str = f"source_pipeline.pipeline = '{dataset}'"

    query_lines = [
        "SELECT",
        "log.content_type,",
        "count(DISTINCT log.resource) AS resource_count",
        "FROM",
        "log",
        *joins,
        "WHERE " + where_str if where_str is not None else "",
        "GROUP BY",
        "log.content_type",
    ]

    sql = " ".join(query_lines)
    with Database(digital_land_db_path) as db:
        rows = db.execute(sql).fetchall()
    columns = rows[0].keys() if rows else []
    return [create_dict(columns, row) for row in rows]


def get_source_counts(pipeline=None):
    # returns high level source counts
    sql = """
            SELECT
              COUNT(DISTINCT source.source) AS sources,
              COUNT(
                DISTINCT CASE
                  WHEN source.end_date == '' THEN source.source
                  WHEN strftime('%Y%m%d', source.end_date) >= strftime('%Y%m%d', 'now') THEN source.source
                END
              ) AS active,
              COUNT(
                DISTINCT CASE
                  WHEN end_date != '' THEN source.source
                  WHEN strftime('%Y%m%d', source.end_date) <= strftime('%Y%m%d', 'now') THEN source.source
                END
              ) AS inactive,
              COUNT(DISTINCT source_pipeline.pipeline) AS pipelines
            FROM
              source
              INNER JOIN source_pipeline ON source.source = source_pipeline.source
            WHERE source.endpoint != '' """

    if pipeline:
        sql += " AND source_pipeline.pipeline = :pipeline"

    with Database(digital_land_db_path) as db:
        if pipeline:
            rows = db.execute(sql, {"pipeline": pipeline}).fetchall()
        else:
            rows = db.execute(sql).fetchall()

    columns = rows[0].keys() if rows else []
    return [create_dict(columns, row) for row in rows]


def get_monthly_source_counts(pipeline=None):

    with Database(digital_land_db_path) as db:

        if pipeline:
            sql = """SELECT
                  strftime('%Y-%m', source.start_date) AS yyyy_mm,
                  count(distinct source.source) AS count
                FROM
                  source
                  INNER JOIN source_pipeline ON source.source = source_pipeline.source
                WHERE
                  source.start_date != ""
                  AND source_pipeline.pipeline = :pipeline
                GROUP BY
                  yyyy_mm
                ORDER BY
                  yyyy_mm"""

            rows = db.execute(sql, {"pipeline": pipeline}).fetchall()

        else:
            sql = """SELECT
                    strftime('%Y-%m', source.start_date) as yyyy_mm, 
                    count(distinct source.source) as count
                FROM source
                WHERE source.start_date != ""
                GROUP BY yyyy_mm
                ORDER BY yyyy_mm"""

            rows = db.execute(sql).fetchall()

    columns = rows[0].keys() if rows else []
    return [create_dict(columns, row) for row in rows]
