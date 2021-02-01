from pathlib import Path
import json
import csv
import time
from threading import Thread
from logger import OneLogger

import factory
from modbus_source import JsonSource, TcpSource

_ADDRESS_START_FROM = 1
class ModbusController:
    def __init__(self,
        config_path: str,
        logger=None,
        mirror_mode: str = factory.DEFAULT_MIRROR_MODE,
        server_mode: str = factory.DEFAULT_SERVER_MODE,
    ):
        self._SetLogger(logger)
        self._GetConfig(config_path)
        self._SetupJsonSource()

        self.mirror = factory.MIRROR[mirror_mode](
            src_list=self._GetSrcList(),
            logger=self.logger,
        )
        self.server : factory.SyncServer = factory.SERVER[server_mode](
            host=self.config_dict['server_host'],
            port=self.config_dict['server_port'],
            logger=self.logger,
        )
        self.server.Setup(self)

    def _SetLogger(self, logger):
        if logger is None:
            logger = OneLogger(
                __class__.__name__,
                level_str='debug',
            )
        self.logger = logger

    def _GetConfig(self, config_path):
        with open(config_path, 'r') as f:
            self.config_dict = json.load(f)
        self.config_dict['address_start_from'] = _ADDRESS_START_FROM

    def _GetSrcList(self):
        src_list = []
        with open(self.config_dict['data_address'], 'r', encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                try:
                    if r.get('SourceIP', '').replace('.', '').isdigit() \
                    and r.get('SourceAddress', '').isdigit() \
                    and r.get('TargetAddress', '').isdigit():
                        # add TcpSource
                        src_list.append(TcpSource(r, self.config_dict))
                    
                    elif r.get('TargetWritable') == '*':
                        # add JsonSource
                        src_list.append(JsonSource.FromDict(r, self.config_dict))
                    
                    else:
                        continue
                
                except Exception as e:
                    self.logger.warning(f'Invalid source: {r}')
        
        # for fpath in Path(self.config_dict['register_folder']).glob('*.json'):
        #     src_list.append(JsonSource.FromFile(fpath))

        return src_list
    
    def _SetupJsonSource(self):
        JsonSource.default_datatype_str = self.config_dict['default_datatype']
        JsonSource.default_addr_start_from = _ADDRESS_START_FROM
        JsonSource.default_folder = Path(self.config_dict['register_folder'])

    def Start(self, delay, refresh_sec):
        thread = Thread(target=self.UpdateLoop, args=(delay, refresh_sec))
        thread.start()

        try:
            self.server.Run()
        except KeyboardInterrupt:
            self.logger.info('KeyboarInterrupt')
            del thread

    def UpdateLoop(self, delay_sec=0, interval_sec=1):
        self.mirror.Connect()
        if delay_sec: time.sleep(delay_sec)
        while True:
            self.mirror.Read()
            self.WriteContext()
            time.sleep(interval_sec)

    def WriteContext(self):
        for src in self.mirror.src_list:
            if src.value is None: continue

            self.server.context[0x00].setValues(
                fx=src.pointType.fx,
                address=src.target_address_from0,
                values=src.value,
                writeback=False,
            )
    
    def WriteMirror(self, fx, address, values):
        matched_src_list = self.mirror._MatchSourceList(fx, address)
        if len(matched_src_list) == 1:
            src = matched_src_list[0]
            if src.length == len(values):
                original_value = src.value
                req,err = src.Write(values)
                if req:
                    self.logger.info(f'Writeback success for {src} : {original_value} -> {src.value}')
                else:
                    self.logger.error(f'Writeback failed. {src} {err}')
            else:
                self.logger.warning(f'Unmatched data length: {len(values)} / from source_list: {src.length}')
        elif len(matched_src_list) > 1:
            self.logger.warning('\n'.join([f'Duplicated sources of fx={fx} address={address}', *(str(src) for src in matched_src_list)]))
        else:
            self.logger.warning(f'No matched source of fx={fx} address={address}')
            # src = JsonSource.FromFx(fx, address, values)
            # req,_ = src.Write()
            # if req:
            #     self.src_list.append(src)
            #     self.logger.info(f'New source created {src} val={values}')
            # else:
            #     self.logger.error(f'Failed to create JsonSource {src}')

if __name__ == "__main__":
    ctrl = ModbusController('./config.json', mirror_mode='sync', server_mode='sync')
    ctrl.Start(1, 0.5)