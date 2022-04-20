import os
import sqlite3
from pydantic import BaseModel, Field


class OpcuaConfig(BaseModel):
    separator: str = Field(alias='separator', default='+-')
    security: bool = Field(alias='security', default=True)
    crt_path: str = Field(alias='crt_path', default='../config/security/client_crt.der')
    key_path: str = Field(alias='key_path', default='../config/security/client_key.pem')


class SourceConfig(BaseModel):
    address_path: str = Field(alias='address_path', default='./address.csv')
    register_folder: str = Field(alias='register_folder', default='./.register/')
    addr_start_from: int = Field(alias='addr_start_from', default=1)
    source_port: int = Field(alias='source_port', default=502)
    source_sid: int = Field(alias='source_sid', default=0x01)
    pointtype_str: str = Field(alias='pointtype_str', default='hr')
    datatype_str: str = Field(alias='datatype_str', default='float32')
    abcd_str: str = Field(alias='abcd_str', default='ABCD')
    server_host: str = Field(alias='server_host', default='127.0.0.1')
    server_port: int = Field(alias='server_port', default=5020)
    server_sid: int = Field(alias='server_sid', default=0x00)
    server_null_value: int = Field(alias='server_null_value', default=-99)
    mirror_refresh_sec: float = Field(alias='mirror_refresh_sec', default=0.5)
    mirror_retry_sec: int = Field(alias='mirror_retry_sec', default=10 * 60)
    readwrite_retry_sec: int = Field(alias='readwrite_retry_sec', default=10 * 60)
    shutdown_delay_sec: int = Field(alias='shutdown_delay_sec', default=0)
    opcua: OpcuaConfig = Field(alias='opcua', default=None)


class Config(SourceConfig):
    @classmethod
    def from_sqllite(cls, sql_path):
        """ 根據 sqllite database設定檔獲取實例
        """
        con = sqlite3.connect(sql_path)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('select * from config')
        config_dict = dict(cur.fetchone())
        config_dict['opcua'] = OpcuaConfig(**config_dict)
        cur.close()
        con.close()
        return cls(**config_dict)

    @classmethod
    def create(cls, config_path):
        ext = os.path.splitext(config_path)[-1]
        if ext == '.json':
            config = Config.parse_file(config_path)
        elif ext == '.db':
            config = Config.from_sqllite(config_path)
        else:
            raise ValueError('Config副檔名應為.json or .db')
        return config

class MetaSingleTon(type):
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


if __name__ == '__main__':
    res_sql = Config.from_sqllite('../test.db').dict()
    print('sql:', res_sql)
