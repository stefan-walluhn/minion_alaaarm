from alaaarm.config import config
from alaaarm.handlers import echo_handler
from alaaarm.pushover.client import PushoverClient


if __name__ == '__main__':
    pcl = PushoverClient(config['pushover']['email'],
                         config['pushover']['password'])
    pcl.wait_for_messages(echo_handler)
