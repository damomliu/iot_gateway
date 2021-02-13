import abc
from threading import Thread
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
        
        self._thread = None
        
    @property
    def address_tuple(self): return (self.host, self.port)

    def _SetIdentity(self):
        self.identity = ModbusDeviceIdentification()
        self.identity.VendorName = ServerInfo.vendor
        self.identity.ModelName = ServerInfo.name
        self.identity.MajorMinorRevision = __class__.__name__

    def Setup(self, context, *args, **kw):
        """set attribute "context" for server"""        
        self.context = context

    @abc.abstractmethod
    def Run(self):
        """Run server as the main thread"""   
        raise NotImplementedError

    def Start(self, name=None):
        """Run server in another thread"""
        self._thread = Thread(target=self.Run, name=name)
        self._thread.start()

    @abc.abstractmethod
    def Stop(self):
        """Close/Shutdown the thread initiated by Start() method"""
        raise NotImplementedError
