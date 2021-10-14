import asyncio
import click
import requests
import websockets
from playsound import playsound


class PushoverClient():
    def __init__(self, email, password):
        self.email = email
        self.password = password

        self._secret = None
        self._device_id = None

    @property
    def secret(self):
        if not self._secret:
            self._secret = requests.post(
                'https://api.pushover.net/1/users/login.json',
                data={'email': self.email, 'password': self.password}
            ).json()['secret']

        return self._secret

    @property
    def device_id(self):
        # XXX device `python_test` must not exists!
        if not self._device_id:
            self._device_id = requests.post(
                'https://api.pushover.net/1/devices.json',
                data={'secret': self.secret,
                      'name': 'python_test',
                      'os': 'O'}
            ).json()['id']

        return self._device_id

    def get_messages(self):
        response = requests.get('https://api.pushover.net/1/messages.json',
                                params={'secret': self.secret,
                                        'device_id': self.device_id})
        return response.json()

    async def notifications(self):
        async with websockets.connect('wss://client.pushover.net/push') as ws:
            await ws.send('login:{device_id}:{secret}\n'.format(
                device_id=self.device_id, secret=self.secret)
            )
            while True:
                response = await ws.recv()
                if response == b'!':
                    playsound('alaaarm.webm')




@click.command()
@click.option('-e', '--email',
              required=True,
              help='Pushover account e-mail address')
@click.option('-p', '--password', prompt=True, hide_input=True)
def pushover_client(email, password):
    pcl = PushoverClient(email, password)
    pcl.get_messages()

    asyncio.run(pcl.notifications())


if __name__ == '__main__':
    pushover_client()
