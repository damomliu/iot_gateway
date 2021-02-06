from os import replace
from . import PointType, DataType
from ._base import SourceBase, TargetBase, _get, _clean_dict


class TcpSource(SourceBase):
    _default_slave_id = 0x00
    _default_port = None
    def _get_default(self, arg, _attr_name):
        if arg is None:
            return getattr(__class__, f'_default{_attr_name}')
        else:
            return arg

    def __init__(
        self, ip, port, address, target, desc=None,
        slave_id:int=None,
        point_type_str:str=None,
        data_type_str:str=None,
        addr_start_from=None,
        is_writable:bool=False,
    ) -> None:

        super().__init__(ip=ip, port=port, address=address, target=target, desc=desc)
        self.slave_id = slave_id
        self.pointType = PointType(point_type_str) if point_type_str else self.target.pointType
        self.dataType = DataType(data_type_str) if data_type_str else self.target.dataType
        self.addr_start_from = addr_start_from if addr_start_from else self.target.addr_start_from
        self.is_writable = bool(is_writable)

        self.client = None
        self.is_connected = False
        self.values = None
        self._PreCheck()

    def _PreCheck(self):
        assert all([
            self.ip.replace('.','').isdigit(),
            isinstance(self.port, int),
            isinstance(self.address, int),
            isinstance(self.slave_id, int),
            self.addr_start_from in [0,1],
        ])

    def __repr__(self) -> str:
        rep_str = f'<{__class__.__name__}@{self.ip}/{self.pointType.type_str}_{self.dataType.repr_short}_{self.address}'
        if self.length > 1: rep_str += f'(*{self.length})'
        return rep_str + f' : {self.target.repr_postfix}'

    @property
    def address_from0(self): return self.address - self.addr_start_from
    @property
    def length(self): return self.dataType.length

    @classmethod
    def FromDict(cls, is_writable=False, **kw):
        assert all([getattr(cls, attr) is not None for attr in [
            '_default_slave_id',
            '_default_port',
        ]]), f'Need to setup default value for <{cls.__name__}>'
        
        target = ModbusTarget.FromDict(**kw)
        kwargs = _clean_dict(
            ip=kw['SourceIP'],
            port=_get(kw, 'SourcePort', cls._default_port),
            address=int(kw['SourceAddress']),
            target=target,
            slave_id=cls._default_slave_id,
            point_type_str=kw.get('SourcePointType'),
            data_type_str=kw.get('SourceDataype'),
            addr_start_from=kw.get('addr_start_from'),
            is_writable=is_writable,
            desc=kw.get('SourceDesc'),
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


class ModbusTarget(TargetBase):
    _default_pointtype_str = None
    _default_datatype_str = None
    _default_addr_start_from = None

    def __init__(
        self,
        address,
        point_type_str,
        data_type_str,
        addr_start_from=1,
        desc=None
    ):
        self.address = int(address)
        self.pointType = PointType(point_type_str)
        self.dataType = DataType(data_type_str, self.pointType)
        self.addr_start_from = addr_start_from
        self.desc = desc if desc else ''

    def _PreCheck(self):
        assert all([
            isinstance(self.address, int),
            self.addr_start_from in [0,1],
        ])        

    def __repr__(self):
        rep_str = f'<{__class__.__name__}/{self.pointType.type_str}_{self.dataType.repr_short}_{self.address}'
        if self.length > 1: rep_str += f'(*{self.length})'
        return rep_str + '>'
    @property
    def repr_postfix(self): return str(self)[14:]

    @property
    def length(self): return self.dataType.length
    @property
    def address_from0(self): return self.address - self.addr_start_from
    @property
    def address_set(self):
        _range = range(self.address_from0, self.address_from0 + self.length)
        return set(list(_range))

    @classmethod
    def FromDict(cls, **kw):
        assert all([getattr(ModbusTarget, attr) is not None for attr in [
            '_default_pointtype_str',
            '_default_datatype_str',
            '_default_addr_start_from',
        ]]), f'Need to setup default value for <{__class__.__name__}>'

        kwargs = _clean_dict(
            address=kw['TargetAddress'],
            point_type_str=_get(kw, 'PointType', cls._default_pointtype_str),
            data_type_str=_get(kw, 'DataType', cls._default_datatype_str),
            addr_start_from=_get(kw, 'addr_start_from', cls._default_addr_start_from),
            desc=kw.get('TargetDesc'),
        )
        return cls(**kwargs)
