from typing import List
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from modbus_source import JsonSource, TcpSource

class SyncMirror():
    def __init__(self, src_list:List[TcpSource], logger) -> None:
        self.src_list = src_list
        self.logger = logger
        self._SetClient()
        
    def _SetClient(self):
        for src in self.src_list:
            if isinstance(src, TcpSource):
                if not src.client:
                    src.client = ModbusClient(src.ip, src.port)
    
    def _ConnectOne(self, src:TcpSource):
        if isinstance(src, TcpSource):
            if src.client.connect():
                src.is_connected = True
                return True
            else:
                return False
        
        elif isinstance(src, JsonSource):
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
            
    def Writeback(self, fx, address, values):
        matched_src_list = self._MatchSourceList(fx, address)
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
            # self.logger.warning(f'No matched source of fx={fx} address={address}')
            src = JsonSource.FromFx(fx, address, values)
            req,_ = src.Write()
            if req:
                self.src_list.append(src)
                self.logger.info(f'New source created {src} val={values}')
            else:
                self.logger.error(f'Failed to create JsonSource {src}')
    
    def _MatchSourceList(self, fx, address):
        matched_list = []
        for src in self.src_list:
            if isinstance(src, TcpSource):
                src_target_address = src.target_address_from0
            elif isinstance(src, JsonSource):
                src_target_address = src._target_address
            else:
                raise NotImplementedError(f'source type {type(src)}')

            if address == src_target_address:
                matched_list.append(src)

        return matched_list
