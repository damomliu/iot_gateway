from .hsl_lib.client import ModbusTcpNet

from . import PointType, DataType
from ._base import SourceBase, _clean_dict, _get
from .pymodbus import ModbusTarget


class HslModbusTcpSource(SourceBase):
    _default_slave_id = 0x01
    _default_port = None

    def __init__(
            self, ip, port, address, target, desc=None,
            slave_id: int = None,
            point_type_str: str = None,
            data_type_str: str = None,
            addr_start_from=None,
            formula_x_str: str = None,
            is_writable: bool = False,
    ) -> None:

        super().__init__(ip, port, address, target, desc=desc)
        self.slave_id = int(slave_id or __class__._default_slave_id)
        self.pointType = PointType(point_type_str) if point_type_str else self.target.pointType
        self.dataType = DataType(data_type_str, self.pointType) if data_type_str else self.target.dataType
        self.addr_start_from = addr_start_from if addr_start_from else self.target.addr_start_from
        self.formula_x_str = formula_x_str
        self.is_writable = bool(is_writable)

        self._PreCheck()

        self.client = ModbusTcpNet(self.ip, self.port, self.slave_id)
        self.client.isAddressStartWithZero = not self.addr_start_from
        self.is_connected = False
        self._SetTrans()

    def _PreCheck(self):
        assert all([
            self.ip.replace('.', '').isdigit(),
            isinstance(self.port, int),
            isinstance(self.address, int),
            isinstance(self.slave_id, int),
            self.addr_start_from in [0, 1],
        ])

    def _SetTrans(self):
        byte_order = self.dataType._order['byteorder']
        word_order = self.dataType._order['wordorder']
        order = (byte_order, word_order)
        if order == ('>', '>'):
            self.client.SetDataFormat = 'ABCD'
        elif order == ('<', '>'):
            self.client.SetDataFormat = 'BADC'
        elif order == ('>', '<'):
            self.client.SetDataFormat = 'CDAB'
        elif order == ('<', '<'):
            self.client.SetDataFormat = 'DCBA'

    def __repr__(self) -> str:
        rep_str = f'<{__class__.__name__}@{self.ip}/{self.pointType.type_str}_{self.dataType.repr_short}_{self.address}'
        if self.length > 1: rep_str += f'(*{self.length})'
        return rep_str + f' : {self.target.repr_postfix}'

    @property
    def address_from0(self):
        return self.address - self.addr_start_from

    @classmethod
    def FromDict(cls, is_writable=False, **kw):
        assert all([getattr(cls, attr) is not None for attr in [
            '_default_slave_id',
            '_default_port',
        ]]), f'Need to setup default value for <{cls.__name__}>'

        target = ModbusTarget.FromDict(**kw)
        kwargs = _clean_dict(
            ip=kw['sourceIP'],
            port=int(_get(kw, 'sourcePort', cls._default_port)),
            address=int(kw['sourceAddress']),
            target=target,
            slave_id=kw.get("sourceDeviceID"),
            point_type_str=kw.get('sourcePointType'),
            data_type_str=kw.get('sourceDataype'),
            addr_start_from=kw.get('addr_start_from'),
            formula_x_str=kw.get('formulaX'),
            is_writable=is_writable,
            desc=kw.get('sourceDesc'),
        )
        return cls(**kwargs)

    def Connect(self):
        if not self.is_connected:
            res = self.client.ConnectServer()
            if res.IsSuccess:
                self.is_connected = True
                return 1, None
            else:
                return 0, res.ToMessageShowString()
        else:
            return 1, None

    def Disconnect(self):
        if self.is_connected:
            res = self.client.ConnectClose()
            if res.IsSuccess:
                self.is_connected = False
                return 1
            else:
                return 0
        else:
            return 0

    def RequestStr(self, attr_name='fx', index=-1):
        fx = getattr(self.pointType, attr_name)
        if isinstance(fx, list):
            fx = fx[index]

        _str = f'x={fx}'
        if self.slave_id:
            _str += f';s={self.slave_id}'
        _str += f';{self.address}'
        return _str

    def _ReadWriteTrans(self, func_str):
        assert func_str in ['r', 'w']

        func_name = None
        bit_N = self.dataType.bit_N
        if self.dataType.basic_type_str == 'bits':
            func_name = dict(r='TransBool', w='BoolTransByte')

        elif self.dataType.basic_type_str == 'int':
            func_name = dict(
                r=f'TransInt{bit_N}',
                w=f'Int{bit_N}TransByte',
            )
        elif self.dataType.basic_type_str == 'uint':
            func_name = dict(
                r=f'TransUInt{bit_N}',
                w=f'UInt{bit_N}TransByte'
            )
        elif self.dataType.basic_type_str == 'float':
            if bit_N == 32:
                func_name = dict(r='TransSingle', w='FloatTransByte')
            elif bit_N == 64:
                func_name = dict(r='TransDouble', w='DoubleTransByte')

        if not func_name: raise NotImplementedError
        return getattr(self.client.byteTransform, func_name[func_str])

    @property
    def _ReadTrans(self):
        return self._ReadWriteTrans('r')

    @property
    def _WriteTrans(self):
        return self._ReadWriteTrans('w')

    @property
    def _ReadLength(self):
        if self.pointType.type_str in ['hr', 'ir']:
            return len(self) * 2
        else:
            return len(self)

    def Read(self):
        res = self.client.Read(self.RequestStr('fx'), self._ReadLength)
        if res.IsSuccess:
            val = self._ReadTrans(res.Content, index=0)
            if self.dataType.basic_type_str == 'bits':
                self.values = [val]
            else:
                self.values = self.dataType.Encode(val)

            return 1, self.values
        else:
            self.values = None
            return 0, res.ToMessageShowString()

    def Write(self, values):
        if self.is_writable:
            try:
                if self.dataType.basic_type_str == 'bits':
                    req_val = values
                else:
                    req_val = self._WriteTrans(self.dataType.Decode(values))

                res = self.client.Write(self.RequestStr('write_fx'), req_val)
                if res.IsSuccess:
                    self.values = values
                    return 1, None
                else:
                    return 0, res.ToMessageShowString()
            except Exception as e:
                return 0, e
        else:
            return 0, Exception('TargetNotWritable')
