# -*- coding: gbk -*-
################################################################################
#   农信银系统：系统调度类.通存通兑主机对账文件下载
#===============================================================================
#   交易文件:   rccpsTDZJDZGetFile.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-11-27
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsHostFunc,rccpsFtpFunc
import rccpsDBTrcc_mbrifa

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.通存通兑主机对账文件下载[rccpsTDZJDZGetFile]进入***")
        
        #==========获取中心日期================================================
        AfaLoggerFunc.tradeInfo(">>>开始获取前中心工作日期")
        
        mbrifa_where_dict = {}
        mbrifa_where_dict['OPRTYPNO'] = "30"
        
        mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
        
        if mbrifa_dict == None:
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","查询当前中心日期异常")
            
        NCCWKDAT  = mbrifa_dict['NOTE1'][:8]                  #对账日期
        NCCWKDAT_LIST = mbrifa_dict['NOTE3'].split(',')       #需要对账的中心日期(包括本清算工作日和之前的非清算工作日)
        
        
        
        AfaLoggerFunc.tradeInfo(">>>开始注册主机对账文件生成")
        
        #==========主机交易前处理==============================================
        TradeContext.HostCode = '8825'                        #交易代码
        TradeContext.STRDAT = min( NCCWKDAT_LIST )            #起始日期
        TradeContext.ENDDAT = max( NCCWKDAT_LIST )            #终止日期
        TradeContext.BESBNO = PL_BESBNO_BCLRSB                #机构号码
        TradeContext.BETELR = PL_BETELR_AUTO                  #自动柜员
            
        AfaLoggerFunc.tradeInfo("起始日期 = [" + TradeContext.STRDAT + "]")
        AfaLoggerFunc.tradeInfo("终止日期 = [" + TradeContext.ENDDAT + "]")
        #================发起注册主机对账文件生成==========================
        rccpsHostFunc.CommHost( TradeContext.HostCode )
        
        AfaLoggerFunc.tradeInfo("errorCode = [" + TradeContext.errorCode + "]")
        AfaLoggerFunc.tradeInfo("errorMsg  = [" + TradeContext.errorMsg  + "]")
        
        #================判断注册主机对账返回信息==============================
        
        if TradeContext.errorCode != '0000':
            rccpsCronFunc.cronExit("S999","注册主机对账文件生成异常")
        else:
            AfaLoggerFunc.tradeInfo("注册主机对账文件生成成功")
 
        AfaLoggerFunc.tradeInfo(">>>结束注册主机对账文件生成")
        
        #================下载主机对帐文件======================================
        AfaLoggerFunc.tradeInfo(">>>开始下载主机对账文件")
        #==========文件名===============
        host_path = 'BANKMDS'                                   #主机路径
        file_path = 'NXSCA'           #本地路径
        
        if( not rccpsFtpFunc.getHost(file_path,host_path)):
            rccpsCronFunc.cronExit('A099', '下载主机对账文件异常')
        AfaLoggerFunc.tradeInfo(">>>结束下载主机对账文件")
        
        #================主机对帐文件转码======================================
        AfaLoggerFunc.tradeInfo(">>>开始转码主机对账文件")
        dFileName = 'rccpsdz' + NCCWKDAT
        sFileName = 'NXSCA'
        fldName = 'nxsca.fld'
        if( not rccpsCronFunc.FormatFile('0', fldName, sFileName, dFileName)):
            rccpsCronFunc.cronExit('A099', '转换主机对账文件编码异常')
        AfaLoggerFunc.tradeInfo(">>>结束转码主机对账文件")
        
        #================关闭通存通兑主机对账明细账下载系统调度,打开通存通兑主机对账文件导入系统调度==
        AfaLoggerFunc.tradeInfo(">>>开始关闭通存通兑主机对账明细账下载系统调度,打开通存通兑主机对账文件导入系统调度")
        if not rccpsCronFunc.closeCron("00068"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","关闭通存通兑对账明细账下载系统调度异常")
            
        if not rccpsCronFunc.openCron("00069"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","打开通存通兑对账文件导入系统调度异常")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit异常")
        AfaLoggerFunc.tradeInfo(">>>Commit成功")
        
        AfaLoggerFunc.tradeInfo(">>>结束关闭通存通兑主机对账明细账下载系统调度,打开通存通兑主机对账文件导入系统调度")
        
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.通存通兑对账明细账勾兑[rccpsTDDZMXCompare]退出***")
    
    except Exception, e:
        #所有异常

        if not AfaDBFunc.RollbackSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeInfo(">>>Rollback异常")
        AfaLoggerFunc.tradeInfo(">>>Rollback成功")

        if( not TradeContext.existVariable( "errorCode" ) or str(e) ):
            TradeContext.errorCode = 'A9999'
            TradeContext.errorMsg = '系统错误['+ str(e) +']'

        if TradeContext.errorCode != '0000' :
            AfaLoggerFunc.tradeInfo( 'errorCode=['+TradeContext.errorCode+']' )
            AfaLoggerFunc.tradeInfo( 'errorMsg=['+TradeContext.errorMsg+']' )
            AfaLoggerFunc.tradeInfo('***[rccpsTDZJDZGetFile]交易中断***')

        sys.exit(-1)
