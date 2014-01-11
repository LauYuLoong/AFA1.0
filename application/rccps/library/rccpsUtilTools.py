# -*- coding: gbk -*-
##################################################################
#   农信银系统.常用工具类
#=================================================================
#   程序文件:   rccpsUtilTools.py
#   作    者:   关彬捷
#   修改时间:   2008-10-28
##################################################################
import time,random,TradeContext,AfaDBFunc,AfaFlowControl

#删除字符串中的换行符0x0a
def replaceRet( s ):
    temp=[]
    for i in range( len( s ) ):
        if s[i] != '\x0a':
            temp.append( s[i] )
    return ''.join( temp )

#李亚杰  20081121 增加字符串金额相加函数
def JEDelDot( s ):
    if( s.find('.')):
        a = s.split('.')
        if len(a[1]) <= 2:
            s = a[0] + a[1].ljust(2,'0')
            return s
    else:
        s = s + '00'
        return s
        
def AddDot(a,b):
    a = JEDelDot( a )
    b = JEDelDot( b )
    c = str(int(a) + int(b))
    return c[:-2] + '.' + c[-2:]

def FormatMoney(str):
    tmp_list = str.split('.')
    return tmp_list[0] + '.' + tmp_list[1].ljust(2,'0')
