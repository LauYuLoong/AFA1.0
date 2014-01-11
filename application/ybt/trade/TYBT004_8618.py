# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   TYBT004_8618.py
#   ����˵��:   [����ͨ���ܲ�ѯ]
#   �޸�ʱ��:   2010-07-30
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaDBFunc
import AfaHostFunc,LoggerHandler,YbtFunc
from types import *

def SubModuleDoFst( ):
    
    AfaLoggerFunc.tradeInfo( '��ʼ�����ܲ�ѯ���ױ���' )
    
    if( not (TradeContext.existVariable( "insuid" ) ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '������[insuid]ֵ������!' )

    if( not (TradeContext.existVariable( "productid" ) ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '����[productid]ֵ������!' )

    if( not (TradeContext.existVariable( "instno" ) ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '������[instno]ֵ������!' )

    if( not (TradeContext.existVariable( "salerno" ) ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '����Ա������[salerno]ֵ������!' )

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
    AfaLoggerFunc.tradeInfo('��������ͨ���ܲ�ѯ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    
    tradelogger = LoggerHandler.getLogger( "ybt" )
    
    res = YbtFunc.CreatTotalReport(tradelogger)
    if(res != 0):
        return False
    else:
        TradeContext.errorCode = '0000'
        return True
