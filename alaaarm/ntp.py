import ntptime
import ulogging as logging
from machine import Timer


log = logging.getLogger()


def sync():
    ntptime.settime()
    log.info('synced rtc using ntp')


def sync_periodic(period):
    Timer(0).init(period=period,
                  mode=Timer.PERIODIC,
                  callback=lambda t: ntp.sync())

    sync()
