import json
import urllib.parse
import functools
from datetime import datetime

from application.caching import get
from application.utils import (
    create_dict,
    index_by,
    months_since,
    month_dict,
    this_month,
    yesterday,
)


class DLDatasette:
    BASE_URL = "https://datasette.digital-land.info/digital-land/"

    def __init__(self):
        pass

    def generate_query(self, table, params, format="json"):
        param_str = ""
        if params.keys():
            param_str = "&".join([f"{k}={v}" for k, v in params.items()])
        return "%s%s.%s?%s" % (self.BASE_URL, table, format, param_str)

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

    def get_sources_per_dataset_for_organisation(self, organisation):
        # returns number of sources with and without endpoint for each dataset for the provided organisation
        query = (
            "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++source_pipeline.pipeline+AS+pipeline%2C%0D%0A++COUNT%28DISTINCT+source.source%29+AS+sources%2C%0D%0A++SUM%28CASE+WHEN+%28source.endpoint%29+is+not+null+and+%28source.endpoint%29+%21%3D+%22%22+THEN+1+ELSE+0+END%29++AS+sources_with_endpoint%0D%0Afrom%0D%0A++source%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0Awhere%0D%0A++source.organisation+%3D+%3Aorganisation%0D%0Agroup+by%0D%0A++source_pipeline.pipeline&organisation="
            + DLDatasette.urlencode(organisation)
        )
        return self.sqlQuery(query, results="rows_with_column_names")

    def get_all_sources_for_organisation(self, organisation):
        query = (
            "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++source.source%2C%0D%0A++source.organisation%2C%0D%0A++organisation.name%2C%0D%0A++source.endpoint%2C%0D%0A++source.documentation_url%2C%0D%0A++source.entry_date%2C%0D%0A++source.start_date%2C%0D%0A++source.end_date%2C%0D%0A++source_pipeline.pipeline%0D%0Afrom%0D%0A++source%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0A++INNER+JOIN+organisation+ON+source.organisation+%3D+organisation.organisation%0D%0Awhere%0D%0Asource.organisation+LIKE+%3Aorganisation%0D%0Aorder+by%0D%0A++source.start_date+DESC&organisation="
            + organisation
        )
        return self.sqlQuery(query, results="rows_with_column_names")

    def source_counts(self, pipeline=None):
        # returns high level source counts
        query = "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++COUNT%28DISTINCT+source.source%29+AS+sources%2C%0D%0A++COUNT%28%0D%0A++++DISTINCT+CASE%0D%0A++++++WHEN+source.end_date+%3D%3D+%27%27+THEN+source.source%0D%0A++++++WHEN+strftime%28%27%25Y%25m%25d%27%2C+source.end_date%29+%3E%3D+strftime%28%27%25Y%25m%25d%27%2C+%27now%27%29+THEN+source.source%0D%0A++++END%0D%0A++%29+AS+active%2C%0D%0A++COUNT%28%0D%0A++++DISTINCT+CASE%0D%0A++++++WHEN+end_date+%21%3D+%27%27+THEN+source.source%0D%0A++++++WHEN+strftime%28%27%25Y%25m%25d%27%2C+source.end_date%29+%3C%3D+strftime%28%27%25Y%25m%25d%27%2C+%27now%27%29+THEN+source.source%0D%0A++++END%0D%0A++%29+AS+inactive%2C%0D%0A++COUNT%28DISTINCT+source_pipeline.pipeline%29+AS+pipelines%0D%0Afrom%0D%0A++source%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0Awhere%0D%0Asource.endpoint+%21%3D+%27%27%0D%0A%0D%0A"
        if pipeline:
            query = (
                query
                + "AND+source_pipeline.pipeline+%3D+%3Apipeline%0D%0A%0D%0A&pipeline="
                + pipeline
            )
        return self.sqlQuery(query, results="rows_with_column_names")

    def get_monthly_source_counts(self, pipeline=None):
        query = "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++strftime%28%27%25Y-%25m%27%2C+source.start_date%29+as+yyyy_mm%2C%0D%0A++count%28distinct+source.source%29%0D%0Afrom%0D%0A++source%0D%0Awhere%0D%0A++source.start_date+%21%3D+%22%22%0D%0Agroup+by%0D%0A++yyyy_mm%0D%0Aorder+by%0D%0A++yyyy_mm"
        if pipeline:
            query = (
                "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++strftime%28%27%25Y-%25m%27%2C+source.start_date%29+as+yyyy_mm%2C%0D%0A++count%28distinct+source.source%29%0D%0Afrom%0D%0A++source%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0Awhere%0D%0A++source.start_date+%21%3D+%22%22%0D%0A++AND+source_pipeline.pipeline+%3D+%3Apipeline%0D%0Agroup+by%0D%0A++yyyy_mm%0D%0Aorder+by%0D%0A++yyyy_mm&pipeline="
                + pipeline
            )
        return self.sqlQuery(query, results="rows")

    def get_blank_sources(self, pipeline):
        query = (
            "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++source.source%2C%0D%0A++source.organisation%2C%0D%0A++organisation.name%2C%0D%0A++source.endpoint%2C%0D%0A++source.documentation_url%2C%0D%0A++source.entry_date%2C%0D%0A++source.start_date%2C%0D%0A++source.end_date%2C%0D%0A++GROUP_CONCAT%28DISTINCT+source_pipeline.pipeline%29+AS+pipeline%0D%0Afrom%0D%0A++source%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0A++INNER+JOIN+organisation+ON+source.organisation+%3D+organisation.organisation%0D%0Awhere%0D%0Apipeline+LIKE+%3Apipeline+AND%0D%0Asource.endpoint+%3D+%27%27%0D%0Agroup+by%0D%0Aorganisation.organisation%0D%0Aorder+by%0D%0A++organisation.name&pipeline="
            + pipeline
        )
        return self.sqlQuery(query, results="rows_with_column_names")

    def get_total_entity_count(self):
        query = "https://datasette.digital-land.info/entity.json?sql=select%0D%0A++COUNT%28DISTINCT+entity%29+AS+count%0D%0Afrom%0D%0A++entity%0D%0A"
        results = self.sqlQuery(query, results="rows")
        return results[0][0] if bool(results) else 0

    def get_entity_count(self, pipeline=None):
        if pipeline is not None:
            query = "https://datasette.digital-land.info/entity.json?sql=select%0D%0Adataset%2C%0D%0A++COUNT%28DISTINCT+entity%29+AS+count%0D%0Afrom%0D%0A++entity%0D%0Agroup+by%0D%0Adataset%0D%0A"
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
        query = "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++strftime%28%27%25Y-%25m%27%2C+resource.start_date%29+as+yyyy_mm%2C%0D%0A++count%28distinct+resource.resource%29%0D%0Afrom%0D%0A++resource%0D%0Awhere%0D%0A++resource.start_date+%21%3D+%22%22%0D%0Agroup+by%0D%0A++yyyy_mm%0D%0Aorder+by%0D%0A++yyyy_mm"
        if pipeline:
            query = (
                "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++strftime%28%27%25Y-%25m%27%2C+resource.start_date%29+as+yyyy_mm%2C%0D%0A++count%28distinct+resource.resource%29%0D%0Afrom%0D%0A++resource%0D%0A++INNER+JOIN+resource_endpoint+ON+resource.resource+%3D+resource_endpoint.resource%0D%0A++INNER+JOIN+endpoint+ON+resource_endpoint.endpoint+%3D+endpoint.endpoint%0D%0A++INNER+JOIN+source+ON+resource_endpoint.endpoint+%3D+source.endpoint%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0Awhere%0D%0A++resource.start_date+%21%3D+%22%22%0D%0A++AND+source_pipeline.pipeline+%3D+%3Apipeline%0D%0Agroup+by%0D%0A++yyyy_mm%0D%0Aorder+by%0D%0A++yyyy_mm&pipeline="
                + pipeline
            )
        return self.sqlQuery(query, results="rows")

    def get_latest_resource(self, dataset):
        query = (
            "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++resource.resource%2C%0D%0A++resource.end_date%2C%0D%0A++resource.entry_date%2C%0D%0A++resource.start_date%2C%0D%0A++source_pipeline.pipeline%0D%0Afrom%0D%0A++resource%0D%0A++INNER+JOIN+resource_endpoint+ON+resource.resource+%3D+resource_endpoint.resource%0D%0A++INNER+JOIN+source+ON+resource_endpoint.endpoint+%3D+source.endpoint%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0Awhere%0D%0A++source_pipeline.pipeline+%3D+%3Apipeline%0D%0Aorder+by%0D%0A++resource.start_date+DESC%0D%0Alimit+1&pipeline="
            + dataset
        )
        results = self.sqlQuery(query)
        if len(results["rows"]):
            return create_dict(results["columns"], results["rows"][0])
        return []

    def get_new_resources(self, dates=[yesterday(string=True)]):
        params = [f"d{i}" for i in range(0, len(dates))]
        date_params = dict(zip(params, dates))
        datasette_param_str = "%2C+".join([f"%3A{p}" for p in params])
        query = "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++DISTINCT+resource%2C%0D%0A++start_date%0D%0Afrom%0D%0A++resource%0D%0Awhere%0D%0A++start_date+in+%28{}%29%0D%0Aorder+by%0D%0A++start_date%0D%0A&{}".format(
            datasette_param_str, urllib.parse.urlencode(date_params)
        )
        return self.sqlQuery(query, results="rows_with_column_names")

    def get_expected_publishers(self):
        query = "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0Asource.organisation%2C%0D%0Aorganisation.name%2C%0D%0A++COUNT%28%0D%0A++++DISTINCT+CASE%0D%0A++++++WHEN+source.endpoint+%21%3D+%27%27+THEN+source.organisation%0D%0A++++END%0D%0A++%29+AS+active%0D%0Afrom%0D%0A++source%0D%0A++INNER+JOIN+organisation+ON+source.organisation+%3D+organisation.organisation%0D%0Agroup+by%0D%0A++source.organisation"
        return index_by(
            "organisation", self.sqlQuery(query, results="rows_with_column_names")
        )

    # log related
    def get_daily_log_summary(self, date=yesterday(string=True)):
        query = (
            "http://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++entry_date%2C%0D%0A++status%2C%0D%0A++COUNT%28DISTINCT+endpoint%29+AS+count%0D%0Afrom%0D%0A++log%0D%0Awhere%0D%0A++%22entry_date%22+%3D+%3Adate%0D%0Agroup+by%0D%0A++status&date="
            + date
        )
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


def sources_with_endpoint():
    # query
    # "https://datasette.digital-land.info/digital-land/source.json?endpoint__notblank=1&_labels=on"
    ds = DLDatasette()

    endpoint_results = ds.query("source", {"endpoint__notblank": 1, "_labels": "on"})
    print(endpoint_results)

    # https://datasette.digital-land.info/digital-land/source?documentation_url__isblank=1&endpoint__notblank=1
    no_documentation_url_results = ds.query(
        "source",
        {
            "endpoint__notblank": 1,
            "documentation_url__isblank": 1,
            "_labels": "on",
            "_facet": "collection",
        },
    )

    return {
        "with_endpoint": endpoint_results["filtered_table_rows_count"],
        "no_documentation": {
            "count": no_documentation_url_results["filtered_table_rows_count"],
            "collection": no_documentation_url_results["facet_results"]["collection"][
                "results"
            ],
        },
    }


def datasets_for_an_organisation(id):
    org_id = id.replace(":", "%3A")
    ds = DLDatasette()
    # returns a list of resources for the organisation
    query = (
        "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++resource.resource%2C%0D%0A++resource.end_date%2C%0D%0A++source.source%2C%0D%0A++resource_endpoint.endpoint%2C%0D%0A++endpoint.endpoint_url%2C%0D%0A++source.organisation%2C%0D%0A++source_pipeline.pipeline%0D%0Afrom%0D%0A++resource%0D%0A++INNER+JOIN+resource_endpoint+ON+resource.resource+%3D+resource_endpoint.resource%0D%0A++INNER+JOIN+endpoint+ON+resource_endpoint.endpoint+%3D+endpoint.endpoint%0D%0A++INNER+JOIN+source+ON+resource_endpoint.endpoint+%3D+source.endpoint%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0AWHERE%0D%0A++source.organisation+%3D+%3Aorganisation%0D%0AGROUP+BY%0D%0A++resource.resource&organisation="
        + org_id
    )
    r1 = ds.sqlQuery(query)

    # returns some counts per dataset (pipeline) for the organisation
    query2 = (
        "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++COUNT%28DISTINCT+resource.resource%29+AS+resources%2C%0D%0A++COUNT%28DISTINCT+CASE+%0D%0A++++WHEN+resource.end_date+%3D%3D+%27%27+THEN+resource.resource%0D%0A++++WHEN+strftime%28%27%25Y%25m%25d%27%2C+resource.end_date%29+%3E%3D+strftime%28%27%25Y%25m%25d%27%2C+%27now%27%29+THEN+resource.resource%0D%0A++END%29+AS+active_resources%2C%0D%0A++COUNT%28DISTINCT+resource_endpoint.endpoint%29+AS+endpoints%2C%0D%0A++source_pipeline.pipeline+AS+pipeline%0D%0Afrom%0D%0A++resource%0D%0A++INNER+JOIN+resource_endpoint+ON+resource.resource+%3D+resource_endpoint.resource%0D%0A++INNER+JOIN+endpoint+ON+resource_endpoint.endpoint+%3D+endpoint.endpoint%0D%0A++INNER+JOIN+source+ON+resource_endpoint.endpoint+%3D+source.endpoint%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0A++INNER+JOIN+organisation+ON+source.organisation+%3D+organisation.organisation%0D%0Awhere%0D%0A++organisation.organisation+%3D+%3Aorganisation%0D%0AGROUP+BY%0D%0A++source.organisation%2C%0D%0A++source_pipeline.pipeline&organisation="
        + org_id
    )
    r2 = ds.sqlQuery(query2)
    return {
        "resources": r1["rows"],
        "datasets_covered": list(set([r[6] for r in r1["rows"]])),
        "dataset_counts": [create_dict(r2["columns"], row) for row in r2["rows"]],
    }


def datasets_by_organistion():
    query = "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++organisation.name%2C%0D%0A++source.organisation%2C%0D%0A++organisation.end_date+AS+organisation_end_date%2C%0D%0A++COUNT%28DISTINCT+resource.resource%29+AS+resources%2C%0D%0A++COUNT%28%0D%0A++++DISTINCT+CASE%0D%0A++++++WHEN+resource.end_date+%3D%3D+%27%27+THEN+resource.resource%0D%0A++++++WHEN+strftime%28%27%25Y%25m%25d%27%2C+resource.end_date%29+%3E%3D+strftime%28%27%25Y%25m%25d%27%2C+%27now%27%29+THEN+resource.resource%0D%0A++++END%0D%0A++%29+AS+active%2C%0D%0A++COUNT%28DISTINCT+resource_endpoint.endpoint%29+AS+endpoints%2C%0D%0A++COUNT%28DISTINCT+source_pipeline.pipeline%29+AS+pipelines%0D%0Afrom%0D%0A++resource%0D%0A++INNER+JOIN+resource_endpoint+ON+resource.resource+%3D+resource_endpoint.resource%0D%0A++INNER+JOIN+endpoint+ON+resource_endpoint.endpoint+%3D+endpoint.endpoint%0D%0A++INNER+JOIN+source+ON+resource_endpoint.endpoint+%3D+source.endpoint%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0A++INNER+JOIN+organisation+ON+source.organisation+%3D+organisation.organisation%0D%0AGROUP+BY%0D%0A++source.organisation"
    ds = DLDatasette()
    results = ds.sqlQuery(query)
    organisations = [create_dict(results["columns"], row) for row in results["rows"]]
    return index_by("organisation", organisations)


def get_monthly_counts(pipeline=None):
    ds = DLDatasette()
    source_counts = ds.get_monthly_source_counts(pipeline)
    resource_counts = ds.get_monthly_resource_counts(pipeline)

    # handle if either are empty
    if not bool(source_counts):
        return None

    first_source_month_str = source_counts[0][0]
    first_resource_month_str = (
        resource_counts[0][0] if bool(resource_counts) else this_month()
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
            if row[0] in d.keys():
                d[row[0]] = d[row[0]] + row[1]
        # needs to be in tuple form
        counts[k] = [(k, v) for k, v in d.items()]
    counts["months"] = list(all_months.keys())
    return counts


def publisher_counts(pipeline):
    # returns resource, active resource, endpoints, sources, active source, latest resource date and days since update
    ds = DLDatasette()
    query = (
        "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++organisation.name%2C%0D%0A++source.organisation%2C%0D%0A++organisation.end_date+AS+organisation_end_date%2C%0D%0A++COUNT%28DISTINCT+resource.resource%29+AS+resources%2C%0D%0A++COUNT%28%0D%0A++++DISTINCT+CASE%0D%0A++++++WHEN+resource.end_date+%3D%3D+%27%27+THEN+resource.resource%0D%0A++++++WHEN+strftime%28%27%25Y%25m%25d%27%2C+resource.end_date%29+%3E%3D+strftime%28%27%25Y%25m%25d%27%2C+%27now%27%29+THEN+resource.resource%0D%0A++++END%0D%0A++%29+AS+active_resources%2C%0D%0A++COUNT%28DISTINCT+resource_endpoint.endpoint%29+AS+endpoints%2C%0D%0A++COUNT%28DISTINCT+source.source%29+AS+sources%2C%0D%0A++COUNT%28%0D%0A++++DISTINCT+CASE%0D%0A++++++WHEN+source.end_date+%3D%3D+%27%27+THEN+source.source%0D%0A++++++WHEN+strftime%28%27%25Y%25m%25d%27%2C+source.end_date%29+%3E%3D+strftime%28%27%25Y%25m%25d%27%2C+%27now%27%29+THEN+source.source%0D%0A++++END%0D%0A++%29+AS+active_sources%2C%0D%0A++MAX%28resource.start_date%29%2C%0D%0A++Cast+%28%0D%0A++++%28%0D%0A++++++julianday%28%27now%27%29+-+julianday%28MAX%28resource.start_date%29%29%0D%0A++++%29+AS+INTEGER%0D%0A++%29+as+days_since_update%0D%0Afrom%0D%0A++resource%0D%0A++INNER+JOIN+resource_endpoint+ON+resource.resource+%3D+resource_endpoint.resource%0D%0A++INNER+JOIN+endpoint+ON+resource_endpoint.endpoint+%3D+endpoint.endpoint%0D%0A++INNER+JOIN+source+ON+resource_endpoint.endpoint+%3D+source.endpoint%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0A++INNER+JOIN+organisation+ON+source.organisation+%3D+organisation.organisation%0D%0Awhere%0D%0A++source_pipeline.pipeline+%3D+%3Apipeline%0D%0AGROUP+BY%0D%0A++source.organisation&pipeline="
        + pipeline
    )
    results = ds.sqlQuery(query)
    organisations = [create_dict(results["columns"], row) for row in results["rows"]]
    return index_by("organisation", organisations)


def total_publisher_coverage():
    # returns count for expected publishers and publishers with source that have an endpoint
    ds = DLDatasette()
    query = "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++count%28DISTINCT+source.organisation%29+AS+total%2C%0D%0A++COUNT%28%0D%0A++++DISTINCT+CASE%0D%0A++++++WHEN+source.endpoint+%21%3D+%27%27+THEN+source.organisation%0D%0A++++END%0D%0A++%29+AS+active%0D%0Afrom%0D%0A++source%0D%0Awhere%0D%0Asource.organisation+%21%3D+%27%27%0D%0Aorder+by%0D%0A++source.source"
    results = ds.sqlQuery(query)
    return create_dict(results["columns"], results["rows"][0])


# returns organisation counts per dataset
def publisher_coverage(pipeline=None):
    ds = DLDatasette()
    query = "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++source_pipeline.pipeline%2C%0D%0A++count%28DISTINCT+source.organisation%29+as+expected_publishers%2C%0D%0A++COUNT%28%0D%0A++++DISTINCT+CASE%0D%0A++++++WHEN+source.endpoint+%21%3D+%27%27+THEN+source.organisation%0D%0A++++END%0D%0A++%29+AS+publishers%0D%0Afrom%0D%0A++source%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0Agroup+by%0D%0Asource_pipeline.pipeline"
    if pipeline is not None:
        query = (
            "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++count%28DISTINCT+source.organisation%29+as+expected_publishers%2C%0D%0A++COUNT%28%0D%0A++++DISTINCT+CASE%0D%0A++++++WHEN+source.endpoint+%21%3D+%27%27+THEN+source.organisation%0D%0A++++END%0D%0A++%29+AS+publishers%0D%0Afrom%0D%0A++source%0D%0A++INNER+JOIN+source_pipeline+on+source.source+%3D+source_pipeline.source%0D%0Awhere%0D%0A++source_pipeline.pipeline+%3D+%3Apipeline&pipeline="
            + pipeline
        )
    results = ds.sqlQuery(query)
    return [create_dict(results["columns"], row) for row in results["rows"]]


def active_resources(pipeline):
    ds = DLDatasette()
    query = (
        "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++resource.resource%2C%0D%0A++resource_organisation.organisation%2C%0D%0A++resource.end_date%2C%0D%0A++resource.entry_date%2C%0D%0A++resource.start_date%2C%0D%0A++source_pipeline.pipeline%0D%0Afrom%0D%0A++resource%0D%0A++INNER+JOIN+resource_endpoint+ON+resource.resource+%3D+resource_endpoint.resource%0D%0A++INNER+JOIN+resource_organisation+ON+resource.resource+%3D+resource_organisation.resource%0D%0A++INNER+JOIN+source+ON+resource_endpoint.endpoint+%3D+source.endpoint%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0Awhere%0D%0A++source_pipeline.pipeline+%3D+%3Apipeline%0D%0A++AND+%28resource.end_date+%3D%3D+%27%27+OR+strftime%28%27%25Y%25m%25d%27%2C+resource.end_date%29+%3E%3D+strftime%28%27%25Y%25m%25d%27%2C+%27now%27%29%29%0D%0Aorder+by%0D%0A++resource.end_date+ASC%0D%0A&pipeline="
        + pipeline
    )
    results = ds.sqlQuery(query)
    return [create_dict(results["columns"], row) for row in results["rows"]]


def sources_by_dataset(pipeline=None):
    ds = DLDatasette()
    query = "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++count%28DISTINCT+source.source%29+as+total%2C%0D%0A++COUNT%28DISTINCT+CASE+%0D%0A++++WHEN+source.end_date+%3D%3D+%27%27+AND+source.endpoint+%21%3D+%27%27+THEN+source.source%0D%0A++++WHEN+strftime%28%27%25Y%25m%25d%27%2C+source.end_date%29+%3E%3D+strftime%28%27%25Y%25m%25d%27%2C+%27now%27%29+AND+source.endpoint+%21%3D+%27%27+THEN+source.source%0D%0A++END%29+AS+active_sources%2C%0D%0A++COUNT%28DISTINCT+CASE+%0D%0A++++WHEN+source.endpoint+%3D%3D+%27%27+THEN+source.source%0D%0A++END%29+AS+blank_sources%2C%0D%0A++COUNT%28DISTINCT+CASE+%0D%0A++++WHEN+source.end_date+%21%3D+%27%27+AND+strftime%28%27%25Y%25m%25d%27%2C+source.end_date%29+%3C%3D+strftime%28%27%25Y%25m%25d%27%2C+%27now%27%29++THEN+source.source%0D%0A++END%29+AS+ended_sources%2C%0D%0A++source_pipeline.pipeline%0D%0Afrom%0D%0A++source%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0Agroup+by%0D%0Asource_pipeline.pipeline%0D%0A"
    if pipeline:
        query = (
            "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++source.source%2C%0D%0A++source.organisation%2C%0D%0A++organisation.name%2C%0D%0A++source_pipeline.pipeline%0D%0Afrom%0D%0A++source%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0A++INNER+JOIN+organisation+on+source.organisation+%3D+organisation.organisation%0D%0Awhere%0D%0A++source_pipeline.pipeline+%3D+%3Apipeline%0D%0A++AND+source.end_date+%3D%3D+%27%27%0D%0A++AND+source.endpoint+%21%3D+%27%27%0D%0Aorder+by%0D%0A++organisation.name%0D%0A&pipeline="
            + pipeline
        )
    results = ds.sqlQuery(query)
    return [create_dict(results["columns"], row) for row in results["rows"]]


def source_count_per_organisation():
    ds = DLDatasette()
    query = "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++organisation.name%2C%0D%0A++source.organisation%2C%0D%0A++organisation.end_date+AS+organisation_end_date%2C%0D%0A++COUNT%28DISTINCT+source_pipeline.pipeline%29+AS+pipelines%2C%0D%0A++COUNT%28DISTINCT+source.source%29+AS+sources%0D%0Afrom%0D%0Asource%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0A++INNER+JOIN+organisation+ON+source.organisation+%3D+organisation.organisation%0D%0Awhere%0D%0Asource.endpoint+%21%3D+%27%27%0D%0AGROUP+BY%0D%0A++source.organisation"
    results = ds.sqlQuery(query)
    return [create_dict(results["columns"], row) for row in results["rows"]]


def get_sources(limit=100, filter=None, include_blanks=False):
    ds = DLDatasette()
    if not include_blanks:
        where_clause = "where%0D%0A++source.endpoint+%21%3D+%27%27%0D%0A"
    # "where%0D%0A++source_pipeline.pipeline+LIKE+%3Apipeline%0D%0A++AND+source.endpoint+%21%3D+%27%27%0D%0A"
    params = ""
    limit_str = ""
    if limit:
        limit_str = "%0D%0Alimit+{}".format(limit)
    if filter:
        where_clause, params = DLDatasette.sql_for_filter(
            filter,
            {
                "organisation": "source.organisation",
                "endpoint_": "endpoint.endpoint",
                "source": "source.source",
            },
        )
        if not include_blanks:
            where_clause = where_clause + "++AND+source.endpoint+%21%3D+%27%27%0D%0A"
    query = "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++source.source%2C%0D%0A++source.organisation%2C%0D%0A++organisation.name%2C%0D%0A++source.endpoint%2C%0D%0A++source.documentation_url%2C%0D%0A++source.entry_date%2C%0D%0A++source.start_date%2C%0D%0A++source.end_date%2C%0D%0A++GROUP_CONCAT%28DISTINCT+source_pipeline.pipeline%29+AS+pipeline%0D%0Afrom%0D%0A++source%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0A++INNER+JOIN+organisation+ON+source.organisation+%3D+organisation.organisation%0D%0A++INNER+JOIN+endpoint+ON+source.endpoint+%3D+endpoint.endpoint%0D%0A{}group+by%0D%0Asource.source%0D%0Aorder+by%0D%0A++source.start_date+DESC{}{}".format(
        where_clause, limit_str, params
    )
    print(query)
    results = ds.sqlQuery(query)
    return [create_dict(results["columns"], row) for row in results["rows"]]


def get_blank_source(source):
    ds = DLDatasette()
    query = (
        "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++source.attribution%2C%0D%0A++source.collection%2C%0D%0A++source.documentation_url%2C%0D%0A++source.end_date%2C%0D%0A++source.endpoint%2C%0D%0A++source.entry_date%2C%0D%0A++source.licence%2C%0D%0A++source.organisation%2C%0D%0A++source.source%2C%0D%0A++source.start_date%0D%0Afrom%0D%0A++source%0D%0Awhere%0D%0A++source.source+%3D+%3Asource%0D%0Aorder+by%0D%0A++source.source&source="
        + source
    )
    results = ds.sqlQuery(query)
    return [create_dict(results["columns"], row) for row in results["rows"]]


def get_source(source):
    ds = DLDatasette()
    query = (
        "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++source.attribution%2C%0D%0A++source.collection%2C%0D%0A++source.documentation_url%2C%0D%0A++source.end_date%2C%0D%0A++source.endpoint%2C%0D%0A++endpoint.endpoint_url%2C%0D%0A++source.entry_date%2C%0D%0A++source.licence%2C%0D%0A++source.organisation%2C%0D%0A++source.source%2C%0D%0A++source.start_date%0D%0Afrom%0D%0A++source%0D%0A++INNER+JOIN+endpoint+ON+source.endpoint+%3D+endpoint.endpoint%0D%0Awhere%0D%0A++source.source+%3D+%3Asource%0D%0Aorder+by%0D%0A++source.source&source="
        + source
    )
    results = ds.sqlQuery(query)
    if len(results["rows"]) == 0:
        return get_blank_source(source)
    return [create_dict(results["columns"], row) for row in results["rows"]]


def clean_content_type_field(rows):
    for row in rows:
        if row.get("content_type"):
            row["content_type"] = list(set(row["content_type"].split(";")))
    return rows


def get_resources(limit=100, filter=None):
    ds = DLDatasette()
    where_clause = ""
    params = ""
    limit_str = ""
    if limit:
        limit_str = "%0D%0Alimit+{}".format(limit)
    if filter:
        where_clause, params = DLDatasette.sql_for_filter(
            filter,
            {
                "organisation": "resource_organisation.organisation",
                "source": "source.source",
                "resource": "resource.resource",
            },
        )
    query = "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++DISTINCT+resource.resource%2C%0D%0A++resource.entry_date%2C%0D%0A++resource.start_date%2C%0D%0A++resource.end_date%2C%0D%0A++REPLACE%28GROUP_CONCAT%28DISTINCT+resource_organisation.organisation%29%2C%22%2C%22%2C+%22%3B%22%29+AS+organisation%2C%0D%0A++REPLACE%28GROUP_CONCAT%28DISTINCT+organisation.name%29%2C%22%2C%22%2C+%22%3B%22%29+AS+name%2C%0D%0A++REPLACE%28%0D%0A++++GROUP_CONCAT%28DISTINCT+log.content_type%29%2C%0D%0A++++%22%2C%22%2C%0D%0A++++%22%3B%22%0D%0A++%29+AS+content_type%2C%0D%0A++REPLACE%28%0D%0A++++GROUP_CONCAT%28DISTINCT+source_pipeline.pipeline%29%2C%0D%0A++++%22%2C%22%2C%0D%0A++++%22%3B%22%0D%0A++%29+AS+pipeline%0D%0Afrom%0D%0A++resource%0D%0A++INNER+JOIN+resource_organisation+ON+resource.resource+%3D+resource_organisation.resource%0D%0A++INNER+JOIN+organisation+ON+resource_organisation.organisation+%3D+organisation.organisation%0D%0A++INNER+JOIN+resource_endpoint+ON+resource.resource+%3D+resource_endpoint.resource%0D%0A++INNER+JOIN+endpoint+ON+resource_endpoint.endpoint+%3D+endpoint.endpoint%0D%0A++INNER+JOIN+log+ON+resource.resource+%3D+log.resource%0D%0A++INNER+JOIN+source+ON+source.endpoint+%3D+resource_endpoint.endpoint%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0A{}group+by%0D%0A++resource.resource%0D%0Aorder+by%0D%0Aresource.start_date+DESC{}{}".format(
        where_clause, limit_str, params
    )
    results = ds.sqlQuery(query)
    return [create_dict(results["columns"], row) for row in results["rows"]]


def get_resource(resource):
    ds = DLDatasette()
    # e.g https://datasette.digital-land.info/digital-land?sql=select%0D%0A++DISTINCT+resource.resource%2C%0D%0A++resource.entry_date%2C%0D%0A++resource.start_date%2C%0D%0A++resource.end_date%2C%0D%0A++resource_organisation.organisation%2C%0D%0A++organisation.name%2C%0D%0A++endpoint.endpoint%2C%0D%0A++endpoint.endpoint_url%2C%0D%0A++REPLACE%28GROUP_CONCAT%28DISTINCT+log.content_type%29%2C+%22%2C%22%2C+%22%3B%22%29+AS+content_type%2C%0D%0A++REPLACE%28GROUP_CONCAT%28DISTINCT+source_pipeline.pipeline%29%2C+%22%2C%22%2C+%22%3B%22%29+AS+pipeline%0D%0Afrom%0D%0A++resource%0D%0A++INNER+JOIN+resource_organisation+ON+resource.resource+%3D+resource_organisation.resource%0D%0A++INNER+JOIN+organisation+ON+resource_organisation.organisation+%3D+organisation.organisation%0D%0A++INNER+JOIN+resource_endpoint+ON+resource.resource+%3D+resource_endpoint.resource%0D%0A++INNER+JOIN+endpoint+ON+resource_endpoint.endpoint+%3D+endpoint.endpoint%0D%0A++INNER+JOIN+log+ON+resource.resource+%3D+log.resource%0D%0A++INNER+JOIN+source+ON+source.endpoint+%3D+resource_endpoint.endpoint%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0Awhere%0D%0A++resource.resource+%3D+%3Aresource%0D%0Agroup+by%0D%0A++endpoint.endpoint&resource=0001a1baf9ddd7505cfef2e671292122de73a44299e5f5e584e9ec1514c0181c
    query = (
        "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++DISTINCT+resource.resource%2C%0D%0A++resource.entry_date%2C%0D%0A++resource.start_date%2C%0D%0A++resource.end_date%2C%0D%0A++resource_organisation.organisation%2C%0D%0A++organisation.name%2C%0D%0A++endpoint.endpoint%2C%0D%0A++endpoint.endpoint_url%2C%0D%0A++REPLACE%28GROUP_CONCAT%28DISTINCT+log.content_type%29%2C+%22%2C%22%2C+%22%3B%22%29+AS+content_type%2C%0D%0A++REPLACE%28GROUP_CONCAT%28DISTINCT+source_pipeline.pipeline%29%2C+%22%2C%22%2C+%22%3B%22%29+AS+pipeline%0D%0Afrom%0D%0A++resource%0D%0A++INNER+JOIN+resource_organisation+ON+resource.resource+%3D+resource_organisation.resource%0D%0A++INNER+JOIN+organisation+ON+resource_organisation.organisation+%3D+organisation.organisation%0D%0A++INNER+JOIN+resource_endpoint+ON+resource.resource+%3D+resource_endpoint.resource%0D%0A++INNER+JOIN+endpoint+ON+resource_endpoint.endpoint+%3D+endpoint.endpoint%0D%0A++INNER+JOIN+log+ON+resource.resource+%3D+log.resource%0D%0A++INNER+JOIN+source+ON+source.endpoint+%3D+resource_endpoint.endpoint%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0Awhere%0D%0A++resource.resource+%3D+%3Aresource%0D%0Agroup+by%0D%0A++endpoint.endpoint&resource="
        + resource
    )
    results = ds.sqlQuery(query)
    return clean_content_type_field(
        [create_dict(results["columns"], row) for row in results["rows"]]
    )


def resources_by_dataset(pipeline=None):
    ds = DLDatasette()
    query = "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++count%28DISTINCT+resource.resource%29+as+total%2C%0D%0A++COUNT%28%0D%0A++++DISTINCT+CASE%0D%0A++++++WHEN+resource.end_date+%3D%3D+%27%27+THEN+resource.resource%0D%0A++++++WHEN+strftime%28%27%25Y%25m%25d%27%2C+resource.end_date%29+%3E%3D+strftime%28%27%25Y%25m%25d%27%2C+%27now%27%29+THEN+resource.resource%0D%0A++++END%0D%0A++%29+AS+active_resources%2C%0D%0A++COUNT%28%0D%0A++++DISTINCT+CASE%0D%0A++++++WHEN+resource.end_date+%21%3D+%27%27%0D%0A++++++AND+strftime%28%27%25Y%25m%25d%27%2C+resource.end_date%29+%3C%3D+strftime%28%27%25Y%25m%25d%27%2C+%27now%27%29+THEN+resource.resource%0D%0A++++END%0D%0A++%29+AS+ended_resources%2C%0D%0A++source_pipeline.pipeline%0D%0Afrom%0D%0A++resource%0D%0A++INNER+JOIN+resource_endpoint+ON+resource.resource+%3D+resource_endpoint.resource%0D%0A++INNER+JOIN+source+ON+source.endpoint+%3D+resource_endpoint.endpoint%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0Agroup+by%0D%0A++source_pipeline.pipeline"
    if pipeline:
        query = (
            "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++count%28DISTINCT+resource.resource%29+as+total%2C%0D%0A++COUNT%28%0D%0A++++DISTINCT+CASE%0D%0A++++++WHEN+resource.end_date+%3D%3D+%27%27+THEN+resource.resource%0D%0A++++++WHEN+strftime%28%27%25Y%25m%25d%27%2C+resource.end_date%29+%3E%3D+strftime%28%27%25Y%25m%25d%27%2C+%27now%27%29+THEN+resource.resource%0D%0A++++END%0D%0A++%29+AS+active_resources%2C%0D%0A++COUNT%28%0D%0A++++DISTINCT+CASE%0D%0A++++++WHEN+resource.end_date+%21%3D+%27%27%0D%0A++++++AND+strftime%28%27%25Y%25m%25d%27%2C+resource.end_date%29+%3C%3D+strftime%28%27%25Y%25m%25d%27%2C+%27now%27%29+THEN+resource.resource%0D%0A++++END%0D%0A++%29+AS+ended_resources%2C%0D%0A++source_pipeline.pipeline%0D%0Afrom%0D%0A++resource%0D%0A++INNER+JOIN+resource_endpoint+ON+resource.resource+%3D+resource_endpoint.resource%0D%0A++INNER+JOIN+source+ON+source.endpoint+%3D+resource_endpoint.endpoint%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0Awhere%0D%0Asource_pipeline.pipeline+%3D+%3Apipeline%0D%0Agroup+by%0D%0A++source_pipeline.pipeline&pipeline="
            + pipeline
        )
    results = ds.sqlQuery(query)
    return [create_dict(results["columns"], row) for row in results["rows"]]


def first_and_last_resource(pipeline=None):
    ds = DLDatasette()
    query = "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++resource.resource%2C%0D%0A++MAX%28resource.start_date%29+AS+latest%2C%0D%0A++MIN%28resource.start_date%29+AS+first%2C%0D%0A++source_pipeline.pipeline%0D%0Afrom%0D%0A++resource%0D%0A++INNER+JOIN+resource_endpoint+ON+resource.resource+%3D+resource_endpoint.resource%0D%0A++INNER+JOIN+source+ON+resource_endpoint.endpoint+%3D+source.endpoint%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0Agroup+by%0D%0A++source_pipeline.pipeline%0D%0Aorder+by%0D%0A++resource.start_date+DESC"
    results = ds.sqlQuery(query)
    return [create_dict(results["columns"], row) for row in results["rows"]]


def get_datasets(filter=None):
    ds = DLDatasette()
    where_clause = ""
    params = ""
    if filter:
        where_clause, params = DLDatasette.sql_for_filter(
            filter, {"active": "dataset_active", "theme": "dataset_theme.theme"}
        )
    query = "https://datasette.digital-land.info/digital-land.json?sql=SELECT%0D%0A++DISTINCT+dataset.dataset%2C%0D%0A++dataset.name%2C%0D%0A++dataset.plural%2C%0D%0A++dataset.typology%2C%0D%0A++%28%0D%0A++++CASE%0D%0A++++++WHEN+pipeline.pipeline+IS+NOT+NULL+THEN+1%0D%0A++++++WHEN+pipeline.pipeline+IS+NULL+THEN+0%0D%0A++++END%0D%0A++%29+AS+dataset_active%2C%0D%0A++GROUP_CONCAT%28dataset_theme.theme%2C+%22%3B%22%29+AS+dataset_themes%0D%0AFROM%0D%0A++dataset%0D%0A++LEFT+JOIN+pipeline+ON+dataset.dataset+%3D+pipeline.pipeline%0D%0A++INNER+JOIN+dataset_theme+ON+dataset.dataset+%3D+dataset_theme.dataset%0D%0A{}group+by%0D%0A++dataset.dataset%0D%0Aorder+by%0D%0Adataset.name+ASC{}".format(
        where_clause, params
    )
    results = ds.sqlQuery(query)
    return [create_dict(results["columns"], row) for row in results["rows"]]


def get_datasets_info(split=False):
    ds = DLDatasette()
    query = "https://datasette.digital-land.info/digital-land.json?sql=SELECT%0D%0A++DISTINCT+dataset.dataset%2C%0D%0A++dataset.name%2C%0D%0A++dataset.plural%2C%0D%0A++dataset.typology%2C%0D%0A++%28%0D%0A++++CASE%0D%0A++++++WHEN+pipeline.pipeline+IS+NOT+NULL+THEN+1%0D%0A++++END%0D%0A++%29+AS+dataset_active%2C%0D%0A++GROUP_CONCAT%28dataset_theme.theme%2C+%22%3B%22%29+AS+themes%0D%0AFROM%0D%0A++dataset%0D%0A++LEFT+JOIN+pipeline+ON+dataset.dataset+%3D+pipeline.pipeline%0D%0A++INNER+JOIN+dataset_theme+ON+dataset.dataset+%3D+dataset_theme.dataset%0D%0Agroup+by%0D%0Adataset.dataset"
    results = ds.sqlQuery(query)
    if split:
        return {
            "active": [
                create_dict(results["columns"], row)
                for row in results["rows"]
                if row[4] == 1
            ],
            "inactive": [
                create_dict(results["columns"], row)
                for row in results["rows"]
                if row[4] != 1
            ],
        }
    return [create_dict(results["columns"], row) for row in results["rows"]]


def get_organisation(id):
    ds = DLDatasette()
    query = (
        "https://datasette.digital-land.info/digital-land/organisation.json?_sort=organisation&organisation__exact="
        + id
    )
    results = ds.sqlQuery(query)
    return create_dict(results["columns"], results["rows"][0])


def get_resource_count():
    ds = DLDatasette()
    query = "http://datasette.digital-land.info/digital-land.json?sql=select+count%28distinct+resource%29+from+resource"
    results = ds.sqlQuery(query)
    return results["rows"][0][0]


def get_datasets_summary():
    # get all the datasets listed with their active status
    all_datasets = index_by("dataset", get_datasets_info())
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

    print(all_datasets)
    print("MISSING")
    print(set(missing))

    return all_datasets


def content_type_counts(pipeline=None):
    ds = DLDatasette()
    query = "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++content_type%2C%0D%0A++count%28DISTINCT+resource%29+AS+resource_count%0D%0Afrom%0D%0A++log%0D%0Agroup+by%0D%0A++content_type%0D%0A"
    if pipeline:
        query = (
            "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++content_type%2C%0D%0A++count%28DISTINCT+resource%29+AS+resource_count%0D%0Afrom%0D%0A++log%0D%0A++INNER+JOIN+source+ON+log.endpoint+%3D+source.endpoint%0D%0A++INNER+JOIN+source_pipeline+on+source.source+%3D+source_pipeline.source%0D%0Awhere%0D%0Asource_pipeline.pipeline+%3D+%3Apipeline%0D%0Agroup+by%0D%0A++content_type%0D%0A&pipeline="
            + pipeline
        )
    results = ds.sqlQuery(query)
    return sorted(
        [create_dict(results["columns"], row) for row in results["rows"]],
        key=lambda x: x["resource_count"],
        reverse=True,
    )


def resources_of_type(t):
    ds = DLDatasette()
    query = (
        "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++log.content_type%2C%0D%0A++log.resource%0D%0Afrom%0D%0A++log%0D%0A++INNER+JOIN+source+ON+log.endpoint+%3D+source.endpoint%0D%0A++INNER+JOIN+source_pipeline+on+source.source+%3D+source_pipeline.source%0D%0Awhere%0D%0A++log.content_type+%3D+%3Atype%0D%0Agroup+by%0D%0A+log.resource&type="
        + t
    )
    results = ds.sqlQuery(query)
    return [create_dict(results["columns"], row) for row in results["rows"]]


def entry_count(dataset, resource=None):
    ds = DLDatasette()
    query = "https://datasette.digital-land.info/{}.json?sql=select%0D%0A++resource%2C%0D%0A++count%28id%29+AS+entries%0D%0Afrom%0D%0A++entry%0D%0Agroup+by%0D%0Aresource".format(
        dataset
    )
    if resource is not None:
        query = "https://datasette.digital-land.info/{}.json?sql=select%0D%0A++resource%2C%0D%0A++count%28id%29+AS+entries%0D%0Afrom%0D%0A++entry%0D%0Awhere%0D%0A++resource+%3D+%3Aresource%0D%0Agroup+by%0D%0A++resource&resource={}".format(
            dataset, resource
        )
    results = ds.sqlQuery(query)
    return [create_dict(results["columns"], row) for row in results["rows"]]


def get_theme():
    ds = DLDatasette()
    query = "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++name%2C%0D%0A++theme%0D%0Afrom%0D%0A++theme%0D%0Aorder+by%0D%0A++theme%0D%0A"
    results = ds.sqlQuery(query)
    return [create_dict(results["columns"], row) for row in results["rows"]]


def get_typology():
    ds = DLDatasette()
    query = "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++name%2C%0D%0A++typology%0D%0Afrom%0D%0A++typology%0D%0Aorder+by%0D%0A++typology"
    results = ds.sqlQuery(query)
    return [create_dict(results["columns"], row) for row in results["rows"]]


def dataset_latest_logs():
    ds = DLDatasette()
    query = "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++source_pipeline.pipeline%2C%0D%0A++MAX%28log.entry_date%29+AS+latest_attempt%0D%0Afrom%0D%0A++source%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0A++INNER+JOIN+log+ON+source.endpoint+%3D+log.endpoint%0D%0Agroup+by%0D%0Asource_pipeline.pipeline%0D%0A%0D%0A"
    results = ds.sqlQuery(query)
    return index_by(
        "pipeline", [create_dict(results["columns"], row) for row in results["rows"]]
    )
