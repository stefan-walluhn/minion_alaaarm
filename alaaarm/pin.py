import ulogging as logging


log = logging.getLogger()


class DummyPin():
    OUT = None


class DummySignal():
    def on(self):
        log.info('pin on')

    def off(self):
        log.info('pin off')
