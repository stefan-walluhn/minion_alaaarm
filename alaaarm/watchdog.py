import ulogging as logging


log = logging.getLogger()


class DummyWatchdog():
    def feed(self):
        log.info('feed watchdog')
