from pydantic import BaseModel, Field

from . import PyModbusTcpSource, JsonSource, HslModbusTcpSource


class TargetAddress(BaseModel):
    # Field(alias= 'address欄位名稱')
    target_address: int = Field(alias='TargetAddress')
    point_type: str = Field(alias='PointType', default=None)
    data_type: str = Field(alias='DataType', default=None)
    abcd: str = Field(alias='ABCD', default=None)
    addr_start_from: str = Field(alias='addr_start_from', default=None)
    target_desc: str = Field(alias='TargetDesc', default=None)


class SourceAddress(BaseModel):
    source_protocol: str = Field(alias='SourceProtocol')
    source_ip: str = Field(alias='SourceIP')
    source_port: int = Field(alias='SourcePort', default=None)
    source_address: str = Field(alias='SourceAddress', default=None)
    source_deviceID: str = Field(alias='SourceDeviceID', default=None)
    source_pointtype: str = Field(alias='SourcePointType', default=None)
    source_dataype: str = Field(alias='SourceDataype', default=None)
    addr_start_from: str = Field(alias='addr_start_from', default=None)
    formulaX: str = Field(alias='FormulaX', default=None)
    source_desc: str = Field(alias='SourceDesc', default=None)


class Address(BaseModel):
    source: SourceAddress
    target: TargetAddress

    @classmethod
    def from_dict(cls, data_dict):
        """ dict 欄位名稱 需包含 SourceAddress & TargetAddress 預設好的欄位"""
        address_dict = {}
        address_dict['source'] = SourceAddress(**data_dict)
        address_dict['target'] = TargetAddress(**data_dict)
        return cls(**address_dict)

    def to_source(self):
        r = self.dict()
        protocol_str = r['source'].get('source_protocol')
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
