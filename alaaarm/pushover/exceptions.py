class DeviceRegistrationError(Exception):
    def __init__(self, reason):
        self.reason = reason


class NoMessagesException(Exception):
    def __str__(self):
        return 'There are no messages for this Pushover device'
