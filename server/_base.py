import abc
from pymodbus.device import ModbusDeviceIdentification

class ServerInfo:
    name = 'Modbus Controller'
    vendor = 'CYAN Intelligent'

class ServerBase(metaclass=abc.ABCMeta):
    def __init__(self, host:str, port:int, logger) -> None:
        self.host = host
        self.port = port
        self.logger = logger
        self._SetIdentity()
        
    @property
    def address_tuple(self): return (self.host, self.port)

    def _SetIdentity(self):
        self.identity = ModbusDeviceIdentification()
        self.identity.VendorName = ServerInfo.vendor
        self.identity.ModelName = ServerInfo.name
        self.identity.MajorMinorRevision = __class__.__name__

    @abc.abstractmethod
    def SetContext(self, ctrl): raise NotImplementedError

    @abc.abstractmethod
    def Run(self):
        """Run server as the main thread
        """   
        raise NotImplementedError

    @abc.abstractmethod
    def Start(self): raise NotImplementedError

    @abc.abstractmethod
    def Stop(self): raise NotImplementedError
