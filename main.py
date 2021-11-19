import ulogging as logging

from alaaarm import bootstrap
from alaaarm.config import config
from alaaarm import filters
from alaaarm import handlers
from alaaarm.pushover.frame import Frame


WATCHDOG_TIMEOUT_MINUTE = 2
ALARM_GPIO = 16
NTP_SYNC_EVERY_HOUR = 1


log = logging.getLogger()


def run():
    alarm_pin = bootstrap.init_pin(ALARM_GPIO)

    dog = bootstrap.init_watchdog(WATCHDOG_TIMEOUT_MINUTE * 60 * 1000)

    bootstrap.init_console_syslog()

    if 'wifi' in config:
        bootstrap.init_wifi(config['wifi']['essid'],
                            config['wifi']['password'])
        dog.feed()

    if 'syslog' in config:
        bootstrap.init_remote_syslog(config['syslog']['host'],
                                     config['syslog']['port'])
        dog.feed()

    bootstrap.init_rtc(NTP_SYNC_EVERY_HOUR * 3600 * 1000)

    pushover_client = bootstrap.init_pushover_client(
        config['pushover']['email'],
        config['pushover']['password'],
        config['pushover']['device_name'],
        config['pushover']['device_id']
    )
    dog.feed()

    log.info('starting Pushover client')
    pushover_client.wait_for_frames(
        handlers.multiplex_handler(
            handlers.log_handler,
            filters.frame_filter(
                Frame.NEW_MESSAGE,
                filters.do_not_disturb_filter(
                    config['do_not_disturb']['before'],
                    config['do_not_disturb']['after'],
                    handlers.pin_handler(alarm_pin)
                )
            ),
            filters.frame_filter(Frame.KEEP_ALIVE,
                                 handlers.watchdog_handler(dog))
        )
    )
    log.critical('Pushover client finished')


if __name__ == '__main__':
    run()
