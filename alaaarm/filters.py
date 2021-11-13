import time
import ulogging as logging


log = logging.getLogger()


def frame_filter(frame, handler):
    def _filter(frm):
        if frm == frame:
            handler(frm)

    return _filter


def do_not_disturb_filter(before_hour, after_hour, handler):
    def _filter(frm):
        current_hour = time.localtime()[3]
        if current_hour >= before_hour and current_hour < after_hour:
            handler(frm)
        else:
            log.info('do not disturb, not triggering handler')

    return _filter
