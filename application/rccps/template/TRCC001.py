# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.本地类操作模板(1.本地操作)
#===============================================================================
#   模板文件:   TRCC001.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘雨龙
#   修改时间:   2008-06-02
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
import rccpsFunc
from types import *
from rccpsConst import *

def main( ):

    AfaLoggerFunc.tradeInfo('***农信银系统: 往账.本地类操作模板['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']进入***')
    try:
        #=====================初始化返回报文变量================================
        TradeContext.tradeResponse=[]

        #=====================获取系统日期时间==================================
        #TradeContext.BJEDTE=AfaUtilTools.GetHostDate( )
        TradeContext.BJETIM=AfaUtilTools.GetSysTime( )
        #TradeContext.BESBNO = '3400008889'

        #=====================系统公共校验======================================
        if not rccpsFunc.ChkPubInfo(PL_BRSFLG_SND) :
            raise AfaFlowControl.flowException( )

        #=====================系统状态校验======================================
        if not rccpsFunc.ChkSysInfo( 'AFA' ) :
            raise AfaFlowControl.flowException( )

        #=====================机构合法性校验====================================
        #if not rccpsFunc.ChkUnitInfo( ) :
        #    raise AfaFlowControl.flowException( )

        #=====================动态加载交易脚本==================================
        trxModuleName = 'T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode
        try:
            trxModuleHandle=__import__( trxModuleName )

        except Exception, e:
            AfaLoggerFunc.tradeInfo(e)
            raise AfaFlowControl.flowException( 'A0001', '加载交易脚本失败或交易脚本不存在,执行交易失败' )

        #=====================个性化处理(本地操作)==============================
        AfaLoggerFunc.tradeInfo( 'TransCode:' + TradeContext.TransCode )
        if not trxModuleHandle.SubModuleDoFst( ) :
            raise AfaFlowControl.flowException( )

        #=====================自动打包==========================================
        AfaFunc.autoPackData()

        #=====================退出模板==========================================
        AfaLoggerFunc.tradeInfo('***农信银系统: 往账.本地类操作模板['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']退出***')


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
