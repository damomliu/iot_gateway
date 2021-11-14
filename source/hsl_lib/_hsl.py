import struct
from .BasicFramework import SoftBasic, SoftZipped
from .Language import DefaultLanguage

class HslProtocol:
	'''用于本程序集访问通信的暗号说明'''
	@staticmethod
	def HeadByteLength():
		'''规定所有的网络传输指令头都为32字节'''
		return 32
	@staticmethod
	def ProtocolBufferSize():
		'''所有网络通信中的缓冲池数据信息'''
		return 1024
	@staticmethod
	def ProtocolCheckSecends():
		'''用于心跳程序的暗号信息'''
		return 1
	@staticmethod
	def ProtocolClientQuit():
		'''客户端退出消息'''
		return 2
	@staticmethod
	def ProtocolClientRefuseLogin():
		'''因为客户端达到上限而拒绝登录'''
		return 3
	@staticmethod
	def ProtocolClientAllowLogin():
		'''允许客户端登录到服务器'''
		return 4
	@staticmethod
	def ProtocolAccountLogin():
		'''客户端登录的暗号信息'''
		return 5
	@staticmethod
	def ProtocolAccountRejectLogin():
		'''客户端登录的暗号信息'''
		return 6
	@staticmethod
	def ProtocolUserString():
		'''说明发送的只是文本信息'''
		return 1001
	@staticmethod
	def ProtocolUserBytes():
		'''发送的数据就是普通的字节数组'''
		return 1002
	@staticmethod
	def ProtocolUserBitmap():
		'''发送的数据就是普通的图片数据'''
		return 1003
	@staticmethod
	def ProtocolUserException():
		'''发送的数据是一条异常的数据，字符串为异常消息'''
		return 1004
	@staticmethod
	def ProtocolUserStringArray():
		'''说明发送的数据是字符串的数组'''
		return 1005
	@staticmethod
	def ProtocolFileDownload():
		'''请求文件下载的暗号'''
		return 2001
	@staticmethod
	def ProtocolFileUpload():
		'''请求文件上传的暗号'''
		return 2002
	@staticmethod
	def ProtocolFileDelete():
		'''请求删除文件的暗号'''
		return 2003
	@staticmethod
	def ProtocolFileCheckRight():
		'''文件校验成功'''
		return 2004
	@staticmethod
	def ProtocolFileCheckError():
		'''文件校验失败'''
		return 2005
	@staticmethod
	def ProtocolFileSaveError():
		'''文件保存失败'''
		return 2006
	@staticmethod
	def ProtocolFileDirectoryFiles():
		'''请求文件列表的暗号'''
		return 2007
	@staticmethod
	def ProtocolFileDirectories():
		'''请求子文件的列表暗号'''
		return 2008
	@staticmethod
	def ProtocolProgressReport():
		'''进度返回暗号'''
		return 2009
	@staticmethod
	def ProtocolNoZipped():
		'''不压缩数据字节'''
		return 3001
	@staticmethod
	def ProtocolZipped():
		'''压缩数据字节'''
		return 3002
	@staticmethod
	def CommandBytesBase( command, customer, token, data ):
		'''生成终极传送指令的方法，所有的数据均通过该方法出来'''
		_zipped = HslProtocol.ProtocolNoZipped()
		buffer = None
		_sendLength = 0
		if data == None:
			buffer = bytearray(HslProtocol.HeadByteLength())
		else:
			data = HslSecurity.ByteEncrypt( data )
			if len(data) > 102400:
				data = SoftZipped.CompressBytes( data )
				_zipped = HslProtocol.ProtocolZipped()
			buffer = bytearray( HslProtocol.HeadByteLength() + len(data) )
			_sendLength = len(data)
		
		buffer[0:4] = struct.pack( '<i', command )
		buffer[4:8] = struct.pack( '<i', customer )
		buffer[8:12] = struct.pack( '<i', _zipped)
		buffer[12:28] = SoftBasic.TokenToBytes(token)
		buffer[28:32] = struct.pack( '<i', _sendLength)
		if _sendLength>0:
			buffer[32:_sendLength+32]=data
		return buffer
	@staticmethod
	def CommandAnalysis( head, content ):
		'''解析接收到数据，先解压缩后进行解密'''
		if content != None:
			_zipped = struct.unpack('<i', head[8:12])[0]
			if _zipped == HslProtocol.ProtocolZipped():
				content = SoftZipped.Decompress( content )
			return HslSecurity.ByteEncrypt(content)
		return bytearray(0)
	@staticmethod
	def CommandBytes( customer, token, data ):
		'''获取发送字节数据的实际数据，带指令头'''
		return HslProtocol.CommandBytesBase( HslProtocol.ProtocolUserBytes(), customer, token, data )
	@staticmethod
	def CommandString( customer, token, data ):
		'''获取发送字节数据的实际数据，带指令头'''
		if data == None: 
			return HslProtocol.CommandBytesBase( HslProtocol.ProtocolUserString(), customer, token, None )
		else:
			buffer = SoftBasic.StringToUnicodeBytes(data)
			return HslProtocol.CommandBytesBase( HslProtocol.ProtocolUserString(), customer, token, buffer )
	@staticmethod
	def PackStringArrayToByte( data ):
		'''将字符串打包成字节数组内容'''
		if data == None: return bytearray(0)

		buffer = bytearray(0)
		buffer.extend( struct.pack('<i', len(data)))

		for i in range(len(data)):
			if data[i] == None or data[i] == "":
				buffer.extend( struct.pack('<i', 0))
			else:
				tmp = SoftBasic.StringToUnicodeBytes(data[i])
				buffer.extend( struct.pack('<i', len(tmp)))
				buffer.extend( tmp )
		return buffer
	@staticmethod
	def UnPackStringArrayFromByte( content ):
		'''将字节数组还原成真实的字符串数组'''
		if content == None or len(content) < 4:
			return None
		index = 0
		count = struct.unpack('<i', content[ index : index + 4])[0]
		result = []
		index = index + 4
		for i in range(count):
			length = struct.unpack('<i', content[ index : index + 4])[0]
			index = index + 4
			if length > 0:
				result.append( content[ index : index + length ].decode('utf-16') )
			else:
				result.append( "" )
			index = index + length
		return result


class HslSecurity:
	@staticmethod
	def ByteEncrypt( enBytes ):
		'''加密方法，只对当前的程序集开放'''
		if (enBytes == None) : return None
		result = bytearray(len(enBytes))
		for i in range(len(enBytes)):
			result[i] = enBytes[i] ^ 0xB5
		return result
	@staticmethod
	def ByteDecrypt( deBytes ):
		'''解密方法，只对当前的程序集开放'''
		return HslSecurity.ByteEncrypt(deBytes)


class StringResources:
	'''系统的资源类，System String Resouces'''
	Language = DefaultLanguage()


class OperateResult:
	'''结果对象类，可以携带额外的数据信息'''
	def __init__(self, err = 0, msg = ""):
		'''
		实例化一个IsSuccess为False的默认对象，可以指定错误码和错误信息 -> OperateResult

		Parameter
		  err: int 错误码
		  msg: str 错误信息
		Return
		  OperateResult: 结果对象
		'''
		self.ErrorCode = err
		self.Message = msg
		self.IsSuccess = False
	# 是否成功的标志
	IsSuccess = False
	# 操作返回的错误消息
	Message = StringResources.Language.UnknownError
	# 错误码
	ErrorCode = 10000
	# 返回显示的文本
	def ToMessageShowString( self ):
		'''获取错误代号及文本描述'''
		return StringResources.Language.ErrorCode + ":" + str(self.ErrorCode) + "\r\n" + StringResources.Language.TextDescription + ":" + self.Message
	def CopyErrorFromOther(self, result):
		'''从另一个结果类中拷贝错误信息'''
		if result != None:
			self.ErrorCode = result.ErrorCode
			self.Message = result.Message
	@staticmethod
	def CreateFailedResult( result ):
		'''
		创建一个失败的结果对象，将会复制拷贝result的值 -> OperateResult

		Parameter
		  result: OperateResult 继承自该类型的其他任何数据对象
		Return
		  OperateResult: 新的一个IsSuccess为False的对象
		'''
		failed = OperateResult()
		if result != None:
			failed.ErrorCode = result.ErrorCode
			failed.Message = result.Message
		return failed
	@staticmethod
	def CreateSuccessResult( Content1 = None, Content2 = None, Content3 = None, Content4 = None, Content5 = None, Content6 = None, Content7 = None, Content8 = None, Content9 = None, Content10 = None):
		'''
		创建一个成功的对象

		可以指定内容信息，当然也可以不去指定，就是单纯的一个成功的对象
		'''
		success = OperateResult()
		success.IsSuccess = True
		success.Message = StringResources.Language.SuccessText
		if(Content2 == None and Content3 == None and Content4 == None and Content5 == None and Content6 == None and Content7 == None and Content8 == None and Content9 == None and Content10 == None) :
			success.Content = Content1
		else:
			success.Content1 = Content1
			success.Content2 = Content2
			success.Content3 = Content3
			success.Content4 = Content4
			success.Content5 = Content5
			success.Content6 = Content6
			success.Content7 = Content7
			success.Content8 = Content8
			success.Content9 = Content9
			success.Content10 = Content10
		return success
