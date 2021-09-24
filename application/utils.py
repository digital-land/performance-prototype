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
