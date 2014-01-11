# -*- coding: gbk -*-
##################################################################
#   ����ͨϵͳ .���ù�����
#=================================================================
#   �����ļ�:   UtilTools.py
#   �޸�ʱ��:   2006-08-11
##################################################################
import time,random,ConfigParser,os

#��ȥ�ո�(�Ʊ��)
def ltrim( s ):
    return s.lstrip( )

#����ȥ�ո�
def lrtrim( s ):
    return s.strip( )

#��ȥ�ո�
def rtrim( s ):
    return s.rstrip( )

#ȥ���пո�
def trim( s ):
    temp=[]
    for i in range( len( s ) ):
        if s[i]!='\x20' and s[i]!='\x09':
            temp.append( s[i] )
    return ''.join( temp )

#ɾ���ض��ַ� 
def Delchar( a, b ):
    return a.replace( b, '' )

#split() ���ָ�����
def Split( a, b ):
    return a.split( b )

#����� aΪ��Ҫ����string bΪ����ܳ��� cΪ����ַ� Ĭ��Ϊ'0'���޲���Cʱ��
def Lfill( a, b, c='0' ):
    return a.rjust( b, c )
    
#����� aΪ��Ҫ����string bΪ����ܳ��� cΪ����ַ� Ĭ��Ϊ'0'���޲���Cʱ��
def Rfill( a, b, c='0' ):
    return a.ljust( b, c )

#���ָ����ϣ�bΪ�ָ����aΪ��stringΪԪ�ص�list
def Combine( a, b ):
    return b.join( a )

#����ǧ�ַ�  ���Ϊ�ַ��� ��С���� �������κ���� .1���Ͳ���
def InsComma( s ):
    t=s.find( '.' )
    temp=list( s )
    if s[0]!='-':
        for x in xrange( t-3, 0, -3 ):
            temp.insert( x, ',' )
        return ''.join( temp )
    else:
        for x in xrange( t-3, 0+1, -3 ):
            temp.insert( x, ',' )
        return ''.join( temp )


#ɾ��ǧ�ַ�
def DelComma( s ):
    return ''.join( s.split( ',' ) )

#����С����
def InsDot( s, b=2 ):
    s=str(s)
    if s[0]!='-': 
        if len( s )>b:
            temp=list( s )
            temp.insert( len( temp )-b, '.' )
            return ''.join( temp )
        else: 
            return '0.'+'0'*( b-len(s) )+s
    else:
        if len( s[1:] )>b:
            temp=list( s )
            temp.insert( len( temp )-b, '.' )
            return ''.join( temp )
        else:
            return '-'+'0.'+'0'*( b-len(s[1:]) )+s[1:]

#ɾ��С����
def DelDot( s ):
    s=str(s)
    temp=s.find( '.' )
    return str( int( s[0:temp]+s[temp+1:len( s )] ) )

#����һ ����С�����ǧ�ַ�
def Convert( s, b=2 ):
    s=str(s)
    t=InsDot(s,b)
    return InsComma(t)



#ɾ������һ
def Unconvert( s ):
    s=str(s)
    t=s.replace( ',', '' )
    return str( int( t.replace( '.', '' ) ) )

#��ȡϵͳʱ��
def GetSysTime( ):
    return time.strftime( '%H%M%S', time.localtime( ) )

#��ȡ��ʽʱ��
def GetSysTimeFormat( format ):
    return time.strftime( format, time.localtime( ) )

#��ȡϵͳ����
def GetSysDate( ):
    return time.strftime( '%Y%m%d', time.localtime( ) )

#���ڼӷָ���
def DateAddSign( date, sign='-' ):
    if( len( date ) == 8 and date.isdigit( ) ):
        return date[0:4]+sign+date[4:6]+sign+date[6:8]
    else:
        return date

#����ȥ�ָ���
def DateDelSign( date ):
    if( len( date ) != 10 ):
        return date
    else:
        return date[0:4]+date[5:7]+date[8:10]

#ʱ��ӷָ�ð��
def TimeAddSign( time ):
    sign=':'
    if( len( time ) == 6 and time.isdigit( ) ):
        return time[0:2]+sign+time[2:4]+sign+time[4:6]
    else:
        return time

#ʱ��ȥ�ָ�ð��
def TimeDelSign( time ):
    if( len( time ) != 8 ):
        return time
    else:
        return time[0:2]+time[3:5]+time[6:8]

#==========================�����ת�������Ĵ�д==========================
def ToCNAmount( numStr="0", minUnitFlag=0 ):
    MaxStrLen=12
    tmpResult=""
    sResult=""
    sCount=( "��", "Ҽ", "��", "��", "��", "��", "½", "��", "��", "��" )
    sUnit=( "ʰ", "��", "Ǫ", "��", "ʰ", "��", "Ǫ", "��", "ʰ", "Ԫ", "��", "��" )

    sln = len( numStr )
    if sln > MaxStrLen :
        return None
    for i in range( 0, sln ):
        if i<2 and sln>2 and minUnitFlag==0 and int( numStr[sln-2] )==0 and int( numStr[sln-1] )==0 :
            tmpResult=""
        else:
            tmpResult=tmpResult+sUnit[MaxStrLen-1-i]+sCount[int( numStr[sln-i-1] )]
    nTmp=len( tmpResult )
    for i in range( 0, nTmp/2 ):
        sResult=sResult+tmpResult[nTmp-2-2*i:nTmp-2*i]
    if sln>2 and minUnitFlag==0 and int( numStr[sln-2] )==0 and int( numStr[sln-1] )==0:
        sResult=sResult+"��"
    return sResult
    
#Noneת����'',ֻ�ܽ�None����List�е�Noneת����'',ֻ֧��һά
def ListFilterNone( resource,result='' ):
    if( resource is None ):
        return result
    if( type( resource ) is not list and type( resource ) is not tuple):
        return resource
    if( len( resource )==0 ):
        return resource
    if( type( resource ) is  tuple ):
        resource=list(resource)
    for i in range( 0, len( resource ) ):
        resource[i]=ListFilterNone(resource[i],result)
    return resource
    

#=======================??????????===========================
def Randstr(a=16):
    temp=[]
    for x in xrange(0,a):
        temp.append(random.choice(['1','2','3','4','5','6','7','8','9','0']))
    return ''.join(temp)
    
#��ȡ�ַ������Ӵ�
def substr( srcString ,ibegin, iend):
    desString =""
    for i in range(ibegin-1,iend):
        desString = desString +srcString[i]
    return desString

#    ��ָ�����ַ����������ַ�����ָ���ĳ���
def lFillWithChar( srcString, totalLength, fillChar ):
    srcLen = len( srcString )    
    if( srcLen > totalLength ):
        print "Error: string too long,can't fill(", srcLen, ">", totalLength, ")!"
        return None       
    if( srcLen == totalLength ):
        return srcString
            
    if( srcLen < totalLength ):
        result = srcString
        while( srcLen < totalLength ):
            result = fillChar + result
            srcLen = srcLen + 1
        return result
        
#    ��ָ�����ַ����ұ�����ַ�����ָ���ĳ���
def rFillWithChar( srcString, totalLength, fillChar ):
    srcLen = len( srcString )    
    if( srcLen > totalLength ):
        print "Error: string too long,can't fill(", srcLen, ">", totalLength, ")!"
        return None       
    if( srcLen == totalLength ):
        return srcString
            
    if( srcLen < totalLength ):
        result = srcString
        while( srcLen < totalLength ):
            result = result + fillChar
            srcLen = srcLen + 1
        return result

#    ���ַ�����߿�ʼɾ��ָ�����ַ�
def lStripChar( srcString , stripChar ):
    index = 0
    while( srcString[index] == stripChar ):
        index = index + 1    
    return srcString[index:]
 
#    ���ַ����ұ߿�ʼɾ��ָ�����ַ� 
def rStripChar( srcString , stripChar ):
    index = len( srcString )
    while( srcString[index - 1] == stripChar ):
        index = index - 1    
    return srcString[:index]

#    �ַ������/ɾ���ո��
def lFillWithBlank( srcString, totalLength ):
    return lFillWithChar( srcString, totalLength, ' ' )
def rFillWithBlank( srcString, totalLength ):
    return rFillWithChar( srcString, totalLength, ' ' ) 
def lStripBlank( srcString ):
    return lStripChar( srcString , ' ' )       
def rStripBlank( srcString ):
    return rStripChar( srcString , ' ' )

#    �ַ������/ɾ��"0"
def lFillWithZero( srcString, totalLength ):
    return lFillWithChar( srcString, totalLength, '0' )
def rFillWithZero( srcString, totalLength ):
    return rFillWithChar( srcString, totalLength, '0' )    
def lStripZero( srcString ):
    return lStripChar( srcString , '0' )   
def rStripZero( srcString ):
    return rStripChar( srcString , '0' )
    
    

#    ͨ�������ļ���ʽ��ȡ�ػ����̵�sleepʱ��
def getConfig( configFileName = None ):
	config = ConfigParser.ConfigParser( )
	if( configFileName == None ):
		configFileName = os.environ['AFAP_HOME'] + '/conf/yxtconf/yxt.conf'   
	config.readfp( open( configFileName ) )
	result = [config.get( 'YXTCONFIG', 'KERNELTIME' ), config.getint( 'YXTCONFIG', 'AFAPTIME' ), config.getint( 'YXTCONFIG', 'SMSTIME' )]
	return result
