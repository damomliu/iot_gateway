import json
import sqlite3
from pydantic import BaseModel


class Config(BaseModel):
    address_path: str
    register_folder: str
    source_port: int
    pointtype_str: str
    datatype_str: str
    abcd_str: str
    server_host: str
    server_port: int
    separator: str
    security: bool
    crt_path: str
    key_path: str

    @classmethod
    def get_from_json(cls, json_path):
        """ 根據 csv 設定檔獲取實例
        """
        with open(json_path, 'r', encoding='utf-8-sig') as f:
            config_dict = json.load(f)
            return cls(**config_dict)

    @classmethod
    def get_from_sql(cls, sql_path):
        """ 根據 sqllite database設定檔獲取實例
        """
        con = sqlite3.connect(sql_path)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('select * from config')
        config_dict = dict(cur.fetchone())
        cur.close()
        con.close()
        return cls(**config_dict)

if __name__ == '__main__':
    res_json = Config.get_from_json('C:\\Users\\u1021\\Desktop\\Work\\Mission\\config\\ctrl_config.json').dict()
    print('json:', res_json)

    res_sql = Config.get_from_sql('../test.db').dict()
    print('sql:', res_sql)

