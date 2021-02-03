import json
from pathlib import Path

from . import PointType, DataType
from ._base import SourceBase, _get


class TcpSource(SourceBase):
    _default_slave_id = 0x00
    _default_src_port = None

    def _get_default(self, arg, _attr_name):
        if arg is None:
            return getattr(__class__, f'_default{_attr_name}')
        else:
            return arg

    def __init__(
        self,
        address, point_type_str, data_type_str, addr_start_from,
        src_ip, src_address,
        src_port=None, slave_id=None, is_writable=False,
        target_desc='', src_desc='',
    ):
        super().__init__(address, point_type_str, data_type_str, addr_start_from)
        self.ip = src_ip
        self.port = self._get_default(src_port, '_src_port')
        self.slave_id = self._get_default(slave_id, '_slave_id')
        self._address = src_address
        self.desc = {'src': src_desc, 'target': target_desc}

        self.is_writable = is_writable

        self.client = None
        self.is_connected = False
        self.values = None

    def __repr__(self) -> str:
        return f'<{__class__.__name__} {self.dataType.type_str}@{self.ip}/{self.pointType.type_str}_{self._address}:{self._target_address}>'

    @property
    def address_from0(self): return self._address - self._addr_start_from

    @classmethod
    def FromDict(cls, **kw):
        assert all([getattr(__class__, attr) is not None for attr in [
            '_default_slave_id',
            '_default_src_port',
            '_default_pointtype_str',
            '_default_datatype_str',
            '_default_addr_start_from',
        ]]), f'Need to setup default value for <{__class__.__name__}>'

        kwargs = dict(
            address=int(kw['TargetAddress']),
            point_type_str=_get(kw, 'PointType', __class__._default_pointtype_str),
            data_type_str=_get(kw, 'DataType', __class__._default_datatype_str),
            addr_start_from=_get(kw, 'addr_start_from', __class__._default_addr_start_from),
            src_ip=kw['SourceIP'],
            src_address=int(kw['SourceAddress']),
            is_writable=(kw.get('TargetWritable') == '*'),
            target_desc=kw.get('TargetDesc',''),
            src_desc=kw.get('SourceDesc',''),
        )
        return cls(**kwargs)

    def Connect(self):
        if self.client.connect():
            self.is_connected = True
            return 1,None
        else:
            return 0,self.client

    def Read(self):
        req,val = self.pointType.RequestValue(self.client, self.address_from0, count=self.length, unit=self.slave_id)
        if req:
            self.values = val[:self.length]
            return 1,None
        else:
            return 0,val

    def Write(self, values):
        if self.is_writable:
            writeFunc = self.pointType._WriteFunc(self.client)
            values = values[:self.length]
            req = writeFunc(self.address_from0, values)
            if not req.isError():
                self.values = values
                return 1,None
            else:
                return 0,req
        else:
            return 0,Exception('TargetNotWriable')
