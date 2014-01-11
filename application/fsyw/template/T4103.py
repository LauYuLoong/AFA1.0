# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.ȡ���ɷѽ���ģ�壨ֻ��������.
#=================================================================
#   �����ļ�:   4103.py
#   �޸�ʱ��:   2007-10-17 
#   ��    �ߣ�  ZZH
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, FSTransDtlFunc, AfaFlowControl, AfaFsFunc
import TransBillFunc, AfaHostFunc
from types import *

def main( ):
    
    AfaLoggerFunc.tradeInfo( '======����ȡ���ɷѽ���ģ��['+TradeContext.TemplateCode+']=====' )
        
    try:
        #=============��ʼ�����ر��ı���====================
        TradeContext.tradeResponse=[]


        #=============��ȡ��ǰϵͳʱ��====================
        TradeContext.workDate = AfaUtilTools.GetSysDate( )
        TradeContext.workTime = AfaUtilTools.GetSysTime( )

        #begin 20100625 �������޸�
        #TradeContext.sysId       = "AG2008"
        TradeContext.sysId       = TradeContext.appNo
        #end

        TradeContext.agentFlag   = "01"
        TradeContext.__respFlag__='0'

        #=============����ӿ�1====================
        subModuleExistFlag=0
        subModuleName = 'T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode
        try:
            subModuleHandle=__import__( subModuleName )
        except Exception, e:
            AfaLoggerFunc.tradeInfo( e)
        else:
            AfaLoggerFunc.tradeInfo( 'ִ��['+subModuleName+']ģ��' )
            subModuleExistFlag=1
            if( not subModuleHandle.SubModuleDealFst( ) ):
                raise AfaFlowControl.flowException( )

        
        #============У�鹫���ڵ����Ч��==================
        if ( not AfaFsFunc.Cancel_ChkVariableExist( ) ):
            raise AfaFlowControl.flowException( )


        #=============�ж�Ӧ��״̬====================
        if( not AfaFsFunc.ChkAppStatus( ) ):
            raise AfaFlowControl.flowException( )


        #=============�жϷ����������Ƿ�ƥ��ԭ����====================
        if( not AfaFsFunc.ChkRevInfo( TradeContext.preAgentSerno ) ):
            raise AfaFlowControl.flowException( )


        #=============��ȡƽ̨��ˮ��====================
        if( not AfaFunc.GetSerialno( ) ):
            raise AfaFlowControl.flowException( )


        #=============ת��====================
        TradeContext.channelCode = "005"
        TradeContext.userno    = TradeContext.userNo
        TradeContext.tellerno  = TradeContext.teller
        TradeContext.cashTelno = TradeContext.teller
        TradeContext.unitno    = "00000001"
        TradeContext.subUnitno = "00000000"
        if (TradeContext.catrFlag == '0'):    #�ֽ�
            TradeContext.accType = "000"
        else:
            TradeContext.accType = "001"

        #=============������ˮ��====================
        if( not FSTransDtlFunc.InsertDtl( ) ):
            raise AfaFlowControl.flowException( )


        #=============������ͨѶ====================
        AfaHostFunc.CommHost( )
       
        errorCode=TradeContext.errorCode


        #=============���½�����ˮ====================
        if( not FSTransDtlFunc.UpdateDtl( 'TRADE' ) ):
            if errorCode == '0000':
                TradeContext.errorMsg='ȡ�����׳ɹ� '+TradeContext.errorMsg
                
            raise AfaFlowControl.flowException( )


        #=============����ӿ�3====================
        if subModuleExistFlag==1 :
            if( not subModuleHandle.SubModuleDealSnd( ) ):
                TradeContext.errorMsg='ȡ�����׳ɹ� '+TradeContext.errorMsg
                raise AfaFlowControl.flowException( )


        #=============�Զ����====================
        AfaFunc.autoPackData()

        AfaLoggerFunc.tradeInfo( '�˳�ȡ���ɷѽ���ģ��['+TradeContext.TemplateCode+']' )

    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )

    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )

    except Exception, e:
        AfaFlowControl.exitMainFlow( str( e ) )
