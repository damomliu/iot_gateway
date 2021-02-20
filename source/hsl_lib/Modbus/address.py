import struct

from .. import OperateResult, SoftBasic, StringResources
from ..Core import DeviceAddressBase


class ModbusInfo:
	'''Modbus协议相关的一些信息'''
	@staticmethod
	def ReadCoil():
		'''读取线圈功能码'''
		return 0x01
	@staticmethod
	def ReadDiscrete():
		'''读取寄存器功能码'''
		return 0x02
	@staticmethod
	def ReadRegister():
		'''读取寄存器功能码'''
		return 0x03
	@staticmethod
	def ReadInputRegister():
		'''读取输入寄存器'''
		return 0x04
	@staticmethod
	def WriteOneCoil():
		'''写单个寄存器'''
		return 0x05
	@staticmethod
	def WriteOneRegister():
		'''写单个寄存器'''
		return 0x06
	@staticmethod
	def WriteCoil():
		'''写多个线圈'''
		return 0x0F
	@staticmethod
	def WriteRegister():
		'''写多个寄存器'''
		return 0x10
	@staticmethod
	def FunctionCodeNotSupport():
		'''不支持该功能码'''
		return 0x01
	@staticmethod
	def FunctionCodeOverBound():
		'''该地址越界'''
		return 0x02
	@staticmethod
	def FunctionCodeQuantityOver():
		'''读取长度超过最大值'''
		return 0x03
	@staticmethod
	def FunctionCodeReadWriteException():
		'''读写异常'''
		return 0x04
	@staticmethod
	def PackCommandToTcp( value, id ):
		'''将modbus指令打包成Modbus-Tcp指令'''
		buffer = bytearray( len(value) + 6)
		buffer[0:2] = struct.pack('>H',id)
		buffer[4:6] = struct.pack('>H',len(value))
		buffer[6:len(buffer)] = value
		return buffer
	@staticmethod
	def GetDescriptionByErrorCode( code ):
		'''通过错误码来获取到对应的文本消息'''
		if code == 0x01: return StringResources.Language.ModbusTcpFunctionCodeNotSupport
		elif code == 0x02: return StringResources.Language.ModbusTcpFunctionCodeOverBound
		elif code == 0x03: return StringResources.Language.ModbusTcpFunctionCodeQuantityOver
		elif code == 0x04: return StringResources.Language.ModbusTcpFunctionCodeReadWriteException
		else: return StringResources.Language.UnknownError
	@staticmethod
	def AnalysisReadAddress( address, isStartWithZero ):
		'''分析Modbus协议的地址信息，该地址适应于tcp及rtu模式'''
		try:
			mAddress = ModbusAddress(address)
			if isStartWithZero == False:
				if mAddress.Address < 1:
					raise RuntimeError(StringResources.Language.ModbusAddressMustMoreThanOne)
				else:
					mAddress.Address = mAddress.Address - 1
			return OperateResult.CreateSuccessResult(mAddress)
		except Exception as ex:
			return OperateResult( msg = str(ex))

class ModbusAddress(DeviceAddressBase):
	'''Modbus协议的地址类'''
	Station = 0
	Function = ModbusInfo.ReadRegister()
	def __init__(self, address = "0"):
		self.Station = -1
		self.Function = ModbusInfo.ReadRegister()
		self.Address = 0
		self.AnalysisAddress(address)

	def AnalysisAddress( self, address = "0" ):
		'''解析Modbus的地址码'''
		if address.find(';')>=0:
			listAddress = address.split(";")
			for index in range(len(listAddress)):
				if listAddress[index][0] == 's' or listAddress[index][0] == 'S':
					self.Station = int(listAddress[index][2:])
				elif listAddress[index][0] == 'x' or listAddress[index][0] == 'X':
					self.Function = int(listAddress[index][2:])
				else:
					self.Address = int(listAddress[index])
		else:
			self.Address = int(address)
	
	def CreateReadCoils( self, station, length ):
		'''创建一个读取线圈的字节对象'''
		buffer = bytearray(6)
		if self.Station < 0 :
			buffer[0] = station
		else:
			buffer[0] = self.Station
		buffer[1] = ModbusInfo.ReadCoil()
		buffer[2:4] = struct.pack('>H', self.Address)
		buffer[4:6] = struct.pack('>H', length)
		return buffer
	def CreateReadDiscrete( self, station, length ):
		'''创建一个读取离散输入的字节对象'''
		buffer = bytearray(6)
		if self.Station < 0 :
			buffer[0] = station
		else:
			buffer[0] = self.Station
		buffer[1] = ModbusInfo.ReadDiscrete()
		buffer[2:4] = struct.pack('>H', self.Address)
		buffer[4:6] = struct.pack('>H', length)
		return buffer
	def CreateReadRegister( self, station, length ):
		'''创建一个读取寄存器的字节对象'''
		buffer = bytearray(6)
		if self.Station < 0 :
			buffer[0] = station
		else:
			buffer[0] = self.Station
		buffer[1] = self.Function
		buffer[2:4] = struct.pack('>H', self.Address)
		buffer[4:6] = struct.pack('>H', length)
		return buffer
	def CreateReadInputRegister( self, station, length ):
		'''创建一个读取寄存器的字节对象'''
		buffer = bytearray(6)
		if self.Station < 0 :
			buffer[0] = station
		else:
			buffer[0] = self.Station
		buffer[1] = ModbusInfo.ReadInputRegister()
		buffer[2:4] = struct.pack('>H', self.Address)
		buffer[4:6] = struct.pack('>H', length)
		return buffer
	def CreateWriteOneCoil(self, station, value):
		'''创建一个写入单个线圈的指令'''
		buffer = bytearray(6)
		if self.Station < 0 :
			buffer[0] = station
		else:
			buffer[0] = self.Station
		buffer[1] = ModbusInfo.WriteOneCoil()
		buffer[2:4] = struct.pack('>H', self.Address)
		if value == True:
			buffer[4] = 0xFF
		return buffer
	def CreateWriteOneRegister(self, station, values):
		'''创建一个写入单个寄存器的指令'''
		buffer = bytearray(6)
		if self.Station < 0 :
			buffer[0] = station
		else:
			buffer[0] = self.Station
		buffer[1] = ModbusInfo.WriteOneRegister()
		buffer[2:4] = struct.pack('>H', self.Address)
		buffer[4:6] = values
		return buffer
	def CreateWriteCoil(self, station, values):
		'''创建一个写入批量线圈的指令'''
		data = SoftBasic.BoolArrayToByte( values )
		buffer = bytearray(7 + len(data))
		if self.Station < 0 :
			buffer[0] = station
		else:
			buffer[0] = self.Station
		buffer[1] = ModbusInfo.WriteCoil()
		buffer[2:4] = struct.pack('>H', self.Address)
		buffer[4:6] = struct.pack('>H', len(values))
		buffer[6] = len(data)
		buffer[7:len(buffer)] = data
		return buffer
	def CreateWriteRegister(self, station, values):
		'''创建一个写入批量寄存器的指令'''
		buffer = bytearray(7 + len(values))
		if self.Station < 0 :
			buffer[0] = station
		else:
			buffer[0] = self.Station
		buffer[1] = ModbusInfo.WriteRegister()
		buffer[2:4] = struct.pack('>H', self.Address)
		buffer[4:6] = struct.pack('>H', len(values)//2)
		buffer[6] = len(values)
		buffer[7:len(buffer)] = values
		return buffer
	def AddressAdd(self, value):
		'''地址新增指定的数'''
		modbusAddress = ModbusAddress()
		modbusAddress.Station = self.Station
		modbusAddress.Function = self.Function
		modbusAddress.Address = self.Address+value
		return modbusAddress
