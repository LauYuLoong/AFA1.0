# -*- coding: gbk -*-
##################################################################
#   农信银.查询业务.汇票汇总核对查询
#=================================================================
#   程序文件:   TRCC001_8547.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘雨龙
#   修改时间:   2008-06-12
##################################################################
#   修改者  ：  潘广通
#   修改时间：  2008-09-18
#   修改内容：  行内金额的统计
##################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,rccpsDBTrcc_hpdzhz
import rccpsDBTrcc_bilbka,AfaDBFunc
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '>>>开始汇票汇总核对查询' )
    #=====判断接口是否存在====
    if not TradeContext.existVariable("NCCWKDAT"):
        TradeContext.errorCode = 'N999'
        TradeContext.errorMsg = '中心日期为空'
        return False

    #=====按行号查询====
    sql = "NCCWKDAT = '" + TradeContext.NCCWKDAT + "'"
    #=====查询数据库，得到查询结果集====
    record=rccpsDBTrcc_hpdzhz.selectm(TradeContext.RECSTRNO,10,sql,"")  
    if record == None:
        return AfaFlowControl.ExitThisFlow('D000','数据库操作失败')
    elif len(record) <= 0:
        return AfaFlowControl.ExitThisFlow('D000','没有满足条件的记录')
    else:
        filename = 'rccps_' + TradeContext.BETELR + '_' + AfaUtilTools.GetSysDate() + '_' + TradeContext.TransCode 
        try:
            f=open("/home/maps/afa/tmp/"+filename,"w")
        except IOError:
            AfaLoggerFunc.tradeDebug('打开文件失败')
            return AfaFlowControl.ExitThisFlow('A999','打开文件失败')

        AfaLoggerFunc.tradeDebug( '文件名：' + filename )
        #=====组织返回文件====
        AfaLoggerFunc.tradeDebug( 'start=' + str(record) )
        
        for i in range( 0, len(record) ):
                        
            #=====通过交易代码和往来标示来判断业务种类====
            #=====合计 往账汇总====
            if( record[i]['TRCCO'] == '0000000' and record[i]['BRSFLG'] == '0' ):
                AfaLoggerFunc.tradeInfo('开始合计 往账汇总')
                #=====贷方汇总金额====   
                AfaLoggerFunc.tradeInfo('合计 往账汇总__贷方汇总金额')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(OCCAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sql为：'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRCTAMT =0.00
                    else:
                        TradeContext.INRCTAMT = bilinf_list[0][0]
#                TradeContext.INRCTAMT = 0.00
                
                #=====借方汇总金额====    
                AfaLoggerFunc.tradeInfo('合计 往账汇总__借方汇总金额')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(OCCAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sql为：'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = bilinf_list[0][0]
                        
                
                        
                #=====扎差汇总金额====
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                
                #=====贷方圈存金额====
                AfaLoggerFunc.tradeInfo('合计 往账汇总__贷方圈存金额')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO in('2100001','2100103','2100101') and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilkba_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO in('2100001','2100103','2100101')  and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO in('2100001','2100103','2100101')  and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sql为：'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                AfaLoggerFunc.tradeDebug('bilinf_list[0][0]:'+str(bilinf_list[0][0]))
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRCLAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRCLAMT = 0.00
                    else:
                        TradeContext.INRCLAMT = bilinf_list[0][0]
                #=====借方圈存金额====
                AfaLoggerFunc.tradeInfo('合计 往账汇总__借方圈存金额')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO in('2100001','2100103','2100101') and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilkba_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO in('2100001','2100103','2100101') and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO in('2100001','2100103','2100101') and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sql为：'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                AfaLoggerFunc.tradeDebug('bilinf_list[0][0]:'+str(bilinf_list[0][0]))
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRDLAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRDLAMT = 0.00
                    else:
                        TradeContext.INRDLAMT = bilinf_list[0][0]
                
                #=====扎差圈存金额====
                TradeContext.INROFSLAMT = TradeContext.INRCLAMT - TradeContext.INRDLAMT
                
#======================================================================================================                
            #=====合计 来张汇总====    
            elif( record[i]['TRCCO'] == '0000000' and record[i]['BRSFLG'] == '1' ):
                AfaLoggerFunc.tradeInfo('开始合计 来账汇总')
                
                #=====贷方汇总金额====
                AfaLoggerFunc.tradeInfo('开始合计 来账汇总__贷方汇总金额')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='1' and DCFLG='2' and TRCCO in('2100100') and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='1' and DCFLG='2' and TRCCO in('2100100') and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='1' and DCFLG='2' and TRCCO in('2100100') and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(OCCAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sql为：'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(bilinf_list) == 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = bilinf_list[0][0]
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('开始合计 来账汇总__借方汇总金额')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='1' and DCFLG='1' and TRCCO in('2100100','2100101','2100103') and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='1' and DCFLG='1' and TRCCO in('2100100','2100101','2100103') and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='1' and DCFLG='1' and TRCCO in('2100100','2100101','2100103') and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(OCCAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sql为：'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(bilinf_list) == 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = bilinf_list[0][0]
                
                #=====扎差汇总金额====
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                
                #=====贷方圈存金额====
                AfaLoggerFunc.tradeInfo('开始合计 来账汇总__贷方圈存金额')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='1' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='1' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='1' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sql为：'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(bilinf_list) == 0 ):
                    TradeContext.INRCLAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRCLAMT = 0.00
                    else:
                        TradeContext.INRCLAMT = bilinf_list[0][0]

#                TradeContext.INRCLAMT = 0.00
                        
                #=====借方圈存金额====
                AfaLoggerFunc.tradeInfo('开始合计 来账汇总__借方圈存金额')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='1' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='1' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='1' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sql为：'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(bilinf_list) == 0 ):
                    TradeContext.INRDLAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRDLAMT = 0.00
                    else:
                        TradeContext.INRDLAMT = bilinf_list[0][0]
                
                #=====扎差圈存金额====
                TradeContext.INROFSLAMT = TradeContext.INRCLAMT - TradeContext.INRDLAMT
            
#=============================================================================================================================            
            #=====合计 扎差汇总====
            elif( record[i]['TRCCO'] == '0000000' and record[i]['BRSFLG'] == '9' ):
                AfaLoggerFunc.tradeInfo('开始合计 扎差汇总')
                #=====贷方汇总金额====
                AfaLoggerFunc.tradeInfo('开始合计 扎差汇总__贷方汇总金额')
                bilbka_sql1 = "select BILVER from rcc_bilbka where DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71','42') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71','42') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71','42') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(OCCAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sql为：'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = bilinf_list[0][0]
                
                AfaLoggerFunc.tradeDebug('INRCTAMT为：'+ str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('开始合计 扎差汇总__借方汇总金额')
                bilbka_sql1 = "select BILVER from rcc_bilbka where DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71','42') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71','42') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71','42') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(OCCAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sql为：'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    #=====刘雨龙 20081014====
                    else:
                        TradeContext.INRDTAMT = bilinf_list[0][0]
                        
                AfaLoggerFunc.tradeDebug('INRDTAMT为：'+ str(TradeContext.INRDTAMT))
                        
                #=====扎差汇总金额====
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                
                #=====贷方圈存金额====
                AfaLoggerFunc.tradeInfo('开始合计 扎差汇总__贷方圈存金额')
                bilbka_sql1 = "select BILVER||BILNO||BILRS from rcc_bilbka where DCFLG='1' and TRCCO in('2100100','2100101','2100103') and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71','42') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where DCFLG='1' and TRCCO in('2100100','2100101','2100103') and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71','42') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where DCFLG='1' and TRCCO in('2100100','2100101','2100103') and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71','42') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER||BILNO||BILRS in(" + bilbka_sql1 + ")"
                #bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                #bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sql为：'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(bilinf_list) == 0 ):
                    TradeContext.INRCLAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRCLAMT = 0.00
                    else:
                        TradeContext.INRCLAMT = bilinf_list[0][0]
                        
                AfaLoggerFunc.tradeDebug('INRCTAMT为：'+ str(TradeContext.INRCLAMT))
                        
                #=====借方圈存金额====
                AfaLoggerFunc.tradeInfo('开始合计 扎差汇总__借方圈存金额')
                bilbka_sql1 = "select BILVER from rcc_bilbka where DCFLG='2' and TRCCO='2100001' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71','42') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where DCFLG='2' and TRCCO='2100001' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71','42') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where DCFLG='2' and TRCCO='2100001' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71','42') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sql为：'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(bilinf_list) == 0 ):
                    TradeContext.INRDLAMT = 0.00
                else:
                    if( bilinf_list[0][0] ==None ):
                        TradeContext.INRDLAMT = 0.00
                    else:
                        TradeContext.INRDLAMT = bilinf_list[0][0]
                        
                AfaLoggerFunc.tradeDebug('INRCTAMT为：'+ str(TradeContext.INRDLAMT))
                
                #=====扎差圈存金额====
                TradeContext.INROFSLAMT = TradeContext.INRCLAMT - TradeContext.INRDLAMT
            
#====================================================================================================            
            #=====汇票签发 往帐====
            elif( record[i]['TRCCO'] == '2100001' and record[i]['BRSFLG'] == '0' ):
                AfaLoggerFunc.tradeInfo('开始汇票签发 往账')
                #=====贷方汇总金额====
                TradeContext.INRCTAMT = 0
                
                #=====借方汇总金额====
                TradeContext.INRDTAMT = 0
                        
                #=====扎差汇总金额====
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                
                #=====贷方圈存金额====
                AfaLoggerFunc.tradeInfo('开始汇票签发 往帐__贷方圈存金额')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100001' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100001' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100001' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sql为：'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(bilinf_list) == 0 ):
                    TradeContext.INRCLAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRCLAMT = 0.00
                    else:
                        TradeContext.INRCLAMT = bilinf_list[0][0]
              
                #=====借方圈存金额====
                AfaLoggerFunc.tradeInfo('开始汇票签发 往帐__借方圈存金额')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100001' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100001' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100001' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sql为：'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(bilinf_list) == 0 ):
                    TradeContext.INRDLAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRDLAMT = 0.00
                    else:
                        TradeContext.INRDLAMT = bilinf_list[0][0]
#                TradeContext.INRDLAMT = 0.00
                
                #=====扎差圈存金额====
                TradeContext.INROFSLAMT = TradeContext.INRCLAMT - TradeContext.INRDLAMT
            
#===================================================================================================            
            #=====汇票解付 往帐====
            elif( record[i]['TRCCO'] == '2100100' and record[i]['BRSFLG'] == '0' ):
                AfaLoggerFunc.tradeInfo('汇票解付 往账汇总')
                #=====贷方汇总金额====
                AfaLoggerFunc.tradeInfo('汇票解付 往账汇总__贷方汇总金额')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(OCCAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sql为：'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = bilinf_list[0][0]

#                TradeContext.INRCTAMT = 0.00
                        
                AfaLoggerFunc.tradeDebug('INRCTAMT为：'+ str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('汇票解付 往账__借方汇总金额')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(OCCAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sql为：'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = bilinf_list[0][0]
                        
                #=====扎差汇总金额====
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                
                #=====贷方圈存金额====
                TradeContext.INRCLAMT = 0.00
                
                #=====借方圈存金额====
                TradeContext.INRDLAMT = 0.00
                
                #=====扎差圈存金额====
                TradeContext.INROFSLAMT = TradeContext.INRCLAMT - TradeContext.INRDLAMT
                
#===========================================================================================================           
            #=====汇票解付 来账====
            elif( record[i]['TRCCO'] == '2100100' and record[i]['BRSFLG'] == '1' ):
                AfaLoggerFunc.tradeInfo('开始汇票解付 来账')
                #=====贷方汇总金额====
                AfaLoggerFunc.tradeInfo('汇票解付 来账__贷方汇总金额')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='1' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='1' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='1' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(OCCAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sql为：'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRCTAMT = 0.00
                    else:
                        TradeContext.INRCTAMT = bilinf_list[0][0]
                
                AfaLoggerFunc.tradeDebug('INRCTAMT为：'+  str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                AfaLoggerFunc.tradeInfo('汇票解付 来账__借方汇总金额')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='1' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='1' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='1' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(OCCAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sql为：'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRDTAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRDTAMT = 0.00
                    else:
                        TradeContext.INRDTAMT = bilinf_list[0][0]

                #=====扎差汇总金额====
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                
                #=====贷方圈存金额====
                AfaLoggerFunc.tradeInfo('汇票解付 来账__贷方圈存金额')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='1' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='1' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='1' and DCFLG='1' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sql为：'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRCLAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRCLAMT = 0.00
                    else:
                        TradeContext.INRCLAMT = bilinf_list[0][0]

#                TradeContext.INRCLAMT = 0.00
                        
                AfaLoggerFunc.tradeDebug('INRCLAMT为：' + str(TradeContext.INRCLAMT))
                
                #=====借方圈存金额====
                AfaLoggerFunc.tradeInfo('汇票解付 来账__借方圈存金额')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='1' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='1' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='1' and DCFLG='2' and TRCCO='2100100' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT in('70','71') and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sql为：'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRDLAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRDLAMT = 0.00
                    else:
                        TradeContext.INRDLAMT = bilinf_list[0][0]
                TradeContext.INRDLAMT = 0.00
                
                #=====扎差圈存金额====
                TradeContext.INROFSLAMT = TradeContext.INRCLAMT - TradeContext.INRDLAMT

#==================================================================================================================                
            #=====汇票撤销 往帐====
            elif( record[i]['TRCCO'] == '2100101' and record[i]['BRSFLG'] == '0' ):
                AfaLoggerFunc.tradeInfo('开始汇票撤销 往账')
                #=====贷方汇总金额====
                AfaLoggerFunc.tradeInfo('汇票撤销 往账__贷方汇总金额')
#                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100101' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
#                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
#                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100101' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
#                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
#                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100101' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
#                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
#                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
#                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
#                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
#                AfaLoggerFunc.tradeInfo('bilinf_sql为：'+ bilinf_sql)
#                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
#                if( bilinf_list == None ):
#                    f.close()
#                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
#                elif( len(bilinf_list) <= 0 ):
#                    TradeContext.INRCTAMT = 0.00
#                else:
#                    if( bilinf_list[0][0] == None ):
#                        TradeContext.INRCTAMT = 0.00
#                    else:
#                        TradeContext.INRCTAMT = bilinf_list[0][0]

                TradeContext.INRCTAMT = 0.00
                
                AfaLoggerFunc.tradeDebug('INRCTAMT为：'+ str(TradeContext.INRCTAMT))
                
                #=====借方汇总金额====
                TradeContext.INRDTAMT = 0.00
                        
                #=====扎差汇总金额====
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                
                #=====贷方圈存金额====
                AfaLoggerFunc.tradeInfo('汇票撤销 往账__借方圈存金额')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100101' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100101' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100101' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sql为：'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRCLAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRCLAMT = 0.00
                    else:
                        TradeContext.INRCLAMT = bilinf_list[0][0]
#                TradeContext.INRCLAMT = 0.00
                
                #=====借方圈存金额====
                AfaLoggerFunc.tradeInfo('汇票撤销 往账__借方圈存金额')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100101' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100101' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100101' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sql为：'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRDLAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRDLAMT = 0.00
                    else:
                        TradeContext.INRDLAMT = bilinf_list[0][0]
                
                #=====扎差圈存金额====
                TradeContext.INROFSLAMT = TradeContext.INRCLAMT - TradeContext.INRDLAMT

#==========================================================================================================
            #=====汇票退票 往账====
            elif( record[i]['TRCCO'] == '2100103' and record[i]['BRSFLG'] == '0' ):
                AfaLoggerFunc.tradeInfo('开始汇票退票 往账')
                #=====贷方汇总金额====
                AfaLoggerFunc.tradeInfo('汇票退票 往账汇总__贷方汇总金额')
#                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100103' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
#                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
#                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100103' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
#                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
#                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100103' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
#                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
#                bilinf_sql = "select sum(OCCAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
#                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
#                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
#                AfaLoggerFunc.tradeInfo('bilinf_sql为：'+ bilinf_sql)
#                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
#                if( bilinf_list == None ):
#                    f.close()
#                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
#                elif( len(bilinf_list) <= 0 ):
#                    TradeContext.INRCTAMT = 0.00
#                else:
#                    if( bilinf_list[0][0] == None ):
#                        TradeContext.INRCTAMT = 0.00
#                    else:
#                        TradeContext.INRCTAMT = bilinf_list[0][0]
#                        
#                AfaLoggerFunc.tradeInfo('INRCTAMT为：'+ str(TradeContext.INRCTAMT))
                TradeContext.INRCTAMT = 0.00
                
                #=====借方汇总金额====
                TradeContext.INRDTAMT = 0.00
                        
                #=====扎差汇总金额====
                TradeContext.INROFSTAMT = TradeContext.INRCTAMT - TradeContext.INRDTAMT
                
                #=====贷方圈存金额====
                AfaLoggerFunc.tradeInfo('汇票退票 往账汇总__贷方圈存金额')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100103' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100103' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='1' and TRCCO='2100103' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sql为：'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRCTAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRCLAMT = 0.00
                    else:
                        TradeContext.INRCLAMT = bilinf_list[0][0]

#                TradeContext.INRCLAMT = 0.00
                        
                AfaLoggerFunc.tradeDebug('INRCLAMT为：'+ str(TradeContext.INRCLAMT))

                
                #=====借方圈存金额====
                AfaLoggerFunc.tradeInfo('汇票退票 往账__借方圈存金额')
                bilbka_sql1 = "select BILVER from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100103' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql1 = bilbka_sql1 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql2 = "select BILNO from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100103' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql2 = bilbka_sql2 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilbka_sql3 = "select BILRS from rcc_bilbka where BRSFLG='0' and DCFLG='2' and TRCCO='2100103' and NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
                bilbka_sql3 = bilbka_sql3 + " and BSPSQN in(select BSPSQN from rcc_spbsta where BCSTAT='" + PL_BCSTAT_MFESTL + "' and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                bilinf_sql = "select sum(BILAMT) from rcc_bilinf where BILVER in(" + bilbka_sql1 + ")"
                bilinf_sql = bilinf_sql + " and BILNO in(" + bilbka_sql2 + ")"
                bilinf_sql = bilinf_sql + " and BILRS in(" + bilbka_sql3 + ")"
                bilinf_sql = bilinf_sql + " with ur "
                AfaLoggerFunc.tradeDebug('bilinf_sql为：'+ bilinf_sql)
                bilinf_list = AfaDBFunc.SelectSql(bilinf_sql)
                if( bilinf_list == None ):
                    f.close()
                    return AfaFlowControl.ExitThisFlow('D000','汇票信息登记簿操作失败')
                elif( len(bilinf_list) <= 0 ):
                    TradeContext.INRDLAMT = 0.00
                else:
                    if( bilinf_list[0][0] == None ):
                        TradeContext.INRDLAMT = 0.00
                    else:
                        TradeContext.INRDLAMT = bilinf_list[0][0]
                
                #=====扎差圈存金额====
                TradeContext.INROFSLAMT = TradeContext.INRCLAMT - TradeContext.INRDLAMT
            
#==========================================================================================================================================                
            AfaLoggerFunc.tradeInfo('行内汇总扎差额为：'+str(TradeContext.INROFSTAMT))
           
            #=====计算行内总比数====
            AfaLoggerFunc.tradeInfo('开始计算行内总比数')
            #=====组织查询bilbka的查询语句====
            bilbka_sql = ""
            bilbka_sql = "select count(*) from rcc_bilbka where "           
            bilbka_sql = bilbka_sql + "NCCWKDAT='" + record[i]['NCCWKDAT'] + "'"
            
            if record[i]['TRCCO'] == '0000000':
                bilbka_sql = bilbka_sql + " and TRCCO in ('2100001','2100100','2100101','2100103')"
            else:
                bilbka_sql = bilbka_sql + " and TRCCO='" + record[i]['TRCCO'] + "'"
                
            if record[i]['BRSFLG'] == '9':
                bilbka_sql = bilbka_sql + " and BRSFLG in ('1','0')"
            else:
                bilbka_sql = bilbka_sql + " and BRSFLG='" + record[i]['BRSFLG'] + "'"
                
            if( record[i]['BRSFLG'] == PL_BRSFLG_SND ):
                bilbka_sql = bilbka_sql + " and bspsqn in (select bspsqn from rcc_spbsta where bcstat='" + PL_BCSTAT_MFESTL + "'"
                bilbka_sql = bilbka_sql + " and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                
            elif( record[i]['BRSFLG'] == PL_BRSFLG_RCV ):
                bilbka_sql = bilbka_sql + " and bspsqn in (select bspsqn from rcc_spbsta where bcstat in('70','71')"
                bilbka_sql = bilbka_sql + " and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                
            else:
                bilbka_sql = bilbka_sql + " and bspsqn in (select bspsqn from rcc_spbsta where bcstat in('70','71','42')"
                bilbka_sql = bilbka_sql + " and BDWFLG='" + PL_BDWFLG_SUCC + "')"
                
            bilinf_sql = bilinf_sql + " with ur "
            AfaLoggerFunc.tradeDebug( 'SQLl==' + bilbka_sql )
            #count = rccpsDBTrcc_bilbka.count(bilbka_sql)
            AfaLoggerFunc.tradeDebug("<<<查询总比数")
            count = AfaDBFunc.SelectSql(bilbka_sql)
            if count == None:
                f.close()
                return AfaFlowControl.ExitThisFlow('D000','查询总比数失败')
            else:
                TradeContext.INRTCNT = str(count[0][0])                  
            AfaLoggerFunc.tradeDebug( '行内总笔数=' + TradeContext.INRTCNT )
            
            #=====开始组织文件内容====
            filecont = ''
            filecont = filecont + record[i]['NCCWKDAT']         + "|" + record[i]['TRCCO']           + "|"
            filecont = filecont + record[i]['BRSFLG']           + "|" + record[i]['TRCNAM']          + "|"
            filecont = filecont + record[i]['TRCRSNM']          + "|" + str(record[i]['TCNT'])       + "|"
            filecont = filecont + TradeContext.INRTCNT          + "|"
            filecont = filecont + str(record[i]['CTAMT'])       + "|" + str(record[i]['CLAMT'])      + "|"
            filecont = filecont + str(TradeContext.INRCTAMT)    + "|" + str(TradeContext.INRCLAMT)   + "|"
            filecont = filecont + str(record[i]['DTAMT'])       + "|" + str(record[i]['DLAMT'])      + "|"
            filecont = filecont + str(TradeContext.INRDTAMT)    + "|" + str(TradeContext.INRDLAMT)   + "|"
            filecont = filecont + str(record[i]['OFSTAMT'])     + "|" + str(record[i]['OFSLAMT'])    + "|"
            filecont = filecont + str(TradeContext.INROFSTAMT)  + "|" + str(TradeContext.INROFSLAMT) + "|\n"
            AfaLoggerFunc.tradeDebug( '文件内容=' + filecont )

            #=====写入文件====
            f.write(filecont)
            
        #=====关闭文件====
        f.close()

    #=====查询总记录数====
    allcount=rccpsDBTrcc_hpdzhz.count(sql)     #得到总记录笔数
    if(allcount==None):
        return AfaFlowControl.ExitThisFlow('D000','数据库操作失败')
    else:
        TradeContext.RECALLCOUNT = str(allcount)

    TradeContext.PBDAFILE = filename 
    TradeContext.RECCOUNT = str(len(record))
    TradeContext.errorMsg="查询成功"
    TradeContext.errorCode="0000"
    
    return True
