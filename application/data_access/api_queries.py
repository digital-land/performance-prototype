from application.caching import get

API_URL = "https://www.digital-land.info/entity.json"

# TODO move to local db
def get_entities(parameters):
    params = ""
    for p, v in parameters.items():
        prefix = "?" if params == "" else "&"
        params = params + prefix + f"{p}={v}"
    url = f"{API_URL}{params}"
    result = get(url, format="json")
    return result["entities"]


def get_organisation_entity(prefix, reference):
    return get_entities({"prefix": prefix, "reference": reference})


def get_organisation_entity_number(prefix, reference):
    results = get_organisation_entity(prefix, reference)
    if len(results):
        return results[0]["entity"]
    return None
