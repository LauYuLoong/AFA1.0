# -*- coding: gbk -*-
##################################################################
#              ����ũ��������ͨѶӳ���ļ�����
#=================================================================
#                ��    �ߣ�    �� �� ��
#                �޸�ʱ�䣺    20060907
##################################################################
from HostRegexpDef import *
import struct, HostContext, LoggerHandler

isDebug = False
logger = LoggerHandler.getLogger( 'hostComm' )

#	��ָ����ģ���л�ȡָ�����Ƶı���ֵ
def loadVar( moduleName, varName ):
	module=__import__( moduleName )
	if module.existVariable( varName ) :
		return getattr( module, varName )
	else:
		return None

#	��ָ�����ƺ�ֵ�ı������õ�ָ����ģ����
def storeVar( moduleName, varName , varValue ):
	module=__import__( moduleName )
	setattr( module, varName, varValue )

#	���ַ����Ҳ��ո�ָ���ĳ���
def rightFillBlank( srcString, totalLength ):
	srcLen = len( srcString )
	if( srcLen > totalLength ):
		raise StandardError, "����������%s����%d����ָ���ĳ�������%d"%( srcString, srcLen, totalLength )
	if( srcLen == totalLength ):
		return srcString

	result = srcString
	while( srcLen < totalLength ):
		result = result + " "
		srcLen = srcLen + 1
	return result

#	���ַ����ұߵĿո�ɾ��
def rightTrimBlank( srcString ):
	index = len( srcString )
	while( srcString[index - 1] == " " ):
		index = index - 1    
	return srcString[:index]

#	�������Ͷ��������ƴװ����������VRoute��Ҫ�ĸ�ʽ����VRoute�������������ݳ���ת��
def genSimpleField( destType, varName, varValue ):
	#	�ֶ����Ƴ���	�ֶ�����	�ֶ�����	�ֶγ���	�ֶ�ֵ
	result = struct.pack( "B", len( varName ) ) + varName + struct.pack( "B", int( destType ) )
	if( destType == "3" ):		#	�ֽ�����
		result += struct.pack( "B", int( varValue ) )
	elif( destType == "4" ):	#	���������ݣ��������ֽ�
		result += struct.pack( "!H", int( varValue ) )
	elif( destType == "5" ):	#	4λ���Σ�����������
		result += struct.pack( "!L", int( varValue ) )
	elif( destType == "6" ):	#	С�����ַ�����ʽ
		result += struct.pack( "B", len( varValue ) ) + varValue
	elif( destType == "7" ):	#	���ַ������ַ�����ʽ
		result += struct.pack( "B", len( varValue ) ) + varValue
	elif( destType == "8" ):	#	���ֽ������ֽ�����ʽ
		result += struct.pack( "B", len( varValue ) ) + varValue
	elif( destType == "9" ):	#	���ڣ��ַ�����ʽ����YYYYMMDD�ķ�ʽ
		result += varValue
	elif( destType == "10" ):	#	ʱ�䣬�ַ�����ʽ����HHMMSS�ķ�ʽ
		result += varValue
	elif( destType == "11" ):	#	���ַ������ַ�����ʽ
		result += struct.pack( "!H", len( varValue ) ) + varValue
	elif( destType == "12" ):	#	���ֽ������ֽ�����ʽ
		result += struct.pack( "!H", len( varValue ) ) + varValue
	else:						#	�޷�ʶ������Ͷ���
		result = None
	return result

#	�����ݴ����Vroute��ʶ��Ľṹ��
def genStructField( structData ):
	result = struct.pack( "B", 0 ) + struct.pack( "B", 1 ) + struct.pack( "!H", len( structData ) ) + structData
	return result

#	�����ݴ����Vroute��ʶ�������ṹ
def genArrayField( arrayName, arraySize, arrayData ):
	result = struct.pack( "B", len( arrayName ) ) + arrayName + struct.pack( "B", 2 ) + struct.pack( "!H", arraySize ) + struct.pack( "!H", len( arrayData ) ) + arrayData
	return result

#	���ݱ������������������ı���
def genReqMsg( sysId, serviceName, respData ):
	result = struct.pack( "BBB", 1, 0, 0 ) + sysId + serviceName + "01" + struct.pack( "!LLL", len( respData ) , 8, 0 ) + respData
	result = struct.pack( "!L", len( result ) + 4 ) + result
	return result

#	����ӳ���ļ����ɱ���
def hostPack( mapping, sysId, serviceName ):
	if( len( sysId ) != 4 ):
		print "������ϵͳ��%sλ��������������4��"%sysId
		sysId = rightFillBlank( sysId, 4 )
	if( len( serviceName ) != 10 ):
		print "�����ķ�������%sλ��������������10��"%serviceName
		serviceName = rightFillBlank( serviceName, 10 )
	lineNo , result = 0, ''
	isRepeat, repeatCount, repeatSeq, stack, repeatCountName, arrayName= False, 0, 0, [], '', ''
	mapFile = open( mapping, 'r' )
	for line in mapFile.readlines( ):
		lineNo += 1
		# �ж������Ƿ���ע��
		if ( pComment.match( line ) != None ) : continue
		# �ж������Ƿ��ǿ���
		if ( pBlank.match( line ) != None ) : continue
	
		# �ж��Ƿ�Ϊһ����ֶ�����
		mField = pCommDefField.match( line )
		if mField != None :
			#	���ӳ���ļ����ֶΣ���ʽΪ��	��� �������� Ŀ�곤�� ģ���� ������ Ĭ��ֵ ��������
			seqNo, fillType, targetLen, moduleName, varName, defalutVal, description = mField.groups( )

			#	��ȡָ���ֶε�ֵ
			var = loadVar( moduleName, varName )
			if ( var == None ): # ���ָ���ı��������ڣ�����ȱʡֵ
				if ( not isRepeat ):
					var = defalutVal
					storeVar( moduleName, varName , var )
				else:
					var = []
					for i in range( repeatCount ): var.append( defalutVal )
					storeVar( moduleName, varName , var )
			if ( not ( type( var ) is str ) ) and ( not ( type( var ) is list ) ): var = str( var )# ����������ת��Ϊ�ַ�������
 			if ( type( var ) is list ) and ( not isRepeat ):
 				mapFile.close( )
				raise StandardError, "��������ӳ���ļ��У�����ѭ���еı�������Ϊ�������ͣ�\n[%s] ��%i�У�%s" % ( mapping , lineNo, line )
			if ( type( var ) is str ) and isRepeat:
				mapFile.close( )
				raise StandardError, "��������ӳ���ļ��У�ѭ���еı�������Ϊ�������ͣ�\n[%s] ��%i�У�%s" % ( mapping, lineNo, line )
			if isRepeat and len( var ) < repeatCount:
				mapFile.close( )
				raise StandardError, "��������ӳ���ļ��У�ѭ��������%s�����ݸ���%dС���趨ѭ������%s=%d��\n[%s] ��%i�У�%s" % ( moduleName+'.'+varName, len( var ), repeatCountName, repeatCount, mapping, lineNo, line )

			#	У���ֶ�ֵ��������ַ�������ַ�����
			if not isRepeat :
				fillResult = genSimpleField( fillType, varName, var )
				if( fillResult == None ):raise StandardError, "��������ӳ���ļ��У��ֶ�[%s]������[%s]�޷�ʶ��\n[%s] ��%i�У�%s"% ( var, fillType, mapping, lineNo, line )
				if( isDebug ):logger.debug( "���������ݵ���������[%s=%s]"%( varName, var ) )
				result += fillResult
			else:
				repeatSeq += 1
				for i in range( repeatCount ) :
					tempVar = var[i]
					tmp = genSimpleField( fillType, varName, tempVar )
					if( tmp == None ):raise StandardError, "��������ӳ���ļ��У��ֶ�[%s]������[%s]�޷�ʶ��\n[%s] ��%i�У�%s"% ( tempVar, fillType, mapping, lineNo, line )
					if( isDebug ):logger.debug( "�������������ݵ���������[%s=%s]"%( varName, tempVar ) )
					stack.insert( i * repeatSeq + repeatSeq - 1 , tmp )
			continue

		# �ж��Ƿ���ѭ����ʼ
		mForb = pForb.match( line )
		if mForb != None :
			if isRepeat :
				mapFile.close( )
				raise StandardError, "��������ӳ���ļ���ѭ������Ƕ�ף�\n[%s] ��%i�У�%s" % ( mapping, lineNo, line )
			isRepeat = True
			# forb	���ѭ������	ģ����	������	���͸�VRoute����������
			maxRepeatCount, moduleName, varName, arrayName = mForb.groups( )
			repeatCount = loadVar( moduleName, varName )
			if repeatCount == None:
				mapFile.close( )
				raise StandardError, "��������ӳ���ļ���ѭ������û���ҵ���\n[%s] ��%i�У�%s" % ( mapping, lineNo, line )

			repeatCount = int( repeatCount )
			maxRepeatCount = int( maxRepeatCount )
			if( repeatCount > maxRepeatCount ):
				mapFile.close( )
				raise StandardError, "��������ӳ���ļ��У�ѭ����ʵ�ʴ���%d�������ѭ������%d��\n[%s] ��%i�У�%s" % ( count, maxRepeatCount, mapping, lineNo, line )
			repeatSeq, stack, repeatCountName = 0, [], moduleName + '.' + varName
			continue
		
		# �ж��Ƿ���ѭ������
		mFore = pFore.match( line )
		if mFore != None :
			if not isRepeat :
				mapFile.close( )
				raise StandardError, "��������ӳ���ļ���fore�޷��ҵ���Ӧ��forb��\n[%s] ��%i�У�%s" % ( mapping, lineNo, line )
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

		# û��ƥ���κθ�ʽ�������ʽ������
		mapFile.close( )
		raise StandardError, "��������ӳ���ļ����﷨����\n[%s] ��%i�У�%s" % ( mapping, lineNo, line )
	mapFile.close( )
	if result == '' :
		raise StandardError, "��������ӳ���ļ�����\n[%s] ������Ϊ���ַ���" % ( mapping )
	
	#	ƴװ����ͷ��Ϣ:	�ܳ���	Э��汾��	���Ļ�������	ϵͳ��ʶ	�����������	Ӧ�ñ�������01		Ӧ�ñ��ĳ���	��ѡͷ
	result = genReqMsg( sysId, serviceName, result )
	return result

#	��������ӳ��б�����ŵ�HostContext��
def appendDataToList( fieldName , fieldValue ):
	var = loadVar( "HostContext", fieldName )
	if( var == None ):
		storeVar( "HostContext", fieldName , [fieldValue] )
	else:
		var.append( fieldValue )
		storeVar( "HostContext", fieldName , var )

#	��ֽṹ���͵��ֶ�
def analyzeStructData( dataBody ):
	index = 0
	while( index < len( dataBody ) ):
		#	����ֶ�����
		nameLen = struct.unpack( "B", dataBody[index] )[0]
		index += 1
		fieldName = dataBody[index : index + nameLen]
		index += nameLen

		#	����ֶ�ֵ
		valType = struct.unpack( "B", dataBody[index] )[0]
		index += 1
		if( valType == 3 ):			#	�ֽ�����
			fieldValue = struct.unpack( "B", dataBody[index] )[0]
			index += 1
			appendDataToList( fieldName , fieldValue )
		elif( valType == 4 ):		#	����������
			fieldValue = struct.unpack( "!H", dataBody[index : index+2] )[0]
			index += 2
			appendDataToList( fieldName , fieldValue )
		elif( valType == 5 ):		#	4λ����
			fieldValue = struct.unpack( "!L", dataBody[index : index+4] )[0]
			index += 4
			appendDataToList( fieldName , fieldValue )
		elif( valType == 6 ):		#	С��
			valueLen = struct.unpack( "B", dataBody[index] )[0]
			index += 1
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			appendDataToList( fieldName , fieldValue )
		elif( valType == 7 ):		#	���ַ���
			valueLen = struct.unpack( "B", dataBody[index] )[0]
			index += 1
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			appendDataToList( fieldName , fieldValue )
		elif( valType == 8 ):		#	���ֽ���
			valueLen = struct.unpack( "B", dataBody[index] )[0]
			index += 1
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			appendDataToList( fieldName , fieldValue )
		elif( valType == 9 ):		#	����
			fieldValue = dataBody[index : index+8]
			index += 8
			appendDataToList( fieldName , fieldValue )
		elif( valType == 10 ):		#	ʱ��
			fieldValue = dataBody[index : index+6]
			index += 6
			appendDataToList( fieldName , fieldValue )
		elif( valType == 11 ):		#	���ַ���
			valueLen = struct.unpack( "!H", dataBody[index : index+2] )[0]
			index += 2
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			appendDataToList( fieldName , fieldValue )
		elif( valType == 12 ):		#	���ֽ���
			valueLen = struct.unpack( "!H", dataBody[index : index+2] )[0]
			index += 2
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			appendDataToList( fieldName , fieldValue )
		else:
			raise StandardError, "���������������ʹ���0(" + str(valType) + ")"
			
		if( isDebug ):logger.debug( "����ֽṹ�����ݡ���[%s=%s]"%( fieldName, str( fieldValue ) ) )

#	����������͵��ֶ�
def analyzeArrayData( recordNum, dataBody ):
	index = 0
	while( index < len( dataBody ) ):
		#	����ֶ�����
		nameLen = struct.unpack( "B", dataBody[index] )[0]
		index += 1
		fieldName = dataBody[index : index + nameLen]
		index += nameLen

		#	����ֶ�ֵ
		valType = struct.unpack( "B", dataBody[index] )[0]
		index += 1
		if( valType == 1 ):			#	�ṹ������
			structLen = struct.unpack( "!H", dataBody[index : index+2] )[0]
			index += 2
			fieldValue = dataBody[index : index+structLen]
			index += structLen
			analyzeStructData( fieldValue )
		elif( valType == 3 ):		#	�ֽ�����
			fieldValue = struct.unpack( "B", dataBody[index] )[0]
			index += 1
			appendDataToList( fieldName , fieldValue )
		elif( valType == 4 ):		#	����������
			fieldValue = struct.unpack( "!H", dataBody[index : index+2] )[0]
			index += 2
			appendDataToList( fieldName , fieldValue )
		elif( valType == 5 ):		#	4λ����
			fieldValue = struct.unpack( "!L", dataBody[index : index+4] )[0]
			index += 4
			appendDataToList( fieldName , fieldValue )
		elif( valType == 6 ):		#	С��,�ַ�����ʽ
			valueLen = struct.unpack( "B", dataBody[index] )[0]
			index += 1
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			appendDataToList( fieldName , fieldValue )
		elif( valType == 7 ):		#	���ַ���
			valueLen = struct.unpack( "B", dataBody[index] )[0]
			index += 1
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			appendDataToList( fieldName , fieldValue )
		elif( valType == 8 ):		#	���ֽ���
			valueLen = struct.unpack( "B", dataBody[index] )[0]
			index += 1
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			appendDataToList( fieldName , fieldValue )
		elif( valType == 9 ):		#	����,�ַ�����ʽ
			fieldValue = dataBody[index : index+8]
			index += 8
			appendDataToList( fieldName , fieldValue )
		elif( valType == 10 ):		#	ʱ��,�ַ�����ʽ
			fieldValue = dataBody[index : index+6]
			index += 6
			appendDataToList( fieldName , fieldValue )
		elif( valType == 11 ):		#	���ַ���,�ַ�����ʽ
			valueLen = struct.unpack( "!H", dataBody[index : index+2] )[0]
			index += 2
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			appendDataToList( fieldName , fieldValue )
		elif( valType == 12 ):		#	���ֽ���
			valueLen = struct.unpack( "!H", dataBody[index : index+2] )[0]
			index += 2
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			appendDataToList( fieldName , fieldValue )
		else:
			raise StandardError, "���������������ʹ���1(" + str(valType) + ")"
			
		if( isDebug and valType != 1 ):logger.debug( "������������ݡ���[%s=%s]"%( fieldName , str( fieldValue ) ) )

#	���һ���ֶΣ������������͵ı�����Ҫ���⴦��
def analyzeDataBody( dataBody ):
	index = 0
	while( index < len( dataBody ) ):
		#	����ֶ�����
		nameLen = struct.unpack( "B", dataBody[index] )[0]
		index += 1
		fieldName = dataBody[index : index + nameLen]
		index += nameLen

		#	����ֶ�ֵ
		valType = struct.unpack( "B", dataBody[index] )[0]
		index += 1
		if( valType == 2 ):			#	��������
			recordNum, arrayLen = struct.unpack( "!HH", dataBody[index : index+4] )
			index += 4
			fieldValue = dataBody[index : index+arrayLen]
			index += arrayLen
			analyzeArrayData( recordNum, fieldValue )
		elif( valType == 3 ):		#	�ֽ�����
			fieldValue = struct.unpack( "B", dataBody[index] )[0]
			index += 1
			storeVar( "HostContext", fieldName , fieldValue )
		elif( valType == 4 ):		#	����������
			fieldValue = struct.unpack( "!H", dataBody[index : index+2] )[0]
			index += 2
			storeVar( "HostContext", fieldName , fieldValue )
		elif( valType == 5 ):		#	4λ����
			fieldValue = struct.unpack( "!L", dataBody[index : index+4] )[0]
			index += 4
			storeVar( "HostContext", fieldName , fieldValue )
		elif( valType == 6 ):		#	С��,�ַ�����ʽ
			valueLen = struct.unpack( "B", dataBody[index] )[0]
			index += 1
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			storeVar( "HostContext", fieldName , fieldValue )
		elif( valType == 7 ):		#	���ַ���
			valueLen = struct.unpack( "B", dataBody[index] )[0]
			index += 1
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			storeVar( "HostContext", fieldName , fieldValue )
		elif( valType == 8 ):		#	���ֽ���
			valueLen = struct.unpack( "B", dataBody[index] )[0]
			index += 1
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			storeVar( "HostContext", fieldName , fieldValue )
		elif( valType == 9 ):		#	����,�ַ�����ʽ
			fieldValue = dataBody[index : index+8]
			index += 8
			storeVar( "HostContext", fieldName , fieldValue )
		elif( valType == 10 ):		#	ʱ��,�ַ�����ʽ
			fieldValue = dataBody[index : index+6]
			index += 6
			storeVar( "HostContext", fieldName , fieldValue )
		elif( valType == 11 ):		#	���ַ���,�ַ�����ʽ
			valueLen = struct.unpack( "!H", dataBody[index : index+2] )[0]
			index += 2
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			storeVar( "HostContext", fieldName , fieldValue )
		elif( valType == 12 ):		#	���ֽ���
			valueLen = struct.unpack( "!H", dataBody[index : index+2] )[0]
			index += 2
			fieldValue = dataBody[index : index+valueLen]
			index += valueLen
			storeVar( "HostContext", fieldName , fieldValue )
		else:
			raise StandardError, "���������������ʹ���2(" + str(valType) + ")"
			
		if( isDebug and valType != 2 ):logger.debug( "����ְ������ݡ���[%s=%s]"%( fieldName, str( fieldValue ) ) )

#	���������ص������Զ���ֵ��ű�HostContext�й�����ʹ��
def hostUnpack( respData ):
	successFlag = struct.unpack( "B", respData[6] )[0]
	if( successFlag == 2 ):
		#print "�����ɹ�����"
		analyzeDataBody( respData[35 : ] )
	elif( ( successFlag == 3 ) or ( successFlag == 4 ) ):
		HostContext.host_Error = True
		HostContext.host_ErrorType = 7
		HostContext.host_ErrorMsg = rightTrimBlank( respData[11 : 21] )
	else:
		raise StandardError, "δ֪��������������"
