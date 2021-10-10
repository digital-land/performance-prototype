import json
from datetime import datetime

from application.caching import get
from application.utils import create_dict, index_by, months_since, month_dict


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

        # only returns 100
        r = get(query)
        return json.loads(r)

    def sqlQuery(self, query):
        r = get(query)
        return json.loads(r)

    @staticmethod
    def urlencode(s):
        s.replace(":", "%3A")
        return s


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
    # "https://datasette.digital-land.info/digital-land/source.json?_sort=rowid&endpoint__notblank=1&_labels=on"
    ds = DLDatasette()

    endpoint_results = ds.query("source", {"endpoint__notblank": 1, "_labels": "on"})

    # https://datasette.digital-land.info/digital-land/source?_sort=rowid&documentation_url__isblank=1&endpoint__notblank=1
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


def sources_per_dataset_for_organisation(id):
    query = (
        "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++source_pipeline.pipeline+AS+pipeline%2C%0D%0A++COUNT%28DISTINCT+source.source%29+AS+sources%2C%0D%0A++SUM%28CASE+WHEN+%28source.endpoint%29+is+not+null+and+%28source.endpoint%29+%21%3D+%22%22+THEN+1+ELSE+0+END%29++AS+sources_with_endpoint%0D%0Afrom%0D%0A++source%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0Awhere%0D%0A++source.organisation+%3D+%3Aorganisation%0D%0Agroup+by%0D%0A++source_pipeline.pipeline&organisation="
        + DLDatasette.urlencode(id)
    )
    ds = DLDatasette()
    r1 = ds.sqlQuery(query)
    return [create_dict(r1["columns"], row) for row in r1["rows"]]


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


def total_entities():
    query = "https://datasette.digital-land.info/view_model.json?sql=select+count%28*%29+from+entity+order+by+entity"
    ds = DLDatasette()
    results = ds.sqlQuery(query)
    return results["rows"][0][0]


def latest_resource(dataset):
    ds = DLDatasette()
    query = (
        "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++resource.resource%2C%0D%0A++resource.end_date%2C%0D%0A++resource.entry_date%2C%0D%0A++resource.start_date%2C%0D%0A++source_pipeline.pipeline%0D%0Afrom%0D%0A++resource%0D%0A++INNER+JOIN+resource_endpoint+ON+resource.resource+%3D+resource_endpoint.resource%0D%0A++INNER+JOIN+source+ON+resource_endpoint.endpoint+%3D+source.endpoint%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0Awhere%0D%0A++source_pipeline.pipeline+%3D+%3Apipeline%0D%0Aorder+by%0D%0A++resource.start_date+DESC%0D%0Alimit+1&pipeline="
        + dataset
    )
    r1 = ds.sqlQuery(query)
    if len(r1["rows"]):
        return create_dict(r1["columns"], r1["rows"][0])
    return []


def source_monthly_counts(pipeline=None):
    ds = DLDatasette()
    query = "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++strftime%28%27%25Y-%25m%27%2C+source.start_date%29+as+yyyy_mm%2C%0D%0A++count%28distinct+source.source%29%0D%0Afrom%0D%0A++source%0D%0Awhere%0D%0A++source.start_date+%21%3D+%22%22%0D%0Agroup+by%0D%0A++yyyy_mm%0D%0Aorder+by%0D%0A++yyyy_mm"
    if pipeline:
        query = (
            "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++strftime%28%27%25Y-%25m%27%2C+source.start_date%29+as+yyyy_mm%2C%0D%0A++count%28distinct+source.source%29%0D%0Afrom%0D%0A++source%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0Awhere%0D%0A++source.start_date+%21%3D+%22%22%0D%0A++AND+source_pipeline.pipeline+%3D+%3Apipeline%0D%0Agroup+by%0D%0A++yyyy_mm%0D%0Aorder+by%0D%0A++yyyy_mm&pipeline="
            + pipeline
        )
    results = ds.sqlQuery(query)
    return results["rows"]


def resource_monthly_counts(pipeline=None):
    ds = DLDatasette()
    query = "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++strftime%28%27%25Y-%25m%27%2C+resource.start_date%29+as+yyyy_mm%2C%0D%0A++count%28distinct+resource.resource%29%0D%0Afrom%0D%0A++resource%0D%0Awhere%0D%0A++resource.start_date+%21%3D+%22%22%0D%0Agroup+by%0D%0A++yyyy_mm%0D%0Aorder+by%0D%0A++yyyy_mm"
    if pipeline:
        query = (
            "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++strftime%28%27%25Y-%25m%27%2C+resource.start_date%29+as+yyyy_mm%2C%0D%0A++count%28distinct+resource.resource%29%0D%0Afrom%0D%0A++resource%0D%0A++INNER+JOIN+resource_endpoint+ON+resource.resource+%3D+resource_endpoint.resource%0D%0A++INNER+JOIN+endpoint+ON+resource_endpoint.endpoint+%3D+endpoint.endpoint%0D%0A++INNER+JOIN+source+ON+resource_endpoint.endpoint+%3D+source.endpoint%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0Awhere%0D%0A++resource.start_date+%21%3D+%22%22%0D%0A++AND+source_pipeline.pipeline+%3D+%3Apipeline%0D%0Agroup+by%0D%0A++yyyy_mm%0D%0Aorder+by%0D%0A++yyyy_mm&pipeline="
            + pipeline
        )
    results = ds.sqlQuery(query)
    return results["rows"]


def get_monthly_counts(pipeline=None):
    resource_counts = resource_monthly_counts(pipeline)
    source_counts = source_monthly_counts(pipeline)
    first_resource_month_str = resource_counts[0][0]
    first_source_month_str = source_counts[0][0]

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
    ds = DLDatasette()
    query = (
        "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++organisation.name%2C%0D%0A++source.organisation%2C%0D%0A++organisation.end_date+AS+organisation_end_date%2C%0D%0A++COUNT%28DISTINCT+resource.resource%29+AS+resources%2C%0D%0A++COUNT%28%0D%0A++++DISTINCT+CASE%0D%0A++++++WHEN+resource.end_date+%3D%3D+%27%27+THEN+resource.resource%0D%0A++++++WHEN+strftime%28%27%25Y%25m%25d%27%2C+resource.end_date%29+%3E%3D+strftime%28%27%25Y%25m%25d%27%2C+%27now%27%29+THEN+resource.resource%0D%0A++++END%0D%0A++%29+AS+active_resources%2C%0D%0A++COUNT%28DISTINCT+resource_endpoint.endpoint%29+AS+endpoints%2C%0D%0A++COUNT%28DISTINCT+source.source%29+AS+sources%2C%0D%0A++COUNT%28%0D%0A++++DISTINCT+CASE%0D%0A++++++WHEN+source.end_date+%3D%3D+%27%27+THEN+source.source%0D%0A++++++WHEN+strftime%28%27%25Y%25m%25d%27%2C+source.end_date%29+%3E%3D+strftime%28%27%25Y%25m%25d%27%2C+%27now%27%29+THEN+source.source%0D%0A++++END%0D%0A++%29+AS+active_sources%2C%0D%0A++MAX%28resource.start_date%29%2C%0D%0A++Cast+%28%0D%0A++++%28%0D%0A++++++julianday%28%27now%27%29+-+julianday%28MAX%28resource.start_date%29%29%0D%0A++++%29+AS+INTEGER%0D%0A++%29+as+days_since_update%0D%0Afrom%0D%0A++resource%0D%0A++INNER+JOIN+resource_endpoint+ON+resource.resource+%3D+resource_endpoint.resource%0D%0A++INNER+JOIN+endpoint+ON+resource_endpoint.endpoint+%3D+endpoint.endpoint%0D%0A++INNER+JOIN+source+ON+resource_endpoint.endpoint+%3D+source.endpoint%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0A++INNER+JOIN+organisation+ON+source.organisation+%3D+organisation.organisation%0D%0Awhere%0D%0A++source_pipeline.pipeline+%3D+%3Apipeline%0D%0AGROUP+BY%0D%0A++source.organisation&pipeline="
        + pipeline
    )
    results = ds.sqlQuery(query)
    organisations = [create_dict(results["columns"], row) for row in results["rows"]]
    return index_by("organisation", organisations)


def entity_count(pipeline):
    ds = DLDatasette()
    query = f"https://datasette.digital-land.info/{pipeline}.json?sql=select%0D%0A++count%28DISTINCT+entity%29+AS+entities%0D%0Afrom%0D%0A++entity"
    results = ds.sqlQuery(query)
    return results["rows"][0][0]


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


def active_datasets():
    ds = DLDatasette()
    query = "https://datasette.digital-land.info/digital-land/dataset.json?_labels=on"
    results = ds.sqlQuery(query)
    return results["rows"]


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


def get_source(source):
    ds = DLDatasette()
    source_result = ds.query(
        "source",
        {"source__exact": source, "_labels": "on"},
    )
    return source_result["rows"]


def resources_by_dataset():
    ds = DLDatasette()
    query = "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++count%28DISTINCT+resource.resource%29+as+total%2C%0D%0A++COUNT%28%0D%0A++++DISTINCT+CASE%0D%0A++++++WHEN+resource.end_date+%3D%3D+%27%27+THEN+resource.resource%0D%0A++++++WHEN+strftime%28%27%25Y%25m%25d%27%2C+resource.end_date%29+%3E%3D+strftime%28%27%25Y%25m%25d%27%2C+%27now%27%29+THEN+resource.resource%0D%0A++++END%0D%0A++%29+AS+active_resources%2C%0D%0A++COUNT%28%0D%0A++++DISTINCT+CASE%0D%0A++++++WHEN+resource.end_date+%21%3D+%27%27%0D%0A++++++AND+strftime%28%27%25Y%25m%25d%27%2C+resource.end_date%29+%3C%3D+strftime%28%27%25Y%25m%25d%27%2C+%27now%27%29+THEN+resource.resource%0D%0A++++END%0D%0A++%29+AS+ended_resources%2C%0D%0A++source_pipeline.pipeline%0D%0Afrom%0D%0A++resource%0D%0A++INNER+JOIN+resource_endpoint+ON+resource.resource+%3D+resource_endpoint.resource%0D%0A++INNER+JOIN+source+ON+source.endpoint+%3D+resource_endpoint.endpoint%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0Agroup+by%0D%0A++source_pipeline.pipeline"
    results = ds.sqlQuery(query)
    return [create_dict(results["columns"], row) for row in results["rows"]]


def first_and_last_resource(pipeline=None):
    ds = DLDatasette()
    query = "https://datasette.digital-land.info/digital-land.json?sql=select%0D%0A++resource.resource%2C%0D%0A++MAX%28resource.start_date%29+AS+latest%2C%0D%0A++MIN%28resource.start_date%29+AS+first%2C%0D%0A++source_pipeline.pipeline%0D%0Afrom%0D%0A++resource%0D%0A++INNER+JOIN+resource_endpoint+ON+resource.resource+%3D+resource_endpoint.resource%0D%0A++INNER+JOIN+source+ON+resource_endpoint.endpoint+%3D+source.endpoint%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0Agroup+by%0D%0A++source_pipeline.pipeline%0D%0Aorder+by%0D%0A++resource.start_date+DESC"
    results = ds.sqlQuery(query)
    return [create_dict(results["columns"], row) for row in results["rows"]]


def datasets(split=False):
    ds = DLDatasette()
    query = "https://datasette.digital-land.info/digital-land.json?sql=SELECT%0D%0A++DISTINCT+dataset.dataset%2C%0D%0A++dataset.name%2C%0D%0A++%28%0D%0A++++CASE%0D%0A++++++WHEN+pipeline.pipeline+IS+NOT+NULL+THEN+1%0D%0A++++END%0D%0A++%29+AS+dataset_active%2C%0D%0A++GROUP_CONCAT%28dataset_theme.theme%2C+%22%3B%22%29+AS+themes%0D%0AFROM%0D%0A++dataset%0D%0A++LEFT+JOIN+pipeline+ON+dataset.dataset+%3D+pipeline.pipeline%0D%0A++INNER+JOIN+dataset_theme+ON+dataset.dataset+%3D+dataset_theme.dataset%0D%0Agroup+by%0D%0Adataset.dataset"
    results = ds.sqlQuery(query)
    if split:
        return {
            "active": [
                create_dict(results["columns"], row)
                for row in results["rows"]
                if row[2] == 1
            ],
            "inactive": [
                create_dict(results["columns"], row)
                for row in results["rows"]
                if row[2] != 1
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
    all_datasets = index_by("dataset", datasets())
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
