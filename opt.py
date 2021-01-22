from logger import OneLogger

POINT_TYPE = {
    'co': dict(fx=1, desc='Coil'),
    'di': dict(fx=2, desc='Discrete Input'),
    'hr': dict(fx=3, desc='Holding Register'),
    'ir': dict(fx=4, desc='Input Register')
}

class PROJECT:
    name = 'Modbus Controller'
    vendor = 'CYAN Intelligent'

class DEFAULT:
    SOURCE_SLAVE_ID = 0x00
