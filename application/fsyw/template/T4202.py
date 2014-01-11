# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.�ɷѽ���ģ�壨�������������ϵ�������.
#=================================================================
#   �����ļ�:   4202.py
#   �޸�ʱ��:   2006-09-11
#   ����һ����־flag �����ж��Ƿ������ʧ��
#   ���������ʧ��(�Ϸʵ���)��Ϊ�ɹ�����
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, FSTransDtlFunc, AfaFlowControl, AfaFsFunc
import Party3Context, AfaAfeFunc, AfaHostFunc
from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('======����ɷѽ���ģ��['+TradeContext.TemplateCode+']=======')
    
    flag = 0
    
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
            if not subModuleHandle.SubModuleDoFst( ) :
                raise AfaFlowControl.flowException( )


        #=============��ȡƽ̨��ˮ��====================
        if AfaFunc.GetSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )


        #============У�鹫���ڵ����Ч��==================
        if( not AfaFsFunc.Pay_ChkVariableExist( ) ):
            raise AfaFlowControl.flowException( )


        #=============��ѯժҪ����====================
        if not AfaFunc.GetSummaryInfo( ) :
            raise AfaFlowControl.flowException( )
            
        #=============�ж�ϵͳ״̬====================
        if not AfaFsFunc.ChkAppStatus( ) :
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
        if not FSTransDtlFunc.InsertDtl( ) :
            raise AfaFlowControl.flowException( )

        #=============������ͨѶ====================
        AfaHostFunc.CommHost()

        #=============������������״̬====================
        if( not FSTransDtlFunc.UpdateDtl( 'BANK' ) ):
            if( TradeContext.__status__=='2' ):
                flag = 1
                raise AfaFlowControl.accException( )

            raise AfaFlowControl.flowException( )

        #=============����ӿ�2====================
        if subModuleExistFlag==1 :
            if not subModuleHandle.SubModuledoSnd( ) :
                raise AfaFlowControl.flowException( )

        AfaLoggerFunc.tradeInfo('��ͨѶǰ��ͨѶ')
            
        #=============��ͨѶǰ��ͨѶ====================
        AfaAfeFunc.CommAfe()

        #=============���µ���������״̬====================
        if( not FSTransDtlFunc.UpdateDtl( 'CORP' ) ):
            raise AfaFlowControl.accException( )

        #=============����ӿ�3====================
        billData=[]
        if subModuleExistFlag==1 :
            billData=subModuleHandle.SubModuledoTrd( )
            if billData==None :
                raise AfaFlowControl.flowException( )

        #=============�Զ����====================
        AfaFunc.autoPackData()

        #print TradeContext.tradeResponse

        AfaLoggerFunc.tradeInfo('=====�˳��ɷѽ���ģ��['+TradeContext.TemplateCode+']=====')

        #=============�����˳�====================

    except AfaFlowControl.flowException, e:
        # print e
        AfaFlowControl.exitMainFlow( )

    except AfaFlowControl.accException,e:
        # print e

        if TradeContext.existVariable("errorMsg"):
            ErrorMessage = TradeContext.errorMsg
        else:
            ErrorMessage = ""

        AfaLoggerFunc.tradeInfo('������:' + ErrorMessage)
        AfaLoggerFunc.tradeInfo('�Զ�����')

        if flag==1 and TradeContext.__status__ == '2':
            AfaLoggerFunc.tradeInfo('�����쳣���-->����')
            TradeContext.__autoRevTranCtl__= '1'

        elif flag==0 and ( TradeContext.__status__ == '1' or TradeContext.__status__ == '2' ):
            AfaLoggerFunc.tradeInfo('������(ʧ�ܻ��쳣)���-->����')
            TradeContext.__autoRevTranCtl__= '1'

        else:
            #����ʧ�ܡ��������쳣
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
            AfaHostFunc.CommHost()

            #=============������������״̬====================
            if( not FSTransDtlFunc.UpdateDtl( 'BANK' ) ):
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
        # print e
        AfaFlowControl.exitMainFlow( str(e))
