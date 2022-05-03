import struct
from .. import SoftBasic
from . import INetMessage

from ..Modbus import ModbusTcpMessage
from ..Profinet.AllenBradley import AllenBradleyMessage
from ..Profinet.Melsec import MelsecA1EBinaryMessage, MelsecQnA3EAsciiMessage, MelsecQnA3EBinaryMessage
from ..Profinet.Omron import FinsMessage
from ..Profinet.Siemens import S7Message


class FetchWriteMessage (INetMessage):
	'''西门子Fetch/Write消息解析协议'''
	def ProtocolHeadBytesLength(self):
		'''协议头数据长度，也即是第一次接收的数据长度'''
		return 16
	def GetContentLengthByHeadBytes(self):
		'''二次接收的数据长度'''
		if self.SendBytes != None:
			if self.SendBytes[5] == 0x04: return 0
			else: return self.SendBytes[12] * 256 + self.SendBytes[13]
		else:
			return 16
	def CheckHeadBytesLegal(self,token):
		'''令牌检查是否成功'''
		if self.HeadBytes != None:
			if self.HeadBytes[0] == 0x53 and self.HeadBytes[1] == 0x35:
				return True
			else:
				return False
		else:
			return False
	def GetHeadBytesIdentity(self):
		'''获取头子节里的消息标识'''
		return self.HeadBytes[3]

class HslMessage (INetMessage):
	'''本组件系统使用的默认的消息规则，说明解析和反解析规则的'''
	def ProtocolHeadBytesLength(self):
		'''协议头数据长度，也即是第一次接收的数据长度'''
		return 32
	def GetContentLengthByHeadBytes(self):
		'''二次接收的数据长度'''
		if self.HeadBytes != None:
			buffer = bytearray(4)
			buffer[0:4] = self.HeadBytes[28:32]
			return struct.unpack('<i',buffer)[0]
		else:
			return 0
	def GetHeadBytesIdentity(self):
		'''获取头子节里的消息标识'''
		if self.HeadBytes != None:
			buffer = bytearray(4)
			buffer[0:4] = self.HeadBytes[4:8]
			return struct.unpack('<i',buffer)[0]
		else:
			return 0
	def CheckHeadBytesLegal(self,token):
		'''令牌检查是否成功'''
		if self.HeadBytes == None:
			return False
		else:
			return SoftBasic.IsTwoBytesEquel(self.HeadBytes,12,token,0,16)

class EFORTMessage (INetMessage):
	'''埃夫特机器人的消息对象'''
	def ProtocolHeadBytesLength(self):
		'''协议头数据长度，也即是第一次接收的数据长度'''
		return 18
	def GetContentLengthByHeadBytes(self):
		'''二次接收的数据长度'''
		if self.HeadBytes != None:
			return struct.unpack('<h',self.HeadBytes[16:18])[0] - 18
		else:
			return 0
	def CheckHeadBytesLegal(self,token):
		'''令牌检查是否成功'''
		return True

class EFORTMessagePrevious (INetMessage):
	'''旧版的机器人的消息类对象，保留此类为了实现兼容'''
	def ProtocolHeadBytesLength(self):
		'''协议头数据长度，也即是第一次接收的数据长度'''
		return 17
	def GetContentLengthByHeadBytes(self):
		'''二次接收的数据长度'''
		if self.HeadBytes != None:
			return struct.unpack('<h',self.HeadBytes[15:17])[0] - 17
		else:
			return 0
	def CheckHeadBytesLegal(self,token):
		'''令牌检查是否成功'''
		return True
	
class KukaVarProxyMessage(INetMessage):
	'''Kuka机器人的 KRC4 控制器中的服务器KUKAVARPROXY'''
	def ProtocolHeadBytesLength(self):
		'''协议头数据长度，也即是第一次接收的数据长度'''
		return 4
	def GetContentLengthByHeadBytes(self):
		'''二次接收的数据长度'''
		if self.HeadBytes != None:
			return self.HeadBytes[2]*256 + self.HeadBytes[3]
		else:
			return 0
	def CheckHeadBytesLegal(self,token):
		'''令牌检查是否成功'''
		return True

class SAMMessage(INetMessage):
	def ProtocolHeadBytesLength(self):
		'''协议头数据长度，也即是第一次接收的数据长度'''
		return 7
	def GetContentLengthByHeadBytes(self):
		'''二次接收的数据长度'''
		if self.HeadBytes != None:
			if (self.HeadBytes) >= 7:
				return self.HeadBytes[5] * 256 + self.HeadBytes[6]
		else:
			return 0
	def CheckHeadBytesLegal(self,token):
		'''令牌检查是否成功'''
		if self.HeadBytes == None: return False
		return self.HeadBytes[0] == 0xAA and self.HeadBytes[1] == 0xAA and self.HeadBytes[2] == 0xAA and self.HeadBytes[3] == 0x96 and self.HeadBytes[4] == 0x69
