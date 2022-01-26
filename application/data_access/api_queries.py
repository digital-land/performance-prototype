from application.caching import get

API_URL = "https://www.digital-land.info/entity.json"


def get_entities(parameters):
    params = ""
    for p, v in parameters.items():
        prefix = "?" if params == "" else "&"
        params = params + prefix + f"{p}={v}"
    url = f"{API_URL}{params}"
    return get(url, format="json")
