# -*- coding: gbk -*-
##################################################################
#   农信银.查询业务.汇兑汇总核对查询
#=================================================================
#   程序文件:   TRCC001_8546.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘雨龙
#   修改时间:   2008-06-12
##################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,rccpsDBTrcc_hddzhz,os
import rccpsDBTrcc_trcbka,AfaDBFunc

from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作)交易[TRC001_8546]进入***' )
    
    #=====判断接口是否存在====
    if not TradeContext.existVariable("NCCWKDAT"):
        return AfaFlowControl.ExitThisFlow('M999','中心工作日期[NCCWKDAT]不存在')

    #=====按行号查询====
    sql = "NCCWKDAT = '" + TradeContext.NCCWKDAT + "'"
    
    #=====查询数据库，得到查询结果集====
    record=rccpsDBTrcc_hddzhz.selectm(TradeContext.RECSTRNO,10,sql,"")  
    if record == None:
        return AfaFlowControl.ExitThisFlow('D000','数据库操作失败')
    elif len(record) <= 0:
        return AfaFlowControl.ExitThisFlow('D000','没有满足条件的记录')
    else:
        #=====打开文件操作====
        filename = 'rccps_' + TradeContext.BETELR + '_' + AfaUtilTools.GetSysDate() + '_' + TradeContext.TransCode 
        try:
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('A999','打开文件失败')

        #=====组织返回文件====
        for i in range( 0, len(record) ):
            #=====判断业务类型和往来标示=====
            if( record[i]['TRCCO'] == '0000000' and record[i]['BRSFLG'] == '0' ):
                #=====合计 往帐汇总====
                AfaLoggerFunc.tradeInfo('合计 往帐汇总')
                                
                #=====贷方汇总金额====
                AfaLoggerFunc.tradeInfo('合计 往帐汇总__贷方汇总')

                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='" + PL_BCSTAT_MFESTL + "'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('合计 往帐汇总__借方汇总')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='" + PL_BCSTAT_MFESTL + "'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))
                
                #=====扎差汇总金额====
                AfaLoggerFunc.tradeInfo('合计 往帐汇总__扎差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))
                
            
###########################################################################################################################
            
            elif( record[i]['TRCCO'] == '0000000' and record[i]['BRSFLG'] == '1' ):
                #=====合计 来帐汇总====
                AfaLoggerFunc.tradeInfo('合计 来帐汇总')
                #=====贷方汇总金额====
                AfaLoggerFunc.tradeInfo('合计 来帐汇总__贷方汇总')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('合计 来帐汇总__借方汇总')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))
                
                #=====扎差汇总金额====
                AfaLoggerFunc.tradeInfo('合计 来帐汇总__扎差汇总')   
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))
            
############################################################################################################################# 
            
            elif( record[i]['TRCCO'] == '0000000' and record[i]['BRSFLG'] == '9' ):
                #=====合计 扎差汇总====
                AfaLoggerFunc.tradeInfo('合计 扎差汇总')
                #=====贷方汇总金额====
                AfaLoggerFunc.tradeInfo('合计 扎差汇总__贷方汇总')
                
#                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','42','80')"
#                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
#                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
#                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
#                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
#                if( trcbka_list == None ):
#                    f.close()
#                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
#                elif( len(trcbka_list) <= 0 ):
#                    TradeContext.INRCTAMT = 0.00
#                else:
#                    if( trcbka_list[0][0] == None ):
#                        TradeContext.INRCTAMT = 0.00
#                    else:
#                        TradeContext.INRCTAMT = trcbka_list[0][0]
                        
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='42'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT1 = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT1 = 0.00
                    else:
                        TradeContext.INRCTAMT1 = trcbka_list[0][0]
                        
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT2 = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT2 = 0.00
                    else:
                        TradeContext.INRCTAMT2 = trcbka_list[0][0]
                        
                TradeContext.INRCTAMT = TradeContext.INRCTAMT1 + TradeContext.INRCTAMT2
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('合计 扎差汇总__借方汇总')
                
#                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','42','80')"
#                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
#                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
#                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
#                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
#                if( trcbka_list == None ):
#                    f.close()
#                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
#                elif( len(trcbka_list) <= 0 ):
#                    TradeContext.INRDTAMT = 0.00
#                else:
#                    if( trcbka_list[0][0] == None ):
#                        TradeContext.INRDTAMT = 0.00
#                    else:
#                        TradeContext.INRDTAMT = trcbka_list[0][0]

                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='42'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT1 = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT1 = 0.00
                    else:
                        TradeContext.INRDTAMT1 = trcbka_list[0][0]
                        
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where BRSFLG='1' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT2 = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT2 = 0.00
                    else:
                        TradeContext.INRDTAMT2 = trcbka_list[0][0]
                        
                TradeContext.INRDTAMT = TradeContext.INRDTAMT1 + TradeContext.INRDTAMT2
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))
                
                #=====扎差汇总金额====
                AfaLoggerFunc.tradeInfo('合计 扎差汇总__扎差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))   
            
##############################################################################################################################            
            
            elif( record[i]['TRCCO'] == '2000001' and record[i]['BRSFLG'] == '0' ):
                #=====汇兑 往帐====
                AfaLoggerFunc.tradeInfo('汇兑 往帐')
                #=====贷方汇总金额====
                AfaLoggerFunc.tradeInfo('汇兑 往帐__贷方汇总')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='" + PL_BCSTAT_MFESTL + "'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000001' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('汇兑 往帐__借方汇总')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='" + PL_BCSTAT_MFESTL + "'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000001' and BRSFLG='0' and  DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))
                
                #=====扎差汇总金额====
                AfaLoggerFunc.tradeInfo('汇兑 往帐__扎差汇总')   
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))   
            
##############################################################################################################################            
            
            elif( record[i]['TRCCO'] == '2000001' and record[i]['BRSFLG'] == '1' ):
                #=====汇兑 来帐====
                AfaLoggerFunc.tradeInfo('汇兑 来帐')
                #=====贷方汇总金额====
                AfaLoggerFunc.tradeInfo('汇兑 来帐__贷方汇总')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000001' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('汇兑 来帐__借方汇总')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000001' and BRSFLG='1' and  DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRDTAMT为：'+  str(TradeContext.INRDTAMT))
                
                #=====扎差汇总金额====
                AfaLoggerFunc.tradeInfo('汇兑 来帐__扎差汇总') 
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))     
            
##############################################################################################################################            

            elif( record[i]['TRCCO'] == '2000002' and record[i]['BRSFLG'] == '0' ):
                #=====委托收款划回 往账====
                AfaLoggerFunc.tradeInfo('委托收款划回 往账')
                #=====贷方汇总金额====
                AfaLoggerFunc.tradeInfo('委托收款划回 往账__贷方汇总')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='" + PL_BCSTAT_MFESTL + "'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000002' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('委托收款划回 往账__借方汇总')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='" + PL_BCSTAT_MFESTL + "'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000002' and BRSFLG='0' and  DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = trcbka_list[0][0]
                        
                #=====扎差汇总金额====
                AfaLoggerFunc.tradeInfo('委托收款划回 往账__扎差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))   
            
##############################################################################################################################            

            elif( record[i]['TRCCO'] == '2000002' and record[i]['BRSFLG'] == '1' ):
                #=====委托收款划回 来账====
                AfaLoggerFunc.tradeInfo('委托收款划回 来账')
                #=====贷方汇总金额====
                AfaLoggerFunc.tradeInfo('委托收款划回 来账__贷方汇总')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000002' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('委托收款划回 来帐__借方汇总')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000002' and BRSFLG='1' and  DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = trcbka_list[0][0]
                        
                #=====扎差汇总金额====
                AfaLoggerFunc.tradeInfo('委托收款划回 来账__扎差汇总') 
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))   
            
##############################################################################################################################            

            elif( record[i]['TRCCO'] == '2000003' and record[i]['BRSFLG'] == '0' ):
                #=====托收承付划回 往账====
                AfaLoggerFunc.tradeInfo('托收承付划回 往账')
                #=====贷方汇总金额====
                AfaLoggerFunc.tradeInfo('托收承付划回 往账__贷方汇总')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='" + PL_BCSTAT_MFESTL + "'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000003' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('托收承付划回 往账__借方汇总')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='" + PL_BCSTAT_MFESTL + "'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000003' and BRSFLG='0' and  DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = trcbka_list[0][0]
                        
                #=====扎差汇总金额====
                AfaLoggerFunc.tradeInfo('托收承付划回 往账__扎差汇总') 
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))   
            
##############################################################################################################################            

            elif( record[i]['TRCCO'] == '2000003' and record[i]['BRSFLG'] == '1' ):
                #=====托收承付划回 来账====
                AfaLoggerFunc.tradeInfo('托收承付划回 来账')
                #=====贷方汇总金额====
                AfaLoggerFunc.tradeInfo('托收承付划回 来账__贷方汇总')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000003' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('托收承付划回 来账__借方汇总')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000003' and BRSFLG='1' and  DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = trcbka_list[0][0]
                        
                #=====扎差汇总金额====
                AfaLoggerFunc.tradeInfo('托收承付划回 来账__扎差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT))   
            
##############################################################################################################################            
            
            elif( record[i]['TRCCO'] == '2000004' and record[i]['BRSFLG'] == '0' ):
                #=====贷记退汇业务 往账====
                AfaLoggerFunc.tradeInfo('贷记退汇业务 往账')
                #=====贷方汇总金额====
                AfaLoggerFunc.tradeInfo('贷记退汇业务 往账__贷方汇总')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='" + PL_BCSTAT_MFESTL + "'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000004' and BRSFLG='0' and DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('贷记退汇业务 往账__借方汇总')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='" + PL_BCSTAT_MFESTL + "'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000004' and BRSFLG='0' and  DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = trcbka_list[0][0]
                        
                #=====扎差汇总金额====
                AfaLoggerFunc.tradeInfo('贷记退汇业务 往账__扎差汇总') 
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT)) 
            
###############################################################################################################################            
            
            elif( record[i]['TRCCO'] == '2000004' and record[i]['BRSFLG'] == '1' ):
                #=====贷记退汇业务 来账====
                AfaLoggerFunc.tradeInfo('贷记退汇业务 来账')
                #=====贷方汇总金额====
                AfaLoggerFunc.tradeInfo('贷记退汇业务 来账__贷方汇总')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000004' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = trcbka_list[0][0]
                                        
                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('贷记退汇业务 来账__借方汇总')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000004' and BRSFLG='1' and  DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = trcbka_list[0][0]
                        
                #=====扎差汇总金额====
                AfaLoggerFunc.tradeInfo('贷记退汇业务 来账__扎差汇总') 
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT)) 
            
###############################################################################################################################            

            elif( record[i]['TRCCO'] == '2000009' and record[i]['BRSFLG'] == '0' ):
                #=====新旧系统对接 往账====
                AfaLoggerFunc.tradeInfo('新旧系统对接 往账')
                #=====贷方汇总金额====
                AfaLoggerFunc.tradeInfo('新旧系统对接 往账__贷方汇总')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='" + PL_BCSTAT_MFESTL + "'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000009' and BRSFLG='0' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = trcbka_list[0][0]
                        
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('新旧系统对接 往账__借方汇总')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat='" + PL_BCSTAT_MFESTL + "'"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000009' and BRSFLG='0' and  DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = trcbka_list[0][0]
                        
                #=====扎差汇总金额====
                AfaLoggerFunc.tradeInfo('新旧系统对接 往账__扎差汇总')
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT)) 
            
###############################################################################################################################            
            
            elif( record[i]['TRCCO'] == '2000009' and record[i]['BRSFLG'] == '1' ):
                #=====新旧系统对接 来账====
                AfaLoggerFunc.tradeInfo('新旧系统对接 来账')
                #=====贷方汇总金额====
                AfaLoggerFunc.tradeInfo('新旧系统对接 来账__贷方汇总')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000009' and BRSFLG='1' and DCFLG='2' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = trcbka_list[0][0]
                        
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('新旧系统对接 来账__借方汇总')
                
                spbsta_sql = "select BSPSQN from rcc_spbsta where bcstat in('70','71','80')"
                trcbka_sql = "select sum(OCCAMT) from rcc_trcbka where TRCCO='2000009' and BRSFLG='1' and  DCFLG='1' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                trcbka_sql = trcbka_sql + " and BSPSQN in(" + spbsta_sql + ")"
                AfaLoggerFunc.tradeInfo('trcbka_sql为：' + trcbka_sql)
                trcbka_list = AfaDBFunc.SelectSql(trcbka_sql)
                if( trcbka_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(trcbka_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( trcbka_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = trcbka_list[0][0]
                        
                #=====扎差汇总金额====
                AfaLoggerFunc.tradeInfo('新旧系统对接 来账__扎差汇总') 
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                AfaLoggerFunc.tradeInfo('INROFSTAMT为：'+ str(TradeContext.INROFSTAMT)) 
            
###############################################################################################################################            

            
            #====需要从汇兑业务登记簿统计行内汇兑业务金额和总笔数====
            trcbka_sql = "select count(*) from rcc_trcbka where "
            trcbka_sql = trcbka_sql + "NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
 
            #=====判断BRSFLG====
            if str(record[i]['BRSFLG']) != '9':
                trcbka_sql = trcbka_sql + " and BRSFLG='" + record[i]['BRSFLG'] + "'"
            
            #=====判断TRCCO====
            if str(record[i]['TRCCO']) != '0000000':
                trcbka_sql = trcbka_sql + " and TRCCO ='" + record[i]['TRCCO'] + "'"

            #=====根据来往账赋值不同的交易状态====
            if record[i]['BRSFLG'] == PL_BRSFLG_SND:
                #=====联表查询需要特殊处理===
                trcbka_sql = trcbka_sql + " and bspsqn in (select bspsqn from rcc_spbsta where bcstat ='" + PL_BCSTAT_MFESTL + "'"
                trcbka_sql = trcbka_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "')"
            elif record[i]['BRSFLG'] == PL_BRSFLG_RCV:
                trcbka_sql = trcbka_sql + " and bspsqn in (select bspsqn from rcc_spbsta where bcstat in ('70','71','80')"
                trcbka_sql = trcbka_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "')"
            else:
                trcbka_sql = trcbka_sql + " and bspsqn in (select bspsqn from rcc_spbsta where bcstat in ('70','71','42','80')"
                trcbka_sql = trcbka_sql + " and bdwflg='" + PL_BDWFLG_SUCC + "')"
            AfaLoggerFunc.tradeDebug( 'sql==' + trcbka_sql ) 
            
            #=====查询数据库====
            count = AfaDBFunc.SelectSql(trcbka_sql)
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
            filecont = filecont + record[i]['NCCWKDAT']     + "|" + record[i]['TRCCO']            + "|"
            filecont = filecont + record[i]['BRSFLG']       + "|" + record[i]['TRCNAM']           + "|"
            filecont = filecont + record[i]['TRCRSNM']      + "|" + str(record[i]['TCNT'])        + "|"
            filecont = filecont + TradeContext.INRTCNT      + "|"                                 
            filecont = filecont + str(record[i]['CTAMT'])   + "|" + str(TradeContext.INRCTAMT)    + "|"
            filecont = filecont + str(record[i]['DTAMT'])   + "|" + str(TradeContext.INRDTAMT)    + "|"
            filecont = filecont + str(record[i]['OFSTAMT']) + "|" + str(TradeContext.INROFSTAMT)  + "|\n"
            f.write(filecont)

        #=====关闭文件====
        f.close()

    #=====查询总记录数====
    allcount=rccpsDBTrcc_hddzhz.count(sql)     #得到总记录笔数
    if(allcount==None):
        return AfaFlowControl.ExitThisFlow('D000','数据库操作失败')
    else:
        TradeContext.RECALLCOUNT = str(allcount)

    TradeContext.PBDAFILE = filename            #文件名
    TradeContext.RECCOUNT = str(len(record))    #查询笔数
    TradeContext.errorMsg="查询成功"
    TradeContext.errorCode="0000"
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作)交易[TRC001_8546]退出***' )
    return True
