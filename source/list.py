import os.path
from collections import Counter
from .status import SourceStatus
import csv
from .pymodbus import PyModbusTcpSource
from .json import JsonSource
from .hsl import HslModbusTcpSource
import sqlite3


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
    def read_failed(self):
        return [src for src in self if src.status == SourceStatus.READING_FAILED]

    def set_readfail_recover(self, src):
        src.status = SourceStatus.READING_FAILED_RECOVER

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

        return {k: dict(v) for k, v in counter_dict.items()}

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


class SourceList(list):
    def __init__(self, origin_path, logger):
        super().__init__()
        self.origin_path = origin_path
        self.logger = logger
        self.load_src_list()

    def readsqldata(self):
        con = sqlite3.connect(self.origin_path)
        cur = con.cursor()
        cur.execute('select * from address')
        dict_list = []
        for data in cur.fetchall():
            source_dict = {}
            source_dict['SourceProtocol'] = data[0]
            source_dict['SourceIP'] = data[1]
            source_dict['SourcePort'] = data[2]
            source_dict['SourceDeviceID'] = data[3]
            source_dict['SourcePointType'] = data[4]
            source_dict['SourceAddress'] = data[5]
            source_dict['SourceDataype'] = data[6]
            source_dict['TargetAddress'] = data[7]
            source_dict['DataType'] = data[8]
            source_dict['ABCD'] = data[9]
            source_dict['FormulaX'] = data[10]
            source_dict['TargetDesc'] = data[11]
            source_dict['SourceDesc'] = data[12]
            dict_list.append(source_dict)
        cur.close()
        con.close()
        return dict_list

    def append_source(self, dict_list):
        for r in dict_list:
            protocol_str = r.get('SourceProtocol')
            try:
                if protocol_str.startswith('modbus_tcp'):
                    # add TcpSource
                    if protocol_str.endswith('tcp1'):
                        self.append(PyModbusTcpSource.FromDict(**r, is_writable=False))
                    elif protocol_str.endswith('tcp1rw'):
                        self.append(PyModbusTcpSource.FromDict(**r, is_writable=True))
                    elif protocol_str.endswith('tcp2'):
                        self.append(HslModbusTcpSource.FromDict(**r, is_writable=False))
                    elif protocol_str.endswith('tcp2rw'):
                        self.append(HslModbusTcpSource.FromDict(**r, is_writable=True))

                elif protocol_str == 'json':
                    # add JsonSource
                    self.append(JsonSource.FromDict(**r))

                else:
                    continue

            except Exception as e:
                self.logger.warning(f'Invalid source: {e} / {r}')

    def load_src_list(self):
        ext = os.path.splitext(self.origin_path)[-1]
        if ext == '.csv':
            with open(self.origin_path, 'r', encoding='utf-8-sig') as f:
                dict_list = list(csv.DictReader(f))[1:]
        elif ext == '.db':
            dict_list = self.readsqldata()
        else:
            raise ValueError('副檔名應為.csv or .db')
        self.append_source(dict_list)

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
    summary = [f'{k} * {v}' for k, v in counter.items()]
    if expand_failed:
        summary.extend(failed_list)
    if expand_success:
        summary.extend(success_list)
    return summary
