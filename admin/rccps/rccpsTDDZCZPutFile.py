# -*- coding: gbk -*-
################################################################################
#   农信银系统：系统调度类.农信银通存通兑错账文件生成及发送到差错处理平台
#===============================================================================
#   交易文件:   rccpsTDDZCZPutFile.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-12-10
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsFtpFunc,rccpsDBFunc,rccpsState,rccpsHostFunc,rccpsUtilTools
import rccpsDBTrcc_mbrifa,rccpsDBTrcc_tddzmx,rccpsDBTrcc_tddzcz

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.农信银通存通兑错账文件生成及发送到差错处理平台[rccpsTDDZCZPutFile]进入***")
        
        #==========获取中心日期================================================
        AfaLoggerFunc.tradeInfo(">>>开始获取前中心工作日期")
        
        mbrifa_where_dict = {}
        mbrifa_where_dict['OPRTYPNO'] = "30"
        
        mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
        
        if mbrifa_dict == None:
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","查询当前中心日期异常")
            
        NCCWKDAT = mbrifa_dict['NOTE1'][:8]                           #对账日期
        LNCCWKDAT = "('" + mbrifa_dict['NOTE3'].replace(",","','") + "')"
        
        AfaLoggerFunc.tradeInfo(">>>结束获取前中心工作日期")
        
        #================根据通存通兑对账明细登记簿,生成通存通兑差错处理文件============
        AfaLoggerFunc.tradeInfo(">>>开始生成通存通兑差错处理文件")
        
        tddzcz_where_sql = "NCCWKDAT in " + LNCCWKDAT
        
        tddzcz_list = rccpsDBTrcc_tddzcz.selectm(1,0,tddzcz_where_sql,"")
        
        if tddzcz_list == None:
            rccpsCronFunc.cronExit("S999","查询通存通兑对账错账登记簿异常")
            
        file_path = os.environ['AFAP_HOME'] + "/data/rccps/errorfile/EXPREQ" + NCCWKDAT + '01.BIN'
        
        fp = open(file_path,"wb")
        
        if fp == None:
            rccpsCronFunc.cronExit("S999","打开通存通兑对账差错明细文件异常")
            
        file_line = ""
        
        if len(tddzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo(">>>通存通兑对账明细登记簿中无对应记录")
        else:
            for i in xrange(len(tddzcz_list)):
                
                file_line = file_line + tddzcz_list[i]['SNDMBRCO'].ljust(10,' ')   + '|'
                file_line = file_line + tddzcz_list[i]['RCVMBRCO'].ljust(10,' ')   + '|'
                file_line = file_line + tddzcz_list[i]['TRCCO'].ljust(7,' ')       + '|'
                file_line = file_line + tddzcz_list[i]['DCFLG'].ljust(1,' ')       + '|'
                file_line = file_line + tddzcz_list[i]['TRCNO'].ljust(8,' ')       + '|'
                file_line = file_line + tddzcz_list[i]['TRCDAT'].ljust(8,' ')      + '|'
                file_line = file_line + tddzcz_list[i]['NCCWKDAT'].ljust(8,' ')    + '|'
                file_line = file_line + tddzcz_list[i]['PYRACC'].ljust(32,' ')     + '|'
                file_line = file_line + tddzcz_list[i]['PYEACC'].ljust(32,' ')     + '|'
                file_line = file_line + tddzcz_list[i]['CUR'].ljust(3,' ')         + '|'
                file_line = file_line + rccpsUtilTools.FormatMoney(str(tddzcz_list[i]['OCCAMT'])).ljust(15,' ')     + '|'
                file_line = file_line + rccpsUtilTools.FormatMoney(str(tddzcz_list[i]['LOCOCCAMT'])).ljust(15,' ')  + '|'
                file_line = file_line + rccpsUtilTools.FormatMoney(str(tddzcz_list[i]['CUSCHRG'])).ljust(15,' ')    + '|'
                file_line = file_line + rccpsUtilTools.FormatMoney(str(tddzcz_list[i]['LOCCUSCHRG'])).ljust(15,' ') + '|'
                file_line = file_line + tddzcz_list[i]['ORTRCNO'].ljust(8,' ')     + '|'
                file_line = file_line + tddzcz_list[i]['EACTYP'].ljust(2,' ')      + '|'
                file_line = file_line + tddzcz_list[i]['SNDBNKCO'].ljust(10,' ')   + '|'
                file_line = file_line + tddzcz_list[i]['RCVBNKCO'].ljust(10,' ')   + '|'
                file_line = file_line + "\n"
                
        fp.write(file_line)
        
        fp.close()
        
        AfaLoggerFunc.tradeInfo(">>>结束生成通存通兑差错处理文件")
        
        #关彬捷  20081216  屏蔽ftp到差错处理平台相关处理
        ##================FTP文件到主机=========================================
        #dFileName = "RCCPSTDDZCZ"  + NCCWKDAT
        #
        #AfaLoggerFunc.tradeInfo(">>>开始FTP文件到差错处理平台")
        #if not rccpsFtpFunc.putERRSYS(dFileName):
        #    rccpsCronFunc.cronExit("S999","FTP文件到差错处理平台异常")
        #    
        #AfaLoggerFunc.tradeInfo(">>>结束FTP文件到差错处理平台")
        
        #================关闭通存通兑对账错账文件生成及发送到差错处理平台系统调度==========
        AfaLoggerFunc.tradeInfo(">>>开始关闭通存通兑对账错账文件生成及发送到差错处理平台系统调度")
        if not rccpsCronFunc.closeCron("00060"):
            rccpsCronFunc.cronExit("S999","关闭通存通兑对账错账文件生成及发送到差错处理平台调度异常")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit异常")
        AfaLoggerFunc.tradeInfo(">>>Commit成功")
        
        AfaLoggerFunc.tradeInfo(">>>结束关闭通存通兑对账错账文件生成及发送到差错处理平台系统调度")
        
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.农信银通存通兑错账文件生成及发送到差错处理平台[rccpsTDDZCZPutFile]退出***")
    
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
            AfaLoggerFunc.tradeInfo('***[rccpsTDDZCZPutFile]交易中断***')

        sys.exit(-1)
