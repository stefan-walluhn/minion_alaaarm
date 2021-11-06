import ulogging as logging


log = logging.getLogger()


def get_watchdog():
    try:
        from machine import WDT
    except ImportError:
        log.warning('there is no hardware watchdog, use dummy implementation')
        from alaaarm.watchdog.dummy import DummyWatchdog as WDT

    return WDT
