import json
from pathlib import Path
from .point_type import PointType
from ._base import SourceBase, _get


class JsonSource(SourceBase):
    _default_folder = None

    def __init__(self, filepath:Path, address, point_type_str, data_type_str, addr_start_from, val=None):
        super().__init__(address, point_type_str, data_type_str, addr_start_from=addr_start_from)
        self.values = val
        self.filepath = filepath

    def __repr__(self) -> str:
        return f'<{__class__.__name__} {self.dataType.type_str}/{self.pointType.type_str}:{self._target_address}>'

    @classmethod
    def FromDict(cls, **kw):
        assert all([getattr(__class__, attr) is not None for attr in [
            '_default_folder',
            '_default_pointtype_str',
            '_default_datatype_str',
            '_default_addr_start_from',
        ]]), f'Need to setup default value for <{__class__.__name__}>'

        kwargs = dict(
            address=int(kw['TargetAddress']),
            point_type_str=_get(kw, 'PointType', __class__._default_pointtype_str),
            data_type_str=_get(kw, 'DataType', __class__._default_datatype_str),
            addr_start_from=_get(kw, 'addr_start_from', __class__._default_addr_start_from),
        )
        kwargs.update(
            filepath=__class__._default_folder / f'{kwargs["point_type_str"]}_{kwargs["address"]:05d}.json',
        )
        # filepath = __class__._default_folder / f'{point_type_str}_{address:05d}.json',
        return cls(**kwargs)

    # @classmethod
    # def FromFile(cls, filepath):
    #     with open(filepath, 'r') as f:
    #         _dict = json.load(f)
    #     return cls(filepath, **_dict)

    # @classmethod
    # def FromFx(cls, fx, address, values):
    #     assert all([
    #         __class__._default_datatype_str is not None,
    #         __class__._default_addr_start_from is not None,
    #         __class__._default_folder is not None,
    #     ]), f'Need to setup default value for <{__class__.__name__}>'

    #     if fx in [6, 16]:
    #         pt = 'hr'
    #     elif fx in [5, 16]:
    #         pt = 'co'
    #     else:
    #         raise RuntimeError(f'Invalid fx = {fx}')

    #     if not hasattr(values, '__iter__'):
    #         values = [values]

    #     return cls(
    #         filepath=__class__._default_folder / f'{pt}_{address:05d}.json',
    #         address=address,
    #         point_type_str=pt,
    #         data_type_str=__class__._default_datatype_str,
    #         addr_start_from=__class__._default_addr_start_from,
    #         val=values,
    #     )

    @property
    def dict(self):
        return dict(
            address=self._target_address,
            point_type_str=self.pointType.type_str,
            data_type_str=self.dataType.type_str,
            addr_start_from=self._addr_start_from,
            val=self.values,
        )

    def Connect(self):
        res_list = []
        info_list = []
        if not self.filepath.exists():
            wres,winfo = self.Write([0] * self.length)
            if not wres:
                res_list.append(0)
                info_list.append(f'...file created failed {self} {winfo}')
            else:
                res_list.append(-1)
                info_list.append(f'..created {self}')

        rres,rinfo = self.Read()
        res_list.append(rres)
        if rinfo: info_list.append(str(rinfo))
        try:
            info_list.append(f'val={self.dataType.Decode(self.values)}')
        except:
            pass

        return all(res_list), info_list

    def Read(self):
        try:
            with open(self.filepath, 'r') as f:
                _dict = json.load(f)

            if self.pointType.type_str != _dict['point_type_str']:
                self.pointType = PointType(_dict['point_type_str'])
            if self.dataType.type_str != _dict['data_type_str']:
                raise Exception('Datatype Change')

            self._target_address = _dict['address']
            self._addr_start_from = _dict['addr_start_from']
            self.values = _dict['val']

            return 1,None
        except Exception as e:
            return 0,e

    def Write(self, values=None):
        if values is None:
            if self.values is None: raise RuntimeError(f'No values to be written: {self}')
            values = self.values
        else:
            self.values = values[:self.length]

        try:
            if not self.filepath.parent.is_dir(): self.filepath.parent.mkdir()
            with open(self.filepath, 'w+') as f:
                json.dump(self.dict, f, indent=2)
            return 1,None
        except Exception as e:
            return 0,e
