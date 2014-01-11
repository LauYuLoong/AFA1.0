# -*- coding: gbk -*-
################################################################################
#   农信银系统：系统调度类.行号生效处理
#===============================================================================
#   交易文件:   rccpsHHEffict.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-09-15
################################################################################
import TradeContext
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys,AfaHostFunc
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsState,rccpsDBFunc,rccpsHostFunc,rccpsUtilTools
import rccpsDBTrcc_paybnk

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit("usage: rccpsHHImport.py filename")
        
    try:
        local_file_home = os.environ['AFAP_HOME'] + "/data/rccps/"
        file_path = "filein/" + sys.argv[1]
        
        AfaLoggerFunc.tradeInfo(">>>开始更新行名行号表农信银资金清算系统行名行号")
        
        pfile = open(local_file_home + file_path,"rb")
        file_line = " "
        
        while file_line:
            file_line = AfaUtilTools.trim(pfile.readline())   
            file_line = rccpsUtilTools.replaceRet(file_line)
            
            if file_line == "":
                continue
                
            line_list = file_line.split('|')
            
            paybnk_where_dict = {}
            paybnk_where_dict['BANKBIN'] = line_list[0]
            tmp_paybnk_dict = rccpsDBTrcc_paybnk.selectu(paybnk_where_dict)
            if tmp_paybnk_dict == None:
                if not AfaDBFunc.RollbackSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    AfaLoggerFunc.tradeError(">>>Rollback异常")
                AfaLoggerFunc.tradeInfo(">>>Rollback成功")
                rccpsCronFunc.cronExit("S999","查询将登记行号是否存在异常")
            
            paybnk_dict = {}
            paybnk_dict['BANKBIN']      = line_list[0][:10]
            paybnk_dict['BANKSTATUS']   = line_list[1][:1]
            paybnk_dict['BANKATTR']     = line_list[2][:2]
            paybnk_dict['STLBANKBIN']   = line_list[3][:10]
            paybnk_dict['BANKNAM']      = line_list[4][:60]
            paybnk_dict['BANKADDR']     = line_list[5][:60]
            paybnk_dict['BANKPC']       = line_list[6][:6]
            paybnk_dict['BANKTEL']      = line_list[7][:30]
            paybnk_dict['EFCTDAT']      = line_list[8][:8]
            paybnk_dict['INVDAT']       = line_list[9][:8]
            paybnk_dict['ALTTYPE']      = line_list[10][:1]
            paybnk_dict['PRIVILEGE']    = line_list[11][:20]
            paybnk_dict['STRINFO']      = line_list[12][:60]
            
            if len(tmp_paybnk_dict) <= 0:
                #=====行名行号表中不存在此行号,插入新行号=======================
                ret = rccpsDBTrcc_paybnk.insert(paybnk_dict)
                AfaLoggerFunc.tradeInfo("插入新行号")
                if ret <= 0:
                    if not AfaDBFunc.RollbackSql( ):
                        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        AfaLoggerFunc.tradeError(">>>Rollback异常")
                    AfaLoggerFunc.tradeInfo(">>>Rollback成功")
                    rccpsCronFunc.cronExit("S999","插入新行号异常")
                    
            #else:
            #    #=====行名行号表中存在此行号,更新行号信息=======================
            #    ret = rccpsDBTrcc_paybnk.update(paybnk_dict,paybnk_where_dict)
            #    AfaLoggerFunc.tradeInfo("更新旧行号")
            #    if ret <= 0:
            #        if not AfaDBFunc.RollbackSql( ):
            #            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            #            AfaLoggerFunc.tradeError(">>>Rollback异常")
            #        AfaLoggerFunc.tradeInfo(">>>Rollback成功")
            #        rccpsCronFunc.cronExit("S999","更新旧行号异常")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit异常")
        AfaLoggerFunc.tradeInfo(">>>Commit成功")
        
        AfaLoggerFunc.tradeInfo(">>>结束更新行名行号表农信银资金清算系统行名行号")
        
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
            AfaLoggerFunc.tradeInfo("***[rccpsHHEffict]交易中断***")

        sys.exit(-1)