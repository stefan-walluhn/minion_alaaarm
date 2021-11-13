import time
import ulogging as logging

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


def pin_handler(pin):
    def _handler(frm):
        if frm == frame.NEW_MESSAGE:
            pin.on()
            time.sleep(0.2)
            pin.off()

    return _handler


def watchdog_handler(dog):
    def _handler(frm):
        if frm == frame.KEEP_ALIVE:
            dog.feed()

    return _handler


def multiplex_handler(*handlers):
    def _handler(frm):
        for handler in handlers:
            handler(frm)

    return _handler
