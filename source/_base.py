from . import PointType, DataType

class SourceBase:
    def __init__(self, address, point_type_str, data_type_str, addr_start_from=1):
        self.pointType = PointType(point_type_str)
        self.dataType = DataType(data_type_str, self.pointType)
        self._addr_start_from = addr_start_from
        self._target_address = address

    @property
    def length(self): return self.dataType.length
    @property
    def target_address_from0(self): return self._target_address - self._addr_start_from
    @property
    def target_address_set(self):
        _range = range(self.target_address_from0, self.target_address_from0 + self.length)
        return set(list(_range))

    @property
    def address_from0(self): raise NotImplementedError
    def Connect(self):
        """
        Return:
            1,None: connect 成功、無多餘訊息
            1,info_str: connect 成功、並附帶訊息
            0,info_str: connect 失敗、附帶錯誤訊息err 
        """        
        raise NotImplementedError
    def Read(self):
        """
        Return:
            1,None: connect 成功、無多餘訊息
            1,info_str: connect 成功、並附帶訊息
            0,info_str: connect 失敗、附帶錯誤訊息err 
        """   
        raise NotImplementedError
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