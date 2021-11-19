import sys
import usocket as socket


class Severity:
  CRITICAL = 2
  ERROR = 3
  WARN = 4
  INFO = 6
  DEBUG = 7


class SyslogMessage:
    @classmethod
    def from_log_record(cls, record):
        return cls(record.message,
                   severity=getattr(Severity, record.levelname))

    def __init__(self, message, severity=7, facility=1):
        self.message = message
        self.severity = severity
        self.facility = facility

    @property
    def pri(self):
        return self.severity + (self.facility << 3)

    def __str__(self):
        return f'<{self.pri}>{self.message}'


class SyslogClient:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self._host = host
        self._port = port
        self._dst = None

    @property
    def dst(self):
        if not self._dst:
            self._resolve_dst()

        return self._dst

    def send(self, msg):
        try:
            self.socket.sendto(str(msg).encode(), self.dst[0][-1])
        except OSError:
            pass

    def _resolve_dst(self):
        self._dst = socket.getaddrinfo(self._host, self._port)


class RemoteHandler:
    def __init__(self, host='localhost', port=514):
        self.syslog_client = SyslogClient(host, port)

    def emit(self, record):
        self.syslog_client.send(SyslogMessage.from_log_record(record))


class ConsoleHandler:
    def emit(self, record):
        print(record.levelname, ":", record.name, ":", record.message,
              sep="", file=sys.stderr)
