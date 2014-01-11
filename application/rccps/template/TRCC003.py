# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������ģ��(1.���ز��� 2.���Ĳ���)
#===============================================================================
#   ģ���ļ�:   TRCC003.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ������
#   �޸�ʱ��:   2008-06-02
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
import rccpsFunc,rccpsGetFunc,AfaAfeFunc,rccpsConst
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
        #�ر�� 20081111 �޸�ί������Ϊ��������
        #TradeContext.TRCDAT=AfaUtilTools.GetHostDate( )
        #�޸Ľ���
        #TradeContext.TRCDAT = PL_BJEDTE


        #=====================ϵͳ����У��======================================
        if not rccpsFunc.ChkPubInfo(PL_BRSFLG_SND) :
            raise AfaFlowControl.flowException( )

        #=====================ϵͳ״̬У��======================================
        if not rccpsFunc.ChkSysInfo( 'RCCPS' ) :
            raise AfaFlowControl.flowException( )

        #=====================�����Ϸ���У��====================================
        if not rccpsFunc.ChkUnitInfo( PL_BRSFLG_SND ) :
            raise AfaFlowControl.flowException( )

        #=====================��ȡ��������====================================
        if not rccpsFunc.GetNCCDate( ) :
            raise AfaFlowControl.flowException( )
            
        #�ر�� 20081111 �޸�ί������Ϊ��������
        TradeContext.TRCDAT=TradeContext.NCCworkDate
        #�޸Ľ���


        #=====================��ȡƽ̨��ˮ��====================================
        if rccpsGetFunc.GetSerialno(PL_BRSFLG_SND) == -1 :
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


        #=====================����ǰ����(���ز���,����ǰ����)===================
        if not trxModuleHandle.SubModuleDoFst( ) :
            raise AfaFlowControl.flowException( )


        #=====================������ͨѶ========================================
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
