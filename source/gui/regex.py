from math import inf


def number(min_length: int = 0, max_length: int = inf) -> str:
    return r"\d{%s,%s}" % (min_length, max_length if max_length < inf else "")


ipv4_check, ipv4_type = r"\d{1,3}(\.\d{1,3}){3}", r"[\d\.]{0,15}"
port_check, port_type = number(min_length=1, max_length=5), number(min_length=0, max_length=5)

username_check, username_type = r".{1,16}", r".{0,16}"

