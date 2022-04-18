from pydantic import BaseModel
from source.pymodbus import PyModbusTcpSource
from source.json import JsonSource
from source.hsl import HslModbusTcpSource

class TargetAddress(BaseModel):
    TargetAddress: int
    PointType: str = None
    DataType: str
    ABCD: str
    addr_start_from: str = None
    TargetDesc: str

class SourceAddress(BaseModel):
    SourceProtocol: str
    SourceIP: str
    SourcePort: int
    SourceAddress: str
    SourceDeviceID: str
    SourcePointType: str
    SourceDataype: str
    addr_start_from: str = None
    FormulaX: str
    SourceDesc: str

class Address(TargetAddress,SourceAddress):

    def to_source(self,logger):
        r = self.dict()
        protocol_str = r.get('SourceProtocol')
        try:
            if protocol_str.startswith('modbus_tcp'):
                # add TcpSource
                if protocol_str.endswith('tcp1'):
                    return PyModbusTcpSource.FromDict(**r, is_writable=False)
                elif protocol_str.endswith('tcp1rw'):
                    return PyModbusTcpSource.FromDict(**r, is_writable=True)
                elif protocol_str.endswith('tcp2'):
                    return HslModbusTcpSource.FromDict(**r, is_writable=False)
                elif protocol_str.endswith('tcp2rw'):
                    return HslModbusTcpSource.FromDict(**r, is_writable=True)

            elif protocol_str == 'json':
                # add JsonSource
                return JsonSource.FromDict(**r)
            else:
                raise ValueError('Source 應為 PyModbusTcpSource or HslModbusTcpSource or JsonSource')

        except Exception as e:
            logger.warning(f'Invalid source: {e} / {r}')
