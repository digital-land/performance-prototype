from datetime import datetime
from application.data_access.sqlite_db import SqliteDatabase
from application.factory import digital_land_db_path
from application.utils import (
    create_dict,
    index_by,
    months_since,
    month_dict,
    this_month,
    yesterday,
)

from application.data_access.digital_land_queries import (
    get_datasets,
    get_monthly_source_counts,
)


def sql_for_filter(filters, mappings={}):
    if len(filters.keys()) == 0:
        return "", ""
    where_str = "where%0D%0A"
    clauses = []
    param_str = ""
    for filter, value in filters.items():
        column = filter
        if filter in mappings.keys():
            column = mappings[filter]
        clauses.append("{}+LIKE+%3A{}%0D%0A".format(column, filter))
        param = "&{}={}".format(filter, value)
        param_str = param_str + param
    return where_str + "AND%0D%0A".join(clauses), param_str


def get_monthly_resource_counts(pipeline=None):

    if not pipeline:

        sql = """SELECT
              strftime('%Y-%m', resource.start_date) AS yyyy_mm,
              count(distinct resource.resource) AS count
            FROM
              resource
            WHERE
              resource.start_date != ""
            GROUP BY
              yyyy_mm
            ORDER BY
              yyyy_mm"""

    else:
        sql = """
            SELECT
              strftime('%Y-%m', resource.start_date) AS yyyy_mm,
              count(distinct resource.resource) AS count
            FROM
              resource
              INNER JOIN resource_endpoint ON resource.resource = resource_endpoint.resource
              INNER JOIN endpoint ON resource_endpoint.endpoint = endpoint.endpoint
              INNER JOIN source ON resource_endpoint.endpoint = source.endpoint
              INNER JOIN source_pipeline ON source.source = source_pipeline.source
            WHERE
              resource.start_date != ""
              AND source_pipeline.pipeline = :pipeline
            GROUP BY
              yyyy_mm
            ORDER BY
              yyyy_mm"""

    with SqliteDatabase(digital_land_db_path) as db:
        if pipeline:
            rows = db.execute(sql, {"pipeline": pipeline}).fetchall()
        else:
            rows = db.execute(sql).fetchall()

    columns = rows[0].keys() if rows else []
    return [create_dict(columns, row) for row in rows]


def get_new_resources(dates=[yesterday(string=True)]):

    if len(dates) == 1:
        sql = f"""SELECT
            DISTINCT resource, start_date
            FROM resource
            WHERE start_date = '{dates[0]}'
            ORDER BY start_date"""
    else:
        sql = """SELECT
                DISTINCT resource, start_date
                FROM resource
                WHERE start_date IN %(dates)s
                ORDER BY start_date
                """ % {
            "dates": tuple(dates)
        }

    with SqliteDatabase(digital_land_db_path) as db:
        rows = db.execute(sql).fetchall()
    return rows


def by_collection(data):
    # used to by pipeline
    by_collection = {}
    for r in data:
        id = r["collection"]["value"]
        name = r["collection"]["label"]
        by_collection.setdefault(id, {"name": name, "source": []})
        by_collection[id]["source"].append(r)
    return by_collection


def get_monthly_counts(pipeline=None):
    source_counts = get_monthly_source_counts(pipeline)
    resource_counts = get_monthly_resource_counts(pipeline)

    # handle if either are empty
    if not bool(source_counts):
        return None

    first_source_month_str = source_counts[0]["yyyy_mm"]
    first_resource_month_str = (
        resource_counts[0]["yyyy_mm"] if bool(resource_counts) else this_month()
    )

    earliest = (
        first_source_month_str
        if first_source_month_str < first_resource_month_str
        else first_resource_month_str
    )
    start_date = datetime.strptime(earliest, "%Y-%m")
    months_since_start = months_since(start_date)
    all_months = month_dict(months_since_start)

    counts = {}
    for k, v in {"resources": resource_counts, "sources": source_counts}.items():
        d = all_months.copy()
        for row in v:
            if row["yyyy_mm"] in d.keys():
                d[row["yyyy_mm"]] = d[row["yyyy_mm"]] + row["count"]
        # needs to be in tuple form
        counts[k] = [(k, v) for k, v in d.items()]
    counts["months"] = list(all_months.keys())
    return counts


def publisher_counts(pipeline):
    # returns resource, active resource, endpoints, sources, active source, latest resource date and days since update

    sql = """
          SELECT
          organisation.name,
          source.organisation,
          organisation.end_date AS organisation_end_date,
          COUNT(DISTINCT resource.resource) AS resources,
          COUNT(
            DISTINCT CASE
              WHEN resource.end_date == '' THEN resource.resource
              WHEN strftime('%Y%m%d', resource.end_date) >= strftime('%Y%m%d', 'now') THEN resource.resource
            END
          ) AS active_resources,
          COUNT(DISTINCT resource_endpoint.endpoint) AS endpoints,
          COUNT(DISTINCT source.source) AS sources,
          COUNT(
            DISTINCT CASE
              WHEN source.end_date == '' THEN source.source
              WHEN strftime('%Y%m%d', source.end_date) >= strftime('%Y%m%d', 'now') THEN source.source
            END
          ) AS active_sources,
          MAX(resource.start_date),
          Cast (
            (
              julianday('now') - julianday(MAX(resource.start_date))
            ) AS INTEGER
          ) AS days_since_update
        FROM
          resource
          INNER JOIN resource_endpoint ON resource.resource = resource_endpoint.resource
          INNER JOIN endpoint ON resource_endpoint.endpoint = endpoint.endpoint
          INNER JOIN source ON resource_endpoint.endpoint = source.endpoint
          INNER JOIN source_pipeline ON source.source = source_pipeline.source
          INNER JOIN organisation ON source.organisation = organisation.organisation
        WHERE
          source_pipeline.pipeline = :pipeline
        GROUP BY
          source.organisation"""

    with SqliteDatabase(digital_land_db_path) as db:
        rows = db.execute(sql, {"pipeline": pipeline}).fetchall()

    columns = rows[0].keys() if rows else []
    organisations = [create_dict(columns, row) for row in rows]

    return index_by("organisation", organisations)


# returns organisation counts per dataset
def publisher_coverage(pipeline=None):

    # TODO handle when pipeline is not None
    sql = """
            SELECT
              source_pipeline.pipeline,
              count(DISTINCT source.organisation) as expected_publishers,
              COUNT(
                DISTINCT CASE
                  WHEN source.endpoint != '' THEN source.organisation
                END
              ) AS publishers
            FROM
              source
              INNER JOIN source_pipeline ON source.source = source_pipeline.source
            GROUP BY
            source_pipeline.pipeline
    """

    with SqliteDatabase(digital_land_db_path) as db:
        rows = db.execute(sql).fetchall()

    columns = rows[0].keys() if rows else []
    return [create_dict(columns, row) for row in rows]


def resources_by_dataset(pipeline=None):
    # TODO handle when pipeline is not None
    sql = """
        SELECT
      count(DISTINCT resource.resource) AS total,
      count(
        DISTINCT CASE
          WHEN resource.end_date == '' THEN resource.resource
          WHEN strftime('%Y%m%d', resource.end_date) >= strftime('%Y%m%d', 'now') THEN resource.resource
        END
      ) AS active_resources,
      count(
        DISTINCT CASE
          WHEN resource.end_date != ''
          AND strftime('%Y%m%d', resource.end_date) <= strftime('%Y%m%d', 'now') THEN resource.resource
        END
      ) AS ended_resources,
      source_pipeline.pipeline
    FROM
      resource
      INNER JOIN resource_endpoint ON resource.resource = resource_endpoint.resource
      INNER JOIN source ON source.endpoint = resource_endpoint.endpoint
      INNER JOIN source_pipeline ON source.source = source_pipeline.source
    GROUP BY
      source_pipeline.pipeline
    """
    with SqliteDatabase(digital_land_db_path) as db:
        rows = db.execute(sql).fetchall()

    columns = rows[0].keys() if rows else []
    return [create_dict(columns, row) for row in rows]


def first_and_last_resource(pipeline=None):
    # used by get_datasets_summary
    sql = """
          SELECT
          resource.resource,
          MAX(resource.start_date) AS latest,
          MIN(resource.start_date) AS first,
          source_pipeline.pipeline
        FROM
          resource
          INNER JOIN resource_endpoint ON resource.resource = resource_endpoint.resource
          INNER JOIN source ON resource_endpoint.endpoint = source.endpoint
          INNER JOIN source_pipeline ON source.source = source_pipeline.source
        GROUP BY
          source_pipeline.pipeline
        ORDER BY
          resource.start_date DESC"""

    with SqliteDatabase(digital_land_db_path) as db:
        rows = db.execute(sql).fetchall()

    columns = rows[0].keys() if rows else []
    return [create_dict(columns, row) for row in rows]


def get_datasets_summary():
    # get all the datasets listed with their active status
    all_datasets = index_by("dataset", get_datasets())
    missing = []

    # add the publisher coverage numbers
    dataset_coverage = publisher_coverage()
    for d in dataset_coverage:
        if all_datasets.get(d["pipeline"]):
            all_datasets[d["pipeline"]] = {**all_datasets[d["pipeline"]], **d}
        else:
            missing.append(d["pipeline"])

    # add the total resource count
    dataset_resource_counts = resources_by_dataset()
    for d in dataset_resource_counts:
        if all_datasets.get(d["pipeline"]):
            all_datasets[d["pipeline"]] = {**all_datasets[d["pipeline"]], **d}
        else:
            missing.append(d["pipeline"])

    # add the first and last resource dates
    dataset_resource_dates = first_and_last_resource()
    for d in dataset_resource_dates:
        if all_datasets.get(d["pipeline"]):
            all_datasets[d["pipeline"]] = {**all_datasets[d["pipeline"]], **d}
        else:
            missing.append(d["pipeline"])

    return all_datasets
