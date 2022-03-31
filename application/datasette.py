import json
import urllib.parse
import functools
from datetime import datetime

from application.caching import get
from application.data_access.db import Database
from application.factory import sqlite_db_path
from application.utils import (
    create_dict,
    index_by,
    months_since,
    month_dict,
    this_month,
    yesterday,
)

from application.data_access.digital_land_queries import (
    fetch_datasets,
    get_monthly_source_counts,
)


class DLDatasette:

    BASE_URL = "https://datasette.digital-land.info"

    def __init__(self):
        pass

    def generate_query(self, table, params, format="json"):
        param_str = ""
        if params.keys():
            param_str = "&".join([f"{k}={v}" for k, v in params.items()])
        return "%s/digital-land/%s.%s?%s" % (self.BASE_URL, table, format, param_str)

    def query(self, table, params, format="json"):
        query = self.generate_query(table, params, format)
        print("Running: ", query)

        # only returns 100
        r = get(query)
        if r is None:
            return None
        return json.loads(r)

    def sqlQuery(self, query, results="complete"):
        r = get(query)
        if r is None:
            return None
        response = json.loads(r)
        if results == "rows":
            return response["rows"]
        if results == "rows_with_column_names":
            return [create_dict(response["columns"], row) for row in response["rows"]]
        return response

    @staticmethod
    def urlencode(s):
        s.replace(":", "%3A")
        return s

    @staticmethod
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

    def get_total_entity_count(self):
        query = f"{self.BASE_URL}/entity.json?sql=select%0D%0A++COUNT%28DISTINCT+entity%29+AS+count%0D%0Afrom%0D%0A++entity%0D%0A"  # noqa
        results = self.sqlQuery(query, results="rows")
        return results[0][0] if bool(results) else 0

    def get_entity_count(self, pipeline=None):
        if pipeline is not None:
            query = f"{self.BASE_URL}/entity.json?sql=select%0D%0Adataset%2C%0D%0A++COUNT%28DISTINCT+entity%29+AS+count%0D%0Afrom%0D%0A++entity%0D%0Agroup+by%0D%0Adataset%0D%0A"  # noqa
            results = index_by(
                "dataset", self.sqlQuery(query, results="rows_with_column_names")
            )
            return (
                results.get(pipeline)["count"]
                if results.get(pipeline) is not None
                else 0
            )

        return self.get_total_entity_count()

    def get_monthly_resource_counts(self, pipeline=None):
        if not pipeline:

            sql = """SELECT
                  strftime('%Y-%m', resource.start_date) as yyyy_mm,
                  count(distinct resource.resource) as count
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
                    select
              source_pipeline.pipeline,
              count(DISTINCT source.organisation) as expected_publishers,
              COUNT(
                DISTINCT CASE
                  WHEN source.endpoint != '' THEN source.organisation
                END
              ) AS publishers
            from
              source
              INNER JOIN source_pipeline ON source.source = source_pipeline.source
            group by
            source_pipeline.pipeline
    """

        with Database(sqlite_db_path) as db:
            rows = db.execute(sql).fetchall()

        columns = rows[0].keys() if rows else []
        return [create_dict(columns, row) for row in rows]

    def get_latest_resource(self, dataset):
        query = (
            f"{self.BASE_URL}/digital-land.json?sql=select%0D%0A++resource.resource%2C%0D%0A++resource.end_date%2C%0D%0A++resource.entry_date%2C%0D%0A++resource.start_date%2C%0D%0A++source_pipeline.pipeline%0D%0Afrom%0D%0A++resource%0D%0A++INNER+JOIN+resource_endpoint+ON+resource.resource+%3D+resource_endpoint.resource%0D%0A++INNER+JOIN+source+ON+resource_endpoint.endpoint+%3D+source.endpoint%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0Awhere%0D%0A++source_pipeline.pipeline+%3D+%3Apipeline%0D%0Aorder+by%0D%0A++resource.start_date+DESC%0D%0Alimit+1&pipeline="  # noqa
            + dataset
        )
        print("GET LATEST RESOURCE: ", query)
        results = self.sqlQuery(query)
        if len(results["rows"]):
            return create_dict(results["columns"], results["rows"][0])
        return []

    def get_new_resources(self, dates=[yesterday(string=True)]):
        params = [f"d{i}" for i in range(0, len(dates))]
        date_params = dict(zip(params, dates))
        datasette_param_str = "%2C+".join([f"%3A{p}" for p in params])
        query = "{}/digital-land.json?sql=select%0D%0A++DISTINCT+resource%2C%0D%0A++start_date%0D%0Afrom%0D%0A++resource%0D%0Awhere%0D%0A++start_date+in+%28{}%29%0D%0Aorder+by%0D%0A++start_date%0D%0A&{}".format(  # noqa
            self.BASE_URL, datasette_param_str, urllib.parse.urlencode(date_params)
        )  # noqa
        return self.sqlQuery(query, results="rows_with_column_names")


def sql_str_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        ds = DLDatasette()
        query = func(*args, **kwargs)
        result = ds.sqlQuery(query)
        return [create_dict(result["columns"], row) for row in result["rows"]]

    return wrapper


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
    ds = DLDatasette()
    source_counts = get_monthly_source_counts(pipeline)
    resource_counts = ds.get_monthly_resource_counts(pipeline)

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
    ds = DLDatasette()
    query = (
        f"{ds.BASE_URL}/digital-land.json?sql=select%0D%0A++organisation.name%2C%0D%0A++source.organisation%2C%0D%0A++organisation.end_date+AS+organisation_end_date%2C%0D%0A++COUNT%28DISTINCT+resource.resource%29+AS+resources%2C%0D%0A++COUNT%28%0D%0A++++DISTINCT+CASE%0D%0A++++++WHEN+resource.end_date+%3D%3D+%27%27+THEN+resource.resource%0D%0A++++++WHEN+strftime%28%27%25Y%25m%25d%27%2C+resource.end_date%29+%3E%3D+strftime%28%27%25Y%25m%25d%27%2C+%27now%27%29+THEN+resource.resource%0D%0A++++END%0D%0A++%29+AS+active_resources%2C%0D%0A++COUNT%28DISTINCT+resource_endpoint.endpoint%29+AS+endpoints%2C%0D%0A++COUNT%28DISTINCT+source.source%29+AS+sources%2C%0D%0A++COUNT%28%0D%0A++++DISTINCT+CASE%0D%0A++++++WHEN+source.end_date+%3D%3D+%27%27+THEN+source.source%0D%0A++++++WHEN+strftime%28%27%25Y%25m%25d%27%2C+source.end_date%29+%3E%3D+strftime%28%27%25Y%25m%25d%27%2C+%27now%27%29+THEN+source.source%0D%0A++++END%0D%0A++%29+AS+active_sources%2C%0D%0A++MAX%28resource.start_date%29%2C%0D%0A++Cast+%28%0D%0A++++%28%0D%0A++++++julianday%28%27now%27%29+-+julianday%28MAX%28resource.start_date%29%29%0D%0A++++%29+AS+INTEGER%0D%0A++%29+as+days_since_update%0D%0Afrom%0D%0A++resource%0D%0A++INNER+JOIN+resource_endpoint+ON+resource.resource+%3D+resource_endpoint.resource%0D%0A++INNER+JOIN+endpoint+ON+resource_endpoint.endpoint+%3D+endpoint.endpoint%0D%0A++INNER+JOIN+source+ON+resource_endpoint.endpoint+%3D+source.endpoint%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0A++INNER+JOIN+organisation+ON+source.organisation+%3D+organisation.organisation%0D%0Awhere%0D%0A++source_pipeline.pipeline+%3D+%3Apipeline%0D%0AGROUP+BY%0D%0A++source.organisation&pipeline="  # noqa
        + pipeline
    )
    results = ds.sqlQuery(query)
    organisations = [create_dict(results["columns"], row) for row in results["rows"]]
    print("Publihser ===COUNTS====", query)
    return index_by("organisation", organisations)


# returns organisation counts per dataset
def publisher_coverage(pipeline=None):
    # used by get_datasets_summary
    ds = DLDatasette()
    query = f"{ds.BASE_URL}/digital-land.json?sql=select%0D%0A++source_pipeline.pipeline%2C%0D%0A++count%28DISTINCT+source.organisation%29+as+expected_publishers%2C%0D%0A++COUNT%28%0D%0A++++DISTINCT+CASE%0D%0A++++++WHEN+source.endpoint+%21%3D+%27%27+THEN+source.organisation%0D%0A++++END%0D%0A++%29+AS+publishers%0D%0Afrom%0D%0A++source%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0Agroup+by%0D%0Asource_pipeline.pipeline"  # noqa
    if pipeline is not None:
        query = (
            f"{ds.BASE_URL}/digital-land.json?sql=select%0D%0A++count%28DISTINCT+source.organisation%29+as+expected_publishers%2C%0D%0A++COUNT%28%0D%0A++++DISTINCT+CASE%0D%0A++++++WHEN+source.endpoint+%21%3D+%27%27+THEN+source.organisation%0D%0A++++END%0D%0A++%29+AS+publishers%0D%0Afrom%0D%0A++source%0D%0A++INNER+JOIN+source_pipeline+on+source.source+%3D+source_pipeline.source%0D%0Awhere%0D%0A++source_pipeline.pipeline+%3D+%3Apipeline&pipeline="  # noqa
            + pipeline
        )
    print("DATASET PUB COUNT", query)
    results = ds.sqlQuery(query)
    return [create_dict(results["columns"], row) for row in results["rows"]]


def resources_by_dataset(pipeline=None):
    # used by get_datasets_summary
    ds = DLDatasette()
    query = f"{ds.BASE_URL}/digital-land.json?sql=select%0D%0A++count%28DISTINCT+resource.resource%29+as+total%2C%0D%0A++COUNT%28%0D%0A++++DISTINCT+CASE%0D%0A++++++WHEN+resource.end_date+%3D%3D+%27%27+THEN+resource.resource%0D%0A++++++WHEN+strftime%28%27%25Y%25m%25d%27%2C+resource.end_date%29+%3E%3D+strftime%28%27%25Y%25m%25d%27%2C+%27now%27%29+THEN+resource.resource%0D%0A++++END%0D%0A++%29+AS+active_resources%2C%0D%0A++COUNT%28%0D%0A++++DISTINCT+CASE%0D%0A++++++WHEN+resource.end_date+%21%3D+%27%27%0D%0A++++++AND+strftime%28%27%25Y%25m%25d%27%2C+resource.end_date%29+%3C%3D+strftime%28%27%25Y%25m%25d%27%2C+%27now%27%29+THEN+resource.resource%0D%0A++++END%0D%0A++%29+AS+ended_resources%2C%0D%0A++source_pipeline.pipeline%0D%0Afrom%0D%0A++resource%0D%0A++INNER+JOIN+resource_endpoint+ON+resource.resource+%3D+resource_endpoint.resource%0D%0A++INNER+JOIN+source+ON+source.endpoint+%3D+resource_endpoint.endpoint%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0Agroup+by%0D%0A++source_pipeline.pipeline"  # noqa
    if pipeline:
        query = (
            f"{ds.BASE_URL}/digital-land.json?sql=select%0D%0A++count%28DISTINCT+resource.resource%29+as+total%2C%0D%0A++COUNT%28%0D%0A++++DISTINCT+CASE%0D%0A++++++WHEN+resource.end_date+%3D%3D+%27%27+THEN+resource.resource%0D%0A++++++WHEN+strftime%28%27%25Y%25m%25d%27%2C+resource.end_date%29+%3E%3D+strftime%28%27%25Y%25m%25d%27%2C+%27now%27%29+THEN+resource.resource%0D%0A++++END%0D%0A++%29+AS+active_resources%2C%0D%0A++COUNT%28%0D%0A++++DISTINCT+CASE%0D%0A++++++WHEN+resource.end_date+%21%3D+%27%27%0D%0A++++++AND+strftime%28%27%25Y%25m%25d%27%2C+resource.end_date%29+%3C%3D+strftime%28%27%25Y%25m%25d%27%2C+%27now%27%29+THEN+resource.resource%0D%0A++++END%0D%0A++%29+AS+ended_resources%2C%0D%0A++source_pipeline.pipeline%0D%0Afrom%0D%0A++resource%0D%0A++INNER+JOIN+resource_endpoint+ON+resource.resource+%3D+resource_endpoint.resource%0D%0A++INNER+JOIN+source+ON+source.endpoint+%3D+resource_endpoint.endpoint%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0Awhere%0D%0Asource_pipeline.pipeline+%3D+%3Apipeline%0D%0Agroup+by%0D%0A++source_pipeline.pipeline&pipeline="  # noqa
            + pipeline
        )
    print("RESOURCES BY DATASET", query)
    results = ds.sqlQuery(query)
    return [create_dict(results["columns"], row) for row in results["rows"]]


def first_and_last_resource(pipeline=None):
    # used by get_datasets_summary
    ds = DLDatasette()
    query = f"{ds.BASE_URL}/digital-land.json?sql=select%0D%0A++resource.resource%2C%0D%0A++MAX%28resource.start_date%29+AS+latest%2C%0D%0A++MIN%28resource.start_date%29+AS+first%2C%0D%0A++source_pipeline.pipeline%0D%0Afrom%0D%0A++resource%0D%0A++INNER+JOIN+resource_endpoint+ON+resource.resource+%3D+resource_endpoint.resource%0D%0A++INNER+JOIN+source+ON+resource_endpoint.endpoint+%3D+source.endpoint%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0Agroup+by%0D%0A++source_pipeline.pipeline%0D%0Aorder+by%0D%0A++resource.start_date+DESC"  # noqa
    results = ds.sqlQuery(query)
    return [create_dict(results["columns"], row) for row in results["rows"]]


def get_datasets_summary():
    # get all the datasets listed with their active status
    all_datasets = index_by("dataset", fetch_datasets())
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

    print("MISSING")
    print(set(missing))

    return all_datasets
