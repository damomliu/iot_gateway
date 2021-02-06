import abc
from os import remove, replace
from . import PointType, DataType


class TargetBase(metaclass=abc.ABCMeta):
    pass


class SourceBase(metaclass=abc.ABCMeta):
    def __init__(self, ip, port, address, target:TargetBase, desc=None) -> None:
        assert isinstance(target, TargetBase)
        self.ip = ip
        self.port = port
        self.address = address
        self.target = target
        self.desc = desc if desc else ''

    @property
    def length(self): return self.target.length

    @abc.abstractmethod
    def Connect(self):
        """
        Return:
            1,None: connect 成功、無多餘訊息
            1,info_str: connect 成功、並附帶訊息
            0,info_str: connect 失敗、附帶錯誤訊息err 
        """
        raise NotImplementedError

    @abc.abstractmethod
    def Read(self):
        """
        Return:
            1,None: connect 成功、無多餘訊息
            1,info_str: connect 成功、並附帶訊息
            0,info_str: connect 失敗、附帶錯誤訊息err 
        """
        raise NotImplementedError

    @abc.abstractmethod
    def Write(self, values):
        """
        Return:
            1,None: connect 成功、無多餘訊息
            1,info_str: connect 成功、並附帶訊息
            0,info_str: connect 失敗、附帶錯誤訊息err 
        """
        raise NotImplementedError


def _get(_dict, key, val_if_none):
    if _dict.get(key):
        return _dict.get(key)
    else:
        return val_if_none

def _clean_dict(**kw):
    return {k:v for k,v in kw.items() if all([v is not None, v != ''])}