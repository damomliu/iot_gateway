from pydantic import BaseModel,Field

# from . import PyModbusTcpSource, JsonSource, HslModbusTcpSource

from source.pymodbus import PyModbusTcpSource
from source.json import JsonSource
from source.hsl import HslModbusTcpSource

# 預設值新增
class TargetAddress(BaseModel):
    # Field(alias= 'address欄位名稱')
    targetAddress: int = Field(alias='TargetAddress')
    pointType: str = Field(alias='PointType', default=None)
    dataType: str = Field(alias='DataType', default=None)
    abcd: str = Field(alias='ABCD', default=None)
    addr_start_from: str = Field(alias='addr_start_from', default=None)
    targetDesc: str = Field(alias='TargetDesc', default=None)


class SourceAddress(BaseModel):
    sourceProtocol: str = Field(alias='SourceProtocol')
    sourceIP: str = Field(alias='SourceIP')
    sourcePort: int = Field(alias='SourcePort', default=None)
    sourceAddress: str = Field(alias='SourceAddress', default=None)
    sourceDeviceID: str = Field(alias='SourceDeviceID', default=None)
    sourcePointType: str = Field(alias='SourcePointType', default=None)
    sourceDataype: str = Field(alias='SourceDataype', default=None)
    addr_start_from: str = Field(alias='addr_start_from', default=None)
    formulaX: str = Field(alias='FormulaX', default=None)
    sourceDesc: str = Field(alias='SourceDesc', default=None)


class Address(TargetAddress,SourceAddress):

    def to_source(self):
        r = self.dict()
        protocol_str = r.get('sourceProtocol')
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

