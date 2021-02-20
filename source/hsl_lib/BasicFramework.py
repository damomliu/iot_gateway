import uuid
import random
import threading
import gzip

class SoftBasic:
	'''系统运行的基础方法，提供了一些基本的辅助方法'''
	@staticmethod
	def GetSizeDescription(size:int):
		'''获取指定数据大小的文本描述字符串'''
		if size < 1000:
			return str(size) + " B"
		elif size < (1000 * 1000):
			data = float(size) / 1024
			return '{:.2f}'.format(data) + " Kb"
		elif size < (1000 * 1000 * 1000):
			data = float(size) / 1024 / 1024
			return '{:.2f}'.format(data) + " Mb"
		else:
			data = float(size) / 1024 / 1024 / 1024
			return '{:.2f}'.format(data) + " Gb"
	@staticmethod
	def GetTimeSpanDescription( totalSeconds ):
		'''从一个时间差返回带单位的描述'''
		if totalSeconds <= 60:
			return int(totalSeconds) + " 秒"
		elif totalSeconds <= 3600:
			return '{:.1f}'.format(totalSeconds / 60) + " 分钟"
		elif totalSeconds <= 86400:
			return '{:.1f}'.format(totalSeconds / 3600) + " 小时"
		else:
			return '{:.1f}'.format(totalSeconds / 86400) + " 天"
	@staticmethod
	def ArrayFormat( array, format = None):
		'''将数组格式化为显示的字符串的信息，支持所有的类型对象'''
		if array == None:
			return None
		sb = "["
		for i in range(len(array)):
			if format == None:
				sb += str(array[i])
			else:
				sb += format.format(array[i])
			if i != (len(array) - 1):
				sb += ","
		sb += "]"
		return sb
		
	@staticmethod
	def ByteToHexString(inBytes,segment=' '):
		'''将字节数组转换成十六进制的表示形式，需要传入2个参数，数据和分隔符，该方法还存在一点问题'''
		str_list = []
		for byte in inBytes:
			str_list.append('{:02X}'.format(byte))
		if segment != None: 
			return segment.join(str_list)
		else:
			return ''.join(str_list)
	@staticmethod
	def ByteToBoolArray( InBytes, length = None ):
		'''从字节数组中提取bool数组变量信息'''
		if InBytes == None:
			return None
		if length == None:
			length = len(InBytes) * 8
		if length > len(InBytes) * 8:
			length = len(InBytes) * 8
		buffer = []
		for  i in range(length):
			index = i // 8
			offect = i % 8

			temp = 0
			if offect == 0 : temp = 0x01
			elif offect == 1 : temp = 0x02
			elif offect == 2 : temp = 0x04
			elif offect == 3 : temp = 0x08
			elif offect == 4 : temp = 0x10
			elif offect == 5 : temp = 0x20
			elif offect == 6 : temp = 0x40
			elif offect == 7 : temp = 0x80

			if (InBytes[index] & temp) == temp:
				buffer.append(True)
			else:
				buffer.append(False)
		return buffer
	@staticmethod
	def BoolArrayToByte( array ):
		'''从bool数组变量变成byte数组'''
		if (array == None) : return None

		length = 0
		if len(array) % 8 == 0:
			length = int(len(array) / 8)
		else:
			length = int(len(array) / 8) + 1
		buffer = bytearray(length)

		for i in range(len(array)):
			index = i // 8
			offect = i % 8

			temp = 0
			if offect == 0 : temp = 0x01
			elif offect == 1 : temp = 0x02
			elif offect == 2 : temp = 0x04
			elif offect == 3 : temp = 0x08
			elif offect == 4 : temp = 0x10
			elif offect == 5 : temp = 0x20
			elif offect == 6 : temp = 0x40
			elif offect == 7 : temp = 0x80

			if array[i] : buffer[index] += temp
		return buffer
	@staticmethod
	def HexStringToBytes( hex ):
		'''将hex字符串转化为byte数组'''
		return bytes.fromhex(hex)
	@staticmethod
	def BytesArrayExpandToLengthEven(array):
		'''扩充一个整型的数据长度为偶数个'''
		if len(array) % 2 == 1:
			array.append(0)
		return array
	@staticmethod
	def IsTwoBytesEquel( b1, start1, b2, start2, length ):
		'''判断两个字节的指定部分是否相同'''
		if b1 == None or b2 == None: return False
		for ii in range(length):
			if b1[ii+start1] != b2[ii+start2]: return False
		return True
	@staticmethod
	def IsTwoBytesAllEquel( b1, b2 ):
		'''判断两个字节是否相同'''
		if b1 == None or b2 == None: return False
		if len(b1) != len(b2) : return False

		for ii in range(len(b1)):
			if b1[ii] != b2[ii]: return False
		return True
	@staticmethod
	def TokenToBytes( token ):
		'''将uuid的token值转化成统一的bytes数组，方便和java，C#通讯'''
		buffer = bytearray(token.bytes)
		buffer[0],buffer[1],buffer[2],buffer[3] = buffer[3],buffer[2],buffer[1],buffer[0]
		buffer[4],buffer[5] = buffer[5],buffer[4]
		buffer[6],buffer[7] = buffer[7],buffer[6]
		return buffer
	@staticmethod
	def ArrayExpandToLength( value, length ):
		'''将数组扩充到指定的长度'''
		buffer = bytearray(length)
		if len(value) >= length:
			buffer[0:] = value[0:len(value)]
		else:
			buffer[0:len(value)] = value
		return buffer
	@staticmethod
	def ArrayExpandToLengthEven( value ):
		'''将数组扩充到偶数的长度'''
		if len(value) % 2 == 0:
			return value
		else:
			buffer = bytearray(len(value)+1)
			buffer[0:len(value)] = value
			return value
	@staticmethod
	def StringToUnicodeBytes( value ):
		'''获取字符串的unicode编码字符'''
		if value == None: return bytearray(0)

		buffer = value.encode('utf-16')
		if len(buffer) > 1 and buffer[0] == 255 and buffer[1] == 254:
			buffer = buffer[2:len(buffer)]
		return buffer
	@staticmethod
	def GetUniqueStringByGuidAndRandom():
		'''获取一串唯一的随机字符串，长度为20，由Guid码和4位数的随机数组成，保证字符串的唯一性'''
		return SoftBasic.ByteToHexString(SoftBasic.TokenToBytes(uuid.uuid1()), None) + str(random.randint(12, 20))


class SoftIncrementCount:
	'''一个简单的不持久化的序号自增类，采用线程安全实现，并允许指定最大数字，到达后清空从指定数开始'''
	start = 0
	current = 0
	maxValue = 100000000000000000000000000
	hybirdLock = threading.Lock()
	def __init__(self, maxValue:int, start:int):
		'''实例化一个自增信息的对象，包括最大值
		
		Parameter
		  maxValue: int 当前的最大值，传入一个整数即可
		  start: int 开始值，重置后，也将从这个值开始计数
		'''
		self.maxValue = maxValue
		self.start = start
	def __str__(self):
		'''
		返回表示当前对象的字符串 -> string 当前的数值
		'''
		return str(self.current)
	def GetCurrentValue( self ):
		'''获取自增信息'''
		value = 0
		self.hybirdLock.acquire()
		value = self.current
		self.current = self.current + 1
		if self.current > self.maxValue:
			self.current = self.start
		self.hybirdLock.release()
		return value


class SoftZipped:
	'''一个负责压缩解压数据字节的类'''
	@staticmethod
	def CompressBytes( inBytes ):
		'''压缩字节数据'''
		if inBytes == None : return None
		return gzip.compress( inBytes )
	@staticmethod
	def Decompress( inBytes ):
		'''解压字节数据'''
		if inBytes == None : return None
		return gzip.decompress( inBytes )

