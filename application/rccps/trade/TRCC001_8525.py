# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.本地类操作(1.本地操作).汇票业务明细查询
#===============================================================================
#   交易文件:   TRCC001_8525.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-07-09
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_bilbka


#=====================个性化处理(本地操作)======================================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作).汇票业务明细查询[TRC001_8525]进入***' )
    
    #=================必要性检查================================================
    AfaLoggerFunc.tradeDebug(">>>开始必要性检查")
    
    if not TradeContext.existVariable('STRDAT'):
        return AfaFlowControl.ExitThisFlow('S999','起始日期[STRDAT]不存在' )
    elif len(TradeContext.STRDAT) <= 0:
        return AfaFlowControl.ExitThisFlow('S999','起始日期[STRDAT]不能为空' )
        
    if not TradeContext.existVariable('ENDDAT'):
        return AfaFlowControl.ExitThisFlow('S999','终止日期[ENDDAT]不存在' )
    elif len(TradeContext.ENDDAT) <= 0:
        return AfaFlowControl.ExitThisFlow('S999','终止日期[ENDDAT]不能为空' )
        
    AfaLoggerFunc.tradeDebug(">>>结束必要性检查")
    
    #=================组织查询sql语句===========================================
    AfaLoggerFunc.tradeDebug(">>>开始组织查询sql语句")
    
    bilbka_where_sql = ""
    bilbka_where_sql = bilbka_where_sql + "BESBNO='" + TradeContext.BESBNO + "' "
    bilbka_where_sql = bilbka_where_sql + "and BJEDTE >= '" + TradeContext.STRDAT + "' and BJEDTE <= '" + TradeContext.ENDDAT + "'"
    
    #=====判断往来标志是否存在====
    if TradeContext.existVariable('BRSFLG'):
        if len(TradeContext.BRSFLG) > 0:
            bilbka_where_sql = bilbka_where_sql + " and BRSFLG = '" + TradeContext.BRSFLG + "'"
    
    #=====判断交易代码是否存在====
    if TradeContext.existVariable('TRCCO'):
        if len(TradeContext.TRCCO) > 0:
            bilbka_where_sql = bilbka_where_sql + " and TRCCO = '" + TradeContext.TRCCO + "'"
    
    #=====判断报单序号是否存在====        
    if TradeContext.existVariable('BSPSQN'):
        if len(TradeContext.BSPSQN) > 0:
            bilbka_where_sql = bilbka_where_sql + " and BSPSQN = '" + TradeContext.BSPSQN + "'"
    
    #=====判断汇票本行他行标识是否存在====
    if TradeContext.existVariable('BILRS'):
        if len(TradeContext.BILRS) > 0:
            bilbka_where_sql = bilbka_where_sql + " and BILRS = '" + TradeContext.BILRS + "'"
    
    #=====判断汇票版本号是否存在====        
    if TradeContext.existVariable('BILVER'):
        if len(TradeContext.BILVER) > 0:
            bilbka_where_sql = bilbka_where_sql + " and BILVER = '" + TradeContext.BILVER + "'"
    
    #=====判断汇票号码是否存在====
    if TradeContext.existVariable('BILNO'):
        if len(TradeContext.BILNO) > 0:
            bilbka_where_sql = bilbka_where_sql + " and BILNO = '" + TradeContext.BILNO + "'"
    
    #=====判断接收行号是否存在====        
    if TradeContext.existVariable('RCVBNKCO'):
        if len(TradeContext.RCVBNKCO) > 0:
            bilbka_where_sql = bilbka_where_sql + " and RCVBNKCO = '" + TradeContext.RCVBNKCO + "'"
            
    AfaLoggerFunc.tradeDebug(">>>结束组织查询sql语句")
            
    #================查询总笔数==================================================
    AfaLoggerFunc.tradeInfo(">>>开始组织查询总笔数")
    
    all_count = rccpsDBTrcc_bilbka.count(bilbka_where_sql)
    
    AfaLoggerFunc.tradeInfo(">>>结束组织查询总笔数")
    
    if all_count < 0:
        return AfaFlowControl.ExitThisFlow('S999','查询总笔数异常')        
    if all_count == 0:
        return AfaFlowControl.ExitThisFlow('S999','无查询对应记录')        
    if all_count > 0:
        TradeContext.RECALLCOUNT = str(all_count)                #总笔数
        #============查询明细记录================================================
        AfaLoggerFunc.tradeDebug(">>>开始查询明细记录")
        
        bilbka_order_sql = " order by BJEDTE DESC,BSPSQN DESC "
        
        bilbka_dict = rccpsDBTrcc_bilbka.selectm(TradeContext.RECSTRNO,10,bilbka_where_sql,bilbka_order_sql)
        
        AfaLoggerFunc.tradeDebug(">>>结束查询明细记录")
        
        if bilbka_dict == None:
            return AfaFlowControl.ExitThisFlow('S999','查询明细记录异常')        
        if len(bilbka_dict) <= 0:
            return AfaFlowControl.ExitThisFlow('S999','查询明细无记录')
        else:
            TradeContext.RECCOUNT = str(len(bilbka_dict))         #本次查询笔数
            #========生成输出form文件============================================
            AfaLoggerFunc.tradeInfo(">>>开始生成文件")
            
            file_name = "rccps_" + TradeContext.BETELR + "_" + AfaUtilTools.GetHostDate() + "_" + TradeContext.TransCode
            
            try:
            	fpath=os.environ["AFAP_HOME"]+"/tmp/"
            	fp=open(fpath+file_name,"w") 
            except IOError:
                return AfaFlowControl.ExitThisFlow('S999','打开文件失败')
            
            for i in xrange(len(bilbka_dict)):
                #====查询此交易状态信息==========================================
                stat_dict = {}
                ret = rccpsState.getTransStateCur(bilbka_dict[i]['BJEDTE'],bilbka_dict[i]['BSPSQN'],stat_dict)
                
                if not ret:
                    AfaLoggerFunc.tradeDebug("查询交易状态信息异常")
                    return AfaFlowControl.ExitThisFlow('S999','生成文件异常')
                
                file_line = bilbka_dict[i]['BJEDTE']   + "|" \
                          + bilbka_dict[i]['BSPSQN']   + "|" \
                          + bilbka_dict[i]['BRSFLG']   + "|" \
                          + bilbka_dict[i]['OPRNO']    + "|" \
                          + bilbka_dict[i]['BESBNO']   + "|" \
                          + bilbka_dict[i]['BEACSB']   + "|" \
                          + bilbka_dict[i]['BETELR']   + "|" \
                          + bilbka_dict[i]['BEAUUS']   + "|" \
                          + bilbka_dict[i]['BBSSRC']   + "|" \
                          + bilbka_dict[i]['DASQ']     + "|" \
                          + bilbka_dict[i]['DCFLG']    + "|" \
                          + bilbka_dict[i]['NCCWKDAT'] + "|" \
                          + bilbka_dict[i]['TRCCO']    + "|" \
                          + bilbka_dict[i]['TRCDAT']   + "|" \
                          + bilbka_dict[i]['TRCNO']    + "|" \
                          + bilbka_dict[i]['SNDBNKCO'] + "|" \
                          + bilbka_dict[i]['SNDBNKNM'] + "|" \
                          + bilbka_dict[i]['RCVBNKCO'] + "|" \
                          + bilbka_dict[i]['RCVBNKNM'] + "|" \
                          + bilbka_dict[i]['BILVER']   + "|" \
                          + bilbka_dict[i]['BILNO']    + "|" \
                          + bilbka_dict[i]['BILRS']    + "|" \
                          + bilbka_dict[i]['HPSTAT']   + "|" \
                          + stat_dict['BCSTAT']        + "|" \
                          + stat_dict['BDWFLG']        + "|" 
                fp.write(file_line + "\n")
                
            fp.close()
            AfaLoggerFunc.tradeInfo(">>>结束生成文件")
        
        TradeContext.PBDAFILE = file_name       #文件名
        TradeContext.errorCode = "0000"
        TradeContext.errorMsg  = "成功"
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作).汇票业务明细查询[TRC001_8525]退出***' )
    return True
