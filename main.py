from controller import ModbusController
from logger import OneLogger


LOG_PATH = '../log/ctrl.log'
CONFIG_PATH = '../config/ctrl_config.json'
# CONFIG_PATH = 'test.db'

if __name__ == "__main__":
    LOGGER = OneLogger('CTRL', log_path=LOG_PATH, rotate=True)
    LOGGER.info(f'===== Starting ModbusController {ModbusController.__version__} =====')

    CTRL = ModbusController.from_config(CONFIG_PATH, logger=LOGGER)
    CTRL.verbose = True
    CTRL.Start()
