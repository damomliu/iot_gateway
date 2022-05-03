from enum import Enum
from sys import byteorder

from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from . import PointType

_DEFAULT_BYTE_ORDER = '>'
_DEFAULT_WORD_ORDER = '>'


class EDataOrder(Enum):
    ABCD = ">>"
    CDAB = "><"
    BADC = "<>"
    DCBA = "<<"

    @property
    def to_pymodbus(self):
        return dict(byteorder=self.value[0], wordorder=self.value[1])


class DataType:
    def __init__(
        self,
        type_str: str,
        pointType: PointType = PointType.DEFAULT(),
        byteorder=_DEFAULT_BYTE_ORDER,
        wordorder=_DEFAULT_WORD_ORDER
    ) -> None:
        self.type_str = type_str.lower()
        self._pType = pointType
        self._order = dict(byteorder=byteorder, wordorder=wordorder)
        
        self._GetFuncName()
        self._GetLength()

    def __repr__(self): return f'<{__class__.__name__}: {self.type_str}>'
    def __str__(self): return self.type_str
    @property
    def repr_short(self):
        if self._func_postfix == 'bits':
            return 'bool'
        elif self._func_postfix == 'string':
            return 'str'
        else:
            bitN,datatype = self._func_postfix.split('_')
            return f'{datatype[0]}{bitN.replace("bit", "")}'

    @property
    def _func_postfix(self):
        if self.basic_type_str in ['bits', 'string']:
            return self.basic_type_str
        elif self.bit_N is not None:
            return f'{self.bit_N}bit_{self.basic_type_str}'
        else:
            return None

    def _GetFuncName(self):
        self._add_by_bits = False
        self.bit_N = None
        self.basic_type_str = None

        if self.type_str in ['bool', 'boolean']:
            self.basic_type_str = 'bits'
            self._add_by_bits = True

        elif self.type_str in ['str', 'string']:
            self.basic_type_str = 'string'

        elif self.type_str.startswith('int'):
            self.basic_type_str = 'int'
            _bit = int(self.type_str[3:])
            if _bit in [8, 16, 32, 64]:
                self.bit_N = _bit

        elif self.type_str.startswith('uint'):
            self.basic_type_str = 'uint'
            _bit = int(self.type_str[4:])
            if _bit in [8, 16, 32, 64]:
                self.bit_N = _bit

        elif self.type_str.startswith('float'):
            self.basic_type_str = 'float'
            _bit = int(self.type_str[len('float'):])
            if _bit in [16, 32, 64]:
                self.bit_N = _bit

        if self._func_postfix is None:
            raise ValueError(f'Invalid Data Type: {self.type_str}')
    
    @property
    def _AddFuncName(self): return 'add_' + self._func_postfix
    @property
    def _DecodeFuncName(self): return 'decode_' + self._func_postfix

    def _GetLength(self):
        dump_val = 0x0
        self.Encode(dump_val)

        payload = self.builder.build()
        self._length = len(payload)
        self.builder.reset()

    @property
    def length(self): return self._length

    def Encode(self, val):
        self.builder = BinaryPayloadBuilder(**self._order)
        add_func = getattr(self.builder, self._AddFuncName)
        
        if self._add_by_bits:
            add_func([val])
        else:
            add_func(val)
            
        if self._pType.IsRegister:
            return self.builder.to_registers()
        else:
            if self._add_by_bits:
                return self.builder.to_coils()[-1]
            else:
                return self.builder.to_coils()

    def Decode(self, binary):
        if self._pType.IsRegister:
            self.decoder = BinaryPayloadDecoder.fromRegisters(binary, **self._order)
        else:
            self.decoder = BinaryPayloadDecoder.fromCoils(binary, **self._order)
        
        decode_func = getattr(self.decoder, self._DecodeFuncName)
        val = decode_func()
        if self._add_by_bits:
            return val[0]
        else:
            return val