from time import sleep
import struct

from .. import HslProtocol, OperateResult
from ..Core import RegularByteTransform, HslMessage
from ..Core.IMessage import HslMessage
from ..Core.Net import NetworkDoubleBase, NetworkXBase, AppSession

__all__ = [
	'NetSimplifyClient',
	'NetPushClient',
]

class NetSimplifyClient(NetworkDoubleBase):
	'''异步访问数据的客户端类，用于向服务器请求一些确定的数据信息'''
	def __init__(self, ipAddress, port):
		'''实例化一个客户端的对象，用于和服务器通信'''
		super().__init__()
		self.iNetMessage = HslMessage()
		self.byteTransform = RegularByteTransform()
		self.ipAddress = ipAddress
		self.port = port

	def InitializationOnConnect( self, socket ):
		'''连接上服务器后需要进行的初始化操作，无论是否允许操作都要进行验证'''
		if self.isUseAccountCertificate == True:
			return self.AccountCertificate( socket )
		return OperateResult.CreateSuccessResult()

	def ReadFromServer( self, customer, send = None):
		'''客户端向服务器进行请求，请求数据，类型取决于你的send的类型'''
		if send == None: return
		if type(send) == str:
			read = self.__ReadFromServerBase(  HslProtocol.CommandString( customer, self.Token, send))
			if read.IsSuccess == False:
				return OperateResult.CreateFailedResult( read )
			
			return OperateResult.CreateSuccessResult( read.Content.decode('utf-16') )
		else:
			return self.__ReadFromServerBase( HslProtocol.CommandBytes( customer, self.Token, send))

	def __ReadFromServerBase( self, send):
		'''需要发送的底层数据'''
		read = self.ReadFromCoreServer( send )
		if read.IsSuccess == False:
			return read

		headBytes = bytearray(HslProtocol.HeadByteLength())
		contentBytes = bytearray(len(read.Content) - HslProtocol.HeadByteLength())

		headBytes[0:HslProtocol.HeadByteLength()] = read.Content[0:HslProtocol.HeadByteLength()]
		if len(contentBytes) > 0:
			contentBytes[0:len(contentBytes)] = read.Content[HslProtocol.HeadByteLength():len(read.Content)]

		contentBytes = HslProtocol.CommandAnalysis( headBytes, contentBytes )
		return OperateResult.CreateSuccessResult( contentBytes )


class NetPushClient(NetworkXBase):
	'''发布订阅类的客户端，使用指定的关键订阅相关的数据推送信息'''
	def __init__( self, ipAddress, port, key):
		'''实例化一个发布订阅类的客户端，需要指定ip地址，端口，及订阅关键字'''
		super().__init__()
		self.IpAddress = ipAddress
		self.Port = port
		self.keyWord = key
		self.ReConnectTime = 10
		self.action = None
	def DataProcessingCenter( self, session, protocol, customer, content ):
		if protocol == HslProtocol.ProtocolUserString():
			if self.action != None: self.action( self.keyWord, content.decode('utf-16') )
	def SocketReceiveException( self, session ):
		# 发生异常的时候需要进行重新连接
		while True:
			print('NetPushClient wait 10s to reconnect server')
			sleep( self.ReConnectTime )

			if self.CreatePush( ).IsSuccess == True:
				break
	def CreatePush( self, pushCallBack = None ):
		'''创建数据推送服务'''
		if pushCallBack == None:
			if self.CoreSocket != None: self.CoreSocket.close( )
			connect = self.CreateSocketAndConnect( self.IpAddress, self.Port, 5000 )
			if connect.IsSuccess == False: return connect

			send = self.SendStringAndCheckReceive( connect.Content, 0, self.keyWord )
			if send.IsSuccess == False: return send

			receive = self.ReceiveStringContentFromSocket( connect.Content )
			if receive.IsSuccess == False : return receive

			if receive.Content1 != 0: return OperateResult( msg = receive.Content2 )

			appSession = AppSession( )
			self.CoreSocket = connect.Content
			appSession.WorkSocket = connect.Content
			self.BeginReceiveBackground( appSession )

			return OperateResult.CreateSuccessResult( )
		else:
			self.action = pushCallBack
			return self.CreatePush( )
	def ClosePush( self ):
		'''关闭消息推送的界面'''
		self.action = None
		if self.CoreSocket != None:
			self.Send(self.CoreSocket, struct.pack('<i', 100 ) )

		self.CloseSocket(self.CoreSocket)
