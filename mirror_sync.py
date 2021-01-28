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
    
    def Read(self):
        for src in self.src_list:
            req,val = src.Read()
            if not req:
                self.logger.error(f'Read failed {src} {val}')
            
    
    def Writeback(self, fx, address, values):
        matched_src_list = self._MatchSource(fx, address)
        if len(matched_src_list) == 1:
            src = matched_src_list[0]
            if src.length == len(values):
                original_value = src.value
                req = src.Write(values)
                if req:
                    self.logger.info(f'Writeback success for {src} : {original_value} -> {src.value}')
                else:
                    self.logger.error(f'Writeback failed. {src} {req}')
            else:
                self.logger.warning(f'Unmatched data length: {len(values)} / from source_list: {src.length}')
        elif len(matched_src_list) > 1:
            self.logger.warning('\n'.join([f'Duplicated sources of fx={fx} address={address}', *(str(src) for src in matched_src_list)]))
        else:
            self.logger.warning(f'No matched source of fx={fx} address={address}')
    
    def _MatchSource(self, fx, address):
        matched_list = []
        for src in self.src_list:
            if address == src.target_address_from0:
                matched_list.append(src)

        return matched_list
