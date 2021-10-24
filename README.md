# MicroPython based Pushover Open Client

## Usage

Ceate `config.json`:

```
{
    "syslog": {
        "host": "127.0.0.1",
        "port": 514
    },
    "pushover": {
        "email": "your@pushover.email",
        "password": "your_pushover_password"
    }
}
```

Start client:

`micropython alaaaaaarm.py`

## LICENSE

[logging](https://github.com/micropython/micropython-lib/tree/master/python-stdlib/logging) is [licensed](https://github.com/micropython/micropython-lib/blob/master/LICENSE) under MIT license.

[urequests](https://github.com/micropython/micropython-lib/tree/master/python-ecosys/urequests) is [licensed](https://github.com/micropython/micropython-lib/blob/master/LICENSE) under MIT license.

[usocketio/uwebsocket](https://github.com/danni/uwebsockets) is [licensed](https://github.com/danni/uwebsockets/blob/esp8266/LICENSE) under MIT license.
