import abc
from os import remove, replace
from . import PointType, DataType


class SourcePairBase(metaclass=abc.ABCMeta):
    def __init__(self, client, target, desc=None):
        assert isinstance(client, ClientBase)
        assert isinstance(target, TargetBase)

        self.client = client
        self.target = target
        self.desc = desc if desc else ''
        self.values = None

    @property
    def length(self): return self.target.length
    def __len__(self): return self.length

    def Connect(self): return self.client.Connect()
    def Disconnect(self): return self.client.Disconnect()

    @abc.abstractmethod
    def Read(self): raise NotImplementedError
    @abc.abstractmethod
    def Write(self, val): raise NotImplementedError


class CommonSourcePair(SourcePairBase):
    pass


class TargetBase(metaclass=abc.ABCMeta):
    pass


class ClientBase(metaclass=abc.ABCMeta):
    def __init__(self, ip, port) -> None:
        self.ip = ip
        self.port = port
        self.values = None
        self._PreCheck()

    def _PreCheck(self):
        assert all([
            self.ip.replace('.','').isdigit(),
            isinstance(self.port, int),
        ])

    @abc.abstractmethod
    def __eq__(self, o) -> bool: raise NotImplementedError

    @abc.abstractmethod
    def Connect(self):
        """
        Return:
            1,None: connect 成功、無多餘訊息
            1,info_str: connect 成功、並附帶訊息
            0,info_str: connect 失敗、附帶錯誤訊息err 
        """
        raise NotImplementedError

    @abc.abstractclassmethod
    def Disconnect(self):
        """
        Return:
            1: 從已連接的狀態變成離線、可能附帶訊息 info_str
            0: 原本就沒有連線
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


class SourceBase(metaclass=abc.ABCMeta):
    def __init__(self, ip, port, address, target:TargetBase, desc=None) -> None:
        assert isinstance(target, TargetBase)
        self.ip = ip
        self.port = port
        self.address = address
        self.target = target
        self.desc = desc if desc else ''

        self.values = None
        self.client = None

    @property
    def length(self): return self.target.length
    def __len__(self): return self.length

    @abc.abstractmethod
    def Connect(self):
        """
        Return:
            1,None: connect 成功、無多餘訊息
            1,info_str: connect 成功、並附帶訊息
            0,info_str: connect 失敗、附帶錯誤訊息err 
        """
        raise NotImplementedError

    @abc.abstractclassmethod
    def Disconnect(self):
        """
        Return:
            1: 從已連接的狀態變成離線、可能附帶訊息 info_str
            0: 原本就沒有連線
        """        
        raise NotImplementedError

    def __del__(self):
        self.Disconnect()

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