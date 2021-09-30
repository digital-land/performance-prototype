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
