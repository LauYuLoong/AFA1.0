  # -*- coding: gbk -*-
################################################################################
#   ���մ���.ģ��.��ѯģ��
#===============================================================================
#   ģ���ļ�:   5201.py
#   
#   �޸�ʱ��:   2006-04-06
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,Party3Context,AfaAfeFunc,AfaFlowControl,AfaAhAdb
from types import *

def main( ):
    AfaLoggerFunc.tradeInfo('******̫����ѯģ��[' + TradeContext.TemplateCode + ']����******')
    try:
        
        #=====================��ʼ�����ر��ı���================================
        TradeContext.tradeResponse=[]
        
        #��ȡ��ǰϵͳʱ��
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )
        
        #=====================����ӿ�(ǰ����)==================================
        subModuleExistFlag = 0
        subModuleName = 'T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode
        try:
            subModuleHandle=__import__( subModuleName )
        except Exception, e:
            AfaLoggerFunc.tradeInfo( e)
        else:
            AfaLoggerFunc.tradeInfo( 'ִ��['+subModuleName+']ģ��' )
            subModuleExistFlag=1
            if not subModuleHandle.SubModuleDoFst( ) :
                raise AfaFlowControl.flowException( )
        
        #=====================У�鹫���ڵ����Ч��==============================
        if( not AfaFunc.Query_ChkVariableExist( ) ):
            raise AfaFlowControl.flowException( )
        
        #=====================�ж�Ӧ��ϵͳ״̬==================================
        if not AfaFunc.ChkSysStatus( ) :
            raise AfaFlowControl.flowException( )
        #=====================�ж��̻�״̬======================================
        if not AfaFunc.ChkUnitStatus( ) :
            raise AfaFlowControl.flowException( )
        
        #=====================�ж�����״̬======================================
        if not AfaFunc.ChkChannelStatus( ) :
            raise AfaFlowControl.flowException( )
        
        #=====================��ȡƽ̨��ˮ��====================================
        if AfaFunc.GetSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )
        
        #=====================������ˮ��========================================
        #if TradeContext.TransCode == "8430":    #ֻ���±�����Ǽ���ˮ
        #    if not AfaAhAdb.AdbInsertQueDtl( ) :
        #        raise AfaFlowControl.flowException( )
        
        #=====================�������ϵͳ����==================================
        AfaAfeFunc.CommAfe()
        
        #=====================����ӿ�(����)==================================
        if subModuleExistFlag==1 :
            if not subModuleHandle.SubModuleDoSnd( ) :
                raise AfaFlowControl.flowException( )
        
        #=====================�Զ����==========================================
        AfaFunc.autoPackData()
        
        #=====================�˳�ģ��==========================================
        AfaLoggerFunc.tradeInfo('******̫����ѯģ���˳�******')
        
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
