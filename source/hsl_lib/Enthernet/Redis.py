from .. import OperateResult, SoftBasic, StringResources
from ..Core import NetSupport, RegularByteTransform, HslMessage
from ..Core.Net import NetworkDoubleBase


class RedisHelper:
	'''提供了redis辅助类的一些方法'''
	@staticmethod
	def ReceiveCommandLine( socket ):
		'''接收一行命令数据'''
		return NetSupport.ReceiveCommandLineFromSocket(socket, ord('\n'))
	@staticmethod
	def ReceiveCommandString( socket, length ):
		'''接收一行字符串的信息'''
		try:
			bufferArray = bytearray()
			bufferArray.extend(NetSupport.ReadBytesFromSocket(socket, length))

			commandTail = RedisHelper.ReceiveCommandLine(socket)
			if commandTail.IsSuccess == False: return commandTail

			bufferArray.extend(commandTail.Content)
			return OperateResult.CreateSuccessResult(bufferArray)
		except Exception as e:
			return OperateResult(str(e))
	@staticmethod
	def ReceiveCommand( socket ):
		'''从网络接收一条redis消息'''
		bufferArray = bytearray()
		readCommandLine = RedisHelper.ReceiveCommandLine( socket )
		if readCommandLine.IsSuccess == False: return readCommandLine
		
		bufferArray.extend(readCommandLine.Content)
		if readCommandLine.Content[0] == ord('+') or readCommandLine.Content[0] == ord('-') or readCommandLine.Content[0] == ord(':'):
			# 状态回复，错误回复，整数回复
			return OperateResult.CreateSuccessResult(bufferArray)
		elif readCommandLine.Content[0] == ord('$'):
			# 批量回复，允许最大512M字节
			lengthResult = RedisHelper.GetNumberFromCommandLine(readCommandLine.Content)
			if lengthResult.IsSuccess == False: return OperateResult.CreateFailedResult(lengthResult)
			
			if lengthResult.Content < 0: return OperateResult.CreateSuccessResult(bufferArray)
			
			# 接收字符串信息
			receiveContent = RedisHelper.ReceiveCommandString(socket, lengthResult.Content)
			if receiveContent.IsSuccess == False: return receiveContent
			
			bufferArray.extend(receiveContent.Content)
			return OperateResult.CreateSuccessResult(bufferArray)
		elif readCommandLine.Content[0] == ord('*'):
			# 多参数的情况的回复
			lengthResult = RedisHelper.GetNumberFromCommandLine( readCommandLine.Content )
			if lengthResult.IsSuccess == False: return lengthResult
			
			for i in range(lengthResult.Content):
				receiveCommand = RedisHelper.ReceiveCommand( socket )
				if receiveCommand.IsSuccess == False: return receiveCommand
				bufferArray.extend(receiveCommand.Content)
			
			return OperateResult.CreateSuccessResult(bufferArray)
		else:
			return OperateResult("Not Supported HeadCode:" + chr(readCommandLine.Content[0]))
				

	@staticmethod
	def PackStringCommand( commands ):
		'''将字符串数组打包成一个redis的报文信息'''
		sb = "*"
		sb += str(len(commands))
		sb += "\r\n"
		for i in range(len(commands)):
			sb += "$"
			sb += str(len(commands[i].encode(encoding='utf-8')))
			sb += "\r\n"
			sb += commands[i]
			sb += "\r\n"
		return sb.encode(encoding='utf-8')

	@staticmethod
	def GetNumberFromCommandLine( commandLine ):
		'''从原始的结果数据对象中提取出数字数据'''
		try:
			command = commandLine.decode(encoding='utf-8').strip('\r\n')
			return OperateResult.CreateSuccessResult(int(command[1:]))
		except Exception as e:
			return OperateResult(msg = str(e))
	@staticmethod
	def GetStringFromCommandLine( commandLine ):
		'''从结果的数据对象里提取字符串的信息'''
		try:
			if commandLine[0] != ord('$'): return OperateResult(commandLine.decode(encoding='utf-8'))
			
			index_start = -1
			index_end = -1
			for i in range(len(commandLine)):
				if commandLine[i] == ord('\n') or commandLine[i] == ord('\r'):
					index_start = i
				if commandLine[i] == ord('\n'):
					index_end = i
					break
			length = int(commandLine[1: index_start].decode(encoding='utf-8'))
			if length < 0: return OperateResult(msg="(nil) None Value")
				
			return OperateResult.CreateSuccessResult(commandLine[index_end + 1:index_end + 1 + length].decode(encoding='utf-8'))
		except Exception as e:
			return OperateResult(msg = str(e))
	@staticmethod
	def GetStringsFromCommandLine( commandLine ):
		'''从redis的结果数据中分析出所有的字符串信息'''
		# try:
		lists = []
		if commandLine[0] != ord('*'): return OperateResult(commandLine.decode(encoding='utf-8'))

		index = 0
		for i in range(len(commandLine)):
			if commandLine[i] == ord('\n') or commandLine[i] == ord('\r'):
				index = i
				break
		length = int(commandLine[1: index].decode(encoding='utf-8'))
		for i in range(length):
			# 提取所有的字符串内容
			index_end = -1
			for j in range(len(commandLine)):
				if commandLine[j + index] == ord('\n'):
					index_end = j + index
					break
			index = index_end + 1
			if commandLine[index] == ord('$'):
				# 寻找子字符串
				index_start = -1
				for j in range(len(commandLine)):
					if commandLine[j + index] == ord('\n') or commandLine[j + index] == ord('\r'):
						index_start = j + index
						break
				stringLength = int(commandLine[index + 1: index_start].decode(encoding='utf-8'))
				if stringLength >= 0:
					for j in range(len(commandLine)):
						if commandLine[j + index] == ord('\n'):
							index_end = j + index
							break
					index = index_end + 1
					lists.append(commandLine[index:index+stringLength].decode(encoding='utf-8'))
					index = index + stringLength
				else:
					lists.append(None)
			else:
				index_start = -1
				for j in range(len(commandLine)):
					if commandLine[j + index] == ord('\n') or commandLine[j + index] == ord('\r'):
						index_start = j + index
						break
				lists.append(commandLine[index, index_start - 1].decode(encoding='utf-8'))
		return OperateResult.CreateSuccessResult(lists)
		# except Exception as e:
		#	return OperateResult(msg = str(e))

class RedisClient( NetworkDoubleBase ):
	'''这是一个redis的客户端类，支持读取，写入，发布订阅，但是不支持订阅，如果需要订阅，请使用另一个类'''
	def __init__(self, ipAddress, port, password):
		'''实例化一个客户端的对象，用于和服务器通信'''
		super().__init__()
		self.iNetMessage = HslMessage()
		self.byteTransform = RegularByteTransform()
		self.ipAddress = ipAddress
		self.port = port
		self.receiveTimeOut = 30000
		self.Password = password
	def InitializationOnConnect( self, socket ):
		'''如果设置了密码，对密码进行验证'''
		if self.Password == None: return super().InitializationOnConnect( socket )
		if self.Password == "": return super().InitializationOnConnect( socket )
		
		command = RedisHelper.PackStringCommand( ["AUTH", self.Password] )
		read = self.ReadFromCoreSocketServer( socket, command )
		if read.IsSuccess == False: return read
		
		msg = read.Content.decode(encoding='utf-8')
		if msg.startswith("+OK") == False: return OperateResult(msg)

		return OperateResult.CreateSuccessResult( )
	def ReadFromCoreSocketServer( self, socket, send ):
		'''在其他指定的套接字上，使用报文来通讯，传入需要发送的消息，返回一条完整的数据指令'''
		sendResult = self.Send( socket, send )
		if sendResult.IsSuccess == False: return OperateResult.CreateFailedResult(sendResult)
		
		tmp = SoftBasic.ByteToHexString(send, ' ')
		if self.receiveTimeOut < 0: return OperateResult.CreateSuccessResult(bytearray())

		return RedisHelper.ReceiveCommand(socket)
	def ReadCustomer( self, command ):
		'''自定义的指令交互方法，该指令用空格分割，举例：LTRIM AAAAA 0 999 就是收缩列表，GET AAA 就是获取键值，需要对返回的数据进行二次分析'''
		byteCommand = RedisHelper.PackStringCommand( command.split( ' ' ) )

		read = self.ReadFromCoreServer( byteCommand )
		if read.IsSuccess == False: return OperateResult.CreateFailedResult(read)
	
		return OperateResult.CreateSuccessResult(read.Content.decode(encoding='utf-8'))
	def OperateResultFromServer(self, commands):
		'''向服务器请求指令，并返回Redis的结果对象，本结果对象使用所有的类型读写'''
		command = RedisHelper.PackStringCommand( commands )

		read = self.ReadFromCoreServer(command)
		if read.IsSuccess == False: return OperateResult.CreateFailedResult(read)
		
		msg = read.Content.decode(encoding='utf-8')
		if msg.startswith("-") == True: return OperateResult(msg=msg)
		if msg.startswith(":") == True: return RedisHelper.GetNumberFromCommandLine( read.Content )
		if msg.startswith("$") == True: return RedisHelper.GetStringFromCommandLine( read.Content )
		if msg.startswith("*") == True: return RedisHelper.GetStringsFromCommandLine( read.Content )
		if msg.startswith("+") == True: return OperateResult.CreateSuccessResult(msg[1:].strip('\r\n'))
		return OperateResult(msg=StringResources.Language.NotSupportedDataType)

	def DeleteKey( self, keys ):
		'''删除给定的一个或多个 key 。不存在的 key 会被忽略。'''
		if type(keys) == list:
			lists = ['DEL']
			lists.extend(keys)
			return self.OperateResultFromServer(lists)
		else:
			return self.DeleteKey([keys])
	def ExistsKey( self, key ):
		'''检查给定 key 是否存在。若 key 存在，返回 1 ，否则返回 0 。'''
		return self.OperateResultFromServer( ["EXISTS", key ] )
	def ExpireKey( self, key ):
		'''为给定 key 设置生存时间，当 key 过期时(生存时间为 0 )，它会被自动删除。设置成功返回 1 。当 key 不存在或者不能为 key 设置生存时间时，返回 0 。'''
		return self.OperateResultFromServer( ["EXPIRE", key ] )
	def ReadAllKeys( self, pattern ):
		'''查找所有符合给定模式 pattern 的 key 。* 匹配数据库中所有 key。
      h?llo 匹配 hello ， hallo 和 hxllo 等。
      h[ae]llo 匹配 hello 和 hallo ，但不匹配 hillo 。'''
		return self.OperateResultFromServer( ["KEYS", pattern ] )
	def MoveKey( self, key, db ):
		'''将当前数据库的 key 移动到给定的数据库 db 当中。
     如果当前数据库(源数据库)和给定数据库(目标数据库)有相同名字的给定 key ，或者 key 不存在于当前数据库，那么 MOVE 没有任何效果。
     因此，也可以利用这一特性，将 MOVE 当作锁(locking)原语(primitive)。'''
		return self.OperateResultFromServer( ["MOVE", str(db) ] )
	def PersistKey( self, key ):
		'''移除给定 key 的生存时间，将这个 key 从『易失的』(带生存时间 key )转换成『持久的』(一个不带生存时间、永不过期的 key )。
      当生存时间移除成功时，返回 1 .
      如果 key 不存在或 key 没有设置生存时间，返回 0 。'''
		return self.OperateResultFromServer( ["PERSIST", key ] )
	def ReadRandomKey( self ):
		'''从当前数据库中随机返回(不删除)一个 key 。
      当数据库不为空时，返回一个 key 。
      当数据库为空时，返回 nil 。'''
		return self.OperateResultFromServer( ["RANDOMKEY" ] )
	def RenameKey( self, key1, key2 ):
		'''将 key 改名为 newkey 。
      当 key 和 newkey 相同，或者 key 不存在时，返回一个错误。
      当 newkey 已经存在时， RENAME 命令将覆盖旧值。'''
		return self.OperateResultFromServer( ["RENAME", key1, key2 ] )
	def ReadKeyType( self, key ):
		'''返回 key 所储存的值的类型。none (key不存在)，string (字符串)，list (列表)，set (集合)，zset (有序集)，hash (哈希表)'''
		return self.OperateResultFromServer( ["TYPE", key ] )
	def AppendKey( self, key, value ):
		'''如果 key 已经存在并且是一个字符串， APPEND 命令将 value 追加到 key 原来的值的末尾。
      如果 key 不存在， APPEND 就简单地将给定 key 设为 value ，就像执行 SET key value 一样。
      返回追加 value 之后， key 中字符串的长度。'''
		return self.OperateResultFromServer( ["APPEND", key, value ] )
	def DecrementKey( self, key, value = None ):
		'''将 key 所储存的值减去减量 decrement 。如果 key 不存在，那么 key 的值会先被初始化为 0 ，然后再执行 DECR 操作。
      如果值包含错误的类型，或字符串类型的值不能表示为数字，那么返回一个错误。
      本操作的值限制在 64 位(bit)有符号数字表示之内。
      返回减去 decrement 之后， key 的值。'''
		return self.OperateResultFromServer( [ "DECR", key ] ) if value == None else self.OperateResultFromServer( [ "DECRBY", key, str(value) ] )
	def ReadKeyRange( self, key, start, end ):
		'''返回 key 中字符串值的子字符串，字符串的截取范围由 start 和 end 两个偏移量决定(包括 start 和 end 在内)。
      负数偏移量表示从字符串最后开始计数， -1 表示最后一个字符， -2 表示倒数第二个，以此类推。
      返回截取得出的子字符串。'''
		return self.OperateResultFromServer( [ "GETRANGE", key, str(start), str(end) ] )
	def ReadAndWriteKey( self, key, value ):
		'''将给定 key 的值设为 value ，并返回 key 的旧值(old value)。当 key 存在但不是字符串类型时，返回一个错误。key 不存在时，返回 nil '''
		return self.OperateResultFromServer( [ "GETSET", key, value ] )
	def IncrementKey( self, key, value = None ):
		'''如果传入的value可以是int值或是空值，或是float值，将 key 所储存的值加上增量 increment 。如果 key 不存在，那么 key 的值会先被初始化为 0 ，然后再执行 INCR 操作。
      如果值包含错误的类型，或字符串类型的值不能表示为数字，那么返回一个错误。'''
		if value == None or type(value) == int:
			return self.OperateResultFromServer( [ "INCR", key ] ) if value == None else self.OperateResultFromServer( [ "INCRBY", key, str(value) ] )
		elif type(value) == float:
			return self.OperateResultFromServer( [ "INCRBYFLOAT", key, str(value) ] )
		else:
			return OperateResult( msg = StringResources.Language.NotSupportedDataType )
	def ReadKey( self, key ):
		'''返回 key 所关联的字符串值。如果 key 不存在那么返回特殊值 nil 。假如 key 储存的值不是字符串类型，返回一个错误，因为 GET 只能用于处理字符串值。
			也可以传入所读取的关键字数组，将返回值数组信息'''
		if type(key) == list:
			lists = ['MGET']
			lists.extend(key)
			return self.OperateResultFromServer( lists )
		else:
			return self.OperateResultFromServer( ["GET", key] )
	def WriteKeys( self, keys, values ):
		'''同时设置一个或多个 key-value 对。
    	如果某个给定 key 已经存在，那么 MSET 会用新值覆盖原来的旧值，如果这不是你所希望的效果，请考虑使用 MSETNX 命令：它只会在所有给定 key 都不存在的情况下进行设置操作。'''
		if len(keys) != len(values): raise Exception('Two array length is not same')
		lists = [ 'MSET' ]
		for i in range(len(keys)):
			lists.append(keys[i])
			lists.append(values[i])
		
		return self.OperateResultFromServer( lists )
	def WriteKey( self, key, value ):
		'''将字符串值 value 关联到 key 。如果 key 已经持有其他值， SET 就覆写旧值，无视类型。
      对于某个原本带有生存时间（TTL）的键来说， 当 SET 命令成功在这个键上执行时， 这个键原有的 TTL 将被清除。'''
		return self.OperateResultFromServer( [ "SET", key, value ] )
	def WriteExpireKey( self, key, value, seconds ):
		'''将值 value 关联到 key ，并将 key 的生存时间设为 seconds (以秒为单位)。如果 key 已经存在， SETEX 命令将覆写旧值。'''
		return self.OperateResultFromServer( [ "SETEX", key, str(seconds), value ] )
	def WriteKeyIfNotExists( self, key, value ):
		'''将 key 的值设为 value ，当且仅当 key 不存在。若给定的 key 已经存在，则 SETNX 不做任何动作。设置成功，返回 1 。设置失败，返回 0 。'''
		return self.OperateResultFromServer( [ "SETNX", key, value ] )
	def WriteKeyRange( self, key, value, offset ):
		'''用 value 参数覆写(overwrite)给定 key 所储存的字符串值，从偏移量 offset 开始。不存在的 key 当作空白字符串处理。返回被 SETRANGE 修改之后，字符串的长度。'''
		return self.OperateResultFromServer( [ "SETRANGE", key, str(offset), value ] )
	def ReadKeyLength( self, key ):
		'''返回 key 所储存的字符串值的长度。当 key 储存的不是字符串值时，返回一个错误。返回符串值的长度。当 key 不存在时，返回 0 。'''
		return self.OperateResultFromServer( [ "STRLEN", key ] )
	def ListInsertBefore( self, key, value, pivot ):
		'''将值 value 插入到列表 key 当中，位于值 pivot 之前。
      当 pivot 不存在于列表 key 时，不执行任何操作。
      当 key 不存在时， key 被视为空列表，不执行任何操作。
      如果 key 不是列表类型，返回一个错误。'''
		return self.OperateResultFromServer( [ "LINSERT", key, "BEFORE", pivot, value ] )
	def ListInsertAfter( self, key, value, pivot ):
		'''将值 value 插入到列表 key 当中，位于值 pivot 之后。
      当 pivot 不存在于列表 key 时，不执行任何操作。
      当 key 不存在时， key 被视为空列表，不执行任何操作。
      如果 key 不是列表类型，返回一个错误。'''
		return self.OperateResultFromServer( [ "LINSERT", key, "AFTER", pivot, value ] )
	def GetListLength( self, key ):
		'''返回列表 key 的长度。如果 key 不存在，则 key 被解释为一个空列表，返回 0 .如果 key 不是列表类型，返回一个错误。'''
		return self.OperateResultFromServer( [ "LLEN", key ] )
	def ReadListByIndex( self, key, index ):
		'''返回列表 key 中，下标为 index 的元素。下标(index)参数 start 和 stop 都以 0 为底，也就是说，以 0 表示列表的第一个元素，以 1 表示列表的第二个元素，以此类推。
      你也可以使用负数下标，以 -1 表示列表的最后一个元素， -2 表示列表的倒数第二个元素，以此类推。如果 key 不是列表类型，返回一个错误。'''
		return self.OperateResultFromServer( [ "LINDEX", key, str(index) ] )
	def ListLeftPop( self, key ):
		'''移除并返回列表 key 的头元素。列表的头元素。当 key 不存在时，返回 nil 。'''
		return self.OperateResultFromServer( [ "LPOP", key ] )
	def ListLeftPush( self, key, value ):
		'''将一个或多个值 value 插入到列表 key 的表头，如果 key 不存在，一个空列表会被创建并执行 LPUSH 操作。当 key 存在但不是列表类型时，返回一个错误。返回执行 LPUSH 命令后，列表的长度。'''
		if type(value) == list:
			lists = [ "LPUSH" ]
			lists.append( key )
			lists.extend( value )
			return self.OperateResultFromServer( lists )
		else:
			return self.ListLeftPush( key, [ value ] )
	def ListLeftPushX( self, key, value ):
		'''将值 value 插入到列表 key 的表头，当且仅当 key 存在并且是一个列表。和 LPUSH 命令相反，当 key 不存在时， LPUSHX 命令什么也不做。
      返回LPUSHX 命令执行之后，表的长度。'''
		return self.OperateResultFromServer( [ "LPUSHX", key, value ] )
	def ListRange( self, key, start, stop ):
		'''返回列表 key 中指定区间内的元素，区间以偏移量 start 和 stop 指定。
      下标(index)参数 start 和 stop 都以 0 为底，也就是说，以 0 表示列表的第一个元素，以 1 表示列表的第二个元素，以此类推。
      你也可以使用负数下标，以 -1 表示列表的最后一个元素， -2 表示列表的倒数第二个元素，以此类推。
    	返回一个列表，包含指定区间内的元素。'''
		return self.OperateResultFromServer( [ "LRANGE", key, str(start), str(stop) ] )
	def ListRemoveElementMatch( self, key, count, value ):
		'''根据参数 count 的值，移除列表中与参数 value 相等的元素。count 的值可以是以下几种：
      count > 0 : 从表头开始向表尾搜索，移除与 value 相等的元素，数量为 count 。
      count &lt; 0 : 从表尾开始向表头搜索，移除与 value 相等的元素，数量为 count 的绝对值。
      count = 0 : 移除表中所有与 value 相等的值。
      返回被移除的数量。'''
		return self.OperateResultFromServer( [ "LREM", key, str(count), value ] )
	def ListSet( self, key, index, value ):
		'''设置数组的某一个索引的数据信息，当 index 参数超出范围，或对一个空列表( key 不存在)进行 LSET 时，返回一个错误。'''
		return self.OperateResultFromServer( [ "LSET", key, str(index), value ] )
	def ListTrim( self, key, start, end ):
		'''对一个列表进行修剪(trim)，就是说，让列表只保留指定区间内的元素，不在指定区间之内的元素都将被删除。
      举个例子，执行命令 LTRIM list 0 2 ，表示只保留列表 list 的前三个元素，其余元素全部删除。
      下标( index)参数 start 和 stop 都以 0 为底，也就是说，以 0 表示列表的第一个元素，以 1 表示列表的第二个元素，以此类推。
      你也可以使用负数下标，以 -1 表示列表的最后一个元素， -2 表示列表的倒数第二个元素，以此类推。'''
		return self.OperateResultFromServer( [ "LTRIM", key, str(start), str(end) ] )
	def ListRightPop( self, key ):
		'''移除并返回列表 key 的尾元素。当 key 不存在时，返回 nil 。'''
		return self.OperateResultFromServer( [ "RPOP", key ] )
	def ListRightPopLeftPush( self, key1, key2 ):
		'''命令 RPOPLPUSH 在一个原子时间内，执行以下两个动作：
      1. 将列表 source 中的最后一个元素( 尾元素)弹出，并返回给客户端。
      2. 将 source 弹出的元素插入到列表 destination ，作为 destination 列表的的头元素。

      举个例子，你有两个列表 source 和 destination ， source 列表有元素 a, b, c ， destination 列表有元素 x, y, z ，执行 RPOPLPUSH source destination 之后， source 列表包含元素 a, b ， destination 列表包含元素 c, x, y, z ，并且元素 c 会被返回给客户端。
      如果 source 不存在，值 nil 被返回，并且不执行其他动作。
      如果 source 和 destination 相同，则列表中的表尾元素被移动到表头，并返回该元素，可以把这种特殊情况视作列表的旋转( rotation)操作。'''
		return self.OperateResultFromServer( [ "RPOPLPUSH", key1, key2 ] )
	def ListRightPush( self, key, value ):
		'''将一个或多个值 value 插入到列表 key 的表尾(最右边)。
        如果有多个 value 值，那么各个 value 值按从左到右的顺序依次插入到表尾：比如对一个空列表 mylist 执行 RPUSH mylist a b c ，得出的结果列表为 a b c ，
        如果 key 不存在，一个空列表会被创建并执行 RPUSH 操作。当 key 存在但不是列表类型时，返回一个错误。
        返回执行 RPUSH 操作后，表的长度。'''
		if type(value) == list:
			lists = [ "RPUSH", key ]
			lists.extend( value )
			return self.OperateResultFromServer( lists )
		else:
			return self.ListRightPush( key, [ value ] )
	def ListRightPushX( self, key, value ):
		'''将值 value 插入到列表 key 的表尾，当且仅当 key 存在并且是一个列表。
      和 RPUSH 命令相反，当 key 不存在时， RPUSHX 命令什么也不做。'''
		return self.OperateResultFromServer( [ "RPUSHX", key, value ] )
	def DeleteHashKey( self, key, field ):
		'''删除哈希表 key 中的一个或多个指定域，不存在的域将被忽略。返回被成功移除的域的数量，不包括被忽略的域。'''
		if type(field) == list:
			lists = [ "HDEL", key ]
			lists.extend( field )
			return self.OperateResultFromServer( lists )
		else:
			return self.DeleteHashKey( key, [ field ] )
	def ExistsHashKey( self, key, field ):
		'''查看哈希表 key 中，给定域 field 是否存在。如果哈希表含有给定域，返回 1 。
      如果哈希表不含有给定域，或 key 不存在，返回 0 。'''
		return self.OperateResultFromServer( [ "HEXISTS", key, field ] )
	def ReadHashKey( self, key, field ):
		'''返回哈希表 key 中给定域一个或是多个 field 的值。当给定域不存在或是给定 key 不存在时，返回 nil '''
		if type(field) == list:
			lists = [ "HMGET", key ]
			lists.extend( field )
			return self.OperateResultFromServer( lists )
		else:
			return self.OperateResultFromServer( [ "HGET", key, field ] )
	def ReadHashKeyAll( self, key ):
		'''返回哈希表 key 中，所有的域和值。在返回值里，紧跟每个域名(field name)之后是域的值(value)，所以返回值的长度是哈希表大小的两倍。'''
		return self.OperateResultFromServer( [ "HGETALL", key ] )
	def IncrementHashKey( self, key, field, value ):
		'''为哈希表 key 中的域 field 的值加上增量 increment 。增量也可以为负数，相当于对给定域进行减法操作。
      如果 key 不存在，一个新的哈希表被创建并执行 HINCRBY 命令。返回执行 HINCRBY 命令之后，哈希表 key 中域 field 的值。'''
		if type(value) == int:
			return self.OperateResultFromServer( [ "HINCRBY", key, field, str(value) ] )
		elif type(value) == float:
			return self.OperateResultFromServer( [ "HINCRBYFLOAT", key, field, str(value) ] )
	def ReadHashKeys( self, key ):
		'''返回哈希表 key 中的所有域。当 key 不存在时，返回一个空表。'''
		return self.OperateResultFromServer( [ "HKEYS", key ] )
	def ReadHashKeyLength( self, key ):
		'''返回哈希表 key 中域的数量。当 key 不存在时，返回 0 。'''
		return self.OperateResultFromServer( [ "HLEN", key ] )
	def WriteHashKey( self, key, field, value ):
		'''将哈希表 key 中的域 field 的值设为 value 。
      如果 key 不存在，一个新的哈希表被创建并进行 HSET 操作。
      如果域 field 已经存在于哈希表中，旧值将被覆盖。
      如果 field 是哈希表中的一个新建域，并且值设置成功，返回 1 。
      如果哈希表中域 field 已经存在且旧值已被新值覆盖，返回 0 。'''
		return self.OperateResultFromServer( [ "HSET", key, field, value ] )
	def WriteHashKeys( self, key, fields, values ):
		'''同时将多个 field-value (域-值)对设置到哈希表 key 中。
      此命令会覆盖哈希表中已存在的域。
      如果 key 不存在，一个空哈希表被创建并执行 HMSET 操作。'''
		lists = [ "HMSET", key ]
		for i in range(len(fields)):
			lists.append( fields[i] )
			lists.append( values[i] )
		return self.OperateResultFromServer( lists )
	def WriteHashKeyNx( self, key, field, value ):
		'''将哈希表 key 中的域 field 的值设置为 value ，当且仅当域 field 不存在。若域 field 已经存在，该操作无效。
      设置成功，返回 1 。如果给定域已经存在且没有操作被执行，返回 0 。'''
		return self.OperateResultFromServer( [ "HSETNX", key, field, value ] )
	def ReadHashValues( self, key ):
		'''返回哈希表 key 中所有域的值。当 key 不存在时，返回一个空表。'''
		return self.OperateResultFromServer( [ "HVALS", key ] )
	def Save( self ):
		'''SAVE 命令执行一个同步保存操作，将当前 Redis 实例的所有数据快照(snapshot)以 RDB 文件的形式保存到硬盘。'''
		return self.OperateResultFromServer( [ "SAVE" ] )
	def SaveAsync( self ):
		'''在后台异步(Asynchronously)保存当前数据库的数据到磁盘。
      BGSAVE 命令执行之后立即返回 OK ，然后 Redis fork 出一个新子进程，
			原来的 Redis 进程(父进程)继续处理客户端请求，而子进程则负责将数据保存到磁盘，然后退出。'''
		return self.OperateResultFromServer( [ "BGSAVE" ] )
	def Publish( self, channel, message ):
		'''将信息 message 发送到指定的频道 channel，返回接收到信息 message 的订阅者数量。'''
		return self.OperateResultFromServer( [ "PUBLISH", channel, message ] )
	def SelectDB( self, db ):
		'''切换到指定的数据库，数据库索引号 index 用数字值指定，以 0 作为起始索引值。默认使用 0 号数据库。'''
		return self.OperateResultFromServer( [ "SELECT", str(db) ] )

