# -*- coding: gbk -*-
################################################################################
#   农信银系统：系统调度类.汇票对账汇总文件导入
#===============================================================================
#   交易文件:   rccpsHPDZHZFileImport.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-06-25
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsDBFunc,rccpsUtilTools
import rccpsDBTrcc_mbrifa,rccpsDBTrcc_hpdzhz


if __name__ == '__main__':
    try:
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.汇票对账汇总文件导入[rccpsHPDZHZFileImport]进入***")
        
        local_home = os.environ['AFAP_HOME'] + "/data/rccps/"
        
        #==========获取中心日期================================================
        AfaLoggerFunc.tradeInfo(">>>开始获取前中心工作日期")
        
        mbrifa_where_dict = {}
        mbrifa_where_dict['OPRTYPNO'] = "20"
        
        mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
        
        if mbrifa_dict == None:
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","查询当前中心日期异常")
            
        NCCWKDAT = mbrifa_dict['NOTE1'][:8]                           #对账日期
        
        AfaLoggerFunc.tradeInfo(">>>结束获取前中心工作日期")
        
        #====================导入汇票对账汇总文件===================================
        AfaLoggerFunc.tradeInfo(">>>开始导入汇票对账汇总文件")
        
        file_path = local_home + "settlefile/HPHZCNY1340000008" + NCCWKDAT
        
        fp = open(file_path,"r")
        
        if fp == None:
            rccpsCronFunc.cronExit("S999","打开汇票对账汇总文件异常")
            
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
            
            hpdzhz_insert_dict = {}
            
            hpdzhz_insert_dict['NCCWKDAT'] = NCCWKDAT
            hpdzhz_insert_dict['TRCCO']    = line_list[0][:7]
            hpdzhz_insert_dict['TRCNAM']   = line_list[1][:8]
            hpdzhz_insert_dict['TRCRSNM']  = line_list[2][:8]
            hpdzhz_insert_dict['TCNT']     = line_list[3][:10]
            hpdzhz_insert_dict['CTAMT']    = line_list[4][:18]
            hpdzhz_insert_dict['DTAMT']    = line_list[5][:18]
            hpdzhz_insert_dict['OFSTAMT']  = line_list[6][:18]
            hpdzhz_insert_dict['CLAMT']    = line_list[7][:18]
            hpdzhz_insert_dict['DLAMT']    = line_list[8][:18]
            hpdzhz_insert_dict['OFSLAMT']  = line_list[9][:18]
            hpdzhz_insert_dict['NOTE1']    = NCCWKDAT          #对账日期
            
            if hpdzhz_insert_dict['TRCRSNM'][:4] == "往账":
                hpdzhz_insert_dict['BRSFLG'] = PL_BRSFLG_SND
            elif hpdzhz_insert_dict['TRCRSNM'][:4] == "来账":
                hpdzhz_insert_dict['BRSFLG'] = PL_BRSFLG_RCV
            else:
                hpdzhz_insert_dict['BRSFLG'] = '9'
            
            ret = rccpsDBTrcc_hpdzhz.insert(hpdzhz_insert_dict)
            
            if ret <= 0:
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                rccpsCronFunc.cronExit("S999","导入汇票对账汇总文件异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束导入汇票对账汇总文件")
        
        #====================关闭汇票对账汇总文件导入系统调度,打开汇票对账明细账勾兑====
        AfaLoggerFunc.tradeInfo(">>>开始关闭汇票对账汇总文件导入系统调度,打开汇票对账明细账勾兑")
        if not rccpsCronFunc.closeCron("00042"):
            rccpsCronFunc.cronExit("S999","关闭汇票对账文件导入系统调度异常")
            
        if not rccpsCronFunc.openCron("00043"):
            rccpsCronFunc.cronExit("S999","打开汇票对账汇总文件导入系统调度异常")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit异常")
        AfaLoggerFunc.tradeInfo(">>>Commit成功")
        
        AfaLoggerFunc.tradeInfo(">>>结束关闭汇票对账明细文件导入系统调度,打开汇票对账汇总文件导入系统调度")
        
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.汇票对账汇总文件导入[rccpsHPDZHZFileImport]退出***")   
        
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
            AfaLoggerFunc.tradeInfo('***[rccpsHPDZHZFileImport]交易中断***')

        sys.exit(-1)
