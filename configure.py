import click
import json

from alaaarm.pushover.client import PushoverClient
from alaaarm.pushover.exceptions import DeviceRegistrationError


@click.command()
@click.option('-e', '--email', prompt=True, help="Pushover email")
@click.option('--password', prompt=True, hide_input=True)
def configure(email, password):
    config = {'pushover': {'email': email, 'password': password}}

    pushover_client = PushoverClient(email, password)
    try:
        config['pushover']['device_id'] = pushover_client.device_id
    except DeviceRegistrationError as e:
        raise click.ClickException(
            f'failed to register pushover device: {e}')

    click.echo(json.dumps(config, sort_keys=True, indent=4))


if __name__ == '__main__':
    configure()
