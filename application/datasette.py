import json

from application.caching import get


class DLDatasette:
    BASE_URL = "http://datasetteawsentityv2-env.eba-gbrdriub.eu-west-2.elasticbeanstalk.com/digital-land/"

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
    # "http://datasetteawsentityv2-env.eba-gbrdriub.eu-west-2.elasticbeanstalk.com/digital-land/source.json?_sort=rowid&endpoint__notblank=1&_labels=on"
    ds = DLDatasette()

    endpoint_results = ds.query("source", {"endpoint__notblank": 1, "_labels": "on"})

    # http://datasetteawsentityv2-env.eba-gbrdriub.eu-west-2.elasticbeanstalk.com/digital-land/source?_sort=rowid&documentation_url__isblank=1&endpoint__notblank=1
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


def datasets_per_organisation(id):
    org_id = id.replace(":", "%3A")
    query = (
        "http://datasetteawsentityv2-env.eba-gbrdriub.eu-west-2.elasticbeanstalk.com/digital-land.json?sql=select%0D%0A++resource.resource%2C%0D%0A++resource.end_date%2C%0D%0A++source.source%2C%0D%0A++resource_endpoint.endpoint%2C%0D%0A++endpoint.endpoint_url%2C%0D%0A++source.organisation%2C%0D%0A++source_pipeline.pipeline%0D%0Afrom%0D%0A++resource%0D%0A++INNER+JOIN+resource_endpoint+ON+resource.resource+%3D+resource_endpoint.resource%0D%0A++INNER+JOIN+endpoint+ON+resource_endpoint.endpoint+%3D+endpoint.endpoint%0D%0A++INNER+JOIN+source+ON+resource_endpoint.endpoint+%3D+source.endpoint%0D%0A++INNER+JOIN+source_pipeline+ON+source.source+%3D+source_pipeline.source%0D%0AWHERE%0D%0A++source.organisation+%3D+%3Aorganisation%0D%0AGROUP+BY%0D%0A++resource.resource&organisation="
        + org_id
    )
    ds = DLDatasette()
    results = ds.sqlQuery(query)
    return {
        "resources": results["rows"],
        "datasets_covered": list(set([r[6] for r in results["rows"]])),
    }
