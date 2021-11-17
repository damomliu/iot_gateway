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

    @property
    def wait_retry(self):
        return [src for src in self if src.status == SourceStatus.CONNECTED_FAILED]

    @property
    def retry_failed(self):
        return [src for src in self if src.status == SourceStatus.RETRY_FAILED]

    def set_connected(self, connected_src):
        """ 將已連線的 src, 及共用同個 Client 的其他 src 狀態設為 CONNECTED"""
        for src in self:
            if src.client == connected_src.client:
                src.status = SourceStatus.CONNECTED

    def set_connect_failed(self, failed_src):
        for src in self:
            if src.client == failed_src.client:
                src.status = SourceStatus.CONNECTED_FAILED

    def set_retry_failed(self, failed_src):
        for src in self:
            if src.client == failed_src.client:
                src.status = SourceStatus.RETRY_FAILED

    @property
    def wait_read(self):
        return [src for src in self if src.status.wait_read]

    def set_reading(self, src):
        src.status = SourceStatus.READING

    def set_read_failed(self, src):
        src.status = SourceStatus.READING_FAILED

    @property
    def counter(self):
        counter_dict = {}
        for src in self:
            src_class = src.__class__.__name__
            src_status = src.status.name
            if counter_dict.get(src_class):
                counter_dict[src_class].update([src_status])
            else:
                counter_dict[src_class] = Counter([src_status])

        return {k: dict(v) for k,v in counter_dict.items()}

    @property
    def client_list(self) -> list:
        _list = []
        for src in self:
            if src.client not in _list:
                _list.append(src.client)
        return _list

    @property
    def status(self) -> list:
        counter = Counter()
        mixed_dict = {}
        for client in self.client_list:
            sources = [src for src in self if src.client == client]
            src_counter = Counter([src.status.name for src in sources])
            if len(src_counter) == 1:
                counter.update([sources[0].status.name])
            else:
                counter.update(["mixed"])
                mixed_dict[str(client)] = _client_summary(sources)

        return [dict(counter), mixed_dict]


def _client_summary(source_list, expand_failed=True, expand_success=False):
    counter = Counter()
    success_list = []
    failed_list = []
    for src in source_list:
        counter.update([src.status.name])
        if src.status.something_failed:
            failed_list.append(str(src))
        else:
            success_list.append(str(src))
    summary = [f'{k} * {v}' for k,v in counter.items()]
    if expand_failed:
        summary.extend(failed_list)
    if expand_success:
        summary.extend(success_list)
    return summary
