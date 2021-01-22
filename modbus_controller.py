import csv
import json
import logging
import asyncio
import time
from threading import Thread

from pymodbus.device import ModbusDeviceIdentification
import pymodbus.datastore as ds

POINT_TYPES = {'co': 1, 'di': 2, 'hr': 3, 'ir': 4}

class SyncModbusController:
    def __init__(self, config_path: str, logger=None, src_mode_str='sync', refresh_sec:float=1) -> None:
        self._SetLogger(logger)
        self._GetConfig(config_path)
        self._GetSources(src_mode_str)

        self.context_list_dict = {pt: [0] * 0xFF for pt in POINT_TYPES}
        self._SetupServer()

    def _SetLogger(self, logger):
        if logger is None:
            logger = logging.getLogger(__class__.__name__)
            logger_format = logging.Formatter(
                '%(asctime)s@' + logger.name + '[%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(logger_format)

            logger.addHandler(stream_handler)
            logger.setLevel(logging.DEBUG)

        self.logger = logger

    def _GetConfig(self, config_path):
        with open(config_path, 'r') as f:
            self.config_dict = json.load(f)

    @property
    def server_address(self): return (self.config_dict['server_host'], self.config_dict['server_port'])

    def _GetSources(self, src_mode_str):
        if src_mode_str == 'sync':
            from pymodbus.client.sync import ModbusTcpClient as ModbusClient
        elif src_mode_str == 'async':
            self._GetSources_async()
        else:
            self.logger.error(f'SourceMode not supported: {src_mode_str}')

        self.src_list = []
        with open(self.config_dict['data_address'], 'r', encoding='utf-8-sig') as f:
            rows = csv.DictReader(f)
            for i,r in enumerate(rows):
                ip = r['SourceIP']
                address = int(r['SourceAddress'])
                # if ip in self.src_ip_list:
                if False:
                    self.logger.warning(f'Duplicated IP [{ip}] at row[{i+2}]')
                    continue
                else:
                    port = r.get('SourcePort', self.config_dict['default_source_port'])
                    src = ModbusClient(ip, port=port)
                    src.address = address
                    src.length = int(r.get('SourceLength') if r.get('SourceLength') else self.config_dict['default_source_length'])
                    if src.length > 1:
                        src.length = int(src.length / 2)
                    src.point_type = r.get('SourcePointType') if r.get('SourcePointType') else self.config_dict['default_source_pointtype']
                    src.value = None
                    src.desc = r.get('SourceDesc')

                    src.target_address = int(r['TargetAddress'])
                    src.target_desc = r.get('TargetDesc')
                    self.src_list.append(src)

    # def _GetSources_async(self):
    #     from pymodbus.client.asynchronous.tcp import AsyncModbusTCPClient as ModbusClient
    #     from pymodbus.client.asynchronous import schedulers

    #     self.src_list = []
    #     loop = asyncio.new_event_loop()
    #     with open(self.config_dict['data_address'], 'r', encoding='utf-8-sig') as f:
    #         rows = csv.DictReader(f)
    #         for i,r in enumerate(rows):
    #             ip = r['SourceIP']
    #             address = int(r['SourceAddress'])
    #             if False:
    #                 self.logger.warning(f'Duplicated IP [{ip}] at row[{i+2}]')
    #                 continue
    #             else:
    #                 port = r.get('SourcePort', self.config_dict['default_source_port'])
    #                 loop, src = ModbusClient(schedulers.ASYNC_IO, host=ip, port=port)
    #                 src.address = address
    #                 src.length = int(r.get('SourceLength') if r.get('SourceLength') else self.config_dict['default_source_length'])
    #                 if src.length > 1:
    #                     src.length = int(src.length / 2)
    #                 src.point_type = r.get('SourcePointType') if r.get('SourcePointType') else self.config_dict['default_source_pointtype']
    #                 src.value = None
    #                 src.desc = r.get('SourceDesc')

    #                 src.target_address = int(r['TargetAddress'])
    #                 src.target_desc = r.get('TargetDesc')
    #                 self.src_list.append(src)

    @property
    def src_ip_list(self): return [src.host for src in self.src_list]

    def _ConnectSource(self):
        for i,src in enumerate(self.src_list[:]):
            src.connect()
            if src.socket is None:
                self.logger.warning(f'not connected : {src.host}')
                del self.src_list[i]

        self.logger.info(f'connected to {len(self.src_list)} sources')

        src_table_str = (
            '[target] ip @address *length\n' +
            '\n'.join(f'[{src.target_address}] {src.host} @{src.address} *{src.length}' for src in self.src_list)
        )
        self.logger.debug(src_table_str)

    def _DisconnectSource(self):
        for src in self.src_list:
            src.close()

    @staticmethod
    def _Valid(req, point_type):
        if not req.isError():
            if point_type in ['co', 'di']:
                return req.bits
            elif point_type in ['hr', 'ir']:
                return req.registers
            else:
                raise KeyError(f'Invalid point_type: {point_type}')

    def _UpdateFromAllSource(self):
        slave_id = 0x00
        for src in self.src_list:
            args = (src.address, src.length)
            read_func = dict(
                co=src.read_coils,
                di=src.read_discrete_inputs,
                hr=src.read_holding_registers,
                ir=src.read_input_registers
            )[src.point_type]
            src.value = self._Valid(read_func(*args), src.point_type)
            self.context_list_dict[src.point_type][src.target_address] = src.value
            
            fx_int = POINT_TYPES[src.point_type]
            self.context[slave_id].setValues(fx_int, src.target_address, src.value)

    def _SetupServer(self):
        kw = {pt: ds.ModbusSequentialDataBlock(0, self.context_list_dict[pt]) for pt in POINT_TYPES}
        store = ds.ModbusSlaveContext(**kw, zero_mode=False)
        self.context = ds.ModbusServerContext(slaves=store, single=True)

        self.identity = ModbusDeviceIdentification()
        self.identity.VendorName = 'CYAN Intelligent'
        self.identity.ProductCode = ''
        self.identity.VendorUrl = 'Modbus Controller'
        self.identity.ModelName = 'Modbus Controller'
        self.identity.MajorMinorRevision = '0.0.0'

    def Update(self, delay_sec=0, interval=1):
        self._ConnectSource()
        if delay_sec: time.sleep(delay_sec)
        while True:
            self._UpdateFromAllSource()
            time.sleep(interval)

    def Run(self):
        from pymodbus.server.sync import StartTcpServer
        
        thread = Thread(target=self.Update, args=(3, 1))
        thread.start()
        
        StartTcpServer(
            self.context,
            identity=self.identity,
            address=self.server_address,
        )


class AsyncModbusController:
    async def _AsyncServer(self):
        from pymodbus.server.async_io import StartTcpServer
        await StartTcpServer(
            self.context,
            identity=self.identity,
            address=self.server_address,
            allow_reuse_address=True,
            defer_start=False
        )

    def Run(self):
        asyncio.run(self._AsyncServer())


if __name__ == "__main__":
    modbusCtrl = SyncModbusController('./config.json', src_mode_str='sync')
    modbusCtrl.Run()
