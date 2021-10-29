from pymodbus.client.sync import ModbusTcpClient

from . import PointType, DataType
from ._base import SourcePairBase, ClientBase, TargetBase, _get, _clean_dict


class PyModbusTcpSource(SourcePairBase):
    _default_slave_id = 0x01
    _default_port = None

    def __init__(
        self, client, target, desc=None,
        address: int = None,
        slave_id: int = None,
        point_type_str: str = None,
        data_type_str: str = None,
        addr_start_from=None,
        formula_x_str: str = None,
        is_writable: bool = False,
    ) -> None:

        super().__init__(client, target, desc)
        self.address = address
        self.slave_id = int(slave_id or __class__._default_slave_id)
        self.pointType = PointType(
            point_type_str) if point_type_str else self.target.pointType
        self.dataType = DataType(
            data_type_str, self.pointType) if data_type_str else self.target.dataType
        self.addr_start_from = addr_start_from if addr_start_from else self.target.addr_start_from
        self.formula_x_str = formula_x_str
        self.is_writable = bool(is_writable)

        self._PreCheck()

    def _PreCheck(self):
        assert all([
            isinstance(self.address, int),
            isinstance(self.slave_id, int),
            self.addr_start_from in [0, 1],
        ])

    def __repr__(self) -> str:
        rep_str = f'<{__class__.__name__}@{self.client.ip}/{self.pointType.type_str}_{self.dataType.repr_short}_{self.address}'
        if len(self) > 1:
            rep_str += f'(*{len(self)})'
        return rep_str + f' : {self.target.repr_postfix}'

    @property
    def address_from0(self): return self.address - self.addr_start_from
    def __len__(self): return self.dataType.length

    @classmethod
    def FromDict(cls, is_writable=False, **kw):
        assert all([getattr(cls, attr) is not None for attr in [
            '_default_slave_id',
            '_default_port',
        ]]), f'Need to setup default value for <{cls.__name__}>'

        target = ModbusTarget.FromDict(**kw)
        client = PyModbusTcpClient(
            ip=kw['SourceIP'],
            port=int(_get(kw, 'SourcePort', cls._default_port)),
        )
        kwargs = _clean_dict(
            client=client,
            target=target,
            address=int(kw['SourceAddress']),
            slave_id=kw.get("SourceDeviceID"),
            point_type_str=kw.get('SourcePointType'),
            data_type_str=kw.get('SourceDataype'),
            addr_start_from=kw.get('addr_start_from'),
            formula_x_str=kw.get('FormulaX'),
            is_writable=is_writable,
            desc=kw.get('SourceDesc'),
        )
        return cls(**kwargs)

    def Read(self):
        req, val = self.client.Read(
            self.pointType, self.address_from0, len(self), self.slave_id)
        if req:
            self.values = val[:len(self)]
            return 1, val
        else:
            self.values = None
            return 0, val

    def Write(self, values):
        if self.is_writable:
            values = values[:len(self)]
            req, info = self.client.Write(
                values, self.pointType, self.address_from0, self.slave_id)
            if req:
                self.values = values
                return 1, values
            else:
                return 0, info
        else:
            return 0, Exception('SourceNotWriable')


class PyModbusTcpClient(ClientBase, ModbusTcpClient):
    def __init__(self, ip, port):
        ClientBase.__init__(self, ip, port)
        ModbusTcpClient.__init__(self, ip, port)

    def __repr__(self) -> str:
        return f'<{__class__.__name__}@{self.ip}:{self.port}'

    def __eq__(self, o) -> bool:
        if not isinstance(o, type(self)):
            return False
        else:
            return all([
                self.ip == o.ip,
                self.port == o.port,
            ])

    def Connect(self):
        if self.connect():
            return 1, None
        else:
            return 0, self

    def Disconnect(self):
        if self.connect():
            self.close()
            return 1
        else:
            return 0

    def Read(self, point_type: PointType, address_from0: int, count: int, unit: int):
        req, val = point_type.RequestValue(
            self, address_from0, count, unit=unit)
        return req, val

    def Write(self, values, point_type: PointType, address_from0: int, unit: int):
        try:
            writeFunc = point_type._WriteFunc(self)
            req = writeFunc(address_from0, values, unit=unit)
            if req.isError():
                return 0, req
            else:
                return 1, values

        except Exception as e:
            return 0, e


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
            self.addr_start_from in [0, 1],
        ])

    def __repr__(self):
        rep_str = f'<{__class__.__name__}/{self.pointType.type_str}_{self.dataType.repr_short}_{self.address}'
        if self.length > 1:
            rep_str += f'(*{self.length})'
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
            addr_start_from=_get(kw, 'addr_start_from',
                                 cls._default_addr_start_from),
            desc=kw.get('TargetDesc'),
        )
        return cls(**kwargs)
