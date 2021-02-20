import struct

from .. import OperateResult, StringResources, SoftBasic
from ..Core import ByteTransformHelper, RegularByteTransform, INetMessage, NetworkDeviceBase

__all__ = [
	'AllenBradleyHelper',
	'AllenBradleyNet',
	'AllenBradleyMessage',
]
class AllenBradleyHelper:
	CIP_READ_DATA = 0x4C
	CIP_WRITE_DATA = 0x4D
	CIP_READ_WRITE_DATA = 0x4E
	CIP_READ_FRAGMENT = 0x52
	CIP_WRITE_FRAGMENT = 0x53
	CIP_READ_LIST = 0x55
	CIP_MULTIREAD_DATA = 0x1000
	CIP_Type_Bool = 0xC1
	CIP_Type_Byte = 0xC2
	CIP_Type_Word = 0xC3
	CIP_Type_DWord = 0xC4
	CIP_Type_LInt = 0xC5
	CIP_Type_Real = 0xCA
	CIP_Type_Double = 0xCB
	CIP_Type_Struct = 0xCC
	CIP_Type_String = 0xD0
	CIP_Type_BitArray = 0xD3

	@staticmethod
	def BuildRequestPathCommand( address ):
		'''创建路径指令
		
		Parameter
		  address: string ab的地址信息
		Return
		  bytearray: 指令结果
		'''
		ms = bytearray(0)
		tagNames = address.split( "." )

		for i in range(len(tagNames)):
			strIndex = ""
			indexFirst = tagNames[i].find( "[" )
			indexSecond = tagNames[i].find( "]" )
			if indexFirst > 0 and indexSecond > 0 and indexSecond > indexFirst:
				strIndex = tagNames[i][ indexFirst + 1: indexSecond ]
				tagNames[i] = tagNames[i][ 0: indexFirst ]
			ms.append(0x91) # 固定
			ms.append(len(tagNames[i]))
			nameBytes = tagNames[i].encode(encoding='utf-8')
			ms.extend(nameBytes)
			if len(nameBytes) % 2 == 1 : ms.append(0x00)
			
			if strIndex.strip() != "":
				indexs = strIndex.split(",")
				for j in range(len(indexs)):
					index = int( indexs[j] )
					if index < 256 :
						ms.append(0x28)
						ms.append(index)
					else:
						ms.append(0x29)
						ms.append(0x00)
						ms.append(struct.pack("<i",index)[0])
						ms.append(struct.pack("<i",index)[1])
		return ms

	@staticmethod
	def PackRequestHeader( command, session, commandSpecificData ):
		'''
		将CommandSpecificData的命令，打包成可发送的数据指令 -> bytes

		Prarameter
		  command: ushort 实际的命令暗号
		  session: uint 当前会话的id
		  commandSpecificData: byteArray CommandSpecificData命令
		Return
		  bytes: 最终可发送的数据命令
		'''
		buffer = bytearray(len(commandSpecificData) + 24)
		buffer[ 24 : 24 + len(commandSpecificData) ] = commandSpecificData
		buffer[ 0:2 ] = struct.pack('<H',command)
		buffer[ 2:4 ] = struct.pack('<H',len(commandSpecificData))
		buffer[ 4:8 ] = struct.pack('<I',session)
		return buffer
	@staticmethod
	def PackRequsetRead( address, length ):
		'''
		打包生成一个请求读取数据的节点信息，CIP指令信息 -> bytes

		Prarameter
		  address: string 地址
		  length: ushort 指代数组的长度
		Return 
		  bytes: CIP的指令信息
		'''
		buffer = bytearray(1024)
		offect = 0
		buffer[offect] = AllenBradleyHelper.CIP_READ_DATA
		offect += 1
		offect += 1
		
		requestPath = AllenBradleyHelper.BuildRequestPathCommand( address )
		buffer[offect:offect + len(requestPath)] = requestPath
		offect += len(requestPath)

		buffer[1] = (offect - 2) // 2
		buffer[offect] = struct.pack('<i',length)[0]
		offect += 1
		buffer[offect] = struct.pack('<i',length)[1]
		offect += 1

		return buffer[0:offect]
	@staticmethod
	def PackRequestReadSegment( address, startIndex, length ):
		'''打包生成一个请求读取数据片段的节点信息，CIP指令信息
		
		Prarameter
		  address: string 地址
		  length: ushort 指代数组的长度
		Return 
		  bytes: CIP的指令信息'''
		buffer = bytearray(1024)
		offect = 0
		buffer[offect] = AllenBradleyHelper.CIP_READ_FRAGMENT
		offect += 1
		offect += 1

		requestPath = AllenBradleyHelper.BuildRequestPathCommand( address )
		buffer[offect:offect + len(requestPath)] = requestPath
		offect += len(requestPath)

		buffer[1] = (offect - 2) // 2
		buffer[offect] = struct.pack('<i',length)[0]
		offect += 1
		buffer[offect] = struct.pack('<i',length)[1]
		offect += 1
		buffer[offect + 0] = struct.pack('<i',startIndex)[0]
		buffer[offect + 1] = struct.pack('<i',startIndex)[1]
		buffer[offect + 2] = struct.pack('<i',startIndex)[2]
		buffer[offect + 3] = struct.pack('<i',startIndex)[3]
		offect += 4

		return buffer[0:offect]
	@staticmethod
	def PackRequestWrite( address, typeCode, value, length = 1 ):
		'''
		根据指定的数据和类型，生成对应的数据 -> bytes

		Prarameter
		  address: string 地址
		  typeCode: ushort 数据类型
		  value: bytes 字节值
		  length: ushort 如果节点为数组，就是数组长度
		Return
		  bytes: CIP的指令信息
		'''
		buffer = bytearray(1024)
		offect = 0
		buffer[offect] = AllenBradleyHelper.CIP_WRITE_DATA
		offect += 1
		offect += 1
		
		requestPath = AllenBradleyHelper.BuildRequestPathCommand( address )
		buffer[offect:offect + len(requestPath)] = requestPath
		offect += len(requestPath)

		buffer[1] = (offect - 2) // 2
		buffer[offect] = struct.pack('<i',typeCode)[0]
		offect += 1
		buffer[offect] = struct.pack('<i',typeCode)[1]
		offect += 1
		buffer[offect] = struct.pack('<i',length)[0]
		offect += 1
		buffer[offect] = struct.pack('<i',length)[1]
		offect += 1

		buffer[offect:offect + len(value)] = value
		offect += len(value)
		return buffer[0:offect]
	@staticmethod
	def PackCommandService( portSlot, cips ):
		'''将所有的cip指定进行打包操作。

		Prarameter
		  portSlot: bytearray PLC所在的面板槽号
		  cips: bytearray list cip指令内容
		Return
		  bytes: CIP的指令信息
		'''
		ms = bytearray(0)
		ms.append(0xB2)
		ms.append(0x00)
		ms.append(0x00)
		ms.append(0x00)

		ms.append(0x52)
		ms.append(0x02)
		ms.append(0x20)
		ms.append(0x06)
		ms.append(0x24)
		ms.append(0x01)
		ms.append(0x0A)
		ms.append(0xF0)
		ms.append(0x00)
		ms.append(0x00)

		count = 0
		if len(cips) == 1:
			ms.extend(cips[0])
			count += len(cips[0])
		else:
			ms.append(0x0A)
			ms.append(0x02)
			ms.append(0x20)
			ms.append(0x02)
			ms.append(0x24)
			ms.append(0x01)
			count += 8

			ms.extend(struct.pack('<H',len(cips) ) )
			offect = 0x02 + 2 * len(cips)
			count += 2 * len(cips)

			for i in range(len(cips)):
				ms.extend(struct.pack('<H',offect ))
				offect = offect + len(cips[i])
			
			for i in range(len(cips)):
				ms.extend(cips[i])
				count += len(cips[i])
		
		ms.append((len(portSlot) + 1) // 2)
		ms.append(0x00)
		ms.extend(portSlot)
		if len(portSlot) % 2 == 1:
			ms.append(0x00)
		
		ms[12:14] = struct.pack('<H',count )
		ms[2:4] =  struct.pack('<H',len(ms) - 4 )
		return ms
	@staticmethod
	def PackCommandSpecificData( service ):
		'''生成读取直接节点数据信息的内容
		
		Prarameter
		  service: bytearray list 服务的指令内容
		Return
		  bytes: 最终的指令值
		'''
		buffer = bytearray(0)
		buffer.append( 0x00 )
		buffer.append( 0x00 )
		buffer.append( 0x00 )
		buffer.append( 0x00 )
		buffer.append( 0x01 )     # 超时
		buffer.append( 0x00 )
		buffer.extend(struct.pack('<H',len(service) ))
		for i in range(len(service)):
			buffer.extend(service[i])
		return buffer
	@staticmethod
	def ExtractActualData( response, isRead ):
		'''从PLC反馈的数据解析
		
		Prarameter
		  response: bytearray PLC的反馈数据
		  isRead: bool 是否是返回的操作
		Return
		  bytes: 最终的指令值
		  int: ushort的类型
		  bool: 是否包含额外的数据
		'''
		data = bytearray()
		offset = 38
		hasMoreData = False
		dataType = 0
		count = struct.unpack("<H", response[38:40])[0]
		if struct.unpack("<i", response[40:44])[0] == 0x8A:
			offset = 44
			dataCount = struct.unpack("<H", response[offset:offset + 2])[0]
			for i in range(dataCount):
				offsetStart = struct.unpack("<H", response[offset + 2 + i * 2 : offset + 4 + i * 2])[0] + offset
				if i == dataCount - 1:
					offsetEnd = len(response)
				else:
					offsetEnd = struct.unpack("<H", response[offset + 2 + i * 2 : offset + 4 + i * 2] )[0]
				err = struct.unpack("<H", response[offsetStart + 2 : offsetStart + 4])[0]
				if err == 0x04 : return OperateResult(err=err, msg=StringResources.Language.AllenBradley04)
				elif err == 0x05 : return OperateResult(err=err, msg=StringResources.Language.AllenBradley05)
				elif err == 0x06 :
					if response[offset + 2] == 0xD2 or response[offset + 2] == 0xCC:
						return OperateResult(err=err,msg=StringResources.Language.AllenBradley06)
					break
				elif err == 0x0A : return OperateResult(err=err,msg=StringResources.Language.AllenBradley0A)
				elif err == 0x13 : return OperateResult(err=err,msg= StringResources.Language.AllenBradley13)
				elif err == 0x1C : return OperateResult(err = err, msg= StringResources.Language.AllenBradley1C)
				elif err == 0x1E : return OperateResult(err=err,msg=StringResources.Language.AllenBradley1E)
				elif err == 0x26 : return OperateResult(err=err, msg=StringResources.Language.AllenBradley26)
				elif err == 0x00 : break
				else : return OperateResult(err= err, msg= StringResources.Language.UnknownError)
				if isRead == True:
					for j in range(offsetStart + 6, offsetEnd, 1):
						data.append(response[j])
		else:
			err = response[offset + 4]
			if err == 0x04 : return OperateResult(err=err, msg=StringResources.Language.AllenBradley04)
			elif err == 0x05 : return OperateResult(err=err, msg=StringResources.Language.AllenBradley05)
			elif err == 0x06 : hasMoreData = True
			elif err == 0x0A : return OperateResult(err=err,msg=StringResources.Language.AllenBradley0A)
			elif err == 0x13 : return OperateResult(err=err,msg= StringResources.Language.AllenBradley13)
			elif err == 0x1C : return OperateResult(err = err, msg= StringResources.Language.AllenBradley1C)
			elif err == 0x1E : return OperateResult(err=err,msg=StringResources.Language.AllenBradley1E)
			elif err == 0x26 : return OperateResult(err=err, msg=StringResources.Language.AllenBradley26)
			elif err == 0x00 : None
			else : return OperateResult(err= err, msg= StringResources.Language.UnknownError)

			if response[offset + 2] == 0xCD or response[offset + 2] == 0xD3 :
				return OperateResult.CreateSuccessResult( data, dataType, hasMoreData )
			if response[offset + 2] == 0xCC or response[offset + 2] == 0xD2 :
				for i in range(offset + 8, offset + 2+ count, 1):
					data.append( response[i] )
				dataType = struct.unpack( '<H', response[offset + 6:offset + 8] )[0]
			elif response[offset + 2] == 0xD5 :
				for i in range(offset + 6, offset + 2+ count, 1):
					data.append( response[i] )
		return OperateResult.CreateSuccessResult( data, dataType, hasMoreData )


class AllenBradleyNet(NetworkDeviceBase):
	def __init__(self, ipAddress, port):
		'''Instantiate a communication object for a Allenbradley PLC protocol
		
		Prarameter
		  ipAddress: string PLC的ip地址
		  port: int plc的端口号
		'''
		super().__init__()
		self.iNetMessage = AllenBradleyMessage()
		self.byteTransform = RegularByteTransform()
		self.SessionHandle = 0
		self.Slot = 0
		self.PortSlot = None
		self.CipCommand = 0x6F
		self.WordLength = 2
		self.ipAddress = ipAddress
		self.port = port
	def InitializationOnConnect( self, socket ):
		'''After connecting the Allenbradley plc, a next step handshake protocol is required'''
		read = self.ReadFromCoreServerBase( socket, self.RegisterSessionHandle( ) )
		if read.IsSuccess == False : return read

		# Check the returned status
		check = self.CheckResponse( read.Content1 )
		if check.IsSuccess == False : return check

		# Extract session ID
		self.SessionHandle = struct.unpack( "<I", read.Content1[4:8] )[0]
		return OperateResult.CreateSuccessResult()
	def ExtraOnDisconnect( self, socket):
		'''A next step handshake agreement is required before disconnecting the Allenbradley plc'''
		# Unregister session Information
		read = self.ReadFromCoreServerBase( socket, self.UnRegisterSessionHandle( ) )
		if read.IsSuccess == False : return read

		return OperateResult.CreateSuccessResult()
	def BuildReadCommand( self, address, length = None ):
		'''Build a read command bytes
		
		Prarameter
		  address: string array : the address of the tag name
		  length: int array : Array information, if not arrays, is 1
		Rrturn
		  OperateResult<ByteArray>: Message information that contains the result object'''
		if address == None : raise Exception("address or length is null")
		if length == None:
			length = []
			for i in range(len(address)):
				length.append(1)
			return self.BuildReadCommand(address, length)
		if len(address) != len(length) : raise Exception("address and length is not same array")

		try:
			cips = []
			for i in range(len(address)):
				cips.append(AllenBradleyHelper.PackRequsetRead(address[i],length[i]))
			commandSpecificData = AllenBradleyHelper.PackCommandSpecificData( [bytearray(4), AllenBradleyHelper.PackCommandService( self.PortSlot if self.PortSlot != None else bytearray([ 0x01, self.Slot]), cips ) ])
			return OperateResult.CreateSuccessResult( AllenBradleyHelper.PackRequestHeader( self.CipCommand, self.SessionHandle, commandSpecificData ) )
		except Exception as e:
			return OperateResult(err=10000, msg="Address Wrong:" + str(e))
	def BuildWriteCommand( self, address, typeCode, data, length = 1 ):
		'''Create a written message instruction
		
		Prarameter
		  address: string The address of the tag name 
		  TypeCode: ushort : Data type
		  data: bytearray the source data
		  length: int the length of data if array
		Rrturn
		  OperateResult<ByteArray>: Message information that contains the result object'''
		try:
			cip = AllenBradleyHelper.PackRequestWrite( address, typeCode, data, length )
			commandSpecificData = AllenBradleyHelper.PackCommandSpecificData( [bytearray(4), AllenBradleyHelper.PackCommandService( self.PortSlot if self.PortSlot != None else bytearray([ 0x01, self.Slot]), [cip] ) ])
			
			return OperateResult.CreateSuccessResult( AllenBradleyHelper.PackRequestHeader( self.CipCommand, self.SessionHandle, commandSpecificData ) )
		except Exception as e:
			return OperateResult(msg="Address Wrong:" + str(e))
	def Read( self, address, length ):
		'''Read data information, data length for read array length information

		Prarameter
		  address: Address format of the node
		  length: In the case of arrays, the length of the array 
		Rrturn
		  OperateResult<ByteArray>: Message information that contains the result object
		'''
		if type(address) == list and type(length) == list:
			# 指令生成 -> Instruction Generation
			command = self.BuildReadCommand( address, length )
			if command.IsSuccess == False: return command

            # 核心交互 -> Core Interactions
			read = self.ReadFromCoreServer( command.Content )
			if read.IsSuccess == False : return read

            # 检查反馈 -> Check Feedback
			check = self.CheckResponse( read.Content )
			if check.IsSuccess == False : return check

            # 提取数据 -> Extracting data
			extract = AllenBradleyHelper.ExtractActualData( read.Content, True )
			if extract.IsSuccess == False : return extract

			return OperateResult.CreateSuccessResult(extract.Content1)

		if length > 1:
			return self.ReadSegment( address, 0, length )
		else:
			return self.Read( [address] , [length] )
	def ReadSegment( self, address, startIndex, length ):
		'''Read Segment Data Array form plc, use address tag name
		
		Prarameter
		  address: string: Tag name in plc
		  startIndex: int :array start index, uint byte index
		  length: int: array length, data item length
		Rrturn
		  OperateResult<ByteArray>: Message information that contains the result object
		'''
		try:
			bytesContent = bytearray()
			while True:
				read = self.ReadCipFromServer( AllenBradleyHelper.PackRequestReadSegment( address, startIndex, length ) )
				if read.IsSuccess == False : return read

				# 提取数据 -> Extracting data
				analysis = AllenBradleyHelper.ExtractActualData( read.Content, True )
				if analysis.IsSuccess == False : return analysis

				startIndex += len(analysis.Content1)
				bytesContent.extend(analysis.Content1)

				if analysis.Content3 == False : break
			return OperateResult.CreateSuccessResult(bytesContent)
		except Exception as ex:
			return OperateResult(msg=str(ex))
	def ReadCipFromServer( self, cips):
		'''使用CIP报文和服务器进行核心的数据交换
		
		Prarameter
		  cips: bytearray: 单个的CIP指令
		Rrturn
		  OperateResult<ByteArray>: Message information that contains the result object
		'''
		if type(cips) != list:
			cips = [ cips ]
		commandSpecificData = AllenBradleyHelper.PackCommandSpecificData( [bytearray(4), AllenBradleyHelper.PackCommandService( self.PortSlot if self.PortSlot != None else bytearray([ 0x01, self.Slot ]), cips )] )
		command = AllenBradleyHelper.PackRequestHeader( self.CipCommand, self.SessionHandle, commandSpecificData )

		read = self.ReadFromCoreServer( command )
		if read.IsSuccess == False : return read

		# Check the returned status
		check = self.CheckResponse( read.Content )
		if check.IsSuccess == False : return check

		return OperateResult.CreateSuccessResult( read.Content )
	def ReadEipFromServer( self, eip ):
		''''''
		if type(eip) != list:
			return self.ReadEipFromServer([eip])
		else:
			commandSpecificData = AllenBradleyHelper.PackCommandSpecificData( eip )
			command = AllenBradleyHelper.PackRequestHeader( self.CipCommand, self.SessionHandle, commandSpecificData )

			# 核心交互 -> Core Interactions
			read = self.ReadFromCoreServer( command )
			if read.IsSuccess == False : return read

			# 检查反馈 -> Check Feedback
			check = self.CheckResponse( read.Content )
			if check.IsSuccess : return check

			return OperateResult.CreateSuccessResult(read.Content)
	def ReadBool( self, address ):
		'''读取单个的bool数据信息 -> Read a single BOOL data information
		
		Prarameter
		  address: string: 节点的名称 -> Name of the node 
		Rrturn
		  OperateResult<bool>: 带有结果对象的结果数据 -> Result data with result info
		'''
		read = self.Read( address, 1 )
		if read.IsSuccess == False : return read

		return OperateResult.CreateSuccessResult(self.byteTransform.TransBool(read.Content, 0))
	def ReadBoolArray(self, address):
		'''批量读取的bool数组信息 -> Bulk read of bool array information

		Prarameter
		  address: string: 节点的名称 -> Name of the node 
		Rrturn
		  OperateResult<bool[]>: 带有结果对象的结果数据 -> Result data with result info
		'''
		read = self.Read( address, 1 )
		if read.IsSuccess == False : return read

		return OperateResult.CreateSuccessResult(self.byteTransform.TransBoolArray(read.Content, 0, len(read.Content)))
	def ReadByte( self, address ):
		'''读取PLC的byte类型的数据 -> Read the byte type of PLC data
		
		Prarameter
		  address: string: 节点的名称 -> Name of the node 
		Rrturn
		  OperateResult<byte>: 带有结果对象的结果数据 -> Result data with result info
		'''
		read = self.Read( address, 1 )
		if read.IsSuccess == False: return read

		return OperateResult.CreateSuccessResult(read.Content[0])
	def ReadInt16( self, address, length = None ):
		'''读取PLC的short类型的数组 -> Read an array of the short type of the PLC'''
		if(length == None):
			return ByteTransformHelper.GetResultFromArray( self.ReadInt16(address, 1) )
		else:
			return ByteTransformHelper.GetResultFromBytes( self.Read( address, length ), lambda m : self.byteTransform.TransInt16Array( m, 0, length ) )
	def ReadUInt16( self, address, length = None ):
		'''读取PLC的ushort类型的数组 -> An array that reads the ushort type of the PLC'''
		if(length == None):
			return ByteTransformHelper.GetResultFromArray( self.ReadUInt16(address, 1) )
		else:
			return ByteTransformHelper.GetResultFromBytes( self.Read( address, length ), lambda m : self.byteTransform.TransUInt16Array( m, 0, length ) )
	def ReadInt32( self, address, length = None ):
		'''读取PLC的int类型的数组 -> An array that reads the int type of the PLC'''
		if(length == None):
			return ByteTransformHelper.GetResultFromArray( self.ReadInt32(address, 1) )
		else:
			return ByteTransformHelper.GetResultFromBytes( self.Read( address, length ), lambda m : self.byteTransform.TransInt32Array( m, 0, length ) )
	def ReadUInt32( self, address, length = None ):
		'''读取PLC的uint类型的数组 -> An array that reads the uint type of the PLC'''
		if(length == None):
			return ByteTransformHelper.GetResultFromArray( self.ReadUInt32(address, 1) )
		else:
			return ByteTransformHelper.GetResultFromBytes( self.Read( address, length ), lambda m : self.byteTransform.TransUInt32Array( m, 0, length ) )
	def ReadFloat( self, address, length = None ):
		'''读取PLC的float类型的数组 -> An array that reads the float type of the PLC'''
		if(length == None):
			return ByteTransformHelper.GetResultFromArray( self.ReadFloat(address, 1) )
		else:
			return ByteTransformHelper.GetResultFromBytes( self.Read( address, length ), lambda m : self.byteTransform.TransSingleArray( m, 0, length ) )
	def ReadInt64( self, address, length = None ):
		'''读取PLC的long类型的数组 -> An array that reads the long type of the PLC'''
		if(length == None):
			return ByteTransformHelper.GetResultFromArray( self.ReadInt64(address, 1) )
		else:
			return ByteTransformHelper.GetResultFromBytes( self.Read( address, length ), lambda m : self.byteTransform.TransInt64Array( m, 0, length ) )
	def ReadUInt64( self, address, length = None ):
		'''读取PLC的ulong类型的数组 -> An array that reads the ulong type of the PLC'''
		if(length == None):
			return ByteTransformHelper.GetResultFromArray( self.ReadUInt64(address, 1) )
		else:
			return ByteTransformHelper.GetResultFromBytes( self.Read( address, length ), lambda m : self.byteTransform.TransUInt64Array( m, 0, length ) )
	def ReadDouble( self, address, length = None ):
		'''读取PLC的double类型的数组 -> An array that reads the double type of the PLC'''
		if(length == None):
			return ByteTransformHelper.GetResultFromArray( self.ReadDouble(address, 1) )
		else:
			return ByteTransformHelper.GetResultFromBytes( self.Read( address, length ), lambda m : self.byteTransform.TransDoubleArray( m, 0, length ) )
	def ReadString( self, address ):
		'''读取PLC的string类型的数据 -> read plc string type value'''
		return super().ReadString( address, 1 )

	def Write( self, address, value ):
		'''当前的PLC不支持该功能，需要调用WriteTag(string, ushort, byte[], int) 方法来实现。'''
		return bytearray( StringResources.Language.NotSupportedFunction + " Please refer to use WriteTag instead ")
	def WriteTag( self, address, typeCode, value, length = 1 ):
		'''使用指定的类型写入指定的节点数据 -> Writes the specified node data with the specified type'''
		command = self.BuildWriteCommand( address, typeCode, value, length )
		if command.IsSuccess == False : return command

		read = self.ReadFromCoreServer( command.Content )
		if read.IsSuccess == False : return read

		check = self.CheckResponse( read.Content )
		if check.IsSuccess == False : return check

		return AllenBradleyHelper.ExtractActualData( read.Content, False )

	def WriteBool( self, address, value ):
		'''向设备中写入bool数据或是数组，返回是否写入成功'''
		return self.WriteTag(address,AllenBradleyHelper.CIP_Type_Bool , bytearray([0xFF,0xFF] if value == True else bytearray([0x00,0x00]) ))
	def WriteByte( self, address, value ):
		'''向PLC中写入byte数据，返回是否写入成功'''
		return self.WriteTag( address, AllenBradleyHelper.CIP_Type_Byte, bytearray([value,0x00] ))
	def WriteInt16( self, address, value ):
		'''向PLC中写入short数组，返回是否写入成功 -> Writes a short array to the PLC to return whether the write was successful'''
		if type(value) == list:
			return self.WriteTag( address, AllenBradleyHelper.CIP_Type_Word, self.byteTransform.Int16ArrayTransByte( value ), len(value) )
		else:
			return self.WriteInt16( address, [value] )
	def WriteUInt16( self, address, value ):
		'''向PLC中写入ushort数组，返回是否写入成功 -> Writes an array of ushort to the PLC to return whether the write was successful'''
		if type(value) == list:
			return self.WriteTag( address, AllenBradleyHelper.CIP_Type_Word, self.byteTransform.UInt16ArrayTransByte( value ), len(value) )
		else:
			return self.WriteUInt16( address, [value] )
	def WriteInt32( self, address, value ):
		'''向PLC中写入int数组，返回是否写入成功 -> Writes a int array to the PLC to return whether the write was successful'''
		if type(value) == list:
			return self.WriteTag( address, AllenBradleyHelper.CIP_Type_DWord, self.byteTransform.Int32ArrayTransByte( value ), len(value) )
		else:
			return self.WriteInt32( address, [value] )
	def WriteUInt32( self, address, value ):
		'''向PLC中写入uint数组，返回是否写入成功 -> Writes a uint array to the PLC to return whether the write was successful'''
		if type(value) == list:
			return self.WriteTag( address, AllenBradleyHelper.CIP_Type_DWord, self.byteTransform.UInt32ArrayTransByte( value ), len(value) )
		else:
			return self.WriteUInt32( address, [value] )
	def WriteFloat( self, address, value ):
		'''向PLC中写入float数组，返回是否写入成功 -> Writes a float array to the PLC to return whether the write was successful'''
		if type(value) == list:
			return self.WriteTag( address, AllenBradleyHelper.CIP_Type_Real, self.byteTransform.FloatArrayTransByte( value ), len(value) )
		else:
			return self.WriteFloat( address, [value] )
	def WriteInt64( self, address, value ):
		'''向PLC中写入long数组，返回是否写入成功 -> Writes a long array to the PLC to return whether the write was successful'''
		if type(value) == list:
			return self.WriteTag( address, AllenBradleyHelper.CIP_Type_LInt, self.byteTransform.Int64ArrayTransByte( value ), len(value) )
		else:
			return self.WriteInt64( address, [value] )
	def WriteUInt64( self, address, value ):
		'''向PLC中写入ulong数组，返回是否写入成功 -> Writes a ulong array to the PLC to return whether the write was successful'''
		if type(value) == list:
			return self.WriteTag( address, AllenBradleyHelper.CIP_Type_LInt, self.byteTransform.UInt64ArrayTransByte( value ), len(value) )
		else:
			return self.WriteUInt64( address, [value] )
	def WriteDouble( self, address, value ):
		'''向PLC中写入double数组，返回是否写入成功 -> Writes a double array to the PLC to return whether the write was successful'''
		if type(value) == list:
			return self.WriteTag( address, AllenBradleyHelper.CIP_Type_Double, self.byteTransform.DoubleArrayTransByte( value ), len(value) )
		else:
			return self.WriteDouble( address, [value] )
	def WriteString( self, address, value ):
		'''向PLC中写入string数据，返回是否写入成功，针对的是ASCII编码的数据内容'''
		if value == None : value = ""

		data = value.encode('ascii')
		write = self.WriteInt32( address + ".LEN", len(data) )
		if write.IsSuccess == False : return write

		buffer = SoftBasic.ArrayExpandToLengthEven( data )
		return self.WriteTag( address + ".DATA[0]", AllenBradleyHelper.CIP_Type_Byte, buffer, len(data ) )
	def RegisterSessionHandle( self ):
		'''向PLC注册会话ID的报文 -> Register a message with the PLC for the session ID'''
		commandSpecificData = bytearray( [0x01, 0x00, 0x00, 0x00 ])
		return AllenBradleyHelper.PackRequestHeader( 0x65, 0, commandSpecificData )
	def UnRegisterSessionHandle( self ):
		'''获取卸载一个已注册的会话的报文 -> Get a message to uninstall a registered session'''
		return AllenBradleyHelper.PackRequestHeader( 0x66, self.SessionHandle, bytearray(0) )
	def CheckResponse( self, response ):
		try:
			status = self.byteTransform.TransInt32( response, 8 )
			if status == 0 : return OperateResult.CreateSuccessResult( )

			msg = ""
			if status == 0x01 : msg = StringResources.Language.AllenBradleySessionStatus01
			elif status == 0x02 : msg = StringResources.Language.AllenBradleySessionStatus02
			elif status == 0x03 : msg = StringResources.Language.AllenBradleySessionStatus03
			elif status == 0x64 : msg = StringResources.Language.AllenBradleySessionStatus64
			elif status == 0x65 : msg = StringResources.Language.AllenBradleySessionStatus65
			elif status == 0x69 : msg = StringResources.Language.AllenBradleySessionStatus69
			else: msg = StringResources.Language.UnknownError

			return OperateResult(msg=msg)
		except Exception as ex:
			return OperateResult(msg=str(ex))


class AllenBradleyMessage (INetMessage):
	'''用于和 AllenBradley PLC 交互的消息协议类'''
	def ProtocolHeadBytesLength(self):
		'''协议头数据长度，也即是第一次接收的数据长度'''
		return 24
	def GetContentLengthByHeadBytes(self):
		'''二次接收的数据长度'''
		if self.HeadBytes != None:
			return struct.unpack('<h',self.HeadBytes[2:4])[0]
		else:
			return 0
	def CheckHeadBytesLegal(self,token):
		'''令牌检查是否成功'''
		return True
	def GetHeadBytesIdentity(self):
		'''获取头子节里的消息标识'''
		return 0

