from typing import List
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from mirror_sources import MirrorSourceList
from modbus_source import JsonSource, TcpSource

class SyncMirror():
    def __init__(self, src_list, logger) -> None:
        self.logger = logger
        self.src_list = MirrorSourceList(mirror=self)
        for src in src_list:
            self.src_list.append(src)
        self._SetClient()
    
    def _Validate(self, new_src):
        for src in self.src_list:
            if src.pointType.type_str != new_src.pointType.type_str: continue
            if src.target_address_set.intersection(new_src.target_address_set):
                self.logger.warning(f'Address conflict!! src={src} / new_src={new_src}')
                return -1
    
    def _SetClient(self):
        for src in self.src_list:
            if isinstance(src, TcpSource):
                if not src.client:
                    src.client = ModbusClient(src.ip, src.port)
    
    def _ConnectOne(self, src):
        if isinstance(src, TcpSource):
            if src.client.connect():
                src.is_connected = True
                return True
            else:
                return False
        
        elif isinstance(src, JsonSource):
            if not src.filepath.exists():
                self.logger.info(f'...created {src}')
                src.Write([0] * src.length)
            req,_ = src.Read()
            return req
    
    def Connect(self):
        for src in self.src_list[:]:
            if not self._ConnectOne(src):
                self.logger.warning(f'...not connected : {src}')
                self.src_list.remove(src)
            else:
                self.logger.debug(f'connected to {src} OK')
        
        self.logger.info(f'Mirroring from [{len(self.src_list)}] sources')
    
    def Disconnect(self):
        for src in self.src_list:
            if not hasattr(src, 'client'): continue
            if src.is_connected:
                src.client.close()
    
    def __del__(self):
        try:
            self.Disconnect()
        except:
            pass
    
    def Read(self):
        for src in self.src_list:
            req,val = src.Read()
            if not req:
                self.logger.error(f'Read failed {src} {val}')
            
    def _MatchSourceList(self, fx, address):
        matched_list = []
        for src in self.src_list:
            if address == src.target_address_from0 and fx in src.pointType.write_fx:
                matched_list.append(src)

        return matched_list
