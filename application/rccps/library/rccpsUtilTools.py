# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ.���ù�����
#=================================================================
#   �����ļ�:   rccpsUtilTools.py
#   ��    ��:   �ر��
#   �޸�ʱ��:   2008-10-28
##################################################################
import time,random,TradeContext,AfaDBFunc,AfaFlowControl

#ɾ���ַ����еĻ��з�0x0a
def replaceRet( s ):
    temp=[]
    for i in range( len( s ) ):
        if s[i] != '\x0a':
            temp.append( s[i] )
    return ''.join( temp )

#���ǽ�  20081121 �����ַ��������Ӻ���
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
