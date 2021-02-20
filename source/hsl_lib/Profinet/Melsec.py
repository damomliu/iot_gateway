import struct

from .. import OperateResult, StringResources
from ..Core import RegularByteTransform, ByteTransformHelper, INetMessage, NetworkDeviceBase
from ..Core.Net import NetworkDeviceBase

__all__ = [
	'MelsecA1EDataType', 'MelsecMcDataType',
	'ByteTransformHelper',
	'MelsecA1ENet', 'MelsecMcNet', 'MelsecMcAsciiNet',
	'MelsecA1EBinaryMessage', 'MelsecQnA3EBinaryMessage', 'MelsecQnA3EAsciiMessage',
]


class MelsecA1EDataType:
	'''三菱PLC的数据类型，此处包含了几个常用的类型'''
	def __init__(self, code0, code1, typeCode, asciiCode, fromBase):
		'''如果您清楚类型代号，可以根据值进行扩展'''
		self.DataCode = bytearray(2)
		self.DataType = 0
		self.DataCode[0] = code0
		self.DataCode[1] = code1
		self.AsciiCode = asciiCode
		self.FromBase = fromBase
		if typeCode < 2:
			self.DataType = typeCode
	
	@staticmethod
	def GetX():
		'''X输入寄存器'''
		return MelsecA1EDataType(0x58,0x20,0x01,'X*',8)
	@staticmethod
	def GetY():
		'''Y输出寄存器'''
		return MelsecA1EDataType(0x59,0x20,0x01,'Y*',8)
	@staticmethod
	def GetM():
		'''M中间寄存器'''
		return MelsecA1EDataType(0x4D,0x20,0x01,'M*',10)
	@staticmethod
	def GetS():
		'''S状态寄存器'''
		return MelsecA1EDataType(0x53,0x20,0x01,'S*',10)
	@staticmethod
	def GetD():
		'''D数据寄存器'''
		return MelsecA1EDataType(0x44,0x20,0x00,'D*',10)
	@staticmethod
	def GetR():
		'''R文件寄存器'''
		return MelsecA1EDataType(0x52,0x20,0x00,'R*',10)

class MelsecMcDataType:
	'''三菱PLC的数据类型，此处包含了几个常用的类型'''
	DataCode = 0
	DataType = 0
	AsciiCode = 0
	FromBase = 0
	def __init__(self, code, typeCode, asciiCode, fromBase):
		'''如果您清楚类型代号，可以根据值进行扩展'''
		self.DataCode = code
		self.AsciiCode = asciiCode
		self.FromBase = fromBase
		if typeCode < 2:
			self.DataType = typeCode

	@staticmethod
	def GetX():
		'''X输入寄存器'''
		return MelsecMcDataType(0x9C,0x01,'X*',16)
	@staticmethod
	def GetY():
		'''Y输出寄存器'''
		return MelsecMcDataType(0x9D,0x01,'Y*',16)
	@staticmethod
	def GetM():
		'''M中间寄存器'''
		return MelsecMcDataType(0x90,0x01,'M*',10)
	@staticmethod
	def GetD():
		'''D数据寄存器'''
		return MelsecMcDataType(0xA8,0x00,'D*',10)
	@staticmethod
	def GetW():
		'''W链接寄存器'''
		return MelsecMcDataType(0xB4,0x00,'W*',16)
	@staticmethod
	def GetL():
		'''L锁存继电器'''
		return MelsecMcDataType(0x92,0x01,'L*',10)
	@staticmethod
	def GetF():
		'''F报警器'''
		return MelsecMcDataType(0x93,0x01,'F*',10)
	@staticmethod
	def GetV():
		'''V边沿继电器'''
		return MelsecMcDataType(0x93,0x01,'V*',10)
	@staticmethod
	def GetB():
		'''B链接继电器'''
		return MelsecMcDataType(0xA,0x01,'B*',16)
	@staticmethod
	def GetR():
		'''R文件寄存器'''
		return MelsecMcDataType(0xAF,0x00,'R*',10)
	@staticmethod
	def GetS():
		'''S步进继电器'''
		return MelsecMcDataType(0x98,0x01,'S*',10)
	@staticmethod
	def GetZ():
		'''变址寄存器'''
		return MelsecMcDataType(0xCC,0x00,'Z*',10)
	@staticmethod
	def GetT():
		'''定时器的值'''
		return MelsecMcDataType(0xC2,0x00,'TN',10)
	@staticmethod
	def GetC():
		'''计数器的值'''
		return MelsecMcDataType(0xC5,0x00,'CN',10)

class MelsecHelper:
	'''所有三菱通讯类的通用辅助工具类，包含了一些通用的静态方法，可以使用本类来获取一些原始的报文信息。详细的操作参见例子'''
	@staticmethod
	def McA1EAnalysisAddress( address = "0" ):
		result = OperateResult()
		try:
			if address.startswith("X") or address.startswith("x"):
				result.Content1 = MelsecA1EDataType.GetX()
				result.Content2 = int(address[1:], MelsecA1EDataType.GetX().FromBase)
			elif address.startswith("Y") or address.startswith("y"):
				result.Content1 = MelsecA1EDataType.GetY()
				result.Content2 = int(address[1:], MelsecA1EDataType.GetY().FromBase)
			elif address.startswith("M") or address.startswith("m"):
				result.Content1 = MelsecA1EDataType.GetM()
				result.Content2 = int(address[1:], MelsecA1EDataType.GetM().FromBase)
			elif address.startswith("S") or address.startswith("s"):
				result.Content1 = MelsecA1EDataType.GetS()
				result.Content2 = int(address[1:], MelsecA1EDataType.GetS().FromBase)
			elif address.startswith("D") or address.startswith("d"):
				result.Content1 = MelsecA1EDataType.GetD()
				result.Content2 = int(address[1:], MelsecA1EDataType.GetD().FromBase)
			elif address.startswith("R") or address.startswith("r"):
				result.Content1 = MelsecA1EDataType.GetR()
				result.Content2 = int(address[1:], MelsecA1EDataType.GetR().FromBase)
			else:
				raise Exception("type not supported!")
		except Exception as ex:
			result.Message = str(ex)
			return result
		
		result.IsSuccess = True
		result.Message = StringResources.Language.SuccessText
		return result
	@staticmethod
	def McAnalysisAddress( address = "0" ):
		result = OperateResult()
		try:
			if address.startswith("M") or address.startswith("m"):
				result.Content1 = MelsecMcDataType.GetM()
				result.Content2 = int(address[1:], MelsecMcDataType.GetM().FromBase)
			elif address.startswith("X") or address.startswith("x"):
				result.Content1 = MelsecMcDataType.GetX()
				result.Content2 = int(address[1:], MelsecMcDataType.GetX().FromBase)
			elif address.startswith("Y") or address.startswith("y"):
				result.Content1 = MelsecMcDataType.GetY()
				result.Content2 = int(address[1:], MelsecMcDataType.GetY().FromBase)
			elif address.startswith("D") or address.startswith("d"):
				result.Content1 = MelsecMcDataType.GetD()
				result.Content2 = int(address[1:], MelsecMcDataType.GetD().FromBase)
			elif address.startswith("W") or address.startswith("w"):
				result.Content1 = MelsecMcDataType.GetW()
				result.Content2 = int(address[1:], MelsecMcDataType.GetW().FromBase)
			elif address.startswith("L") or address.startswith("l"):
				result.Content1 = MelsecMcDataType.GetL()
				result.Content2 = int(address[1:], MelsecMcDataType.GetL().FromBase)
			elif address.startswith("F") or address.startswith("f"):
				result.Content1 = MelsecMcDataType.GetF()
				result.Content2 = int(address[1:], MelsecMcDataType.GetF().FromBase)
			elif address.startswith("V") or address.startswith("v"):
				result.Content1 = MelsecMcDataType.GetV()
				result.Content2 = int(address[1:], MelsecMcDataType.GetV().FromBase)
			elif address.startswith("B") or address.startswith("b"):
				result.Content1 = MelsecMcDataType.GetB()
				result.Content2 = int(address[1:], MelsecMcDataType.GetB().FromBase)
			elif address.startswith("R") or address.startswith("r"):
				result.Content1 = MelsecMcDataType.GetR()
				result.Content2 = int(address[1:], MelsecMcDataType.GetR().FromBase)
			elif address.startswith("S") or address.startswith("s"):
				result.Content1 = MelsecMcDataType.GetS()
				result.Content2 = int(address[1:], MelsecMcDataType.GetS().FromBase)
			elif address.startswith("Z") or address.startswith("z"):
				result.Content1 = MelsecMcDataType.GetZ()
				result.Content2 = int(address[1:], MelsecMcDataType.GetZ().FromBase)
			elif address.startswith("T") or address.startswith("t"):
				result.Content1 = MelsecMcDataType.GetT()
				result.Content2 = int(address[1:], MelsecMcDataType.GetT().FromBase)
			elif address.startswith("C") or address.startswith("c"):
				result.Content1 = MelsecMcDataType.GetC()
				result.Content2 = int(address[1:], MelsecMcDataType.GetC().FromBase)
			else:
				raise Exception("type not supported!")
		except Exception as ex:
			result.Message = str(ex)
			return result
		
		result.IsSuccess = True
		result.Message = StringResources.Language.SuccessText
		return result
	@staticmethod
	def BuildBytesFromData( value, length = None ):
		'''从数据构建一个ASCII格式地址字节'''
		if length == None:
			return ('{:02X}'.format(value)).encode('ascii')
		else:
			return (('{:0'+ str(length) +'X}').format(value)).encode('ascii')
	@staticmethod
	def BuildBytesFromAddress( address, dataType ):
		'''从三菱的地址中构建MC协议的6字节的ASCII格式的地址'''
		if dataType.FromBase == 10:
			return ('{:06d}'.format(address)).encode('ascii')
		else:
			return ('{:06X}'.format(address)).encode('ascii')
	@staticmethod
	def FxCalculateCRC( data ):
		'''计算Fx协议指令的和校验信息'''
		sum = 0
		index = 1
		while index < (len(data) - 2):
			sum += data[index]
			index=index+1
		return MelsecHelper.BuildBytesFromData( sum )
	@staticmethod
	def CheckCRC( data ):
		'''检查指定的和校验是否是正确的'''
		crc = MelsecHelper.FxCalculateCRC( data )
		if (crc[0] != data[data.Length - 2]) : return False
		if (crc[1] != data[data.Length - 1]) : return False
		return True
		
class MelsecA1ENet(NetworkDeviceBase):
	'''三菱PLC通讯协议，采用A兼容1E帧协议实现，使用二进制码通讯，请根据实际型号来进行选取'''
	def __init__(self,ipAddress= "127.0.0.1",port = 0):
		super().__init__()
		'''实例化一个三菱的A兼容1E帧协议的通讯对象'''
		self.PLCNumber = 0xFF
		self.iNetMessage = MelsecA1EBinaryMessage()
		self.byteTransform = RegularByteTransform()
		self.ipAddress = ipAddress
		self.port = port
		self.WordLength = 1
	@staticmethod
	def BuildReadCommand(address,length,isBit,plcNumber):
		'''根据类型地址长度确认需要读取的指令头'''
		analysis = MelsecHelper.McA1EAnalysisAddress( address )
		if analysis.IsSuccess == False : return OperateResult.CreateFailedResult( analysis )
		
		subtitle = 0x00 if isBit else 0x01

		_PLCCommand = bytearray(12)
		_PLCCommand[0]  = subtitle                               # 副标题
		_PLCCommand[1]  = plcNumber                              # PLC编号
		_PLCCommand[2]  = 0x0A                                   # CPU监视定时器（L）这里设置为0x00,0x0A，等待CPU返回的时间为10*250ms=2.5秒
		_PLCCommand[3]  = 0x00                                   # CPU监视定时器（H）
		_PLCCommand[4]  = analysis.Content2 % 256                # 起始软元件（开始读取的地址）
		_PLCCommand[5]  = analysis.Content2 // 256
		_PLCCommand[6]  = 0x00
		_PLCCommand[7]  = 0x00
		_PLCCommand[8]  = analysis.Content1.DataCode[1]          # 软元件代码（L）
		_PLCCommand[9]  = analysis.Content1.DataCode[0]          # 软元件代码（H）
		_PLCCommand[10] = length % 256                           # 软元件点数
		_PLCCommand[11] = 0x00

		return OperateResult.CreateSuccessResult( _PLCCommand )
	@staticmethod
	def BuildWriteCommand( address,value,plcNumber):
		'''根据类型地址以及需要写入的数据来生成指令头'''
		analysis = MelsecHelper.McA1EAnalysisAddress( address )
		if analysis.IsSuccess == False : return OperateResult.CreateFailedResult( analysis )
		
		length = -1
		if analysis.Content1.DataType == 1:
			# 按照位写入的操作，数据需要重新计算
			length2 =  len(value) // 2 + 1
			if len(value) % 2 == 0 : 
				length2 = len(value) // 2
			buffer = bytearray(length2)

			for i in range(length2):
				if value[i * 2 + 0] != 0x00 :
					buffer[i] += 0x10
				if (i * 2 + 1) < len(value) :
					if value[i * 2 + 1] != 0x00 :
						buffer[i] += 0x01
			length = len(value)
			value = buffer

		subtitle = 0
		if analysis.Content1.DataType == 0x01:
			subtitle = 0x02
		else:
			subtitle = 0x03
		
		_PLCCommand = bytearray(12 + len(value))
		_PLCCommand[0]  = subtitle                               # 副标题
		_PLCCommand[1]  = plcNumber                              # PLC编号
		_PLCCommand[2]  = 0x0A                                   # CPU监视定时器（L）这里设置为0x00,0x0A，等待CPU返回的时间为10*250ms=2.5秒
		_PLCCommand[3]  = 0x00                                   # CPU监视定时器（H）
		_PLCCommand[4]  = analysis.Content2 % 256                # 起始软元件（开始读取的地址）
		_PLCCommand[5]  = analysis.Content2 // 256
		_PLCCommand[6]  = 0x00
		_PLCCommand[7]  = 0x00
		_PLCCommand[8]  = analysis.Content1.DataCode[1]          # 软元件代码（L）
		_PLCCommand[9]  = analysis.Content1.DataCode[0]          # 软元件代码（H）
		_PLCCommand[10] = length % 256                           # 软元件点数
		_PLCCommand[11] = 0x00

		# 判断是否进行位操作
		if analysis.Content1.DataType == 1:
			if length > 0:
				_PLCCommand[10] = length % 256                   # 软元件点数
			else:
				_PLCCommand[10] = len(value) * 2 % 256           # 软元件点数
		else:
			_PLCCommand[10] = len(value) // 2 % 256              # 软元件点数
		_PLCCommand[12:] = value

		return OperateResult.CreateSuccessResult( _PLCCommand )
	@staticmethod
	def ExtractActualData( response, isBit ):
		''' 从PLC反馈的数据中提取出实际的数据内容，需要传入反馈数据，是否位读取'''
		if isBit == True:
			# 位读取
			Content = bytearray((len(response) - 2) * 2)
			i = 2
			while i < len(response):
				if (response[i] & 0x10) == 0x10:
					Content[(i - 2) * 2 + 0] = 0x01
				if (response[i] & 0x01) == 0x01:
					Content[(i - 2) * 2 + 1] = 0x01
				i = i + 1

			return OperateResult.CreateSuccessResult( Content )
		else:
			# 字读取
			return OperateResult.CreateSuccessResult( response[2:] )
	def Read( self, address, length ):
		'''从三菱PLC中读取想要的数据，返回读取结果'''
		# 获取指令
		command = MelsecA1ENet.BuildReadCommand( address, length, False, self.PLCNumber )
		if command.IsSuccess == False :
			return OperateResult.CreateFailedResult( command )

		# 核心交互
		read = self.ReadFromCoreServer( command.Content )
		if read.IsSuccess == False : return OperateResult.CreateFailedResult( read )

		# 错误代码验证
		errorCode = read.Content[1]
		if errorCode != 0 : return OperateResult(err=errorCode, msg=StringResources.Language.MelsecPleaseReferToManulDocument)

		# 数据解析，需要传入是否使用位的参数
		return MelsecA1ENet.ExtractActualData( read.Content, False )
	def ReadBool( self, address, length = None ):
		'''从三菱PLC中批量读取位软元件，返回读取结果'''
		if length == None:
			read = self.ReadBool(address,1)
			if read.IsSuccess == False:
				return OperateResult.CreateFailedResult(read)
			else:
				return OperateResult.CreateSuccessResult(read.Content[0])
		else:
			# 获取指令
			command = MelsecA1ENet.BuildReadCommand( address, length, True, self.PLCNumber )
			if command.IsSuccess == False :
				return OperateResult.CreateFailedResult( command )

			# 核心交互
			read = self.ReadFromCoreServer( command.Content )
			if read.IsSuccess == False : return OperateResult.CreateFailedResult( read )

			# 错误代码验证
			errorCode = read.Content[1]
			if errorCode != 0 : return OperateResult(err=errorCode, msg=StringResources.Language.MelsecPleaseReferToManulDocument)

			# 数据解析，需要传入是否使用位的参数
			extract = MelsecA1ENet.ExtractActualData( read.Content, True )
			if extract.IsSuccess == False: return OperateResult.CreateFailedResult( extract )

			# 转化bool数组
			content = []
			for i in range(length):
				if read.Content[i] == 0x01:
					content.append(True)
				else:
					content.append(False)
			return OperateResult.CreateSuccessResult( content )
	def Write( self, address, value ):
		'''向PLC写入数据，数据格式为原始的字节类型'''
		# 解析指令
		command = MelsecA1ENet.BuildWriteCommand( address, value, self.PLCNumber )
		if command.IsSuccess == False : return command

		# 核心交互
		read = self.ReadFromCoreServer( command.Content )
		if read.IsSuccess == False : return read

		# 错误码校验
		errorCode = read.Content[1]
		if errorCode != 0 : return OperateResult(err=errorCode, msg=StringResources.Language.MelsecPleaseReferToManulDocument)

		# 成功
		return OperateResult.CreateSuccessResult( )
	def WriteBool( self, address, values ):
		'''向PLC中位软元件写入bool数组或是值，返回值说明，比如你写入M100,values[0]对应M100'''
		if type(values) == list:
			buffer = bytearray(len(values))
			for i in range(len(values)):
				if values[i] == True:
					buffer[i] = 0x01
			return self.Write(address, buffer)
		else:
			return self.Write(address,[values])
			
class MelsecMcNet(NetworkDeviceBase):
	'''三菱PLC通讯类，采用Qna兼容3E帧协议实现，需要在PLC侧先的以太网模块先进行配置，必须为二进制通讯'''
	def __init__(self,ipAddress= "127.0.0.1",port = 0):
		super().__init__()
		'''实例化一个三菱的Qna兼容3E帧协议的通讯对象'''
		self.NetworkNumber = 0
		self.NetworkStationNumber = 0
		self.iNetMessage = MelsecQnA3EBinaryMessage()
		self.byteTransform = RegularByteTransform()
		self.ipAddress = ipAddress
		self.port = port
		self.WordLength = 1
	@staticmethod
	def BuildReadCommand( address, length, isBit, networkNumber = 0, networkStationNumber = 0 ):
		'''根据类型地址长度确认需要读取的指令头'''
		analysis = MelsecHelper.McAnalysisAddress( address )
		if analysis.IsSuccess == False : return OperateResult.CreateFailedResult( analysis )

		_PLCCommand = bytearray(21)
		_PLCCommand[0]  = 0x50                                   # 副标题
		_PLCCommand[1]  = 0x00
		_PLCCommand[2]  = networkNumber                          # 网络号
		_PLCCommand[3]  = 0xFF                                   # PLC编号
		_PLCCommand[4]  = 0xFF                                   # 目标模块IO编号
		_PLCCommand[5]  = 0x03
		_PLCCommand[6]  = networkStationNumber                   # 目标模块站号
		_PLCCommand[7]  = 0x0C                                   # 请求数据长度
		_PLCCommand[8]  = 0x00
		_PLCCommand[9]  = 0x0A                                   # CPU监视定时器
		_PLCCommand[10] = 0x00
		_PLCCommand[11] = 0x01                                   # 批量读取数据命令
		_PLCCommand[12] = 0x04
		_PLCCommand[13] = 0x01 if isBit else 0x00                # 以点为单位还是字为单位成批读取
		_PLCCommand[14] = 0x00
		_PLCCommand[15] = analysis.Content2 % 256                # 起始地址的地位
		_PLCCommand[16] = analysis.Content2 // 256
		_PLCCommand[17] = 0x00
		_PLCCommand[18] = analysis.Content1.DataCode             # 指明读取的数据
		_PLCCommand[19] = length % 256                           # 软元件长度的地位
		_PLCCommand[20] = length // 256

		return OperateResult.CreateSuccessResult( _PLCCommand )
	@staticmethod
	def BuildWriteCommand( address, value, networkNumber = 0, networkStationNumber = 0 ):
		'''根据类型地址以及需要写入的数据来生成指令头'''
		analysis = MelsecHelper.McAnalysisAddress( address )
		if analysis.IsSuccess == False : return OperateResult.CreateFailedResult( analysis )
		
		length = -1
		if analysis.Content1.DataType == 1:
			# 按照位写入的操作，数据需要重新计算
			length2 =  len(value) // 2 + 1
			if len(value) % 2 == 0 : 
				length2 = len(value) // 2
			buffer = bytearray(length2)

			for i in range(length2):
				if value[i * 2 + 0] != 0x00 :
					buffer[i] += 0x10
				if (i * 2 + 1) < len(value) :
					if value[i * 2 + 1] != 0x00 :
						buffer[i] += 0x01
			length = len(value)
			value = buffer
		
		_PLCCommand = bytearray(21 + len(value))
		_PLCCommand[0]  = 0x50                                          # 副标题
		_PLCCommand[1]  = 0x00
		_PLCCommand[2]  = networkNumber                                 # 网络号
		_PLCCommand[3]  = 0xFF                                          # PLC编号
		_PLCCommand[4]  = 0xFF                                          # 目标模块IO编号
		_PLCCommand[5]  = 0x03
		_PLCCommand[6]  = networkStationNumber                          # 目标模块站号
		_PLCCommand[7]  = (len(_PLCCommand) - 9) % 256                  # 请求数据长度
		_PLCCommand[8]  = (len(_PLCCommand) - 9) // 256
		_PLCCommand[9]  = 0x0A                                          # CPU监视定时器
		_PLCCommand[10] = 0x00
		_PLCCommand[11] = 0x01                                          # 批量读取数据命令
		_PLCCommand[12] = 0x14
		_PLCCommand[13] = analysis.Content1.DataType                    # 以点为单位还是字为单位成批读取
		_PLCCommand[14] = 0x00
		_PLCCommand[15] = analysis.Content2 % 256                       # 起始地址的地位
		_PLCCommand[16] = analysis.Content2 // 256
		_PLCCommand[17] = 0x00
		_PLCCommand[18] = analysis.Content1.DataCode                    # 指明写入的数据

		# 判断是否进行位操作
		if analysis.Content1.DataType == 1:
			if length > 0:
				_PLCCommand[19] = length % 256                          # 软元件长度的地位
				_PLCCommand[20] = length // 256
			else:
				_PLCCommand[19] = len(value) * 2 % 256                  # 软元件长度的地位
				_PLCCommand[20] = len(value) * 2 // 256 
		else:
			_PLCCommand[19] = len(value) // 2 % 256                     # 软元件长度的地位
			_PLCCommand[20] = len(value) // 2 // 256
		_PLCCommand[21:] = value

		return OperateResult.CreateSuccessResult( _PLCCommand )
	@staticmethod
	def ExtractActualData( response, isBit ):
		''' 从PLC反馈的数据中提取出实际的数据内容，需要传入反馈数据，是否位读取'''
		if isBit == True:
			# 位读取
			Content = bytearray((len(response) - 11) * 2)
			i = 11
			while i < len(response):
				if (response[i] & 0x10) == 0x10:
					Content[(i - 11) * 2 + 0] = 0x01
				if (response[i] & 0x01) == 0x01:
					Content[(i - 11) * 2 + 1] = 0x01
				i = i + 1

			return OperateResult.CreateSuccessResult( Content )
		else:
			# 字读取
			Content = bytearray(len(response) - 11)
			Content[0:] = response[11:]

			return OperateResult.CreateSuccessResult( Content )
	def Read( self, address, length ):
		'''从三菱PLC中读取想要的数据，返回读取结果'''
		# 获取指令
		command = MelsecMcNet.BuildReadCommand( address, length, False, self.NetworkNumber, self.NetworkStationNumber )
		if command.IsSuccess == False :
			return OperateResult.CreateFailedResult( command )

		# 核心交互
		read = self.ReadFromCoreServer( command.Content )
		if read.IsSuccess == False : return OperateResult.CreateFailedResult( read )

		# 错误代码验证
		errorCode = read.Content[9] * 256 + read.Content[10]
		if errorCode != 0 : return OperateResult(err=errorCode, msg=StringResources.Language.MelsecPleaseReferToManulDocument)

		# 数据解析，需要传入是否使用位的参数
		return MelsecMcNet.ExtractActualData( read.Content, False )
	def ReadBool( self, address, length = None ):
		'''从三菱PLC中批量读取位软元件，返回读取结果'''
		if length == None:
			return ByteTransformHelper.GetResultFromArray( self.ReadBool( address, 1 ) )
		else:
			# 获取指令
			command = MelsecMcNet.BuildReadCommand( address, length, True, self.NetworkNumber, self.NetworkStationNumber )
			if command.IsSuccess == False : return OperateResult.CreateFailedResult( command )

			# 核心交互
			read = self.ReadFromCoreServer( command.Content )
			if read.IsSuccess == False : return OperateResult.CreateFailedResult( read )

			# 错误代码验证
			errorCode = read.Content[9] * 256 + read.Content[10]
			if errorCode != 0 : return OperateResult(err=errorCode, msg=StringResources.Language.MelsecPleaseReferToManulDocument)

			# 数据解析，需要传入是否使用位的参数
			extract =  MelsecMcNet.ExtractActualData( read.Content, True )
			if extract.IsSuccess == False : return OperateResult.CreateFailedResult( extract )

			# 转化bool数组
			content = []
			for i in range(length):
				if extract.Content[i] == 0x01:
					content.append(True)
				else:
					content.append(False)
			return OperateResult.CreateSuccessResult( content )
	def Write( self, address, value ):
		'''向PLC写入数据，数据格式为原始的字节类型'''
		# 解析指令
		command = MelsecMcNet.BuildWriteCommand( address, value, self.NetworkNumber, self.NetworkStationNumber )
		if command.IsSuccess == False : return command

		# 核心交互
		read = self.ReadFromCoreServer( command.Content )
		if read.IsSuccess == False : return read

		# 错误码校验
		errorCode = read.Content[9] * 256 + read.Content[10]
		if errorCode != 0 : return OperateResult(err=errorCode, msg=StringResources.Language.MelsecPleaseReferToManulDocument )

		# 成功
		return OperateResult.CreateSuccessResult( )
	def WriteBool( self, address, values ):
		'''向PLC中位软元件写入bool数组或是值，返回值说明，比如你写入M100,values[0]对应M100'''
		if type(values) == list:
			buffer = bytearray(len(values))
			for i in range(len(values)):
				if values[i] == True:
					buffer[i] = 0x01
			return self.Write(address, buffer)
		else:
			return self.WriteBool(address,[values])

class MelsecMcAsciiNet(NetworkDeviceBase):
	'''三菱PLC通讯类，采用Qna兼容3E帧协议实现，需要在PLC侧先的以太网模块先进行配置，必须为ASCII通讯格式'''
	def __init__(self,ipAddress= "127.0.0.1",port = 0):
		super().__init__()
		'''实例化一个三菱的Qna兼容3E帧协议的通讯对象'''
		self.NetworkNumber = 0
		self.NetworkStationNumber = 0
		self.iNetMessage = MelsecQnA3EAsciiMessage()
		self.byteTransform = RegularByteTransform()
		self.ipAddress = ipAddress
		self.port = port
		self.WordLength = 1
	@staticmethod
	def BuildReadCommand( address, length, isBit, networkNumber = 0, networkStationNumber = 0 ):
		'''根据类型地址长度确认需要读取的报文'''
		analysis = MelsecHelper.McAnalysisAddress( address )
		if analysis.IsSuccess == False : return OperateResult.CreateFailedResult( analysis )

		# 默认信息----注意：高低字节交错
		_PLCCommand = bytearray(42)
		_PLCCommand[ 0] = 0x35                                                               # 副标题
		_PLCCommand[ 1] = 0x30
		_PLCCommand[ 2] = 0x30
		_PLCCommand[ 3] = 0x30
		_PLCCommand[ 4] = MelsecHelper.BuildBytesFromData( networkNumber )[0]                # 网络号
		_PLCCommand[ 5] = MelsecHelper.BuildBytesFromData( networkNumber )[1]
		_PLCCommand[ 6] = 0x46                                                               # PLC编号
		_PLCCommand[ 7] = 0x46
		_PLCCommand[ 8] = 0x30                                                               # 目标模块IO编号
		_PLCCommand[ 9] = 0x33
		_PLCCommand[10] = 0x46
		_PLCCommand[11] = 0x46
		_PLCCommand[12] = MelsecHelper.BuildBytesFromData( networkStationNumber )[0]         # 目标模块站号
		_PLCCommand[13] = MelsecHelper.BuildBytesFromData( networkStationNumber )[1]
		_PLCCommand[14] = 0x30                                                               # 请求数据长度
		_PLCCommand[15] = 0x30
		_PLCCommand[16] = 0x31
		_PLCCommand[17] = 0x38
		_PLCCommand[18] = 0x30                                                               # CPU监视定时器
		_PLCCommand[19] = 0x30
		_PLCCommand[20] = 0x31
		_PLCCommand[21] = 0x30
		_PLCCommand[22] = 0x30                                                               # 批量读取数据命令
		_PLCCommand[23] = 0x34
		_PLCCommand[24] = 0x30
		_PLCCommand[25] = 0x31
		_PLCCommand[26] = 0x30                                                               # 以点为单位还是字为单位成批读取
		_PLCCommand[27] = 0x30
		_PLCCommand[28] = 0x30
		_PLCCommand[29] = 0x31 if isBit else 0x30
		_PLCCommand[30] = analysis.Content1.AsciiCode.encode('ascii')[0]                     # 软元件类型
		_PLCCommand[31] = analysis.Content1.AsciiCode.encode('ascii')[1]
		_PLCCommand[32:38] = MelsecHelper.BuildBytesFromAddress( analysis.Content2, analysis.Content1 )           # 起始地址的地位
		_PLCCommand[38:42] = MelsecHelper.BuildBytesFromData( length, 4 )                    # 软元件点数

		return OperateResult.CreateSuccessResult( _PLCCommand )
	@staticmethod
	def BuildWriteCommand( address, value, networkNumber = 0, networkStationNumber = 0 ):
		'''根据类型地址以及需要写入的数据来生成报文'''
		analysis = MelsecHelper.McAnalysisAddress( address )
		if analysis.IsSuccess == False : return OperateResult.CreateFailedResult( analysis )

		# 预处理指令
		if analysis.Content1.DataType == 0x01:
			# 位写入
			buffer = bytearray(len(value))
			for i in range(len(buffer)):
				buffer[i] = 0x30 if value[i] == 0x00 else 0x31
			value = buffer
		else:
			# 字写入
			buffer = bytearray(len(value) * 2)
			for i in range(len(value) // 2):
				tmp = value[i*2]+ value[i*2+1]*256
				buffer[4*i:4*i+4] = MelsecHelper.BuildBytesFromData( tmp, 4 )
			value = buffer

		# 默认信息----注意：高低字节交错

		_PLCCommand = bytearray(42 + len(value))

		_PLCCommand[ 0] = 0x35                                                                              # 副标题
		_PLCCommand[ 1] = 0x30
		_PLCCommand[ 2] = 0x30
		_PLCCommand[ 3] = 0x30
		_PLCCommand[ 4] = MelsecHelper.BuildBytesFromData( networkNumber )[0]                               # 网络号
		_PLCCommand[ 5] = MelsecHelper.BuildBytesFromData( networkNumber )[1]
		_PLCCommand[ 6] = 0x46                                                                              # PLC编号
		_PLCCommand[ 7] = 0x46
		_PLCCommand[ 8] = 0x30                                                                              # 目标模块IO编号
		_PLCCommand[ 9] = 0x33
		_PLCCommand[10] = 0x46
		_PLCCommand[11] = 0x46
		_PLCCommand[12] = MelsecHelper.BuildBytesFromData( networkStationNumber )[0]                        # 目标模块站号
		_PLCCommand[13] = MelsecHelper.BuildBytesFromData( networkStationNumber )[1]
		_PLCCommand[14] = MelsecHelper.BuildBytesFromData( len(_PLCCommand) - 18, 4 )[0]           # 请求数据长度
		_PLCCommand[15] = MelsecHelper.BuildBytesFromData( len(_PLCCommand) - 18, 4 )[1]
		_PLCCommand[16] = MelsecHelper.BuildBytesFromData( len(_PLCCommand) - 18, 4 )[2]
		_PLCCommand[17] = MelsecHelper.BuildBytesFromData( len(_PLCCommand) - 18, 4 )[3]
		_PLCCommand[18] = 0x30                                                                              # CPU监视定时器
		_PLCCommand[19] = 0x30
		_PLCCommand[20] = 0x31
		_PLCCommand[21] = 0x30
		_PLCCommand[22] = 0x31                                                                              # 批量写入的命令
		_PLCCommand[23] = 0x34
		_PLCCommand[24] = 0x30
		_PLCCommand[25] = 0x31
		_PLCCommand[26] = 0x30                                                                              # 子命令
		_PLCCommand[27] = 0x30
		_PLCCommand[28] = 0x30
		_PLCCommand[29] = 0x30 if analysis.Content1.DataType == 0 else 0x31
		_PLCCommand[30] = analysis.Content1.AsciiCode.encode('ascii')[0]                         # 软元件类型
		_PLCCommand[31] = analysis.Content1.AsciiCode.encode('ascii')[1]
		_PLCCommand[32] = MelsecHelper.BuildBytesFromAddress( analysis.Content2, analysis.Content1 )[0]     # 起始地址的地位
		_PLCCommand[33] = MelsecHelper.BuildBytesFromAddress( analysis.Content2, analysis.Content1 )[1]
		_PLCCommand[34] = MelsecHelper.BuildBytesFromAddress( analysis.Content2, analysis.Content1 )[2]
		_PLCCommand[35] = MelsecHelper.BuildBytesFromAddress( analysis.Content2, analysis.Content1 )[3]
		_PLCCommand[36] = MelsecHelper.BuildBytesFromAddress( analysis.Content2, analysis.Content1 )[4]
		_PLCCommand[37] = MelsecHelper.BuildBytesFromAddress( analysis.Content2, analysis.Content1 )[5]

		# 判断是否进行位操作
		if (analysis.Content1.DataType == 1):
			_PLCCommand[38] = MelsecHelper.BuildBytesFromData( len(value), 4 )[0]                    # 软元件点数
			_PLCCommand[39] = MelsecHelper.BuildBytesFromData( len(value), 4 )[1]
			_PLCCommand[40] = MelsecHelper.BuildBytesFromData( len(value), 4 )[2]
			_PLCCommand[41] = MelsecHelper.BuildBytesFromData( len(value), 4 )[3]
		else:
			_PLCCommand[38] = MelsecHelper.BuildBytesFromData( len(value) // 4, 4 )[0]              # 软元件点数
			_PLCCommand[39] = MelsecHelper.BuildBytesFromData( len(value) // 4, 4 )[1]
			_PLCCommand[40] = MelsecHelper.BuildBytesFromData( len(value) // 4, 4 )[2]
			_PLCCommand[41] = MelsecHelper.BuildBytesFromData( len(value) // 4, 4 )[3]
		_PLCCommand[42:] = value

		return OperateResult.CreateSuccessResult( _PLCCommand )

	@staticmethod
	def ExtractActualData( response, isBit ):
		'''从PLC反馈的数据中提取出实际的数据内容，需要传入反馈数据，是否位读取'''
		if isBit == True:
			# 位读取
			Content = bytearray(len(response) - 22)
			for i in range(22,len(response)):
				Content[i - 22] = 0x00 if response[i] == 0x30 else 0x01

			return OperateResult.CreateSuccessResult( Content )
		else:
			# 字读取
			Content = bytearray((len(response) - 22) // 2)
			for i in range(len(Content)//2):
				tmp = int(response[i * 4 + 22:i * 4 + 26].decode('ascii'),16)
				Content[i * 2:i * 2+2] = struct.pack('<H',tmp)

			return OperateResult.CreateSuccessResult( Content )

	def Read( self, address, length ):
		'''从三菱PLC中读取想要的数据，返回读取结果'''
		# 获取指令
		command = MelsecMcAsciiNet.BuildReadCommand( address, length, False, self.NetworkNumber, self.NetworkStationNumber )
		if command.IsSuccess == False : return OperateResult.CreateFailedResult( command )

		# 核心交互
		read = self.ReadFromCoreServer( command.Content )
		if read.IsSuccess == False : return OperateResult.CreateFailedResult( read )

		# 错误代码验证
		errorCode = int( read.Content[18:22].decode('ascii'), 16 )
		if errorCode != 0 : return OperateResult( err= errorCode, msg = StringResources.Language.MelsecPleaseReferToManulDocument )

		# 数据解析，需要传入是否使用位的参数
		return MelsecMcAsciiNet.ExtractActualData( read.Content, False )
	def ReadBool( self, address, length = None ):
		if length == None:
			return ByteTransformHelper.GetResultFromArray( self.ReadBool( address, 1 ) )
		else:
			# 获取指令
			command = MelsecMcAsciiNet.BuildReadCommand( address, length, True, self.NetworkNumber, self.NetworkStationNumber )
			if command.IsSuccess == False : return OperateResult.CreateFailedResult( command )
			
			# 核心交互
			read = self.ReadFromCoreServer( command.Content )
			if read.IsSuccess == False : return OperateResult.CreateFailedResult( read )

			# 错误代码验证
			errorCode = int( read.Content[18:22].decode('ascii'), 16 )
			if errorCode != 0 : return OperateResult( err= errorCode, msg = StringResources.Language.MelsecPleaseReferToManulDocument )
				
			# 数据解析，需要传入是否使用位的参数
			extract =  MelsecMcAsciiNet.ExtractActualData( read.Content, True )
			if extract.IsSuccess == False : return OperateResult.CreateFailedResult( extract )

			# 转化bool数组
			content = []
			for i in range(length):
				if extract.Content[i] == 0x01:
					content.append(True)
				else:
					content.append(False)
			return OperateResult.CreateSuccessResult( content )

	def Write( self, address, value ):
		'''向PLC写入数据，数据格式为原始的字节类型'''
		# 解析指令
		command = MelsecMcAsciiNet.BuildWriteCommand( address, value, self.NetworkNumber, self.NetworkStationNumber )
		if command.IsSuccess == False : return command

		# 核心交互
		read = self.ReadFromCoreServer( command.Content )
		if read.IsSuccess == False : return read

		# 错误码验证
		errorCode = int( read.Content[18:22].decode('ascii'), 16 )
		if errorCode != 0 : return OperateResult( err = errorCode, msg = StringResources.Language.MelsecPleaseReferToManulDocument )

		# 写入成功
		return OperateResult.CreateSuccessResult( )
	def WriteBool( self, address, values ):
		'''向PLC中位软元件写入bool数组，返回值说明，比如你写入M100,values[0]对应M100'''
		if type(values) == list:
			buffer = bytearray(len(values))
			for i in range(len(buffer)):
				buffer[i] = 0x01 if values[i] == True else 0x00
			return self.Write( address, buffer )
		else:
			return self.WriteBool( address, [values] )


class MelsecA1EBinaryMessage(INetMessage):
	'''三菱的A兼容1E帧协议解析规则'''
	def	ProtocolHeadBytesLength(self):
		'''协议头数据长度，也即是第一次接收的数据长度'''
		return 2
	def	GetContentLengthByHeadBytes(self):
		'''二次接收的数据长度'''
		contentLength = 0
		if self.HeadBytes[1] == 0x5B:
			contentLength = 2
		else:
			length = 0
			if self.SendBytes[10] % 2 == 0:
				length = self.SendBytes[10]
			else:
				length = self.SendBytes[10] + 1

			if self.HeadBytes[0] == 0x80:
				contentLength = int(length / 2)
			elif self.HeadBytes[0] == 0x81:
				contentLength = self.SendBytes[10] * 2
			elif self.HeadBytes[0] == 0x82:
				contentLength = 0
			elif self.HeadBytes[0] == 0x83:
				contentLength = 0
			# 在A兼容1E协议中，写入值后，若不发生异常，只返回副标题 + 结束代码(0x00)
			# 这已经在协议头部读取过了，后面要读取的长度为0（contentLength=0）
		return contentLength
	def	CheckHeadBytesLegal(self,token):
		'''令牌检查是否成功'''
		if self.HeadBytes != None:
			if self.HeadBytes[0] - self.SendBytes[0] == 0x80:
				return True
			else:
				return False
		else:
			return False

class MelsecQnA3EBinaryMessage(INetMessage):
	'''三菱的Qna兼容3E帧协议解析规则'''
	def ProtocolHeadBytesLength(self):
		'''协议头数据长度，也即是第一次接收的数据长度'''
		return 9
	def GetContentLengthByHeadBytes(self):
		'''二次接收的数据长度'''
		if self.HeadBytes != None:
			return self.HeadBytes[8] * 256 + self.HeadBytes[7]
		else:
			return 0
	def CheckHeadBytesLegal(self,token):
		'''令牌检查是否成功'''
		if self.HeadBytes != None:
			if self.HeadBytes[0] == 0xD0 and self.HeadBytes[1] == 0x00:
				return True
			else:
				return False
		else:
			return False

class MelsecQnA3EAsciiMessage(INetMessage):
	'''三菱的Qna兼容3E帧的ASCII协议解析规则'''
	def ProtocolHeadBytesLength(self):
		'''协议头数据长度，也即是第一次接收的数据长度'''
		return 18
	def GetContentLengthByHeadBytes(self):
		'''二次接收的数据长度'''
		if self.HeadBytes != None:
			return int(self.HeadBytes[14:18].decode('ascii'),16)
		else:
			return 0
	def CheckHeadBytesLegal(self,token):
		'''令牌检查是否成功'''
		if self.HeadBytes != None:
			if self.HeadBytes[0] == ord('D') and self.HeadBytes[1] == ord('0') and self.HeadBytes[2] == ord('0') and self.HeadBytes[3] == ord('0'):
				return True
			else:
				return False
		else:
			return False
