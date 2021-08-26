def clean_int_filter(s):
    if s == "":
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
