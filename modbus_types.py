from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder


class PointType:
    OPTIONS = ['co', 'di', 'hr', 'ir']

    def __init__(self, type_str:str):
        self.type_str = type_str.lower()
        assert self.type_str in __class__.OPTIONS
        self.fx = None
        self.desc = None
        self._SetValue()

    def _SetValue(self):
        if self.type_str == 'co':
            self.fx = 1
            self.desc = 'Coil'
        elif self.type_str == 'di':
            self.fx = 2
            self.desc = 'Discrete Input'
        elif self.type_str == 'hr':
            self.fx = 3
            self.desc = 'Holding Register'
        elif self.type_str == 'ir':
            self.fx = 4
            self.desc = 'Input Register'

        for attr in [self.fx, self.desc]:
            if attr is None:
                raise ValueError(f'Invalue Point Type: {self.type_str}')

    def __repr__(self): return f'<{__class__.__name__}: {self.type_str}>'
    def __str__(self): return self.type_str

    @classmethod
    def DEFAULT(cls): return cls('hr')

    @property
    def IsRegister(self): return self.type_str in ['hr', 'ir']

    def _RequestFunc(self, client):
        req = dict(
            co=client.read_coils,
            di=client.read_discrete_inputs,
            hr=client.read_holding_registers,
            ir=client.read_input_registers,
        )

        return req[self.type_str]

    def RequestValue(self, client, *args, **kw):
        req = self._RequestFunc(client)(*args, **kw)
        if not req.isError():
            if self.type_str in ['co', 'di']:
                return 1,req.bits
            elif self.type_str in ['hr', 'ir']:
                return 1,req.registers

        else:
            return 0,req

_DEFAULT_BYTE_ORDER = '>'
_DEFAULT_WORD_ORDER = '>'

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

    def _GetFuncName(self):
        self._func_postfix = None
        self._add_by_bits = False

        if self.type_str in ['bool', 'boolean']:
            self._func_postfix = 'bits'
            self._add_by_bits = True
        elif self.type_str in ['str', 'string']:
            self._func_postfix = 'string'
        elif self.type_str.startswith('int'):
            _bit = int(self.type_str[3:])
            if _bit == 8:
                self._func_postfix = '8bit_int'
            elif _bit == 16:
                self._func_postfix = '16bit_int'
            elif _bit == 32:
                self._func_postfix = '32bit_int'
            elif _bit == 64:
                self._func_postfix = '64bit_int'
        elif self.type_str.startswith('uint'):
            _bit = int(self.type_str[4:])
            if _bit == 8:
                self._func_postfix = '8bit_uint'
            elif _bit == 16:
                self._func_postfix = '16bit_uint'
            elif _bit == 32:
                self._func_postfix = '32bit_uint'
            elif _bit == 64:
                self._func_postfix = '64bit_uint'
        elif self.type_str.startswith('float'):
            _bit = int(self.type_str[len('float'):])
            if _bit == 16:
                self._func_postfix = '16bit_float'
            elif _bit == 32:
                self._func_postfix = '32bit_float'
            elif _bit == 64:
                self._func_postfix = '64bit_float'

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
            return val[-1]
        else:
            return val