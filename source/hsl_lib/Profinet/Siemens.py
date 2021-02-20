from enum import Enum

from .. import OperateResult, StringResources, SoftBasic
from ..Core import (
    RegularByteTransform, ReverseBytesTransform, ReverseWordTransform, ByteTransformHelper,
    NetworkDeviceBase,
    INetMessage
)

__all__ = [
	'S7Message',
	'SiemensS7Net', 'SiemensPLCS', 'SiemensFetchWriteNet',
]

class SiemensPLCS(Enum):
	'''西门子PLC的类型对象'''
	S1200 = 0
	S300 = 1
	S400 = 2
	S1500 = 3
	S200Smart = 4

class SiemensS7Net(NetworkDeviceBase):
	'''一个西门子的客户端类，使用S7协议来进行数据交互，支持s200smart，s300，s400，s1200，s1500的通讯
	
	在实例化的时候除了需要指定PLC型号，ip地址之外，有些特殊的plc是需要设置机架号和槽号的，示例的示例如下：

	siemens = SiemensS7Net(SiemensPLCS.S1200, "192.168.8.13")

	siemens.SetSlotAndRack(0, 2)  # 这行代码不是必须的，S400系列时需要根据实际来进行设置，才能正确的读到数据
	'''
	def __init__(self, siemens, ipAddress = "127.0.0.1"):
		super().__init__()
		'''实例化一个西门子的S7协议的通讯对象并指定Ip地址'''
		self.CurrentPlc = SiemensPLCS.S1200
		self.plcHead1 = bytearray([0x03,0x00,0x00,0x16,0x11,0xE0,0x00,0x00,0x00,0x01,0x00,0xC0,0x01,0x0A,0xC1,0x02,0x01,0x02,0xC2,0x02,0x01,0x00])
		self.plcHead2 = bytearray([0x03,0x00,0x00,0x19,0x02,0xF0,0x80,0x32,0x01,0x00,0x00,0x04,0x00,0x00,0x08,0x00,0x00,0xF0,0x00,0x00,0x01,0x00,0x01,0x01,0xE0])
		self.plcOrderNumber = bytearray([0x03,0x00,0x00,0x21,0x02,0xF0,0x80,0x32,0x07,0x00,0x00,0x00,0x01,0x00,0x08,0x00,0x08,0x00,0x01,0x12,0x04,0x11,0x44,0x01,0x00,0xFF,0x09,0x00,0x04,0x00,0x11,0x00,0x00])
		self.plcHead1_200smart = bytearray([0x03,0x00,0x00,0x16,0x11,0xE0,0x00,0x00,0x00,0x01,0x00,0xC1,0x02,0x10,0x00,0xC2,0x02,0x03,0x00,0xC0,0x01,0x0A])
		self.plcHead2_200smart = bytearray([0x03,0x00,0x00,0x19,0x02,0xF0,0x80,0x32,0x01,0x00,0x00,0xCC,0xC1,0x00,0x08,0x00,0x00,0xF0,0x00,0x00,0x01,0x00,0x01,0x03,0xC0])
		self.WordLength = 2
		self.ipAddress = ipAddress
		self.port = 102
		self.CurrentPlc = siemens
		self.iNetMessage = S7Message()
		self.byteTransform = ReverseBytesTransform()

		if siemens == SiemensPLCS.S1200:
			self.plcHead1[21] = 0
		elif siemens == SiemensPLCS.S300:
			self.plcHead1[21] = 2
		elif siemens == SiemensPLCS.S400:
			self.plcHead1[21] = 3
			self.plcHead1[17] = 0x00
		elif siemens == SiemensPLCS.S1500:
			self.plcHead1[21] = 0
		elif siemens == SiemensPLCS.S200Smart:
			self.plcHead1 = self.plcHead1_200smart
			self.plcHead2 = self.plcHead2_200smart
		else:
			self.plcHead1[18] = 0
	@staticmethod
	def CalculateAddressStarted( address = "M0" ):
		'''计算特殊的地址信息'''
		if address.find('.') >= 0:
			temp = address.split(".")
			return int(temp[0]) * 8 + int(temp[1])
		else:
			return int( address ) * 8
	@staticmethod
	def AnalysisAddress( address = 'M0' ):
		'''解析数据地址，解析出地址类型，起始地址，DB块的地址'''
		result = OperateResult( )
		try:
			result.Content3 = 0
			if address[0] == 'I':
				result.Content1 = 0x81
				result.Content2 = SiemensS7Net.CalculateAddressStarted( address[1:] )
			elif address[0] == 'Q':
				result.Content1 = 0x82
				result.Content2 = SiemensS7Net.CalculateAddressStarted( address[1:] )
			elif address[0] == 'M':
				result.Content1 = 0x83
				result.Content2 = SiemensS7Net.CalculateAddressStarted( address[1:] )
			elif address[0] == 'D' or address[0:2] == "DB":
				result.Content1 = 0x84
				adds = address.split(".")
				if address[1] == 'B':
					result.Content3 = int( adds[0][2:] )
				else:
					result.Content3 = int( adds[0][1:] )
				result.Content2 = SiemensS7Net.CalculateAddressStarted( address[ (address.find( '.' ) + 1):]) 
			elif address[0] == 'T':
				result.Content1 = 0x1D
				result.Content2 = SiemensS7Net.CalculateAddressStarted( address[1:] )
			elif address[0] == 'C':
				result.Content1 = 0x1C
				result.Content2 = SiemensS7Net.CalculateAddressStarted( address[1:] )
			elif address[0] == 'V':
				result.Content1 = 0x84
				result.Content3 = 1
				result.Content2 = SiemensS7Net.CalculateAddressStarted( address[1:] )
			else:
				result.Message = StringResources.Language.NotSupportedDataType
				result.Content1 = 0
				result.Content2 = 0
				result.Content3 = 0
				return result
		except Exception as ex:
			result.Message = str(ex)
			return result

		result.IsSuccess = True
		return result
	@staticmethod
	def BuildReadCommand( address, length ):
		'''生成一个读取字数据指令头的通用方法'''
		if address == None : raise Exception( "address" )
		if length == None : raise Exception( "count" )
		if len(address) != len(length) : raise Exception( "两个参数的个数不统一" )
		if len(length) > 19 : raise Exception( "读取的数组数量不允许大于19" )

		readCount = len(length)
		_PLCCommand = bytearray(19 + readCount * 12)
		# ======================================================================================
		_PLCCommand[0] = 0x03                                                # 报文头
		_PLCCommand[1] = 0x00
		_PLCCommand[2] = len(_PLCCommand) // 256                           # 长度
		_PLCCommand[3] = len(_PLCCommand) % 256
		_PLCCommand[4] = 0x02                                                # 固定
		_PLCCommand[5] = 0xF0
		_PLCCommand[6] = 0x80
		_PLCCommand[7] = 0x32                                                # 协议标识
		_PLCCommand[8] = 0x01                                                # 命令：发
		_PLCCommand[9] = 0x00                                                # redundancy identification (reserved): 0x0000;
		_PLCCommand[10] = 0x00                                               # protocol data unit reference; it’s increased by request event;
		_PLCCommand[11] = 0x00
		_PLCCommand[12] = 0x01                                               # 参数命令数据总长度
		_PLCCommand[13] = (len(_PLCCommand) - 17) // 256
		_PLCCommand[14] = (len(_PLCCommand) - 17) % 256
		_PLCCommand[15] = 0x00                                               # 读取内部数据时为00，读取CPU型号为Data数据长度
		_PLCCommand[16] = 0x00
		# =====================================================================================
		_PLCCommand[17] = 0x04                                               # 读写指令，04读，05写
		_PLCCommand[18] = readCount                                    # 读取数据块个数

		for ii in range(readCount):
			#===========================================================================================
			# 指定有效值类型
			_PLCCommand[19 + ii * 12] = 0x12
			# 接下来本次地址访问长度
			_PLCCommand[20 + ii * 12] = 0x0A
			# 语法标记，ANY
			_PLCCommand[21 + ii * 12] = 0x10
			# 按字为单位
			_PLCCommand[22 + ii * 12] = 0x02
			# 访问数据的个数
			_PLCCommand[23 + ii * 12] = length[ii] // 256
			_PLCCommand[24 + ii * 12] = length[ii] % 256
			# DB块编号，如果访问的是DB块的话
			_PLCCommand[25 + ii * 12] = address[ii].Content3 // 256
			_PLCCommand[26 + ii * 12] = address[ii].Content3 % 256
			# 访问数据类型
			_PLCCommand[27 + ii * 12] = address[ii].Content1
			# 偏移位置
			_PLCCommand[28 + ii * 12] = address[ii].Content2 // 256 // 256 % 256
			_PLCCommand[29 + ii * 12] = address[ii].Content2 // 256 % 256
			_PLCCommand[30 + ii * 12] = address[ii].Content2 % 256

		return OperateResult.CreateSuccessResult( _PLCCommand )
	@staticmethod
	def BuildBitReadCommand( address ):
		'''生成一个位读取数据指令头的通用方法'''
		analysis = SiemensS7Net.AnalysisAddress( address )
		if analysis.IsSuccess == False : return OperateResult.CreateFailedResult( analysis )

		_PLCCommand = bytearray(31)
		# 报文头
		_PLCCommand[0] = 0x03
		_PLCCommand[1] = 0x00
		# 长度
		_PLCCommand[2] = len(_PLCCommand) // 256
		_PLCCommand[3] = len(_PLCCommand) % 256
		# 固定
		_PLCCommand[4] = 0x02
		_PLCCommand[5] = 0xF0
		_PLCCommand[6] = 0x80
		_PLCCommand[7] = 0x32
		# 命令：发
		_PLCCommand[8] = 0x01
		# 标识序列号
		_PLCCommand[9] = 0x00
		_PLCCommand[10] = 0x00
		_PLCCommand[11] = 0x00
		_PLCCommand[12] = 0x01
		# 命令数据总长度
		_PLCCommand[13] = (len(_PLCCommand) - 17) // 256
		_PLCCommand[14] = (len(_PLCCommand) - 17) % 256

		_PLCCommand[15] = 0x00
		_PLCCommand[16] = 0x00

		# 命令起始符
		_PLCCommand[17] = 0x04
		# 读取数据块个数
		_PLCCommand[18] = 0x01

		#===========================================================================================
		# 读取地址的前缀
		_PLCCommand[19] = 0x12
		_PLCCommand[20] = 0x0A
		_PLCCommand[21] = 0x10
		# 读取的数据时位
		_PLCCommand[22] = 0x01
		# 访问数据的个数
		_PLCCommand[23] = 0x00
		_PLCCommand[24] = 0x01
		# DB块编号，如果访问的是DB块的话
		_PLCCommand[25] = analysis.Content3 // 256
		_PLCCommand[26] = analysis.Content3 % 256
		# 访问数据类型
		_PLCCommand[27] = analysis.Content1
		# 偏移位置
		_PLCCommand[28] = analysis.Content2 // 256 // 256 % 256
		_PLCCommand[29] = analysis.Content2 // 256 % 256
		_PLCCommand[30] = analysis.Content2 % 256

		return OperateResult.CreateSuccessResult( _PLCCommand )
	@staticmethod
	def BuildWriteByteCommand( address, data ):
		'''生成一个写入字节数据的指令'''
		if data == None : data = bytearray(0)
		analysis = SiemensS7Net.AnalysisAddress( address )
		if analysis.IsSuccess == False : return OperateResult.CreateFailedResult(analysis)

		_PLCCommand = bytearray(35 + len(data))
		_PLCCommand[0] = 0x03
		_PLCCommand[1] = 0x00
		# 长度
		_PLCCommand[2] = (35 + len(data)) // 256
		_PLCCommand[3] = (35 + len(data)) % 256
		# 固定
		_PLCCommand[4] = 0x02
		_PLCCommand[5] = 0xF0
		_PLCCommand[6] = 0x80
		_PLCCommand[7] = 0x32
		# 命令 发
		_PLCCommand[8] = 0x01
		# 标识序列号
		_PLCCommand[9] = 0x00
		_PLCCommand[10] = 0x00
		_PLCCommand[11] = 0x00
		_PLCCommand[12] = 0x01
		# 固定
		_PLCCommand[13] = 0x00
		_PLCCommand[14] = 0x0E
		# 写入长度+4
		_PLCCommand[15] = (4 + len(data)) // 256
		_PLCCommand[16] = (4 + len(data)) % 256
		# 读写指令
		_PLCCommand[17] = 0x05
		# 写入数据块个数
		_PLCCommand[18] = 0x01
		# 固定，返回数据长度
		_PLCCommand[19] = 0x12
		_PLCCommand[20] = 0x0A
		_PLCCommand[21] = 0x10
		# 写入方式，1是按位，2是按字
		_PLCCommand[22] = 0x02
		# 写入数据的个数
		_PLCCommand[23] = len(data) // 256
		_PLCCommand[24] = len(data) % 256
		# DB块编号，如果访问的是DB块的话
		_PLCCommand[25] = analysis.Content3 // 256
		_PLCCommand[26] = analysis.Content3 % 256
		# 写入数据的类型
		_PLCCommand[27] = analysis.Content1
		# 偏移位置
		_PLCCommand[28] = analysis.Content2 // 256 // 256 % 256
		_PLCCommand[29] = analysis.Content2 // 256 % 256
		_PLCCommand[30] = analysis.Content2 % 256
		# 按字写入
		_PLCCommand[31] = 0x00
		_PLCCommand[32] = 0x04
		# 按位计算的长度
		_PLCCommand[33] = len(data) * 8 // 256
		_PLCCommand[34] = len(data) * 8 % 256

		_PLCCommand[35:] = data

		return OperateResult.CreateSuccessResult(_PLCCommand)
	@staticmethod
	def BuildWriteBitCommand( address, data ):
		analysis = SiemensS7Net.AnalysisAddress( address )
		if analysis.IsSuccess == False : return OperateResult.CreateFailedResult(analysis)

		buffer = bytearray(1)
		if data == True : buffer[0] = 0x01

		_PLCCommand = bytearray(35 + len(buffer))
		_PLCCommand[0] = 0x03
		_PLCCommand[1] = 0x00
		# 长度
		_PLCCommand[2] = (35 + len(buffer)) // 256
		_PLCCommand[3] = (35 + len(buffer)) % 256
		# 固定
		_PLCCommand[4] = 0x02
		_PLCCommand[5] = 0xF0
		_PLCCommand[6] = 0x80
		_PLCCommand[7] = 0x32
		# 命令 发
		_PLCCommand[8] = 0x01
		# 标识序列号
		_PLCCommand[9] = 0x00
		_PLCCommand[10] = 0x00
		_PLCCommand[11] = 0x00
		_PLCCommand[12] = 0x01
		# 固定
		_PLCCommand[13] = 0x00
		_PLCCommand[14] = 0x0E
		# 写入长度+4
		_PLCCommand[15] = (4 + len(buffer)) // 256
		_PLCCommand[16] = (4 + len(buffer)) % 256
		# 命令起始符
		_PLCCommand[17] = 0x05
		# 写入数据块个数
		_PLCCommand[18] = 0x01
		_PLCCommand[19] = 0x12
		_PLCCommand[20] = 0x0A
		_PLCCommand[21] = 0x10
		# 写入方式，1是按位，2是按字
		_PLCCommand[22] = 0x01
		# 写入数据的个数
		_PLCCommand[23] = len(buffer) // 256
		_PLCCommand[24] = len(buffer) % 256
		# DB块编号，如果访问的是DB块的话
		_PLCCommand[25] = analysis.Content3 // 256
		_PLCCommand[26] = analysis.Content3 % 256
		# 写入数据的类型
		_PLCCommand[27] = analysis.Content1
		# 偏移位置
		_PLCCommand[28] = analysis.Content2 // 256 // 256
		_PLCCommand[29] = analysis.Content2 // 256
		_PLCCommand[30] = analysis.Content2 % 256
		# 按位写入
		_PLCCommand[31] = 0x00
		_PLCCommand[32] = 0x03
		# 按位计算的长度
		_PLCCommand[33] = len(buffer) // 256
		_PLCCommand[34] = len(buffer) % 256

		_PLCCommand[35:] = buffer

		return OperateResult.CreateSuccessResult(_PLCCommand)
	def SetSlotAndRack(self, rack, slot):
		'''设置西门字的机架号和槽号的信息，当和400PLC通信时就需要动态来调整'''
		self.plcHead1[21] = (rack * 0x20) + slot
	def InitializationOnConnect( self, socket ):
		'''连接上服务器后需要进行的二次握手操作'''
		# msg = SoftBasic.ByteToHexString(self.plcHead1, ' ')
		# 第一次握手
		read_first = self.ReadFromCoreServerBase( socket, self.plcHead1 )
		if read_first.IsSuccess == False : return read_first

		# 第二次握手
		read_second = self.ReadFromCoreServerBase( socket, self.plcHead2 )
		if read_second.IsSuccess == False : return read_second

		# 返回成功的信号
		return OperateResult.CreateSuccessResult( )
	def ReadOrderNumber( self ):
		'''从PLC读取订货号信息'''
		read = self.ReadFromCoreServer( self.plcOrderNumber )
		if read.IsSuccess == False : return OperateResult.CreateFailedResult( read )

		return OperateResult.CreateSuccessResult( read.Content[71:92].decode('ascii') )
	def __ReadBase( self, address, length ):
		'''基础的读取方法，外界不应该调用本方法'''
		command = SiemensS7Net.BuildReadCommand( address, length )
		if command.IsSuccess == False : return command

		read = self.ReadFromCoreServer( command.Content )
		if read.IsSuccess == False : return read

		# 分析结果
		receiveCount = 0
		for i in range(len(length)):
			receiveCount += length[i]

		if len(read.Content) >= 21 and read.Content[20] == len(length) :
			buffer = bytearray(receiveCount)
			kk = 0
			ll = 0
			ii = 21
			while ii < len(read.Content):
				if ii + 1 < len(read.Content):
					if read.Content[ii] == 0xFF and read.Content[ii + 1] == 0x04:
						# 有数据
						buffer[ll : ll + length[kk]] = read.Content[ii+4 : ii+4+length[kk]]
						ii += length[kk] + 3
						ll += length[kk]
						kk += 1
				ii += 1
			return OperateResult.CreateSuccessResult( buffer )
		else :
			result = OperateResult()
			result.ErrorCode = read.ErrorCode
			result.Message = StringResources.Language.SiemensDataLengthCheckFailed
			return result
	
	def Read( self, address, length ):
		'''从PLC读取数据，地址格式为I100，Q100，DB20.100，M100，T100，C100以字节为单位'''
		if type(address) == list and type(length) == list:
			addressResult = []
			for i in range(length):
				tmp = SiemensS7Net.AnalysisAddress( address[i] )
				if tmp.IsSuccess == False : return OperateResult.CreateFailedResult( addressResult[i] )

				addressResult.append( tmp )
			return self.__ReadBase( addressResult, length )
		else:
			addressResult = SiemensS7Net.AnalysisAddress( address )
			if addressResult.IsSuccess == False : return OperateResult.CreateFailedResult( addressResult )

			bytesContent = bytearray()
			alreadyFinished = 0
			while alreadyFinished < length :
				readLength = min( length - alreadyFinished, 200 )
				read = self.__ReadBase( [ addressResult ], [ readLength ] )
				if read.IsSuccess == True :
					bytesContent.extend( read.Content )
				else:
					return read

				alreadyFinished += readLength
				addressResult.Content2 += readLength * 8

			return OperateResult.CreateSuccessResult( bytesContent )
	def __ReadBitFromPLC( self, address ):
		'''从PLC读取数据，地址格式为I100，Q100，DB20.100，M100，以位为单位'''
		# 指令生成
		command = SiemensS7Net.BuildBitReadCommand( address )
		if command.IsSuccess == False : return OperateResult.CreateFailedResult( command )

		# 核心交互
		read = self.ReadFromCoreServer( command.Content )
		if read.IsSuccess == False : return read

		# 分析结果
		receiveCount = 1
		if len(read.Content) >= 21 and read.Content[20] == 1 :
			buffer = bytearray(receiveCount)
			if 22 < len(read.Content) :
				if read.Content[21] == 0xFF and read.Content[22] == 0x03:
					# 有数据
					buffer[0] = read.Content[25]
			return OperateResult.CreateSuccessResult( buffer )
		else:
			result = OperateResult()
			result.ErrorCode = read.ErrorCode
			result.Message = StringResources.Language.SiemensDataLengthCheckFailed
			return result
	def ReadBool( self, address ):
		'''读取指定地址的bool数据'''
		return ByteTransformHelper.GetResultFromBytes( self.__ReadBitFromPLC( address ), lambda m: self.byteTransform.TransBool( m, 0 ) )
	def ReadByte( self, address ):
		'''读取指定地址的byte数据'''
		return ByteTransformHelper.GetResultFromArray( self.Read( address, 1 ) )
	def __WriteBase( self, entireValue ):
		'''基础的写入数据的操作支持'''
		write = self.ReadFromCoreServer( entireValue )
		if write.IsSuccess == False : return write

		if write.Content[len(write.Content) - 1] != 0xFF :
			# 写入异常
			return OperateResult( msg = "写入数据异常", err = write.Content[write.Content.Length - 1])
		else:
			return OperateResult.CreateSuccessResult( )
	def Write( self, address, value ):
		'''将数据写入到PLC数据，地址格式为I100，Q100，DB20.100，M100，以字节为单位'''
		command = self.BuildWriteByteCommand( address, value )
		if command.IsSuccess == False : return command

		return self.__WriteBase( command.Content )
	def WriteBool( self, address, value ):
		'''写入PLC的一个位，例如"M100.6"，"I100.7"，"Q100.0"，"DB20.100.0"，如果只写了"M100"默认为"M100.0'''
		# 生成指令
		command = SiemensS7Net.BuildWriteBitCommand( address, value )
		if command.IsSuccess == False : return command

		return self.__WriteBase( command.Content )
	def WriteByte( self, address, value ):
		'''向PLC中写入byte数据，返回值说明'''
		return self.Write( address, [value] )

class SiemensFetchWriteNet(NetworkDeviceBase):
	'''使用了Fetch/Write协议来和西门子进行通讯，该种方法需要在PLC侧进行一些配置'''
	def __init__( self, ipAddress = '127.0.0.1', port = 1000 ):
		''' 实例化一个西门子的Fetch/Write协议的通讯对象，可以指定ip地址及端口号'''
		super().__init__()
		self.ipAddress = ipAddress
		self.port = port
		self.WordLength = 2
	@staticmethod
	def CalculateAddressStarted( address = "M100" ):
		'''计算特殊的地址信息'''
		if address.find( '.' ) < 0:
			return int( address )
		else:
			temp = address.split( '.' )
			return int( temp[0] )
	@staticmethod
	def AnalysisAddress( address = "M100" ):
		'''解析数据地址，解析出地址类型，起始地址，DB块的地址'''
		result = OperateResult( )
		try:
			result.Content3 = 0
			if address[0] == 'I':
				result.Content1 = 0x03
				result.Content2 = SiemensFetchWriteNet.CalculateAddressStarted( address[1:] )
			elif address[0] == 'Q':
				result.Content1 = 0x04
				result.Content2 = SiemensFetchWriteNet.CalculateAddressStarted( address[1:] )
			elif address[0] == 'M':
				result.Content1 = 0x02
				result.Content2 = SiemensFetchWriteNet.CalculateAddressStarted( address[1:] )
			elif address[0] == 'D' or address.startswith("DB"):
				result.Content1 = 0x01
				adds = address.split( '.' )
				if address[1] == 'B':
					result.Content3 = int( adds[0][2:] )
				else:
					result.Content3 = int( adds[0][1:] )

				if result.Content3 > 255:
					result.Message = StringResources.Language.SiemensDBAddressNotAllowedLargerThan255
					return result

				result.Content2 = SiemensFetchWriteNet.CalculateAddressStarted( address[ address.find( '.' ) + 1:] )
			elif address[0] == 'T':
				result.Content1 = 0x07
				result.Content2 = SiemensFetchWriteNet.CalculateAddressStarted( address[1:] )
			elif address[0] == 'C':
				result.Content1 = 0x06
				result.Content2 = SiemensFetchWriteNet.CalculateAddressStarted( address[1:])
			else:
				result.Message = StringResources.Language.NotSupportedDataType
				result.Content1 = 0
				result.Content2 = 0
				result.Content3 = 0
				return result
		except Exception as ex:
			result.Message = str(ex)
			return result

		result.IsSuccess = True
		return result
	@staticmethod
	def BuildReadCommand( address, count ):
		'''生成一个读取字数据指令头的通用方法'''
		result = OperateResult( )

		analysis = SiemensFetchWriteNet.AnalysisAddress( address )
		if analysis.IsSuccess == False :
			result.CopyErrorFromOther( analysis )
			return result

		_PLCCommand = bytearray(16)
		_PLCCommand[0] = 0x53
		_PLCCommand[1] = 0x35
		_PLCCommand[2] = 0x10
		_PLCCommand[3] = 0x01
		_PLCCommand[4] = 0x03
		_PLCCommand[5] = 0x05
		_PLCCommand[6] = 0x03
		_PLCCommand[7] = 0x08

		# 指定数据区
		_PLCCommand[8] = analysis.Content1
		_PLCCommand[9] = analysis.Content3

		# 指定数据地址
		_PLCCommand[10] =analysis.Content2 // 256
		_PLCCommand[11] = analysis.Content2 % 256

		if analysis.Content1 == 0x01 or analysis.Content1 == 0x06 or analysis.Content1 == 0x07:
			if count % 2 != 0:
				result.Message = StringResources.Language.SiemensReadLengthMustBeEvenNumber
				return result
			else:
				# 指定数据长度
				_PLCCommand[12] = count // 2 // 256
				_PLCCommand[13] = count // 2 % 256
		else:
			# 指定数据长度
			_PLCCommand[12] = count // 256
			_PLCCommand[13] = count % 256

		_PLCCommand[14] = 0xff
		_PLCCommand[15] = 0x02

		result.Content = _PLCCommand
		result.IsSuccess = True
		return result
	@staticmethod
	def BuildWriteCommand( address, data ):
		'''生成一个写入字节数据的指令'''
		if data == None : data = bytearray(0)
		result = OperateResult( )

		analysis = SiemensFetchWriteNet.AnalysisAddress( address )
		if analysis.IsSuccess == False:
			result.CopyErrorFromOther( analysis )
			return result

		_PLCCommand = bytearray(16 + len(data))
		_PLCCommand[0] = 0x53
		_PLCCommand[1] = 0x35
		_PLCCommand[2] = 0x10
		_PLCCommand[3] = 0x01
		_PLCCommand[4] = 0x03
		_PLCCommand[5] = 0x03
		_PLCCommand[6] = 0x03
		_PLCCommand[7] = 0x08

		# 指定数据区
		_PLCCommand[8] = analysis.Content1
		_PLCCommand[9] = analysis.Content3

		# 指定数据地址
		_PLCCommand[10] = analysis.Content2 // 256
		_PLCCommand[11] = analysis.Content2 % 256

		if analysis.Content1 == 0x01 or analysis.Content1 == 0x06 or analysis.Content1 == 0x07:
			if data.Length % 2 != 0:
				result.Message = StringResources.Language.SiemensReadLengthMustBeEvenNumber
				return result
			else:
				# 指定数据长度
				_PLCCommand[12] = data.Length // 2 // 256
				_PLCCommand[13] = data.Length // 2 % 256
		else:
			# 指定数据长度
			_PLCCommand[12] = data.Length // 256
			_PLCCommand[13] = data.Length % 256
		_PLCCommand[14] = 0xff
		_PLCCommand[15] = 0x02

		# 放置数据
		_PLCCommand[16:16+len(data)] = data

		result.Content = _PLCCommand
		result.IsSuccess = True
		return result
	def Read( self, address, length ):
		'''从PLC读取数据，地址格式为I100，Q100，DB20.100，M100，T100，C100，以字节为单位'''
		# 指令解析 -> Instruction parsing
		command = SiemensFetchWriteNet.BuildReadCommand( address, length )
		if command.IsSuccess == False : return command

		# 核心交互 -> Core Interactions
		read = self.ReadFromCoreServer( command.Content )
		if read.IsSuccess == False : return read

		# 错误码验证 -> Error code Verification
		if read.Content[8] != 0x00 : return OperateResult(read.Content[8],"发生了异常，具体信息查找Fetch/Write协议文档")

		# 读取正确 -> Read Right
		buffer = bytearray(len(read.Content) - 16)
		buffer[0:len(buffer)] = read.Content[16:16+len(buffer)]
		return OperateResult.CreateSuccessResult( buffer )
	def ReadByte( self, address ):
		'''读取指定地址的byte数据'''
		return ByteTransformHelper.GetResultFromArray( self.Read( address, 1 ) )
	def Write( self, address, value ):
		'''将数据写入到PLC数据，地址格式为I100，Q100，DB20.100，M100，以字节为单位'''
		# 指令解析 -> Instruction parsing
		command = SiemensFetchWriteNet.BuildWriteCommand( address, value )
		if command.IsSuccess == False : return command

		# 核心交互 -> Core Interactions
		write = self.ReadFromCoreServer( command.Content )
		if write.IsSuccess == False : return write

		# 错误码验证 -> Error code Verification
		if (write.Content[8] != 0x00) : OperateResult(err = write.Content[8], msg = "西门子PLC写入失败！")

		# 写入成功 -> Write Right
		return OperateResult.CreateSuccessResult( )
	def WriteBool( self, address, values):
		'''向PLC中写入byte数据，返回是否写入成功 -> Writes byte data to the PLC and returns whether the write succeeded'''
		if type(values) == list:
			return self.Write( address, SoftBasic.BoolArrayToByte( values ) )
		else:
			return self.WriteBool( address, [ values ] )


class S7Message (INetMessage):
	'''西门子s7协议的消息接收规则'''
	def ProtocolHeadBytesLength(self):
		'''协议头数据长度，也即是第一次接收的数据长度'''
		return 4
	def GetContentLengthByHeadBytes(self):
		'''二次接收的数据长度'''
		if self.HeadBytes != None:
			return self.HeadBytes[2]*256 + self.HeadBytes[3]-4
		else:
			return 0
	def CheckHeadBytesLegal(self,token):
		'''令牌检查是否成功'''
		if self.HeadBytes != None:
			if self.HeadBytes[0] == 0x03 and self.HeadBytes[1] == 0x00:
				return True
			else:
				return False
		else:
			return False

