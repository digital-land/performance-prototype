import urllib.parse

from application.caching import get
from application.utils import create_dict
from flask import abort


DATASETTE_URL = "https://datasette.digital-land.info"


# TODO - this data is not in digital land db but each dataset has own
# database so unless we download every sqlite db for each dataset
# this will have to carry on using datasette for the moment
def fetch_resource_from_dataset(database_name, resource):
    query_lines = [
        "SELECT",
        "*",
        "FROM",
        "dataset_resource",
        "WHERE",
        f"resource = '{resource}'",
    ]
    query_str = " ".join(query_lines)
    query = urllib.parse.quote(query_str)
    url = f"{DATASETTE_URL}/{database_name}.json?sql={query}"
    result = get(url, format="json")
    if not result or not result["rows"]:
        return abort(404)
    return create_dict(result["columns"], result["rows"][0])


def fetch_entry_count(database_name, resource):
    r = fetch_resource_from_dataset(database_name, resource)
    return r["entry_count"]
