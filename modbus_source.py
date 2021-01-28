import pymodbus.datastore as ds

from modbus_types import PointType, DataType
import opt


class Source:
    def __init__(self, row, config_dict):
        self.ip = row['SourceIP']
        self.port = row.get('SourcePort', config_dict['default_source_port'])
        self.slave_id = _get(row, 'SourceSlaveID', opt.DEFAULT.SOURCE_SLAVE_ID)
        self.desc = row.get('SourceDesc')

        point_type_str = _get(row, 'SourcePointType', config_dict['default_source_pointtype'])
        self.pointType = PointType(point_type_str)

        data_type_str = _get(row, 'SourceDataType', config_dict['default_source_datatype'])
        self.dataType = DataType(data_type_str, self.pointType)

        self._addr_start_from = int(config_dict['address_start_from_1'])
        self._address = int(row['SourceAddress'])
        self._target_address = int(row['TargetAddress'])
        self.target_desc = row.get('TargetDesc')

        self.client = None
        self.is_connected = False
        self.value = None

    def __repr__(self) -> str:
        return f'<{__class__.__name__} {self.dataType.type_str}@{self.ip}/{self.pointType.type_str}_{self._address}:{self._target_address}>'

    @property
    def length(self): return self.dataType.length
    @property
    def address_from0(self): return self._address - self._addr_start_from
    @property
    def target_address_from0(self): return self._target_address - self._addr_start_from


def _get(_dict, key, val_if_none):
    if _dict.get(key):
        return _dict.get(key)
    else:
        return val_if_none


class LinkedSlaveContext(ds.ModbusSlaveContext):
    def __init__(self, mirror, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mirror = mirror

    def setValues(self, fx, address, values, writeback=True):
        super().setValues(fx, address, values)
        if writeback:
            self.mirror.Writeback(fx, address, values)
