try:
    import logging
except ImportError:
    import ulogging as logging

from alaaarm.pushover import api as pushover_api
from alaaarm.pushover import frame
from alaaarm.pushover.exceptions import (DeviceRegistrationError,
                                         NoMessagesException)


log = logging.getLogger()


class PushoverClient():
    def __init__(self, email, password, device_name, device_id=None):
        self.email = email
        self.password = password
        self.device_name = device_name

        self._secret = None
        self._device_id = device_id

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
        if not self._device_id:
            response = pushover_api.post(
                'devices.json',
                data={'secret': self.secret,
                      'name': self.device_name,
                      'os': 'O'}
            ).json()

            if response['status'] != 1:
                raise DeviceRegistrationError(response['errors'])

            self._device_id = response['id']

        return self._device_id

    def get_messages(self):
        response = pushover_api.get(
            'messages.json',
            params={'secret': self.secret, 'device_id': self.device_id}
        ).json()

        return response['messages']

    def delete_messages(self):
        log.info('deleting all Pushover messages for this device')

        try:
            self._update_highest_message()
        except NoMessagesException:
            pass

    def _update_highest_message(self):
        return pushover_api.post(
            '/'.join(['devices',
                      self.device_id,
                      'update_highest_message.json']),
            data={'secret': self.secret,
                  'message': str(self._get_max_message_id())}
        ).json()

    def _get_max_message_id(self):
        msg_ids = [m['id'] for m in self.get_messages()]
        try:
            return max(msg_ids)
        except ValueError:
            raise NoMessagesException()

    def wait_for_frames(self, handler):
        log.info('waiting for Pushover frames')
        # pre-fetch data to reduce parallel ssl connections
        self.device_id
        self.secret

        while True:
            with pushover_api.websocket() as ws:
                ws.send('login:{device_id}:{secret}\n'.format(
                    device_id=self.device_id, secret=self.secret)
                )

                while True:
                    response = ws.recv()
                    handler(response)
                    if response == frame.RELOAD:
                        # reload request, reconnect
                        log.warning('received reload request, reconnecting')
                        break
                    if response == frame.ERROR:
                        # permanent error, terminate
                        log.warning('received permanent error, '
                                    'stop frame processing')
                        return
                    if response == frame.ANOTHER_SESSION:
                        # session closed, terminate
                        log.warning('another session was started, '
                                    'stop frame processing')
                        return
