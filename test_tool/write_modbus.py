import time
import random
import click
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from source import PointType, DataType


def write(*point_addr_value_list, ip='127.0.0.1', port=502):
    client = ModbusClient(ip, port=port)
    client.connect()
    
    for pt,addr,val,dt in point_addr_value_list:
        pt = PointType(pt)
        if dt.startswith('int'):
            val = int(val)
        elif dt.startswith('float'):
            val = float(val)
        elif dt.startswith('bool'):
            val = int(val) != 0
        
        dt = DataType(dt)
        writeFunc = pt._WriteFunc(client)
        req = writeFunc(addr, dt.Encode(val))
        print(not req.isError())
        print(req)

    client.close()

@click.command()
@click.argument('point')
@click.argument('addr', type=int)
@click.argument('val')
@click.argument('datatype', type=str, default='float32')
@click.option('--ip', type=str, default='127.0.0.1')
@click.option('--port', type=int, default=502)
def random_loop(point, addr, val, datatype, ip, port):
    write((point, addr, val, datatype), ip=ip, port=port)

if __name__ == "__main__":
    random_loop()
