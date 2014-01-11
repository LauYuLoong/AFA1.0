# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.�ɷѽ���ģ�壨ֻ������������δ֪���Զ�������. Ϊ�˷�˰�˸���������������ʺ�
#=================================================================
#   �����ļ�:   4102.py
#   �޸�ʱ��:   2007-10-17
#   ��    �ߣ�  ZZH
##################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,FSTransDtlFunc,AfaFlowControl,AfaFsFunc
import AfaAfeFunc, AfaHostFunc
from types import *

from types import *

def main( ):
    
    AfaLoggerFunc.tradeInfo('======����ɷѽ���ģ��['+TradeContext.TemplateCode+']=======')

    #begin 20100625 �������޸�
    #TradeContext.sysId       = "AG2008"
    TradeContext.sysId       = TradeContext.appNo
    #end

    TradeContext.agentFlag = "01"
    TradeContext.__respFlag__='0'

    flag = 0

    try:
        #=============��ʼ�����ر��ı���====================
        TradeContext.tradeResponse=[]

        #=============��ȡ��ǰϵͳʱ��====================
        TradeContext.workDate = AfaUtilTools.GetSysDate( )
        TradeContext.workTime = AfaUtilTools.GetSysTime( )

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
            if not subModuleHandle.SubModuleDoFst( ) :
                raise AfaFlowControl.flowException( )


        #=============��ȡƽ̨��ˮ��====================
        if AfaFunc.GetSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )

        AfaLoggerFunc.tradeInfo('======1=======')

        #============У�鹫���ڵ����Ч��==================
        if( not AfaFsFunc.Pay_ChkVariableExist( ) ):
            raise AfaFlowControl.flowException( )

        AfaLoggerFunc.tradeInfo('======2=======')

        #=============�ж�Ӧ��״̬====================
        if not AfaFsFunc.ChkAppStatus( ) :
            raise AfaFlowControl.flowException( )

        AfaLoggerFunc.tradeInfo('======3=======')

        if subModuleExistFlag==1 :
            subModuleHandle.SubModuleDoFstMore( ) 

        AfaLoggerFunc.tradeInfo('======4=======')

        #=============��ѯժҪ����====================
        if not AfaFunc.GetSummaryInfo( ) :
            raise AfaFlowControl.flowException( )

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
        if not FSTransDtlFunc.InsertDtl( ) :
            raise AfaFlowControl.flowException( )

        AfaLoggerFunc.tradeInfo('======5.5=======')


        #=============������ͨѶ====================
        AfaHostFunc.CommHost()

        AfaLoggerFunc.tradeInfo('======6=======')

        #=============������������״̬====================
        if( not FSTransDtlFunc.UpdateDtl( 'TRADE' ) ):
            if( TradeContext.__status__=='2' ):
                raise AfaFlowControl.accException( )
            raise AfaFlowControl.flowException( )

        AfaLoggerFunc.tradeInfo('======7=======')

        billData=[]
        if subModuleExistFlag==1 :
            billData=subModuleHandle.SubModuledoSnd( )
            if billData==None :
                raise AfaFlowControl.flowException( )

        AfaLoggerFunc.tradeInfo('======8=======')

        #=============�Զ����====================
        AfaFunc.autoPackData()

        AfaLoggerFunc.tradeInfo('=====�˳��ɷѽ���ģ��['+TradeContext.TemplateCode+']=====')

        #=============�����˳�====================

    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )

    except AfaFlowControl.accException,e:

        if TradeContext.existVariable("errorMsg"):
            ErrorMessage = TradeContext.errorMsg
        else:
            ErrorMessage = ""

        AfaLoggerFunc.tradeInfo('������:' + ErrorMessage)
        
        AfaLoggerFunc.tradeInfo('�Զ�����')

        if TradeContext.__status__ == '2':
            AfaLoggerFunc.tradeInfo('�����쳣���-->����')
            TradeContext.__autoRevTranCtl__= '1'

        else:
            #����ʧ��
            TradeContext.__autoRevTranCtl__= '0'

        #=============�Զ�����====================
        if TradeContext.__autoRevTranCtl__=='1' :

            #�Զ��������ݳ�ʼ��
            TradeContext.revTranF      = '2'
            TradeContext.preAgentSerno = TradeContext.agentSerialno
            TradeContext.revTrxDate    = TradeContext.workDate

            if AfaFunc.GetSerialno( ) == -1 :
                raise AfaFlowControl.exitMainFlow( )


            #=============������ˮ��====================
            if not FSTransDtlFunc.InsertDtl( ) :
                raise AfaFlowControl.exitMainFlow( )

            #=============������ͨѶ====================
            AfaHostFunc.CommHost( )


            #=============������������״̬====================
            if( not FSTransDtlFunc.UpdateDtl( 'TRADE' ) ):
                raise AfaFlowControl.exitMainFlow( )


            TradeContext.errorCode = 'A0048'

            if TradeContext.__status__ == '0':
                TradeContext.errorMsg = '�����������쳣:' + ErrorMessage + '(ϵͳ�Զ������ɹ�)'
            else:
                TradeContext.errorMsg = '�����������쳣:' + ErrorMessage + '(ϵͳ�Զ�����ʧ��)'

            AfaFlowControl.exitMainFlow()

        else:
            AfaFlowControl.exitMainFlow( )

        AfaFlowControl.exitMainFlow( )

    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
