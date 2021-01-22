import time
import click
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ConnectionException


def read(*point_addr_len_list, ip=None, port=None):
    client = ModbusClient(ip, port=port)
    client.connect()
    
    val_list = []
    for pt,addr,l in point_addr_len_list:
        if l > 1:
            l /= 2
            l = int(l)
    
        if pt == 'co':
            rr = client.read_coils(addr, l)
            val = rr.bits if not rr.isError() else 'err'
        elif pt == 'di':
            rr = client.read_discrete_inputs(addr, l)
            val = rr.bits if not rr.isError() else 'err'
        elif pt == 'hr':
            rr = client.read_holding_registers(addr, l)
            val = rr.registers if not rr.isError() else 'err'
        elif pt == 'ir':
            rr = client.read_input_registers(addr, l)
            val = rr.registers if not rr.isError() else 'err'
        
        if l == 1: val = val[0]
        val_list.append(val)

    client.close()
    return val_list

@click.command()
@click.argument('intval', nargs=1, type=float, default=1)
@click.argument('point', nargs=-1)
@click.option('--ip', type=str)
@click.option('--port', type=int, default=502)
def read_loop(point, intval, ip, port):
    pts = point[::2]
    addr_len_list = [addr_len for addr_len in point[1::2]]
    addrs = []
    len_list = []
    for al in addr_len_list:
        if ':' in al:
            a,l = al.split(':')
            addrs.append(int(a))
            len_list.append(int(l))
        else:
            addrs.append(int(al))
            len_list.append(1)

    while True:
        try:
            val_list = read(*zip(pts, addrs, len_list), ip=ip, port=port)
            info_str = ip + ''.join(f'[{pt}_{addr}] {val}'.ljust(15) for pt,addr,val in zip(pts, addrs, val_list))
            print(info_str)
            time.sleep(intval)
        except ConnectionException:
            print('connection loss...')
            time.sleep(30)

if __name__ == "__main__":
    read_loop()
