import json
from pathlib import Path

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
    def target_address_set(self):
        length = self.length
        addr = self.target_address_from0
        _set = set()
        while length:
            _set.add(addr)
            addr += 1
            length -= 1
        return _set

    @property
    def address_from0(self): raise NotImplementedError
    def Read(self): raise NotImplementedError
    def Write(self, values): raise NotImplementedError

class TcpSource(SourceBase):
    def __init__(self, row, config_dict):
        address = int(row['TargetAddress'])
        point_type_str = _get(row, 'PointType', config_dict['default_pointtype'])
        data_type_str = _get(row, 'DataType', config_dict['default_datatype'])
        addr_start_from = config_dict['address_start_from']
        super().__init__(address, point_type_str, data_type_str, addr_start_from)

        self.ip = row['SourceIP']
        self.port = row.get('SourcePort', config_dict['default_source_port'])
        self.slave_id = _get(row, 'SourceSlaveID', opt.DEFAULT.SOURCE_SLAVE_ID)
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

    def Read(self):
        req,val = self.pointType.RequestValue(self.client, self.address_from0, count=self.length, unit=self.slave_id)
        if req: self.values = val[:self.length]
        return req,val

    def Write(self, values):
        writeFunc = self.pointType._WriteFunc(self.client)
        req = writeFunc(self.address_from0, values)
        if not req.isError():
            self.values = values
            return 1,req
        else:
            return 0,req


class JsonSource(SourceBase):
    default_datatype_str = None
    default_addr_start_from = None
    default_folder = None

    def __init__(self, filepath:Path, address, point_type_str, data_type_str, addr_start_from, val=None):
        super().__init__(address, point_type_str, data_type_str, addr_start_from=addr_start_from)
        self.values = val
        self.filepath = filepath

    def __repr__(self) -> str:
        return f'<{__class__.__name__} {self.dataType.type_str}/{self.pointType.type_str}:{self._target_address}>'
    
    @classmethod
    def FromDict(cls, row, config_dict):
        address = int(row['TargetAddress'])
        point_type_str = _get(row, 'PointType', config_dict['default_pointtype'])
        data_type_str = _get(row, 'DataType', config_dict['default_datatype'])
        addr_start_from = config_dict.get('address_start_from', 1)
        filepath = __class__.default_folder / f'{point_type_str}_{address:05d}.json'
        return cls(filepath, address, point_type_str, data_type_str, addr_start_from)

    @classmethod
    def FromFile(cls, filepath):
        with open(filepath, 'r') as f:
            _dict = json.load(f)
        return cls(filepath, **_dict)

    @classmethod
    def FromFx(cls, fx, address, values):
        assert all([
            __class__.default_datatype_str is not None,
            __class__.default_addr_start_from is not None,
            __class__.default_folder is not None,
        ]), f'Need to setup default value for {__class__.__name__}.{__name__}'
        
        if fx in [6, 16]:
            pt = 'hr'
        elif fx in [5, 16]:
            pt = 'co'
        else:
            raise RuntimeError(f'Invalid fx = {fx}')

        if not hasattr(values, '__iter__'):
            values = [values]

        return cls(
            filepath=__class__.default_folder / f'{pt}_{address:05d}.json',
            address=address,
            point_type_str=pt,
            data_type_str=__class__.default_datatype_str,
            addr_start_from=__class__.default_addr_start_from,
            val=values,
        )
    @property
    def dict(self):
        return dict(
            address=self._target_address,
            point_type_str=self.pointType.type_str,
            data_type_str=self.dataType.type_str,
            addr_start_from=self._addr_start_from,
            val=self.values,
        )

    def Read(self):
        try:
            with open(self.filepath, 'r') as f:
                _dict = json.load(f)
            
            if self.pointType.type_str != _dict['point_type_str']:
                self.pointType = PointType(_dict['point_type_str'])
            if self.dataType.type_str != _dict['data_type_str']:
                raise Exception('Datatype Change')
            
            self._target_address = _dict['address']
            self._addr_start_from = _dict['addr_start_from']
            self.values = _dict['val']
            
            return 1,self.values
        except Exception as e:
            return 0,e

    def Write(self, values=None):
        if values is None:
            if self.values is None: raise RuntimeError(f'No values to be written: {self}')
            values = self.values
        else:
            self.values = values
        
        try:
            if not self.filepath.parent.is_dir(): self.filepath.parent.mkdir()
            with open(self.filepath, 'w+') as f:
                json.dump(self.dict, f, indent=2)
            return 1,self.dict
        except Exception as e:
            return 0,e


def _get(_dict, key, val_if_none):
    if _dict.get(key):
        return _dict.get(key)
    else:
        return val_if_none
