from modbus_types import PointType, DataType
import opt


class SourceBase:
    def __init__(self, address, point_type_str, data_type_str, addr_start_from=1):
        self.pointType = PointType(point_type_str)
        self.dataType = DataType(data_type_str, self.pointType)
        self._addr_start_from = addr_start_from
        self._target_address = address

    @property
    def length(self): return self.dataType.length
    @property
    def target_address_from0(self): return self._target_address - self._addr_start_from
    
    @property
    def address_from0(self): raise NotImplemented
    def Read(self): raise NotImplemented
    def Write(self, values): raise NotImplemented

class TcpSource(SourceBase):
    def __init__(self, row, config_dict):
        address = int(row['TargetAddress'])
        point_type_str = _get(row, 'SourcePointType', config_dict['default_source_pointtype'])
        data_type_str = _get(row, 'SourceDataType', config_dict['default_source_datatype'])
        addr_start_from = int(config_dict['address_start_from_1'])
        super().__init__(address, point_type_str, data_type_str, addr_start_from)
        
        self.ip = row['SourceIP']
        self.port = row.get('SourcePort', config_dict['default_source_port'])
        self.slave_id = _get(row, 'SourceSlaveID', opt.DEFAULT.SOURCE_SLAVE_ID)
        self.desc = row.get('SourceDesc')
        self._address = int(row['SourceAddress'])
        self.target_desc = row.get('TargetDesc')

        self.client = None
        self.is_connected = False
        self.value = None

    def __repr__(self) -> str:
        return f'<{__class__.__name__} {self.dataType.type_str}@{self.ip}/{self.pointType.type_str}_{self._address}:{self._target_address}>'

    @property
    def address_from0(self): return self._address - self._addr_start_from
    
    def Read(self):
        req,val = self.pointType.RequestValue(self.client, self.address_from0, count=self.length, unit=self.slave_id)
        if req: self.value = val[:self.length]
        return req,val
    
    def Write(self, values):
        writeFunc = self.pointType._WriteFunc(self.client, values)
        req = writeFunc(self.address_from0, values)
        if not req.isError():
            self.value = values
            return 1,req
        else:
            return 0,req


class JsonSource:
    def __init__(self, row, config_dict):
        super().__init__(row, config_dict)



def _get(_dict, key, val_if_none):
    if _dict.get(key):
        return _dict.get(key)
    else:
        return val_if_none
