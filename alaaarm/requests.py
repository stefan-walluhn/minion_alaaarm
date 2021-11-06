import urequests


def to_url_params(url, params=None):
    if not params:
        return url

    return '?'.join([url, '&'.join(["=".join(i) for i in params.items()])])


def to_x_www_form_urlencoded(data):
    return str.encode('&'.join(["=".join(i) for i in data.items()]))


def get(url, params=None, **kwargs):
    return urequests.get(to_url_params(url, params), **kwargs)


def post(url, data=None, **kwargs):
    return urequests.post(url, data=to_x_www_form_urlencoded(data), **kwargs)
