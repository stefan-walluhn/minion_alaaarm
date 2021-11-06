import ulogging as logging
import usocket as socket

from alaaarm import watchdog
from alaaarm import wifi
from alaaarm.config import config
from alaaarm.handlers import (log_handler,
                              watchdog_handler,
                              multiplex_handler)
from alaaarm.logging import SyslogHandler
from alaaarm.pushover.client import PushoverClient


log = logging.getLogger()


def run():
    if 'wifi' in config:
        wifi.connect(config['wifi']['essid'], config['wifi']['password'])

    if 'syslog' in config:
        syslog_server = socket.getaddrinfo(config['syslog']['host'],
                                           config['syslog']['port'])
        log.addHandler(SyslogHandler(dest=syslog_server))

    pcl = PushoverClient(config['pushover']['email'],
                         config['pushover']['password'],
                         device_id=config['pushover']['device_id'])

    handlers = [log_handler,
                watchdog_handler(watchdog.WDT(timeout=120000))]

    log.info('starting Pushover client')
    pcl.delete_messages()
    pcl.wait_for_frames(multiplex_handler(handlers))
    log.critical('Pushover client finished')


if __name__ == '__main__':
    run()
