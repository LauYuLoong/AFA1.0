# -*- coding: gbk -*-
###############################################################################
# Copyright (c) 2006,北京赞同科技发展有限公司.第三事业部
# All rights reserved.
#
# 文件名称：TPS001_8455.py
# 文件标识：
# 摘    要：财税库行.查询交易明细
#
# 当前版本：1.0
# 作    者：
# 完成日期：2006年12月05日
#
# 取代版本：
# 原 作 者：
# 完成日期：
###############################################################################
import TradeContext, AfaDBFunc,AfaLoggerFunc
import  TipsFunc,os
#LoggerHandler, UtilTools,  UtilTools,
def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo( '进入查询交易明细['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']'  )

    try:
        sqlstr = "SELECT SERIALNO,WORKDATE,TAXPAYCODE,TAXPAYNAME,DRACCNO,AMOUNT,BANKSTATUS,BANKSERNO,CORPSTATUS,CORPSERNO,ERRORMSG FROM TIPS_MAINTRANSDTL WHERE 1=1 "
        #网点限制
        if not QueryBrno(TradeContext.brno):
            sqlstr = sqlstr + " AND BRNO='"     +  TradeContext.brno   + "'"
        else:
            sqlstr = sqlstr + " AND NOTE3='"     +  TradeContext.PayBkCode   + "'"    
            
        if( TradeContext.existVariable('serNo') and len(TradeContext.serNo) > 0 ):
             sqlstr = sqlstr + " AND SERIALNO='"     +  TradeContext.serNo   + "'"
        else:
            sqlstr = sqlstr + " AND REVTRANF='" +  "0"                     + "'"
        
            sqlstr = sqlstr + " AND WORKDATE BETWEEN '" + TradeContext.beginDate + "' AND '"+ TradeContext.endDate+"'"
        
            if ( TradeContext.existVariable('transStatus') and len(TradeContext.transStatus) > 0 ):
                if ( TradeContext.transStatus=='1' ):              #成功
                    AfaLoggerFunc.tradeInfo('>>>查询成功流水')
                    sqlstr = sqlstr + " AND BANKSTATUS='0'"
                    sqlstr = sqlstr + " AND CORPSTATUS='0'"
        
                elif ( TradeContext.transStatus=='2' ):            #失败
                    AfaLoggerFunc.tradeInfo('>>>查询失败流水')
                    sqlstr = sqlstr + " AND BANKSTATUS='1'"
        
                elif ( TradeContext.transStatus=='3' ):            #异常
                    AfaLoggerFunc.tradeInfo('>>>查询异常流水')
                    sqlstr = sqlstr + " AND ( BANKSTATUS='2'"
                    sqlstr = sqlstr + " OR (BANKSTATUS='0' AND CORPSTATUS='1')"
                    sqlstr = sqlstr + " OR (BANKSTATUS='0' AND CORPSTATUS='2') )"
        
                else:
                    AfaLoggerFunc.tradeInfo('>>>查询全部流水')
                    
            if ( TradeContext.existVariable('transChannel') and len(TradeContext.transChannel) > 0 ):
                if ( TradeContext.transChannel=='1' ):              #柜面缴费
                    AfaLoggerFunc.tradeInfo('>>>柜面缴费')
                    sqlstr = sqlstr + " AND TRADETYPE='1'"
        
                elif ( TradeContext.transChannel=='7' ):            #第三方实时缴费
                    AfaLoggerFunc.tradeInfo('>>>第三方实时缴费')
                    sqlstr = sqlstr + " AND TRADETYPE='7'"
        
                elif ( TradeContext.transChannel=='8' ):            #第三方批量缴费
                    AfaLoggerFunc.tradeInfo('>>>第三方批量缴费')
                    sqlstr = sqlstr + " AND TRADETYPE='8'"
        
                else:
                    AfaLoggerFunc.tradeInfo('>>>全部')
        
            if ( TradeContext.existVariable('userno') and len(TradeContext.userno) > 0 ):
                sqlstr = sqlstr + " AND TAXPAYCODE='" + TradeContext.userno + "'"
        
        AfaLoggerFunc.tradeInfo(sqlstr)
    
        records = AfaDBFunc.SelectSql( sqlstr )
        if ( records==None or len(records) == 0 ):
            return TipsFunc.ExitThisFlow('A0001', '无交易明细')
    
        else:
            AfaLoggerFunc.tradeInfo('总共有[' + str(len(records)) + ']条流水')
    
        mx_file_name = os.environ['AFAP_HOME'] + '/tmp/' + 'AH_' + TradeContext.teller + '.txt'
        TradeContext.tradeResponse.append(['fileName',  'AH_' + TradeContext.teller + '.txt'])
    
        if (os.path.exists(mx_file_name) and os.path.isfile(mx_file_name)):
            #文件存在,先删除-再创建
            os.system("rm " + mx_file_name)
    
        sfp = open(mx_file_name, "w")
        AfaLoggerFunc.tradeInfo('明细文件=['+mx_file_name+']')
    
        i = 0
        while ( i  < len(records) ):
            A0 = str(records[i][0]).strip()         #SERIALNO
            A1 = str(records[i][1]).strip()         #WORKDATE
            A2 = str(records[i][2]).strip()         #USERNO
            A3 = str(records[i][3]).strip()         #USERNAME
            A4 = str(records[i][4]).strip()         #ACCNO
            A5 = str(records[i][5]).strip()         #AMOUNT
            A6 = str(records[i][6]).strip()         #BANKSTATUS
            A7 = str(records[i][7]).strip()         #SERIALNO
            A8 = str(records[i][8]).strip()         #CORPSTATUS
            A9 = str(records[i][9]).strip()         #CORPSERNO
            A10 = str(records[i][10]).strip()         #ERRORMSG
            
            sfp.write(A0 +  '|'  +  A1 +  '|'  +  A2 +  '|'  +  A3 +  '|'  +  A4 +  '|'  +  A5 +  '|'  +  A6  +  '|'  +  A7 +  '|' +  A8 +  '|'+  A9 +  '|' +  A10 +  '|' + '\n')
    
            i=i+1
    
        sfp.close()
    
        TradeContext.tradeResponse.append(['errorCode',  '0000'])
        TradeContext.tradeResponse.append(['errorMsg',   '交易成功'])
        return True
    except TipsFunc.flowException, e:
        return TipsFunc.ExitThisFlow('9999',str(e))

def QueryBrno(brno):
    AfaLoggerFunc.tradeInfo('查询机构对应的付款行号')
    sql="select brno,paybkcode from TIPS_BRANCH_ADM where brno='"+brno+"'"
    AfaLoggerFunc.tradeInfo(sql)
    records=AfaDBFunc.SelectSql(sql)
    if records==None:
        return False
    elif(len(records)==0):
        return False
    else:
        TradeContext.PayBkCode=records[0][1]
        return True
        
    
    