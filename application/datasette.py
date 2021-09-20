import requests


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
        r = requests.get(query)
        return r.json()


def sources_with_endpoint():
    # query
    # "http://datasetteawsentityv2-env.eba-gbrdriub.eu-west-2.elasticbeanstalk.com/digital-land/source.json?_sort=rowid&endpoint__notblank=1&_labels=on"
    ds = DLDatasette()

    endpoint_results = ds.query("source", {"endpoint__notblank": 1, "_labels": "on"})

    # http://datasetteawsentityv2-env.eba-gbrdriub.eu-west-2.elasticbeanstalk.com/digital-land/source?_sort=rowid&documentation_url__isblank=1&endpoint__notblank=1
    no_documentation_url_results = ds.query(
        "source",
        {"endpoint__notblank": 1, "documentation_url__isblank": 1, "_labels": "on"},
    )

    return {
        "with_endpoint": endpoint_results["filtered_table_rows_count"],
        "no_documentation": {
            "count": no_documentation_url_results["filtered_table_rows_count"],
            "rows": no_documentation_url_results["rows"],
        },
    }
