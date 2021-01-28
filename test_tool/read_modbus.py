import time
import click
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.exceptions import ConnectionException

from modbus_types import PointType, DataType


def read(*point_addr_data_list, ip=None, port=None):
    client = ModbusClient(ip, port=port)
    client.connect()
    if not client.socket: return []*len(point_addr_data_list)
    
    val_list = []
    for pt,addr,data in point_addr_data_list:
        req,vals = pt.RequestValue(client, addr, count=data.length)
        if req:
            val_list.append(data.Decode(vals))
        else:
            print(vals)

    client.close()
    return val_list

@click.command()
@click.argument('intval', nargs=1, type=float, default=1)
@click.argument('point', nargs=-1)
@click.option('--ip', type=str, default='127.0.0.1')
@click.option('--port', type=int, default=502)
def read_loop(point, intval, ip, port):
    pts = [PointType(pt) for pt in point[::2]]
    addr_data_list = point[1::2]
    addrs = []
    data_list = []
    for i,al in enumerate(addr_data_list):
        if ':' in al:
            a,l = al.split(':')
            addrs.append(int(a))
            data_list.append(DataType(l, pts[i]))
        else:
            addrs.append(int(al))
            data_list.append(DataType('bool', pts[i]))

    while True:
        try:
            val_list = read(*zip(pts, addrs, data_list), ip=ip, port=port)
            info_str = f'{ip}:{port} ' + ' '.join(f'[{pt}_{addr}:{data.type_str}]{val}'.ljust(15) for pt,addr,data,val in zip(pts, addrs, data_list, val_list))
            print(info_str)
            time.sleep(intval)
        except ConnectionException:
            print('connection loss...', end='')
            time.sleep(50)
            print('retry')
        
        except Exception as e:
            print(e)
            break

if __name__ == "__main__":
    read_loop()
