# -*- coding: gbk -*-
##################################################################
#   ��˰���к�������.�ɷѽ���ģ�壨�������������ϵ�������.
#=================================================================
#   �����ļ�:   TPS004.py
#   �޸�ʱ��:   2008-5-2 10:24
#   ����һ����־flag �����ж��Ƿ������ʧ��
#   ���������ʧ����Ϊ�ɹ�����
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools, AfaFlowControl, TipsFunc
import Party3Context,AfaAfeFunc,AfaHostFunc
from types import *

def main( ):
    AfaLoggerFunc.tradeInfo('======����ɷѽ���ģ��['+TradeContext.TemplateCode+']=======')
    flag = 0
    try:
        #=============��ʼ�����ر��ı���====================
        TradeContext.tradeResponse=[]

        #=============��ȡ��ǰϵͳʱ��====================
        if not (TradeContext.existVariable( "workDate" ) and len(TradeContext.workDate)>0):
            TradeContext.workDate = UtilTools.GetSysDate( )
        TradeContext.workTime = UtilTools.GetSysTime( )
        
        TradeContext.appNo      ='TIPS'
        TradeContext.busiNo     ='00000000000001'

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
        if TipsFunc.GetSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )

        #============У�鹫���ڵ����Ч��==================
        if( not TipsFunc.Pay_ChkVariableExist( ) ):
            raise AfaFlowControl.flowException( )

        ##=============�ж�Ӧ��״̬====================
        #if not TipsFunc.ChkAppStatus( ) :
        #    raise AfaFlowControl.flowException( )
        #
        #=============��ѯժҪ����====================
        #if not TipsFunc.GetSummaryCode( ) :
        #    raise AfaFlowControl.flowException( )
        #
        #=============������ˮ��====================
        if not TipsFunc.InsertDtl( ) :
            raise AfaFlowControl.flowException( )

        #=============������ͨѶ====================
        TipsFunc.CommHost()

        #=============������������״̬====================
        if( not TipsFunc.UpdateDtl( 'BANK' ) ):
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
        if( not TransDtlFunc.UpdateDtl( 'CORP' ) ):
            raise AfaFlowControl.accException( )

        #=============����ӿ�3====================
        billData=[]
        if subModuleExistFlag==1 :
            billData=subModuleHandle.SubModuledoTrd( )
            if billData==None :
                raise AfaFlowControl.flowException( )

        #=============��Ʊ��Ϣ����====================
        if not ( TransBillFunc.InsertBill( billData ) ) :
            raise AfaFlowControl.flowException( )

        #=============�Զ����====================
        TipsFunc.autoPackData()

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

            if TipsFunc.GetSerialno( ) == -1 :
                raise AfaFlowControl.exitMainFlow( )

             #=============������ˮ��====================
            if not TransDtlFunc.InsertDtl( ) :
                raise AfaFlowControl.exitMainFlow( )

            #=============������ͨѶ====================
            TipsFunc.CommHost()

            #=============������������״̬====================
            if( not TipsFunc.UpdateDtl( 'BANK' ) ):
                raise AfaFlowControl.exitMainFlow( )

            TradeContext.errorCode = 'A0048'

            if TradeContext.__status__ == '0':
                TradeContext.errorMsg = '����ʧ��:' + ErrorMessage + '(ϵͳ�Զ������ɹ�)'
            else:
                TradeContext.errorMsg = '����ʧ��:' + ErrorMessage + '(ϵͳ�Զ�����ʧ��)'

            AfaFlowControl.exitMainFlow()

        else:
            AfaFlowControl.exitMainFlow( )

        AfaFlowControl.exitMainFlow( )

    except Exception, e:
        # print e
        AfaFlowControl.exitMainFlow( str(e))
