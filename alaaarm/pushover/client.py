import logging

from alaaarm.pushover import api as pushover_api
from alaaarm.pushover import msg


log = logging.getLogger()


class PushoverClient():
    def __init__(self, email, password):
        self.email = email
        self.password = password

        self._secret = None
        self._device_id = None

    @property
    def secret(self):
        if not self._secret:
            self._secret = pushover_api.post(
                'users/login.json',
                data={'email': self.email, 'password': self.password}
            ).json()['secret']

        return self._secret

    @property
    def device_id(self):
        # XXX device `python_test` must not exists!
        if not self._device_id:
            self._device_id = pushover_api.post(
                'devices.json',
                data={'secret': self.secret, 'name': 'python_test', 'os': 'O'}
            ).json()['id']

        return self._device_id

    def get_messages(self):
        response = pushover_api.get(
            'messages.json',
            params={'secret': self.secret, 'device_id': self.device_id}
        )

        return response.json()

    def wait_for_messages(self, handler):
        while True:
            with pushover_api.websocket() as ws:
                ws.send('login:{device_id}:{secret}\n'.format(
                    device_id=self.device_id, secret=self.secret)
                )

                while True:
                    response = ws.recv()
                    handler(response)
                    if response == msg.RELOAD:
                        # reload request, reconnect
                        log.warning('received reload request, reconnecting')
                        break
                    if response == msg.ERROR:
                        # permanent error, terminate
                        log.warning('received permanent error, '
                                    'stop message processing')
                        return
                    if response == msg.ANOTHER_SESSION:
                        # session closed, terminate
                        log.warning('another session was started, '
                                    'stop message processing')
                        return
