# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.�����ֵ�
#=================================================================
#   �����ļ�:   AfaDict.py
#   �޸�ʱ��:   2006-09-26
##################################################################
import os
from types import *
import exceptions, TradeContext, AfaDBFunc, TradeException, AfaUtilTools
import ConfigParser, time, Party3Context,AfaLoggerFunc,AfaFlowControl

#����item,�ӱ�code���ӱ�codename
def GetDictItem(MainItemName,SubCode):
    if len(MainItemName)==0 or len(SubCode)==0  :
        return False
    MainItem=GetMainDict(MainItemName)
    if MainItem!='0':
        SubCodeName=GetSubDict(MainItem,SubCode)
        return SubCodeName
    else:
        return SubCode
#��ȡ��������
def GetMainDict(ItemName):
    AfaLoggerFunc.tradeInfo('��ȡ�ֵ���������' )
    AfaLoggerFunc.tradeInfo('|'+ItemName+'|')
    sql_m="SELECT * FROM AFA_MAINDICT "
    sql_m=sql_m+"WHERE ITEMENAME='"+ItemName+"'"
    sql_m=sql_m+" ORDER BY ITEM"
    records_m = AfaDBFunc.SelectSql(sql_m)
    AfaLoggerFunc.tradeInfo(sql_m)
    if( records_m == None or len(records_m) == 0):
        AfaLoggerFunc.tradeFatal(sql_m)
        return '0'
    AfaUtilTools.ListFilterNone( records_m )
    AfaLoggerFunc.tradeInfo('|'+records_m[0][0]+'|'+records_m[0][1]+'|'+records_m[0][2]+'|')
    return records_m[0][0]

#��ȡ�ӱ�����
def GetSubDict(MainItem,SubCode):
    AfaLoggerFunc.tradeInfo('��ȡ�ֵ��ӱ�����' )
    AfaLoggerFunc.tradeInfo('|'+MainItem+'|'+SubCode+'|')
    sql_m="SELECT * FROM AFA_SUBDICT "
    sql_m=sql_m+"WHERE ITEM='"+MainItem+"'"
    sql_m=sql_m+"AND CODE='"+SubCode+"'"
    sql_m=sql_m+" ORDER BY ITEM,CODE"
    records_m = AfaDBFunc.SelectSql(sql_m)
    AfaLoggerFunc.tradeInfo(sql_m)
    if( records_m == None or len(records_m) == 0):
        AfaLoggerFunc.tradeFatal(sql_m)
        return 'δ֪'
    AfaUtilTools.ListFilterNone( records_m )
    AfaLoggerFunc.tradeInfo('|'+records_m[0][0]+'|'+records_m[0][1]+'|'+records_m[0][2]+'|')
    return records_m[0][2]
    