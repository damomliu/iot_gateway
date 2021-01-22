import time
import random
import click
from pymodbus.client.sync import ModbusTcpClient as ModbusClient


def write(*point_addr_value_list):
    client = ModbusClient('192.168.4.150', port=502)
    client.connect()
    
    for pt,addr,val in point_addr_value_list:
        if pt == 'co':
            client.write_coil(addr, bool(val))
        elif pt == 'hr':
            client.write_register(addr, val)

    client.close()

@click.command()
@click.argument('point')
@click.argument('addr', type=int)
@click.argument('btm', type=int, default=0)
@click.argument('top', type=int, default=1)
@click.argument('intval', type=float, default=1)
def random_loop(point, addr, btm, top, intval):
    while True:
        newval = random.randint(btm, top)
        write((point, addr, newval))
        time.sleep(intval)

if __name__ == "__main__":
    random_loop()
