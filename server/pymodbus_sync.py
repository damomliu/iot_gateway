from pymodbus.server.sync import StartTcpServer, ModbusTcpServer
from ._base import ServerBase

__version__ = (0, 0, 1)

# class SyncServer(ServerBase):
#     """使用 pymodbus 的 StartTcpServer()
#     """    
#     def __init__(self, host: str, port: int, logger) -> None:
#         super().__init__(host, port, logger)
    
#     def _SetIdentity(self):
#         super()._SetIdentity()
#         self.identity.MajorMinorRevision = __version__

#     def Run(self):
#         self.logger.info(f'===== Starting {__class__.__name__} at {self.host}:{self.port} =====')
#         StartTcpServer(
#             self.context,
#             identity=self.identity,
#             address=self.address_tuple,
#         )
    
#     def Stop(self):
#         raise NotImplementedError


class SyncTcpServer(ServerBase, ModbusTcpServer):
    """繼承 pymodbus.ModbuxTcpServer 的子類
    """
    def __init__(self, host: str, port: int, logger) -> None:
        ServerBase.__init__(self, host, port, logger)

    def _SetIdentity(self):
        super()._SetIdentity()
        self.identity.MajorMinorRevision = __version__
    
    def Setup(self, context, allow_reuse_address=False, **kwargs):
        """ModbusTcpServer 的初始化
        """        
        super().Setup(context)
        ModbusTcpServer.__init__(
            self,
            context=self.context,
            identity=self.identity,
            address=self.address_tuple,
            allow_reuse_address=allow_reuse_address,
            **kwargs,
        )

    def Run(self):
        self.logger.info(f'===== Starting {__class__.__name__} at {self.host}:{self.port} =====')
        self.serve_forever()

    def Stop(self):
        self.logger.info('Stopping...')
        # self.server_close()
        self.shutdown()
        self._thread.join()
        self.logger.info('Shutdown complete!')
