import urllib.parse


def generate_sql_where_str(filters, mappings={}):
    if len(filters.keys()) == 0:
        return "", ""
    clauses = []
    param_str = ""
    for filter, value in filters.items():
        column = filter
        if filter in mappings.keys():
            column = mappings[filter]
        clauses.append("{} LIKE :{}".format(column, filter))
        # To Do: can we get rid of params?
        # these are &param=value items
        param = "&{}={}".format(filter, value)
        param_str = param_str + param
    return "WHERE " + " AND ".join(clauses), param_str


def prepare_query_str(lines):
    query_str = " ".join(lines)
    return urllib.parse.quote(query_str)
