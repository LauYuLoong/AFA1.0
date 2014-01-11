# -*- coding: gbk -*-
##################################################################
#   农信银.查询业务.通存通兑汇总核对查询
#=================================================================
#   程序文件:   TRCC001_8568.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘振东
#   修改时间:   2008-12-22
##################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaDBFunc
import rccpsDBTrcc_wtrbka,rccpsDBTrcc_tddzhz
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作)通存通兑汇总核对查询[TRC001_8568]进入***' )
    #=====判断接口是否存在====
    if not TradeContext.existVariable("NCCWKDAT"):
        return AfaFlowControl.ExitThisFlow('M999','中心工作日期[NCCWKDAT]不存在')

    #=====按行号查询====
    sql = "NCCWKDAT = '" + TradeContext.NCCWKDAT + "'"
    
    #=====查询数据库，得到查询结果集====
    record=rccpsDBTrcc_tddzhz.selectm(TradeContext.RECSTRNO,10,sql,"")  
    if record == None:
        return AfaFlowControl.ExitThisFlow('D000','数据库操作失败')
    elif len(record) <= 0:
        return AfaFlowControl.ExitThisFlow('D000','没有满足条件的记录')
    else:
        filename = 'rccps_' + TradeContext.BETELR + '_' + AfaUtilTools.GetSysDate() + '_' + TradeContext.TransCode 
        try:
            f=open("/home/maps/afa/tmp/"+filename,"w")
        except IOError:
            AfaLoggerFunc.tradeInfo('打开文件失败')
            return AfaFlowControl.ExitThisFlow('A999','打开文件失败')

        AfaLoggerFunc.tradeDebug( '文件名：' + filename )
        #=====组织返回文件====
        AfaLoggerFunc.tradeDebug( 'start=' + str(record) )
        
        for i in range( 0, len(record) ):

########################################################################################################################
            #=====判断业务类型和往来标示====
            if( record[i]['TRCCO'] == '0000000' and record[i]['BRSFLG'] == '1'):
                
                ##=====合计 开户汇总====
                AfaLoggerFunc.tradeInfo('开始==合计 开户汇总==')
                
                #=====贷方汇总金额====
                AfaLoggerFunc.tradeInfo('合计 开户汇总__贷方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in (" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为： ' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('合计 开户汇总__借方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))    
                
                #=====贷方汇总手续费====
                AfaLoggerFunc.tradeInfo('合计 开户汇总__贷方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and TRCCO in ('3000102','3000103','3000104','3000105') and CHRGTYP='1'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                AfaLoggerFunc.tradeInfo('合计 开户汇总__借方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and TRCCO in ('3000102','3000103','3000104','3000105') and CHRGTYP='1'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT))   
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('合计 开户汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '0000000' and record[i]['BRSFLG'] == '3' ): 
                
                ##=====合计 调账汇总====
                AfaLoggerFunc.tradeInfo('开始==合计 调账汇总==')
                
                #=====贷方汇总金额====
                AfaLoggerFunc.tradeInfo('合计 调账汇总__贷方汇总金额')
                TradeContext.INRCTAMT = 0.00
                
                #=====借方汇总金额====
                TradeContext.INRDTAMT = 0.00
                
                #=====贷方汇总手续费====
                TradeContext.INRCHRCTAMT = 0.00
                
                #=====借方汇总手续费====
                TradeContext.INRCHRDTAMT = 0.00
                
                #=====轧差汇总金额====
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '0000000' and record[i]['BRSFLG'] == '0' ): 
                
                ##=====合计 受理汇总====
                AfaLoggerFunc.tradeInfo('开始==合计 受理汇总==')
                
                #=====贷方汇总金额====   
                AfaLoggerFunc.tradeInfo('合计 受理汇总__贷方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('合计 受理汇总__借方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))    
                
                #=====贷方汇总手续费====
                AfaLoggerFunc.tradeInfo('合计 受理汇总__贷方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and TRCCO in ('3000102','3000103','3000104','3000105') and CHRGTYP='1'" 
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                AfaLoggerFunc.tradeInfo('合计 受理汇总__借方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and TRCCO in ('3000102','3000103','3000104','3000105') and CHRGTYP='1'" 
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT))
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('合计 受理汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT)) 
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '0000000' and record[i]['BRSFLG'] == '2' ):

                ##=====合计 轧差汇总====
                AfaLoggerFunc.tradeInfo('开始==合计 轧差汇总==')
                
                #=====贷方汇总金额====   
                AfaLoggerFunc.tradeInfo('合计 轧差汇总__贷方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT1 = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT1 = 0.00
                    else:
                        TradeContext.INRCTAMT1 = wtrbka_list[0][0]
                        
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT2 = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT2 = 0.00
                    else:
                        TradeContext.INRCTAMT2 = wtrbka_list[0][0]
               
                TradeContext.INRCTAMT = TradeContext.INRCTAMT1 + TradeContext.INRCTAMT2                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('合计 轧差汇总__借方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT1 = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT1 = 0.00
                    else:
                        TradeContext.INRDTAMT1 = wtrbka_list[0][0]
                        
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT2 = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT2 = 0.00
                    else:
                        TradeContext.INRDTAMT2 = wtrbka_list[0][0]
                                        
                TradeContext.INRDTAMT = TradeContext.INRDTAMT1 + TradeContext.INRDTAMT2                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))    
                
                #=====贷方汇总手续费====
                AfaLoggerFunc.tradeInfo('合计 轧差汇总__贷方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and TRCCO in ('3000102','3000103','3000104','3000105') and CHRGTYP='1'" 
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT1 = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT1 = 0.00
                    else:
                        TradeContext.INRCHRCTAMT1 = wtrbka_list[0][0]
                        
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and TRCCO in ('3000102','3000103','3000104','3000105') and CHRGTYP='1'" 
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT2 = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT2 = 0.00
                    else:
                        TradeContext.INRCHRCTAMT2 = wtrbka_list[0][0]
                                        
                TradeContext.INRCHRCTAMT = TradeContext.INRCHRCTAMT1 + TradeContext.INRCHRCTAMT2                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                AfaLoggerFunc.tradeInfo('合计 轧差汇总__借方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and TRCCO in ('3000102','3000103','3000104','3000105') and CHRGTYP='1'" 
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT1 = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT1 = 0.00
                    else:
                        TradeContext.INRCHRDTAMT1 = wtrbka_list[0][0]
                        
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and TRCCO in ('3000102','3000103','3000104','3000105') and CHRGTYP='1'" 
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT2 = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT2 = 0.00
                    else:
                        TradeContext.INRCHRDTAMT2 = wtrbka_list[0][0]
                                        
                TradeContext.INRCHRDTAMT = TradeContext.INRCHRDTAMT1 + TradeContext.INRCHRDTAMT2                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT))
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('合计 轧差汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000001' and record[i]['BRSFLG'] == '1' ):
                ##=====ATM本转异 开户汇总====
                AfaLoggerFunc.tradeInfo('开始==ATM本转异 开户汇总==')
                
                #=====贷方汇总金额====
                TradeContext.INRCTAMT = 0.00
                
                #=====借方汇总金额====
                TradeContext.INRDTAMT = 0.00
                
                #=====贷方汇总手续费====
                TradeContext.INRCHRCTAMT = 0.00
                
                #=====借方汇总手续费====
                TradeContext.INRCHRDTAMT = 0.00
                
                #=====轧差汇总金额====
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000001' and record[i]['BRSFLG'] == '0' ):
                ##=====ATM本转异 受理汇总====
                AfaLoggerFunc.tradeInfo('开始==ATM本转异 受理汇总==')
                
                #=====贷方汇总金额====
                TradeContext.INRCTAMT = 0.00
                
                #=====借方汇总金额====
                TradeContext.INRDTAMT = 0.00
                
                #=====贷方汇总手续费====
                TradeContext.INRCHRCTAMT = 0.00
                
                #=====借方汇总手续费====
                TradeContext.INRCHRDTAMT = 0.00
                
                #=====轧差汇总金额====
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000002' and record[i]['BRSFLG'] == '1' ):

                ##=====柜台卡存现 开户汇总====
                AfaLoggerFunc.tradeInfo('开始==柜台卡存现 开户汇总==')
                
                #=====贷方汇总金额====   
                AfaLoggerFunc.tradeInfo('柜台卡存现 开户汇总__贷方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000002' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('柜台卡存现 开户汇总__借方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000002' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))    
                
                #=====贷方汇总手续费====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT))
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('柜台卡存现 开户汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT)) 

#########################################################################################################################
            elif( record[i]['TRCCO'] == '3000002' and record[i]['BRSFLG'] == '0' ): 
                
                ##=====柜台卡存现 受理汇总====
                AfaLoggerFunc.tradeInfo('开始==柜台卡存现 受理汇总==')
                
                 #=====贷方汇总金额====   
                AfaLoggerFunc.tradeInfo('柜台卡存现 受理汇总__贷方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000002' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('柜台卡存现 受理汇总__借方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000002' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))    
                
                #=====贷方汇总手续费====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT))
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('柜台卡存现 受理汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))   
                
#########################################################################################################################
            elif( record[i]['TRCCO'] == '3000003' and record[i]['BRSFLG'] == '1' ):

                ##=====柜台卡本转异 开户汇总====
                AfaLoggerFunc.tradeInfo('开始==柜台卡本转异 开户汇总==')
                
                #=====贷方汇总金额====   
                AfaLoggerFunc.tradeInfo('柜台卡本转异 开户汇总__贷方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000003' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('柜台卡本转异 开户汇总__借方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000003' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))    
                
                #=====贷方汇总手续费====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT))
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('柜台卡本转异 开户汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT)) 
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000003' and record[i]['BRSFLG'] == '0' ): 
                
                ##=====柜台卡本转异 受理汇总====
                AfaLoggerFunc.tradeInfo('开始==柜台卡本转异 受理汇总==')
                
                 #=====贷方汇总金额====   
                AfaLoggerFunc.tradeInfo('柜台卡本转异 受理汇总__贷方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000003' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('柜台卡本转异 受理汇总__借方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000003' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))    
                
                #=====贷方汇总手续费====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT))
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('柜台卡本转异 受理汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT)) 
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000004' and record[i]['BRSFLG'] == '1' ):

                ##=====柜台折存现 开户汇总====
                AfaLoggerFunc.tradeInfo('开始==柜台折存现 开户汇总==')
                
                #=====贷方汇总金额====   
                AfaLoggerFunc.tradeInfo('柜台折存现 开户汇总__贷方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000004' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('柜台折存现 开户汇总__借方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000004' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))    
                
                #=====贷方汇总手续费====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT))
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('柜台折存现 开户汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000004' and record[i]['BRSFLG'] == '0' ): 
                
                ##=====柜台折存现 受理汇总====
                AfaLoggerFunc.tradeInfo('开始==柜台折存现 受理汇总==')
                
                 #=====贷方汇总金额====   
                AfaLoggerFunc.tradeInfo('柜台折存现 受理汇总__贷方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000004' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('柜台折存现 受理汇总__借方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000004' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))    
                
                #=====贷方汇总手续费====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT))
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('柜台折存现 受理汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))  
                           
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000005' and record[i]['BRSFLG'] == '1' ):

                ##=====柜台折本转异 开户汇总====
                AfaLoggerFunc.tradeInfo('开始==柜台折本转异 开户汇总==')
                
                #=====贷方汇总金额====   
                AfaLoggerFunc.tradeInfo('柜台折本转异 开户汇总__贷方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000005' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('柜台折本转异 开户汇总__借方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000005' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))    
                
                #=====贷方汇总手续费====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT))
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('柜台折本转异 开户汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT)) 
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000005' and record[i]['BRSFLG'] == '0' ): 
                
                ##=====柜台折本转异 受理汇总====
                AfaLoggerFunc.tradeInfo('开始==柜台折本转异 受理汇总==')
                
                 #=====贷方汇总金额====   
                AfaLoggerFunc.tradeInfo('柜台折本转异 受理汇总__贷方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000005' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('柜台折本转异 受理汇总__借方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000005' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))    
                
                #=====贷方汇总手续费====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT))
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('柜台折本转异 受理汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT)) 
                    
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000100' and record[i]['BRSFLG'] == '1' ):
                
                ##=====ATM取现 开户汇总====
                AfaLoggerFunc.tradeInfo('开始==ATM取现 开户汇总==')
                
                #=====贷方汇总金额====
                TradeContext.INRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                TradeContext.INRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))
                
                #=====贷方汇总手续费====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT))
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('ATM取现 开户汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000100' and record[i]['BRSFLG'] == '0' ):
                
                ##=====ATM取现 受理汇总====
                AfaLoggerFunc.tradeInfo('开始==ATM取现 受理汇总==')
                
                #=====贷方汇总金额====
                TradeContext.INRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                TradeContext.INRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))
                
                #=====贷方汇总手续费====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT))
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('ATM取现 受理汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000101' and record[i]['BRSFLG'] == '1' ):
                
                ##=====ATM异转本 开户汇总====
                AfaLoggerFunc.tradeInfo('开始==ATM异转本 开户汇总==')
                
                #=====贷方汇总金额====
                TradeContext.INRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                TradeContext.INRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))
                
                #=====贷方汇总手续费====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT))
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('ATM异转本 开户汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000101' and record[i]['BRSFLG'] == '0' ):
                
                ##=====ATM异转本 受理汇总====
                AfaLoggerFunc.tradeInfo('开始==ATM异转本 受理汇总==')
                
                #=====贷方汇总金额====
                TradeContext.INRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                TradeContext.INRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))
                
                #=====贷方汇总手续费====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT))
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('ATM异转本 受理汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))
                
########################################################################################################################                
            elif( record[i]['TRCCO'] == '3000102' and record[i]['BRSFLG'] == '1' ):

                ##=====柜台卡取现 开户汇总====
                AfaLoggerFunc.tradeInfo('开始==柜台卡取现 开户汇总==')
                
                #=====贷方汇总金额====   
                AfaLoggerFunc.tradeInfo('柜台卡取现 开户汇总__贷方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000102' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('柜台卡取现 开户汇总__借方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000102' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))    
                
                #=====贷方汇总手续费====
                AfaLoggerFunc.tradeInfo('柜台卡取现 开户汇总__贷方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000102' and CHRGTYP='1' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                AfaLoggerFunc.tradeInfo('柜台卡取现 开户汇总__借方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000102' and CHRGTYP='1' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT))
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('柜台卡取现 开户汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000102' and record[i]['BRSFLG'] == '0' ): 
                
                ##=====柜台卡取现 受理汇总====
                AfaLoggerFunc.tradeInfo('开始==柜台卡取现 受理汇总==')
                
                 #=====贷方汇总金额====   
                AfaLoggerFunc.tradeInfo('柜台卡取现 受理汇总__贷方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000102' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('柜台卡取现 受理汇总__借方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000102' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))    
                
                #=====贷方汇总手续费====
                AfaLoggerFunc.tradeInfo('柜台卡取现 受理汇总__贷方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000102' and CHRGTYP='1' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                AfaLoggerFunc.tradeInfo('柜台卡取现 受理汇总__借方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000102' and CHRGTYP='1' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT))
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('柜台卡取现 受理汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))
                     
########################################################################################################################                          
            elif( record[i]['TRCCO'] == '3000103' and record[i]['BRSFLG'] == '1' ):

                ##=====柜台卡异转本 开户汇总====
                AfaLoggerFunc.tradeInfo('开始==柜台卡异转本 开户汇总==')
                
                #=====贷方汇总金额====   
                AfaLoggerFunc.tradeInfo('柜台卡异转本 开户汇总__贷方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000103' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('柜台卡异转本 开户汇总__借方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000103' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))    
                
                #=====贷方汇总手续费====
                AfaLoggerFunc.tradeInfo('柜台卡异转本 开户汇总__贷方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000103' and CHRGTYP='1' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                AfaLoggerFunc.tradeInfo('柜台卡异转本 开户汇总__借方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000103' and CHRGTYP='1' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT))
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('柜台卡异转本 开户汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))  
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000103' and record[i]['BRSFLG'] == '0' ): 
                
                ##=====柜台卡异转本 受理汇总====
                AfaLoggerFunc.tradeInfo('开始==柜台卡异转本 受理汇总==')
                
                 #=====贷方汇总金额====   
                AfaLoggerFunc.tradeInfo('柜台卡异转本 受理汇总__贷方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000103' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('柜台卡异转本 受理汇总__借方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000103' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))    
                
                #=====贷方汇总手续费====
                AfaLoggerFunc.tradeInfo('柜台卡异转本 受理汇总__贷方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000103' and CHRGTYP='1' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                AfaLoggerFunc.tradeInfo('柜台卡异转本 受理汇总__借方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000103' and CHRGTYP='1' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT))  
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('柜台卡异转本 受理汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))
                        
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000104' and record[i]['BRSFLG'] == '1' ):

                ##=====柜台折取现 开户汇总====
                AfaLoggerFunc.tradeInfo('开始==柜台折取现 开户汇总==')
                
                #=====贷方汇总金额====   
                AfaLoggerFunc.tradeInfo('柜台折取现 开户汇总__贷方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000104' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('柜台折取现 开户汇总__借方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000104' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))    
                
                #=====贷方汇总手续费====
                AfaLoggerFunc.tradeInfo('柜台折取现 开户汇总__贷方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000104' and CHRGTYP='1' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                AfaLoggerFunc.tradeInfo('柜台折取现 开户汇总__借方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000104' and CHRGTYP='1' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT))
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('柜台折取现 开户汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT)) 
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000104' and record[i]['BRSFLG'] == '0' ): 
                
                ##=====柜台折取现 受理汇总====
                AfaLoggerFunc.tradeInfo('开始==柜台折取现 受理汇总==')
                
                 #=====贷方汇总金额====   
                AfaLoggerFunc.tradeInfo('柜台折取现 受理汇总__贷方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000104' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('柜台折取现 受理汇总__借方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000104' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))    
                
                #=====贷方汇总手续费====
                AfaLoggerFunc.tradeInfo('柜台折取现 受理汇总__贷方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000104' and CHRGTYP='1' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                AfaLoggerFunc.tradeInfo('柜台折取现 受理汇总__借方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000104' and CHRGTYP='1' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT)) 
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('柜台折取现 受理汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))
                                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000105' and record[i]['BRSFLG'] == '1' ):

                ##=====柜台折异转本 开户汇总====
                AfaLoggerFunc.tradeInfo('开始==柜台折异转本 开户汇总==')
                
                #=====贷方汇总金额====   
                AfaLoggerFunc.tradeInfo('柜台折异转本 开户汇总__贷方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000105' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('柜台折异转本 开户汇总__借方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000105' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))    
                
                #=====贷方汇总手续费====
                AfaLoggerFunc.tradeInfo('柜台折异转本 开户汇总__贷方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000105' and CHRGTYP='1' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                AfaLoggerFunc.tradeInfo('柜台折异转本 开户汇总__借方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000105' and CHRGTYP='1' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT))
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('柜台折异转本 开户汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT)) 
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000105' and record[i]['BRSFLG'] == '0' ): 
                
                ##=====柜台折异转本 受理汇总====
                AfaLoggerFunc.tradeInfo('开始==柜台折异转本 受理汇总==')
                
                 #=====贷方汇总金额====   
                AfaLoggerFunc.tradeInfo('柜台折异转本 受理汇总__贷方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000105' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('柜台折异转本 受理汇总__借方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000105' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))    
                
                #=====贷方汇总手续费====
                AfaLoggerFunc.tradeInfo('柜台折异转本 受理汇总__贷方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000105' and CHRGTYP='1' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                AfaLoggerFunc.tradeInfo('柜台折异转本 受理汇总__借方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000105' and CHRGTYP='1' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT)) 
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('柜台折异转本 受理汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))
                   
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000503' and record[i]['BRSFLG'] == '1' ):

                ##=====柜台存款确认 开户汇总====
                AfaLoggerFunc.tradeInfo('开始==柜台存款确认 开户汇总==')
                
                #=====贷方汇总金额====   
                AfaLoggerFunc.tradeInfo('柜台存款确认 开户汇总__贷方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000503' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('柜台存款确认 开户汇总__借方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000503' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))    
                
                #=====贷方汇总手续费====
                AfaLoggerFunc.tradeInfo('柜台存款确认 开户汇总__贷方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000503' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                AfaLoggerFunc.tradeInfo('柜台存款确认 开户汇总__借方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('70','72','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000503' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT))
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('柜台存款确认 开户汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT)) 
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000503' and record[i]['BRSFLG'] == '0' ): 
                
                ##=====柜台存款确认 受理汇总====
                AfaLoggerFunc.tradeInfo('开始==柜台存款确认 受理汇总==')
                
                 #=====贷方汇总金额====   
                AfaLoggerFunc.tradeInfo('柜台存款确认 受理汇总__贷方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000503' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('柜台存款确认 受理汇总__借方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000503' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))    
                
                #=====贷方汇总手续费====
                AfaLoggerFunc.tradeInfo('柜台存款确认 受理汇总__贷方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000503' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                AfaLoggerFunc.tradeInfo('柜台存款确认 受理汇总__借方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('42','81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000503' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT)) 
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('柜台存款确认 受理汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT)) 
                   
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000504' and record[i]['BRSFLG'] == '1' ):

                ##=====柜台冲销 开户汇总====
                AfaLoggerFunc.tradeInfo('开始==柜台冲销 开户汇总==')
                
                #=====贷方汇总金额====   
                AfaLoggerFunc.tradeInfo('柜台冲销 开户汇总__贷方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000504' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('柜台冲销 开户汇总__借方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000504' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))    
                
                #=====贷方汇总手续费====
                AfaLoggerFunc.tradeInfo('柜台冲销 开户汇总__贷方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000504' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                AfaLoggerFunc.tradeInfo('柜台冲销 开户汇总__借方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000504' and BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT))
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('柜台冲销 开户汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000504' and record[i]['BRSFLG'] == '0' ): 
                
                ##=====柜台冲销 受理汇总====
                AfaLoggerFunc.tradeInfo('开始==柜台冲销 受理汇总==')
                
                 #=====贷方汇总金额====   
                AfaLoggerFunc.tradeInfo('柜台冲销 受理汇总__贷方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000504' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = wtrbka_list[0][0]
                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('柜台冲销 受理汇总__借方汇总金额')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(OCCAMT) from rcc_wtrbka where TRCCO='3000504' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = wtrbka_list[0][0]
                
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))    
                
                #=====贷方汇总手续费====
                AfaLoggerFunc.tradeInfo('柜台冲销 受理汇总__贷方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000504' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRCTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRCTAMT = 0.00
                    else:
                        TradeContext.INRCHRCTAMT = wtrbka_list[0][0]
                
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                AfaLoggerFunc.tradeInfo('柜台冲销 受理汇总__借方汇总手续费')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in ('81')"
                spbsta_sql = spbsta_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "'"
                wtrbka_sql = "select sum(CUSCHRG) from rcc_wtrbka where TRCCO='3000504' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                wtrbka_sql = wtrbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeDebug('wtrbka_sql为：' + wtrbka_sql)
                wtrbka_list = AfaDBFunc.SelectSql(wtrbka_sql)
                if( wtrbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','通存通兑登记簿操作失败')
                elif( len(wtrbka_list) <= 0 ):
                    TradeContext.INRCHRDTAMT = 0.00
                else:
                    if( wtrbka_list[0][0] == None ):
                        TradeContext.INRCHRDTAMT = 0.00
                    else:
                        TradeContext.INRCHRDTAMT = wtrbka_list[0][0]
                
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT)) 
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('柜台冲销 受理汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000505' and record[i]['BRSFLG'] == '1' ):
                
                ##=====柜台补正交易 开户汇总====
                AfaLoggerFunc.tradeInfo('开始==柜台补正交易 开户汇总==')
                
                #=====贷方汇总金额====
                TradeContext.INRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                TradeContext.INRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))
                
                #=====贷方汇总手续费====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT))
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('柜台补正交易 开户汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))
                
########################################################################################################################
            elif( record[i]['TRCCO'] == '3000505' and record[i]['BRSFLG'] == '0' ):
                
                ##=====柜台补正交易 受理汇总====
                AfaLoggerFunc.tradeInfo('开始==柜台补正交易 受理汇总==')
                
                #=====贷方汇总金额====
                TradeContext.INRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                TradeContext.INRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))
                
                #=====贷方汇总手续费====
                TradeContext.INRCHRCTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRCTAMT为：'+  str(TradeContext.INRCHRCTAMT))
                
                #=====借方汇总手续费====
                TradeContext.INRCHRDTAMT = 0.00
                AfaLoggerFunc.tradeInfo('INRCHRDTAMT为：'+  str(TradeContext.INRCHRDTAMT))
                
                #=====轧差汇总金额====
                AfaLoggerFunc.tradeInfo('柜台补正交易 受理汇总__轧差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT + TradeContext.INRCHRCTAMT - TradeContext.INRDTAMT - TradeContext.INRCHRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))
                   
########################################################################################################################
########################################################################################################################
            
            #====从通存通兑业务登记簿统计行内通存通兑业务总笔数====
            wtrbka_sql = "select count(*) from rcc_wtrbka where NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
            
            #=====判断BRSFLG====
            if str(record[i]['BRSFLG']) != '2':
                wtrbka_sql = wtrbka_sql + " and BRSFLG='" + record[i]['BRSFLG'] + "'"
            
            #=====判断TRCCO====
            if str(record[i]['TRCCO']) != '0000000':
                wtrbka_sql = wtrbka_sql + " and TRCCO ='" + record[i]['TRCCO'] + "'"

            #=====根据来往账赋值不同的交易状态====
            if record[i]['BRSFLG'] == PL_BRSFLG_SND:
                wtrbka_sql = wtrbka_sql + " and bspsqn in (select bspsqn from rcc_spbsta where bcstat in ('42','81')"
                wtrbka_sql = wtrbka_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "')"
            elif record[i]['BRSFLG'] == PL_BRSFLG_RCV:
                wtrbka_sql = wtrbka_sql + " and bspsqn in (select bspsqn from rcc_spbsta where bcstat in ('70','72','81')"
                wtrbka_sql = wtrbka_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "')"
            else:
                wtrbka_sql = wtrbka_sql + " and bspsqn in (select bspsqn from rcc_spbsta where bcstat in ('70','72','42','81')"
                wtrbka_sql = wtrbka_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "')"
            AfaLoggerFunc.tradeDebug( 'sql==' + wtrbka_sql ) 
            
            #=====查询数据库====
            count = AfaDBFunc.SelectSql(wtrbka_sql)
            if(count==None):
                f.close()
                return AfaFlowControl.ExitThisFlow('D000','数据库操作失败')
            if len(count) == 0:
                f.close()
                return AfaFlowControl.ExitThisFlow('D000','无满足条件的记录')
            else:
                TradeContext.INRTCNT = str(count[0][0])
                
            #=====开始组织文件内容====
            filecont = ''
            filecont = filecont + record[i]['NCCWKDAT']       + "|" 
            filecont = filecont + record[i]['TRCCO']          + "|"
            filecont = filecont + record[i]['BRSFLG']         + "|" 
            filecont = filecont + record[i]['TRCNAM']         + "|"
            filecont = filecont + record[i]['TRCRSNM']        + "|" 
            filecont = filecont + str(record[i]['TCNT'])      + "|" + str(TradeContext.INRTCNT)       + "|"                               
            filecont = filecont + str(record[i]['CTAMT'])     + "|" + str(TradeContext.INRCTAMT)      + "|"
            filecont = filecont + str(record[i]['DTAMT'])     + "|" + str(TradeContext.INRDTAMT)      + "|"
            filecont = filecont + str(record[i]['CHRCTAMT'])  + "|" + str(TradeContext.INRCHRCTAMT)   + "|"
            filecont = filecont + str(record[i]['CHRDTAMT'])  + "|" + str(TradeContext.INRCHRDTAMT)   + "|"
            filecont = filecont + str(record[i]['OFSTAMT'])   + "|" + str(TradeContext.INROFSTAMT)    + "|\n"
            f.write(filecont)

        #=====关闭文件====
        f.close()

    #=====查询总记录数====
    allcount=rccpsDBTrcc_tddzhz.count(sql)     #得到总记录笔数
    if(allcount==None):
        return AfaFlowControl.ExitThisFlow('D000','数据库操作失败')
    else:
        TradeContext.RECALLCOUNT = str(allcount)

    TradeContext.PBDAFILE = filename            #文件名
    TradeContext.RECCOUNT = str(len(record))    #查询笔数
    TradeContext.errorMsg="查询成功"
    TradeContext.errorCode="0000"
    
    AfaLoggerFunc.tradeInfo(  '***农信银系统：往账.本地类操作(1.本地操作)通存通兑汇总核对查询[TRC001_8568] 退出***'  )
    return True
