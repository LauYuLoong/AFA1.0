# -*- coding: gbk -*-
##################################################################
#   ��˰���к�������.�ɷѽ���ģ�壨ֻ������������δ֪���Զ�������.
#=================================================================
#   �����ļ�:   TPS002.py
#   �޸�ʱ��:   2008-5-2 10:24
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools, TipsFunc
#import Party3Context,AfaAfeFunc,AfaHostFunc
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
                raise TipsFunc.flowException( )

        #=============��ȡƽ̨��ˮ��====================
        if TipsFunc.GetSerialno( ) == -1 :
            raise TipsFunc.flowException( )

        #============У�鹫���ڵ����Ч��==================
        if( not TipsFunc.Pay_ChkVariableExist( ) ):
            raise TipsFunc.flowException( )

        #=============�ж�Ӧ��״̬====================
        if not TipsFunc.ChkAppStatus( ) :
            raise TipsFunc.flowException( )


        #=============������ˮ��====================
        if not TipsFunc.InsertDtl( ) :
            raise TipsFunc.flowException( )

        #=============������ͨѶ====================
        TipsFunc.CommHost()

        #=============������������״̬====================
        if( not TipsFunc.UpdateDtl( 'TRADE' ) ):
            if( TradeContext.__status__=='2' ):
                raise TipsFunc.accException( )
            raise TipsFunc.flowException( )

        #=============�Զ����====================
        TipsFunc.autoPackData()

        #print TradeContext.tradeResponse

        AfaLoggerFunc.tradeInfo('=====�˳��ɷѽ���ģ��['+TradeContext.TemplateCode+']=====')

        #=============�����˳�====================

    except TipsFunc.flowException, e:
        # print e
        TipsFunc.exitMainFlow( )

    except TipsFunc.accException,e:
        # print e

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

            if TipsFunc.GetSerialno( ) == -1 :
                raise TipsFunc.exitMainFlow( )

             #=============������ˮ��====================
            if not TipsFunc.InsertDtl( ) :
                raise TipsFunc.exitMainFlow( )

            #=============������ͨѶ====================
            TipsFunc.CommHost()

            #=============������������״̬====================
            if( not TipsFunc.UpdateDtl( 'TRADE' ) ):
                raise TipsFunc.exitMainFlow( )

            TradeContext.errorCode = 'A0048'

            if TradeContext.__status__ == '0':
                TradeContext.errorMsg = '����ʧ��:' + ErrorMessage + '(ϵͳ�Զ������ɹ�)'
            else:
                TradeContext.errorMsg = '����ʧ��:' + ErrorMessage + '(ϵͳ�Զ�����ʧ��)'

            TipsFunc.exitMainFlow()

        else:
            TipsFunc.exitMainFlow( )

        TipsFunc.exitMainFlow( )

    except Exception, e:
        # print e
        TipsFunc.exitMainFlow( str(e))
