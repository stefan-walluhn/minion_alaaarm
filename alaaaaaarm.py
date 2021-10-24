import logging
import usocket as socket

from alaaarm.config import config
from alaaarm.handlers import log_handler
from alaaarm.logging import SyslogHandler
from alaaarm.pushover.client import PushoverClient


log = logging.getLogger()


if __name__ == '__main__':
    log.addHandler(
        SyslogHandler(dest=socket.getaddrinfo(config['syslog']['host'],
                                              config['syslog']['port']))
    )
    pcl = PushoverClient(config['pushover']['email'],
                         config['pushover']['password'])
    log.info('starting PushOver client, wait for WebSocket frames')
    pcl.wait_for_frames(log_handler)
    log.critical('PushOver client finished')
