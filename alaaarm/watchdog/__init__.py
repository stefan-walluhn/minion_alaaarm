import ulogging as logging


log = logging.getLogger()


try:
    from machine import WDT
except ImportError:
    log.warning('there is no hardware watchdog, use dummy implementation')
    from alaaarm.watchdog.dummy import DummyWatchdog as WDT
