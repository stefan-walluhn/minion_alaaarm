import ulogging as logging
import usocket as socket

from alaaarm import wifi
from alaaarm.config import config
from alaaarm.handlers import (log_handler,
                              watchdog_handler,
                              multiplex_handler)
from alaaarm.logging import SyslogHandler
from alaaarm.pushover.client import PushoverClient
from alaaarm.watchdog import get_watchdog


WATCHDOG_TIMEOUT_MINUTE = 2


log = logging.getLogger()


def run():
    dog = get_watchdog()(timeout=WATCHDOG_TIMEOUT_MINUTE * 60 * 1000)

    if 'wifi' in config:
        wifi.connect(config['wifi']['essid'], config['wifi']['password'])
        dog.feed()

    if 'syslog' in config:
        syslog_server = socket.getaddrinfo(config['syslog']['host'],
                                           config['syslog']['port'])
        log.addHandler(SyslogHandler(dest=syslog_server))
        dog.feed()

    pcl = PushoverClient(config['pushover']['email'],
                         config['pushover']['password'],
                         config['pushover']['device_name'],
                         device_id=config['pushover']['device_id'])

    handlers = [log_handler, watchdog_handler(dog)]

    log.info('starting Pushover client')
    pcl.delete_messages()
    dog.feed()

    pcl.wait_for_frames(multiplex_handler(handlers))
    log.critical('Pushover client finished')


if __name__ == '__main__':
    run()
