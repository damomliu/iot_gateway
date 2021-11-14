from controller import ModbusController
from logger import OneLogger

if __name__ == "__main__":
    LOGGER = OneLogger('CTRL', log_path='../log/ctrl.log', rotate=True)
    CTRL = ModbusController.FromConfigFile('../config/ctrl_config.json')
    CTRL.Start()
