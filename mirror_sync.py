from typing import List
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from modbus_source import Source

class SyncMirror():
    def __init__(self, src_list:List[Source], logger) -> None:
        self.src_list = src_list
        self.logger = logger
        self._SetClient()
        
    def _SetClient(self):
        for i,src in enumerate(self.src_list):
            if not src.client:
                src.client = ModbusClient(src.ip, src.port)
    
    def _ConnectOne(self, src:Source):
        if src.client.connect():
            src.is_connected = True
            self.logger.debug(f'connected to {src} OK')
            return True
        else:
            self.logger.warning(f'...not connected : {src}')
            return False
    
    def Connect(self):
        for src in self.src_list[:]:
            if not self._ConnectOne(src):
                self.src_list.remove(src)
        
        self.logger.info(f'Mirroring from [{len(self.src_list)}] sources')
    
    def Disconnect(self):
        for src in self.src_list:
            if src.is_connected:
                src.client.close()
    
    def __del__(self):
        try:
            self.Disconnect()
        except:
            pass
    
    def _ReadOne(self, src:Source):
        pointType = src.pointType
        req,val = pointType.RequestValue(src.client, src.address_from0, count=src.length, unit=src.slave_id)
        if not req:
            self.logger.warning(f'{src} {val}')
        else:
            src.value = val[:src.length]

    
    def Read(self):
        for src in self.src_list:
            self._ReadOne(src)
        
