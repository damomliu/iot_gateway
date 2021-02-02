import json
from pathlib import Path

from . import PointType, DataType
from ._base import SourceBase, _get


class TcpSource(SourceBase):
    _DEFAULT_SLAVE_ID = 0x00
    def __init__(self, row, config_dict):
        address = int(row['TargetAddress'])
        point_type_str = _get(row, 'PointType', config_dict['default_pointtype'])
        data_type_str = _get(row, 'DataType', config_dict['default_datatype'])
        addr_start_from = config_dict['address_start_from']
        super().__init__(address, point_type_str, data_type_str, addr_start_from)

        self.ip = row['SourceIP']
        self.port = row.get('SourcePort', config_dict['default_source_port'])
        self.slave_id = _get(row, 'SourceSlaveID', __class__._DEFAULT_SLAVE_ID)
        self.desc = row.get('SourceDesc')
        self._address = int(row['SourceAddress'])
        self.target_desc = row.get('TargetDesc')

        self.client = None
        self.is_connected = False
        self.values = None

    def __repr__(self) -> str:
        return f'<{__class__.__name__} {self.dataType.type_str}@{self.ip}/{self.pointType.type_str}_{self._address}:{self._target_address}>'

    @property
    def address_from0(self): return self._address - self._addr_start_from

    def Connect(self):
        if self.client.connect():
            self.is_connected = True
            return True
        else:
            return False

    def Read(self):
        req,val = self.pointType.RequestValue(self.client, self.address_from0, count=self.length, unit=self.slave_id)
        if req: self.values = val[:self.length]
        return req,val

    def Write(self, values):
        writeFunc = self.pointType._WriteFunc(self.client)
        values = values[:self.length]
        req = writeFunc(self.address_from0, values)
        if not req.isError():
            self.values = values
            return 1,req
        else:
            return 0,req
