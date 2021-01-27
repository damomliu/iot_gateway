from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
import opt

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
            return 0,req.exceptions            

DUMP_VAL = 0x0
class DataType:
    def __init__(self, type_str:str, pointType:PointType=PointType.DEFAULT()) -> None:
        self.type_str = type_str.lower()
        self._pType = pointType
        self._GetFunc()
    
    def __repr__(self): return f'<{__class__.__name__}: {self.type_str}>'
    def __str__(self): return self.type_str

    def _GetFunc(self):
        kw =  dict(
            byteorder=opt.DEFAULT.BYTE_ORDER,
            wordorder=opt.DEFAULT.WORD_ORDER,
        )
        self.builder = BinaryPayloadBuilder(**kw)
        self._addFunc = None
        self._decodeFunc = None
        self._add_by_list = False

        if self.type_str in ['bool', 'boolean']:
            self._addFunc = self.builder.add_bits
            self._add_by_list = True
            self._GetLength_n_Decoder()
            self._decodeFunc = self.decoder.decode_bits
        elif self.type_str in ['str', 'string']:
            self._addFunc = self.builder.add_string
            self._GetLength_n_Decoder()
            self._decodeFunc = self.decoder.decode_string
        elif self.type_str.startswith('int'):
            _bit = int(self.type_str[3:])
            if _bit == 8:
                self._addFunc = self.builder.add_8bit_int
                self._GetLength_n_Decoder()
                self._decodeFunc = self.decoder.decode_8bit_int
            elif _bit == 16:
                self._addFunc = self.builder.add_16bit_int
                self._GetLength_n_Decoder()
                self._decodeFunc = self.decoder.decode_16bit_int
            elif _bit == 32:
                self._addFunc = self.builder.add_32bit_int
                self._GetLength_n_Decoder()
                self._decodeFunc = self.decoder.decode_32bit_int
            elif _bit == 64:
                self._addFunc = self.builder.add_64bit_int
                self._GetLength_n_Decoder()
                self._decodeFunc = self.decoder.decode_64bit_int
        elif self.type_str.startswith('uint'):
            _bit = int(self.type_str[4:])
            if _bit == 8:
                self._addFunc = self.builder.add_8bit_uint
                self._GetLength_n_Decoder()
                self._decodeFunc = self.decoder.decode_8bit_uint
            elif _bit == 16:
                self._addFunc = self.builder.add_16bit_uint
                self._GetLength_n_Decoder()
                self._decodeFunc = self.decoder.decode_16bit_uint
            elif _bit == 32:
                self._addFunc = self.builder.add_32bit_uint
                self._GetLength_n_Decoder()
                self._decodeFunc = self.decoder.decode_32bit_uint
            elif _bit == 64:
                self._addFunc = self.builder.add_64bit_uint
                self._GetLength_n_Decoder()
                self._decodeFunc = self.decoder.decode_64bit_uint
        elif self.type_str.startswith('float'):
            _bit = int(self.type_str[len('float'):])
            if _bit == 16:
                self._addFunc = self.builder.add_16bit_float
                self._GetLength_n_Decoder()
                self._decodeFunc = self.decoder.decode_16bit_float
            elif _bit == 32:
                self._addFunc = self.builder.add_32bit_float
                self._GetLength_n_Decoder()
                self._decodeFunc = self.decoder.decode_32bit_float
            elif _bit == 64:
                self._addFunc = self.builder.add_64bit_float
                self._GetLength_n_Decoder()
                self._decodeFunc = self.decoder.decode_64bit_float

        if any([
            self._addFunc is None,
            self._decodeFunc is None,
        ]):
            raise ValueError(f'Invalid Data Type: {self.type_str}')

    def _GetLength_n_Decoder(self):
        if self._add_by_list:
            self._addFunc([DUMP_VAL])
        else:
            self._addFunc(DUMP_VAL)
        
        payload = self.builder.build()
        self._length = len(payload)
        if self._pType.IsRegister:
            self.decoder = BinaryPayloadDecoder.fromRegisters(self.builder.to_registers())
            self.decoder.reset()
        else:
            self.decoder = BinaryPayloadDecoder.fromCoils(self.builder.to_coils())
            self.decoder.reset()

    @property
    def length(self): return self._length
