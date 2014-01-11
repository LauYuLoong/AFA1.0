# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   TYBT004_8619.py
#   ����˵��:   [����ͨ��ϸ��ѯ]
#   �޸�ʱ��:   2010-08-12
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaDBFunc
import AfaHostFunc,YbtFunc,LoggerHandler
from types import *

def SubModuleDoFst( ):
    
    AfaLoggerFunc.tradeInfo( '��ʼ�����ױ���' )
    
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
            return AfaFlowControl.ExitThisFlow( 'A0001', '�ն˺�[termid]ֵ������!' )
        
    return True

def SubModuleDoSnd():
    
    AfaLoggerFunc.tradeInfo('��������ͨ��ϸ��ѯ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
   
    tradelogger = LoggerHandler.getLogger( "ybt" )
    
    res = YbtFunc.CreatDetailReport(tradelogger)
    if(res != 0):
        #return AfaFlowControl.ExitThisFlow("A999","��������ͨ��ϸ����ʧ��")
        return False
    else:
        TradeContext.errorCode = '0000'
        return True
