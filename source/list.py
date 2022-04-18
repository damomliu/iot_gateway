import csv
import sqlite3
import os.path
from collections import Counter
from .status import SourceStatus
from model.Address import Address


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


class AddressList(list):
    def __init__(self, origin_path, logger):
        super().__init__()
        self.origin_path = origin_path
        self.logger = logger
        self.load_src_list()

    def read_sqllite(self):
        con = sqlite3.connect(self.origin_path)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('select * from address')
        sqllite_list = []
        for data in cur.fetchall():
            sqllite_list.append(dict(data))
        cur.close()
        con.close()
        return sqllite_list

    def to_src_list(self):
        source_list = []
        for address in self:
            try:
                source_list.append(address.to_source())
            except Exception as e:
                self.logger.warning(f'Invalid source: {e} / {address}')

        return source_list

    def load_src_list(self):
        """
            model.Address: 將輸入的數據從 dict形式 轉變成 Address 物件 ，定義數據輸入的欄位型別，確保系統中 數據型別的一致性
            source.AddressList:  處理 Address物件列表 ，將每筆 Address物件，依照條件轉變成相應的Source，確保後續系統操作時 Source物件格式 一致性
            source.MirrorSourceList: 對於 Source物件列表進行驗證，確保 Source物件格式 正確性，以便於後續系統使用
        """
        ext = os.path.splitext(self.origin_path)[-1]
        try:
            if ext == '.csv':
                with open(self.origin_path, 'r', encoding='utf-8-sig') as f:
                    dict_list = list(csv.DictReader(f))[1:]
            elif ext == '.db':
                dict_list = self.read_sqllite()
            else:
                raise ValueError('副檔名應為.csv or .db')

            for l in dict_list:
                self.append(Address(**l))

        except Exception as e:
            self.logger.warning(f'Invalid Source_come_from: {e}')


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
