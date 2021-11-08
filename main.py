import ulogging as logging

from alaaarm import bootstrap
from alaaarm.config import config
from alaaarm.handlers import (log_handler,
                              pin_handler,
                              watchdog_handler,
                              multiplex_handler)
from alaaarm.pushover.client import PushoverClient


WATCHDOG_TIMEOUT_MINUTE = 2
ALARM_GPIO = 16


log = logging.getLogger()


def run():
    alarm_pin = bootstrap.init_pin(ALARM_GPIO)
    dog = bootstrap.init_watchdog(WATCHDOG_TIMEOUT_MINUTE * 60 * 1000)

    if 'wifi' in config:
        bootstrap.init_wifi(config['wifi']['essid'],
                            config['wifi']['password'])
        dog.feed()

    if 'syslog' in config:
        bootstrap.init_syslog(config['syslog']['host'],
                              config['syslog']['port'])
        dog.feed()

    pcl = PushoverClient(config['pushover']['email'],
                         config['pushover']['password'],
                         config['pushover']['device_name'],
                         device_id=config['pushover']['device_id'])

    handlers = [log_handler, pin_handler(alarm_pin), watchdog_handler(dog)]

    log.info('starting Pushover client')
    pcl.delete_messages()
    dog.feed()

    pcl.wait_for_frames(multiplex_handler(handlers))
    log.critical('Pushover client finished')


if __name__ == '__main__':
    run()
