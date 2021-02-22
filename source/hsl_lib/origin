'''
	From https://github.com/dathlin/HslCommunicationPython
	(pip install HslCommunication==1.0.4)
'''
'''
             ///\      ///\             /////////\              ///\
            //\\/      //\/           //\\\\\\\\//\            //\\/
           //\/       //\/          //\\/       \\/           //\/
          //\/       //\/           \//\                     //\/
         /////////////\/             \//////\               //\/
        //\\\\\\\\\//\/               \\\\\//\             //\/
       //\/       //\/                     \//\           //\/
      //\/       //\/           ///\      //\\/          //\/       //\
     ///\      ///\/            \/////////\\/           /////////////\/
     \\\/      \\\/              \\\\\\\\\/             \\\\\\\\\\\\\/             Present by Richard.Hu

	CopyRight by Richard.Hu 2017-2020
	 本程序的版权归胡少林所有，源代码仅限于学术研究使用，商用需要授权，在没有获得商用版权的情况下，应用于商用项目，将依法追究法律责任，感谢支持，详细说明请参照：

	 企业商用说明：仅限于公司开发的软件，该软件的署名必须为授权公司，不得改成他人或是公司（除非他人或公司已经取得商用授权），该软件不能被转卖。授权不限制项目，一次授权，终生使用。

	 关于授权的步骤：
	     1. 签合同，双方在合同上签字
		 2. 付款，支持支付宝，微信，银行卡
		 3. 开发票，增值税普票（个人找税务局代开的）
		 4. 加入 Hsl超级VIP群 即获得源代码和超级激活码，永久支持更新。
		 5. 注册官网的git账户
		 6. 专业培训额外付费，1000元人民币1小时，培训控件使用，控件开发。
		 7. 联系方式：Email:hsl200909@163.com   QQ:200962190   Weichat:13516702732

	官网：http://www.hslcommunication.cn  如果不能访问，请访问：http://118.24.36.220


	The copyright of this program belongs to Hu Shaolin. The source code is limited to academic research. Commercial licenses are required. 
	If commercial copyrights are not obtained and applied to commercial projects, legal liability will be investigated. Thank you for your support. For details, please refer to:


	Personal commercial description: It is limited to software developed by individuals. The software must be signed by an authorized person. 
	It must not be changed to another person or company (unless another person or company has obtained a commercial license). 
	The software cannot be resold. Authorization does not limit the project, once authorized, lifetime use.

	Enterprise commercial description: It is limited to the software developed by the company. The signature of the software must be an authorized company. 
	It must not be changed to another person or company (unless someone else or the company has obtained a commercial license). The software cannot be resold. 
	Authorization does not limit the project, once authorized, lifetime use.

	Steps on authorization:
	1. Sign the contract, both parties sign the contract
	2. Payment, support Alipay, WeChat, bank card
	3. Invoice, general VAT ticket (issued on behalf of the individual, registered companies will be different later)
	4. Join the Hsl Super VIP Group to get the source code and super activation code, and always support updates.
	5. Register git account on official website
	6. Professional training costs an additional fee of 1,000 yuan per hour, training controls use, control development.
	7. Contact: Email: hsl200909@163.com QQ: 200962190 Weichat: 13516702732
	
	Website：http://www.hslcommunication.cn  If you cannot access, please visit: http://118.24.36.220

'''
import string
import uuid
import socket
import struct
import threading
import gzip
import datetime
import random
from time import sleep
from enum import Enum

class DefaultLanguage(object):
	'''系统的语言基类，默认也即是中文版本'''
	AuthorizationFailed = "系统授权失败，需要使用激活码授权，谢谢支持。"
	ConnectedFailed = "连接失败："
	ConnectedSuccess = "连接成功！"
	UnknownError = "未知错误"
	ErrorCode = "错误代号"
	TextDescription = "文本描述"
	ExceptionMessage = "错误信息："
	ExceptionSourse = "错误源："
	ExceptionType = "错误类型："
	ExceptionStackTrace = "错误堆栈："
	ExceptopnTargetSite = "错误方法："
	ExceprionCustomer = "用户自定义方法出错："
	SuccessText = "成功"
	TwoParametersLengthIsNotSame = "两个参数的个数不一致"
	NotSupportedFunction = "当前的功能逻辑不支持"
	NotSupportedDataType = "输入的类型不支持，请重新输入"
	DataLengthIsNotEnough = "接收的数据长度不足，应该值:{0},实际值:{1}"
	ReceiveDataTimeout = "接收数据超时："
	ReceiveDataLengthTooShort = "接收的数据长度太短："
	MessageTip = "消息提示："
	Close = "关闭"
	Time = "时间："
	SoftWare = "软件："
	BugSubmit = "Bug提交"
	MailServerCenter = "邮件发送系统"
	MailSendTail = "邮件服务系统自动发出，请勿回复！"
	IpAddresError = "Ip地址输入异常，格式不正确"
	Send = "发送"
	Receive = "接收"
	# 系统相关的错误信息
	SystemInstallOperater = "安装新系统：IP为"
	SystemUpdateOperater = "更新新系统：IP为"
	# 套接字相关的信息描述
	SocketIOException = "套接字传送数据异常："
	SocketSendException = "同步数据发送异常："
	SocketHeadReceiveException = "指令头接收异常："
	SocketContentReceiveException = "内容数据接收异常："
	SocketContentRemoteReceiveException = "对方内容数据接收异常："
	SocketAcceptCallbackException = "异步接受传入的连接尝试"
	SocketReAcceptCallbackException = "重新异步接受传入的连接尝试"
	SocketSendAsyncException = "异步数据发送出错:"
	SocketEndSendException = "异步数据结束挂起发送出错"
	SocketReceiveException = "异步数据发送出错:"
	SocketEndReceiveException = "异步数据结束接收指令头出错"
	SocketRemoteCloseException = "远程主机强迫关闭了一个现有的连接"
	# 文件相关的信息
	FileDownloadSuccess = "文件下载成功"
	FileDownloadFailed = "文件下载异常"
	FileUploadFailed = "文件上传异常"
	FileUploadSuccess = "文件上传成功"
	FileDeleteFailed = "文件删除异常"
	FileDeleteSuccess = "文件删除成功"
	FileReceiveFailed = "确认文件接收异常"
	FileNotExist = "文件不存在"
	FileSaveFailed = "文件存储失败"
	FileLoadFailed = "文件加载失败"
	FileSendClientFailed = "文件发送的时候发生了异常"
	FileWriteToNetFailed = "文件写入网络异常"
	FileReadFromNetFailed = "从网络读取文件异常"
	FilePathCreateFailed = "文件夹路径创建失败："
	FileRemoteNotExist = "对方文件不存在，无法接收！"
	# 服务器的引擎相关数据
	TokenCheckFailed = "接收验证令牌不一致"
	TokenCheckTimeout = "接收验证超时:"
	CommandHeadCodeCheckFailed = "命令头校验失败"
	CommandLengthCheckFailed = "命令长度检查失败"
	NetClientAliasFailed = "客户端的别名接收失败："
	NetEngineStart = "启动引擎"
	NetEngineClose = "关闭引擎"
	NetClientOnline = "上线"
	NetClientOffline = "下线"
	NetClientBreak = "异常掉线"
	NetClientFull = "服务器承载上限，收到超出的请求连接。"
	NetClientLoginFailed = "客户端登录中错误："
	NetHeartCheckFailed = "心跳验证异常："
	NetHeartCheckTimeout = "心跳验证超时，强制下线："
	DataSourseFormatError = "数据源格式不正确"
	ServerFileCheckFailed = "服务器确认文件失败，请重新上传"
	ClientOnlineInfo = "客户端 [ {0} ] 上线"
	ClientOfflineInfo = "客户端 [ {0} ] 下线"
	ClientDisableLogin = "客户端 [ {0} ] 不被信任，禁止登录"
	# Client 相关
	ReConnectServerSuccess = "重连服务器成功"
	ReConnectServerAfterTenSeconds = "在10秒后重新连接服务器"
	KeyIsNotAllowedNull = "关键字不允许为空"
	KeyIsExistAlready = "当前的关键字已经存在"
	KeyIsNotExist = "当前订阅的关键字不存在"
	ConnectingServer = "正在连接服务器..."
	ConnectFailedAndWait = "连接断开，等待{0}秒后重新连接"
	AttemptConnectServer = "正在尝试第{0}次连接服务器"
	ConnectServerSuccess = "连接服务器成功"
	GetClientIpaddressFailed = "客户端IP地址获取失败"
	ConnectionIsNotAvailable = "当前的连接不可用"
	DeviceCurrentIsLoginRepeat = "当前设备的id重复登录"
	DeviceCurrentIsLoginForbidden = "当前设备的id禁止登录"
	PasswordCheckFailed = "密码验证失败"
	DataTransformError = "数据转换失败，源数据："
	RemoteClosedConnection = "远程关闭了连接"
	# 日志相关
	LogNetDebug = "调试"
	LogNetInfo = "信息"
	LogNetWarn = "警告"
	LogNetError = "错误"
	LogNetFatal = "致命"
	LogNetAbandon = "放弃"
	LogNetAll = "全部"
	# Modbus相关
	ModbusTcpFunctionCodeNotSupport = "不支持的功能码"
	ModbusTcpFunctionCodeOverBound = "读取的数据越界"
	ModbusTcpFunctionCodeQuantityOver = "读取长度超过最大值"
	ModbusTcpFunctionCodeReadWriteException = "读写异常"
	ModbusTcpReadCoilException = "读取线圈异常"
	ModbusTcpWriteCoilException = "写入线圈异常"
	ModbusTcpReadRegisterException = "读取寄存器异常"
	ModbusTcpWriteRegisterException = "写入寄存器异常"
	ModbusAddressMustMoreThanOne = "地址值在起始地址为1的情况下，必须大于1"
	ModbusAsciiFormatCheckFailed = "Modbus的ascii指令检查失败，不是modbus-ascii报文"
	ModbusCRCCheckFailed = "Modbus的CRC校验检查失败"
	ModbusLRCCheckFailed = "Modbus的LRC校验检查失败"
	ModbusMatchFailed = "不是标准的modbus协议"
	# Melsec PLC 相关
	MelsecPleaseReferToManulDocument = "请查看三菱的通讯手册来查看报警的具体信息"
	MelsecReadBitInfo = "读取位变量数组只能针对位软元件，如果读取字软元件，请调用Read方法"
	MelsecCurrentTypeNotSupportedWordOperate = "当前的类型不支持字读写"
	MelsecCurrentTypeNotSupportedBitOperate = "当前的类型不支持位读写"
	MelsecFxReceiveZore = "接收的数据长度为0"
	MelsecFxAckNagative = "PLC反馈的数据无效"
	MelsecFxAckWrong = "PLC反馈信号错误："
	MelsecFxCrcCheckFailed = "PLC反馈报文的和校验失败！"
	# Siemens PLC 相关
	SiemensDBAddressNotAllowedLargerThan255 = "DB块数据无法大于255"
	SiemensReadLengthMustBeEvenNumber = "读取的数据长度必须为偶数"
	SiemensWriteError = "写入数据异常，代号为："
	SiemensReadLengthCannotLargerThan19 = "读取的数组数量不允许大于19"
	SiemensDataLengthCheckFailed = "数据块长度校验失败，请检查是否开启put/get以及关闭db块优化"
	SiemensFWError = "发生了异常，具体信息查找Fetch/Write协议文档"
	SiemensReadLengthOverPlcAssign = "读取的数据范围超出了PLC的设定"
	# Omron PLC 相关
	OmronAddressMustBeZeroToFiveteen = "输入的位地址只能在0-15之间"
	OmronReceiveDataError = "数据接收异常"
	OmronStatus0 = "通讯正常"
	OmronStatus1 = "消息头不是FINS"
	OmronStatus2 = "数据长度太长"
	OmronStatus3 = "该命令不支持"
	OmronStatus20 = "超过连接上限"
	OmronStatus21 = "指定的节点已经处于连接中"
	OmronStatus22 = "尝试去连接一个受保护的网络节点，该节点还未配置到PLC中"
	OmronStatus23 = "当前客户端的网络节点超过正常范围"
	OmronStatus24 = "当前客户端的网络节点已经被使用"
	OmronStatus25 = "所有的网络节点已经被使用"
	# AB PLC 相关
	AllenBradley04 = "它没有正确生成或匹配标记不存在。"
	AllenBradley05 = "引用的特定项（通常是实例）无法找到。"
	AllenBradley06 = "请求的数据量不适合响应缓冲区。 发生了部分数据传输。"
	AllenBradley0A = "尝试处理其中一个属性时发生错误。"
	AllenBradley13 = "命令中没有提供足够的命令数据/参数来执行所请求的服务。"
	AllenBradley1C = "与属性计数相比，提供的属性数量不足。"
	AllenBradley1E = "此服务中的服务请求出错。"
	AllenBradley26 = "IOI字长与处理的IOI数量不匹配。"

	AllenBradleySessionStatus00 = "成功"
	AllenBradleySessionStatus01 = "发件人发出无效或不受支持的封装命令。"
	AllenBradleySessionStatus02 = "接收器中的内存资源不足以处理命令。 这不是一个应用程序错误。 相反，只有在封装层无法获得所需内存资源的情况下才会导致此问题。"
	AllenBradleySessionStatus03 = "封装消息的数据部分中的数据形成不良或不正确。"
	AllenBradleySessionStatus64 = "向目标发送封装消息时，始发者使用了无效的会话句柄。"
	AllenBradleySessionStatus65 = "目标收到一个无效长度的信息。"
	AllenBradleySessionStatus69 = "不支持的封装协议修订。"
	# Panasonic PLC 相关
	PanasonicReceiveLengthMustLargerThan9 = "接收数据长度必须大于9"
	PanasonicAddressParameterCannotBeNull = "地址参数不允许为空"
	PanasonicMewStatus20 = "错误未知"
	PanasonicMewStatus21 = "NACK错误，远程单元无法被正确识别，或者发生了数据错误。"
	PanasonicMewStatus22 = "WACK 错误:用于远程单元的接收缓冲区已满。"
	PanasonicMewStatus23 = "多重端口错误:远程单元编号(01 至 16)设置与本地单元重复。"
	PanasonicMewStatus24 = "传输格式错误:试图发送不符合传输格式的数据，或者某一帧数据溢出或发生了数据错误。"
	PanasonicMewStatus25 = "硬件错误:传输系统硬件停止操作。"
	PanasonicMewStatus26 = "单元号错误:远程单元的编号设置超出 01 至 63 的范围。"
	PanasonicMewStatus27 = "不支持错误:接收方数据帧溢出. 试图在不同的模块之间发送不同帧长度的数据。"
	PanasonicMewStatus28 = "无应答错误:远程单元不存在. (超时)。"
	PanasonicMewStatus29 = "缓冲区关闭错误:试图发送或接收处于关闭状态的缓冲区。"
	PanasonicMewStatus30 = "超时错误:持续处于传输禁止状态。"
	PanasonicMewStatus40 = "BCC 错误:在指令数据中发生传输错误。"
	PanasonicMewStatus41 = "格式错误:所发送的指令信息不符合传输格式。"
	PanasonicMewStatus42 = "不支持错误:发送了一个未被支持的指令。向未被支持的目标站发送了指令。"
	PanasonicMewStatus43 = "处理步骤错误:在处于传输请求信息挂起时,发送了其他指令。"
	PanasonicMewStatus50 = "链接设置错误:设置了实际不存在的链接编号。"
	PanasonicMewStatus51 = "同时操作错误:当向其他单元发出指令时,本地单元的传输缓冲区已满。"
	PanasonicMewStatus52 = "传输禁止错误:无法向其他单元传输。"
	PanasonicMewStatus53 = "忙错误:在接收到指令时,正在处理其他指令。"
	PanasonicMewStatus60 = "参数错误:在指令中包含有无法使用的代码,或者代码没有附带区域指定参数(X, Y, D), 等以外。"
	PanasonicMewStatus61 = "数据错误:触点编号,区域编号,数据代码格式(BCD,hex,等)上溢出, 下溢出以及区域指定错误。"
	PanasonicMewStatus62 = "寄存器错误:过多记录数据在未记录状态下的操作（监控记录、跟踪记录等。)。"
	PanasonicMewStatus63 = "PLC 模式错误:当一条指令发出时，运行模式不能够对指令进行处理。"
	PanasonicMewStatus65 = "保护错误:在存储保护状态下执行写操作到程序区域或系统寄存器。"
	PanasonicMewStatus66 = "地址错误:地址（程序地址、绝对地址等）数据编码形式（BCD、hex 等）、上溢、下溢或指定范围错误。"
	PanasonicMewStatus67 = "丢失数据错误:要读的数据不存在。（读取没有写入注释寄存区的数据。。"
	# 永宏plc相关的信息
	FatekStatus02 = "不合法数值"
	FatekStatus03 = "禁止写入"
	FatekStatus04 = "不合法的命令码"
	FatekStatus05 = "不能激活(下RUN命令但Ladder Checksum不合)"
	FatekStatus06 = "不能激活(下RUN命令但PLC ID≠ Ladder ID)"
	FatekStatus07 = "不能激活（下RUN命令但程序语法错误）"
	FatekStatus09 = "不能激活（下RUN命令，但Ladder之程序指令PLC无法执行）"
	FatekStatus10 = "不合法的地址"
	# 富士plc相关的信息
	FujiSpbStatus01 = "对ROM进行了写入"
	FujiSpbStatus02 = "接收了未定义的命令或无法处理的命令"
	FujiSpbStatus03 = "数据部分有矛盾（参数异常）"
	FujiSpbStatus04 = "由于收到了其他编程器的传送联锁，因此无法处理"
	FujiSpbStatus05 = "模块序号不正确"
	FujiSpbStatus06 = "检索项目未找到"
	FujiSpbStatus07 = "指定了超出模块范围的地址（写入时）"
	FujiSpbStatus09 = "由于故障程序无法执行（RUN）"
	FujiSpbStatus0C = "密码不一致"



	def __setattr__(self, f, v):
		'''强制所有的属性为只读的，无法进行更改和设置'''
		raise AttributeError('{}.{} is READ ONLY'.format(type(self).__name__, f))

class English(DefaultLanguage):
	'''English Version Text'''
	AuthorizationFailed = "System authorization failed, need to use activation code authorization, thank you for your support."
	ConnectedFailed = "Connected Failed: "
	ConnectedSuccess = "Connect Success !"
	UnknownError = "Unknown Error"
	ErrorCode = "Error Code: "
	TextDescription = "Description: "
	ExceptionMessage = "Exception Info: "
	ExceptionSourse = "Exception Sourse："
	ExceptionType = "Exception Type："
	ExceptionStackTrace = "Exception Stack: "
	ExceptopnTargetSite = "Exception Method: "
	ExceprionCustomer = "Error in user-defined method: "
	SuccessText = "Success"
	TwoParametersLengthIsNotSame = "Two Parameter Length is not same"
	NotSupportedDataType = "Unsupported DataType, input again"
	NotSupportedFunction = "The current feature logic does not support"
	DataLengthIsNotEnough = "Receive length is not enough，Should:{0},Actual:{1}"
	ReceiveDataTimeout = "Receive timeout: "
	ReceiveDataLengthTooShort = "Receive length is too short: "
	MessageTip = "Message prompt:"
	Close = "Close"
	Time = "Time:"
	SoftWare = "Software:"
	BugSubmit = "Bug submit"
	MailServerCenter = "Mail Center System"
	MailSendTail = "Mail Service system issued automatically, do not reply"
	IpAddresError = "IP address input exception, format is incorrect"
	Send = "Send"
	Receive = "Receive"
	# System about
	SystemInstallOperater = "Install new software: ip address is"
	SystemUpdateOperater = "Update software: ip address is"
	# Socket-related Information description
	SocketIOException = "Socket transport error: "
	SocketSendException = "Synchronous Data Send exception: "
	SocketHeadReceiveException = "Command header receive exception: "
	SocketContentReceiveException = "Content Data Receive exception: "
	SocketContentRemoteReceiveException = "Recipient content Data Receive exception: "
	SocketAcceptCallbackException = "Asynchronously accepts an incoming connection attempt: "
	SocketReAcceptCallbackException = "To re-accept incoming connection attempts asynchronously"
	SocketSendAsyncException = "Asynchronous Data send Error: "
	SocketEndSendException = "Asynchronous data end callback send Error"
	SocketReceiveException = "Asynchronous Data send Error: "
	SocketEndReceiveException = "Asynchronous data end receive instruction header error"
	SocketRemoteCloseException = "An existing connection was forcibly closed by the remote host"
	# File related information
	FileDownloadSuccess = "File Download Successful"
	FileDownloadFailed = "File Download exception"
	FileUploadFailed = "File Upload exception"
	FileUploadSuccess = "File Upload Successful"
	FileDeleteFailed = "File Delete exception"
	FileDeleteSuccess = "File deletion succeeded"
	FileReceiveFailed = "Confirm File Receive exception"
	FileNotExist = "File does not exist"
	FileSaveFailed = "File Store failed"
	FileLoadFailed = "File load failed"
	FileSendClientFailed = "An exception occurred when the file was sent"
	FileWriteToNetFailed = "File Write Network exception"
	FileReadFromNetFailed = "Read file exceptions from the network"
	FilePathCreateFailed = "Folder path creation failed: "
	FileRemoteNotExist = "The other file does not exist, cannot receive!"
	# Engine-related data for the server
	TokenCheckFailed = "Receive authentication token inconsistency"
	TokenCheckTimeout = "Receive authentication timeout: "
	CommandHeadCodeCheckFailed = "Command header check failed"
	CommandLengthCheckFailed = "Command length check failed"
	NetClientAliasFailed = "Client's alias receive failed: "
	NetEngineStart = "Start engine"
	NetEngineClose = "Shutting down the engine"
	NetClientOnline = "Online"
	NetClientOffline = "Offline"
	NetClientBreak = "Abnormal offline"
	NetClientFull = "The server hosts the upper limit and receives an exceeded request connection."
	NetClientLoginFailed = "Error in Client logon: "
	NetHeartCheckFailed = "Heartbeat Validation exception: "
	NetHeartCheckTimeout = "Heartbeat verification timeout, force offline: "
	DataSourseFormatError = "Data source format is incorrect"
	ServerFileCheckFailed = "Server confirmed file failed, please re-upload"
	ClientOnlineInfo = "Client [ {0} ] Online"
	ClientOfflineInfo = "Client [ {0} ] Offline"
	ClientDisableLogin = "Client [ {0} ] is not trusted, login forbidden"
	# Client related
	ReConnectServerSuccess = "Re-connect server succeeded"
	ReConnectServerAfterTenSeconds = "Reconnect the server after 10 seconds"
	KeyIsNotAllowedNull = "The keyword is not allowed to be empty"
	KeyIsExistAlready = "The current keyword already exists"
	KeyIsNotExist = "The keyword for the current subscription does not exist"
	ConnectingServer = "Connecting to Server..."
	ConnectFailedAndWait = "Connection disconnected, wait {0} seconds to reconnect"
	AttemptConnectServer = "Attempting to connect server {0} times"
	ConnectServerSuccess = "Connection Server succeeded"
	GetClientIpaddressFailed = "Client IP Address acquisition failed"
	ConnectionIsNotAvailable = "The current connection is not available"
	DeviceCurrentIsLoginRepeat = "ID of the current device duplicate login"
	DeviceCurrentIsLoginForbidden = "The ID of the current device prohibits login"
	PasswordCheckFailed = "Password validation failed"
	DataTransformError = "Data conversion failed, source data: "
	RemoteClosedConnection = "Remote shutdown of connection"
	# Log related
	LogNetDebug = "Debug"
	LogNetInfo = "Info"
	LogNetWarn = "Warn"
	LogNetError = "Error"
	LogNetFatal = "Fatal"
	LogNetAbandon = "Abandon"
	LogNetAll = "All"
	# Modbus related
	ModbusTcpFunctionCodeNotSupport = "Unsupported function code"
	ModbusTcpFunctionCodeOverBound = "Data read out of bounds"
	ModbusTcpFunctionCodeQuantityOver = "Read length exceeds maximum value"
	ModbusTcpFunctionCodeReadWriteException = "Read and Write exceptions"
	ModbusTcpReadCoilException = "Read Coil anomalies"
	ModbusTcpWriteCoilException = "Write Coil exception"
	ModbusTcpReadRegisterException = "Read Register exception"
	ModbusTcpWriteRegisterException = "Write Register exception"
	ModbusAddressMustMoreThanOne = "The address value must be greater than 1 in the case where the start address is 1"
	ModbusAsciiFormatCheckFailed = "Modbus ASCII command check failed, not MODBUS-ASCII message"
	ModbusCRCCheckFailed = "The CRC checksum check failed for Modbus"
	ModbusLRCCheckFailed = "The LRC checksum check failed for Modbus"
	ModbusMatchFailed = "Not the standard Modbus protocol"
	# Melsec PLC related
	MelsecPleaseReferToManulDocument = "Please check Mitsubishi's communication manual for details of the alarm."
	MelsecReadBitInfo = "The read bit variable array can only be used for bit soft elements, if you read the word soft component, call the Read method"
	MelsecCurrentTypeNotSupportedWordOperate = "The current type does not support word read and write"
	MelsecCurrentTypeNotSupportedBitOperate = "The current type does not support bit read and write"
	MelsecFxReceiveZore = "The received data length is 0"
	MelsecFxAckNagative = "Invalid data from PLC feedback"
	MelsecFxAckWrong = "PLC Feedback Signal Error: "
	MelsecFxCrcCheckFailed = "PLC Feedback message and check failed!"
	# Siemens PLC related
	SiemensDBAddressNotAllowedLargerThan255 = "DB block data cannot be greater than 255"
	SiemensReadLengthMustBeEvenNumber = "The length of the data read must be an even number"
	SiemensWriteError = "Writes the data exception, the code name is: "
	SiemensReadLengthCannotLargerThan19 = "The number of arrays read does not allow greater than 19"
	SiemensDataLengthCheckFailed = "Block length checksum failed, please check if Put/get is turned on and DB block optimization is turned off"
	SiemensFWError = "An exception occurred, the specific information to find the Fetch/write protocol document"
	SiemensReadLengthOverPlcAssign = "The range of data read exceeds the setting of the PLC"
	# Omron PLC related
	OmronAddressMustBeZeroToFiveteen = "The bit address entered can only be between 0-15"
	OmronReceiveDataError = "Data Receive exception"
	OmronStatus0 = "Communication is normal."
	OmronStatus1 = "The message header is not fins"
	OmronStatus2 = "Data length too long"
	OmronStatus3 = "This command does not support"
	OmronStatus20 = "Exceeding connection limit"
	OmronStatus21 = "The specified node is already in the connection"
	OmronStatus22 = "Attempt to connect to a protected network node that is not yet configured in the PLC"
	OmronStatus23 = "The current client's network node exceeds the normal range"
	OmronStatus24 = "The current client's network node is already in use"
	OmronStatus25 = "All network nodes are already in use"
	# AB PLC related
	AllenBradley04 = "The IOI could not be deciphered. Either it was not formed correctly or the match tag does not exist."
	AllenBradley05 = "The particular item referenced (usually instance) could not be found."
	AllenBradley06 = "The amount of data requested would not fit into the response buffer. Partial data transfer has occurred."
	AllenBradley0A = "An error has occurred trying to process one of the attributes."
	AllenBradley13 = "Not enough command data / parameters were supplied in the command to execute the service requested."
	AllenBradley1C = "An insufficient number of attributes were provided compared to the attribute count."
	AllenBradley1E = "A service request in this service went wrong."
	AllenBradley26 = "The IOI word length did not match the amount of IOI which was processed."

	AllenBradleySessionStatus00 = "success"
	AllenBradleySessionStatus01 = "The sender issued an invalid or unsupported encapsulation command."
	AllenBradleySessionStatus02 = "Insufficient memory resources in the receiver to handle the command. This is not an application error. Instead, it only results if the encapsulation layer cannot obtain memory resources that it need."
	AllenBradleySessionStatus03 = "Poorly formed or incorrect data in the data portion of the encapsulation message."
	AllenBradleySessionStatus64 = "An originator used an invalid session handle when sending an encapsulation message."
	AllenBradleySessionStatus65 = "The target received a message of invalid length."
	AllenBradleySessionStatus69 = "Unsupported encapsulation protocol revision."
	# Panasonic PLC related
	PanasonicReceiveLengthMustLargerThan9 = "The received data length must be greater than 9"
	PanasonicAddressParameterCannotBeNull = "Address parameter is not allowed to be empty"
	PanasonicMewStatus20 = "Error unknown"
	PanasonicMewStatus21 = "Nack error, the remote unit could not be correctly identified, or a data error occurred."
	PanasonicMewStatus22 = "WACK Error: The receive buffer for the remote unit is full."
	PanasonicMewStatus23 = "Multiple port error: The remote unit number (01 to 16) is set to repeat with the local unit."
	PanasonicMewStatus24 = "Transport format error: An attempt was made to send data that does not conform to the transport format, or a frame data overflow or a data error occurred."
	PanasonicMewStatus25 = "Hardware error: Transport system hardware stopped operation."
	PanasonicMewStatus26 = "Unit Number error: The remote unit's numbering setting exceeds the range of 01 to 63."
	PanasonicMewStatus27 = "Error not supported: Receiver data frame overflow. An attempt was made to send data of different frame lengths between different modules."
	PanasonicMewStatus28 = "No answer error: The remote unit does not exist. (timeout)."
	PanasonicMewStatus29 = "Buffer Close error: An attempt was made to send or receive a buffer that is in a closed state."
	PanasonicMewStatus30 = "Timeout error: Persisted in transport forbidden State."
	PanasonicMewStatus40 = "BCC Error: A transmission error occurred in the instruction data."
	PanasonicMewStatus41 = "Malformed: The sent instruction information does not conform to the transmission format."
	PanasonicMewStatus42 = "Error not supported: An unsupported instruction was sent. An instruction was sent to a target station that was not supported."
	PanasonicMewStatus43 = "Processing Step Error: Additional instructions were sent when the transfer request information was suspended."
	PanasonicMewStatus50 = "Link Settings Error: A link number that does not actually exist is set."
	PanasonicMewStatus51 = "Simultaneous operation error: When issuing instructions to other units, the transmit buffer for the local unit is full."
	PanasonicMewStatus52 = "Transport suppression Error: Unable to transfer to other units."
	PanasonicMewStatus53 = "Busy error: Other instructions are being processed when the command is received."
	PanasonicMewStatus60 = "Parameter error: Contains code that cannot be used in the directive, or the code does not have a zone specified parameter (X, Y, D), and so on."
	PanasonicMewStatus61 = "Data error: Contact number, area number, Data code format (BCD,HEX, etc.) overflow, overflow, and area specified error."
	PanasonicMewStatus62 = "Register ERROR: Excessive logging of data in an unregistered state of operations (Monitoring records, tracking records, etc.). )。"
	PanasonicMewStatus63 = "PLC mode error: When an instruction is issued, the run mode is not able to process the instruction."
	PanasonicMewStatus65 = "Protection Error: Performs a write operation to the program area or system register in the storage protection state."
	PanasonicMewStatus66 = "Address Error: Address (program address, absolute address, etc.) Data encoding form (BCD, hex, etc.), overflow, underflow, or specified range error."
	PanasonicMewStatus67 = "Missing data error: The data to be read does not exist. (reads data that is not written to the comment register.)"
	
	# Fatek PLC
	FatekStatus02 = "Illegal value"
	FatekStatus03 = "Write disabled"
	FatekStatus04 = "Invalid command code"
	FatekStatus05 = "Cannot be activated (down RUN command but Ladder Checksum does not match)"
	FatekStatus06 = "Cannot be activated (down RUN command but PLC ID ≠ Ladder ID)"
	FatekStatus07 = "Cannot be activated (down RUN command but program syntax error)"
	FatekStatus09 = "Cannot be activated (down RUN command, but the ladder program command PLC cannot be executed)"
	FatekStatus10 = "Illegal address"

	# Fuji PLC
	FujiSpbStatus01 = "Write to the ROM"
	FujiSpbStatus02 = "Received undefined commands or commands that could not be processed"
	FujiSpbStatus03 = "There is a contradiction in the data part (parameter exception)"
	FujiSpbStatus04 = "Unable to process due to transfer interlocks from other programmers"
	FujiSpbStatus05 = "The module number is incorrect"
	FujiSpbStatus06 = "Search item not found"
	FujiSpbStatus07 = "An address that exceeds the module range (when writing) is specified"
	FujiSpbStatus09 = "Unable to execute due to faulty program (RUN)"
	FujiSpbStatus0C = "Inconsistent password"


	def __setattr__(self, f, v):
		'''All properties is readonly, cannot change by setter'''
		raise AttributeError('{}.{} is READ ONLY'.format(type(self).__name__, f))


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
	
# ↓ Message About Implementation ==========================================================================================

class INetMessage:
	'''数据消息的基本基类'''
	def ProtocolHeadBytesLength(self):
		'''协议头数据长度，也即是第一次接收的数据长度'''
		return 0
	def GetContentLengthByHeadBytes(self):
		'''二次接收的数据长度'''
		return 0
	def CheckHeadBytesLegal(self,toke):
		'''令牌检查是否成功'''
		return False
	def GetHeadBytesIdentity(self):
		'''获取头子节里的消息标识'''
		return 0

	HeadBytes = bytes(0)
	ContentBytes = bytes(0)
	SendBytes = bytes(0)

class S7Message (INetMessage):
	'''西门子s7协议的消息接收规则'''
	def ProtocolHeadBytesLength(self):
		'''协议头数据长度，也即是第一次接收的数据长度'''
		return 4
	def GetContentLengthByHeadBytes(self):
		'''二次接收的数据长度'''
		if self.HeadBytes != None:
			return self.HeadBytes[2]*256 + self.HeadBytes[3]-4
		else:
			return 0
	def CheckHeadBytesLegal(self,token):
		'''令牌检查是否成功'''
		if self.HeadBytes != None:
			if self.HeadBytes[0] == 0x03 and self.HeadBytes[1] == 0x00:
				return True
			else:
				return False
		else:
			return False

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

class ModbusTcpMessage (INetMessage):
	'''Modbus-Tcp协议的信息'''
	def ProtocolHeadBytesLength(self):
		'''协议头数据长度，也即是第一次接收的数据长度'''
		return 6
	def GetContentLengthByHeadBytes(self):
		'''二次接收的数据长度'''
		if self.HeadBytes != None:
			return self.HeadBytes[4] * 256 + self.HeadBytes[5]
		else:
			return 0
	def CheckHeadBytesLegal(self,token):
		'''令牌检查是否成功'''
		return True
	def GetHeadBytesIdentity(self):
		'''获取头子节里的消息标识'''
		return self.HeadBytes[0] * 256 + self.HeadBytes[1]

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

class FinsMessage(INetMessage):
	'''用于欧姆龙通信的Fins协议的消息解析规则'''
	def ProtocolHeadBytesLength(self):
		'''协议头数据长度，也即是第一次接收的数据长度'''
		return 8
	def GetContentLengthByHeadBytes(self):
		'''二次接收的数据长度'''
		if self.HeadBytes != None:
			buffer = bytearray(4)
			buffer[0:4] = self.HeadBytes[4:8]
			return struct.unpack('>i',buffer)[0]
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

# ↑ Message About Implementation ==========================================================================================

# ↓ ByteTransform Implementation ==========================================================================================

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

# ↑ ByteTransform Implementation ==========================================================================================

class DeviceAddressBase:
	'''所有设备通信类的地址基础类'''
	Address = 0
	def AnalysisAddress( self, address: str ):
		'''解析字符串的地址'''
		self.Address = int(address)


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



# ↓ NetSupport Implementation ==========================================================================================

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

# ↑ NetSupport Implementation ==========================================================================================

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

class ModbusInfo:
	'''Modbus协议相关的一些信息'''
	@staticmethod
	def ReadCoil():
		'''读取线圈功能码'''
		return 0x01
	@staticmethod
	def ReadDiscrete():
		'''读取寄存器功能码'''
		return 0x02
	@staticmethod
	def ReadRegister():
		'''读取寄存器功能码'''
		return 0x03
	@staticmethod
	def ReadInputRegister():
		'''读取输入寄存器'''
		return 0x04
	@staticmethod
	def WriteOneCoil():
		'''写单个寄存器'''
		return 0x05
	@staticmethod
	def WriteOneRegister():
		'''写单个寄存器'''
		return 0x06
	@staticmethod
	def WriteCoil():
		'''写多个线圈'''
		return 0x0F
	@staticmethod
	def WriteRegister():
		'''写多个寄存器'''
		return 0x10
	@staticmethod
	def FunctionCodeNotSupport():
		'''不支持该功能码'''
		return 0x01
	@staticmethod
	def FunctionCodeOverBound():
		'''该地址越界'''
		return 0x02
	@staticmethod
	def FunctionCodeQuantityOver():
		'''读取长度超过最大值'''
		return 0x03
	@staticmethod
	def FunctionCodeReadWriteException():
		'''读写异常'''
		return 0x04
	@staticmethod
	def PackCommandToTcp( value, id ):
		'''将modbus指令打包成Modbus-Tcp指令'''
		buffer = bytearray( len(value) + 6)
		buffer[0:2] = struct.pack('>H',id)
		buffer[4:6] = struct.pack('>H',len(value))
		buffer[6:len(buffer)] = value
		return buffer
	@staticmethod
	def GetDescriptionByErrorCode( code ):
		'''通过错误码来获取到对应的文本消息'''
		if code == 0x01: return StringResources.Language.ModbusTcpFunctionCodeNotSupport
		elif code == 0x02: return StringResources.Language.ModbusTcpFunctionCodeOverBound
		elif code == 0x03: return StringResources.Language.ModbusTcpFunctionCodeQuantityOver
		elif code == 0x04: return StringResources.Language.ModbusTcpFunctionCodeReadWriteException
		else: return StringResources.Language.UnknownError
	@staticmethod
	def AnalysisReadAddress( address, isStartWithZero ):
		'''分析Modbus协议的地址信息，该地址适应于tcp及rtu模式'''
		try:
			mAddress = ModbusAddress(address)
			if isStartWithZero == False:
				if mAddress.Address < 1:
					raise RuntimeError(StringResources.Language.ModbusAddressMustMoreThanOne)
				else:
					mAddress.Address = mAddress.Address - 1
			return OperateResult.CreateSuccessResult(mAddress)
		except Exception as ex:
			return OperateResult( msg = str(ex))
			
	

class ModbusAddress(DeviceAddressBase):
	'''Modbus协议的地址类'''
	Station = 0
	Function = ModbusInfo.ReadRegister()
	def __init__(self, address = "0"):
		self.Station = -1
		self.Function = ModbusInfo.ReadRegister()
		self.Address = 0
		self.AnalysisAddress(address)

	def AnalysisAddress( self, address = "0" ):
		'''解析Modbus的地址码'''
		if address.find(';')>=0:
			listAddress = address.split(";")
			for index in range(len(listAddress)):
				if listAddress[index][0] == 's' or listAddress[index][0] == 'S':
					self.Station = int(listAddress[index][2:])
				elif listAddress[index][0] == 'x' or listAddress[index][0] == 'X':
					self.Function = int(listAddress[index][2:])
				else:
					self.Address = int(listAddress[index])
		else:
			self.Address = int(address)
	
	def CreateReadCoils( self, station, length ):
		'''创建一个读取线圈的字节对象'''
		buffer = bytearray(6)
		if self.Station < 0 :
			buffer[0] = station
		else:
			buffer[0] = self.Station
		buffer[1] = ModbusInfo.ReadCoil()
		buffer[2:4] = struct.pack('>H', self.Address)
		buffer[4:6] = struct.pack('>H', length)
		return buffer
	def CreateReadDiscrete( self, station, length ):
		'''创建一个读取离散输入的字节对象'''
		buffer = bytearray(6)
		if self.Station < 0 :
			buffer[0] = station
		else:
			buffer[0] = self.Station
		buffer[1] = ModbusInfo.ReadDiscrete()
		buffer[2:4] = struct.pack('>H', self.Address)
		buffer[4:6] = struct.pack('>H', length)
		return buffer
	def CreateReadRegister( self, station, length ):
		'''创建一个读取寄存器的字节对象'''
		buffer = bytearray(6)
		if self.Station < 0 :
			buffer[0] = station
		else:
			buffer[0] = self.Station
		buffer[1] = self.Function
		buffer[2:4] = struct.pack('>H', self.Address)
		buffer[4:6] = struct.pack('>H', length)
		return buffer
	def CreateReadInputRegister( self, station, length ):
		'''创建一个读取寄存器的字节对象'''
		buffer = bytearray(6)
		if self.Station < 0 :
			buffer[0] = station
		else:
			buffer[0] = self.Station
		buffer[1] = ModbusInfo.ReadInputRegister()
		buffer[2:4] = struct.pack('>H', self.Address)
		buffer[4:6] = struct.pack('>H', length)
		return buffer
	def CreateWriteOneCoil(self, station, value):
		'''创建一个写入单个线圈的指令'''
		buffer = bytearray(6)
		if self.Station < 0 :
			buffer[0] = station
		else:
			buffer[0] = self.Station
		buffer[1] = ModbusInfo.WriteOneCoil()
		buffer[2:4] = struct.pack('>H', self.Address)
		if value == True:
			buffer[4] = 0xFF
		return buffer
	def CreateWriteOneRegister(self, station, values):
		'''创建一个写入单个寄存器的指令'''
		buffer = bytearray(6)
		if self.Station < 0 :
			buffer[0] = station
		else:
			buffer[0] = self.Station
		buffer[1] = ModbusInfo.WriteOneRegister()
		buffer[2:4] = struct.pack('>H', self.Address)
		buffer[4:6] = values
		return buffer
	def CreateWriteCoil(self, station, values):
		'''创建一个写入批量线圈的指令'''
		data = SoftBasic.BoolArrayToByte( values )
		buffer = bytearray(7 + len(data))
		if self.Station < 0 :
			buffer[0] = station
		else:
			buffer[0] = self.Station
		buffer[1] = ModbusInfo.WriteCoil()
		buffer[2:4] = struct.pack('>H', self.Address)
		buffer[4:6] = struct.pack('>H', len(values))
		buffer[6] = len(data)
		buffer[7:len(buffer)] = data
		return buffer
	def CreateWriteRegister(self, station, values):
		'''创建一个写入批量寄存器的指令'''
		buffer = bytearray(7 + len(values))
		if self.Station < 0 :
			buffer[0] = station
		else:
			buffer[0] = self.Station
		buffer[1] = ModbusInfo.WriteRegister()
		buffer[2:4] = struct.pack('>H', self.Address)
		buffer[4:6] = struct.pack('>H', len(values)//2)
		buffer[6] = len(values)
		buffer[7:len(buffer)] = values
		return buffer
	def AddressAdd(self, value):
		'''地址新增指定的数'''
		modbusAddress = ModbusAddress()
		modbusAddress.Station = self.Station
		modbusAddress.Function = self.Function
		modbusAddress.Address = self.Address+value
		return modbusAddress




class ModbusTcpNet(NetworkDeviceBase):
	'''Modbus-Tcp协议的客户端通讯类，方便的和服务器进行数据交互'''
	def __init__(self, ipAddress = '127.0.0.1', port = 502, station = 1):
		super().__init__()
		'''实例化一个MOdbus-Tcp协议的客户端对象'''
		self.WordLength = 1
		self.isAddressStartWithZero = True
		self.softIncrementCount = SoftIncrementCount( 65536, 0 )
		self.station = station
		self.ipAddress = ipAddress
		self.port = port
		self.byteTransform = ReverseWordTransform()
		self.iNetMessage = ModbusTcpMessage()
	def SetDataFormat( self, value ):
		'''多字节的数据是否高低位反转，该设置的改变会影响Int32,UInt32,float,double,Int64,UInt64类型的读写'''
		self.byteTransform.DataFormat = value
	def GetDataFormat( self ):
		'''多字节的数据是否高低位反转，该设置的改变会影响Int32,UInt32,float,double,Int64,UInt64类型的读写'''
		return self.byteTransform.DataFormat
	def SetIsStringReverse( self, value ):
		'''字符串数据是否按照字来反转'''
		self.byteTransform.IsStringReverse = value
	def GetIsStringReverse( self ):
		'''字符串数据是否按照字来反转'''
		return self.byteTransform.IsStringReverse
	def BuildReadCoilCommand(self, address, length):
		'''生成一个读取线圈的指令头'''
		# 分析地址
		analysis = ModbusInfo.AnalysisReadAddress( address, self.isAddressStartWithZero )
		if analysis.IsSuccess == False: return OperateResult.CreateFailedResult(analysis)
		# 获取消息号
		messageId = self.softIncrementCount.GetCurrentValue()
		#生成最终的指令
		buffer = ModbusInfo.PackCommandToTcp(analysis.Content.CreateReadCoils( self.station, length ), messageId)
		return OperateResult.CreateSuccessResult(buffer)
	def BuildReadDiscreteCommand(self, address, length):
		'''生成一个读取离散信息的指令头'''
		# 分析地址
		analysis = ModbusInfo.AnalysisReadAddress( address, self.isAddressStartWithZero )
		if analysis.IsSuccess == False: return OperateResult.CreateFailedResult(analysis)
		# 获取消息号
		messageId = self.softIncrementCount.GetCurrentValue()
		buffer = ModbusInfo.PackCommandToTcp(analysis.Content.CreateReadDiscrete(self.station,length), messageId)
		return OperateResult.CreateSuccessResult(buffer)
	def BuildReadRegisterCommand(self, address, length):
		'''创建一个读取寄存器的字节对象'''
		analysis = ModbusInfo.AnalysisReadAddress( address, self.isAddressStartWithZero )
		if analysis.IsSuccess == False: return OperateResult.CreateFailedResult(analysis)
		# 获取消息号
		messageId = self.softIncrementCount.GetCurrentValue()
		buffer = ModbusInfo.PackCommandToTcp(analysis.Content.CreateReadRegister(self.station,length), messageId)
		return OperateResult.CreateSuccessResult(buffer)
	def BuildReadInputRegisterCommand(self, address, length):
		'''创建一个读取寄存器的字节对象'''
		analysis = ModbusInfo.AnalysisReadAddress( address, self.isAddressStartWithZero )
		if analysis.IsSuccess == False: return OperateResult.CreateFailedResult(analysis)
		# 获取消息号
		messageId = self.softIncrementCount.GetCurrentValue()
		buffer = ModbusInfo.PackCommandToTcp(analysis.Content.CreateReadInputRegister(self.station,length), messageId)
		return OperateResult.CreateSuccessResult(buffer)
	def BuildWriteOneCoilCommand(self, address,value):
		'''生成一个写入单线圈的指令头'''
		analysis = ModbusInfo.AnalysisReadAddress( address, self.isAddressStartWithZero )
		if analysis.IsSuccess == False: return OperateResult.CreateFailedResult(analysis)
		# 获取消息号
		messageId = self.softIncrementCount.GetCurrentValue()
		buffer = ModbusInfo.PackCommandToTcp(analysis.Content.CreateWriteOneCoil(self.station,value), messageId)
		return OperateResult.CreateSuccessResult(buffer)
	def BuildWriteOneRegisterCommand(self, address, values):
		'''生成一个写入单个寄存器的报文'''
		analysis = ModbusInfo.AnalysisReadAddress( address, self.isAddressStartWithZero )
		if analysis.IsSuccess == False: return OperateResult.CreateFailedResult(analysis)
		# 获取消息号
		messageId = self.softIncrementCount.GetCurrentValue()
		buffer = ModbusInfo.PackCommandToTcp(analysis.Content.CreateWriteOneRegister(self.station,values), messageId)
		return OperateResult.CreateSuccessResult(buffer)
	def BuildWriteCoilCommand(self, address, values):
		'''生成批量写入单个线圈的报文信息，需要传入bool数组信息'''
		analysis = ModbusInfo.AnalysisReadAddress( address, self.isAddressStartWithZero )
		if analysis.IsSuccess == False: return OperateResult.CreateFailedResult(analysis)
		# 获取消息号
		messageId = self.softIncrementCount.GetCurrentValue()
		buffer = ModbusInfo.PackCommandToTcp(analysis.Content.CreateWriteCoil(self.station,values), messageId)
		return OperateResult.CreateSuccessResult(buffer)
	def BuildWriteRegisterCommand(self, address, values):
		'''生成批量写入寄存器的报文信息，需要传入byte数组'''
		analysis = ModbusInfo.AnalysisReadAddress( address, self.isAddressStartWithZero )
		if analysis.IsSuccess == False: return OperateResult.CreateFailedResult(analysis)
		# 获取消息号
		messageId = self.softIncrementCount.GetCurrentValue()
		buffer = ModbusInfo.PackCommandToTcp(analysis.Content.CreateWriteRegister(self.station,values), messageId)
		return OperateResult.CreateSuccessResult(buffer)
	def BuildReadModbusAddressCommand( self, address, length ):
		'''生成一个读取寄存器的指令头，address->ModbusAddress'''
		# 获取消息号
		messageId =  self.softIncrementCount.GetCurrentValue()
		# 生成最终tcp指令
		buffer = ModbusInfo.PackCommandToTcp( address.CreateReadRegister( self.station, length ), messageId )
		return OperateResult.CreateSuccessResult( buffer )
	def CheckModbusTcpResponse( self, send ):
		'''检查当前的Modbus-Tcp响应是否是正确的'''
		resultBytes = self.ReadFromCoreServer( send )
		if resultBytes.IsSuccess == True:
			if (send[7] + 0x80) == resultBytes.Content[7]:
				# 发生了错误
				resultBytes.IsSuccess = False
				resultBytes.Message = ModbusInfo.GetDescriptionByErrorCode( resultBytes.Content[8] )
				resultBytes.ErrorCode = resultBytes.Content[8]
		return resultBytes
	def ReadModBusBase( self, code, address, length ):
		'''检查当前的Modbus-Tcp响应是否是正确的'''
		command = None
		if code == ModbusInfo.ReadCoil():
			command = self.BuildReadCoilCommand( address, length )
		elif code == ModbusInfo.ReadDiscrete():
			command = self.BuildReadDiscreteCommand( address, length )
		elif code == ModbusInfo.ReadRegister():
			command = self.BuildReadRegisterCommand( address, length )
		elif code == ModbusInfo.ReadInputRegister():
			command = self.BuildReadInputRegisterCommand( address, length )
		else:
			command = OperateResult( msg = StringResources.Language.ModbusTcpFunctionCodeNotSupport )
		if command.IsSuccess == False : return OperateResult.CreateFailedResult( command )

		resultBytes = self.CheckModbusTcpResponse( command.Content )
		if resultBytes.IsSuccess == True:
			# 二次数据处理
			if len(resultBytes.Content) >= 9:
				buffer = bytearray(len(resultBytes.Content) - 9)
				buffer[0:len(buffer)] = resultBytes.Content[9:]
				resultBytes.Content = buffer
		return resultBytes
	def ReadModBusAddressBase( self, address, length = 1 ):
		'''读取服务器的数据，需要指定不同的功能码'''
		command = self.BuildReadModbusAddressCommand( address, length )
		if command.IsSuccess == False: return OperateResult.CreateFailedResult(command)

		resultBytes = self.CheckModbusTcpResponse( command.Content )
		if resultBytes.IsSuccess == True:
			# 二次数据处理
			if len(resultBytes.Content) >= 9:
				buffer = bytearray(len(resultBytes.Content) - 9)
				buffer[0:len(buffer)] = resultBytes.Content[9:]
				resultBytes.Content = buffer
		return resultBytes
	def ReadCoil( self, address, length = None):
		'''批量的读取线圈，需要指定起始地址，读取长度可选'''
		if length == None:
			read = self.ReadCoil( address, 1 )
			if read.IsSuccess == False : return OperateResult.CreateFailedResult( read )
			return OperateResult.CreateSuccessResult( read.Content[0] )
		else:
			read = self.ReadModBusBase( ModbusInfo.ReadCoil(), address, length )
			if read.IsSuccess == False : return OperateResult.CreateFailedResult( read )

			return OperateResult.CreateSuccessResult( SoftBasic.ByteToBoolArray( read.Content, length ) )
	def ReadDiscrete( self, address, length = None):
		'''批量的读取输入点，需要指定起始地址，可选读取长度'''
		if length == None:
			read = self.ReadDiscrete( address, 1 )
			if read.IsSuccess == False : return OperateResult.CreateFailedResult( read )
			return OperateResult.CreateSuccessResult( read.Content[0] )
		else:
			read = self.ReadModBusBase( ModbusInfo.ReadDiscrete(), address, length )
			if read.IsSuccess == False : return OperateResult.CreateFailedResult( read )
			
			return OperateResult.CreateSuccessResult( SoftBasic.ByteToBoolArray( read.Content, length ) )
	def Read( self, address, length ):
		'''从Modbus服务器批量读取寄存器的信息，需要指定起始地址，读取长度'''
		analysis = ModbusInfo.AnalysisReadAddress( address, self.isAddressStartWithZero )
		if analysis.IsSuccess == False : return OperateResult.CreateFailedResult( analysis )
		return self.ReadModBusAddressBase( analysis.Content, length )
	def WriteOneRegister( self, address, value ):
		'''写一个寄存器数据'''
		if type(value) == list:
			command = self.BuildWriteOneRegisterCommand( address, value )
			if command.IsSuccess == False : return command
			return self.CheckModbusTcpResponse( command.Content )
		else:
			return self.WriteOneRegister(address, struct.pack('>H', value))
	def Write( self, address, value ):
		'''将数据写入到Modbus的寄存器上去，需要指定起始地址和数据内容'''
		command = self.BuildWriteRegisterCommand( address, value )
		if command.IsSuccess == False:
			return command

		return self.CheckModbusTcpResponse( command.Content )
	def WriteCoil( self, address, value ):
		'''批量写线圈信息，指定是否通断'''
		if type(value) == list:
			command = self.BuildWriteCoilCommand( address, value )
			if command.IsSuccess == False : return command
			return self.CheckModbusTcpResponse( command.Content )
		else:
			command = self.BuildWriteOneCoilCommand( address, value )
			if command.IsSuccess == False : return command
			return self.CheckModbusTcpResponse( command.Content )
	def WriteBool( self, address, values ):
		'''批量写寄存器的数据内容'''
		return self.Write( address, SoftBasic.BoolArrayToByte( values ) )

# 三菱的类库
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

# 西门子的数据类
class SiemensPLCS(Enum):
	'''西门子PLC的类型对象'''
	S1200 = 0
	S300 = 1
	S400 = 2
	S1500 = 3
	S200Smart = 4
class SiemensS7Net(NetworkDeviceBase):
	'''一个西门子的客户端类，使用S7协议来进行数据交互，支持s200smart，s300，s400，s1200，s1500的通讯
	
	在实例化的时候除了需要指定PLC型号，ip地址之外，有些特殊的plc是需要设置机架号和槽号的，示例的示例如下：

	siemens = SiemensS7Net(SiemensPLCS.S1200, "192.168.8.13")

	siemens.SetSlotAndRack(0, 2)  # 这行代码不是必须的，S400系列时需要根据实际来进行设置，才能正确的读到数据
	'''
	def __init__(self, siemens, ipAddress = "127.0.0.1"):
		super().__init__()
		'''实例化一个西门子的S7协议的通讯对象并指定Ip地址'''
		self.CurrentPlc = SiemensPLCS.S1200
		self.plcHead1 = bytearray([0x03,0x00,0x00,0x16,0x11,0xE0,0x00,0x00,0x00,0x01,0x00,0xC0,0x01,0x0A,0xC1,0x02,0x01,0x02,0xC2,0x02,0x01,0x00])
		self.plcHead2 = bytearray([0x03,0x00,0x00,0x19,0x02,0xF0,0x80,0x32,0x01,0x00,0x00,0x04,0x00,0x00,0x08,0x00,0x00,0xF0,0x00,0x00,0x01,0x00,0x01,0x01,0xE0])
		self.plcOrderNumber = bytearray([0x03,0x00,0x00,0x21,0x02,0xF0,0x80,0x32,0x07,0x00,0x00,0x00,0x01,0x00,0x08,0x00,0x08,0x00,0x01,0x12,0x04,0x11,0x44,0x01,0x00,0xFF,0x09,0x00,0x04,0x00,0x11,0x00,0x00])
		self.plcHead1_200smart = bytearray([0x03,0x00,0x00,0x16,0x11,0xE0,0x00,0x00,0x00,0x01,0x00,0xC1,0x02,0x10,0x00,0xC2,0x02,0x03,0x00,0xC0,0x01,0x0A])
		self.plcHead2_200smart = bytearray([0x03,0x00,0x00,0x19,0x02,0xF0,0x80,0x32,0x01,0x00,0x00,0xCC,0xC1,0x00,0x08,0x00,0x00,0xF0,0x00,0x00,0x01,0x00,0x01,0x03,0xC0])
		self.WordLength = 2
		self.ipAddress = ipAddress
		self.port = 102
		self.CurrentPlc = siemens
		self.iNetMessage = S7Message()
		self.byteTransform = ReverseBytesTransform()

		if siemens == SiemensPLCS.S1200:
			self.plcHead1[21] = 0
		elif siemens == SiemensPLCS.S300:
			self.plcHead1[21] = 2
		elif siemens == SiemensPLCS.S400:
			self.plcHead1[21] = 3
			self.plcHead1[17] = 0x00
		elif siemens == SiemensPLCS.S1500:
			self.plcHead1[21] = 0
		elif siemens == SiemensPLCS.S200Smart:
			self.plcHead1 = self.plcHead1_200smart
			self.plcHead2 = self.plcHead2_200smart
		else:
			self.plcHead1[18] = 0
	@staticmethod
	def CalculateAddressStarted( address = "M0" ):
		'''计算特殊的地址信息'''
		if address.find('.') >= 0:
			temp = address.split(".")
			return int(temp[0]) * 8 + int(temp[1])
		else:
			return int( address ) * 8
	@staticmethod
	def AnalysisAddress( address = 'M0' ):
		'''解析数据地址，解析出地址类型，起始地址，DB块的地址'''
		result = OperateResult( )
		try:
			result.Content3 = 0
			if address[0] == 'I':
				result.Content1 = 0x81
				result.Content2 = SiemensS7Net.CalculateAddressStarted( address[1:] )
			elif address[0] == 'Q':
				result.Content1 = 0x82
				result.Content2 = SiemensS7Net.CalculateAddressStarted( address[1:] )
			elif address[0] == 'M':
				result.Content1 = 0x83
				result.Content2 = SiemensS7Net.CalculateAddressStarted( address[1:] )
			elif address[0] == 'D' or address[0:2] == "DB":
				result.Content1 = 0x84
				adds = address.split(".")
				if address[1] == 'B':
					result.Content3 = int( adds[0][2:] )
				else:
					result.Content3 = int( adds[0][1:] )
				result.Content2 = SiemensS7Net.CalculateAddressStarted( address[ (address.find( '.' ) + 1):]) 
			elif address[0] == 'T':
				result.Content1 = 0x1D
				result.Content2 = SiemensS7Net.CalculateAddressStarted( address[1:] )
			elif address[0] == 'C':
				result.Content1 = 0x1C
				result.Content2 = SiemensS7Net.CalculateAddressStarted( address[1:] )
			elif address[0] == 'V':
				result.Content1 = 0x84
				result.Content3 = 1
				result.Content2 = SiemensS7Net.CalculateAddressStarted( address[1:] )
			else:
				result.Message = StringResources.Language.NotSupportedDataType
				result.Content1 = 0
				result.Content2 = 0
				result.Content3 = 0
				return result
		except Exception as ex:
			result.Message = str(ex)
			return result

		result.IsSuccess = True
		return result
	@staticmethod
	def BuildReadCommand( address, length ):
		'''生成一个读取字数据指令头的通用方法'''
		if address == None : raise Exception( "address" )
		if length == None : raise Exception( "count" )
		if len(address) != len(length) : raise Exception( "两个参数的个数不统一" )
		if len(length) > 19 : raise Exception( "读取的数组数量不允许大于19" )

		readCount = len(length)
		_PLCCommand = bytearray(19 + readCount * 12)
		# ======================================================================================
		_PLCCommand[0] = 0x03                                                # 报文头
		_PLCCommand[1] = 0x00
		_PLCCommand[2] = len(_PLCCommand) // 256                           # 长度
		_PLCCommand[3] = len(_PLCCommand) % 256
		_PLCCommand[4] = 0x02                                                # 固定
		_PLCCommand[5] = 0xF0
		_PLCCommand[6] = 0x80
		_PLCCommand[7] = 0x32                                                # 协议标识
		_PLCCommand[8] = 0x01                                                # 命令：发
		_PLCCommand[9] = 0x00                                                # redundancy identification (reserved): 0x0000;
		_PLCCommand[10] = 0x00                                               # protocol data unit reference; it’s increased by request event;
		_PLCCommand[11] = 0x00
		_PLCCommand[12] = 0x01                                               # 参数命令数据总长度
		_PLCCommand[13] = (len(_PLCCommand) - 17) // 256
		_PLCCommand[14] = (len(_PLCCommand) - 17) % 256
		_PLCCommand[15] = 0x00                                               # 读取内部数据时为00，读取CPU型号为Data数据长度
		_PLCCommand[16] = 0x00
		# =====================================================================================
		_PLCCommand[17] = 0x04                                               # 读写指令，04读，05写
		_PLCCommand[18] = readCount                                    # 读取数据块个数

		for ii in range(readCount):
			#===========================================================================================
			# 指定有效值类型
			_PLCCommand[19 + ii * 12] = 0x12
			# 接下来本次地址访问长度
			_PLCCommand[20 + ii * 12] = 0x0A
			# 语法标记，ANY
			_PLCCommand[21 + ii * 12] = 0x10
			# 按字为单位
			_PLCCommand[22 + ii * 12] = 0x02
			# 访问数据的个数
			_PLCCommand[23 + ii * 12] = length[ii] // 256
			_PLCCommand[24 + ii * 12] = length[ii] % 256
			# DB块编号，如果访问的是DB块的话
			_PLCCommand[25 + ii * 12] = address[ii].Content3 // 256
			_PLCCommand[26 + ii * 12] = address[ii].Content3 % 256
			# 访问数据类型
			_PLCCommand[27 + ii * 12] = address[ii].Content1
			# 偏移位置
			_PLCCommand[28 + ii * 12] = address[ii].Content2 // 256 // 256 % 256
			_PLCCommand[29 + ii * 12] = address[ii].Content2 // 256 % 256
			_PLCCommand[30 + ii * 12] = address[ii].Content2 % 256

		return OperateResult.CreateSuccessResult( _PLCCommand )
	@staticmethod
	def BuildBitReadCommand( address ):
		'''生成一个位读取数据指令头的通用方法'''
		analysis = SiemensS7Net.AnalysisAddress( address )
		if analysis.IsSuccess == False : return OperateResult.CreateFailedResult( analysis )

		_PLCCommand = bytearray(31)
		# 报文头
		_PLCCommand[0] = 0x03
		_PLCCommand[1] = 0x00
		# 长度
		_PLCCommand[2] = len(_PLCCommand) // 256
		_PLCCommand[3] = len(_PLCCommand) % 256
		# 固定
		_PLCCommand[4] = 0x02
		_PLCCommand[5] = 0xF0
		_PLCCommand[6] = 0x80
		_PLCCommand[7] = 0x32
		# 命令：发
		_PLCCommand[8] = 0x01
		# 标识序列号
		_PLCCommand[9] = 0x00
		_PLCCommand[10] = 0x00
		_PLCCommand[11] = 0x00
		_PLCCommand[12] = 0x01
		# 命令数据总长度
		_PLCCommand[13] = (len(_PLCCommand) - 17) // 256
		_PLCCommand[14] = (len(_PLCCommand) - 17) % 256

		_PLCCommand[15] = 0x00
		_PLCCommand[16] = 0x00

		# 命令起始符
		_PLCCommand[17] = 0x04
		# 读取数据块个数
		_PLCCommand[18] = 0x01

		#===========================================================================================
		# 读取地址的前缀
		_PLCCommand[19] = 0x12
		_PLCCommand[20] = 0x0A
		_PLCCommand[21] = 0x10
		# 读取的数据时位
		_PLCCommand[22] = 0x01
		# 访问数据的个数
		_PLCCommand[23] = 0x00
		_PLCCommand[24] = 0x01
		# DB块编号，如果访问的是DB块的话
		_PLCCommand[25] = analysis.Content3 // 256
		_PLCCommand[26] = analysis.Content3 % 256
		# 访问数据类型
		_PLCCommand[27] = analysis.Content1
		# 偏移位置
		_PLCCommand[28] = analysis.Content2 // 256 // 256 % 256
		_PLCCommand[29] = analysis.Content2 // 256 % 256
		_PLCCommand[30] = analysis.Content2 % 256

		return OperateResult.CreateSuccessResult( _PLCCommand )
	@staticmethod
	def BuildWriteByteCommand( address, data ):
		'''生成一个写入字节数据的指令'''
		if data == None : data = bytearray(0)
		analysis = SiemensS7Net.AnalysisAddress( address )
		if analysis.IsSuccess == False : return OperateResult.CreateFailedResult(analysis)

		_PLCCommand = bytearray(35 + len(data))
		_PLCCommand[0] = 0x03
		_PLCCommand[1] = 0x00
		# 长度
		_PLCCommand[2] = (35 + len(data)) // 256
		_PLCCommand[3] = (35 + len(data)) % 256
		# 固定
		_PLCCommand[4] = 0x02
		_PLCCommand[5] = 0xF0
		_PLCCommand[6] = 0x80
		_PLCCommand[7] = 0x32
		# 命令 发
		_PLCCommand[8] = 0x01
		# 标识序列号
		_PLCCommand[9] = 0x00
		_PLCCommand[10] = 0x00
		_PLCCommand[11] = 0x00
		_PLCCommand[12] = 0x01
		# 固定
		_PLCCommand[13] = 0x00
		_PLCCommand[14] = 0x0E
		# 写入长度+4
		_PLCCommand[15] = (4 + len(data)) // 256
		_PLCCommand[16] = (4 + len(data)) % 256
		# 读写指令
		_PLCCommand[17] = 0x05
		# 写入数据块个数
		_PLCCommand[18] = 0x01
		# 固定，返回数据长度
		_PLCCommand[19] = 0x12
		_PLCCommand[20] = 0x0A
		_PLCCommand[21] = 0x10
		# 写入方式，1是按位，2是按字
		_PLCCommand[22] = 0x02
		# 写入数据的个数
		_PLCCommand[23] = len(data) // 256
		_PLCCommand[24] = len(data) % 256
		# DB块编号，如果访问的是DB块的话
		_PLCCommand[25] = analysis.Content3 // 256
		_PLCCommand[26] = analysis.Content3 % 256
		# 写入数据的类型
		_PLCCommand[27] = analysis.Content1
		# 偏移位置
		_PLCCommand[28] = analysis.Content2 // 256 // 256 % 256
		_PLCCommand[29] = analysis.Content2 // 256 % 256
		_PLCCommand[30] = analysis.Content2 % 256
		# 按字写入
		_PLCCommand[31] = 0x00
		_PLCCommand[32] = 0x04
		# 按位计算的长度
		_PLCCommand[33] = len(data) * 8 // 256
		_PLCCommand[34] = len(data) * 8 % 256

		_PLCCommand[35:] = data

		return OperateResult.CreateSuccessResult(_PLCCommand)
	@staticmethod
	def BuildWriteBitCommand( address, data ):
		analysis = SiemensS7Net.AnalysisAddress( address )
		if analysis.IsSuccess == False : return OperateResult.CreateFailedResult(analysis)

		buffer = bytearray(1)
		if data == True : buffer[0] = 0x01

		_PLCCommand = bytearray(35 + len(buffer))
		_PLCCommand[0] = 0x03
		_PLCCommand[1] = 0x00
		# 长度
		_PLCCommand[2] = (35 + len(buffer)) // 256
		_PLCCommand[3] = (35 + len(buffer)) % 256
		# 固定
		_PLCCommand[4] = 0x02
		_PLCCommand[5] = 0xF0
		_PLCCommand[6] = 0x80
		_PLCCommand[7] = 0x32
		# 命令 发
		_PLCCommand[8] = 0x01
		# 标识序列号
		_PLCCommand[9] = 0x00
		_PLCCommand[10] = 0x00
		_PLCCommand[11] = 0x00
		_PLCCommand[12] = 0x01
		# 固定
		_PLCCommand[13] = 0x00
		_PLCCommand[14] = 0x0E
		# 写入长度+4
		_PLCCommand[15] = (4 + len(buffer)) // 256
		_PLCCommand[16] = (4 + len(buffer)) % 256
		# 命令起始符
		_PLCCommand[17] = 0x05
		# 写入数据块个数
		_PLCCommand[18] = 0x01
		_PLCCommand[19] = 0x12
		_PLCCommand[20] = 0x0A
		_PLCCommand[21] = 0x10
		# 写入方式，1是按位，2是按字
		_PLCCommand[22] = 0x01
		# 写入数据的个数
		_PLCCommand[23] = len(buffer) // 256
		_PLCCommand[24] = len(buffer) % 256
		# DB块编号，如果访问的是DB块的话
		_PLCCommand[25] = analysis.Content3 // 256
		_PLCCommand[26] = analysis.Content3 % 256
		# 写入数据的类型
		_PLCCommand[27] = analysis.Content1
		# 偏移位置
		_PLCCommand[28] = analysis.Content2 // 256 // 256
		_PLCCommand[29] = analysis.Content2 // 256
		_PLCCommand[30] = analysis.Content2 % 256
		# 按位写入
		_PLCCommand[31] = 0x00
		_PLCCommand[32] = 0x03
		# 按位计算的长度
		_PLCCommand[33] = len(buffer) // 256
		_PLCCommand[34] = len(buffer) % 256

		_PLCCommand[35:] = buffer

		return OperateResult.CreateSuccessResult(_PLCCommand)
	def SetSlotAndRack(self, rack, slot):
		'''设置西门字的机架号和槽号的信息，当和400PLC通信时就需要动态来调整'''
		self.plcHead1[21] = (rack * 0x20) + slot
	def InitializationOnConnect( self, socket ):
		'''连接上服务器后需要进行的二次握手操作'''
		# msg = SoftBasic.ByteToHexString(self.plcHead1, ' ')
		# 第一次握手
		read_first = self.ReadFromCoreServerBase( socket, self.plcHead1 )
		if read_first.IsSuccess == False : return read_first

		# 第二次握手
		read_second = self.ReadFromCoreServerBase( socket, self.plcHead2 )
		if read_second.IsSuccess == False : return read_second

		# 返回成功的信号
		return OperateResult.CreateSuccessResult( )
	def ReadOrderNumber( self ):
		'''从PLC读取订货号信息'''
		read = self.ReadFromCoreServer( self.plcOrderNumber )
		if read.IsSuccess == False : return OperateResult.CreateFailedResult( read )

		return OperateResult.CreateSuccessResult( read.Content[71:92].decode('ascii') )
	def __ReadBase( self, address, length ):
		'''基础的读取方法，外界不应该调用本方法'''
		command = SiemensS7Net.BuildReadCommand( address, length )
		if command.IsSuccess == False : return command

		read = self.ReadFromCoreServer( command.Content )
		if read.IsSuccess == False : return read

		# 分析结果
		receiveCount = 0
		for i in range(len(length)):
			receiveCount += length[i]

		if len(read.Content) >= 21 and read.Content[20] == len(length) :
			buffer = bytearray(receiveCount)
			kk = 0
			ll = 0
			ii = 21
			while ii < len(read.Content):
				if ii + 1 < len(read.Content):
					if read.Content[ii] == 0xFF and read.Content[ii + 1] == 0x04:
						# 有数据
						buffer[ll : ll + length[kk]] = read.Content[ii+4 : ii+4+length[kk]]
						ii += length[kk] + 3
						ll += length[kk]
						kk += 1
				ii += 1
			return OperateResult.CreateSuccessResult( buffer )
		else :
			result = OperateResult()
			result.ErrorCode = read.ErrorCode
			result.Message = StringResources.Language.SiemensDataLengthCheckFailed
			return result
	
	def Read( self, address, length ):
		'''从PLC读取数据，地址格式为I100，Q100，DB20.100，M100，T100，C100以字节为单位'''
		if type(address) == list and type(length) == list:
			addressResult = []
			for i in range(length):
				tmp = SiemensS7Net.AnalysisAddress( address[i] )
				if tmp.IsSuccess == False : return OperateResult.CreateFailedResult( addressResult[i] )

				addressResult.append( tmp )
			return self.__ReadBase( addressResult, length )
		else:
			addressResult = SiemensS7Net.AnalysisAddress( address )
			if addressResult.IsSuccess == False : return OperateResult.CreateFailedResult( addressResult )

			bytesContent = bytearray()
			alreadyFinished = 0
			while alreadyFinished < length :
				readLength = min( length - alreadyFinished, 200 )
				read = self.__ReadBase( [ addressResult ], [ readLength ] )
				if read.IsSuccess == True :
					bytesContent.extend( read.Content )
				else:
					return read

				alreadyFinished += readLength
				addressResult.Content2 += readLength * 8

			return OperateResult.CreateSuccessResult( bytesContent )
	def __ReadBitFromPLC( self, address ):
		'''从PLC读取数据，地址格式为I100，Q100，DB20.100，M100，以位为单位'''
		# 指令生成
		command = SiemensS7Net.BuildBitReadCommand( address )
		if command.IsSuccess == False : return OperateResult.CreateFailedResult( command )

		# 核心交互
		read = self.ReadFromCoreServer( command.Content )
		if read.IsSuccess == False : return read

		# 分析结果
		receiveCount = 1
		if len(read.Content) >= 21 and read.Content[20] == 1 :
			buffer = bytearray(receiveCount)
			if 22 < len(read.Content) :
				if read.Content[21] == 0xFF and read.Content[22] == 0x03:
					# 有数据
					buffer[0] = read.Content[25]
			return OperateResult.CreateSuccessResult( buffer )
		else:
			result = OperateResult()
			result.ErrorCode = read.ErrorCode
			result.Message = StringResources.Language.SiemensDataLengthCheckFailed
			return result
	def ReadBool( self, address ):
		'''读取指定地址的bool数据'''
		return ByteTransformHelper.GetResultFromBytes( self.__ReadBitFromPLC( address ), lambda m: self.byteTransform.TransBool( m, 0 ) )
	def ReadByte( self, address ):
		'''读取指定地址的byte数据'''
		return ByteTransformHelper.GetResultFromArray( self.Read( address, 1 ) )
	def __WriteBase( self, entireValue ):
		'''基础的写入数据的操作支持'''
		write = self.ReadFromCoreServer( entireValue )
		if write.IsSuccess == False : return write

		if write.Content[len(write.Content) - 1] != 0xFF :
			# 写入异常
			return OperateResult( msg = "写入数据异常", err = write.Content[write.Content.Length - 1])
		else:
			return OperateResult.CreateSuccessResult( )
	def Write( self, address, value ):
		'''将数据写入到PLC数据，地址格式为I100，Q100，DB20.100，M100，以字节为单位'''
		command = self.BuildWriteByteCommand( address, value )
		if command.IsSuccess == False : return command

		return self.__WriteBase( command.Content )
	def WriteBool( self, address, value ):
		'''写入PLC的一个位，例如"M100.6"，"I100.7"，"Q100.0"，"DB20.100.0"，如果只写了"M100"默认为"M100.0'''
		# 生成指令
		command = SiemensS7Net.BuildWriteBitCommand( address, value )
		if command.IsSuccess == False : return command

		return self.__WriteBase( command.Content )
	def WriteByte( self, address, value ):
		'''向PLC中写入byte数据，返回值说明'''
		return self.Write( address, [value] )
class SiemensFetchWriteNet(NetworkDeviceBase):
	'''使用了Fetch/Write协议来和西门子进行通讯，该种方法需要在PLC侧进行一些配置'''
	def __init__( self, ipAddress = '127.0.0.1', port = 1000 ):
		''' 实例化一个西门子的Fetch/Write协议的通讯对象，可以指定ip地址及端口号'''
		super().__init__()
		self.ipAddress = ipAddress
		self.port = port
		self.WordLength = 2
	@staticmethod
	def CalculateAddressStarted( address = "M100" ):
		'''计算特殊的地址信息'''
		if address.find( '.' ) < 0:
			return int( address )
		else:
			temp = address.split( '.' )
			return int( temp[0] )
	@staticmethod
	def AnalysisAddress( address = "M100" ):
		'''解析数据地址，解析出地址类型，起始地址，DB块的地址'''
		result = OperateResult( )
		try:
			result.Content3 = 0
			if address[0] == 'I':
				result.Content1 = 0x03
				result.Content2 = SiemensFetchWriteNet.CalculateAddressStarted( address[1:] )
			elif address[0] == 'Q':
				result.Content1 = 0x04
				result.Content2 = SiemensFetchWriteNet.CalculateAddressStarted( address[1:] )
			elif address[0] == 'M':
				result.Content1 = 0x02
				result.Content2 = SiemensFetchWriteNet.CalculateAddressStarted( address[1:] )
			elif address[0] == 'D' or address.startswith("DB"):
				result.Content1 = 0x01
				adds = address.split( '.' )
				if address[1] == 'B':
					result.Content3 = int( adds[0][2:] )
				else:
					result.Content3 = int( adds[0][1:] )

				if result.Content3 > 255:
					result.Message = StringResources.Language.SiemensDBAddressNotAllowedLargerThan255
					return result

				result.Content2 = SiemensFetchWriteNet.CalculateAddressStarted( address[ address.find( '.' ) + 1:] )
			elif address[0] == 'T':
				result.Content1 = 0x07
				result.Content2 = SiemensFetchWriteNet.CalculateAddressStarted( address[1:] )
			elif address[0] == 'C':
				result.Content1 = 0x06
				result.Content2 = SiemensFetchWriteNet.CalculateAddressStarted( address[1:])
			else:
				result.Message = StringResources.Language.NotSupportedDataType
				result.Content1 = 0
				result.Content2 = 0
				result.Content3 = 0
				return result
		except Exception as ex:
			result.Message = str(ex)
			return result

		result.IsSuccess = True
		return result
	@staticmethod
	def BuildReadCommand( address, count ):
		'''生成一个读取字数据指令头的通用方法'''
		result = OperateResult( )

		analysis = SiemensFetchWriteNet.AnalysisAddress( address )
		if analysis.IsSuccess == False :
			result.CopyErrorFromOther( analysis )
			return result

		_PLCCommand = bytearray(16)
		_PLCCommand[0] = 0x53
		_PLCCommand[1] = 0x35
		_PLCCommand[2] = 0x10
		_PLCCommand[3] = 0x01
		_PLCCommand[4] = 0x03
		_PLCCommand[5] = 0x05
		_PLCCommand[6] = 0x03
		_PLCCommand[7] = 0x08

		# 指定数据区
		_PLCCommand[8] = analysis.Content1
		_PLCCommand[9] = analysis.Content3

		# 指定数据地址
		_PLCCommand[10] =analysis.Content2 // 256
		_PLCCommand[11] = analysis.Content2 % 256

		if analysis.Content1 == 0x01 or analysis.Content1 == 0x06 or analysis.Content1 == 0x07:
			if count % 2 != 0:
				result.Message = StringResources.Language.SiemensReadLengthMustBeEvenNumber
				return result
			else:
				# 指定数据长度
				_PLCCommand[12] = count // 2 // 256
				_PLCCommand[13] = count // 2 % 256
		else:
			# 指定数据长度
			_PLCCommand[12] = count // 256
			_PLCCommand[13] = count % 256

		_PLCCommand[14] = 0xff
		_PLCCommand[15] = 0x02

		result.Content = _PLCCommand
		result.IsSuccess = True
		return result
	@staticmethod
	def BuildWriteCommand( address, data ):
		'''生成一个写入字节数据的指令'''
		if data == None : data = bytearray(0)
		result = OperateResult( )

		analysis = SiemensFetchWriteNet.AnalysisAddress( address )
		if analysis.IsSuccess == False:
			result.CopyErrorFromOther( analysis )
			return result

		_PLCCommand = bytearray(16 + len(data))
		_PLCCommand[0] = 0x53
		_PLCCommand[1] = 0x35
		_PLCCommand[2] = 0x10
		_PLCCommand[3] = 0x01
		_PLCCommand[4] = 0x03
		_PLCCommand[5] = 0x03
		_PLCCommand[6] = 0x03
		_PLCCommand[7] = 0x08

		# 指定数据区
		_PLCCommand[8] = analysis.Content1
		_PLCCommand[9] = analysis.Content3

		# 指定数据地址
		_PLCCommand[10] = analysis.Content2 // 256
		_PLCCommand[11] = analysis.Content2 % 256

		if analysis.Content1 == 0x01 or analysis.Content1 == 0x06 or analysis.Content1 == 0x07:
			if data.Length % 2 != 0:
				result.Message = StringResources.Language.SiemensReadLengthMustBeEvenNumber
				return result
			else:
				# 指定数据长度
				_PLCCommand[12] = data.Length // 2 // 256
				_PLCCommand[13] = data.Length // 2 % 256
		else:
			# 指定数据长度
			_PLCCommand[12] = data.Length // 256
			_PLCCommand[13] = data.Length % 256
		_PLCCommand[14] = 0xff
		_PLCCommand[15] = 0x02

		# 放置数据
		_PLCCommand[16:16+len(data)] = data

		result.Content = _PLCCommand
		result.IsSuccess = True
		return result
	def Read( self, address, length ):
		'''从PLC读取数据，地址格式为I100，Q100，DB20.100，M100，T100，C100，以字节为单位'''
		# 指令解析 -> Instruction parsing
		command = SiemensFetchWriteNet.BuildReadCommand( address, length )
		if command.IsSuccess == False : return command

		# 核心交互 -> Core Interactions
		read = self.ReadFromCoreServer( command.Content )
		if read.IsSuccess == False : return read

		# 错误码验证 -> Error code Verification
		if read.Content[8] != 0x00 : return OperateResult(read.Content[8],"发生了异常，具体信息查找Fetch/Write协议文档")

		# 读取正确 -> Read Right
		buffer = bytearray(len(read.Content) - 16)
		buffer[0:len(buffer)] = read.Content[16:16+len(buffer)]
		return OperateResult.CreateSuccessResult( buffer )
	def ReadByte( self, address ):
		'''读取指定地址的byte数据'''
		return ByteTransformHelper.GetResultFromArray( self.Read( address, 1 ) )
	def Write( self, address, value ):
		'''将数据写入到PLC数据，地址格式为I100，Q100，DB20.100，M100，以字节为单位'''
		# 指令解析 -> Instruction parsing
		command = SiemensFetchWriteNet.BuildWriteCommand( address, value )
		if command.IsSuccess == False : return command

		# 核心交互 -> Core Interactions
		write = self.ReadFromCoreServer( command.Content )
		if write.IsSuccess == False : return write

		# 错误码验证 -> Error code Verification
		if (write.Content[8] != 0x00) : OperateResult(err = write.Content[8], msg = "西门子PLC写入失败！")

		# 写入成功 -> Write Right
		return OperateResult.CreateSuccessResult( )
	def WriteBool( self, address, values):
		'''向PLC中写入byte数据，返回是否写入成功 -> Writes byte data to the PLC and returns whether the write succeeded'''
		if type(values) == list:
			return self.Write( address, SoftBasic.BoolArrayToByte( values ) )
		else:
			return self.WriteBool( address, [ values ] )

# Omron PLC 通讯类
class OmronFinsDataType:
	'''欧姆龙的Fins协议的数据类型'''
	BitCode = 0
	WordCode = 0
	def __init__(self, bitCode = 0, wordCode = 0):
		'''实例化一个Fins的数据类型'''
		self.BitCode = bitCode
		self.WordCode = wordCode
	@staticmethod
	def DM():
		'''DM Area'''
		return OmronFinsDataType( 0x02, 0x82 )
	@staticmethod
	def CIO():
		'''CIO Area'''
		return OmronFinsDataType( 0x30, 0xB0 )
	@staticmethod
	def WR():
		'''Work Area'''
		return OmronFinsDataType( 0x31, 0xB1 )
	@staticmethod
	def HR():
		'''Holding Bit Area'''
		return OmronFinsDataType( 0x32, 0xB2 )
	@staticmethod
	def AR():
		'''Auxiliary Bit Area'''
		return OmronFinsDataType( 0x33, 0xB3 )

class OmronFinsNet(NetworkDeviceBase):
	'''欧姆龙PLC通讯类，采用Fins-Tcp通信协议实现'''
	def __init__(self,ipAddress="127.0.0.1",port = 9600):
		super().__init__()
		'''实例化一个欧姆龙PLC Fins帧协议的通讯对象'''
		self.WordLength = 1
		self.ipAddress = ipAddress
		self.port = port
		self.byteTransform = ReverseWordTransform()
		self.byteTransform.DataFormat = DataFormat.CDAB
		self.DA1 = int(ipAddress.split(".")[3])
		self.iNetMessage = FinsMessage()
		self.ICF = 0x80
		self.RSV = 0x00
		self.GCT = 0x02
		self.DNA = 0x00
		self.DA1 = 0x13
		self.DA2 = 0x00
		self.SNA = 0x00
		self.SA1 = 0x00
		self.SA2 = 0x00
		self.SID = 0x00
		self.IsChangeSA1AfterReadFailed = False
		self.handSingle = bytearray([0x46, 0x49, 0x4E, 0x53,0x00, 0x00, 0x00, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01])

	def SetSA1(self, value):
		'''设置SA1的方法'''
		self.SA1 = value
		self.handSingle[19] = value

	def PackCommand( self, cmd ):
		'''将普通的指令打包成完整的指令
		
		Parameter
		  cmd: bytearray 原始的fins指令
		Return
		  bytearray: 结果的数据'''
		buffer = bytearray(26 + len(cmd))
		buffer[0:4] = self.handSingle[0:4]
		tmp = struct.pack('>i', len(buffer) - 8 )
		buffer[4:8] = tmp
		buffer[11] = 0x02
		buffer[16] = self.ICF
		buffer[17] = self.RSV
		buffer[18] = self.GCT
		buffer[19] = self.DNA
		buffer[20] = self.DA1
		buffer[21] = self.DA2
		buffer[22] = self.SNA
		buffer[23] = self.SA1
		buffer[24] = self.SA2
		buffer[25] = self.SID
		buffer[26:] = cmd
		return buffer
	def BuildReadCommand( self, address, length , isBit):
		'''根据类型地址长度确认需要读取的指令头
		
		Parameter
		  address: string 起始地址
		  length: ushort 长度
		  isBit: bool 是否是位读取
		Return
		  OperateResult: 结果的数据'''
		command = OmronFinsNetHelper.BuildReadCommand( address, length, isBit )
		if command.IsSuccess == False : return command

		return OperateResult.CreateSuccessResult( self.PackCommand( command.Content ) )
	def BuildWriteCommand( self, address, value, isBit ):
		'''根据类型地址以及需要写入的数据来生成指令头
		
		Parameter
		  address: string 起始地址
		  value: bytearray 真实的数据值信息
		  isBit: bool 是否是位读取
		Return
		  OperateResult: 结果的数据'''
		command = OmronFinsNetHelper.BuildWriteWordCommand( address, value, isBit )
		if command.IsSuccess == False : return command
			
		return OperateResult.CreateSuccessResult( self.PackCommand( command.Content ) )
	def InitializationOnConnect( self, socket ):
		'''在连接上欧姆龙PLC后，需要进行一步握手协议
		
		Parameter
		  socket: Socket 连接的套接字
		Return
		  OperateResult: 是否初始化成功'''
		# 握手信号
		read = self.ReadFromCoreServerBase( socket, self.handSingle )
		if read.IsSuccess == False : return read

		# 检查返回的状态
		buffer = bytearray(4)
		buffer[0] = read.Content2[7]
		buffer[1] = read.Content2[6]
		buffer[2] = read.Content2[5]
		buffer[3] = read.Content2[4]

		status = struct.unpack( '<i',buffer )[0]
		if status != 0 : return OperateResult( err = status, msg = OmronFinsNetHelper.GetStatusDescription( status ) )

		# 提取PLC的节点地址
		if len(read.Content2) >= 24 : self.DA1 = read.Content2[23]

		return OperateResult.CreateSuccessResult( )
	def Read( self, address, length ):
		'''从欧姆龙PLC中读取想要的数据，返回读取结果，读取单位为字
		
		Parameter
		  address: string 读取地址，格式为"D100","C100","W100","H100","A100"
		  length: ushort 读取的数据长度
		Return
		  OperateResult: 带成功标志的结果数据对象'''
		# 获取指令
		command = self.BuildReadCommand( address, length, False )
		if command.IsSuccess == False : return OperateResult.CreateFailedResult( command )

		# 核心数据交互
		read = self.ReadFromCoreServer( command.Content )
		if read.IsSuccess == False : return OperateResult.CreateFailedResult( read )

		# 数据有效性分析
		valid = OmronFinsNetHelper.ResponseValidAnalysis( read.Content, True )
		if valid.IsSuccess == False : return OperateResult.CreateFailedResult( valid )

		# 读取到了正确的数据
		return OperateResult.CreateSuccessResult( valid.Content )
	def Write( self, address, value ):
		'''向PLC中位软元件写入bool数组，返回值说明，比如你写入D100,values[0]对应D100.0
		
		Parameter
		  address: string 读取地址，格式为"D100","C100","W100","H100","A100"
		  value: bytearray 原始的字节数据
		Return
		  OperateResult: 结果内容'''
		# 获取指令
		command = self.BuildWriteCommand( address, value, False )
		if command.IsSuccess == False : return command

		# 核心数据交互
		read = self.ReadFromCoreServer( command.Content )
		if read.IsSuccess == False : return read

		# 数据有效性分析
		valid = OmronFinsNetHelper.ResponseValidAnalysis( read.Content, False )
		if valid.IsSuccess == False : return valid

		# 成功
		return OperateResult.CreateSuccessResult( )
	def ReadBool( self, address, length = None ):
		'''从欧姆龙PLC中批量读取位软元件，返回读取结果
		
		Parameter
		  address: string 读取地址，格式为"D100","C100","W100","H100","A100"
		  length: ushort 读取的长度
		Return
		  OperateResult: 带成功标志的结果数据对象'''
		if length == None:
			read = self.ReadBool( address, 1 )
			if read.IsSuccess == False : return OperateResult.CreateFailedResult( read )

			return OperateResult.CreateSuccessResult( read.Content[0] )
		else:
			# 获取指令
			command = self.BuildReadCommand( address, length, True )
			if command.IsSuccess == False : return OperateResult.CreateFailedResult( command )

			# 核心数据交互
			read = self.ReadFromCoreServer( command.Content )
			if read.IsSuccess == False : return OperateResult.CreateFailedResult( read )

			# 数据有效性分析
			valid = OmronFinsNetHelper.ResponseValidAnalysis( read.Content, True )
			if valid.IsSuccess == False : return OperateResult.CreateFailedResult( valid )

			# 返回正确的数据信息
			content = []
			for i in range(len(valid.Content)):
				if valid.Content[i] == 0x01:
					content.append(True)
				else:
					content.append(False)
			return OperateResult.CreateSuccessResult( content )
	def WriteBool( self, address, values ):
		'''向PLC中位软元件写入bool数组，返回值说明，比如你写入D100,values[0]对应D100.0
		
		Parameter
		  address: string 读取地址，格式为"D100","C100","W100","H100","A100"
		  values: bytearray 要写入的实际数据，可以指定任意的长度
		Return
		  OperateResult: 带成功标志的结果数据对象'''
		if type(values) == list:
			# 获取指令
			content = bytearray(len(values))
			for i in range(len(values)):
				if values[i] == True:
					content[i] = 0x01
				else:
					content[i] = 0x00
			command = self.BuildWriteCommand( address, content, True )
			if command.IsSuccess == False : return command

			# 核心数据交互
			read = self.ReadFromCoreServer( command.Content )
			if read.IsSuccess == False : return read

			# 数据有效性分析
			valid = OmronFinsNetHelper.ResponseValidAnalysis( read.Content, False )
			if valid.IsSuccess == False : return valid

			# 写入成功
			return OperateResult.CreateSuccessResult( )
		else:
			return self.WriteBool( address, [values] )
	def __PackCommand( self, cmd ):
		'''将普通的指令打包成完整的指令'''
		buffer = bytearray(26 + len(cmd))
		self.handSingle[0:4] = buffer[0:4]
		tmp = struct.pack('>i',(len(buffer)-8))
		buffer[4:8] = tmp
		buffer[11] = 0x02
		buffer[16] = self.ICF
		buffer[17] = self.RSV
		buffer[18] = self.GCT
		buffer[19] = self.DNA
		buffer[20] = self.DA1
		buffer[21] = self.DA2
		buffer[22] = self.SNA
		buffer[23] = self.SA1
		buffer[24] = self.SA2
		buffer[25] = self.SID
		buffer[26:] = cmd
		return buffer
	
	def __str__(self):
		'''
		返回表示当前对象的字符串
		'''
		return "OmronFinsNet[" + self.ipAddress + ":" + str(self.port) + "]"
class OmronFinsNetHelper:
	@staticmethod
	def AnalysisAddress( address, isBit ):
		'''解析数据地址，Omron手册第188页

		Parameter
		  address: string 字符串的地址信息
		  isBit: bool 是否是位地址
		Return
		  OperateResult: 结果对象
		'''
		result = OperateResult( )
		try:
			if address[0] == 'D' or address[0] == 'd':
				result.Content1 = OmronFinsDataType.DM()
			elif address[0] == 'C' or address[0] == 'c':
				result.Content1 = OmronFinsDataType.CIO()
			elif address[0] == 'W' or address[0] == 'w':
				result.Content1 = OmronFinsDataType.WR()
			elif address[0] == 'H' or address[0] == 'h':
				result.Content1 = OmronFinsDataType.HR()
			elif address[0] == 'A' or address[0] == 'a':
				result.Content1 = OmronFinsDataType.AR()
			elif address[0] == 'E' or address[0] == 'e':
				# E区，比较复杂，需要专门的计算
				splits = address.split(".")
				block = int(splits[0][1:], 16)
				if block < 16:
					result.Content1 = OmronFinsDataType( 0x20 + block, 0xA0 + block)
				else:
					result.Content1 = OmronFinsDataType( 0xE0 + block - 16, 0x60 + block - 16)
			else: raise Exception( StringResources.Language.NotSupportedDataType )

			if address[0] == 'E' or address[0] == 'e':
				splits = address.split(".")
				if isBit:
					# 位操作
					addr = int( splits[1] )
					result.Content2 = bytearray(3)
					result.Content2[0] = struct.pack("<i", addr )[1]
					result.Content2[1] = struct.pack("<i", addr )[0]

					if splits.Length > 2:
						result.Content2[2] = int( splits[2] )
						if result.Content2[2] > 15:
							raise Exception( StringResources.Language.OmronAddressMustBeZeroToFiveteen )
				else:
					# 字操作
					addr = int( splits[1] )
					result.Content2 =  bytearray(3)
					result.Content2[0] = struct.pack("<i", addr )[1]
					result.Content2[1] = struct.pack("<i", addr )[0]
			else:
				if isBit:
					# 位操作
					splits = address[1:].split(".")
					addr = int( splits[0] )
					result.Content2 = bytearray(3)
					result.Content2[0] = struct.pack("<i", addr )[1]
					result.Content2[1] = struct.pack("<i", addr )[0]

					if len(splits) > 1:
						result.Content2[2] = int( splits[1] )
						if result.Content2[2] > 15:
							raise Exception( StringResources.Language.OmronAddressMustBeZeroToFiveteen )
				else:
					# 字操作
					addr = int( address[1:] )
					result.Content2 = bytearray(3)
					result.Content2[0] = struct.pack("<i", addr )[1]
					result.Content2[1] = struct.pack("<i", addr )[0]
		except Exception as ex:
			result.Message = str(ex)
			return result
		result.IsSuccess = True
		return result

	@staticmethod
	def BuildReadCommand( address, length, isBit ):
		'''
		根据读取的地址，长度，是否位读取创建Fins协议的核心报文
		
		Parameter
		  address: string 字符串的地址信息
		  length: int 读取的数据长度
		  isBit: bool 是否是位地址
		Return
		  OperateResult: 带有成功标识的Fins核心报文
		'''
		analysis = OmronFinsNetHelper.AnalysisAddress( address, isBit )
		if analysis.IsSuccess == False: return OperateResult.CreateFailedResult( analysis )

		_PLCCommand = bytearray(8)
		_PLCCommand[0] = 0x01    # 读取存储区数据
		_PLCCommand[1] = 0x01
		if isBit == True:
			_PLCCommand[2] = analysis.Content1.BitCode
		else:
			_PLCCommand[2] = analysis.Content1.WordCode
		_PLCCommand[3:6] = analysis.Content2
		_PLCCommand[6] = length // 256   # 长度
		_PLCCommand[7] = length % 256
		return OperateResult.CreateSuccessResult( _PLCCommand )

	@staticmethod
	def BuildWriteWordCommand( address, value, isBit ):
		'''根据写入的地址，数据，是否位写入生成Fins协议的核心报文
		
		Parameter
		  address: string 字符串的地址信息
		  value: bytearray 实际的数据内容
		  isBit: bool 是否是位地址
		Return
		  OperateResult: 带有成功标识的Fins核心报文
		'''
		analysis = OmronFinsNetHelper.AnalysisAddress( address, isBit )
		if analysis.IsSuccess == False: return OperateResult.CreateFailedResult( analysis )

		_PLCCommand = bytearray(8 + len(value))
		_PLCCommand[0] = 0x01
		_PLCCommand[1] = 0x02

		if isBit == True:
			_PLCCommand[2] = analysis.Content1.BitCode
		else:
			_PLCCommand[2] = analysis.Content1.WordCode

		_PLCCommand[3:6] = analysis.Content2
		if isBit == True:
			_PLCCommand[6] = len(value) // 256
			_PLCCommand[7] = len(value) % 256
		else:
			_PLCCommand[6] = len(value) // 2 // 256
			_PLCCommand[7] = len(value) // 2 % 256

		_PLCCommand[8:] = value
		return OperateResult.CreateSuccessResult( _PLCCommand )

	@staticmethod
	def ResponseValidAnalysis( response, isRead ):
		'''验证欧姆龙的Fins-TCP返回的数据是否正确的数据，如果正确的话，并返回所有的数据内容
		
		Parameter
		  response: bytearray 来自欧姆龙返回的数据内容
		  isRead: bool 是否读取
		Return
		  OperateResult: 带有是否成功的结果对象
		'''
		if len(response) >= 16:
			# 提取错误码 -> Extracting error Codes
			buffer = bytearray(4)
			buffer[0] = response[15]
			buffer[1] = response[14]
			buffer[2] = response[13]
			buffer[3] = response[12]

			err = struct.unpack('<i',buffer)[0]
			if err > 0 : return OperateResult( err = err, msg = OmronFinsNetHelper.GetStatusDescription( err ) )

			result = response[16:]
			return OmronFinsNetHelper.UdpResponseValidAnalysis( result, isRead )

		return OperateResult( msg= StringResources.Language.OmronReceiveDataError )

	@staticmethod
	def UdpResponseValidAnalysis( response, isRead ):
		''' 验证欧姆龙的Fins-Udp返回的数据是否正确的数据，如果正确的话，并返回所有的数据内容
		
		Parameter
		  response: bytearray 来自欧姆龙返回的数据内容
		  isRead: bool 是否读取
		Return
		  OperateResult: 带有是否成功的结果对象
		'''
		if len(response) >= 14:
			err = response[12] * 256 + response[13]
			# if (err > 0) return new OperateResult<byte[]>( err, StringResources.Language.OmronReceiveDataError );

			if isRead == False:
				success = OperateResult.CreateSuccessResult(bytearray(0))
				success.ErrorCode = err
				success.Message = OmronFinsNetHelper.GetStatusDescription( err ) + " Received:" + SoftBasic.ByteToHexString( response, ' ' )
				return success
			else:
				# 读取操作 -> read operate
				content = response[14:]

				success = OperateResult.CreateSuccessResult( content )
				if len(content) == 0: success.IsSuccess = False
				success.ErrorCode = err
				success.Message = OmronFinsNetHelper.GetStatusDescription( err ) + " Received:" + SoftBasic.ByteToHexString( response, ' ' )
				return success

		return OperateResult( msg= StringResources.Language.OmronReceiveDataError )

	@staticmethod
	def GetStatusDescription( err ):
		'''获取错误信息的字符串描述文本
			
		Parameter
		  err: int 错误码
		Return
		  string: 文本描述
			'''
		if err == 0 : return StringResources.Language.OmronStatus0
		elif err == 1 : return StringResources.Language.OmronStatus1
		elif err == 2 : return StringResources.Language.OmronStatus2
		elif err == 3 : return StringResources.Language.OmronStatus3
		elif err == 20 : return StringResources.Language.OmronStatus20
		elif err == 21 : return StringResources.Language.OmronStatus21
		elif err == 22 : return StringResources.Language.OmronStatus22
		elif err == 23 : return StringResources.Language.OmronStatus23
		elif err == 24 : return StringResources.Language.OmronStatus24
		elif err == 25 : return StringResources.Language.OmronStatus25
		else : return StringResources.Language.UnknownError

# ↓ Ab-plc Implementation ==========================================================================================
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


# ↑ AB-plc Implementation ==========================================================================================

# NetSimplifyClient类
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


# ↓ Redis Implementation ==========================================================================================

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

# ↑ Redis Implementation ==========================================================================================
