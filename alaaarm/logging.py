import sys
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
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self._host = host
        self._port = port
        self._dst = None

    @property
    def dst(self):
        if not self._dst:
            self._dst = self._resolve_dst()

        return self._dst

    def send(self, msg):
        if self.dst:
            self.socket.sendto(str(msg).encode(), self.dst[0][4])

    def _resolve_dst(self):
        try:
            return socket.getaddrinfo(self._host, self._port)
        except OSError:
            return None


class RemoteHandler:
    def __init__(self, host='localhost', port=514):
        self.syslog_client = SyslogClient(host, port)

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
            'WARN': 4,
            'INFO': 6,
            'DEBUG': 7,
        }

        return levelname_to_severity[levelname]


class ConsoleHandler:
    def emit(self, record):
        print(record.levelname, ":", record.name, ":", record.message,
              sep="", file=sys.stderr)
