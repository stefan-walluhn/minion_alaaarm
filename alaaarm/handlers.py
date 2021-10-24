import logging

from alaaarm.pushover import frame


log = logging.getLogger()


frames = {
    frame.KEEP_ALIVE: 'KEEP ALIVE',
    frame.NEW_MESSAGE: 'NEW MESSAGE',
    frame.RELOAD: 'RELOAD',
    frame.ERROR: 'ERROR',
    frame.ANOTHER_SESSION: 'ANOTHER SESSION'
}


def echo_handler(frm):
    print(frames.get(frm, 'Unknown frame: {}'.format(frm)))


def log_handler(frm):
    log.info('received frame: %s',
             frames.get(frm, 'Unknown frame ({})'.format(frm)))
