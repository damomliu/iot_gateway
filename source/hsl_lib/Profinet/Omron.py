import struct

from .. import OperateResult, StringResources, SoftBasic
from ..Core import ReverseBytesTransform, ReverseWordTransform, DataFormat, INetMessage, NetworkDeviceBase

__all__ = [
	'OmronFinsDataType',
	'OmronFinsNetHelper',
	'OmronFinsNet',
	'OmronFinsNetHelper',
]


class OmronFinsDataType:
	'''欧姆龙的Fins协议的数据类型'''
	BitCode = 0
	WordCode = 0
	def __init__(self, bitCode = 0, wordCode = 0):
		'''实例化一个Fins的数据类型'''
		self.BitCode = bitCode
		self.WordCode = wordCode
	@staticmethod
	def DM():
		'''DM Area'''
		return OmronFinsDataType( 0x02, 0x82 )
	@staticmethod
	def CIO():
		'''CIO Area'''
		return OmronFinsDataType( 0x30, 0xB0 )
	@staticmethod
	def WR():
		'''Work Area'''
		return OmronFinsDataType( 0x31, 0xB1 )
	@staticmethod
	def HR():
		'''Holding Bit Area'''
		return OmronFinsDataType( 0x32, 0xB2 )
	@staticmethod
	def AR():
		'''Auxiliary Bit Area'''
		return OmronFinsDataType( 0x33, 0xB3 )

class OmronFinsNet(NetworkDeviceBase):
	'''欧姆龙PLC通讯类，采用Fins-Tcp通信协议实现'''
	def __init__(self,ipAddress="127.0.0.1",port = 9600):
		super().__init__()
		'''实例化一个欧姆龙PLC Fins帧协议的通讯对象'''
		self.WordLength = 1
		self.ipAddress = ipAddress
		self.port = port
		self.byteTransform = ReverseWordTransform()
		self.byteTransform.DataFormat = DataFormat.CDAB
		self.DA1 = int(ipAddress.split(".")[3])
		self.iNetMessage = FinsMessage()
		self.ICF = 0x80
		self.RSV = 0x00
		self.GCT = 0x02
		self.DNA = 0x00
		self.DA1 = 0x13
		self.DA2 = 0x00
		self.SNA = 0x00
		self.SA1 = 0x00
		self.SA2 = 0x00
		self.SID = 0x00
		self.IsChangeSA1AfterReadFailed = False
		self.handSingle = bytearray([0x46, 0x49, 0x4E, 0x53,0x00, 0x00, 0x00, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01])

	def SetSA1(self, value):
		'''设置SA1的方法'''
		self.SA1 = value
		self.handSingle[19] = value

	def PackCommand( self, cmd ):
		'''将普通的指令打包成完整的指令
		
		Parameter
		  cmd: bytearray 原始的fins指令
		Return
		  bytearray: 结果的数据'''
		buffer = bytearray(26 + len(cmd))
		buffer[0:4] = self.handSingle[0:4]
		tmp = struct.pack('>i', len(buffer) - 8 )
		buffer[4:8] = tmp
		buffer[11] = 0x02
		buffer[16] = self.ICF
		buffer[17] = self.RSV
		buffer[18] = self.GCT
		buffer[19] = self.DNA
		buffer[20] = self.DA1
		buffer[21] = self.DA2
		buffer[22] = self.SNA
		buffer[23] = self.SA1
		buffer[24] = self.SA2
		buffer[25] = self.SID
		buffer[26:] = cmd
		return buffer
	def BuildReadCommand( self, address, length , isBit):
		'''根据类型地址长度确认需要读取的指令头
		
		Parameter
		  address: string 起始地址
		  length: ushort 长度
		  isBit: bool 是否是位读取
		Return
		  OperateResult: 结果的数据'''
		command = OmronFinsNetHelper.BuildReadCommand( address, length, isBit )
		if command.IsSuccess == False : return command

		return OperateResult.CreateSuccessResult( self.PackCommand( command.Content ) )
	def BuildWriteCommand( self, address, value, isBit ):
		'''根据类型地址以及需要写入的数据来生成指令头
		
		Parameter
		  address: string 起始地址
		  value: bytearray 真实的数据值信息
		  isBit: bool 是否是位读取
		Return
		  OperateResult: 结果的数据'''
		command = OmronFinsNetHelper.BuildWriteWordCommand( address, value, isBit )
		if command.IsSuccess == False : return command
			
		return OperateResult.CreateSuccessResult( self.PackCommand( command.Content ) )
	def InitializationOnConnect( self, socket ):
		'''在连接上欧姆龙PLC后，需要进行一步握手协议
		
		Parameter
		  socket: Socket 连接的套接字
		Return
		  OperateResult: 是否初始化成功'''
		# 握手信号
		read = self.ReadFromCoreServerBase( socket, self.handSingle )
		if read.IsSuccess == False : return read

		# 检查返回的状态
		buffer = bytearray(4)
		buffer[0] = read.Content2[7]
		buffer[1] = read.Content2[6]
		buffer[2] = read.Content2[5]
		buffer[3] = read.Content2[4]

		status = struct.unpack( '<i',buffer )[0]
		if status != 0 : return OperateResult( err = status, msg = OmronFinsNetHelper.GetStatusDescription( status ) )

		# 提取PLC的节点地址
		if len(read.Content2) >= 24 : self.DA1 = read.Content2[23]

		return OperateResult.CreateSuccessResult( )
	def Read( self, address, length ):
		'''从欧姆龙PLC中读取想要的数据，返回读取结果，读取单位为字
		
		Parameter
		  address: string 读取地址，格式为"D100","C100","W100","H100","A100"
		  length: ushort 读取的数据长度
		Return
		  OperateResult: 带成功标志的结果数据对象'''
		# 获取指令
		command = self.BuildReadCommand( address, length, False )
		if command.IsSuccess == False : return OperateResult.CreateFailedResult( command )

		# 核心数据交互
		read = self.ReadFromCoreServer( command.Content )
		if read.IsSuccess == False : return OperateResult.CreateFailedResult( read )

		# 数据有效性分析
		valid = OmronFinsNetHelper.ResponseValidAnalysis( read.Content, True )
		if valid.IsSuccess == False : return OperateResult.CreateFailedResult( valid )

		# 读取到了正确的数据
		return OperateResult.CreateSuccessResult( valid.Content )
	def Write( self, address, value ):
		'''向PLC中位软元件写入bool数组，返回值说明，比如你写入D100,values[0]对应D100.0
		
		Parameter
		  address: string 读取地址，格式为"D100","C100","W100","H100","A100"
		  value: bytearray 原始的字节数据
		Return
		  OperateResult: 结果内容'''
		# 获取指令
		command = self.BuildWriteCommand( address, value, False )
		if command.IsSuccess == False : return command

		# 核心数据交互
		read = self.ReadFromCoreServer( command.Content )
		if read.IsSuccess == False : return read

		# 数据有效性分析
		valid = OmronFinsNetHelper.ResponseValidAnalysis( read.Content, False )
		if valid.IsSuccess == False : return valid

		# 成功
		return OperateResult.CreateSuccessResult( )
	def ReadBool( self, address, length = None ):
		'''从欧姆龙PLC中批量读取位软元件，返回读取结果
		
		Parameter
		  address: string 读取地址，格式为"D100","C100","W100","H100","A100"
		  length: ushort 读取的长度
		Return
		  OperateResult: 带成功标志的结果数据对象'''
		if length == None:
			read = self.ReadBool( address, 1 )
			if read.IsSuccess == False : return OperateResult.CreateFailedResult( read )

			return OperateResult.CreateSuccessResult( read.Content[0] )
		else:
			# 获取指令
			command = self.BuildReadCommand( address, length, True )
			if command.IsSuccess == False : return OperateResult.CreateFailedResult( command )

			# 核心数据交互
			read = self.ReadFromCoreServer( command.Content )
			if read.IsSuccess == False : return OperateResult.CreateFailedResult( read )

			# 数据有效性分析
			valid = OmronFinsNetHelper.ResponseValidAnalysis( read.Content, True )
			if valid.IsSuccess == False : return OperateResult.CreateFailedResult( valid )

			# 返回正确的数据信息
			content = []
			for i in range(len(valid.Content)):
				if valid.Content[i] == 0x01:
					content.append(True)
				else:
					content.append(False)
			return OperateResult.CreateSuccessResult( content )
	def WriteBool( self, address, values ):
		'''向PLC中位软元件写入bool数组，返回值说明，比如你写入D100,values[0]对应D100.0
		
		Parameter
		  address: string 读取地址，格式为"D100","C100","W100","H100","A100"
		  values: bytearray 要写入的实际数据，可以指定任意的长度
		Return
		  OperateResult: 带成功标志的结果数据对象'''
		if type(values) == list:
			# 获取指令
			content = bytearray(len(values))
			for i in range(len(values)):
				if values[i] == True:
					content[i] = 0x01
				else:
					content[i] = 0x00
			command = self.BuildWriteCommand( address, content, True )
			if command.IsSuccess == False : return command

			# 核心数据交互
			read = self.ReadFromCoreServer( command.Content )
			if read.IsSuccess == False : return read

			# 数据有效性分析
			valid = OmronFinsNetHelper.ResponseValidAnalysis( read.Content, False )
			if valid.IsSuccess == False : return valid

			# 写入成功
			return OperateResult.CreateSuccessResult( )
		else:
			return self.WriteBool( address, [values] )
	def __PackCommand( self, cmd ):
		'''将普通的指令打包成完整的指令'''
		buffer = bytearray(26 + len(cmd))
		self.handSingle[0:4] = buffer[0:4]
		tmp = struct.pack('>i',(len(buffer)-8))
		buffer[4:8] = tmp
		buffer[11] = 0x02
		buffer[16] = self.ICF
		buffer[17] = self.RSV
		buffer[18] = self.GCT
		buffer[19] = self.DNA
		buffer[20] = self.DA1
		buffer[21] = self.DA2
		buffer[22] = self.SNA
		buffer[23] = self.SA1
		buffer[24] = self.SA2
		buffer[25] = self.SID
		buffer[26:] = cmd
		return buffer
	
	def __str__(self):
		'''
		返回表示当前对象的字符串
		'''
		return "OmronFinsNet[" + self.ipAddress + ":" + str(self.port) + "]"

class OmronFinsNetHelper:
	@staticmethod
	def AnalysisAddress( address, isBit ):
		'''解析数据地址，Omron手册第188页

		Parameter
		  address: string 字符串的地址信息
		  isBit: bool 是否是位地址
		Return
		  OperateResult: 结果对象
		'''
		result = OperateResult( )
		try:
			if address[0] == 'D' or address[0] == 'd':
				result.Content1 = OmronFinsDataType.DM()
			elif address[0] == 'C' or address[0] == 'c':
				result.Content1 = OmronFinsDataType.CIO()
			elif address[0] == 'W' or address[0] == 'w':
				result.Content1 = OmronFinsDataType.WR()
			elif address[0] == 'H' or address[0] == 'h':
				result.Content1 = OmronFinsDataType.HR()
			elif address[0] == 'A' or address[0] == 'a':
				result.Content1 = OmronFinsDataType.AR()
			elif address[0] == 'E' or address[0] == 'e':
				# E区，比较复杂，需要专门的计算
				splits = address.split(".")
				block = int(splits[0][1:], 16)
				if block < 16:
					result.Content1 = OmronFinsDataType( 0x20 + block, 0xA0 + block)
				else:
					result.Content1 = OmronFinsDataType( 0xE0 + block - 16, 0x60 + block - 16)
			else: raise Exception( StringResources.Language.NotSupportedDataType )

			if address[0] == 'E' or address[0] == 'e':
				splits = address.split(".")
				if isBit:
					# 位操作
					addr = int( splits[1] )
					result.Content2 = bytearray(3)
					result.Content2[0] = struct.pack("<i", addr )[1]
					result.Content2[1] = struct.pack("<i", addr )[0]

					if splits.Length > 2:
						result.Content2[2] = int( splits[2] )
						if result.Content2[2] > 15:
							raise Exception( StringResources.Language.OmronAddressMustBeZeroToFiveteen )
				else:
					# 字操作
					addr = int( splits[1] )
					result.Content2 =  bytearray(3)
					result.Content2[0] = struct.pack("<i", addr )[1]
					result.Content2[1] = struct.pack("<i", addr )[0]
			else:
				if isBit:
					# 位操作
					splits = address[1:].split(".")
					addr = int( splits[0] )
					result.Content2 = bytearray(3)
					result.Content2[0] = struct.pack("<i", addr )[1]
					result.Content2[1] = struct.pack("<i", addr )[0]

					if len(splits) > 1:
						result.Content2[2] = int( splits[1] )
						if result.Content2[2] > 15:
							raise Exception( StringResources.Language.OmronAddressMustBeZeroToFiveteen )
				else:
					# 字操作
					addr = int( address[1:] )
					result.Content2 = bytearray(3)
					result.Content2[0] = struct.pack("<i", addr )[1]
					result.Content2[1] = struct.pack("<i", addr )[0]
		except Exception as ex:
			result.Message = str(ex)
			return result
		result.IsSuccess = True
		return result

	@staticmethod
	def BuildReadCommand( address, length, isBit ):
		'''
		根据读取的地址，长度，是否位读取创建Fins协议的核心报文
		
		Parameter
		  address: string 字符串的地址信息
		  length: int 读取的数据长度
		  isBit: bool 是否是位地址
		Return
		  OperateResult: 带有成功标识的Fins核心报文
		'''
		analysis = OmronFinsNetHelper.AnalysisAddress( address, isBit )
		if analysis.IsSuccess == False: return OperateResult.CreateFailedResult( analysis )

		_PLCCommand = bytearray(8)
		_PLCCommand[0] = 0x01    # 读取存储区数据
		_PLCCommand[1] = 0x01
		if isBit == True:
			_PLCCommand[2] = analysis.Content1.BitCode
		else:
			_PLCCommand[2] = analysis.Content1.WordCode
		_PLCCommand[3:6] = analysis.Content2
		_PLCCommand[6] = length // 256   # 长度
		_PLCCommand[7] = length % 256
		return OperateResult.CreateSuccessResult( _PLCCommand )

	@staticmethod
	def BuildWriteWordCommand( address, value, isBit ):
		'''根据写入的地址，数据，是否位写入生成Fins协议的核心报文
		
		Parameter
		  address: string 字符串的地址信息
		  value: bytearray 实际的数据内容
		  isBit: bool 是否是位地址
		Return
		  OperateResult: 带有成功标识的Fins核心报文
		'''
		analysis = OmronFinsNetHelper.AnalysisAddress( address, isBit )
		if analysis.IsSuccess == False: return OperateResult.CreateFailedResult( analysis )

		_PLCCommand = bytearray(8 + len(value))
		_PLCCommand[0] = 0x01
		_PLCCommand[1] = 0x02

		if isBit == True:
			_PLCCommand[2] = analysis.Content1.BitCode
		else:
			_PLCCommand[2] = analysis.Content1.WordCode

		_PLCCommand[3:6] = analysis.Content2
		if isBit == True:
			_PLCCommand[6] = len(value) // 256
			_PLCCommand[7] = len(value) % 256
		else:
			_PLCCommand[6] = len(value) // 2 // 256
			_PLCCommand[7] = len(value) // 2 % 256

		_PLCCommand[8:] = value
		return OperateResult.CreateSuccessResult( _PLCCommand )

	@staticmethod
	def ResponseValidAnalysis( response, isRead ):
		'''验证欧姆龙的Fins-TCP返回的数据是否正确的数据，如果正确的话，并返回所有的数据内容
		
		Parameter
		  response: bytearray 来自欧姆龙返回的数据内容
		  isRead: bool 是否读取
		Return
		  OperateResult: 带有是否成功的结果对象
		'''
		if len(response) >= 16:
			# 提取错误码 -> Extracting error Codes
			buffer = bytearray(4)
			buffer[0] = response[15]
			buffer[1] = response[14]
			buffer[2] = response[13]
			buffer[3] = response[12]

			err = struct.unpack('<i',buffer)[0]
			if err > 0 : return OperateResult( err = err, msg = OmronFinsNetHelper.GetStatusDescription( err ) )

			result = response[16:]
			return OmronFinsNetHelper.UdpResponseValidAnalysis( result, isRead )

		return OperateResult( msg= StringResources.Language.OmronReceiveDataError )

	@staticmethod
	def UdpResponseValidAnalysis( response, isRead ):
		''' 验证欧姆龙的Fins-Udp返回的数据是否正确的数据，如果正确的话，并返回所有的数据内容
		
		Parameter
		  response: bytearray 来自欧姆龙返回的数据内容
		  isRead: bool 是否读取
		Return
		  OperateResult: 带有是否成功的结果对象
		'''
		if len(response) >= 14:
			err = response[12] * 256 + response[13]
			# if (err > 0) return new OperateResult<byte[]>( err, StringResources.Language.OmronReceiveDataError );

			if isRead == False:
				success = OperateResult.CreateSuccessResult(bytearray(0))
				success.ErrorCode = err
				success.Message = OmronFinsNetHelper.GetStatusDescription( err ) + " Received:" + SoftBasic.ByteToHexString( response, ' ' )
				return success
			else:
				# 读取操作 -> read operate
				content = response[14:]

				success = OperateResult.CreateSuccessResult( content )
				if len(content) == 0: success.IsSuccess = False
				success.ErrorCode = err
				success.Message = OmronFinsNetHelper.GetStatusDescription( err ) + " Received:" + SoftBasic.ByteToHexString( response, ' ' )
				return success

		return OperateResult( msg= StringResources.Language.OmronReceiveDataError )

	@staticmethod
	def GetStatusDescription( err ):
		'''获取错误信息的字符串描述文本
			
		Parameter
		  err: int 错误码
		Return
		  string: 文本描述
			'''
		if err == 0 : return StringResources.Language.OmronStatus0
		elif err == 1 : return StringResources.Language.OmronStatus1
		elif err == 2 : return StringResources.Language.OmronStatus2
		elif err == 3 : return StringResources.Language.OmronStatus3
		elif err == 20 : return StringResources.Language.OmronStatus20
		elif err == 21 : return StringResources.Language.OmronStatus21
		elif err == 22 : return StringResources.Language.OmronStatus22
		elif err == 23 : return StringResources.Language.OmronStatus23
		elif err == 24 : return StringResources.Language.OmronStatus24
		elif err == 25 : return StringResources.Language.OmronStatus25
		else : return StringResources.Language.UnknownError


class FinsMessage(INetMessage):
	'''用于欧姆龙通信的Fins协议的消息解析规则'''
	def ProtocolHeadBytesLength(self):
		'''协议头数据长度，也即是第一次接收的数据长度'''
		return 8
	def GetContentLengthByHeadBytes(self):
		'''二次接收的数据长度'''
		if self.HeadBytes != None:
			buffer = bytearray(4)
			buffer[0:4] = self.HeadBytes[4:8]
			return struct.unpack('>i',buffer)[0]
		else:
			return 0
	def CheckHeadBytesLegal(self,token):
		'''令牌检查是否成功'''
		return True

