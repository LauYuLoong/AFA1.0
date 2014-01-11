# -*- coding: gbk -*-
###############################################################################
# Copyright (c) 2006,北京赞同科技发展有限公司.应用开发II部
# All rights reserved.
#
# 文件名称：T003001_038504.py
# 文件标识：
# 摘    要：财税库行.对账查询
#   queryType 查询类别 0.合计数 1.对账成功明细 2.对账差异明细 
# 当前版本：1.0
# 作    者：
# 完成日期：2006年12月05日
#
# 取代版本：
# 原 作 者：
# 完成日期：
###############################################################################
import TradeContext, AfaDBFunc,AfaLoggerFunc,ConfigParser,os,TipsFunc
import UtilTools
def SubModuleMainFst( ):
    try:
        #检查机构状态,获取付款行号,收款行号
        if not TipsFunc.ChkBranchStatus():
            return TipsFunc.ExitThisFlow( 'A0027', '检查机构状态失败' )
        if not TipsFunc.ChkLiquidStatus():
            return TipsFunc.ExitThisFlow( 'A0027', '检查清算国库信息失败' )
        
        sqlStr = "SELECT BATCHNO,WORKTIME,DEALSTATUS,ERRORMSG,PAYBKCODE,PAYEEBANKNO,CHKACCTTYPE,PRIORCHKACCTORD,TOTALNUM,TOTALAMT FROM TIPS_CHECKADM WHERE "
        sqlStr = sqlStr +" WORKDATE  = '" + TradeContext.checkDate.strip()   + "'"
        sqlStr = sqlStr +" AND BATCHNO = '"      + TradeContext.checkNo.strip()     + "'"
        sqlStr = sqlStr +" AND PAYBKCODE = '"    + TradeContext.payBkCode.strip()   + "'"
        sqlStr = sqlStr +" and PAYEEBANKNO  = '" + TradeContext.payeeBankNo.strip()      + "'"
        if TradeContext.brno != TradeContext.__mainBrno__: #业务清算行
            sqlStr = sqlStr + " AND BRNO ='"  + TradeContext.brno  + "'"
        Records = AfaDBFunc.SelectSql( sqlStr )
        AfaLoggerFunc.tradeInfo(sqlStr)
        if( Records == None ):
            AfaLoggerFunc.tradeFatal('批量管理表操作异常:'+AfaDBFunc.sqlErrMsg)
            return TipsFunc.ExitThisFlow( 'A0027', '数据库错，批量管理表操作异常' )
        elif(len(Records)==0):
            return TipsFunc.ExitThisFlow( 'A0027', '无此批次' )
        else:
            TradeContext.tradeResponse.append(['bNo'    ,str(Records[0][0])])           #对账批次号
            TradeContext.tradeResponse.append(['wTime'  ,str(Records[0][1])])           #处理时间
            TradeContext.tradeResponse.append(['dSta'   ,str(Records[0][2])])           #批次状态
            TradeContext.tradeResponse.append(['errM'   ,str(Records[0][3])])           #批次处理结果
            TradeContext.tradeResponse.append(['PBk'    ,str(Records[0][4])])           #付款行号
            TradeContext.tradeResponse.append(['PBkN'   ,''])       #付款行名称
            TradeContext.tradeResponse.append(['PeBk'   ,str(Records[0][5])])           #收款行号
            TradeContext.tradeResponse.append(['PeBkN'  ,''])           #收款行名称
            TradeContext.tradeResponse.append(['chkType',str(Records[0][6])])           #对账批次类型
            TradeContext.tradeResponse.append(['pBNo'   ,str(Records[0][7])])           #上一对账批次
            TradeContext.payeeBankNo=Records[0][5]
            #合计        
            if not sumall():
                return False
                
    
        #写入文件
        mx_file_name = os.environ['AFAP_HOME'] + '/tmp/' + 'AH_' + TradeContext.teller + '.txt'
        TradeContext.tradeResponse.append(['fileName',  'AH_' + TradeContext.teller + '.txt'])
        
        if (os.path.exists(mx_file_name) and os.path.isfile(mx_file_name)):
            #文件存在,先删除-再创建
            os.system("rm " + mx_file_name)
        
        sfp = open(mx_file_name, "w")
        AfaLoggerFunc.tradeInfo('明细文件=['+mx_file_name+']')
        
        #明细
        sqlStr = ''
        sqlStr = sqlStr + "WHERE NOTE1 ='" +TradeContext.checkDate +"'"
        sqlStr = sqlStr + " AND NOTE2 = '" +TradeContext.checkNo   +"'"
        sqlStr = sqlStr + " AND NOTE3 ='"  + TradeContext.payBkCode.strip()  + "'"   
        sqlStr = sqlStr + " AND NOTE4 ='"  + TradeContext.payeeBankNo.strip()  + "'"
        if TradeContext.brno != TradeContext.__mainBrno__: #业务清算行
            sqlStr = sqlStr + " AND BRNO ='"  + TradeContext.brno  + "'"
        sqlStr=sqlStr+" AND (CHKFLAG!='9'  and  CORPCHKFLAG='9' or CHKFLAG!='0'  and  CORPCHKFLAG='0')"
        sqlStr=sqlStr+" ORDER BY SERIALNO"
        sqlStr_detail="SELECT WORKDATE,DRACCNO,TAXPAYCODE,cast(AMOUNT as decimal(17,2)),SERIALNO,CORPSERNO,CHKFLAG,CORPCHKFLAG FROM TIPS_MAINTRANSDTL  "
        sqlStr_detail=sqlStr_detail+sqlStr
        AfaLoggerFunc.tradeInfo(sqlStr_detail)
        Records = AfaDBFunc.SelectSql( sqlStr_detail )
        if( Records == None or Records <0):
            sfp.close()
            return TipsFunc.ExitThisFlow( 'A0027', '表操作异常:'+AfaDBFunc.sqlErrMsg )
        elif( len( Records )==0 ):
            sfp.close()
            return TipsFunc.ExitThisFlow( 'A0027', '没有满足条件的数据' )
        else:
            for i in range(0,len(Records)):
                A0 = str(Records[i][0]).strip()         #WORKDATE
                A1 = str(Records[i][1]).strip()         #ACCNO        
                A2 = str(Records[i][2]).strip()         #USERNO       
                A3 = str(Records[i][3]).strip()         #AMOUNT       
                A4 = str(Records[i][4]).strip()         #SERIALNO
                A5 = str(Records[i][5]).strip()         #CORPSERIALNO
                if (Records[i][6]=='0' and Records[i][7]=='0'):
                    A6 = "对账成功"
                elif (Records[i][6]!='9' and Records[i][7]=='9'):
                    A6 = "银行比人行多"
                elif (Records[i][6]!='0' and Records[i][7]=='0'):
                    A6 = "人行比银行多"
                
                sfp.write(A0 +  '|'  +  A1 +  '|'  +  A2 +  '|'  +  A3 +  '|'  +  A4 +  '|'  +  A5 +  '|'  +  A6  +  '|' + '\n')
                
        sfp.close()                
        TradeContext.tradeResponse.append(['errorCode','0000'])
        TradeContext.tradeResponse.append(['errorMsg','交易成功'])

        AfaLoggerFunc.tradeInfo( '退出对账查询[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        return True
    except TipsFunc.flowException, e:
        # print e        
        TipsFunc.exitMainFlow( )
        
    except Exception, e:
        # print e
        TipsFunc.exitMainFlow(str(e))

#查询对账成功，差异笔数和金额
def sumall():       
    #成功总计
    AfaLoggerFunc.tradeInfo('查询对账成功，差异笔数和金额')
    sumsql="SELECT count(*),sum(cast(amount as decimal(17,2))) "
    sumsql = sumsql + "FROM TIPS_MAINTRANSDTL  "
    sumsql = sumsql + "WHERE NOTE1 ='"+TradeContext.checkDate+"'"
    sumsql = sumsql + " AND NOTE2 = '"+TradeContext.checkNo+"'"
    sumsql = sumsql + " AND CHKFLAG='0' and CORPCHKFLAG='0'"
    sumsql = sumsql + " AND NOTE3='"  + TradeContext.payBkCode.strip()  + "'"   
    sumsql = sumsql + " AND NOTE4='"  + TradeContext.payeeBankNo.strip()  + "'"
    sumSucc=AfaDBFunc.SelectSql( sumsql)
    AfaLoggerFunc.tradeInfo(sumsql)
    AfaLoggerFunc.tradeInfo("成功总计"+repr(sumSucc))
    if( sumSucc == None or sumSucc < 0 ):
        # None 查询失败
        return TipsFunc.ExitThisFlow( 'A0025', '数据库操作错误 统计成功笔数出错!'+AfaDBFunc.sqlErrMsg  )
    #差异总计
    sumsql="SELECT count(*),sum(cast(amount as decimal(17,2))) "
    sumsql = sumsql + "FROM TIPS_MAINTRANSDTL  "
    sumsql = sumsql + "WHERE NOTE1 ='"+TradeContext.checkDate+"'"
    sumsql = sumsql + " AND  NOTE2 = '"+TradeContext.checkNo+"'"
    sumsql = sumsql + " AND (CHKFLAG!='9'  and  CORPCHKFLAG='9' or CHKFLAG!='0'  and  CORPCHKFLAG='0')"
    sumsql = sumsql + " AND  NOTE3='"  + TradeContext.payBkCode.strip()  + "'"   
    sumsql = sumsql + " AND NOTE4='"  + TradeContext.payeeBankNo.strip()  + "'"
    AfaLoggerFunc.tradeInfo(sumsql)
    sumFail=AfaDBFunc.SelectSql( sumsql)
    AfaLoggerFunc.tradeInfo("差异总计"+repr(sumFail))
    if( sumFail == None or sumFail < 0):
        # None 查询失败
        return TipsFunc.ExitThisFlow( 'A0025', '数据库操作错误 统计差异笔数出错!' +AfaDBFunc.sqlErrMsg  )
    sumSucc=UtilTools.ListFilterNone(sumSucc,0)
    sumFail=UtilTools.ListFilterNone(sumFail,0)
    TradeContext.tradeResponse.append( ['sSum', str(sumSucc[0][0])] )  
    TradeContext.tradeResponse.append( ['sAmt', str(sumSucc[0][1])] )
    TradeContext.tradeResponse.append( ['fSum', str(sumFail[0][0])] )  
    TradeContext.tradeResponse.append( ['fAmt', str(sumFail[0][1])] )  
    return True
    
