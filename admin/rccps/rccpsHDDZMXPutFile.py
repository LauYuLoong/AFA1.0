# -*- coding: gbk -*-
################################################################################
#   农信银系统：系统调度类.农信银汇兑错账文件生成及发送到主机
#===============================================================================
#   交易文件:   rccpsHDDZMXPutFile.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-06-28
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsFtpFunc,rccpsDBFunc,rccpsState,rccpsHostFunc
import rccpsDBTrcc_mbrifa,rccpsDBTrcc_hddzmx

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.农信银汇兑错账文件生成及发送到主机[rccpsHDDZMXPutFile]进入***")
        
        #==========获取中心日期================================================
        AfaLoggerFunc.tradeInfo(">>>开始获取前中心工作日期")
        
        mbrifa_where_dict = {}
        mbrifa_where_dict['OPRTYPNO'] = "20"
        
        mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
        
        if mbrifa_dict == None:
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","查询当前中心日期异常")
            
        NCCWKDAT = mbrifa_dict['NOTE1'][:8]                           #对账日期
        LNCCWKDAT = "('" + mbrifa_dict['NOTE3'].replace(",","','") + "')"
        
        AfaLoggerFunc.tradeInfo(">>>结束获取前中心工作日期")
        
        #================根据汇兑对账明细登记簿,生成汇兑主机对账文件============
        AfaLoggerFunc.tradeInfo(">>>开始生成汇兑主机对账文件")
        
        hddzmx_where_sql = "NCCWKDAT in " + LNCCWKDAT
        
        hddzmx_list = rccpsDBTrcc_hddzmx.selectm(1,0,hddzmx_where_sql,"")
        
        if hddzmx_list == None:
            rccpsCronFunc.cronExit("S999","查询汇兑对账明细登记簿异常")
            
        file_path = os.environ['AFAP_HOME'] + "/data/rccps/host/RCCPSHDDZMX" + NCCWKDAT
        
        fp = open(file_path,"wb")
        
        if fp == None:
            rccpsCronFunc.cronExit("S999","打开汇兑对账(主机)明细文件异常")
            
        file_line = ""
        
        if len(hddzmx_list) <= 0:
            AfaLoggerFunc.tradeInfo(">>>汇兑对账明细登记簿中无对应记录")
        else:
            for i in xrange(len(hddzmx_list)):
                
                file_line = file_line + "RCC".ljust(8,' ')                     + '|' #代理业务号
                file_line = file_line + hddzmx_list[i]['BJEDTE'].ljust(8,' ')  + '|' #前置日期
                file_line = file_line + hddzmx_list[i]['BSPSQN'].ljust(12,' ') + '|' #前置流水号
                
                trc_dict = {}
                if not rccpsDBFunc.getTransTrc(hddzmx_list[i]['BJEDTE'],hddzmx_list[i]['BSPSQN'],trc_dict):
                    rccpsCronFunc.cronExit("S999","查询交易信息异常")
                
                file_line = file_line + hddzmx_list[i]['SNDBNKCO'].ljust(12,' ') + '|'     #发起行号
                file_line = file_line + hddzmx_list[i]['SNDBNKNM'].ljust(62,' ') + '|'     #发起行名
                file_line = file_line + trc_dict['BRSFLG'].ljust(1,' ')    + '|'     #往来标识
                file_line = file_line + "".ljust(5,' ')                    + '|'     #业务类型
                
                
                #=======根据往来标识获取借贷方信息================================
                if trc_dict['BRSFLG'] == PL_BRSFLG_SND:
                    #===往账查询记账状态信息中的借贷方账号信息==================
                    stat_dict = {}
                    if not rccpsState.getTransStateSet(hddzmx_list[i]['BJEDTE'],hddzmx_list[i]['BSPSQN'],PL_BCSTAT_ACC,PL_BDWFLG_SUCC,stat_dict):
                        rccosCronFunc.cronExit("S999","查询记账状态异常")
                        
                    file_line = file_line + stat_dict['SBAC'].ljust(32,' ')    + '|' #借方账号
                    file_line = file_line + stat_dict['ACNM'].ljust(62,' ')    + '|' #借方户名
                    file_line = file_line + "".ljust(62,' ')                   + '|' #借方地址
                    file_line = file_line + hddzmx_list[i]['RCVBNKCO'].ljust(12,' ') + '|' #接收行号
                    file_line = file_line + hddzmx_list[i]['RCVBNKNM'].ljust(62,' ') + '|' #接收行名
                    file_line = file_line + stat_dict['RBAC'].ljust(32,' ')    + '|' #贷方账号
                    file_line = file_line + stat_dict['OTNM'].ljust(62,' ')    + '|' #贷方户名
                    file_line = file_line + "".ljust(62,' ')                   + '|' #贷方地址
                else:
                    #===来账查询自动入账/自动挂账状态信息中的借贷方账号信息==========
                    stat_dict = {}
                    if not rccpsState.getTransStateSet(hddzmx_list[i]['BJEDTE'],hddzmx_list[i]['BSPSQN'],PL_BCSTAT_AUTO,PL_BDWFLG_SUCC,stat_dict):
                        AfaLoggerFunc.tradeInfo("流水状态登记簿中无自动入账状态,查询自动挂账状态")
                        if not rccpsState.getTransStateSet(hddzmx_list[i]['BJEDTE'],hddzmx_list[i]['BSPSQN'],PL_BCSTAT_HANG,PL_BDWFLG_SUCC,stat_dict):
                            rccpsCronFunc.cronExit("S999","查询自动挂账状态异常")
                            
                    file_line = file_line + stat_dict['SBAC'].ljust(32,' ')    + '|' #借方账号
                    file_line = file_line + stat_dict['ACNM'].ljust(62,' ')    + '|' #借方户名
                    file_line = file_line + "".ljust(62,' ')                   + '|' #借方地址
                    file_line = file_line + hddzmx_list[i]['RCVBNKCO'].ljust(12,' ') + '|' #接收行号
                    file_line = file_line + hddzmx_list[i]['RCVBNKNM'].ljust(62,' ') + '|' #接收行名
                    file_line = file_line + stat_dict['RBAC'].ljust(32,' ')    + '|' #贷方账号
                    file_line = file_line + stat_dict['OTNM'].ljust(62,' ')    + '|' #贷方户名
                    file_line = file_line + "".ljust(62,' ')                   + '|' #贷方地址
                    
                file_line = file_line + str(hddzmx_list[i]['OCCAMT'])      + '|'     #交易金额
                file_line = file_line + "".ljust(1,' ')                    + '|'     #记录状态
                file_line = file_line + "1".ljust(62,' ')                  + '|'     #备用字段1(需要结转,赋1)
                file_line = file_line + "".ljust(62,' ')                   + '|'     #备用字段2
                file_line = file_line + "".ljust(62,' ')                   + '|'     #备用字段3
                file_line = file_line + "".ljust(62,' ')                   + '|'     #备用字段4
                file_line = file_line + "\n"
                
        fp.write(file_line)
        
        fp.close()
        
        #================转换主机对账文件编码==================================
        sFileName = "RCCPSHDDZMX" + NCCWKDAT
        dFileName = "RCCPSFILE.HD"  + NCCWKDAT
        
        if not rccpsCronFunc.FormatFile("1","rccps01.fld",sFileName,dFileName):
            rccpsCronFunc.cronExit("S999","转换主机对账文件编码异常")
            
        AfaLoggerFunc.tradeInfo(">>>结束生成汇兑主机对账文件")
        
        #================FTP文件到主机=========================================
        AfaLoggerFunc.tradeInfo(">>>开始FTP文件到主机")
        if not rccpsFtpFunc.putHost(dFileName):
            rccpsCronFunc.cronExit("S999","FTP文件到主机异常")
            
        AfaLoggerFunc.tradeInfo(">>>结束FTP文件到主机")
        
        #================开始注册主机对账======================================
        AfaLoggerFunc.tradeInfo(">>>开始注册主机对账")
        
        #================获取总笔数和总金额====================================
        AfaLoggerFunc.tradeInfo(">>>开始获取总笔数和总金额")
        
        sql = "select count(*),sum(OCCAMT) from rcc_hddzmx where NCCWKDAT in " + LNCCWKDAT
        
        records = AfaDBFunc.SelectSql(sql)
        
        if records == None:
            rccpsCronFunc.cronExit("S999","获取总笔数和总金额异常")
            
        else:
            rec_count = records[0][0]
            rec_sum   = records[0][1]
            
            if rec_count <= 0:
                rec_count = 0
                rec_sum   = 0.00
            
        AfaLoggerFunc.tradeInfo("对账登记簿中中心日期" + LNCCWKDAT + "交易笔数[" + str(rec_count) + "]交易金额[" + str(rec_sum) + "]")
        
        AfaLoggerFunc.tradeInfo(">>>结束获取总笔数和总金额")
        
        TradeContext.HostCode = '8826'
        TradeContext.BESBNO   = PL_BESBNO_BCLRSB
        TradeContext.BETELR   = PL_BETELR_AUTO
        TradeContext.NBBH     = 'RCC'
        TradeContext.COUT     = rec_count
        TradeContext.TOAM     = rec_sum
        TradeContext.FINA     = 'HD' + NCCWKDAT
        
        #================发起注册主机对账======================================
        rccpsHostFunc.CommHost( TradeContext.HostCode )
        
        AfaLoggerFunc.tradeInfo("errorCode = [" + TradeContext.errorCode + "]")
        AfaLoggerFunc.tradeInfo("errorMsg  = [" + TradeContext.errorMsg + "]")
        
        #================判断注册主机对账返回信息==============================
        
        if TradeContext.errorCode != '0000':
            rccpsCronFunc.cronExit("S999","注册主机对账异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束注册主机对账")
        
        #================关闭汇兑对账错账文件生成及发送到主机系统调度==========
        AfaLoggerFunc.tradeInfo(">>>开始关闭汇兑对账错账文件生成及发送到主机系统调度")
        if not rccpsCronFunc.closeCron("00035"):
            rccpsCronFunc.cronExit("S999","关闭汇兑对账错账文件生成及发送到主机调度异常")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit异常")
        AfaLoggerFunc.tradeInfo(">>>Commit成功")
        
        AfaLoggerFunc.tradeInfo(">>>结束关闭汇兑对账错账文件生成及发送到主机系统调度")
        
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.农信银汇兑错账文件生成及发送到主机[rccpsHDDZMXPutFile]退出***")
    
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
            AfaLoggerFunc.tradeInfo('***[rccpsHDDZMXPutFile]交易中断***')

        sys.exit(-1)
