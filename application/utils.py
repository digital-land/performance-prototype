import json
import datetime
from dateutil.relativedelta import *


def create_dict(keys_list, values_list):
    zip_iterator = zip(keys_list, values_list)
    return dict(zip_iterator)


def index_by(key_field, dict_list):
    idx = {}
    for d in dict_list:
        if key_field in d.keys():
            idx.setdefault(d[key_field], {})
            idx[d[key_field]] = d
    return idx


def index_with_list(key_field, dict_list):
    idx = {}
    for d in dict_list:
        if key_field in d.keys():
            idx.setdefault(d[key_field], [])
            idx[d[key_field]].append(d)
    return idx


def this_month():
    n = datetime.datetime.now()
    return datetime.strptime(n, "%Y-%m")


def months_since(start_date):
    end_date = datetime.datetime.now()
    return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)


def month_dict(num_months):
    counts = {}
    today = datetime.datetime.now()
    for m in list(reversed(range(0, num_months + 1))):
        counts.setdefault((today - relativedelta(months=m)).strftime("%Y-%m"), 0)
    return counts


def resources_per_publishers(resources):
    publishers = {}
    for resource in resources:
        publishers.setdefault(resource["organisation"], [])
        if not resource["resource"] in publishers[resource["organisation"]]:
            publishers[resource["organisation"]].append(resource["resource"])
    return publishers


def yesterday(string=False, frmt="%Y-%m-%d"):
    yesterday = datetime.datetime.now() - datetime.timedelta(1)
    if string:
        return yesterday.strftime(frmt)
    return yesterday


def recent_dates(days=1, frmt="%Y-%m-%d"):
    today = datetime.datetime.now()
    return [(today - datetime.timedelta(d)).strftime(frmt) for d in range(1, days + 1)]


def read_json_file(data_file_path):
    f = open(
        data_file_path,
    )
    data = json.load(f)
    f.close()
    return data
