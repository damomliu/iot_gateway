from collections import Counter
from .status import SourceStatus


class MirrorSourceList(list):
    def __init__(self, *args, mirror):
        super().__init__()
        self.mirror = mirror
        # for arg in args:
        #     self.append(arg)

    def append(self, new_src):
        if self.mirror._Validate(new_src) is not -1:
            super().append(new_src)
            new_src.status = SourceStatus.MIRRORED

            for src in self:
                if src.client == new_src.client:
                    new_src.client = src.client
                    break

    def reset(self, src):
        src.status = SourceStatus.NOT_STARTED

    @property
    def wait_connect(self):
        return [src for src in self if src.status.wait_connect]

    def set_connected(self, connected_src):
        """ 將已連線的 src, 及共用同個 Client 的其他 src 狀態設為 CONNECTED"""
        for src in self:
            if src.client == connected_src.client:
                src.status = SourceStatus.CONNECTED

    def set_connect_failed(self, failed_src):
        for src in self:
            if src.client == failed_src.client:
                src.status = SourceStatus.CONNECTED_FAILED

    @property
    def wait_read(self):
        return [src for src in self if src.status.wait_read]

    def set_reading(self, src):
        src.status = SourceStatus.READING

    def set_read_failed(self, src):
        src.status = SourceStatus.READING_FAILED



    @property
    def counter(self): return Counter(src.__class__.__name__ for src in self)
