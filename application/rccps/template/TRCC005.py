# -*- coding: gbk -*-
################################################################################
#   农信银系统：来账.主机类操作模板(1.本地操作 2.主机记账 3.中心回执)
#===============================================================================
#   模板文件:   TRCC005.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘雨龙
#   修改时间:   2008-06-02
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,rccpsHostFunc,AfaFunc,rccpsGetFunc
import rccpsFunc,rccpsConst
from types import *
from rccpsConst import *

def main( ):


    AfaLoggerFunc.tradeInfo('***农信银系统: 来账.主机类操作模板['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']进入***')


    try:
    
        #=====================初始化返回报文变量================================
        TradeContext.tradeResponse=[]


        #=====================获取系统日期时间==================================
        TradeContext.BJEDTE=AfaUtilTools.GetHostDate( )
        #TradeContext.TRCDAT=AfaUtilTools.GetHostDate( )
        #TradeContext.BJEDTE = PL_BJEDTE
        TradeContext.BJETIM=AfaUtilTools.GetSysTime( )
        #TradeContext.TRCDAT = PL_BJEDTE


        #=====================系统公共校验======================================
        if not rccpsFunc.ChkPubInfo(PL_BRSFLG_RCV) :
            raise AfaFlowControl.flowException( )

        #=====================系统状态校验======================================
        #if not rccpsFunc.ChkSysInfo( 'RCCPS' ) :
        if not rccpsFunc.ChkSysInfo( 'AFA' ) :
            raise AfaFlowControl.flowException(  )

        #=====================机构合法性校验====================================
        if not rccpsFunc.ChkUnitInfo( PL_BRSFLG_RCV ) :
            raise AfaFlowControl.flowException( )

        #=====================获取中心日期====================================
        if not rccpsFunc.GetNCCDate( ) :
            raise AfaFlowControl.flowException( )

        #=====================获取平台流水号====================================
        if rccpsGetFunc.GetSerialno(PL_BRSFLG_RCV) == -1 :
            raise AfaFlowControl.flowException( )


        #=====================获取中心流水号====================================
        if rccpsGetFunc.GetRccSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )
        
        
        #=====================动态加载交易脚本==================================
        trxModuleName = 'T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode
        try:
            trxModuleHandle=__import__( trxModuleName )

        except Exception, e:
            AfaLoggerFunc.tradeInfo(e)
            raise AfaFlowControl.flowException( 'A0001', '加载交易脚本失败或交易脚本不存在,执行交易失败' )


        #=====================交易前处理(登记流水,主机前处理)===================
        if not trxModuleHandle.SubModuleDoFst( ) :
            raise AfaFlowControl.flowException( )


        #=====================与主机通讯========================================
        rccpsHostFunc.CommHost(TradeContext.HostCode)

        #=====================交易中处理(修改流水,主机后处理,中心前处理)========
        if not trxModuleHandle.SubModuleDoSnd( ) :
            raise AfaFlowControl.flowException( )


        #=====================与中心通讯(回执)==================================
        AfaAfeFunc.CommAfe()


        #=====================交易后处理========================================
        if not trxModuleHandle.SubModuleDoTrd():
            raise AfaFlowControl.flowException( )


        #=====================自动打包==========================================
        AfaFunc.autoPackData()


        #=====================退出模板==========================================
        AfaLoggerFunc.tradeInfo('***农信银系统: 来账.主机类操作模板['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']退出***')


    except AfaFlowControl.flowException, e:
        #流程异常
        
        if not AfaDBFunc.RollbackSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeError(">>>Rollback异常")
        AfaLoggerFunc.tradeInfo(">>>Rollback成功")
        
        AfaFlowControl.exitMainFlow( str(e) )

    except AfaFlowControl.accException:
        #账务异常
        
        if not AfaDBFunc.RollbackSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeError(">>>Rollback异常")
        AfaLoggerFunc.tradeInfo(">>>Rollback成功")
        
        AfaFlowControl.exitMainFlow( )
            
    except Exception, e:
        #默认异常
        
        if not AfaDBFunc.RollbackSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeError(">>>Rollback异常")
        AfaLoggerFunc.tradeInfo(">>>Rollback成功")
        
        AfaFlowControl.exitMainFlow( str(e) )
