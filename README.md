# MicroPython based Pushover Open Client

## Usage

### Create config

You need to know the following settings:

* pushover account email
* pushover account password
* pushover device name (choose by yourself)
* pushover device ID (see script below to gather device ID)

optional wifi

* wifi essid
* wifi password

optional remote syslog server

* remote syslog server host
* remote syslog server port

#### create Pushover device and gather device ID by script

You can make use of `create_device.py` to generate a new Pushover device and
gather required credentials. Use python3 (not micropython) to run the script.

```
virtualenv .
./bin/pip install -r requirements
./bin/python create_device.py
```

`create_device.py` will generate a config snipped to use. Make sure to keep the
device ID, since there is no way to get this information without deleting the
device within the Pushover admin interface and re-create it afterwards.

#### Create config file

Ceate `config.json` in project root folder. Wifi and Syslog sections are
optional.:

```
{
    "pushover": {
        "device_id": "your_pushover_device_id",
        "device_name": "your_pushover_device_name",
        "email": "your_pushover_account_email",
        "password": "your_pushover_password"
    },
    "do_not_disturb": {
        "before": 7,
        "after": 22
    },
    "syslog": {
        "host": "127.0.0.1",
        "port": 514
    },
    "wifi": {
        "essid": "your_wifi_essid",
        "password": "your_wifi_password"
    }
}
```

### Run Pushover Open Client

`micropython main.py`

## LICENSE

[logging](https://github.com/micropython/micropython-lib/tree/master/python-stdlib/logging) is [licensed](https://github.com/micropython/micropython-lib/blob/master/LICENSE) under MIT license.

[urequests](https://github.com/micropython/micropython-lib/tree/master/python-ecosys/urequests) is [licensed](https://github.com/micropython/micropython-lib/blob/master/LICENSE) under MIT license.

[usocketio/uwebsocket](https://github.com/danni/uwebsockets) is [licensed](https://github.com/danni/uwebsockets/blob/esp8266/LICENSE) under MIT license.
