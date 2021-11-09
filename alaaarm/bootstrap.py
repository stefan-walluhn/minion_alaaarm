import time
import ulogging as logging
import usocket as socket


log = logging.getLogger()


def init_pin(pin_number):
    try:
        from machine import Pin, Signal
    except ImportError:
        log.warning('there is no hardware pin, use dummy implementation')
        from alaaarm.pin import DummyPin as Pin, DummySignal as Signal

    return Pin(pin_number, Pin.OUT, value=0)


def init_syslog(host, port):
    from alaaarm.logging import SyslogHandler

    syslog_server = socket.getaddrinfo(host, port)
    log.addHandler(SyslogHandler(dest=syslog_server))


def init_watchdog(timeout):
    try:
        from machine import WDT
    except ImportError:
        log.warning('there is no hardware watchdog, use dummy implementation')
        from alaaarm.watchdog import DummyWatchdog as WDT

    return WDT(timeout=timeout)


def init_wifi(essid, password):
    import network

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(essid, password)

        while not wlan.isconnected():
            time.sleep(1)
