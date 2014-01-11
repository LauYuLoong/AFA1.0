# -*- coding: gbk -*-
##################################################################
#   ��˰���к�������.ȡ���ɷѽ���ģ�壨ֻ��������.
#=================================================================
#   �����ļ�:   TPS003.py
#   �޸�ʱ��:   2008-5-2 10:24
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools, TipsFunc
from types import *

def main( ):
    AfaLoggerFunc.tradeInfo( '======����ȡ���ɷѽ���ģ��['+TradeContext.TemplateCode+']=====' )
    try:
        #=============��ʼ�����ر��ı���====================
        TradeContext.tradeResponse=[]
        
        #=============��ȡ��ǰϵͳʱ��====================
        if not (TradeContext.existVariable( "workDate" ) and len(TradeContext.workDate)>0):
            TradeContext.workDate = UtilTools.GetSysDate( )
        TradeContext.workTime = UtilTools.GetSysTime( )
        TradeContext.appNo      ='AG2010'
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
            if( not subModuleHandle.SubModuleDealFst( ) ):
                raise TipsFunc.flowException( )

        #============У�鹫���ڵ����Ч��==================
        if ( not TipsFunc.Cancel_ChkVariableExist( ) ):
            raise TipsFunc.flowException( )

        #=============�ж�Ӧ��״̬====================
        if( not TipsFunc.ChkAppStatus( ) ):
            raise TipsFunc.flowException( )

        #=============�жϷ����������Ƿ�ƥ��ԭ����====================
        if( not TipsFunc.ChkRevInfo( TradeContext.preAgentSerno ) ):
            raise TipsFunc.flowException( )

        #=============��ȡƽ̨��ˮ��====================
        if( not TipsFunc.GetSerialno( ) ):
            raise TipsFunc.flowException( )

        #=============������ˮ��====================
        if( not TipsFunc.InsertDtl( ) ):
            raise TipsFunc.flowException( )

        #=============������ͨѶ====================
        TipsFunc.CommHost( )
       
        errorCode=TradeContext.errorCode
        if TradeContext.errorCode=='SXR0010' :  #ԭ���������ѳ��������ɳɹ�����
            TradeContext.__status__='0'
            TradeContext.errorCode, TradeContext.errorMsg = '0000', '�����ɹ�'

        #=============���½�����ˮ====================
        if( not TipsFunc.UpdateDtl( 'TRADE' ) ):
            if errorCode == '0000':
                TradeContext.errorMsg='ȡ�����׳ɹ� '+TradeContext.errorMsg
            raise TipsFunc.flowException( )

        #=============����ӿ�3====================
        if subModuleExistFlag==1 :
            if( not subModuleHandle.SubModuleDealSnd( ) ):
                TradeContext.errorMsg='ȡ�����׳ɹ� '+TradeContext.errorMsg
                raise TipsFunc.flowException( )

        #=============�Զ����====================
        TipsFunc.autoPackData()
        
        AfaLoggerFunc.tradeInfo( '�˳�ȡ���ɷѽ���ģ��['+TradeContext.TemplateCode+']' )
        
    except TipsFunc.flowException, e:
        # print e
        TipsFunc.exitMainFlow( )
    except TipsFunc.accException:
        # print e
        TipsFunc.exitMainFlow( )
    except Exception, e:
        # print e
        TipsFunc.exitMainFlow( str( e ) )
