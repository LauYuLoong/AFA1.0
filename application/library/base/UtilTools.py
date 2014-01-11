# -*- coding: gbk -*-
##################################################################
#   银信通系统 .常用工具类
#=================================================================
#   程序文件:   UtilTools.py
#   修改时间:   2006-08-11
##################################################################
import time,random,ConfigParser,os

#左去空格(制表符)
def ltrim( s ):
    return s.lstrip( )

#左右去空格
def lrtrim( s ):
    return s.strip( )

#右去空格
def rtrim( s ):
    return s.rstrip( )

#去所有空格
def trim( s ):
    temp=[]
    for i in range( len( s ) ):
        if s[i]!='\x20' and s[i]!='\x09':
            temp.append( s[i] )
    return ''.join( temp )

#删除特定字符 
def Delchar( a, b ):
    return a.replace( b, '' )

#split() 按分割符拆分
def Split( a, b ):
    return a.split( b )

#左填充 a为需要填充的string b为填充总长度 c为填充字符 默认为'0'（无参数C时）
def Lfill( a, b, c='0' ):
    return a.rjust( b, c )
    
#右填充 a为需要填充的string b为填充总长度 c为填充字符 默认为'0'（无参数C时）
def Rfill( a, b, c='0' ):
    return a.ljust( b, c )

#按分割符组合，b为分割符，a为以string为元素的list
def Combine( a, b ):
    return b.join( a )

#插入千分符  金额为字符型 带小数点 否则不做任何添加 .1类型不可
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


#删除千分符
def DelComma( s ):
    return ''.join( s.split( ',' ) )

#插入小数点
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

#删除小数点
def DelDot( s ):
    s=str(s)
    temp=s.find( '.' )
    return str( int( s[0:temp]+s[temp+1:len( s )] ) )

#二合一 增加小数点和千分符
def Convert( s, b=2 ):
    s=str(s)
    t=InsDot(s,b)
    return InsComma(t)



#删除二合一
def Unconvert( s ):
    s=str(s)
    t=s.replace( ',', '' )
    return str( int( t.replace( '.', '' ) ) )

#获取系统时间
def GetSysTime( ):
    return time.strftime( '%H%M%S', time.localtime( ) )

#获取格式时间
def GetSysTimeFormat( format ):
    return time.strftime( format, time.localtime( ) )

#获取系统日期
def GetSysDate( ):
    return time.strftime( '%Y%m%d', time.localtime( ) )

#日期加分隔线
def DateAddSign( date, sign='-' ):
    if( len( date ) == 8 and date.isdigit( ) ):
        return date[0:4]+sign+date[4:6]+sign+date[6:8]
    else:
        return date

#日期去分隔线
def DateDelSign( date ):
    if( len( date ) != 10 ):
        return date
    else:
        return date[0:4]+date[5:7]+date[8:10]

#时间加分隔冒号
def TimeAddSign( time ):
    sign=':'
    if( len( time ) == 6 and time.isdigit( ) ):
        return time[0:2]+sign+time[2:4]+sign+time[4:6]
    else:
        return time

#时间去分隔冒号
def TimeDelSign( time ):
    if( len( time ) != 8 ):
        return time
    else:
        return time[0:2]+time[3:5]+time[6:8]

#==========================将金额转换成中文大写==========================
def ToCNAmount( numStr="0", minUnitFlag=0 ):
    MaxStrLen=12
    tmpResult=""
    sResult=""
    sCount=( "零", "壹", "贰", "叁", "肆", "伍", "陆", "柒", "捌", "玖" )
    sUnit=( "拾", "亿", "仟", "佰", "拾", "万", "仟", "佰", "拾", "元", "角", "分" )

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
        sResult=sResult+"整"
    return sResult
    
#None转换成'',只能将None或者List中的None转换成'',只支持一维
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
    
#获取字符串的子串
def substr( srcString ,ibegin, iend):
    desString =""
    for i in range(ibegin-1,iend):
        desString = desString +srcString[i]
    return desString

#    用指定的字符从左边填充字符串到指定的长度
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
        
#    用指定的字符从右边填充字符串到指定的长度
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

#    从字符串左边开始删除指定的字符
def lStripChar( srcString , stripChar ):
    index = 0
    while( srcString[index] == stripChar ):
        index = index + 1    
    return srcString[index:]
 
#    从字符串右边开始删除指定的字符 
def rStripChar( srcString , stripChar ):
    index = len( srcString )
    while( srcString[index - 1] == stripChar ):
        index = index - 1    
    return srcString[:index]

#    字符串填充/删除空格符
def lFillWithBlank( srcString, totalLength ):
    return lFillWithChar( srcString, totalLength, ' ' )
def rFillWithBlank( srcString, totalLength ):
    return rFillWithChar( srcString, totalLength, ' ' ) 
def lStripBlank( srcString ):
    return lStripChar( srcString , ' ' )       
def rStripBlank( srcString ):
    return rStripChar( srcString , ' ' )

#    字符串填充/删除"0"
def lFillWithZero( srcString, totalLength ):
    return lFillWithChar( srcString, totalLength, '0' )
def rFillWithZero( srcString, totalLength ):
    return rFillWithChar( srcString, totalLength, '0' )    
def lStripZero( srcString ):
    return lStripChar( srcString , '0' )   
def rStripZero( srcString ):
    return rStripChar( srcString , '0' )
    
    

#    通过配置文件方式读取守护进程的sleep时间
def getConfig( configFileName = None ):
	config = ConfigParser.ConfigParser( )
	if( configFileName == None ):
		configFileName = os.environ['AFAP_HOME'] + '/conf/yxtconf/yxt.conf'   
	config.readfp( open( configFileName ) )
	result = [config.get( 'YXTCONFIG', 'KERNELTIME' ), config.getint( 'YXTCONFIG', 'AFAPTIME' ), config.getint( 'YXTCONFIG', 'SMSTIME' )]
	return result
