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
            self.write_fx = [5, 15]
            self.desc = 'Coil'
        elif self.type_str == 'di':
            self.fx = 2
            self.write_fx = []
            self.desc = 'Discrete Input'
        elif self.type_str == 'hr':
            self.fx = 3
            self.write_fx = [6, 16]
            self.desc = 'Holding Register'
        elif self.type_str == 'ir':
            self.fx = 4
            self.write_fx = []
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
    
    def _WriteFunc(self, client):
        req = dict(
            co=client.write_coils,
            hr=client.write_registers,
        )
        return req[self.type_str]
