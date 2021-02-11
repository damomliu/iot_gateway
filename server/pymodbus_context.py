import pymodbus.datastore as ds

class LinkedSlaveContext(ds.ModbusSlaveContext):
    def __init__(self, ctrl, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctrl = ctrl

    def setValues(self, fx, address, values, writeback=True):
        super().setValues(fx, address, values)
        if writeback:
            self.ctrl.WriteMirror(fx, address, values)