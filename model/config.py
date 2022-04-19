import os
import sqlite3
from pydantic import BaseModel


class SourceConfig(BaseModel):
    address_path: str = './address.csv'
    register_folder: str = './.register/'
    addr_start_from: int = 1
    source_port: int = 502
    source_sid: int = 0x01
    pointtype_str: str = 'hr'
    datatype_str: str = 'float32'
    abcd_str: str = 'ABCD'
    server_host: str = '127.0.0.1'
    server_port: int = 5020
    server_sid: int = 0x00
    server_null_value: int = -99
    mirror_refresh_sec: float = 0.5
    mirror_retry_sec: int = 10 * 60
    readwrite_retry_sec: int = 10 * 60
    shutdown_delay_sec: int = 0


class OpcuaConfig(BaseModel):
    separator: str
    security: bool
    crt_path: str
    key_path: str

class MetaSingleTon(type):
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Config(SourceConfig):
    @classmethod
    def from_sqllite(cls, sql_path):
        """ 根據 sqllite database設定檔獲取實例
        """
        con = sqlite3.connect(sql_path)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('select * from config')
        config_dict = cur.fetchone()
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


if __name__ == '__main__':

    res_sql = Config.from_sqllite('../test.db').dict()
    print('sql:', res_sql)

