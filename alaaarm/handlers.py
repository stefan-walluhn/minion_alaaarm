import logging

from alaaarm.pushover import msg


log = logging.getLogger()


messages = {
    msg.KEEP_ALIVE: 'KEEP ALIVE',
    msg.NEW_MESSAGE: 'NEW MESSAGE',
    msg.RELOAD: 'RELOAD',
    msg.ERROR: 'ERROR',
    msg.ANOTHER_SESSION: 'ANOTHER SESSION'
}


def echo_handler(message):
    print(messages.get(message, 'Unknown message: {}'.format(message)))


def log_handler(message):
    log.info('received message: %s',
             messages.get(message, 'Unknown message: {}'.format(message)))
