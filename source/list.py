from collections import Counter
from . import SourceStatus


class MirrorSourceList(list):
    def __init__(self, *args, mirror):
        super().__init__()
        self.mirror = mirror
        # for arg in args:
        #     self.append(arg)

    @property
    def not_started(self):
        return [src for src in self if src.status == SourceStatus.NOT_STARTED]

    @property
    def readable(self):
        return [src for src in self if src.status.readable]

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

    def set_connected(self, src):
        src.status = SourceStatus.CONNECTED

    def set_reading(self, src):
        src.status = SourceStatus.READING

    def retire(self, src):
        # self.remove(src)
        # self._retired.append(src)
        src.status = SourceStatus.READING_FAILED

    def retire_by_client(self, failed_src):
        for src in self:
            if src.client == failed_src.client:
                # self.retired(src)
                src.status = SourceStatus.CONNECTED_FAILED

    @property
    def counter(self): return Counter(src.__class__.__name__ for src in self)
