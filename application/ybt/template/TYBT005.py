# -*- coding: gbk -*-
################################################################################
#   ����ͨ.����ģ��.��ȥ��������ֻȥ����
#===============================================================================
#   ģ���ļ�:   YBT005.py
#   �޸�ʱ��:   2010-08-18
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,Party3Context,AfaTransDtlFunc,AfaAfeFunc,AfaFlowControl,AfaHostFunc,TransBillFunc
from types import *

def main( ):
    AfaLoggerFunc.tradeInfo('******����ͨ���ڳ���ģ��['+TradeContext.TemplateCode+']����******')
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
        if( not AfaFunc.Cancel_ChkVariableExist( ) ):
            raise AfaFlowControl.flowException( )

        #=====================�ж��̻�״̬======================================
        if not AfaFunc.ChkUnitStatus( ) :
            raise AfaFlowControl.flowException( )

        #=====================�ж�����״̬======================================
        if not AfaFunc.ChkChannelStatus( ) :
            raise AfaFlowControl.flowException( )
        
        #=====================�жϷ����������Ƿ�ƥ��ԭ����======================
        if( not AfaFunc.ChkRevInfo( ) ):
            raise AfaFlowControl.flowException( )

        #=====================��ȡƽ̨��ˮ��====================================
        if AfaFunc.GetSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )

        #=====================������ˮ��========================================
        if( not AfaTransDtlFunc.InsertDtl( ) ):
            raise AfaFlowControl.flowException( )

        #=====================����������========================================
        AfaHostFunc.CommHost()

        #=====================���½�����ˮ======================================
        if( not AfaTransDtlFunc.UpdateDtl( 'TRADE' ) ):
            if TradeContext.errorCode == '0000':
                TradeContext.errorMsg='ȡ�����׳ɹ� '+TradeContext.errorMsg
                
            raise AfaFlowControl.flowException( )

        #=====================�Զ����==========================================
        AfaFunc.autoPackData()

        #=====================�����˳�==========================================
        AfaLoggerFunc.tradeInfo('******����ͨ���ڳ���ģ��['+TradeContext.TemplateCode+']�˳�******')

    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
        
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
        
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
