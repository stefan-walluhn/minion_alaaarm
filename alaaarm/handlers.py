import time
import ulogging as logging

from alaaarm.pushover.frame import Frame, frame_to_str


log = logging.getLogger()


def log_handler(frm):
    try:
        log.info('received frame: %s', frame_to_str(frm))
    except KeyError:
        log.warning('received unknown frame: %s', frm.decode())


def pin_handler(pin):
    def _handler(frm):
        pin.on()
        time.sleep(0.2)
        pin.off()

    return _handler


def watchdog_handler(dog):
    def _handler(frm):
        dog.feed()

    return _handler


def multiplex_handler(*handlers):
    def _handler(frm):
        for handler in handlers:
            handler(frm)

    return _handler
