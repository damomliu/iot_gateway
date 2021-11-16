from enum import Enum

class SourceStatus(Enum):
    """
    Enum for source status
    """
    NOT_STARTED = 0

    MIRRORED = 10

    CONNECTED = 1
    CONNECTED_FAILED = -1
    RETRY_FAILED = -11

    READING = 2
    READING_FAILED = -2  # Client connectd, but failed to read data from source

    DISCONNECTED = -3

    @property
    def wait_connect(self):
        return self in (SourceStatus.MIRRORED, SourceStatus.NOT_STARTED)
    @property
    def wait_read(self):
        return self in (SourceStatus.CONNECTED, SourceStatus.READING)
