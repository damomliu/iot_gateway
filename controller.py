import json
import csv
from logger import OneLogger
import time
from threading import Thread

import opt
import factory
from mirror_source import Source


class ModbusController:
    def __init__(self,
        config_path: str,
        logger=None,
        mirror_mode=factory.DEFAULT_MIRROR_MODE,
        server_mode=factory.DEFAULT_SERVER_MODE,
    ):
        self._SetLogger(logger)
        self._GetConfig(config_path)
        
        self.mirror = factory.MIRROR[mirror_mode](
            src_list=self._GetSrcList(),
            logger=self.logger,
        )
        self.server : factory.SyncServer = factory.SERVER[server_mode](
            host=self.config_dict['server_host'],
            port=self.config_dict['server_port'],
            logger=self.logger,
        )

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
        with open(self.config_dict['data_address'], 'r', encoding='utf-8-sig') as f:
            src_list = list(Source(r, self.config_dict) for r in csv.DictReader(f))
        
        return src_list
    
    def Start(self):
        thread = Thread(target=self.UpdateLoop, args=(3, 0.5))
        thread.start()
        
        self.server.Run()
    
    def UpdateLoop(self, delay_sec=0, interval_sec=1):
        self.mirror.Connect()
        if delay_sec: time.sleep(delay_sec)
        while True:
            self.mirror.Read()
            self._UpdateOnce()
            time.sleep(interval_sec)
    
    def _UpdateOnce(self):
        for src in self.mirror.src_list:
            if src.value is None: continue

            fx_int = opt.POINT_TYPE[src.point_type]['fx']
            self.server.context[src.slave_id].setValues(
                fx=fx_int,
                address=src.target_address,
                values=src.value,
            )

if __name__ == "__main__":
    ctrl = ModbusController('./config.json', mirror_mode='sync', server_mode='sync')
    ctrl.Start()