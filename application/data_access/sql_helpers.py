import urllib.parse


def generate_sql_where_str(filters, mappings={}):
    if len(filters.keys()) == 0:
        return ""
    clauses = []
    for filter, value in filters.items():
        column = filter
        if filter in mappings.keys():
            column = mappings[filter]
        clauses.append("{} LIKE :{}".format(column, filter))
    return "WHERE " + " AND ".join(clauses)


def prepare_query_str(lines):
    query_str = " ".join(lines)
    return urllib.parse.quote(query_str)
