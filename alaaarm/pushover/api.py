try:
    from alaaarm import requests
except ModuleNotFoundError:
    import requests


API_URL = 'https://api.pushover.net/1'


def _to_api_url(endpoint):
    return '/'.join([API_URL, endpoint])


def get(endpoint, *args, **kwargs):
    return requests.get(_to_api_url(endpoint), *args, **kwargs)


def post(endpoint, *args, **kwargs):
    return requests.post(_to_api_url(endpoint), *args, **kwargs)


def websocket():
    from  uwebsockets import client

    return client.connect('wss://client.pushover.net/push')
