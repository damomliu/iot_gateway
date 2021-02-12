import pymodbus.datastore as ds
from source import PointType

class LinkedSlaveContext(ds.ModbusSlaveContext):
    def __init__(self, ctrl, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctrl = ctrl

    def setValues(self, fx, address, values, writeback=True):
        super().setValues(fx, address, values)
        if writeback:
            self.ctrl.WriteMirror(fx, address, values)

    @classmethod
    def ServerContext(cls, ctrl, zero_mode:bool=False, single_slave_mode:bool=True):
        kw = {pt: ds.ModbusSequentialDataBlock.create() for pt in PointType.OPTIONS}
        store = cls(ctrl, **kw, zero_mode=zero_mode)
        return ds.ModbusServerContext(slaves=store, single=single_slave_mode)
