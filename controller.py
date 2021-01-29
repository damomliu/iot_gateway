from pathlib import Path
import json
import csv
import time
from threading import Thread
from logger import OneLogger

import factory
from modbus_source import JsonSource, TcpSource


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
        self.server.Setup(self.mirror)

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

    def _GetSrcList(self):
        src_list = []
        with open(self.config_dict['data_address'], 'r', encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                if not r.get('SourceIP'):
                    continue

                try:
                    src_list.append(TcpSource(r, self.config_dict))
                except Exception as e:
                    self.logger.warning(f'Invalid source: {r}')
        
        for fpath in Path(self.config_dict['contract_folder']).glob('*.json'):
            src_list.append(JsonSource.FromFile(fpath))

        return src_list
    
    def _SetupJsonSource(self):
        JsonSource.default_datatype_str = self.config_dict['default_contract_datatype']
        JsonSource.default_addr_start_from = int(self.config_dict['address_start_from_1'])
        JsonSource.default_folder = Path(self.config_dict['contract_folder'])

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
            self._WriteContext()
            time.sleep(interval_sec)

    def _WriteContext(self):
        for src in self.mirror.src_list:
            if src.value is None: continue

            self.server.context[0x00].setValues(
                fx=src.pointType.fx,
                address=src.target_address,
                values=src.value,
                writeback=False,
            )

if __name__ == "__main__":
    ctrl = ModbusController('./config.json', mirror_mode='sync', server_mode='sync')
    ctrl.Start(1, 0.5)