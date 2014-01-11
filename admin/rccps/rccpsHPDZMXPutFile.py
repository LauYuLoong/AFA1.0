# -*- coding: gbk -*-
###############################################################################
#   农信银系统：系统调度类.农信银汇票错账文件生成及发送到主机
#==============================================================================
#   交易文件:   rccpsHPDZMXPutFile.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-06-28
###############################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsFtpFunc,rccpsDBFunc,rccpsState,rccpsHostFunc,rccpsUtilTools
import rccpsDBTrcc_mbrifa,rccpsDBTrcc_hpdzmx

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.农信银汇票错账文件生成及发送到主机[rccpsHPDZMXPutFile]进入***")
        
        #==========获取中心日期================================================
        AfaLoggerFunc.tradeInfo(">>>开始获取前中心工作日期")
        
        mbrifa_where_dict = {}
        mbrifa_where_dict['OPRTYPNO'] = "20"
        
        mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
        
        if mbrifa_dict == None:
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","查询当前中心日期异常")
            
        NCCWKDAT = mbrifa_dict['NOTE1'][:8]                           #对账日期
        LNCCWKDAT = "('" + mbrifa_dict['NOTE4'].replace(",","','") + "')"
        
        AfaLoggerFunc.tradeInfo(">>>结束获取前中心工作日期")
        
        #================根据汇票对账明细登记簿,生成汇票主机对账文件===========
        AfaLoggerFunc.tradeInfo(">>>开始生成汇票主机对账文件")
        
        hpdzmx_where_sql = "NCCWKDAT in " + LNCCWKDAT
        
        hpdzmx_list = rccpsDBTrcc_hpdzmx.selectm(1,0,hpdzmx_where_sql,"")
        
        if hpdzmx_list == None:
            rccpsCronFunc.cronExit("S999","查询汇票对账明细登记簿异常")
            
        file_path = os.environ['AFAP_HOME'] + "/data/rccps/host/RCCPSHPDZMX" + NCCWKDAT
        
        fp = open(file_path,"w")
        
        if fp == None:
            rccpsCronFunc.cronExit("S999","打开汇票对账(主机)明细文件异常")
            
        file_line = ""
        
        if len(hpdzmx_list) <= 0:
            AfaLoggerFunc.tradeInfo(">>>汇票对账明细登记簿中无对应记录")
        else:
            for i in xrange(len(hpdzmx_list)):
                
                file_line = file_line + "RCC".ljust(8,' ')                     + '|' #代理业务号
                file_line = file_line + hpdzmx_list[i]['BJEDTE'].ljust(8,' ')  + '|' #前置日期
                file_line = file_line + hpdzmx_list[i]['BSPSQN'].ljust(12,' ') + '|' #前置流水号
                
                trc_dict = {}
                if not rccpsDBFunc.getTransBil(hpdzmx_list[i]['BJEDTE'],hpdzmx_list[i]['BSPSQN'],trc_dict):
                    rccpsCronFunc.cronExit("S999","查询汇票业务信息异常")
                    
                if not rccpsDBFunc.getInfoBil(trc_dict['BILVER'],trc_dict['BILNO'],trc_dict['BILRS'],trc_dict):
                    rccpsCronFunc.cronExit("S999","查询汇票详细信息异常")
                
                file_line = file_line + hpdzmx_list[i]['SNDBNKCO'].ljust(12,' ') + '|' #发起行号
                file_line = file_line + hpdzmx_list[i]['SNDBNKNM'].ljust(62,' ') + '|' #发起行名
                file_line = file_line + trc_dict['BRSFLG'].ljust(1,' ')        + '|' #往来标识
                file_line = file_line + "".ljust(5,' ')                        + '|' #业务类型
                
                
                #=======根据往来标识去借贷方信息===============================
                if trc_dict['BRSFLG'] == PL_BRSFLG_SND:
                    #===往账查询记账/短款成功状态信息中的借贷方账号信息========
                    
                    if trc_dict['TRCCO'] == '2100101':
                        tmpBCSTAT = PL_BCSTAT_HCAC
                        tmpstr = '抹账'
                    else:
                        tmpBCSTAT = PL_BCSTAT_ACC
                        tmpstr = '记账'
                        
                    stat_dict = {}
                    if not rccpsState.getTransStateSet(hpdzmx_list[i]['BJEDTE'],hpdzmx_list[i]['BSPSQN'],tmpBCSTAT,PL_BDWFLG_SUCC,stat_dict):
                        AfaLoggerFunc.tradeInfo("流水状态登记簿中无" + tmpstr + "状态,开始查询短款状态")
                        if not rccpsState.getTransStateSet(hpdzmx_list[i]['BJEDTE'],hpdzmx_list[i]['BSPSQN'],PL_BCSTAT_SHORT,PL_BDWFLG_SUCC,stat_dict):
                            rccpsCronFunc.cronExit("S999","查询短款状态异常")
                        
                    file_line = file_line + stat_dict['SBAC'].ljust(32,' ')    + '|' #借方账号
                    file_line = file_line + stat_dict['ACNM'].ljust(62,' ')    + '|' #借方户名
                    file_line = file_line + "".ljust(62,' ')                   + '|' #借方地址
                    file_line = file_line + hpdzmx_list[i]['RCVBNKCO'].ljust(12,' ') + '|' #接收行号
                    file_line = file_line + hpdzmx_list[i]['RCVBNKNM'].ljust(62,' ') + '|' #接收行名
                    file_line = file_line + stat_dict['RBAC'].ljust(32,' ')    + '|' #贷方账号
                    file_line = file_line + stat_dict['OTNM'].ljust(62,' ')    + '|' #贷方户名
                    file_line = file_line + "".ljust(62,' ')                   + '|' #贷方地址
                else:
                    #===来账直接取登记簿查询函数查询出的借贷方账号信息=========
                    file_line = file_line + trc_dict['SBAC'].ljust(32,' ')     + '|' #借方账号
                    file_line = file_line + trc_dict['ACNM'].ljust(62,' ')     + '|' #借方户名
                    file_line = file_line + "".ljust(62,' ')                   + '|' #借方地址
                    file_line = file_line + hpdzmx_list[i]['RCVBNKCO'].ljust(12,' ') + '|' #接收行号
                    file_line = file_line + hpdzmx_list[i]['RCVBNKNM'].ljust(62,' ') + '|' #接收行名
                    file_line = file_line + trc_dict['RBAC'].ljust(32,' ')     + '|' #贷方账号
                    file_line = file_line + trc_dict['OTNM'].ljust(62,' ')     + '|' #贷方户名
                    file_line = file_line + "".ljust(62,' ')                   + '|' #贷方地址
                    
                if hpdzmx_list[i]['TRCCO'] == '2100100':
                    file_line = file_line + str(hpdzmx_list[i]['OCCAMT'])      + '|' #交易金额(解付业务,交易金额取实际结算金额)
                elif hpdzmx_list[i]['TRCCO'] == '2100101' and trc_dict['BBSSRC'] != '3':
                    file_line = file_line + "-" + str(hpdzmx_list[i]['BILAMT'])+ '|' #交易金额(撤销业务且资金来源非待销账,交易金额取负出票金额)
                else:
                    file_line = file_line + str(hpdzmx_list[i]['BILAMT'])      + '|' #交易金额(非撤销和解付业务,交易金额取出票金额)
                    
                file_line = file_line + "".ljust(1,' ')                        + '|' #记录状态
                if hpdzmx_list[i]['TRCCO'] == '2100100':
                    file_line = file_line + "1".ljust(62,' ')                  + '|' #备用字段1(解付业务,需要结转,赋1)
                else:
                    file_line = file_line + "0".ljust(62,' ')                  + '|' #备用字段1(非解付业务,不需要结转,赋0)
                file_line = file_line + "".ljust(62,' ')                       + '|' #备用字段2
                file_line = file_line + "".ljust(62,' ')                       + '|' #备用字段3
                file_line = file_line + "".ljust(62,' ')                       + '|' #备用字段4
                file_line = file_line + "\n"
                
        fp.write(file_line)
        
        fp.close()
        
        #====================转换主机对账文件编码==============================
        sFileName = "RCCPSHPDZMX" + NCCWKDAT
        dFileName = "RCCPSFILE.HP"  + NCCWKDAT
        
        if not rccpsCronFunc.FormatFile("1","rccps01.fld",sFileName,dFileName):
            rccpsCronFunc.cronExit("S999","转换主机对账文件编码异常")
            
        AfaLoggerFunc.tradeInfo(">>>结束生成汇票主机对账文件")
        
        #================FTP文件到主机=========================================
        AfaLoggerFunc.tradeInfo(">>>开始FTP文件到主机")
        if not rccpsFtpFunc.putHost(dFileName):
            rccpsCronFunc.cronExit("S999","FTP文件到主机异常")
            
        AfaLoggerFunc.tradeInfo(">>>结束FTP文件到主机")
        
        #================开始注册主机对账======================================
        AfaLoggerFunc.tradeInfo(">>>开始注册主机对账")
        
        #================获取总笔数和总金额====================================
        AfaLoggerFunc.tradeInfo(">>>开始获取总笔数和总金额")
        
        #汇票解付业务,金额取实际结算金额
        sql = "select count(*),sum(OCCAMT) from rcc_hpdzmx where NCCWKDAT in " + LNCCWKDAT
        sql = sql + " and TRCCO in ('2100100') "
        
        records1 = AfaDBFunc.SelectSql(sql)
        
        if records1 == None:
            rccpsCronFunc.cronExit("S999","获取总笔数和总金额异常")
            
        else:
            AfaLoggerFunc.tradeInfo("count:[" + str(records1[0][0]) + "],sum:[" + str(records1[0][1]) + "]")
            rec_count1 = 0
            rec_sum1   = 0.00
            
            if records1[0][0] > 0:
                rec_count1 = records1[0][0]
                rec_sum1   = records1[0][1]
        
        #非汇票解付业务,金额取出票金额
        sql = "select count(*),sum(BILAMT) from rcc_hpdzmx where NCCWKDAT in " + LNCCWKDAT
        sql = sql + " and TRCCO not in ('2100100') "
        
        records2 = AfaDBFunc.SelectSql(sql)
        
        if records2 == None:
            rccpsCronFunc.cronExit("S999","获取总笔数和总金额异常")
            
        else:
            AfaLoggerFunc.tradeInfo("count:[" + str(records2[0][0]) + "],sum:[" + str(records2[0][1]) + "]")
            rec_count2 = 0
            rec_sum2   = 0.00
            
            if records2[0][0] > 0:
                rec_count2 = records2[0][0]
                rec_sum2   = records2[0][1]
                
        rec_count = rec_count1 + rec_count2
        rec_sum   = rec_sum1   + rec_sum2
            
        AfaLoggerFunc.tradeInfo("对账登记簿中中心日期" + LNCCWKDAT + "交易笔数[" + str(rec_count) + "]交易金额[" + str(rec_sum) + "]")
        
        AfaLoggerFunc.tradeInfo(">>>结束获取总笔数和总金额")
        
        TradeContext.HostCode = '8826'
        TradeContext.BESBNO   = PL_BESBNO_BCLRSB
        TradeContext.BETELR   = PL_BETELR_AUTO
        TradeContext.NBBH     = 'RCC'
        TradeContext.COUT     = rec_count
        TradeContext.TOAM     = rec_sum
        TradeContext.FINA     = 'HP' + NCCWKDAT
        
        #================发起注册主机对账======================================
        rccpsHostFunc.CommHost( TradeContext.HostCode )
        
        AfaLoggerFunc.tradeInfo("errorCode = [" + TradeContext.errorCode + "]")
        AfaLoggerFunc.tradeInfo("errorMsg  = [" + TradeContext.errorMsg + "]")
        
        #================判断注册主机对账返回信息==============================
        
        if TradeContext.errorCode != '0000':
            rccpsCronFunc.cronExit("S999","注册主机对账异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束注册主机对账")
        
        #================关闭汇票对账错账文件生成及发送到主机系统调度==========
        AfaLoggerFunc.tradeInfo(">>>开始关闭汇票对账错账文件生成及发送到主机系统调度")
        if not rccpsCronFunc.closeCron("00045"):
            rccpsCronFunc.cronExit("S999","关闭汇票对账错账文件生成及发送到主机调度异常")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit异常")
        AfaLoggerFunc.tradeInfo(">>>Commit成功")
        
        AfaLoggerFunc.tradeInfo(">>>结束关闭汇票对账错账文件生成及发送到主机系统调度")
        
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.农信银汇票错账文件生成及发送到主机[rccpsHPDZMXPutFile]退出***")
    
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
            AfaLoggerFunc.tradeInfo('***[rccpsHPDZMXPutFile]交易中断***')

        sys.exit(-1)
