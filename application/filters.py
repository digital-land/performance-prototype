from datetime import datetime
import urllib.parse

from shapely import wkt


def clean_int_filter(s):
    # s might be passed in as undefined so need to test for that
    if not s or s == "":
        s = "0"
    if isinstance(s, str):
        s = s.replace(",", "")
        return int(s)
    return s


def to_float_filter(s):
    if s == "":
        s = "0"
    if isinstance(s, str):
        s = s.replace(",", "")
        return float(s)
    return s


def days_since(d):
    today = datetime.now()
    if not isinstance(d, datetime):
        d = datetime.strptime(d, "%Y-%m-%d")
    delta = today - d
    return delta.days


def split_filter(s, d):
    return s.split(d)


def urlencode_filter(s):
    return urllib.parse.quote_plus(s)


def remove_query_param_filter(v, filter_name, current_str):
    query_str = str(current_str)
    if f"{filter_name}={v}" in query_str:
        s = query_str.replace(f"{filter_name}={v}", "")
        return "?" + s.strip("&")
    return "?" + query_str


def unhyphenate(s):
    return s.replace("-", " ")


def pass_fail(v):
    if v is None:
        return "no test"
    if v:
        return "pass"
    return "fail"


def date_time_format(d):
    return d.strftime("%A %d-%m-%Y, %H:%M:%S")


def map_link(entity):
    if entity.get("point") is not None:
        coords = wkt.loads(entity["point"])
        return f"dataset={entity['dataset']}#{coords.y},{coords.x},16z"
    return ""
