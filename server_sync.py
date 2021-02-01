from pymodbus.server.sync import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
import pymodbus.datastore as ds

from modbus_types import PointType, DataType
from modbus_context import LinkedSlaveContext
import opt

__version__ = '0.0.0'

class SyncServer:
    def __init__(self, host:str, port:int, logger) -> None:
        self.host = host
        self.port = port
        self.logger = logger
        
    @property
    def address_tuple(self): return (self.host, self.port)

    def Setup(self, ctrl):
        kw = {pt: ds.ModbusSequentialDataBlock.create() for pt in PointType.OPTIONS}
        store = LinkedSlaveContext(ctrl, **kw, zero_mode=False)
        self.context = ds.ModbusServerContext(slaves=store, single=True)

        self.identity = ModbusDeviceIdentification()
        self.identity.VendorName = opt.PROJECT.vendor
        self.identity.ModelName = opt.PROJECT.name
        self.identity.MajorMinorRevision = __version__
    
    def Run(self):
        self.logger.info(f'===== Starting {__class__.__name__} at {self.host}:{self.port} =====')
        StartTcpServer(
            self.context,
            identity=self.identity,
            address=self.address_tuple,
        )