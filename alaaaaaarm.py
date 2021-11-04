import ulogging as logging
import usocket as socket

from alaaarm.config import config
from alaaarm.handlers import log_handler
from alaaarm.logging import SyslogHandler
from alaaarm.pushover.client import PushoverClient


log = logging.getLogger()


if __name__ == '__main__':
    if 'syslog' in config:
        syslog_server = socket.getaddrinfo(config['syslog']['host'],
                                           config['syslog']['port'])
        log.addHandler(SyslogHandler(dest=syslog_server))

    pcl = PushoverClient(config['pushover']['email'],
                         config['pushover']['password'],
                         device_id=config['pushover']['device_id'])

    log.info('starting PushOver client, wait for WebSocket frames')
    pcl.wait_for_frames(log_handler)
    log.critical('PushOver client finished')
