import struct
from .. import OperateResult

class NetSupport:
	'''静态的方法支持类，提供一些网络的静态支持，支持从套接字从同步接收指定长度的字节数据，并支持报告进度。'''
	SocketBufferSize = 2048
	@staticmethod
	def ReadBytesFromSocket(socket, receive, report = None, reportByPercent = False, response = False):
		'''读取socket数据的基础方法，只适合用来接收指令头，或是同步数据'''
		bytes_receive = bytearray()
		count_receive = 0
		percent = 0
		while count_receive < receive:
			receive_length = NetSupport.SocketBufferSize if (receive - count_receive) >= NetSupport.SocketBufferSize else (receive - count_receive)
			bytes_receive.extend( socket.recv( receive_length ) )
			count_receive = len(bytes_receive)
			if reportByPercent:
				percentCurrent = count_receive * 100 / receive
				if percent != percentCurrent:
					percent = percentCurrent
					if report != None: report(count_receive, receive)
			else:
				if report != None: report(count_receive, receive)
			if response: socket.send(struct.pack('<q',count_receive))
		return bytes_receive

	@staticmethod
	def ReceiveCommandLineFromSocket( socket, endCode ):
		'''接收一行命令数据，需要自己指定这个结束符'''
		bufferArray = bytearray()
		try:
			while True:
				head = NetSupport.ReadBytesFromSocket(socket,1)
				bufferArray.extend(head)
				if head[0] == endCode: break
			return OperateResult.CreateSuccessResult(bufferArray)
		except Exception as e:
			return OperateResult(str(e))
