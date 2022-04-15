import json
import csv
import time
import os.path
from pathlib import Path
from threading import Thread, Event
from logger import OneLogger

import factory
from source import ModbusTarget
from source import PyModbusTcpSource, JsonSource, HslModbusTcpSource
from source.list import SourceList
from pymodbus_context import LinkedSlaveContext
from model.config import Config

__version__ = (1, 3, 1)

class ModbusController:
    _default_source_come_from = 'csv'
    _default_address_path = Path('./address.csv')
    _default_register_folder = Path('./.register/')
    _default_addr_start_from = 1
    _default_source_port = 502
    _default_source_sid = 0x01
    _default_pointtype_str = 'hr'
    _default_datatype_str = 'float32'
    _default_server_host = '127.0.0.1'
    _default_abcd_str = 'ABCD'
    _default_server_port = 5020
    _default_server_sid = 0x00
    _default_server_null_value = -99
    _default_mirror_refresh_sec = 0.5
    _default_mirror_retry_sec = 10 * 60
    _default_readwrite_retry_sec = 10 * 60
    _default_shutdown_delay_sec = 0

    __version__ = __version__

    def __init__(self,
                 logger=None,
                 verbose=False,
                 mirror_mode: str = factory.DEFAULT_MIRROR_MODE,
                 server_mode: str = factory.DEFAULT_SERVER_MODE,
                 **kw,
                 ):
        self.verbose = verbose
        self._SetLogger(logger)
        self._SetConfig(**kw)
        self._SetSources()

        self.mirror = factory.MIRROR[mirror_mode](
            src_list=SourceList(self._address_path, self.logger),
            logger=self.logger,
        )
        self.context = LinkedSlaveContext.ServerContext(
            ctrl=self,
            zero_mode=True,
            single_slave_mode=True,
        )
        self.server = factory.SERVER[server_mode](
            host=self._server_host,
            port=self._server_port,
            logger=self.logger,
        )
        self.server.Setup(self.context, allow_reuse_address=True)

        self.__read_request = False
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
        self._abcd_str = self._getattr(kw, 'abcd_str')
        self._server_host = self._getattr(kw, 'server_host')
        self._server_port = int(self._getattr(kw, 'server_port'))
        self._server_sid = int(self._getattr(kw, 'server_sid'))
        self._server_null_value = self._getattr(kw, 'server_null_value')
        self._mirror_refresh_sec = float(self._getattr(kw, 'mirror_refresh_sec'))
        self._mirror_retry_sec = int(self._getattr(kw, 'mirror_retry_sec'))
        self._readwrite_retry_sec = int(self._getattr(kw, 'readwrite_retry_sec'))
        self._shutdown_delay_sec = int(self._getattr(kw, 'shutdown_delay_sec'))

    def _PreCheck(self):
        assert all([
            self._addr_start_from in [0, 1],
            self._server_host.replace('.', '').isdigit(),
        ])
    @classmethod
    def from_config_obj(cls, config_path, *args, **kw):
        ext = os.path.splitext(config_path)[-1]
        if ext == '.json':
            config_dict = Config.get_from_json(config_path).dict()
        elif ext == '.db':
            config_dict = Config.get_from_sql(config_path).dict()
        else:
            raise ValueError('Config副檔名應為.json or .db')
        return cls(*args, **kw, **config_dict)

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
        kw = {attr: getattr(self, '_' + attr) for attr in [
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

    def _SetSources(self):
        ModbusTarget._default_pointtype_str = self._pointtype_str
        ModbusTarget._default_datatype_str = self._datatype_str
        ModbusTarget._default_abcd_str = self._abcd_str
        ModbusTarget._default_addr_start_from = self._addr_start_from

        PyModbusTcpSource._default_port = self._source_port
        PyModbusTcpSource._default_slave_id = self._source_sid

        HslModbusTcpSource._default_port = self._source_port
        HslModbusTcpSource._default_slave_id = self._source_sid

        JsonSource._default_folder = Path(self._register_folder)

    def Start(self):
        self.__runserver_request = False
        # mirror_thread = Thread(target=self.UpdateLoop, name='CtrlMirror')
        # mirror_thread.start()
        connect_thread = Thread(target=self._connect_loop, name='CtrlConnect')
        connect_thread.start()

        readwrite_thread = Thread(target=self._readwrite_loop, name='CtrlReadWrite')
        readwrite_thread.start()

        read_recover_thread = Thread(target=self._readfail_recover_loop, name='CtrlReadfailRecover')
        read_recover_thread.start()

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

    def _connect_loop(self):
        try:
            self.mirror.connect_all()
            self.__read_request = True
        except Exception as e:
            self.logger.error(f'(Connect-Loop) error: {e}')
            self.Stop()

        while True:
            time.sleep(self._mirror_retry_sec)
            try:
                self.mirror.connect_retry()
            except Exception as e:
                self.logger.error(f'(Retry-Loop) error: {e}')

    def _readwrite_loop(self):
        while not self.__read_request:
            pass

        _tag = True
        _times = []
        while True:
            try:
                self.mirror.Read()
                self.WriteContext()
                time.sleep(self._mirror_refresh_sec)
                if _tag:
                    _tag = False
                    self.__runserver_request = True

                if self.verbose:
                    _times.append(time.time())
                    if len(_times) > 1:
                        print(f"[{len(_times) - 1}] {_times[-1] - _times[-2] :.2f}")
                        if len(_times) > 10:
                            time_span = _times[-1] - _times[0]
                            time_avg = time_span / (len(_times) - 1)
                            self.logger.info(f"(Readwrite-Loop) Interval: {time_avg:.1f} sec")
                            _times = _times[-1:]

            except Exception as e:
                self.logger.error(f"(Readwrite-Loop) error: {e}")
                self.logger.info('(Radwrite-Loop) pausing...')
                time.sleep(self._readwrite_retry_sec)
                self.logger.info('(Radwrite-Loop) resumed')

    def _readfail_recover_loop(self):
        while True:
            self.logger.debug('(Readfail-Recover-Loop) recovering...')
            try:
                self.mirror.readfail_recover()
            except Exception as e:
                self.logger.error(f"(Readfail-Recover-Loop) error: {e}")
            finally:
                time.sleep(self._readwrite_retry_sec)

    def WriteContext(self):
        for src in self.mirror.src_list:
            new_val = src.values
            if new_val is None:
                new_val = src.dataType.Encode(self._server_null_value)

            else:
                _encoded = src.dataType.Decode(new_val)
                if src.formula_x_str:
                    try:
                        # 驗證公式的合法性
                        if not all(chr_ in factory.FORMULA_X_VALIABLE_CHRS for chr_ in src.formula_x_str):
                            raise ValueError(
                                f'Invalid formula_x_str: {src.formula_x_str}')

                        _formulated = eval(
                            src.formula_x_str.replace(
                                'x', '{x}'
                            ).replace(
                                'X', '{x}'
                            ).format(x=_encoded)
                        )
                    except Exception as e:
                        self.logger.warning(f'Invalid formula: {e}')
                        _formulated = _encoded
                else:
                    _formulated = _encoded
                new_val = src.target.dataType.Encode(_formulated)

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
