import time
import ulogging as logging

from alaaarm.pushover.client import PushoverClient


log = logging.getLogger()


def init_pin(pin_number):
    try:
        from machine import Pin
    except ImportError:
        log.warning('there is no hardware pin, use dummy implementation')
        from alaaarm.pin import DummyPin as Pin

    return Pin(pin_number, Pin.OUT, value=0)


def init_console_syslog():
    from alaaarm.logging import ConsoleHandler
    log.addHandler(ConsoleHandler())


def init_remote_syslog(host, port):
    from alaaarm.logging import RemoteHandler
    log.addHandler(RemoteHandler(host=host, port=port))


def init_rtc():
    try:
        from alaaarm import ntp
    except ImportError:
        log.warning('there is no hardware timer, not syncing rtc')
        return

    ntp.sync_periodic(3600000)


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


def init_pushover_client(email, password, device_name, device_id):
    client = PushoverClient(email, password, device_name, device_id=device_id)
    client.delete_messages()

    return client
