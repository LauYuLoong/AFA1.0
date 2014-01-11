# -*- coding: gbk -*-
##################################################################
#              安徽农信社主机通讯映射文件定义
#=================================================================
#                作    者：    陈 显 明
#                修改时间：    20060907
##################################################################
from HostRegexpDef import *
import struct, HostContext, LoggerHandler

isDebug = False
logger = LoggerHandler.getLogger( 'hostComm' )

#	从指定的模块中获取指定名称的变量值
def loadVar( moduleName, varName ):
	module=__import__( moduleName )
	if module.existVariable( varName ) :
		return getattr( module, varName )
	else:
		return None

#	把指定名称和值的变量设置到指定的模块中
def storeVar( moduleName, varName , varValue ):
	module=__import__( moduleName )
	setattr( module, varName, varValue )

#	把字符串右补空格到指定的长度
def rightFillBlank( srcString, totalLength ):
	srcLen = len( srcString )
	if( srcLen > totalLength ):
		raise StandardError, "给定的数据%s长度%d超过指定的长度限制%d"%( srcString, srcLen, totalLength )
	if( srcLen == totalLength ):
		return srcString

	result = srcString
	while( srcLen < totalLength ):
		result = result + " "
		srcLen = srcLen + 1
	return result

#	把字符串右边的空格删除
def rightTrimBlank( srcString ):
	index = len( srcString )
	while( srcString[index - 1] == " " ):
		index = index - 1    
	return srcString[:index]

#	根据类型定义把数据拼装成主机网关VRoute需要的格式，由VRoute处理到主机的数据长度转换
def genSimpleField( destType, varName, varValue ):
	#	字段名称长度	字段名称	字段类型	字段长度	字段值
	result = struct.pack( "B", len( varName ) ) + varName + struct.pack( "B", int( destType ) )
	if( destType == "3" ):		#	字节类型
		result += struct.pack( "B", int( varValue ) )
	elif( destType == "4" ):	#	短整形数据，网络序字节
		result += struct.pack( "!H", int( varValue ) )
	elif( destType == "5" ):	#	4位整形，网络序整形
		result += struct.pack( "!L", int( varValue ) )
	elif( destType == "6" ):	#	小数，字符串方式
		result += struct.pack( "B", len( varValue ) ) + varValue
	elif( destType == "7" ):	#	短字符串，字符串方式
		result += struct.pack( "B", len( varValue ) ) + varValue
	elif( destType == "8" ):	#	短字节流，字节流方式
		result += struct.pack( "B", len( varValue ) ) + varValue
	elif( destType == "9" ):	#	日期，字符串方式，以YYYYMMDD的方式
		result += varValue
	elif( destType == "10" ):	#	时间，字符串方式，以HHMMSS的方式
		result += varValue
	elif( destType == "11" ):	#	长字符串，字符串方式
		result += struct.pack( "!H", len( varValue ) ) + varValue
	elif( destType == "12" ):	#	长字节流，字节流方式
		result += struct.pack( "!H", len( varValue ) ) + varValue
	else:						#	无法识别的类型定义
		result = None
	return result

#	把数据打包成Vroute能识别的结构体
def genStructField( structData ):
	result = struct.pack( "B", 0 ) + struct.pack( "B", 1 ) + struct.pack( "!H", len( structData ) ) + structData
	return result

#	把数据打包成Vroute能识别的数组结构
def genArrayField( arrayName, arraySize, arrayData ):
	result = struct.pack( "B", len( arrayName ) ) + arrayName + struct.pack( "B", 2 ) + struct.pack( "!H", arraySize ) + struct.pack( "!H", len( arrayData ) ) + arrayData
	return result

#	根据报文体生成上送主机的报文
def genReqMsg( sysId, serviceName, respData ):
	result = struct.pack( "BBB", 1, 0, 0 ) + sysId + serviceName + "01" + struct.pack( "!LLL", len( respData ) , 8, 0 ) + respData
	result = struct.pack( "!L", len( result ) + 4 ) + result
	return result

#	根据映射文件生成报文
def hostPack( mapping, sysId, serviceName ):
	if( len( sysId ) != 4 ):
		print "给定的系统号%s位数不符（不等于4）"%sysId
		sysId = rightFillBlank( sysId, 4 )
	if( len( serviceName ) != 10 ):
		print "给定的服务名称%s位数不符（不等于10）"%serviceName
		serviceName = rightFillBlank( serviceName, 10 )
	lineNo , result = 0, ''
	isRepeat, repeatCount, repeatSeq, stack, repeatCountName, arrayName= False, 0, 0, [], '', ''
	mapFile = open( mapping, 'r' )
	for line in mapFile.readlines( ):
		lineNo += 1
		# 判断这行是否是注释
		if ( pComment.match( line ) != None ) : continue
		# 判断这行是否是空行
		if ( pBlank.match( line ) != None ) : continue
	
		# 判断是否为一般的字段描述
		mField = pCommDefField.match( line )
		if mField != None :
			#	拆分映射文件的字段，格式为：	序号 数据类型 目标长度 模块名 变量名 默认值 中文描述
			seqNo, fillType, targetLen, moduleName, varName, defalutVal, description = mField.groups( )

			#	获取指定字段的值
			var = loadVar( moduleName, varName )
			if ( var == None ): # 如果指定的变量不存在，填入缺省值
				if ( not isRepeat ):
					var = defalutVal
					storeVar( moduleName, varName , var )
				else:
					var = []
					for i in range( repeatCount ): var.append( defalutVal )
					storeVar( moduleName, varName , var )
			if ( not ( type( var ) is str ) ) and ( not ( type( var ) is list ) ): var = str( var )# 将其它类型转换为字符串类型
 			if ( type( var ) is list ) and ( not isRepeat ):
 				mapFile.close( )
				raise StandardError, "主机报文映射文件中，不在循环中的变量不能为数组类型：\n[%s] 第%i行：%s" % ( mapping , lineNo, line )
			if ( type( var ) is str ) and isRepeat:
				mapFile.close( )
				raise StandardError, "主机报文映射文件中，循环中的变量必须为数组类型：\n[%s] 第%i行：%s" % ( mapping, lineNo, line )
			if isRepeat and len( var ) < repeatCount:
				mapFile.close( )
				raise StandardError, "主机报文映射文件中，循环的数组%s的数据个数%d小于设定循环次数%s=%d：\n[%s] 第%i行：%s" % ( moduleName+'.'+varName, len( var ), repeatCountName, repeatCount, mapping, lineNo, line )

			#	校验字段值，并填充字符到结果字符串中
			if not isRepeat :
				fillResult = genSimpleField( fillType, varName, var )
				if( fillResult == None ):raise StandardError, "主机报文映射文件中，字段[%s]的类型[%s]无法识别\n[%s] 第%i行：%s"% ( var, fillType, mapping, lineNo, line )
				if( isDebug ):logger.debug( "【发送数据到主机】：[%s=%s]"%( varName, var ) )
				result += fillResult
			else:
				repeatSeq += 1
				for i in range( repeatCount ) :
					tempVar = var[i]
					tmp = genSimpleField( fillType, varName, tempVar )
					if( tmp == None ):raise StandardError, "主机报文映射文件中，字段[%s]的类型[%s]无法识别\n[%s] 第%i行：%s"% ( tempVar, fillType, mapping, lineNo, line )
					if( isDebug ):logger.debug( "【发送数组数据到主机】：[%s=%s]"%( varName, tempVar ) )
					stack.insert( i * repeatSeq + repeatSeq - 1 , tmp )
			continue

		# 判断是否是循环开始
		mForb = pForb.match( line )
		if mForb != None :
			if isRepeat :
				mapFile.close( )
				raise StandardError, "主机报文映射文件中循环不能嵌套：\n[%s] 第%i行：%s" % ( mapping, lineNo, line )
			isRepeat = True
			# forb	最大循环次数	模块名	变量名	上送给VRoute的数组名称
			maxRepeatCount, moduleName, varName, arrayName = mForb.groups( )
			repeatCount = loadVar( moduleName, varName )
			if repeatCount == None:
				mapFile.close( )
				raise StandardError, "主机报文映射文件中循环变量没有找到：\n[%s] 第%i行：%s" % ( mapping, lineNo, line )

			repeatCount = int( repeatCount )
			maxRepeatCount = int( maxRepeatCount )
			if( repeatCount > maxRepeatCount ):
				mapFile.close( )
				raise StandardError, "主机报文映射文件中，循环的实际次数%d大于最大循环次数%d：\n[%s] 第%i行：%s" % ( count, maxRepeatCount, mapping, lineNo, line )
			repeatSeq, stack, repeatCountName = 0, [], moduleName + '.' + varName
			continue
		
		# 判断是否是循环结束
		mFore = pFore.match( line )
		if mFore != None :
			if not isRepeat :
				mapFile.close( )
				raise StandardError, "主机报文映射文件中fore无法找到对应的forb：\n[%s] 第%i行：%s" % ( mapping, lineNo, line )
			isRepeat = False
			i, arrayData = 0, ""
			while( i< len( stack ) ):
				structData = ""
				for j in range( repeatSeq ):
					structData += stack[i + j]
				i += repeatSeq
				arrayData += genStructField( structData )
			result += genArrayField( arrayName, repeatCount, arrayData )
			continue

		# 没有匹配任何格式，错误格式的配置
		mapFile.close( )
		raise StandardError, "主机报文映射文件中语法错误：\n[%s] 第%i行：%s" % ( mapping, lineNo, line )
	mapFile.close( )
	if result == '' :
		raise StandardError, "主机报文映射文件错误：\n[%s] 打包结果为空字符串" % ( mapping )
	
	#	拼装报文头信息:	总长度	协议版本号	报文基本类型	系统标识	请求服务名称	应用报文类型01		应用报文长度	可选头
	result = genReqMsg( sysId, serviceName, result )
	return result

#	把数据添加成列表结果存放到HostContext中
def appendDataToList( fieldName , fieldValue ):
	var = loadVar( "HostContext", fieldName )
	if( var == None ):
		storeVar( "HostContext", fieldName , [fieldValue] )
	else:
		var.append( fieldValue )
		storeVar( "HostContext", fieldName , var )

#	拆分结构类型的字段
def analyzeStructData( dataBody ):
	index = 0
	while( index < len( dataBody ) ):
		#	拆分字段名称
		nameLen = struct.unpack( "B", dataBody[index] )[0]
		index += 1
		fieldName = dataBody[index : index + nameLen]
		index += nameLen

		#	拆分字段值
		valType = struct.unpack( "B", dataBody[index] )[0]
		index += 1
		if( valType == 3 ):			#	字节类型
			fieldValue = struct.unpack( "B", dataBody[index] )[0]
			index += 1
			appendDataToList( fieldName , fieldValue )
		elif( valType == 4 ):		#	短整形数据
			fieldValue = struct.unpack( "!H", dataBody[index : index+2] )[0]
			index += 2
			appendDataToList( fieldName , fieldValue )
		elif( valType == 5 ):		#	4位整形
			fieldValue = struct.unpack( "!L", dataBody[index : index+4] )[0]
			index += 4
			appendDataToList( fieldName , fieldValue )
		elif( valType == 6 ):		#	小数
			valueLen = struct.unpack( "B", dataBody[index] )[0]
			index += 1
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			appendDataToList( fieldName , fieldValue )
		elif( valType == 7 ):		#	短字符串
			valueLen = struct.unpack( "B", dataBody[index] )[0]
			index += 1
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			appendDataToList( fieldName , fieldValue )
		elif( valType == 8 ):		#	短字节流
			valueLen = struct.unpack( "B", dataBody[index] )[0]
			index += 1
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			appendDataToList( fieldName , fieldValue )
		elif( valType == 9 ):		#	日期
			fieldValue = dataBody[index : index+8]
			index += 8
			appendDataToList( fieldName , fieldValue )
		elif( valType == 10 ):		#	时间
			fieldValue = dataBody[index : index+6]
			index += 6
			appendDataToList( fieldName , fieldValue )
		elif( valType == 11 ):		#	长字符串
			valueLen = struct.unpack( "!H", dataBody[index : index+2] )[0]
			index += 2
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			appendDataToList( fieldName , fieldValue )
		elif( valType == 12 ):		#	长字节流
			valueLen = struct.unpack( "!H", dataBody[index : index+2] )[0]
			index += 2
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			appendDataToList( fieldName , fieldValue )
		else:
			raise StandardError, "主机返回数据类型错误0(" + str(valType) + ")"
			
		if( isDebug ):logger.debug( "【拆分结构体数据】：[%s=%s]"%( fieldName, str( fieldValue ) ) )

#	拆分数组类型的字段
def analyzeArrayData( recordNum, dataBody ):
	index = 0
	while( index < len( dataBody ) ):
		#	拆分字段名称
		nameLen = struct.unpack( "B", dataBody[index] )[0]
		index += 1
		fieldName = dataBody[index : index + nameLen]
		index += nameLen

		#	拆分字段值
		valType = struct.unpack( "B", dataBody[index] )[0]
		index += 1
		if( valType == 1 ):			#	结构体数据
			structLen = struct.unpack( "!H", dataBody[index : index+2] )[0]
			index += 2
			fieldValue = dataBody[index : index+structLen]
			index += structLen
			analyzeStructData( fieldValue )
		elif( valType == 3 ):		#	字节类型
			fieldValue = struct.unpack( "B", dataBody[index] )[0]
			index += 1
			appendDataToList( fieldName , fieldValue )
		elif( valType == 4 ):		#	短整形数据
			fieldValue = struct.unpack( "!H", dataBody[index : index+2] )[0]
			index += 2
			appendDataToList( fieldName , fieldValue )
		elif( valType == 5 ):		#	4位整形
			fieldValue = struct.unpack( "!L", dataBody[index : index+4] )[0]
			index += 4
			appendDataToList( fieldName , fieldValue )
		elif( valType == 6 ):		#	小数,字符串方式
			valueLen = struct.unpack( "B", dataBody[index] )[0]
			index += 1
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			appendDataToList( fieldName , fieldValue )
		elif( valType == 7 ):		#	短字符串
			valueLen = struct.unpack( "B", dataBody[index] )[0]
			index += 1
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			appendDataToList( fieldName , fieldValue )
		elif( valType == 8 ):		#	短字节流
			valueLen = struct.unpack( "B", dataBody[index] )[0]
			index += 1
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			appendDataToList( fieldName , fieldValue )
		elif( valType == 9 ):		#	日期,字符串方式
			fieldValue = dataBody[index : index+8]
			index += 8
			appendDataToList( fieldName , fieldValue )
		elif( valType == 10 ):		#	时间,字符串方式
			fieldValue = dataBody[index : index+6]
			index += 6
			appendDataToList( fieldName , fieldValue )
		elif( valType == 11 ):		#	长字符串,字符串方式
			valueLen = struct.unpack( "!H", dataBody[index : index+2] )[0]
			index += 2
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			appendDataToList( fieldName , fieldValue )
		elif( valType == 12 ):		#	长字节流
			valueLen = struct.unpack( "!H", dataBody[index : index+2] )[0]
			index += 2
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			appendDataToList( fieldName , fieldValue )
		else:
			raise StandardError, "主机返回数据类型错误1(" + str(valType) + ")"
			
		if( isDebug and valType != 1 ):logger.debug( "【拆分数组数据】：[%s=%s]"%( fieldName , str( fieldValue ) ) )

#	拆分一般字段，对于数组类型的变量需要特殊处理
def analyzeDataBody( dataBody ):
	index = 0
	while( index < len( dataBody ) ):
		#	拆分字段名称
		nameLen = struct.unpack( "B", dataBody[index] )[0]
		index += 1
		fieldName = dataBody[index : index + nameLen]
		index += nameLen

		#	拆分字段值
		valType = struct.unpack( "B", dataBody[index] )[0]
		index += 1
		if( valType == 2 ):			#	数组类型
			recordNum, arrayLen = struct.unpack( "!HH", dataBody[index : index+4] )
			index += 4
			fieldValue = dataBody[index : index+arrayLen]
			index += arrayLen
			analyzeArrayData( recordNum, fieldValue )
		elif( valType == 3 ):		#	字节类型
			fieldValue = struct.unpack( "B", dataBody[index] )[0]
			index += 1
			storeVar( "HostContext", fieldName , fieldValue )
		elif( valType == 4 ):		#	短整形数据
			fieldValue = struct.unpack( "!H", dataBody[index : index+2] )[0]
			index += 2
			storeVar( "HostContext", fieldName , fieldValue )
		elif( valType == 5 ):		#	4位整形
			fieldValue = struct.unpack( "!L", dataBody[index : index+4] )[0]
			index += 4
			storeVar( "HostContext", fieldName , fieldValue )
		elif( valType == 6 ):		#	小数,字符串方式
			valueLen = struct.unpack( "B", dataBody[index] )[0]
			index += 1
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			storeVar( "HostContext", fieldName , fieldValue )
		elif( valType == 7 ):		#	短字符串
			valueLen = struct.unpack( "B", dataBody[index] )[0]
			index += 1
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			storeVar( "HostContext", fieldName , fieldValue )
		elif( valType == 8 ):		#	短字节流
			valueLen = struct.unpack( "B", dataBody[index] )[0]
			index += 1
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			storeVar( "HostContext", fieldName , fieldValue )
		elif( valType == 9 ):		#	日期,字符串方式
			fieldValue = dataBody[index : index+8]
			index += 8
			storeVar( "HostContext", fieldName , fieldValue )
		elif( valType == 10 ):		#	时间,字符串方式
			fieldValue = dataBody[index : index+6]
			index += 6
			storeVar( "HostContext", fieldName , fieldValue )
		elif( valType == 11 ):		#	长字符串,字符串方式
			valueLen = struct.unpack( "!H", dataBody[index : index+2] )[0]
			index += 2
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			storeVar( "HostContext", fieldName , fieldValue )
		elif( valType == 12 ):		#	长字节流
			valueLen = struct.unpack( "!H", dataBody[index : index+2] )[0]
			index += 2
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			storeVar( "HostContext", fieldName , fieldValue )
		else:
			raise StandardError, "主机返回数据类型错误2(" + str(valType) + ")"
			
		if( isDebug and valType != 2 ):logger.debug( "【拆分包体数据】：[%s=%s]"%( fieldName, str( fieldValue ) ) )

#	把主机返回的数据自动拆分到脚本HostContext中供交易使用
def hostUnpack( respData ):
	successFlag = struct.unpack( "B", respData[6] )[0]
	if( successFlag == 2 ):
		#print "主机成功返回"
		analyzeDataBody( respData[35 : ] )
	elif( ( successFlag == 3 ) or ( successFlag == 4 ) ):
		HostContext.host_Error = True
		HostContext.host_ErrorType = 7
		HostContext.host_ErrorMsg = rightTrimBlank( respData[11 : 21] )
	else:
		raise StandardError, "未知的主机返回类型"
