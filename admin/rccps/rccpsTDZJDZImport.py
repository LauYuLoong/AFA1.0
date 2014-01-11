# -*- coding: gbk -*-
################################################################################
#   农信银系统：系统调度类.通存通兑主机对账明细文件导入
#===============================================================================
#   交易文件:   rccpsTDZJDZImport.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-11-27
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc
import rccpsDBTrcc_tdzjmx,rccpsDBTrcc_mbrifa

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.通存通兑主机对账明细文件导入[rccpsTDZJDZImport]进入***")
        
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
        
        #==========删除记账明细簿数据=================================================
        AfaLoggerFunc.tradeInfo(">>>删除记账明细簿数据")
        delsql = "delete from rcc_tdzjmx"
        res = AfaDBFunc.DeleteSqlCmt(delsql)
        if(  res==None or res == -1 ):
            AfaLoggerFunc.tradeDebug(">>>记账明细簿插入数据失败,数据库会滚,抛弃报文")
            AfaDBFunc.RollbackSql()
            rccpsCronFunc.cronExit( '9000', '记账明细簿插入数据失败,数据库会滚,抛弃报文' )  
        else:
            AfaDBFunc.CommitSql()
        
        #==========记账明细簿导入数据=================================================
        AfaLoggerFunc.tradeInfo(">>>记账明细簿导入数据")
        file_name = 'rccpsdz' + NCCWKDAT
        file_path = os.environ['AFAP_HOME'] + "/data/rccps/host/"
        rb = open(file_path + file_name , 'r')
        #读取一行
        lineBuf = rb.readline()
        iLine=0
        while ( len(lineBuf) > 20 ):
            iLine=iLine+1
            sItemBuf = lineBuf.split('|')         
            
            if ( len(sItemBuf) < 16 ):
                rb.close()
                rccpsCronFunc.cronExit( '9000', '数据文件格式错误(' + file_name + ')' )   
                
            tdzjmx_dict = {}
            tdzjmx_dict['NCCWKDAT'] = sItemBuf[2].strip()
            tdzjmx_dict['SCNBBH'] = sItemBuf[1].strip()
            tdzjmx_dict['SCFEDT'] = sItemBuf[3].strip()
            tdzjmx_dict['SCRBSQ'] = sItemBuf[4].strip()
            tdzjmx_dict['SCEYDT'] = sItemBuf[5].strip()
            tdzjmx_dict['SCTLSQ'] = sItemBuf[6].strip()
            tdzjmx_dict['SCRVSB'] = sItemBuf[7].strip()
            tdzjmx_dict['SCCATR'] = sItemBuf[8].strip()
            tdzjmx_dict['SCWLBZ'] = sItemBuf[9].strip()
            tdzjmx_dict['SCTRAM'] = sItemBuf[10].strip()
            if(tdzjmx_dict['SCTRAM'][0] == '-'):
               tdzjmx_dict['SCTRAM'] = tdzjmx_dict['SCTRAM'][1:]
            tdzjmx_dict['SCFLAG'] = sItemBuf[11].strip()
            tdzjmx_dict['SCSTCD'] = sItemBuf[12].strip()
            tdzjmx_dict['SCBYZ1'] = sItemBuf[13].strip()
            tdzjmx_dict['SCBYZ2'] = sItemBuf[14].strip()
            tdzjmx_dict['SCBYZ3'] = sItemBuf[15].strip()
            
            #如果(SCRVSB)冲账标志等于"1"(8820 冲账)，多录入一笔
            if(tdzjmx_dict['SCRVSB'] == '1'):
                tdzjmxcp_dict = {}
                tdzjmxcp_dict = tdzjmx_dict.copy()
                tdzjmxcp_dict['SCRVSB'] = ''
                tdzjmxcp_dict['SCSTCD'] = '1'
                records = rccpsDBTrcc_tdzjmx.insertCmt(tdzjmxcp_dict)      
                if( records == -1):
                    AfaLoggerFunc.tradeDebug(">>>记账明细簿插入数据失败,数据库会滚,抛弃报文")
                    AfaDBFunc.RollbackSql()
                    rccpsCronFunc.cronExit( '9000', '记账明细簿插入数据失败,数据库会滚,抛弃报文' )  
                else:
                    AfaDBFunc.CommitSql()
            
            res = rccpsDBTrcc_tdzjmx.insertCmt(tdzjmx_dict)      
            if( res == -1):
                AfaLoggerFunc.tradeDebug(">>>记账明细簿插入数据失败,数据库会滚,抛弃报文")
                AfaDBFunc.RollbackSql()
                rccpsCronFunc.cronExit( '9000', '记账明细簿插入数据失败,数据库会滚,抛弃报文' )  
            else:
                AfaDBFunc.CommitSql()

            lineBuf = rb.readline()
        
        rb.close()
        
        #================关闭通存通兑主机对账明细账文件导入系统调度,打开通存通兑主机对账勾兑系统调度==
        AfaLoggerFunc.tradeInfo(">>>开始关闭通存通兑主机对账明细账文件导入系统调度,打开通存通兑主机对账勾兑系统调度")
        if not rccpsCronFunc.closeCron("00069"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","关闭通存通兑对账明细账文件导入系统调度异常")
            
        if not rccpsCronFunc.openCron("00070"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","打开通存通兑对账勾兑系统调度异常")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit异常")
        AfaLoggerFunc.tradeInfo(">>>Commit成功")
        
        AfaLoggerFunc.tradeInfo(">>>结束关闭通存通兑主机对账明细账文件导入系统调度,打开通存通兑主机对账勾兑系统调度")
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.通存通兑主机对账明细文件导入[rccpsTDZJDZImport]退出***")
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
            AfaLoggerFunc.tradeInfo('***[rccpsTDZJDZImport]交易中断***')

        sys.exit(-1)