from math import ceil
import re


# The str extracted by re are converted to JSON
def re_str_to_json(info_str):
    regex = re.compile(r'\\(?![/u"])')
    fixed = regex.sub(r"\\\\", info_str)
    return fixed


money_sign = ["$", ","]



def str_to_int(s):
    try:
        if s is not None and (isinstance(s, str)):
            s = s.replace(",", "").replace(" ", "").replace("$", "")
            return int(str(s))
        else:
            return int(s)
    except Exception as e:
        raise e


def str_to_float(s):
    try:
        if s is not None and (isinstance(s, str)):
            s = s.replace(",", "").replace(" ", "").replace("$", "")
            return float(str(s))
        else:
            return float(s)
    except Exception as e:
        raise e


def get_ceil(nominator, denominator):
    try:
        return int(ceil(1.0*nominator/denominator))
    except Exception as e:
        raise e


# def unicode_get(s, d):
#     try:
#         return d.get(unicode(s))
#     except Exception as e:
#         raise e


def cleanUp_string(s):
    try:
        return s.replace('&#39;', "'")
    except Exception as e:
        raise e


def extract_decimal(val):
    if val:
        result = re.search(r"(\d[\d\,\.]*)", str(val),  re.I | re.S)
        if result:
            return result.group(1)
    return None

# print extract_decimal("asd456.4")
def utf8_to_unicode(v):
    try:
        if v:
            val = str(v)
            return val.encode("unicode_escape")
    except Exception as e:
        raise e
    return ''

def get_full_url(base_url, url):
    url_str = str(url)
    if url_str.startswith('http'):
        return url_str
    elif url_str.startswith('/'):
        return base_url + url_str
    else:
        return base_url + '/' + url_str



