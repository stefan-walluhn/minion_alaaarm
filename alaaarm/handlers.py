from alaaarm.pushover import msg


def echo_handler(message):
    messages = {
        msg.KEEP_ALIVE: 'KEEP ALIVE',
        msg.NEW_MESSAGE: 'NEW MESSAGE',
        msg.RELOAD: 'RELOAD',
        msg.ERROR: 'ERROR',
        msg.ANOTHER_SESSION: 'ANOTHER SESSION'
    }

    print(messages.get(message, 'Unknown message: {}'.format(message)))
