import datetime
import socket
import threading
import uuid
import struct

from .. import SoftBasic, OperateResult, StringResources, HslProtocol
from . import ByteTransform, ByteTransformHelper
from . import INetMessage

class AppSession:
	'''网络会话信息'''
	def __init__( self ):
		self.ClientUniqueID = SoftBasic.GetUniqueStringByGuidAndRandom()
		self.HeartTime = datetime.datetime.now()
		self.IpAddress = "127.0.0.1"
		self.Port = 12345
		self.LoginAlias = ""
		self.ClientType = ""
		self.BytesHead = bytearray(32)
		self.BytesContent = bytearray(0)
		self.KeyGroup = ""
		self.WorkSocket = socket.socket()
		self.HybirdLockSend = threading.Lock()
	def Clear( self ):
		self.BytesHead = bytearray(HslProtocol.HeadByteLength())
		self.BytesContent = None


class NetworkBase:
	'''网络基础类的核心'''
	def __init__(self):
		'''初始化方法'''
		super().__init__()
		self.Token = uuid.UUID('{00000000-0000-0000-0000-000000000000}')
		self.CoreSocket = None
	def Receive(self,socket,length):
		'''接收固定长度的字节数组'''
		totle = 0
		data = bytearray()
		try:
			while totle < length:
				data.extend( socket.recv( length-totle ))
				totle = len(data)
			return OperateResult.CreateSuccessResult(data)
		except Exception as e:
			result = OperateResult()
			result.Message = str(e)
			return result
	def Send(self,socket,data):
		'''发送消息给套接字，直到完成的时候返回'''
		try:
			socket.sendall(data)
			return OperateResult.CreateSuccessResult()
		except Exception as e:
			return OperateResult( msg = str(e))

	def CreateSocketAndConnect(self,ipAddress,port,timeout = 10000):
		'''创建一个新的socket对象并连接到远程的地址，默认超时时间为10秒钟'''
		try:
			socketTmp = socket.socket()
			socketTmp.connect((ipAddress,port))
			return OperateResult.CreateSuccessResult(socketTmp)
		except Exception as e:
			return OperateResult( msg = str(e))
	def ReceiveMessage( self, socket, timeOut, netMsg ):
		'''接收一条完整的数据，使用异步接收完成，包含了指令头信息'''
		result = OperateResult()
		headResult = self.Receive( socket, netMsg.ProtocolHeadBytesLength() )
		if headResult.IsSuccess == False:
			result.CopyErrorFromOther(headResult)
			return result
		netMsg.HeadBytes = headResult.Content
		if netMsg.CheckHeadBytesLegal( SoftBasic.TokenToBytes(self.Token) ) == False:
			# 令牌校验失败
			if socket != None: socket.close()
			result.Message = StringResources.Language.TokenCheckFailed
			return result

		contentLength = netMsg.GetContentLengthByHeadBytes( )
		if contentLength == 0:
			netMsg.ContentBytes = bytearray(0)
		else:
			contentResult = self.Receive( socket, contentLength )
			if contentResult.IsSuccess == False:
				result.CopyErrorFromOther( contentResult )
				return result
			netMsg.ContentBytes = contentResult.Content
		
		if netMsg.ContentBytes == None: netMsg.ContentBytes = bytearray(0)
		result.Content = netMsg
		result.IsSuccess = True
		return result
	def CloseSocket(self, socket):
		'''关闭网络'''
		if socket != None:
			socket.close()
	def CheckRemoteToken( self, headBytes ):
		'''检查当前的头子节信息的令牌是否是正确的'''
		return SoftBasic.IsTwoBytesEquel( headBytes,12, SoftBasic.TokenToBytes(self.Token), 0, 16 )
	def SendBaseAndCheckReceive( self, socket, headcode, customer, send ):
		'''[自校验] 发送字节数据并确认对方接收完成数据，如果结果异常，则结束通讯'''
		# 数据处理
		send = HslProtocol.CommandBytesBase( headcode, customer, self.Token, send )

		sendResult = self.Send( socket, send )
		if sendResult.IsSuccess == False:  return sendResult

		# 检查对方接收完成
		checkResult = self.ReceiveLong( socket )
		if checkResult.IsSuccess == False: return checkResult

		# 检查长度接收
		if checkResult.Content != len(send):
			self.CloseSocket(socket)
			return OperateResult( msg = "接收的数据数据长度验证失败")

		return checkResult
	def SendBytesAndCheckReceive( self, socket, customer, send ):
		'''[自校验] 发送字节数据并确认对方接收完成数据，如果结果异常，则结束通讯'''
		return self.SendBaseAndCheckReceive( socket, HslProtocol.ProtocolUserBytes(), customer, send )
	def SendStringAndCheckReceive( self, socket, customer, send ):
		'''[自校验] 直接发送字符串数据并确认对方接收完成数据，如果结果异常，则结束通讯'''
		data = SoftBasic.StringToUnicodeBytes(send)

		return self.SendBaseAndCheckReceive( socket, HslProtocol.ProtocolUserString(), customer, data )
	def ReceiveAndCheckBytes( self, socket, timeout ):
		'''[自校验] 接收一条完整的同步数据，包含头子节和内容字节，基础的数据，如果结果异常，则结束通讯'''
		# 30秒超时接收验证
		# if (timeout > 0) ThreadPool.QueueUserWorkItem( new WaitCallback( ThreadPoolCheckTimeOut ), hslTimeOut );

		# 接收头指令
		headResult = self.Receive(socket, HslProtocol.HeadByteLength())
		if headResult.IsSuccess == False:
			return OperateResult.CreateFailedResult(headResult)

		# 检查令牌
		if self.CheckRemoteToken(headResult.Content) == False:
			self.CloseSocket(socket)
			return OperateResult( msg = StringResources.Language.TokenCheckFailed )

		contentLength = struct.unpack( '<i', headResult.Content[(HslProtocol.HeadByteLength() - 4):])[0]
		# 接收内容
		contentResult = self.Receive(socket, contentLength)
		if contentResult.IsSuccess == False:
			return OperateResult.CreateFailedResult( contentResult )

		# 返回成功信息
		checkResult = self.SendLong(socket, HslProtocol.HeadByteLength() + contentLength)
		if checkResult.IsSuccess == False:
			return OperateResult.CreateFailedResult( checkResult )

		head = headResult.Content
		content = contentResult.Content
		content = HslProtocol.CommandAnalysis(head, content)
		return OperateResult.CreateSuccessResult(head, content)
	def ReceiveStringContentFromSocket( self, socket ):
		'''[自校验] 从网络中接收一个字符串数据，如果结果异常，则结束通讯'''
		receive = self.ReceiveAndCheckBytes(socket, 10000)
		if receive.IsSuccess == False: return OperateResult.CreateFailedResult(receive)

		# 检查是否是字符串信息
		if struct.unpack('<i',receive.Content1[0:4])[0] != HslProtocol.ProtocolUserString():
			self.CloseSocket(socket)
			return OperateResult( msg = "ReceiveStringContentFromSocket异常" )

		if receive.Content2 == None: receive.Content2 = bytearray(0)
		# 分析数据
		return OperateResult.CreateSuccessResult(struct.unpack('<i', receive.Content1[4:8])[0], receive.Content2.decode('utf-16'))
	def ReceiveBytesContentFromSocket( self, socket ):
		'''[自校验] 从网络中接收一串字节数据，如果结果异常，则结束通讯'''
		receive = self.ReceiveAndCheckBytes( socket, 10000 )
		if receive.IsSuccess == False: return OperateResult.CreateFailedResult(receive)

		# 检查是否是字节信息
		if struct.unpack('<i', receive.Content1[0:4])[0] != HslProtocol.ProtocolUserBytes():
			self.CloseSocket(socket)
			return OperateResult( msg = "字节内容检查失败" )
		
		# 分析数据
		return OperateResult.CreateSuccessResult( struct.unpack('<i', receive.Content1[4:8])[0], receive.Content2 )
	def ReceiveLong( self, socket ):
		'''从网络中接收Long数据'''
		read = self.Receive(socket, 8)
		if read.IsSuccess == False: return OperateResult.CreateFailedResult(read)

		return OperateResult.CreateSuccessResult(struct.unpack('<Q', read.Content)[0])
	def SendLong( self, socket, value ):
		'''将Long数据发送到套接字'''
		return self.Send( socket, struct.pack( '<Q', value ) )
	def SendAccountAndCheckReceive( self, socket, customer, name, pwd ):
		'''[自校验] 直接发送字符串数组并确认对方接收完成数据，如果结果异常，则结束通讯'''
		return self.SendBaseAndCheckReceive( socket, HslProtocol.ProtocolAccountLogin(), customer, HslProtocol.PackStringArrayToByte([name, pwd]) )
	def ReceiveStringArrayContentFromSocket( self, socket ):
		''''''
		receive = self.ReceiveAndCheckBytes( socket, 30000 )
		if receive.IsSuccess == False : return receive

		# 检查是否是字符串信息
		if struct.unpack( '<i', receive.Content1[0 : 4])[0] != HslProtocol.ProtocolUserStringArray():
			self.CloseSocket(socket)
			return OperateResult(msg=StringResources.Language.CommandHeadCodeCheckFailed)

		if receive.Content2 == None : receive.Content2 = bytearray(4)
		return OperateResult.CreateSuccessResult( struct.unpack('<i', receive.Content1[4:8])[0], HslProtocol.UnPackStringArrayFromByte(receive.Content2) )


class NetworkDoubleBase(NetworkBase):
	'''支持长连接，短连接两个模式的通用客户端基类'''
	def __init__(self):
		super().__init__()
		self.byteTransform = ByteTransform()
		self.ipAddress = "127.0.0.1"
		self.port = 10000
		self.isPersistentConn = False
		self.isSocketError = False
		self.receiveTimeOut = 10000
		self.isUseSpecifiedSocket = False
		self.interactiveLock = threading.Lock()
		self.iNetMessage = INetMessage()
		self.isUseAccountCertificate = False
		self.userName = ""
		self.password = ""
	
	def SetPersistentConnection( self ):
		'''在读取数据之前可以调用本方法将客户端设置为长连接模式，相当于跳过了ConnectServer的结果验证，对异形客户端无效'''
		self.isPersistentConn = True
	def ConnectServer( self ):
		'''切换短连接模式到长连接模式，后面的每次请求都共享一个通道'''
		self.isPersistentConn = True
		result = OperateResult( )
		# 重新连接之前，先将旧的数据进行清空
		if self.CoreSocket != None: 
			self.CoreSocket.close()

		rSocket = self.CreateSocketAndInitialication( )
		if rSocket.IsSuccess == False:
			self.isSocketError = True
			rSocket.Content = None
			result.Message = rSocket.Message
		else:
			self.CoreSocket = rSocket.Content
			result.IsSuccess = True
		return result
	def ConnectClose( self ):
		'''在长连接模式下，断开服务器的连接，并切换到短连接模式'''
		result = OperateResult( )
		self.isPersistentConn = False

		self.interactiveLock.acquire()
		# 额外操作
		result = self.ExtraOnDisconnect( self.CoreSocket )
		# 关闭信息
		if self.CoreSocket != None : self.CoreSocket.close()
		self.CoreSocket = None
		self.interactiveLock.release( )
		return result
	

	# 初始化的信息方法和连接结束的信息方法，需要在继承类里面进行重新实现
	def InitializationOnConnect( self, socket ):
		'''连接上服务器后需要进行的初始化操作'''
		return OperateResult.CreateSuccessResult()
	def ExtraOnDisconnect( self, socket ):
		'''在将要和服务器进行断开的情况下额外的操作，需要根据对应协议进行重写'''
		return OperateResult.CreateSuccessResult()
	
	def GetAvailableSocket( self ):
		'''获取本次操作的可用的网络套接字'''
		if self.isPersistentConn :
			# 如果是异形模式
			if self.isUseSpecifiedSocket :
				if self.isSocketError:
					return OperateResult( msg = StringResources.Language.ConnectionIsNotAvailable )
				else:
					return OperateResult.CreateSuccessResult( self.CoreSocket )
			else:
				# 长连接模式
				if self.isSocketError or self.CoreSocket == None :
					connect = self.ConnectServer( )
					if connect.IsSuccess == False:
						self.isSocketError = True
						return OperateResult( msg = connect.Message )
					else:
						self.isSocketError = False
						return OperateResult.CreateSuccessResult( self.CoreSocket )
				else:
					return OperateResult.CreateSuccessResult( self.CoreSocket )
		else:
			# 短连接模式
			return self.CreateSocketAndInitialication( )

	def CreateSocketAndInitialication( self ):
		'''连接并初始化网络套接字'''
		result = self.CreateSocketAndConnect( self.ipAddress, self.port, 10000 )
		if result.IsSuccess:
			# 初始化
			initi = self.InitializationOnConnect( result.Content )
			if initi.IsSuccess == False:
				if result.Content != None : result.Content.close( )
				result.IsSuccess = initi.IsSuccess
				result.CopyErrorFromOther( initi )
		return result

	def ReadFromCoreSocketServer( self, socket, send ):
		'''在其他指定的套接字上，使用报文来通讯，传入需要发送的消息，返回一条完整的数据指令'''
		read = self.ReadFromCoreServerBase( socket, send )
		if read.IsSuccess == False: return OperateResult.CreateFailedResult( read )

		# 拼接结果数据
		Content = bytearray(len(read.Content1) + len(read.Content2))
		if len(read.Content1) > 0 : 
			Content[0:len(read.Content1)] = read.Content1
		if len(read.Content2) > 0 : 
			Content[len(read.Content1):len(Content)] = read.Content2
		return OperateResult.CreateSuccessResult( Content )

	def ReadFromCoreServer( self, send ):
		'''使用底层的数据报文来通讯，传入需要发送的消息，返回一条完整的数据指令'''
		result = OperateResult( )
		self.interactiveLock.acquire()
		# 获取有用的网络通道，如果没有，就建立新的连接
		resultSocket = self.GetAvailableSocket( )
		if resultSocket.IsSuccess == False:
			self.isSocketError = True
			self.interactiveLock.release()
			result.CopyErrorFromOther( resultSocket )
			return result

		read = self.ReadFromCoreSocketServer( resultSocket.Content, send )
		if read.IsSuccess :
			self.isSocketError = False
			result.IsSuccess = read.IsSuccess
			result.Content = read.Content
			result.Message = StringResources.Language.SuccessText
			# string tmp2 = BasicFramework.SoftBasic.ByteToHexString( result.Content, '-' )
		else:
			self.isSocketError = True
			result.CopyErrorFromOther( read )

		self.interactiveLock.release()
		if self.isPersistentConn==False:
			if resultSocket.Content != None:
				resultSocket.Content.close()
		return result
		
	def ReadFromCoreServerBase( self, socket, send ):
		'''使用底层的数据报文来通讯，传入需要发送的消息，返回最终的数据结果，被拆分成了头子节和内容字节信息'''
		self.iNetMessage.SendBytes = send
		sendResult = self.Send( socket, send )
		if sendResult.IsSuccess == False:
			if socket!= None : socket.close( )
			return OperateResult.CreateFailedResult( sendResult )

		# 接收超时时间大于0时才允许接收远程的数据
		if (self.receiveTimeOut >= 0):
			# 接收数据信息
			resultReceive = self.ReceiveMessage(socket, 10000, self.iNetMessage)
			if resultReceive.IsSuccess == False:
				socket.close( )
				return OperateResult( msg = "Receive data timeout: " + str(self.receiveTimeOut ) + " Msg:"+ resultReceive.Message)
			return OperateResult.CreateSuccessResult( resultReceive.Content.HeadBytes, resultReceive.Content.ContentBytes )
		else:
			return OperateResult.CreateSuccessResult( bytearray(0), bytearray(0) )
	
	def SetLoginAccount( self, name, pwd ):
		'''设置当前的登录的账户名和密码信息，账户名为空时设置不生效'''
		if name == None or name == "":
			self.isUseAccountCertificate = False
		else:
			self.isUseAccountCertificate = True
			self.userName = name
			self.password = pwd

	def AccountCertificate( self, socket ):
		'''认证账号，将使用已经设置的用户名和密码进行账号认证。'''
		send = self.SendAccountAndCheckReceive( socket, 1, self.userName, self.password )
		if send.IsSuccess == False : return send

		read = self.ReceiveStringArrayContentFromSocket( socket )
		if read.IsSuccess == False : return read

		if read.Content1 == 0 : return OperateResult( msg = read.Content2[0] )
		return OperateResult.CreateSuccessResult( )


class NetworkDeviceBase(NetworkDoubleBase):
	'''设备类的基类，提供了基础的字节读写方法'''
	def __init__(self):
		super().__init__()
		# 单个数据字节的长度，西门子为2，三菱，欧姆龙，modbusTcp就为1
		self.WordLength = 1
		
	def Read( self, address, length ):
		'''从设备读取原始数据
		
		Parameter
		  address: str 设备的地址，具体需要看设备自身的支持
		  length: int 读取的地址长度，至于每个地址占一个字节还是两个字节，取决于具体的设备
		Return
		  OperateResult<bytearray>: 带数据的结果类对象
		'''
		return OperateResult( )
	def Write( self, address, value ):
		'''将原始数据写入设备
		
		Parameter
		  address: str 设备的地址，具体需要看设备自身的支持
		  value: bytearray 原始数据
		Return
		  OperateResult: 带有成功标识的结果对象
		'''
		return OperateResult()
	def ReadBool( self, address, length = None ):
		'''读取设备的bool类型的数据'''
		if length == None:
			return ByteTransformHelper.GetResultFromArray( self.ReadBool(address, 1) )
		else:
			OperateResult(StringResources.Language.NotSupportedFunction)
	def ReadInt16( self, address, length = None ):
		'''读取设备的short类型的数据'''
		if length == None:
			return ByteTransformHelper.GetResultFromArray( self.ReadInt16(address, 1) )
		else:
			return ByteTransformHelper.GetResultFromBytes( self.Read( address, length * self.WordLength ), lambda m: self.byteTransform.TransInt16Array( m, 0, length ) )
	def ReadUInt16( self, address, length = None ):
		'''读取设备的ushort数据类型的数据'''
		if length == None:
			return ByteTransformHelper.GetResultFromArray( self.ReadUInt16(address, 1) )
		else:
			return ByteTransformHelper.GetResultFromBytes( self.Read( address, length * self.WordLength ), lambda m: self.byteTransform.TransUInt16Array( m, 0, length ) )
	def ReadInt32( self, address, length = None ):
		'''读取设备的int类型的数据'''
		if length == None:
			return ByteTransformHelper.GetResultFromArray( self.ReadInt32(address, 1) )
		else:
			return ByteTransformHelper.GetResultFromBytes( self.Read( address, length * self.WordLength * 2 ), lambda m: self.byteTransform.TransInt32Array( m, 0, length ) )
	def ReadUInt32( self, address, length = None ):
		'''读取设备的uint数据类型的数据'''
		if length == None:
			return ByteTransformHelper.GetResultFromArray( self.ReadUInt32(address, 1) )
		else:
			return ByteTransformHelper.GetResultFromBytes( self.Read( address, length * self.WordLength * 2 ), lambda m: self.byteTransform.TransUInt32Array( m, 0, length ) )
	def ReadFloat( self, address, length = None ):
		'''读取设备的float类型的数据'''
		if length == None:
			return ByteTransformHelper.GetResultFromArray( self.ReadFloat(address, 1) )
		else:
			return ByteTransformHelper.GetResultFromBytes( self.Read( address, length * self.WordLength * 2 ), lambda m: self.byteTransform.TransSingleArray( m, 0, length ) )
	def ReadInt64( self, address, length = None ):
		'''读取设备的long类型的数组'''
		if length == None:
			return ByteTransformHelper.GetResultFromArray( self.ReadInt64(address, 1) )
		else:
			return ByteTransformHelper.GetResultFromBytes( self.Read( address, length * self.WordLength * 4 ), lambda m: self.byteTransform.TransInt64Array( m, 0, length ) )
	def ReadUInt64( self, address, length = None ):
		'''读取设备的ulong类型的数组'''
		if length == None:
			return ByteTransformHelper.GetResultFromArray( self.ReadUInt64(address, 1) )
		else:
			return ByteTransformHelper.GetResultFromBytes( self.Read( address, length * self.WordLength * 4 ), lambda m: self.byteTransform.TransUInt64Array( m, 0, length ) )
	def ReadDouble( self, address, length = None ):
		'''读取设备的double类型的数组'''
		if length == None:
			return ByteTransformHelper.GetResultFromArray( self.ReadDouble(address, 1) )
		else:
			return ByteTransformHelper.GetResultFromBytes( self.Read( address, length * self.WordLength * 4 ), lambda m: self.byteTransform.TransDoubleArray( m, 0, length ) )
	def ReadString( self, address, length, encoding = None ):
		'''读取设备的字符串数据，编码为指定的编码信息，如果不指定，那么就是ascii编码'''
		if encoding == None:
			return self.ReadString( address, length, 'ascii' )
		else:
			return ByteTransformHelper.GetResultFromBytes( self.Read( address, length ), lambda m: self.byteTransform.TransString( m, 0, len(m), encoding ) )
	
	def WriteBool( self, address, value ):
		'''向设备中写入bool数据或是数组，返回是否写入成功'''
		if type(value) == list:
			return OperateResult( StringResources.Language.NotSupportedFunction )
		else:
			return self.WriteBool( address, [value] )
	def WriteInt16( self, address, value ):
		'''向设备中写入short数据或是数组，返回是否写入成功'''
		if type(value) == list:
			return self.Write( address, self.byteTransform.Int16ArrayTransByte( value ) )
		else:
			return self.WriteInt16( address, [value] )
	def WriteUInt16( self, address, value ):
		'''向设备中写入short数据或是数组，返回是否写入成功'''
		if type(value) == list:
			return self.Write( address, self.byteTransform.UInt16ArrayTransByte( value ) )
		else:
			return self.WriteUInt16( address, [value] )
	def WriteInt32( self, address, value ):
		'''向设备中写入int数据，返回是否写入成功'''
		if type(value) == list:
			return self.Write( address, self.byteTransform.Int32ArrayTransByte(value) )
		else:
			return self.WriteInt32( address, [value])
	def WriteUInt32( self, address, value):
		'''向设备中写入uint数据，返回是否写入成功'''
		if type(value) == list:
			return self.Write( address, self.byteTransform.UInt32ArrayTransByte(value) )
		else:
			return self.WriteUInt32( address, [value] )
	def WriteFloat( self, address, value ):
		'''向设备中写入float数据，返回是否写入成功'''
		if type(value) == list:
			return self.Write( address, self.byteTransform.FloatArrayTransByte(value) )
		else:
			return self.WriteFloat(address, [value])
	def WriteInt64( self, address, value ):
		'''向设备中写入long数据，返回是否写入成功'''
		if type(value) == list:
			return self.Write( address,  self.byteTransform.Int64ArrayTransByte(value))
		else:
			return self.WriteInt64( address, [value] )
	def WriteUInt64( self, address, value ):
		'''向设备中写入ulong数据，返回是否写入成功'''
		if type(value) == list:
			return self.Write( address,  self.byteTransform.UInt64ArrayTransByte(value))
		else:
			return self.WriteUInt64( address, [value] )
	def WriteDouble( self, address, value ):
		'''向设备中写入double数据，返回是否写入成功'''
		if type(value) == list:
			return self.Write( address, self.byteTransform.DoubleArrayTransByte(value) )
		else:
			return self.WriteDouble( address, [value] )
	def WriteString( self, address, value, length = None ):
		'''向设备中写入string数据，编码为ascii，返回是否写入成功'''
		if length == None:
			return self.Write( address, self.byteTransform.StringTransByte( value, 'ascii' ) )
		else:
			return self.Write( address, SoftBasic.ArrayExpandToLength(self.byteTransform.StringTransByte( value, 'ascii' ), length))
	def WriteUnicodeString( self, address, value, length = None):
		'''向设备中写入string数据，编码为unicode，返回是否写入成功'''
		if length == None:
			temp = SoftBasic.StringToUnicodeBytes(value)
			return self.Write( address, temp )
		else:
			temp = SoftBasic.StringToUnicodeBytes(value)
			temp = SoftBasic.ArrayExpandToLength( temp, length * 2 )
			return self.Write( address, temp )


class NetworkXBase(NetworkBase):
	'''多功能网络类的基类'''
	def __init__(self):
		super().__init__()
		self.ThreadBack = None
	def SendBytesAsync( self, session, content ):
		'''发送数据的方法'''
		if content == None : return
			
		session.HybirdLockSend.acquire()
		self.Send( session.WorkSocket, content )
		session.HybirdLockSend.release()
	def ThreadBackground( self, session ):
		while True:
			if session.WorkSocket == None : break
			readHeadBytes = self.Receive(session.WorkSocket,HslProtocol.HeadByteLength())
			if readHeadBytes.IsSuccess == False :
				self.SocketReceiveException( session )
				return

			length = struct.unpack( '<i', readHeadBytes.Content[28:32])[0]
			readContent = self.Receive(session.WorkSocket,length)
			if readContent.IsSuccess == False :
				self.SocketReceiveException( session )
				return

			if self.CheckRemoteToken( readHeadBytes.Content ):
				head = readHeadBytes.Content
				content = HslProtocol.CommandAnalysis(head,readContent.Content)
				protocol = struct.unpack('<i', head[0:4])[0]
				customer = struct.unpack('<i', head[4:8])[0]

				self.DataProcessingCenter(session,protocol,customer,content)
			else:
				self.AppSessionRemoteClose( session )
	def BeginReceiveBackground( self, session ):
		ThreadBack = threading.Thread(target=self.ThreadBackground,args=[session])
		ThreadBack.start()
	def DataProcessingCenter( self, session, protocol, customer, content ):
		'''数据处理中心，应该继承重写'''
		return
	def SocketReceiveException( self, session ):
		'''接收出错的时候进行处理'''
		return
	def AppSessionRemoteClose( self, session ):
		'''当远端的客户端关闭连接时触发'''
		return
