# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   5204_8438.py
#   ����˵��:   [�����ջ��ܲ�ѯ]
#   �޸�ʱ��:   2009-04-07
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaDBFunc
import AfaHostFunc,CpicFunc,LoggerHandler
from types import *

def SubModuleDoFst( ):
    AfaLoggerFunc.tradeInfo( '��ʼ�����ױ���' )
    #AfaLoggerFunc.tradeInfo( '�����ױ���ֵ����Ч��У��' )
    if( not (TradeContext.existVariable( "startdate" ) and TradeContext.startdate != '00000000') ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '��ʼ����[startdate]ֵ������!' )
    if( not (TradeContext.existVariable( "enddate" ) and TradeContext.enddate != '00000000' ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '��ֹ����[enddate]ֵ������!' )
    if( not TradeContext.existVariable( "channelCode" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '��������[channelCode]ֵ������!' )
    if( TradeContext.channelCode == '005' ):
        if( not TradeContext.existVariable( "tellerno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '��Ա��[tellerno]ֵ������!' )
        if( not TradeContext.existVariable( "brno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '�����[brno]ֵ������!' )
        if( not TradeContext.existVariable( "termid" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '��Ա��[termid]ֵ������!' )
    return True
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('��������ջ��ܲ�ѯ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    #=====�õ�ccip��־��handler====
    tradelogger = LoggerHandler.getLogger( "cpic" )
    res = CpicFunc.CreatReport(tradelogger)
    if(res != 0):
        #return AfaFlowControl.ExitThisFlow("A999","������ϸ����ʧ��")
        return False
    else:
        TradeContext.errorCode = '0000'
        return True
