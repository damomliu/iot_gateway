import json
from pathlib import Path
from . import PointType, DataType
from ._base import SourcePairBase, ClientBase, _get, _clean_dict
from .pymodbus import ModbusTarget


class JsonSource(SourcePairBase):
    _default_folder = None

    def __init__(self, filepath, target,
                 point_type_str: str = None,
                 data_type_str: str = None,
                 formula_x_str: str = None,
                 desc=None,
                 values=None):
        super().__init__(
            client=JsonClient(filepath),
            target=target,
            desc=desc
        )
        self.pointType = PointType(
            point_type_str) if point_type_str else self.target.pointType
        self.dataType = DataType(
            data_type_str, self.pointType) if data_type_str else self.target.dataType
        self.formula_x_str = formula_x_str
        self.values = values

    def __repr__(self) -> str:
        return f'<{__class__.__name__}/{self.target.pointType.type_str} : {self.target.repr_postfix}'

    @property
    def filepath(self):
        return self.client.filepath

    @classmethod
    def from_obj(cls, Address):
        assert all([getattr(__class__, attr) is not None for attr in [
            '_default_folder',
        ]]), f'Need to setup default value for <{__class__.__name__}>'
        target = ModbusTarget.from_address(Address)
        filepath = cls._default_folder / f'{target.pointType.type_str}_{target.address:05d}.json'
        kwargs = _clean_dict(
            filepath=filepath,
            target=target,
            point_type_str=Address.SourcePointType,
            data_type_str=Address.SourceDataype,
            formula_x_str=Address.FormulaX,
            desc=Address.SourceDesc,
        )
        return cls(**kwargs)

    @classmethod
    def FromDict(cls, **kw):
        assert all([getattr(__class__, attr) is not None for attr in [
            '_default_folder',
        ]]), f'Need to setup default value for <{__class__.__name__}>'

        target = ModbusTarget.FromDict(**kw)
        filepath = cls._default_folder / f'{target.pointType.type_str}_{target.address:05d}.json'
        kwargs = _clean_dict(
            filepath=filepath,
            target=target,
            point_type_str=kw.get('SourcePointType'),
            data_type_str=kw.get('SourceDataype'),
            formula_x_str=kw.get('FormulaX'),
            desc=kw.get('SourceDesc')
        )
        return cls(**kwargs)

    @property
    def dict(self):
        return dict(
            address=self.target.address,
            point_type_str=self.target.pointType.type_str,
            data_type_str=self.target.dataType.type_str,
            addr_start_from=self.target.addr_start_from,
            val=self.values,
        )

    def Connect(self):
        res_list = []
        info_list = []
        if not self.filepath.exists():
            wres, winfo = self.Write([0] * self.length)
            if not wres:
                res_list.append(0)
                info_list.append(f'...file created failed {self} {winfo}')
            else:
                res_list.append(-1)
                info_list.append(f'..created {self}')

        rres, rinfo = self.Read()
        res_list.append(rres)
        if rinfo: info_list.append(str(rinfo))
        try:
            info_list.append(f'val={self.target.dataType.Decode(self.values)}')
        except:
            pass
        return all(res_list), info_list

    def Disconnect(self):
        self.values = None
        return 0

    def Read(self):
        try:
            with open(self.filepath, 'r') as f:
                _dict = json.load(f)

            if self.target.pointType.type_str != _dict['point_type_str']:
                self.pointType = PointType(_dict['point_type_str'])
            if self.target.dataType.type_str != _dict['data_type_str']:
                raise Exception('Datatype Change')

            self.target.address = _dict['address']
            self.target.addr_start_from = _dict['addr_start_from']
            self.values = _dict['val']

            return 1, None
        except Exception as e:
            self.values = None
            return 0, e

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
            return 1, None
        except Exception as e:
            return 0, e


class JsonClient(ClientBase):
    def __init__(self, filepath):
        self.filepath = Path(filepath)

    def __eq__(self, o) -> bool:
        if not isinstance(o, JsonClient):
            return False

        else:
            my_path = self.filepath.resolve()
            o_path = Path(o.filepath).resolve()
            return my_path == o_path

    def _error(self):
        raise Exception('JsonClient is not a connection')

    def Connect(self):
        self._error()

    def Disconnect(self):
        self._error()

    def Read(self):
        self._error()

    def Write(self):
        self._error()
