import urequests


class Requests:
    @staticmethod
    def get(url, params=None, **kwargs):
        return urequests.get(Requests._to_url_params(url, params), **kwargs)

    @staticmethod
    def post(url, data=None, **kwargs):
        return urequests.post(url,
                              data=Requests._to_x_www_form_urlencoded(data),
                              **kwargs)

    @staticmethod
    def _to_url_params(url, params=None):
        if not params:
            return url

        return '?'.join([url, Requests._url_encode_data(params)])

    @staticmethod
    def _to_x_www_form_urlencoded(data):
        return str.encode(Requests._url_encode_data(data))

    @staticmethod
    def _url_encode_data(data):
        return '&'.join(["=".join([k, str(v)]) for k, v in data.items()])


get = Requests.get
post = Requests.post
