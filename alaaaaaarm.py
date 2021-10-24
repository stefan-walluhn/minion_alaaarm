import logging

from alaaarm.config import config
from alaaarm.handlers import log_handler
from alaaarm.pushover.client import PushoverClient


log = logging.getLogger()


if __name__ == '__main__':
    pcl = PushoverClient(config['pushover']['email'],
                         config['pushover']['password'])
    log.info('starting PushOver client, wait for messages')
    pcl.wait_for_messages(log_handler)
    log.critical('PushOver client finished')
