import pymodbus.datastore as ds

class LinkedSlaveContext(ds.ModbusSlaveContext):
    def __init__(self, mirror, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mirror = mirror

    def setValues(self, fx, address, values, writeback=True):
        super().setValues(fx, address, values)
        if writeback:
            self.mirror.Writeback(fx, address, values)