# -*- coding: gbk -*-
################################################################################
#   农信银系统：来账.中心类操作(1.本地操作 2.中心回执).公共数据通知报文接收
#===============================================================================
#   模板文件:   TRCC006_1122.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-06-18
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsFtpFunc,rccpsUtilTools
import rccpsDBTrcc_pbdata,rccpsDBTrcc_paybnk,rccpsDBTrcc_cadbnk
import rccpsMap0000Dout_context2CTradeContext,rccpsMap1122CTradeContext2Dpbdata


#=====================交易前处理(登记流水,中心前处理)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***来账.中心类操作(1.本地操作).公共数据通知报文接收[TRCC006_1122]进入***' )
    
    #=================判断是否重复报文==========================================
    AfaLoggerFunc.tradeInfo(">>>开始判断是否重复报文")
    
    pbdata_where_dict = {}
    pbdata_where_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
    pbdata_where_dict['TRCDAT']   = TradeContext.TRCDAT
    pbdata_where_dict['TRCNO']    = TradeContext.TRCNO
    
    pbdata_dict = rccpsDBTrcc_pbdata.selectu(pbdata_where_dict)
    
    if pbdata_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","判断是否重复报文,查询公共数据登记簿相同报文异常")
        
    if len(pbdata_dict) > 0:
        AfaLoggerFunc.tradeInfo("公共数据登记簿中存在相同数据,重复报文,进入下一流程")
        #======为通讯回执报文赋值===================================================
        out_context_dict = {}
        out_context_dict['sysType']  = 'rccpst'
        out_context_dict['TRCCO']    = '9900503'
        out_context_dict['MSGTYPCO'] = 'SET008'
        out_context_dict['RCVMBRCO'] = TradeContext.SNDMBRCO
        out_context_dict['SNDMBRCO'] = TradeContext.RCVMBRCO
        out_context_dict['SNDBRHCO'] = TradeContext.BESBNO
        out_context_dict['SNDCLKNO'] = TradeContext.BETELR
        out_context_dict['SNDTRDAT'] = TradeContext.BJEDTE
        out_context_dict['SNDTRTIM'] = TradeContext.BJETIM
        out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
        out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
        out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
        out_context_dict['OPRTYPNO'] = '99'
        out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
        out_context_dict['TRANTYP']  = '0'
        out_context_dict['ORTRCCO']  = TradeContext.TRCCO
        out_context_dict['PRCCO']    = 'RCCI0000'
        out_context_dict['STRINFO']  = '过期报文'
        
        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        return True
    
    AfaLoggerFunc.tradeInfo(">>>结束判断是否重复报文")
    
    #=================下载公共数据文件==========================================
    AfaLoggerFunc.tradeInfo(">>>开始下载公共数据文件")
    
    rccps_path_list = TradeContext.PBDAFILE.split('/')
    
    file_path = AfaUtilTools.trim(rccps_path_list[len(rccps_path_list)-2] + "/" + rccps_path_list[len(rccps_path_list)-1])
    
    if not rccpsFtpFunc.getRccps(file_path):
        return AfaFlowControl.ExitThisFlow("S999","下载公共数据文件" + file_path + "异常")
    
    AfaLoggerFunc.tradeInfo(">>>结束下载公共数据文件")
    
    #=================登记公共数据通知登记簿====================================
    AfaLoggerFunc.tradeInfo(">>>开始登记公共数据通知登记簿")
    
    pbdata_insert_dict = {}
    if not rccpsMap1122CTradeContext2Dpbdata.map(pbdata_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999","为公共数据通知登记簿赋值异常")
    
    ret = rccpsDBTrcc_pbdata.insert(pbdata_insert_dict)
    
    if ret <= 0:
        if not AfaDBFunc.RollbackSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeError(">>>Rollback异常")
        AfaLoggerFunc.tradeInfo(">>>Rollback成功")
        return AfaFlowControl.ExitThisFlow("S999","登记公共数据通知登记簿异常")
    
    AfaLoggerFunc.tradeInfo(">>>结束登记公共数据通知登记簿")
    
    #=================处理接收到的数据==========================================
    AfaLoggerFunc.tradeInfo(">>>开始处理接收到的数据")
    
    local_file_home = os.environ['AFAP_HOME'] + "/data/rccps/"
    #AfaLoggerFunc.tradeInfo(local_file_home + file_path)
    
    #=================农信银资金清算系统行名行号================================
    if TradeContext.PBDATYP == '001':
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
                return AfaFlowControl.ExitThisFlow("S999","查询将登记行号是否存在异常")
            
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
                    return AfaFlowControl.ExitThisFlow("S999","插入新行号异常")
                    
            else:
                #=====行名行号表中存在此行号,更新行号信息=======================
                ret = rccpsDBTrcc_paybnk.update(paybnk_dict,paybnk_where_dict)
                AfaLoggerFunc.tradeInfo("更新旧行号")
                if ret <= 0:
                    if not AfaDBFunc.RollbackSql( ):
                        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        AfaLoggerFunc.tradeError(">>>Rollback异常")
                    AfaLoggerFunc.tradeInfo(">>>Rollback成功")
                    return AfaFlowControl.ExitThisFlow("S999","更新旧行号异常")
            
        
        AfaLoggerFunc.tradeInfo(">>>结束更新行名行号表农信银资金清算系统行名行号")
        
    #=================特约汇兑系统行名行号======================================
    elif TradeContext.PBDATYP == '011':
        AfaLoggerFunc.tradeInfo(">>>开始更新行名行号表特约汇兑系统行名行号")
        
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
                return AfaFlowControl.ExitThisFlow("S999","查询将登记行号是否存在异常")
            
            paybnk_dict = {}
            paybnk_dict['BANKBIN']      = line_list[0][:10]
            paybnk_dict['BANKNAM']      = line_list[1][:60]
            paybnk_dict['BANKADDR']     = line_list[2][:60]
            paybnk_dict['BANKPC']       = line_list[3][:6]
            paybnk_dict['BANKTEL']      = line_list[4][:30]
            paybnk_dict['EFCTDAT']      = line_list[5][:8]
            paybnk_dict['INVDAT']       = line_list[6][:8]
            paybnk_dict['ALTTYPE']      = line_list[7][:1]
            paybnk_dict['NEWOFLG']      = line_list[8][:1]
            paybnk_dict['STRINFO']      = line_list[9][:60]
            
            if len(tmp_paybnk_dict) <= 0:
                #=====行名行号表中不存在此行号,插入新行号=========
                ret = rccpsDBTrcc_paybnk.insert(paybnk_dict)
                if ret <= 0:
                    if not AfaDBFunc.RollbackSql( ):
                        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        AfaLoggerFunc.tradeError(">>>Rollback异常")
                    AfaLoggerFunc.tradeInfo(">>>Rollback成功")
                    return AfaFlowControl.ExitThisFlow("S999","插入新行号异常")
                    
            else:
                #=====行名行号表中存在此行号,更新行号信息=========
                ret = rccpsDBTrcc_paybnk.update(paybnk_dict,paybnk_where_dict)
                if ret <= 0:
                    if not AfaDBFunc.RollbackSql( ):
                        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        AfaLoggerFunc.tradeError(">>>Rollback异常")
                    AfaLoggerFunc.tradeInfo(">>>Rollback成功")
                    return AfaFlowControl.ExitThisFlow("S999","插入新行号异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束更新行名行号表特约汇兑系统行名行号")
        
    #=================中心下发通知==============================================
    elif TradeContext.PBDATYP == '002':
        AfaLoggerFunc.tradeInfo(">>>开始处理中心下发通知")
        
        AfaLoggerFunc.tradeInfo(">>>中心下发通知文件,不做处理")
        
        AfaLoggerFunc.tradeInfo(">>>结束处理中心下发通知")
        
    #=================存款利息清单==============================================
    elif TradeContext.PBDATYP == '003':
        AfaLoggerFunc.tradeInfo(">>>开始处理存款利息清单")
        
        #=============为存款利息清单文件加抬头==================================
        file = ""
        file = file + "\n"
        file = file + "                    上存农信银资金清算中心存款利息单                    " + "\n"
        file = file + "\n"
        file = file + "\n"
        file = file + "    成员行号：1340000008  成员行名：安徽省联社清算中心    " + "\n"
        file = file + "\n"
        file = file + "".ljust(145,"-")
        file = file + "\n"
        file = file + "账号".ljust(18," ")     + "|"
        file = file + "户名".ljust(60," ")     + "|"
        file = file + "积数".ljust(20," ")     + "|"
        file = file + "利率".ljust(10," ")     + "|"
        file = file + "起息日".ljust(8," ")    + "|"
        file = file + "结息日".ljust(8," ")    + "|"
        file = file + "利息金额".ljust(14," ") + "\n"
        file = file + "".ljust(145,"-")
        file = file + "\n"
        
        pfile = open(local_file_home + file_path,"rb")
        file = file + pfile.read()
        
        pfile.close
        
        file = file + "".ljust(145,"-")
        file = file + "\n"
        file = file + "\n"
        file = file + "\n"
        file = file + "打印日期:                记账:                 复核:                " + "\n"
        
        pfile = open(local_file_home + file_path,"wb")
        pfile.write(file)
        
        pfile.close()
        
        AfaLoggerFunc.tradeInfo(">>>结束处理存款利息清单")
        
    #=================透支利息清单==============================================
    elif TradeContext.PBDATYP == '004':
        AfaLoggerFunc.tradeInfo(">>>开始处理存款利息清单")
        
        #=============为透支利息清单文件加抬头==================================
        file = ""
        file = file + "\n"
        file = file + "                    上存农信银资金清算中心存款透支利息单                    " + "\n"
        file = file + "\n"
        file = file + "\n"
        file = file + "    成员行号：1340000008  成员行名：安徽省联社清算中心    " + "\n"
        file = file + "\n"
        file = file + "".ljust(145,"-")
        file = file + "\n"
        file = file + "账号".ljust(18," ")     + "|"
        file = file + "户名".ljust(60," ")     + "|"
        file = file + "透支积数".ljust(20," ") + "|"
        file = file + "透支利率".ljust(10," ") + "|"
        file = file + "起息日".ljust(8," ")    + "|"
        file = file + "结息日".ljust(8," ")    + "|"
        file = file + "利息金额".ljust(14," ") + "\n"
        file = file + "".ljust(145,"-")
        file = file + "\n"
        
        pfile = open(local_file_home + file_path,"rb")
        file = file + pfile.read()
        
        pfile.close
        
        file = file + "".ljust(145,"-")
        file = file + "\n"
        file = file + "\n"
        file = file + "\n"
        file = file + "打印日期:                记账:                 复核:                " + "\n"
        
        pfile = open(local_file_home + file_path,"wb")
        pfile.write(file)
        
        pfile.close()
        
        AfaLoggerFunc.tradeInfo(">>>结束处理存款利息清单")
        
    #=================手续费扣收清单============================================
    elif TradeContext.PBDATYP == '005':
        AfaLoggerFunc.tradeInfo(">>>开始登记手续费扣收清单")
        
        #=============为手续费扣收清单文件加抬头==================================
        file = ""
        file = file + "\n"
        file = file + "                    农信银资金清算中心业务手续费扣划单                    " + "\n"
        file = file + "\n"
        file = file + "\n"
        file = file + "    成员行号：1340000008  成员行名：安徽省联社清算中心    " + "\n"
        file = file + "\n"
        file = file + "".ljust(268,"-")
        file = file + "\n"
        file = file + "账号".ljust(18," ")              + "|"
        file = file + "户名".ljust(60," ")              + "|"
        file = file + "起始日期".ljust(8," ")           + "|"
        file = file + "终止日期".ljust(8," ")           + "|"
        file = file + "计费总金额".ljust(15," ")        + "|"
        file = file + "折扣率".ljust(11," ")             + "|"
        file = file + "扣费总金额".ljust(15," ")        + "|"
        file = file + "汇兑累计笔数".ljust(10," ")      + "|"
        file = file + "汇兑手续费/笔".ljust(13," ")     + "|"
        file = file + "汇兑计费金额".ljust(16," ")      + "|"
        file = file + "汇票累计笔数".ljust(10," ")      + "|"
        file = file + "汇票手续费/笔".ljust(13," ")     + "|"
        file = file + "汇票计费金额".ljust(16, " ")     + "|"
        file = file + "通存通兑累计笔数".ljust(10," ")  + "|"
        file = file + "通存通兑手续费/笔".ljust(13," ") + "|"
        file = file + "通存通兑计费金额".ljust(16," ")  + "\n"
        file = file + "".ljust(268,"-")
        file = file + "\n"
        
        pfile = open(local_file_home + file_path,"rb")
        file = file + pfile.read()
        
        pfile.close
        
        file = file + "".ljust(268,"-")
        file = file + "\n"
        file = file + "\n"
        file = file + "\n"
        file = file + "打印日期:                记账:                 复核:                " + "\n"
        
        pfile = open(local_file_home + file_path,"wb")
        pfile.write(file)
        
        pfile.close()
        
        AfaLoggerFunc.tradeInfo(">>>结束登记手续费扣收清单")
        
    #=================卡BIN与行号对照===========================================
    elif TradeContext.PBDATYP == '006':
        AfaLoggerFunc.tradeInfo(">>>开始更新卡BIN与行号对照表")
        
        pfile = open(local_file_home + file_path,"r")
        file_line = " "
        
        while file_line:
            file_line = AfaUtilTools.trim(pfile.readline())
            file_line = rccpsUtilTools.replaceRet(file_line)
            #AfaLoggerFunc.tradeInfo("file_line = [" + file_line + "]")
            
            if file_line == "":
                continue
                
            line_list = file_line.split('|')
            
            cadbnk_where_dict = {}
            cadbnk_where_dict['CARDBIN'] = line_list[0][:12]
            
            tmp_cadbnk_dict = rccpsDBTrcc_cadbnk.selectu(cadbnk_where_dict)
            
            if tmp_cadbnk_dict == None:
                if not AfaDBFunc.RollbackSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    AfaLoggerFunc.tradeError(">>>Rollback异常")
                AfaLoggerFunc.tradeInfo(">>>Rollback成功")
                return AfaFlowControl.ExitThisFlow("S999","查询将登记卡BIN是否存在异常")
            
            cadbnk_dict = {}
            cadbnk_dict['CARDBIN']      = line_list[0][:12]
            cadbnk_dict['BANKBIN']      = line_list[1][:10]
            
            if len(tmp_cadbnk_dict) <= 0:
                #=====行名行号表中不存在此卡BIN,插入新卡BIN===================
                ret = rccpsDBTrcc_cadbnk.insert(cadbnk_dict)
                if ret <= 0:
                    if not AfaDBFunc.RollbackSql( ):
                        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        AfaLoggerFunc.tradeError(">>>Rollback异常")
                    AfaLoggerFunc.tradeInfo(">>>Rollback成功")
                    return AfaFlowControl.ExitThisFlow("S999","插入新卡BIN异常")
                    
            else:
                #=====行名行号表中存在此卡BIN,更新卡BIN========================
                ret = rccpsDBTrcc_cadbnk.update(cadbnk_dict,cadbnk_where_dict)
                if ret <= 0:
                    if not AfaDBFunc.RollbackSql( ):
                        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        AfaLoggerFunc.tradeError(">>>Rollback异常")
                    AfaLoggerFunc.tradeInfo(">>>Rollback成功")
                    return AfaFlowControl.ExitThisFlow("S999","插入新卡BIN异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束更新卡BIN与行号对照表")
        
        
    AfaLoggerFunc.tradeInfo(">>>结束处理接收到的数据")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
    AfaLoggerFunc.tradeInfo(">>>Commit成功")
    
    #======为通讯回执报文赋值===================================================
    out_context_dict = {}
    out_context_dict['sysType']  = 'rccpst'
    out_context_dict['TRCCO']    = '9900503'
    out_context_dict['MSGTYPCO'] = 'SET008'
    out_context_dict['RCVMBRCO'] = TradeContext.SNDMBRCO
    out_context_dict['SNDMBRCO'] = TradeContext.RCVMBRCO
    out_context_dict['SNDBRHCO'] = TradeContext.BESBNO
    out_context_dict['SNDCLKNO'] = TradeContext.BETELR
    out_context_dict['SNDTRDAT'] = TradeContext.BJEDTE
    out_context_dict['SNDTRTIM'] = TradeContext.BJETIM
    out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
    out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
    out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
    out_context_dict['OPRTYPNO'] = '99'
    out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
    out_context_dict['TRANTYP']  = '0'
    out_context_dict['ORTRCCO']  = TradeContext.TRCCO
    out_context_dict['PRCCO']    = 'RCCI0000'
    out_context_dict['STRINFO']  = '成功'
    
    rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
    
    AfaLoggerFunc.tradeInfo( '***来账.中心类操作(1.本地操作).公共数据通知报文接收[TRCC006_1122]退出***' )
    
    return True


#=====================交易后处理================================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***来账.中心类操作(2.中心回执).公共数据通知报文接收[TRCC006_1122]进入***' )
    
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
    
    AfaLoggerFunc.tradeInfo( '***来账.中心类操作(2.中心回执).公共数据通知报文接收[TRCC006_1122]退出***' )
    return True
        
