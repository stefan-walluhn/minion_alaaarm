try:
    import logging
except ImportError:
    import ulogging as logging

from alaaarm.pushover.api import pushover_api
from alaaarm.pushover.frame import Frame
from alaaarm.pushover.exceptions import DeviceRegistrationError



log = logging.getLogger()


class PushoverClient():
    def __init__(self, email, password, device_name=None, device_id=None):
        self.email = email
        self.password = password
        self.device_name = device_name

        self._secret = None
        self._device_id = device_id

    @property
    def secret(self):
        if not self._secret:
            response = pushover_api.login(self.email, self.password)
            self._secret = response['secret']

        return self._secret

    @property
    def device_id(self):
        if not self._device_id:
            response = pushover_api.create_device(self.secret,
                                                  self.device_name)

            if response['status'] != 1:
                raise DeviceRegistrationError(response['errors'])

            self._device_id = response['id']

        return self._device_id

    def delete_messages(self):
        log.info('deleting all Pushover messages for this device')

        pushover_api.update_highest_message(self.secret,
                                            self.device_id,
                                            (1 << 128) - 1)

    def wait_for_frames(self, handler,
                        reconnect_after_frames=1000,
                        delete_messages_on_reconnect=True):
        # pre-fetch data to reduce parallel ssl connections
        self.device_id
        self.secret

        while True:
            with pushover_api.websocket() as ws:
                ws.send(f'login:{self.device_id}:{self.secret}\n')

                log.info('logged in, waiting for Pushover frames')
                for _ in range(reconnect_after_frames):
                    response = ws.recv()
                    handler(response)
                    if response == Frame.RELOAD:
                        # reload request, reconnect
                        log.warning('received reload request, reconnecting')
                        break
                    if response == Frame.ERROR:
                        # permanent error, terminate
                        log.warning('received permanent error, '
                                    'stop frame processing')
                        return
                    if response == Frame.ANOTHER_SESSION:
                        # session closed, terminate
                        log.warning('another session was started, '
                                    'stop frame processing')
                        return

            if delete_messages_on_reconnect:
                self.delete_messages()

            log.info('reconnecting')
