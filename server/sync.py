from pymodbus.server.sync import StartTcpServer
import pymodbus.datastore as ds

from ._base import ServerBase
from .modbus_context import LinkedSlaveContext
from source import PointType

__version__ = (0, 0, 1)

class SyncServer(ServerBase):
    def __init__(self, host: str, port: int, logger) -> None:
        super().__init__(host, port, logger)
    
    def _SetIdentity(self):
        super()._SetIdentity()
        self.identity.MajorMinorRevision = __version__

    def SetContext(self, ctrl):
        kw = {pt: ds.ModbusSequentialDataBlock.create() for pt in PointType.OPTIONS}
        store = LinkedSlaveContext(ctrl, **kw, zero_mode=False)
        self.context = ds.ModbusServerContext(slaves=store, single=True)

    def Run(self):
        self.logger.info(f'===== Starting {__class__.__name__} at {self.host}:{self.port} =====')
        StartTcpServer(
            self.context,
            identity=self.identity,
            address=self.address_tuple,
        )
    
    def Start(self):
        raise NotImplementedError
    
    def Stop(self):
        raise NotImplementedError
