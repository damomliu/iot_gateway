from pymodbus.server.sync import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
import pymodbus.datastore as ds

from modbus_types import PointType, DataType
import opt

__version__ = '0.0.0'

class SyncServer:
    def __init__(self, host:str, port:int, logger) -> None:
        self.host = host
        self.port = port
        self.logger = logger
        
        self._Setup()

    @property
    def address_tuple(self): return (self.host, self.port)

    def _Setup(self):
        kw = {pt: ds.ModbusSequentialDataBlock.create() for pt in PointType.OPTIONS}
        store = ds.ModbusSlaveContext(**kw, zero_mode=False)
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