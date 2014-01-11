# -*- coding: gbk -*-
################################################################################
#   农信银系统：系统调度类.通存通兑对账明细文件导入
#===============================================================================
#   交易文件:   rccpsTDDZMXFileImport.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-11-20
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsDBFunc,rccpsUtilTools
import rccpsDBTrcc_mbrifa,rccpsDBTrcc_tddzmx

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.通存通兑对账明细文件导入[rccpsTDDZMXFileImport]进入***")
        
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
        
        #====================导入通存通兑对账明细文件===================================
        AfaLoggerFunc.tradeInfo(">>>开始导入通存通兑对账明细文件")
        
        file_path = local_home + "settlefile/TDMXCNY1340000008" + NCCWKDAT
        
        fp = open(file_path,"r")
        
        if fp == None:
            rccpsCronFunc.cronExit("S999","打开通存通兑对账明细文件异常")
            
        file_line = " "
        
        #关彬捷 20081028 修改需要对账的日期获取方式
        #初始化本次对账需要对账的中心日期
        NCCWKDAT_LIST = []
        NCCWKDAT_LIST.append(NCCWKDAT)
        
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
            
            #若此条记录的中心日期不在需要对账的中心日期列表中,则追加
            if not NCCWKDAT_LIST.__contains__(line_list[0][:8]):
                NCCWKDAT_LIST.append(line_list[0][:8])
            
            tddzmx_insert_dict = {}
            
            tddzmx_insert_dict['NCCWKDAT'] = line_list[0][:8]
            tddzmx_insert_dict['TRCCO']    = line_list[1][:7]
            tddzmx_insert_dict['MSGTYPCO'] = line_list[2][:6]
            tddzmx_insert_dict['RCVMBRCO'] = line_list[3][:10]
            tddzmx_insert_dict['SNDMBRCO'] = line_list[4][:10]
            tddzmx_insert_dict['SNDBRHCO'] = line_list[5][:6]
            tddzmx_insert_dict['SNDCLKNO'] = line_list[6][:8]
            tddzmx_insert_dict['SNDTRDAT'] = line_list[7][:8]
            tddzmx_insert_dict['SNDTRTIM'] = line_list[8][:6]
            tddzmx_insert_dict['MSGFLGNO'] = line_list[9][:26]
            tddzmx_insert_dict['ORMFN']    = line_list[10][:26]
            tddzmx_insert_dict['OPRTYPNO'] = line_list[11][:2]
            tddzmx_insert_dict['ROPRTPNO'] = line_list[12][:2]
            tddzmx_insert_dict['SNDBNKCO'] = line_list[13][:10]
            tddzmx_insert_dict['SNDBNKNM'] = line_list[14][:60]
            tddzmx_insert_dict['RCVBNKCO'] = line_list[15][:10]
            tddzmx_insert_dict['RCVBNKNM'] = line_list[16][:60]
            tddzmx_insert_dict['TRCDAT']   = line_list[17][:8]
            tddzmx_insert_dict['TRCNO']    = line_list[18][:8]
            tddzmx_insert_dict['CUR']      = line_list[19][:3]
            tddzmx_insert_dict['OCCAMT']   = line_list[20][:18]
            tddzmx_insert_dict['CUSCHRG']  = line_list[21][:18]
            tddzmx_insert_dict['PYRMBRCO'] = line_list[22][:10]
            tddzmx_insert_dict['PYRACC']   = line_list[23][:32]
            tddzmx_insert_dict['PYEMBRCO'] = line_list[24][:10]
            tddzmx_insert_dict['PYEACC']   = line_list[25][:32]
            tddzmx_insert_dict['ORTRCCO']  = line_list[26][:7]
            tddzmx_insert_dict['ORTRCNO']  = line_list[27][:8]
            tddzmx_insert_dict['DCFLG']    = line_list[28][:1]
            tddzmx_insert_dict['CBFLG']    = line_list[29][:1]
            tddzmx_insert_dict['CONFFLG']  = line_list[30][:1]
            tddzmx_insert_dict['CANCFLG']  = line_list[31][:1]
            tddzmx_insert_dict['STRINFO']  = line_list[32][:60]
            tddzmx_insert_dict['NOTE1']    = NCCWKDAT            #将对账日期赋值到对账明细表NOTE1字段
            
            #通存通兑对账文件中存款确认和冲销交易不导入对账明细表中
            if tddzmx_insert_dict['TRCCO'] == '3000503' or tddzmx_insert_dict['TRCCO'] == '3000504':
                continue
            
            wtr_dict = {}
            if not rccpsDBFunc.getTransWtrAK(tddzmx_insert_dict['SNDBNKCO'],tddzmx_insert_dict['TRCDAT'],tddzmx_insert_dict['TRCNO'],wtr_dict):
                if AfaDBFunc.sqlErrMsg != "":
                    AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                    rccpsCronFunc.cronExit("S999","查询对账明细行内信息异常")
                else:
                    tddzmx_insert_dict['BJEDTE'] = ""
                    tddzmx_insert_dict['BSPSQN'] = ""
                
            else:
                tddzmx_insert_dict['BJEDTE'] = wtr_dict['BJEDTE']
                tddzmx_insert_dict['BSPSQN'] = wtr_dict['BSPSQN']
            
            ret = rccpsDBTrcc_tddzmx.insert(tddzmx_insert_dict)
            
            if ret <= 0:
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                rccpsCronFunc.cronExit("S999","导入对账明细文件异常")
        
        fp.close()
        AfaLoggerFunc.tradeInfo(">>>结束导入通存通兑对账明细文件")
        
        #更新通存通兑业务需要对账的日期
        AfaLoggerFunc.tradeInfo(">>>开始更新系统状态表中NOTE3字段(通存通兑业务需要对账的日期)")
        
        #关彬捷 20081028 修改需要对账的日期获取方式 删除原方式
        #rec = AfaDBFunc.SelectSql("select distinct(nccwkdat) from rcc_tddzmx where NOTE1 = '" + NCCWKDAT + "'")
        
        #if ret == None:
        #    rccpsCronFunc.cronExit("S999","查询对账明细表中通存通兑业务需要对账的日期异常")
            
        #if len(rec) <= 0:
        #    rccpsCronFunc.cronExit("S999","查询对账明细表中通存通兑业务需要对账的日期异常")
        
        LNCCWKDAT = str(NCCWKDAT_LIST).replace('[','').replace(']','').replace('(','').replace(',)','').replace('\'','')
        LNCCWKDAT = AfaUtilTools.trim(LNCCWKDAT)
        
        AfaLoggerFunc.tradeInfo("NOTE3=[" + LNCCWKDAT + "]")
        
        rec = AfaDBFunc.UpdateSqlCmt("update rcc_mbrifa set note3 = '" + LNCCWKDAT + "' " + " where oprtypno = '30' ")
        
        if rec <= 0:
            rccpsCronFunc.cronExit("S999","更新业务状态表中NOTE3字段异常")
            
        AfaLoggerFunc.tradeInfo(">>>结束更新系统状态表中NOTE3字段(通存通兑业务需要对账的日期)")

        
        #====================关闭通存通兑对账明细文件导入系统调度,打开通存通兑对账汇总文件导入和通存通兑业务量统计系统调度====
        AfaLoggerFunc.tradeInfo(">>>开始关闭通存通兑对账明细文件导入系统调度,打开通存通兑对账汇总文件导入系统调度")
        if not rccpsCronFunc.closeCron("00064"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","关闭通存通兑对账明细文件导入系统调度异常")
            
        if not rccpsCronFunc.openCron("00062"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","打开通存通兑对账汇总文件导入系统调度异常")
            
#        if not rccpsCronFunc.openCron("00066"):
#            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
#            rccpsCronFunc.cronExit("S999","打开通存通兑业务量统计系统调度异常")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit异常")
        AfaLoggerFunc.tradeInfo(">>>Commit成功")
        
        AfaLoggerFunc.tradeInfo(">>>结束关闭通存通兑对账明细文件导入系统调度,打开通存通兑对账汇总文件导入系统调度")
        
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.通存通兑对账明细文件导入[rccpsTDDZMXFileImport]退出***")      
        
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
            AfaLoggerFunc.tradeInfo('***[rccpsTDDZMXFileImport]交易中断***')

        sys.exit(-1)
