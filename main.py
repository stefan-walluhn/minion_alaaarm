import ulogging as logging

from alaaarm import bootstrap
from alaaarm.config import config
from alaaarm.handlers import (log_handler,
                              pin_handler,
                              watchdog_handler,
                              multiplex_handler)


WATCHDOG_TIMEOUT_MINUTE = 2
ALARM_GPIO = 16


log = logging.getLogger()


def run():
    alarm_pin = bootstrap.init_pin(ALARM_GPIO)
    dog = bootstrap.init_watchdog(WATCHDOG_TIMEOUT_MINUTE * 60 * 1000)

    bootstrap.init_console_syslog()
    if 'syslog' in config:
        bootstrap.init_remote_syslog(config['syslog']['host'],
                                     config['syslog']['port'])
        dog.feed()

    if 'wifi' in config:
        bootstrap.init_wifi(config['wifi']['essid'],
                            config['wifi']['password'])
        dog.feed()

    pushover_client = bootstrap.init_pushover_client(
        config['pushover']['email'],
        config['pushover']['password'],
        config['pushover']['device_name'],
        config['pushover']['device_id']
    )
    dog.feed()

    log.info('starting Pushover client')
    pushover_client.wait_for_frames(
        multiplex_handler(log_handler,
                          pin_handler(alarm_pin),
                          watchdog_handler(dog))
    )
    log.critical('Pushover client finished')


if __name__ == '__main__':
    run()
