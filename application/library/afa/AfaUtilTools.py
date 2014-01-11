# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.���ù�����
#=================================================================
#   �����ļ�:   AfaUtilTools.py
#   �޸�ʱ��:   2006-03-31
##################################################################
import time,random,TradeContext,AfaDBFunc,AfaFlowControl

#��ȥ�ո�(�Ʊ��)
def ltrim( s ):
    return s.lstrip( )

#����ȥ�ո�
def lrtrim( s ):
    return s.lstrip( )

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

#=====������ 2008-07-07 ɾ��ԭȡϵͳ������ʱ�亯��=====
#��ȡϵͳʱ��
def GetSysTime( ):
    return time.strftime( '%H%M%S', time.localtime( ) )

#��ȡϵͳ����
def GetSysDate( ):
    return time.strftime( '%Y%m%d', time.localtime( ) )

#��ȡ��ʽʱ��
def GetSysTimeFormat( format ):
    return time.strftime( format, time.localtime( ) )

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

#==========SQL��ѯ����Զ����(TradeContext.tradeResponse)===========
def queryResultAutoPack(queryResult,packNames):

    queryResult=ListFilterNone( queryResult )
    for i in range( 0, len( queryResult ) ):
        j=0
        for name in packNames:
            TradeContext.tradeResponse.append([name,queryResult[i][j]])
            j=j+1
    return True

#====��֯����SQL��(��"set unitno='123',subunitno='1234'"),������where�Ӿ�=====
def updateSqlStr(sqlNames):

    i=1
    sqlStr=' set '
    nameNums=len(sqlNames)
    for name in sqlNames:
        sqlStr=sqlStr+name+"='"+getattr(TradeContext,name)+"'"
        if(i!=nameNums):
            sqlStr=sqlStr+","
        i=i+1
    return sqlStr

#========��֯����SQL��(��"(unitno,subunitno) values('1','2')")===========
def insertSqlStr(sqlNames):

    sqlStr=' ('
    i=1
    nameNums=len(sqlNames)
    for name in sqlNames:
        sqlStr=sqlStr+name
        if(i!=nameNums):
            sqlStr=sqlStr+","
        else:
            sqlStr=sqlStr+")"
        i=i+1
    sqlStr = sqlStr+ " values("
    i=1
    for name in sqlNames:
        sqlStr=sqlStr+"'"+getattr(TradeContext,name)+"'"
        if(i!=nameNums):
            sqlStr=sqlStr+","
        else:
            sqlStr=sqlStr+")"
        i=i+1
    return sqlStr

#=====������ 2008-07-07 ����ȡ���ڡ�ʱ�亯��====
def GetHostDate( ):
    sql = "select workdate from afa_date"
    ret = AfaDBFunc.SelectSql(sql)
    if ret == None:
        return AfaFlowControl.ExitThisFlow('S999','���ݿ����ʧ��')
    if len(ret) <= 0:
        return time.strftime( '%Y%m%d', time.localtime( ) )
    else:
        date = ret[0][0]
    return date 

#�ر�� 20091125 ȥ��������ַ�
def trimchn( s ):
    temp = []
    i = 0
    while(i < len(s)):
        if s[i] <= '\x7f':
            temp.append(s[i])
            i+=1
        else:
            if (i+1 < len(s)) and (s[i+1] > '\x7f'):
                temp.append(s[i])
                temp.append(s[i+1])
                i+=2
            else:
                i+=1
    return ''.join(temp)
