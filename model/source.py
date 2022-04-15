import csv
import sqlite3
from pydantic import BaseModel


class Address(BaseModel):
    SourceProtocol: str
    SourceIP: str
    SourcePort: int
    SourceDeviceID: str
    SourcePointType: str
    SourceAddress: str
    SourceDataype: str
    TargetAddress: int
    DataType: str
    ABCD: str
    FormulaX: str
    TargetDesc: str
    SourceDesc: str
    addr_start_from: str = None

    @classmethod
    def get_from_csv(cls, csv_path):
        """ 根據 csv 設定檔獲取實例
        """
        address_list = []
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            dict_list = list(csv.DictReader(f))[1:]
            for dict in dict_list:
                address_list.append((cls(**dict)))
        return address_list

    @classmethod
    def get_from_sql(cls, sql_path):
        """ 根據 sqllite database設定檔獲取實例
        """
        con = sqlite3.connect(sql_path)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('select * from address')
        sql_list = []
        for data in cur.fetchall():
            sql_list.append((cls(**data)))
        cur.close()
        con.close()
        return sql_list

if __name__ == '__main__':
    res_csv = Address.get_from_csv('../address.csv')
    print('csv:', res_csv)

    res_sql = Address.get_from_sql('../test.db')
    print('sql:', res_sql)
