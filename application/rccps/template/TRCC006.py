# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������ģ��(1.���ز��� 2.���Ļ�ִ)
#===============================================================================
#   ģ���ļ�:   TRCC006.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ������
#   �޸�ʱ��:   2008-06-02
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
import rccpsFunc,rccpsConst,rccpsGetFunc
from types import *
from rccpsConst import *

def main( ):


    AfaLoggerFunc.tradeInfo('***ũ����ϵͳ: ����.���������ģ��['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']����***')
    

    try:
    
        #=====================��ʼ�����ر��ı���================================
        TradeContext.tradeResponse=[]


        #=====================��ȡϵͳ����ʱ��==================================
        TradeContext.BJEDTE=AfaUtilTools.GetHostDate( )
        #TradeContext.BJEDTE = PL_BJEDTE
        TradeContext.BJETIM=AfaUtilTools.GetSysTime( )
        #TradeContext.TRCDAT=AfaUtilTools.GetHostDate( )
        #TradeContext.TRCDAT = PL_BJEDTE

        #=====================ϵͳ����У��======================================
        if not rccpsFunc.ChkPubInfo(PL_BRSFLG_RCV) :
            raise AfaFlowControl.flowException( )

        #=====================ϵͳ״̬У��======================================
        if not rccpsFunc.ChkSysInfo( 'AFA' ) :
            raise AfaFlowControl.flowException( )

        #=====================�����Ϸ���У��====================================
        if not rccpsFunc.ChkUnitInfo( PL_BRSFLG_RCV ) :
            raise AfaFlowControl.flowException( )

        #=====================��ȡ��������====================================
        if not rccpsFunc.GetNCCDate( ) :
            raise AfaFlowControl.flowException( )

        #=====================��ȡƽ̨��ˮ��====================================
        if rccpsGetFunc.GetSerialno(PL_BRSFLG_RCV) == -1 :
            raise AfaFlowControl.flowException( )


        #=====================��ȡ������ˮ��====================================
        if rccpsGetFunc.GetRccSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )
        

        #=====================��̬���ؽ��׽ű�==================================
        trxModuleName = 'T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode
        try:
            trxModuleHandle=__import__( trxModuleName )

        except Exception, e:
            AfaLoggerFunc.tradeInfo(e)
            raise AfaFlowControl.flowException( 'A0001', '���ؽ��׽ű�ʧ�ܻ��׽ű�������,ִ�н���ʧ��' )


        #=====================����ǰ����(�Ǽ���ˮ,����ǰ����)===================
        if not trxModuleHandle.SubModuleDoFst( ) :
            raise AfaFlowControl.flowException( )


        #=====================������ͨѶ(��ִ)==================================
        AfaAfeFunc.CommAfe()

        #=====================���׺���========================================
        if not trxModuleHandle.SubModuleDoSnd( ) :
            raise AfaFlowControl.flowException( )


        #=====================�Զ����==========================================
        AfaFunc.autoPackData()


        #=====================�˳�ģ��==========================================
        AfaLoggerFunc.tradeInfo('***ũ����ϵͳ: ����.���������ģ��['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']�˳�***')


    except AfaFlowControl.flowException, e:
        #�����쳣
        if not AfaDBFunc.RollbackSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeError(">>>Rollback�쳣")
        AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
        
        AfaFlowControl.exitMainFlow( str(e) )

    except AfaFlowControl.accException:
        #�����쳣
        if not AfaDBFunc.RollbackSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeError(">>>Rollback�쳣")
        AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
        
        AfaFlowControl.exitMainFlow( )
            
    except Exception, e:
        #Ĭ���쳣
        if not AfaDBFunc.RollbackSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeError(">>>Rollback�쳣")
        AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
        
        AfaFlowControl.exitMainFlow( str(e) )
