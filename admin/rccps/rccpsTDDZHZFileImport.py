# -*- coding: gbk -*-
################################################################################
#   农信银系统：系统调度类.通存通兑对账汇总文件导入
#===============================================================================
#   交易文件:   rccpsTDDZHZFileImport.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-11-20
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsUtilTools
import rccpsDBTrcc_mbrifa,rccpsDBTrcc_tddzhz

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.通存通兑对账汇总文件导入[rccpsTDDZHZFileImport]进入***")
        
        local_home = os.environ['AFAP_HOME'] + "/data/rccps/"
        
        #==========获取中心日期================================================
        AfaLoggerFunc.tradeInfo(">>>开始获取前中心工作日期")
        
        mbrifa_where_dict = {}
        mbrifa_where_dict['OPRTYPNO'] = "30"
        
        mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
        
        if mbrifa_dict == None:
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","查询当前中心日期异常")
            
        NCCWKDAT = mbrifa_dict['NOTE1'][:8]                           #对账日期
        
        AfaLoggerFunc.tradeInfo(">>>结束获取前中心工作日期")
        
        #====================导入通存通兑对账汇总文件===================================
        AfaLoggerFunc.tradeInfo(">>>开始导入通存通兑对账汇总文件")
        
        file_path = local_home + "settlefile/TDHZCNY1340000008" + NCCWKDAT
        
        fp = open(file_path,"r")
        
        if fp == None:
            rccpsCronFunc.cronExit("S999","打开通存通兑对账汇总文件异常")
            
        file_line = " "
        
        while file_line:
            
            file_line = fp.readline()
            
            #关彬捷 20081028 增加格式化对账文件
            file_line = AfaUtilTools.trim(file_line)
            #张恒 20091125 增加删除对账文件中非法字符
            file_line = AfaUtilTools.trimchn(file_line)
            file_line = rccpsUtilTools.replaceRet(file_line)
            
            if file_line == "":
                continue
                
            line_list = file_line.split('|')
            
            tddzhz_insert_dict = {}
            
            tddzhz_insert_dict['NCCWKDAT'] = NCCWKDAT
            tddzhz_insert_dict['TRCCO']    = line_list[0][:7]
            tddzhz_insert_dict['TRCNAM']   = line_list[1][:12]
            tddzhz_insert_dict['TRCRSNM']  = line_list[2][:8]
            tddzhz_insert_dict['TCNT']     = line_list[3][:10]
            tddzhz_insert_dict['CTAMT']    = line_list[4][:18]
            tddzhz_insert_dict['DTAMT']    = line_list[5][:18]
            tddzhz_insert_dict['CHRCTAMT'] = line_list[6][:18]
            tddzhz_insert_dict['CHRDTAMT'] = line_list[7][:18]
            tddzhz_insert_dict['OFSTAMT']  = line_list[8][:18]
            tddzhz_insert_dict['NOTE1']    = NCCWKDAT          #对账日期
            
            if tddzhz_insert_dict['TRCRSNM'][:4] == "受理":
                tddzhz_insert_dict['BRSFLG'] = PL_BRSFLG_SND
            elif tddzhz_insert_dict['TRCRSNM'][:4] == "开户":
                tddzhz_insert_dict['BRSFLG'] = PL_BRSFLG_RCV
            elif tddzhz_insert_dict['TRCRSNM'][:4] == "轧差":
                tddzhz_insert_dict['BRSFLG'] = '2'
            elif tddzhz_insert_dict['TRCRSNM'][:4] == "调账":
                tddzhz_insert_dict['BRSFLG'] = '3'
            else:
                tddzhz_insert_dict['BRSFLG'] = '9'
            
            ret = rccpsDBTrcc_tddzhz.insert(tddzhz_insert_dict)
            
            if ret <= 0:
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                rccpsCronFunc.cronExit("S999","导入通存通兑对账汇总文件异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束导入通存通兑对账汇总文件")
        
        #====================关闭通存通兑对账汇总文件导入系统调度====
        AfaLoggerFunc.tradeInfo(">>>开始关闭通存通兑对账汇总文件导入系统调度,打开通存通兑主机对账明细文件下载系统调度")
        if not rccpsCronFunc.closeCron("00062"):
            rccpsCronFunc.cronExit("S999","关闭通存通兑对账汇总文件导入系统调度异常")
            
        if not rccpsCronFunc.openCron("00068"):
            rccpsCronFunc.cronExit("S999","打开通存通兑主机对账明细文件下载系统调度异常")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit异常")
        AfaLoggerFunc.tradeInfo(">>>Commit成功")
        
        AfaLoggerFunc.tradeInfo(">>>结束关闭通存通兑对账明细文件导入系统调度,打开通存通兑主机对账明细文件下载系统调度")
        
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.通存通兑对账汇总文件导入[rccpsTDDZHZFileImport]退出***")
        
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
            AfaLoggerFunc.tradeInfo('***[rccpsTDDZHZFileImport]交易中断***')

        sys.exit(-1)
