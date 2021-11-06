import usocket as socket


class SyslogMessage:
    def __init__(self, message, severity=7):
        self.message = message
        self.severity = severity

    @property
    def facility(self):
        return 1    # USER

    @property
    def pri(self):
        return self.severity + (self.facility << 3)

    def __str__(self):
        return '<{pri}>{message}'.format(
            pri=self.pri,
            message=self.message
        )


class SyslogClient:
    def __init__(self, dest):
        self.dest = dest
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, msg):
        self.socket.sendto(str(msg).encode(), self.dest[0][4])


class SyslogHandler:
    def __init__(self, dest=socket.getaddrinfo('localhost', 514)):
        self.syslog_client = SyslogClient(dest)

    def emit(self, record):
        self.syslog_client.send(self._to_syslog_message(record))

    def _to_syslog_message(self, record):
        return SyslogMessage(
            record.message,
            severity=self._levelname_to_syslog_severity(record.levelname)
        )

    def _levelname_to_syslog_severity(self, levelname):
        levelname_to_severity = {
            'CRITICAL': 2,
            'ERROR': 3,
            'WARNING': 4,
            'INFO': 6,
            'DEBUG': 7,
        }

        return levelname_to_severity[levelname]
