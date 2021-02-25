from pathlib import Path
import json
import csv
import time
from threading import Thread, Event
from logger import OneLogger

import factory
from source import ModbusTarget
from source import PyModbusTcpSource, JsonSource, HslModbusTcpSource
from pymodbus_context import LinkedSlaveContext


class ModbusController:
    _default_address_path = Path('./address.csv')
    _default_register_folder = Path('./.register/')
    _default_addr_start_from = 1
    _default_source_port = 502
    _default_source_sid = 0x01
    _default_pointtype_str = 'hr'
    _default_datatype_str = 'float32'
    _default_server_host = '127.0.0.1'
    _default_server_port = 5020
    _default_server_sid = 0x00
    _default_server_null_value = -99
    _default_mirror_refresh_sec = 0.5
    _default_shutdown_delay_sec = 0

    def __init__(self,
        logger=None,
        mirror_mode: str = factory.DEFAULT_MIRROR_MODE,
        server_mode: str = factory.DEFAULT_SERVER_MODE,
        **kw,
    ):
        self._SetLogger(logger)
        self._SetConfig(**kw)
        self._SetSources()

        self.mirror = factory.MIRROR[mirror_mode](
            src_list=self.LoadSrcList(),
            logger=self.logger,
        )
        self.context = LinkedSlaveContext.ServerContext(
            ctrl=self,
            zero_mode=bool(not self._addr_start_from),
            single_slave_mode=True,
        )
        self.server = factory.SERVER[server_mode](
            host=self._server_host,
            port=self._server_port,
            logger=self.logger,
        )
        self.server.Setup(self.context, allow_reuse_address=True)

        self.__runserver_request = False
        self.__shutdown_request = False
        self.__shutdownEvent = Event()

    def _SetLogger(self, logger):
        if logger is None:
            logger = OneLogger(
                __class__.__name__,
                level_str='info',
            )
        self.logger = logger

    def _getattr(self, kw, attr_name):
        _attr = '_' + attr_name
        if not hasattr(self, _attr):
            default_val = getattr(__class__, f'_default{_attr}')
        else:
            default_val = getattr(self, _attr)
        return kw.get(attr_name, default_val)

    def _SetConfig(self, **kw):
        self._address_path = Path(self._getattr(kw, 'address_path'))
        self._addr_start_from = self._getattr(kw, 'addr_start_from')
        self._register_folder = Path(self._getattr(kw, 'register_folder'))
        self._source_port = int(self._getattr(kw, 'source_port'))
        self._source_sid = int(self._getattr(kw, 'source_sid'))
        self._pointtype_str = self._getattr(kw, 'pointtype_str')
        self._datatype_str = self._getattr(kw, 'datatype_str')
        self._server_host = self._getattr(kw, 'server_host')
        self._server_port = int(self._getattr(kw, 'server_port'))
        self._server_sid = int(self._getattr(kw, 'server_sid'))
        self._server_null_value = self._getattr(kw, 'server_null_value')
        self._mirror_refresh_sec = float(self._getattr(kw, 'mirror_refresh_sec'))
        self._shutdown_delay_sec = int(self._getattr(kw, 'shutdown_delay_sec'))
    
    def _PreCheck(self):
        assert all([
            self._addr_start_from in [0,1],
            self._server_host.replace('.','').isdigit(),
        ])

    @classmethod
    def FromConfigFile(cls, config_path, *args, **kw):
        with open(config_path, 'r') as f:
            config_dict = json.load(f)
        return cls(*args, **kw, **config_dict)

    def LoadConfig(self, config_path):
        with open(config_path, 'r') as f:
            config_dict = json.load(f)
        self._SetConfig(**config_dict)

    @property
    def config_dict(self):
        kw = {attr: getattr(self, '_'+attr) for attr in [
            'address_path',
            'addr_start_from',
            'register_folder',
            'source_port',
            'pointtype_str',
            'datatype_str',
            'server_host',
            'server_port',
            'mirror_refresh_sec',
        ]}
        return kw

    def LoadSrcList(self):
        src_list = []
        with open(self._address_path, 'r', encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                protocol_str = r.get('SourceProtocol')
                try:
                    if protocol_str.startswith('modbus_tcp'):
                        # add TcpSource
                        if protocol_str.endswith('tcp1'):
                            src_list.append(PyModbusTcpSource.FromDict(**r, is_writable=False))
                        elif protocol_str.endswith('tcp1rw'):
                            src_list.append(PyModbusTcpSource.FromDict(**r, is_writable=True))
                        elif protocol_str.endswith('tcp2'):
                            src_list.append(HslModbusTcpSource.FromDict(**r, is_writable=False))
                        elif protocol_str.endswith('tcp2rw'):
                            src_list.append(HslModbusTcpSource.FromDict(**r, is_writable=True))

                    elif protocol_str == 'json':
                        # add JsonSource
                        src_list.append(JsonSource.FromDict(**r))

                    else:
                        continue

                except Exception as e:
                    self.logger.warning(f'Invalid source: {e} / {r}')

        # for fpath in Path(self.config_dict['register_folder']).glob('*.json'):
        #     src_list.append(JsonSource.FromFile(fpath))

        return src_list

    def _SetSources(self):
        ModbusTarget._default_pointtype_str = self._pointtype_str
        ModbusTarget._default_datatype_str = self._datatype_str
        ModbusTarget._default_addr_start_from = self._addr_start_from

        PyModbusTcpSource._default_port = self._source_port
        PyModbusTcpSource._default_slave_id = self._source_sid

        HslModbusTcpSource._default_port = self._source_port
        HslModbusTcpSource._default_slave_id = self._source_sid

        JsonSource._default_folder = Path(self._register_folder)

    def Start(self):
        self.__runserver_request = False
        mirror_thread = Thread(target=self.UpdateLoop, name='CtrlMirror')
        mirror_thread.start()

        try:
            while not self.__runserver_request:
                pass
        finally:
            self.__runserver_request = False
            self.server.Start(name='CtrlServer')

        # shutdown_thread = Thread(target=self.Stop, name='CtrlShutdown')
        # shutdown_thread.start()
        self.__shutdownEvent.clear()
        try:
            while not self.__shutdown_request:
                pass
        finally:
            self.__shutdown_request = False
            self.__shutdownEvent.set()

    def Stop(self):
        for i in range(self._shutdown_delay_sec):
            left_sec = self._shutdown_delay_sec - i
            time.sleep(1)
            print(f'<{left_sec}>')

        self.server.Stop()
        self.logger.info('Ctrl closing...')
        self.__shutdown_request = True
        self.__shutdownEvent.wait()
        self.logger.info('Ctrl is closed completely.')
        

    def UpdateLoop(self):
        self.mirror.Connect()

        _tag = True
        while True:
            self.mirror.Read()
            self.WriteContext()
            time.sleep(self._mirror_refresh_sec)
            if _tag:
                _tag = False
                self.__runserver_request = True

    def WriteContext(self):
        for src in self.mirror.src_list:
            new_val = src.values
            if new_val is None:
                new_val = src.dataType.Encode(self._server_null_value)

            self.server.context[0x00].setValues(
                fx=src.target.pointType.fx,
                address=src.target.address_from0,
                values=new_val,
                writeback=False,
            )

    def WriteMirror(self, fx, address, values):
        self.mirror.Write(fx, address, values)


class MetaSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class ControllerSingleton(ModbusController, metaclass=MetaSingleton):
    pass


if __name__ == "__main__":
    # ctrl = ModbusController(mirror_mode='sync', server_mode='sync')
    ctrl = ModbusController.FromConfigFile('./config.json')
    ctrl.Start()