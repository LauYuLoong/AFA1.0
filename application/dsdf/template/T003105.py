# -*- coding: gbk -*-
################################################################################
#   ���մ���.������ģ��
#===============================================================================
#   ģ���ļ�:   003105.py
#   �޸�ʱ��:   2006-04-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaFlowControl,AfaAfeFunc
from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('******���մ���.������ģ��['+TradeContext.TemplateCode+']����******' )

    try:
    
        #=====================��ʼ�����ر��ı���================================
        TradeContext.tradeResponse=[]


        #=====================��ȡ��ǰϵͳʱ��==================================
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )


        #=====================У�鹫���ڵ����Ч��==============================
        if( not TradeContext.existVariable( "rptType" ) ):
            raise AfaFlowControl.flowException( 'A0001', '��������[rptType]ֵ������,���ܱ����ӡ����' )

        if( not TradeContext.existVariable( "zoneno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '������[zoneno]ֵ������,���ܱ����ӡ����' )
            
        if( not TradeContext.existVariable( "brno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '�����[brno]ֵ������,���ܱ����ӡ����' )

        if( not TradeContext.existVariable( "tellerno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '��Ա��[tellerno]ֵ������,���ܱ����ӡ����' )

        if( not TradeContext.existVariable( "beginDate" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '��ʼ����[beginDate]ֵ������,���ܱ����ӡ����' )

        if( not TradeContext.existVariable( "endDate" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '��������[endDate]ֵ������,���ܱ����ӡ����' )


        #�жϻ�������(1-����Ա���� 2-��������� 3-��֧�л��� 4-�����л���)
        if( int( TradeContext.rptType )<1 or int( TradeContext.rptType )>4 ):           
            return AfaFlowControl.ExitThisFlow( 'A0019', '�Ƿ��Ļ�������' )


        #=====================�����л���========================================
        if (int( TradeContext.rptType )==4):
            AfaLoggerFunc.tradeInfo( '�����л���')



        #=====================��֧�л���========================================
        if(int( TradeContext.rptType )==3):
            AfaLoggerFunc.tradeInfo( '��֧�л���')


        #=====================���������========================================
        if (int( TradeContext.rptType )==2):
            AfaLoggerFunc.tradeInfo( '���������')


        #=====================����Ա����========================================
        if (int( TradeContext.rptType )==1):
            AfaLoggerFunc.tradeInfo( '����Ա����')
  
  
        #=====================�Զ����==========================================
        TradeContext.errorCode='0000'
        TradeContext.errorMsg='���׳ɹ�'
        AfaFunc.autoPackData()

        #=====================�����˳�==========================================
        AfaLoggerFunc.tradeInfo('******���մ���.������ģ��['+TradeContext.TemplateCode+']�˳�******' )

    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) ) 
