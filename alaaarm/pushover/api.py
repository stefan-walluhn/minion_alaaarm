try:
    import requests
except ImportError:
    from alaaarm import requests


class Gateway:
    API_URL = 'https://api.pushover.net/1'

    def login(self, email, password):
        response = requests.post(self._to_api_url('users/login.json'),
                                 data={'email': email, 'password': password})

        return response.json()

    def create_device(self, secret, name):
        response = requests.post(
            self._to_api_url('devices.json'),
            data={'secret': secret, 'name': name, 'os': 'O'}
        )

        return response.json()

    def get_messages(self, secret, device_id):
        response = requests.get(
            self._to_api_url('messages.json'),
            params={'secret': secret, 'device_id': device_id})

        return response.json()

    def update_highest_message(self, secret, device_id, message_id):
        response = requests.post(
            self._to_api_url(
                '/'.join(['devices', device_id, 'update_highest_message.json'])
            ),
            data={'secret': secret, 'message': message_id}
        )

        return response.json()

    def websocket(self):
        from uwebsockets import client

        return client.connect('wss://client.pushover.net/push')

    def _to_api_url(self, endpoint):
        return '/'.join([Gateway.API_URL, endpoint])


pushover_api = Gateway()
