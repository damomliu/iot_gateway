import struct

from .. import OperateResult, SoftBasic, StringResources
from ..BasicFramework import SoftIncrementCount
from ..Core import ReverseBytesTransform, ReverseWordTransform, NetworkDeviceBase
from .address import ModbusInfo
from .message import ModbusTcpMessage


class ModbusTcpNet(NetworkDeviceBase):
	'''Modbus-Tcp协议的客户端通讯类，方便的和服务器进行数据交互'''
	def __init__(self, ipAddress = '127.0.0.1', port = 502, station = 1):
		super().__init__()
		'''实例化一个MOdbus-Tcp协议的客户端对象'''
		self.WordLength = 1
		self.isAddressStartWithZero = True
		self.softIncrementCount = SoftIncrementCount( 65536, 0 )
		self.station = station
		self.ipAddress = ipAddress
		self.port = port
		self.byteTransform = ReverseWordTransform()
		self.iNetMessage = ModbusTcpMessage()
	def SetDataFormat( self, value ):
		'''多字节的数据是否高低位反转，该设置的改变会影响Int32,UInt32,float,double,Int64,UInt64类型的读写'''
		self.byteTransform.DataFormat = value
	def GetDataFormat( self ):
		'''多字节的数据是否高低位反转，该设置的改变会影响Int32,UInt32,float,double,Int64,UInt64类型的读写'''
		return self.byteTransform.DataFormat
	def SetIsStringReverse( self, value ):
		'''字符串数据是否按照字来反转'''
		self.byteTransform.IsStringReverse = value
	def GetIsStringReverse( self ):
		'''字符串数据是否按照字来反转'''
		return self.byteTransform.IsStringReverse
	def BuildReadCoilCommand(self, address, length):
		'''生成一个读取线圈的指令头'''
		# 分析地址
		analysis = ModbusInfo.AnalysisReadAddress( address, self.isAddressStartWithZero )
		if analysis.IsSuccess == False: return OperateResult.CreateFailedResult(analysis)
		# 获取消息号
		messageId = self.softIncrementCount.GetCurrentValue()
		#生成最终的指令
		buffer = ModbusInfo.PackCommandToTcp(analysis.Content.CreateReadCoils( self.station, length ), messageId)
		return OperateResult.CreateSuccessResult(buffer)
	def BuildReadDiscreteCommand(self, address, length):
		'''生成一个读取离散信息的指令头'''
		# 分析地址
		analysis = ModbusInfo.AnalysisReadAddress( address, self.isAddressStartWithZero )
		if analysis.IsSuccess == False: return OperateResult.CreateFailedResult(analysis)
		# 获取消息号
		messageId = self.softIncrementCount.GetCurrentValue()
		buffer = ModbusInfo.PackCommandToTcp(analysis.Content.CreateReadDiscrete(self.station,length), messageId)
		return OperateResult.CreateSuccessResult(buffer)
	def BuildReadRegisterCommand(self, address, length):
		'''创建一个读取寄存器的字节对象'''
		analysis = ModbusInfo.AnalysisReadAddress( address, self.isAddressStartWithZero )
		if analysis.IsSuccess == False: return OperateResult.CreateFailedResult(analysis)
		# 获取消息号
		messageId = self.softIncrementCount.GetCurrentValue()
		buffer = ModbusInfo.PackCommandToTcp(analysis.Content.CreateReadRegister(self.station,length), messageId)
		return OperateResult.CreateSuccessResult(buffer)
	def BuildReadInputRegisterCommand(self, address, length):
		'''创建一个读取寄存器的字节对象'''
		analysis = ModbusInfo.AnalysisReadAddress( address, self.isAddressStartWithZero )
		if analysis.IsSuccess == False: return OperateResult.CreateFailedResult(analysis)
		# 获取消息号
		messageId = self.softIncrementCount.GetCurrentValue()
		buffer = ModbusInfo.PackCommandToTcp(analysis.Content.CreateReadInputRegister(self.station,length), messageId)
		return OperateResult.CreateSuccessResult(buffer)
	def BuildWriteOneCoilCommand(self, address,value):
		'''生成一个写入单线圈的指令头'''
		analysis = ModbusInfo.AnalysisReadAddress( address, self.isAddressStartWithZero )
		if analysis.IsSuccess == False: return OperateResult.CreateFailedResult(analysis)
		# 获取消息号
		messageId = self.softIncrementCount.GetCurrentValue()
		buffer = ModbusInfo.PackCommandToTcp(analysis.Content.CreateWriteOneCoil(self.station,value), messageId)
		return OperateResult.CreateSuccessResult(buffer)
	def BuildWriteOneRegisterCommand(self, address, values):
		'''生成一个写入单个寄存器的报文'''
		analysis = ModbusInfo.AnalysisReadAddress( address, self.isAddressStartWithZero )
		if analysis.IsSuccess == False: return OperateResult.CreateFailedResult(analysis)
		# 获取消息号
		messageId = self.softIncrementCount.GetCurrentValue()
		buffer = ModbusInfo.PackCommandToTcp(analysis.Content.CreateWriteOneRegister(self.station,values), messageId)
		return OperateResult.CreateSuccessResult(buffer)
	def BuildWriteCoilCommand(self, address, values):
		'''生成批量写入单个线圈的报文信息，需要传入bool数组信息'''
		analysis = ModbusInfo.AnalysisReadAddress( address, self.isAddressStartWithZero )
		if analysis.IsSuccess == False: return OperateResult.CreateFailedResult(analysis)
		# 获取消息号
		messageId = self.softIncrementCount.GetCurrentValue()
		buffer = ModbusInfo.PackCommandToTcp(analysis.Content.CreateWriteCoil(self.station,values), messageId)
		return OperateResult.CreateSuccessResult(buffer)
	def BuildWriteRegisterCommand(self, address, values):
		'''生成批量写入寄存器的报文信息，需要传入byte数组'''
		analysis = ModbusInfo.AnalysisReadAddress( address, self.isAddressStartWithZero )
		if analysis.IsSuccess == False: return OperateResult.CreateFailedResult(analysis)
		# 获取消息号
		messageId = self.softIncrementCount.GetCurrentValue()
		buffer = ModbusInfo.PackCommandToTcp(analysis.Content.CreateWriteRegister(self.station,values), messageId)
		return OperateResult.CreateSuccessResult(buffer)
	def BuildReadModbusAddressCommand( self, address, length ):
		'''生成一个读取寄存器的指令头，address->ModbusAddress'''
		# 获取消息号
		messageId =  self.softIncrementCount.GetCurrentValue()
		# 生成最终tcp指令
		buffer = ModbusInfo.PackCommandToTcp( address.CreateReadRegister( self.station, length ), messageId )
		return OperateResult.CreateSuccessResult( buffer )
	def CheckModbusTcpResponse( self, send ):
		'''检查当前的Modbus-Tcp响应是否是正确的'''
		resultBytes = self.ReadFromCoreServer( send )
		if resultBytes.IsSuccess == True:
			if (send[7] + 0x80) == resultBytes.Content[7]:
				# 发生了错误
				resultBytes.IsSuccess = False
				resultBytes.Message = ModbusInfo.GetDescriptionByErrorCode( resultBytes.Content[8] )
				resultBytes.ErrorCode = resultBytes.Content[8]
		return resultBytes
	def ReadModBusBase( self, code, address, length ):
		'''检查当前的Modbus-Tcp响应是否是正确的'''
		command = None
		if code == ModbusInfo.ReadCoil():
			command = self.BuildReadCoilCommand( address, length )
		elif code == ModbusInfo.ReadDiscrete():
			command = self.BuildReadDiscreteCommand( address, length )
		elif code == ModbusInfo.ReadRegister():
			command = self.BuildReadRegisterCommand( address, length )
		elif code == ModbusInfo.ReadInputRegister():
			command = self.BuildReadInputRegisterCommand( address, length )
		else:
			command = OperateResult( msg = StringResources.Language.ModbusTcpFunctionCodeNotSupport )
		if command.IsSuccess == False : return OperateResult.CreateFailedResult( command )

		resultBytes = self.CheckModbusTcpResponse( command.Content )
		if resultBytes.IsSuccess == True:
			# 二次数据处理
			if len(resultBytes.Content) >= 9:
				buffer = bytearray(len(resultBytes.Content) - 9)
				buffer[0:len(buffer)] = resultBytes.Content[9:]
				resultBytes.Content = buffer
		return resultBytes
	def ReadModBusAddressBase( self, address, length = 1 ):
		'''读取服务器的数据，需要指定不同的功能码'''
		command = self.BuildReadModbusAddressCommand( address, length )
		if command.IsSuccess == False: return OperateResult.CreateFailedResult(command)

		resultBytes = self.CheckModbusTcpResponse( command.Content )
		if resultBytes.IsSuccess == True:
			# 二次数据处理
			if len(resultBytes.Content) >= 9:
				buffer = bytearray(len(resultBytes.Content) - 9)
				buffer[0:len(buffer)] = resultBytes.Content[9:]
				resultBytes.Content = buffer
		return resultBytes
	def ReadCoil( self, address, length = None):
		'''批量的读取线圈，需要指定起始地址，读取长度可选'''
		if length == None:
			read = self.ReadCoil( address, 1 )
			if read.IsSuccess == False : return OperateResult.CreateFailedResult( read )
			return OperateResult.CreateSuccessResult( read.Content[0] )
		else:
			read = self.ReadModBusBase( ModbusInfo.ReadCoil(), address, length )
			if read.IsSuccess == False : return OperateResult.CreateFailedResult( read )

			return OperateResult.CreateSuccessResult( SoftBasic.ByteToBoolArray( read.Content, length ) )
	def ReadDiscrete( self, address, length = None):
		'''批量的读取输入点，需要指定起始地址，可选读取长度'''
		if length == None:
			read = self.ReadDiscrete( address, 1 )
			if read.IsSuccess == False : return OperateResult.CreateFailedResult( read )
			return OperateResult.CreateSuccessResult( read.Content[0] )
		else:
			read = self.ReadModBusBase( ModbusInfo.ReadDiscrete(), address, length )
			if read.IsSuccess == False : return OperateResult.CreateFailedResult( read )
			
			return OperateResult.CreateSuccessResult( SoftBasic.ByteToBoolArray( read.Content, length ) )
	def Read( self, address, length ):
		'''从Modbus服务器批量读取寄存器的信息，需要指定起始地址，读取长度'''
		analysis = ModbusInfo.AnalysisReadAddress( address, self.isAddressStartWithZero )
		if analysis.IsSuccess == False : return OperateResult.CreateFailedResult( analysis )
		return self.ReadModBusAddressBase( analysis.Content, length )
	def WriteOneRegister( self, address, value ):
		'''写一个寄存器数据'''
		if type(value) == list:
			command = self.BuildWriteOneRegisterCommand( address, value )
			if command.IsSuccess == False : return command
			return self.CheckModbusTcpResponse( command.Content )
		else:
			return self.WriteOneRegister(address, struct.pack('>H', value))
	def Write( self, address, value ):
		'''将数据写入到Modbus的寄存器上去，需要指定起始地址和数据内容'''
		command = self.BuildWriteRegisterCommand( address, value )
		if command.IsSuccess == False:
			return command

		return self.CheckModbusTcpResponse( command.Content )
	def WriteCoil( self, address, value ):
		'''批量写线圈信息，指定是否通断'''
		if type(value) == list:
			command = self.BuildWriteCoilCommand( address, value )
			if command.IsSuccess == False : return command
			return self.CheckModbusTcpResponse( command.Content )
		else:
			command = self.BuildWriteOneCoilCommand( address, value )
			if command.IsSuccess == False : return command
			return self.CheckModbusTcpResponse( command.Content )
	def WriteBool( self, address, values ):
		'''批量写寄存器的数据内容'''
		return self.Write( address, SoftBasic.BoolArrayToByte( values ) )
