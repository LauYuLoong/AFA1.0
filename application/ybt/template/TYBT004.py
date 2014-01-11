  # -*- coding: gbk -*-
################################################################################
#   ����ͨ.��ѯģ��.��ȥ������,��ȥ����
#===============================================================================
#   ģ���ļ�:   YBT004.py
#   �޸�ʱ��:   2010-08-18
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,Party3Context,AfaAfeFunc,AfaFlowControl
from types import *

def main( ):
    AfaLoggerFunc.tradeInfo('******����ͨ���ڲ�ѯģ��[' + TradeContext.TemplateCode + ']����******')
    try:
        
        #=====================��ʼ�����ر��ı���================================
        TradeContext.tradeResponse=[]
        
        #��ȡ��ǰϵͳʱ��
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )
        
        #=====================�ж�Ӧ��ϵͳ״̬==================================
        if not AfaFunc.ChkSysStatus( ) :
            raise AfaFlowControl.flowException( )
        
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
        
        #=====================�ж��̻�״̬======================================
        if not AfaFunc.ChkUnitStatus( ) :
            raise AfaFlowControl.flowException( )
        
        #=====================�ж�����״̬======================================
        if not AfaFunc.ChkChannelStatus( ) :
            raise AfaFlowControl.flowException( )
        
        #=====================��ȡƽ̨��ˮ��====================================
        if AfaFunc.GetSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )
        
        #=====================�������ϵͳ����==================================
        #AfaAfeFunc.CommAfe()
        
        #=====================����ӿ�(����)==================================
        if subModuleExistFlag==1 :
            if not subModuleHandle.SubModuleDoSnd( ) :
                raise AfaFlowControl.flowException( )
        
        #=====================�Զ����==========================================
        AfaFunc.autoPackData()
        
        #=====================�˳�ģ��==========================================
        AfaLoggerFunc.tradeInfo('******����ͨ���ڲ�ѯģ��[' + TradeContext.TemplateCode + ']�˳�******')
        
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )       
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
