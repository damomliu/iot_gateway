from enum import Enum
import struct

from .. import OperateResult, SoftBasic

__all__ = [
	'DataFormat', 'ByteTransform', 'ByteTransformHelper',
	'RegularByteTransform', 'ReverseBytesTransform', 'ReverseWordTransform',
]

class DataFormat(Enum):
	'''应用于多字节数据的解析或是生成格式'''
	ABCD = 0
	BADC = 1
	CDAB = 2
	DCBA = 3

class ByteTransform:
	'''数据转换类的基础，提供了一些基础的方法实现.'''
	DataFormat = DataFormat.DCBA

	def TransBool(self, buffer, index ):
		'''
		将buffer数组转化成bool对象 -> bool

		Parameter
		  buffer: bytes 原始的数据对象
		  index: int 等待数据转换的起始索引
		Return -> bool
		'''
		return ((buffer[index] & 0x01) == 0x01)
	def TransBoolArray(self, buffer, index, length ):
		'''
		将buffer数组转化成bool数组对象，需要转入索引，长度
		
		Parameter
		  buffer: bytes 原始的缓存数据对象
		  index: int 等待数据转换的起始索引
		  length: 转换的字节数的长度
		Return
		  bool[] 解析后的bool数组
		'''
		data = buffer[index:index+length]
		return SoftBasic.ByteToBoolArray( data )

	def TransByte( self, buffer, index ):
		'''
		将buffer中的字节转化成byte对象，需要传入索引
		
		Parameter
		  buffer: bytes 原始的缓存数据对象
		  index: int 等待数据转换的起始索引
		Return
		  byte: 一个byte类型的数据
		'''
		return buffer[index]
	def TransByteArray( self, buffer, index, length ):
		'''
		将buffer中的字节转化成byte数组对象，需要传入索引
		
		Parameter
		  buffer: bytes 原始的缓存数据对象
		  index: int 等待数据转换的起始索引
		  length: int 长度信息
		Return
		  bytearray: byte[]数组
		'''
		data = bytearray(length)
		for i in range(length):
			data[i]=buffer[i+index]
		return data

	def TransInt16( self, buffer, index ):
		'''从缓存中提取short结果
		
		Parameter
		  buffer: bytes 原始的缓存数据对象
		  index: int 等待数据转换的起始索引
		Return
		  int: short数据类型'''
		data = self.TransByteArray(buffer,index,2)
		return struct.unpack('<h',data)[0]
	def TransInt16Array( self, buffer, index, length ):
		'''从缓存中提取short数组结果
		
		Parameter
		  buffer: bytes 原始的缓存数据对象
		  index: int 等待数据转换的起始索引
		  length: int 长度信息
		Return
		  int[]: short类型的数组信息'''
		tmp = []
		for i in range(length):
			tmp.append( self.TransInt16( buffer, index + 2 * i ))
		return tmp

	def TransUInt16(self, buffer, index ):
		'''从缓存中提取ushort结果
		
		Parameter
		  buffer: bytes 原始的缓存数据对象
		  index: int 等待数据转换的起始索引
		Return
		  int: ushort数据类型'''
		data = self.TransByteArray(buffer,index,2)
		return struct.unpack('<H',data)[0]
	def TransUInt16Array(self, buffer, index, length ):
		'''从缓存中提取ushort数组结果
		
		Parameter
		  buffer: bytes 原始的缓存数据对象
		  index: int 等待数据转换的起始索引
		  length: int 长度信息
		Return
		  int[]: ushort类型的数组信息'''
		tmp = []
		for i in range(length):
			tmp.append( self.TransUInt16( buffer, index + 2 * i ))
		return tmp
	
	def TransInt32(self, buffer, index ):
		'''从缓存中提取int结果
		
		Parameter
		  buffer: bytes 原始的缓存数据对象
		  index: int 等待数据转换的起始索引
		Return
		  int: int数据类型'''
		data = self.ByteTransDataFormat4(self.TransByteArray(buffer,index,4))
		return struct.unpack('<i',data)[0]
	def TransInt32Array(self, buffer, index, length ):
		'''从缓存中提取int数组结果

		Parameter
		  buffer: bytes 原始的缓存数据对象
		  index: int 等待数据转换的起始索引
		  length: int 长度信息
		Return
		  int[]: int类型的数组信息'''
		tmp = []
		for i in range(length):
			tmp.append( self.TransInt32( buffer, index + 4 * i ))
		return tmp

	def TransUInt32(self, buffer, index ):
		'''从缓存中提取uint结果
		
		Parameter
		  buffer: bytes 原始的缓存数据对象
		  index: int 等待数据转换的起始索引
		Return
		  int: uint数据类型'''
		data = self.ByteTransDataFormat4(self.TransByteArray(buffer,index,4))
		return struct.unpack('<I',data)[0]
	def TransUInt32Array(self, buffer, index, length ):
		'''从缓存中提取uint数组结果
		
		Parameter
		  buffer: bytes 原始的缓存数据对象
		  index: int 等待数据转换的起始索引
		  length: int 长度信息
		Return
		  int[]: uint类型的数组信息'''
		tmp = []
		for i in range(length):
			tmp.append( self.TransUInt32( buffer, index + 4 * i ))
		return tmp
	
	def TransInt64(self, buffer, index ):
		'''从缓存中提取long结果

		Parameter
		  buffer: bytes 原始的缓存数据对象
		  index: int 等待数据转换的起始索引
		Return
		  int: long数据类型'''
		data = self.ByteTransDataFormat8(self.TransByteArray(buffer,index,8))
		return struct.unpack('<q',data)[0]
	def TransInt64Array(self, buffer, index, length):
		'''从缓存中提取long数组结果
		
		Parameter
		  buffer: bytes 原始的缓存数据对象
		  index: int 等待数据转换的起始索引
		  length: int 长度信息
		Return
		  int[]: long类型的数组信息'''
		tmp = []
		for i in range(length):
			tmp.append( self.TransInt64( buffer, index + 8 * i ))
		return tmp
	
	def TransUInt64(self, buffer, index ):
		'''从缓存中提取ulong结果

		Parameter
		  buffer: bytes 原始的缓存数据对象
		  index: int 等待数据转换的起始索引
		Return
		  int: ulong数据类型'''
		data = self.ByteTransDataFormat8(self.TransByteArray(buffer,index,8))
		return struct.unpack('<Q',data)[0]
	def TransUInt64Array(self, buffer, index, length):
		'''从缓存中提取ulong数组结果
		
		Parameter
		  buffer: bytes 原始的缓存数据对象
		  index: int 等待数据转换的起始索引
		  length: int 长度信息
		Return
		  int[]: ulong类型的数组信息'''
		tmp = []
		for i in range(length):
			tmp.append( self.TransUInt64( buffer, index + 8 * i ))
		return tmp
	
	def TransSingle(self, buffer, index ):
		'''从缓存中提取float结果
		
		Parameter
		  buffer: bytes 原始的缓存数据对象
		  index: int 等待数据转换的起始索引
		Return
		  int: float数据类型'''
		data = self.ByteTransDataFormat4(self.TransByteArray(buffer,index,4))
		return struct.unpack('<f',data)[0]
	def TransSingleArray(self, buffer, index, length):
		'''从缓存中提取float数组结果
		
		Parameter
		  buffer: bytes 原始的缓存数据对象
		  index: int 等待数据转换的起始索引
		  length: int 长度信息
		Return
		  int[]: float类型的数组信息'''
		tmp = []
		for i in range(length):
			tmp.append( self.TransSingle( buffer, index + 4 * i ))
		return tmp
	
	def TransDouble(self, buffer, index ):
		'''从缓存中提取double结果
		
		Parameter
		  buffer: bytes 原始的缓存数据对象
		  index: int 等待数据转换的起始索引
		Return
		  int: double数据类型'''
		data = self.ByteTransDataFormat8(self.TransByteArray(buffer,index,8))
		return struct.unpack('<d',data)[0]
	def TransDoubleArray(self, buffer, index, length):
		'''从缓存中提取double数组结果
		
		Parameter
		  buffer: bytes 原始的缓存数据对象
		  index: int 等待数据转换的起始索引
		  length: int 长度信息
		Return
		  int[]: double类型的数组信息'''
		tmp = []
		for i in range(length):
			tmp.append( self.TransDouble( buffer, index + 8 * i ))
		return tmp

	def TransString( self, buffer, index, length, encoding ):
		'''从缓存中提取string结果，使用指定的编码
		
		Parameter
		  buffer: bytes 原始的缓存数据对象
		  index: int 等待数据转换的起始索引
		  length: int 长度信息
		  encoding: 编码
		Return
		  string: string类型的数组信息
		'''
		data = self.TransByteArray(buffer,index,length)
		return data.decode(encoding)

	def BoolArrayTransByte(self, values):
		'''bool数组变量转化缓存数据，需要传入bool数组
		
		Parameter
		  values: bool[] bool数组
		Return
		  bytearray: 原始的数据信息
		'''
		if (values == None): return None
		return SoftBasic.BoolArrayToByte( values )
	def BoolTransByte(self, value):
		'''bool变量转化缓存数据，需要传入bool值'''
		return self.BoolArrayTransByte([value])

	def ByteTransByte(self, value ):
		'''byte变量转化缓存数据，需要传入byte值'''
		buffer = bytearray(1)
		buffer[0] = value
		return buffer

	def Int16ArrayTransByte(self, values ):
		'''short数组变量转化缓存数据，需要传入short数组'''
		if (values == None) : return None
		buffer = bytearray(len(values) * 2)
		for i in range(len(values)):
			buffer[(i*2): (i*2+2)] = struct.pack('<h',values[i])
		return buffer
	def Int16TransByte(self, value ):
		'''short数组变量转化缓存数据，需要传入short值'''
		return self.Int16ArrayTransByte([value])

	def UInt16ArrayTransByte(self, values ):
		'''ushort数组变量转化缓存数据，需要传入ushort数组'''
		if (values == None) : return None
		buffer = bytearray(len(values) * 2)
		for i in range(len(values)):
			buffer[(i*2): (i*2+2)] = struct.pack('<H',values[i])
		return buffer
	def UInt16TransByte(self, value ):
		'''ushort变量转化缓存数据，需要传入ushort值'''
		return self.UInt16ArrayTransByte([value])

	def Int32ArrayTransByte(self, values ):
		'''int数组变量转化缓存数据，需要传入int数组'''
		if (values == None) : return None
		buffer = bytearray(len(values) * 4)
		for i in range(len(values)):
			buffer[(i*4): (i*4+4)] = self.ByteTransDataFormat4(struct.pack('<i',values[i]))
		return buffer
	def Int32TransByte(self, value ):
		'''int变量转化缓存数据，需要传入int值'''
		return self.Int32ArrayTransByte([value])

	def UInt32ArrayTransByte(self, values ):
		'''uint数组变量转化缓存数据，需要传入uint数组'''
		if (values == None) : return None
		buffer = bytearray(len(values) * 4)
		for i in range(len(values)):
			buffer[(i*4): (i*4+4)] = self.ByteTransDataFormat4(struct.pack('<I',values[i]))
		return buffer
	def UInt32TransByte(self, value ):
		'''uint变量转化缓存数据，需要传入uint值'''
		return self.UInt32ArrayTransByte([value])

	def Int64ArrayTransByte(self, values ):
		'''long数组变量转化缓存数据，需要传入long数组'''
		if (values == None) : return None
		buffer = bytearray(len(values) * 8)
		for i in range(len(values)):
			buffer[(i*8): (i*8+8)] = self.ByteTransDataFormat8(struct.pack('<q',values[i]))
		return buffer
	def Int64TransByte(self, value ):
		'''long变量转化缓存数据，需要传入long值'''
		return self.Int64ArrayTransByte([value])

	def UInt64ArrayTransByte(self, values ):
		'''ulong数组变量转化缓存数据，需要传入ulong数组'''
		if (values == None) : return None
		buffer = bytearray(len(values) * 8)
		for i in range(len(values)):
			buffer[(i*8): (i*8+8)] = self.ByteTransDataFormat8(struct.pack('<Q',values[i]))
		return buffer
	def UInt64TransByte(self, value ):
		'''ulong变量转化缓存数据，需要传入ulong值'''
		return self.UInt64ArrayTransByte([value])

	def FloatArrayTransByte(self, values ):
		'''float数组变量转化缓存数据，需要传入float数组'''
		if (values == None) : return None
		buffer = bytearray(len(values) * 4)
		for i in range(len(values)):
			buffer[(i*4): (i*4+4)] = self.ByteTransDataFormat4(struct.pack('<f',values[i]))
		return buffer
	def FloatTransByte(self, value ):
		'''float变量转化缓存数据，需要传入float值'''
		return self.FloatArrayTransByte([value])

	def DoubleArrayTransByte(self, values ):
		'''double数组变量转化缓存数据，需要传入double数组'''
		if (values == None) : return None
		buffer = bytearray(len(values) * 8)
		for i in range(len(values)):
			buffer[(i*8): (i*8+8)] = self.ByteTransDataFormat8(struct.pack('<d',values[i]))
		return buffer
	def DoubleTransByte(self, value ):
		'''double变量转化缓存数据，需要传入double值'''
		return self.DoubleArrayTransByte([value])

	def StringTransByte(self, value:str, encoding:str ):
		'''使用指定的编码字符串转化缓存数据，需要传入string值及编码信息'''
		return value.encode(encoding)

	def ByteTransDataFormat4(self, value, index = 0 ):
		'''反转多字节的数据信息'''
		buffer = bytearray(4)
		if self.DataFormat == DataFormat.ABCD:
			buffer[0] = value[index + 3]
			buffer[1] = value[index + 2]
			buffer[2] = value[index + 1]
			buffer[3] = value[index + 0]
		elif self.DataFormat == DataFormat.BADC:
			buffer[0] = value[index + 2]
			buffer[1] = value[index + 3]
			buffer[2] = value[index + 0]
			buffer[3] = value[index + 1]
		elif self.DataFormat == DataFormat.CDAB:
			buffer[0] = value[index + 1]
			buffer[1] = value[index + 0]
			buffer[2] = value[index + 3]
			buffer[3] = value[index + 2]
		elif self.DataFormat == DataFormat.DCBA:
			buffer[0] = value[index + 0]
			buffer[1] = value[index + 1]
			buffer[2] = value[index + 2]
			buffer[3] = value[index + 3]
		return buffer

	def ByteTransDataFormat8(self, value, index = 0 ):
		'''反转多字节的数据信息'''
		buffer = bytearray(8)
		if self.DataFormat == DataFormat.ABCD:
			buffer[0] = value[index + 7]
			buffer[1] = value[index + 6]
			buffer[2] = value[index + 5]
			buffer[3] = value[index + 4]
			buffer[4] = value[index + 3]
			buffer[5] = value[index + 2]
			buffer[6] = value[index + 1]
			buffer[7] = value[index + 0]
		elif self.DataFormat == DataFormat.BADC:
			buffer[0] = value[index + 6]
			buffer[1] = value[index + 7]
			buffer[2] = value[index + 4]
			buffer[3] = value[index + 5]
			buffer[4] = value[index + 2]
			buffer[5] = value[index + 3]
			buffer[6] = value[index + 0]
			buffer[7] = value[index + 1]
		elif self.DataFormat == DataFormat.CDAB:
			buffer[0] = value[index + 1]
			buffer[1] = value[index + 0]
			buffer[2] = value[index + 3]
			buffer[3] = value[index + 2]
			buffer[4] = value[index + 5]
			buffer[5] = value[index + 4]
			buffer[6] = value[index + 7]
			buffer[7] = value[index + 6]
		elif self.DataFormat == DataFormat.DCBA:
			buffer[0] = value[index + 0]
			buffer[1] = value[index + 1]
			buffer[2] = value[index + 2]
			buffer[3] = value[index + 3]
			buffer[4] = value[index + 4]
			buffer[5] = value[index + 5]
			buffer[6] = value[index + 6]
			buffer[7] = value[index + 7]
		return buffer

class RegularByteTransform(ByteTransform):
	'''常规的字节转换类'''
	def __init__(self):
		return

class ReverseBytesTransform(ByteTransform):
	'''字节倒序的转换类'''
	def TransInt16(self, buffer, index ):
		'''从缓存中提取short结果'''
		data = self.TransByteArray(buffer,index,2)
		return struct.unpack('>h',data)[0]
	def TransUInt16(self, buffer, index ):
		'''从缓存中提取ushort结果'''
		data = self.TransByteArray(buffer,index,2)
		return struct.unpack('>H',data)[0]
	def TransInt32(self, buffer, index ):
		'''从缓存中提取int结果'''
		data = self.TransByteArray(buffer,index,4)
		return struct.unpack('>i',data)[0]
	def TransUInt32(self, buffer, index ):
		'''从缓存中提取uint结果'''
		data = self.TransByteArray(buffer,index,4)
		return struct.unpack('>I',data)[0]
	def TransInt64(self, buffer, index ):
		'''从缓存中提取long结果'''
		data = self.TransByteArray(buffer,index,8)
		return struct.unpack('>q',data)[0]
	def TransUInt64(self, buffer, index ):
		'''从缓存中提取ulong结果'''
		data = self.TransByteArray(buffer,index,8)
		return struct.unpack('>Q',data)[0]
	def TransSingle(self, buffer, index ):
		'''从缓存中提取float结果'''
		data = self.TransByteArray(buffer,index,4)
		return struct.unpack('>f',data)[0]
	def TransDouble(self, buffer, index ):
		'''从缓存中提取double结果'''
		data = self.TransByteArray(buffer,index,8)
		return struct.unpack('>d',data)[0]
	
	def Int16ArrayTransByte(self, values ):
		'''short数组变量转化缓存数据，需要传入short数组 -> bytearray'''
		if (values == None) : return None
		buffer = bytearray(len(values) * 2)
		for i in range(len(values)):
			buffer[(i*2): (i*2+2)] = struct.pack('>h',values[i])
		return buffer
	def UInt16ArrayTransByte(self, values ):
		'''ushort数组变量转化缓存数据，需要传入ushort数组 -> bytearray'''
		if (values == None) : return None
		buffer = bytearray(len(values) * 2)
		for i in range(len(values)):
			buffer[(i*2): (i*2+2)] = struct.pack('>H',values[i])
		return buffer
	def Int32ArrayTransByte(self, values ):
		'''int数组变量转化缓存数据，需要传入int数组 -> bytearray'''
		if (values == None) : return None
		buffer = bytearray(len(values) * 4)
		for i in range(len(values)):
			buffer[(i*4): (i*4+4)] = struct.pack('>i',values[i])
		return buffer
	def UInt32ArrayTransByte(self, values ):
		'''uint数组变量转化缓存数据，需要传入uint数组 -> bytearray'''
		if (values == None) : return None
		buffer = bytearray(len(values) * 4)
		for i in range(len(values)):
			buffer[(i*4): (i*4+4)] = struct.pack('>I',values[i])
		return buffer
	def Int64ArrayTransByte(self, values ):
		'''long数组变量转化缓存数据，需要传入long数组 -> bytearray'''
		if (values == None) : return None
		buffer = bytearray(len(values) * 8)
		for i in range(len(values)):
			buffer[(i*8): (i*8+8)] = struct.pack('>q',values[i])
		return buffer
	def UInt64ArrayTransByte(self, values ):
		'''ulong数组变量转化缓存数据，需要传入ulong数组 -> bytearray'''
		if (values == None) : return None
		buffer = bytearray(len(values) * 8)
		for i in range(len(values)):
			buffer[(i*8): (i*8+8)] = struct.pack('>Q',values[i])
		return buffer
	def FloatArrayTransByte(self, values ):
		'''float数组变量转化缓存数据，需要传入float数组 -> bytearray'''
		if (values == None) : return None
		buffer = bytearray(len(values) * 4)
		for i in range(len(values)):
			buffer[(i*4): (i*4+4)] = struct.pack('>f',values[i])
		return buffer
	def DoubleArrayTransByte(self, values ):
		'''double数组变量转化缓存数据，需要传入double数组 -> bytearray'''
		if (values == None) : return None
		buffer = bytearray(len(values) * 8)
		for i in range(len(values)):
			buffer[(i*8): (i*8+8)] = struct.pack('>d',values[i])
		return buffer

class ReverseWordTransform(ByteTransform):
	'''按照字节错位的数据转换类'''
	def __init__(self):
		'''初始化方法，重新设置DataFormat'''
		self.DataFormat = DataFormat.ABCD
	
	IsStringReverse = False

	def ReverseBytesByWord( self, buffer, index, length ):
		'''按照字节错位的方法 -> bytearray'''
		if buffer == None: return None
		data = self.TransByteArray(buffer,index,length)
		for i in range(len(data)//2):
			data[i*2+0],data[i*2+1]= data[i*2+1],data[i*2+0]
		return data
	def ReverseAllBytesByWord( self, buffer ):
		'''按照字节错位的方法 -> bytearray'''
		return self.ReverseBytesByWord(buffer,0,len(buffer))
	def TransInt16( self, buffer, index ):
		'''从缓存中提取short结果'''
		data = self.ReverseBytesByWord(buffer,index,2)
		return struct.unpack('<h',data)[0]
	def TransUInt16(self, buffer, index ):
		'''从缓存中提取ushort结果'''
		data = self.ReverseBytesByWord(buffer,index,2)
		return struct.unpack('<H',data)[0]
	def TransString( self, buffer, index, length, encoding ):
		'''从缓存中提取string结果，使用指定的编码'''
		data = self.TransByteArray(buffer,index,length)
		if self.IsStringReverse:
			return self.ReverseAllBytesByWord(data).decode(encoding)
		else:
			return data.decode(encoding)
	
	def Int16ArrayTransByte(self, values ):
		'''short数组变量转化缓存数据，需要传入short数组'''
		buffer = super().Int16ArrayTransByte(values)
		return self.ReverseAllBytesByWord(buffer)
	def UInt16ArrayTransByte(self, values ):
		'''ushort数组变量转化缓存数据，需要传入ushort数组'''
		buffer = super().UInt16ArrayTransByte(values)
		return self.ReverseAllBytesByWord(buffer)
	def StringTransByte(self, value, encoding ):
		'''使用指定的编码字符串转化缓存数据，需要传入string值及编码信息'''
		buffer = value.encode(encoding)
		buffer = SoftBasic.BytesArrayExpandToLengthEven(buffer)
		if self.IsStringReverse:
			return self.ReverseAllBytesByWord( buffer )
		else:
			return buffer

class ByteTransformHelper:
	'''所有数据转换类的静态辅助方法'''
	@staticmethod
	def GetResultFromBytes( result, translator ):
		'''结果转换操作的基础方法，需要支持类型，及转换的委托
		
		Parameter
		  result: OperateResult<bytearray> OperateResult类型的结果对象
		  translator: lambda 一个lambda方法，将bytearray转换真实的对象
		Return
		  OperateResult: 包含真实数据的结果类对象
		'''
		try:
			if result.IsSuccess:
				return OperateResult.CreateSuccessResult(translator( result.Content ))
			else:
				return result
		except Exception as ex:
			return OperateResult(str(ex))
	@staticmethod
	def GetResultFromArray( result ):
		'''结果转换操作的基础方法，需要支持类型，及转换的委托
		
		Parameter
		  result: OperateResult 带数组对象类型的结果对象
		Return
		  OperateResult: 带单个数据的结果类对象
		'''
		if result.IsSuccess == False: return result
		return OperateResult.CreateSuccessResult(result.Content[0])
