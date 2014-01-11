# -*- coding: gbk -*-
##################################################################
#   中间业务平台.TIPS发起明细对账
#=================================================================
#      9  初始
#      2  处理中
#      3  第三方对帐完成
#      4  核心对帐完成
#      0  处理成功
#      1  处理失败
#   程序文件:   TPS001_845004.py
#   修改时间:   2008-12-18 9:41
##################################################################
import TradeContext, AfaLoggerFunc, TipsFunc
import AfaDBFunc
#,datetime,ConfigParser,os,UtilTools,
from types import *

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('财税库行_TIPS发起明细对账_前处理[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
        #============变量值的有效性校验============
        if( not TradeContext.existVariable( "chkAcctOrd" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '[chkAcctOrd]值不存在!' )
        if( not TradeContext.existVariable( "chkDate" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '[chkDate]值不存在!' )
        
        #====判断应用状态=======
        if not TipsFunc.ChkAppStatus():
            return False
                   
        #查询是否重复批次
        AfaLoggerFunc.tradeInfo( '>>>查询是否重复批次' )
        sqlStr = "SELECT DEALSTATUS,WORKDATE,BATCHNO,PAYBKCODE,PAYEEBANKNO,ERRORCODE,ERRORMSG,NOTE2 FROM TIPS_CHECKADM WHERE "
        sqlStr =sqlStr +"  WORKDATE  = '"       + TradeContext.chkDate.strip()         + "'"
        sqlStr =sqlStr +"and BATCHNO   = '"     + TradeContext.chkAcctOrd.strip()      + "'"
        sqlStr =sqlStr +"and PAYEEBANKNO   = '" + TradeContext.payeeBankNo.strip()      + "'"
        sqlStr =sqlStr +"and PAYBKCODE   = '"   + TradeContext.payBkCode.strip()      + "'"
        sqlStr =sqlStr +"and NOTE3   = '"   + TradeContext.CurPackNo.strip()      + "'"
        
        Records = AfaDBFunc.SelectSql( sqlStr )
        AfaLoggerFunc.tradeInfo(sqlStr)
        if( Records == None ):
            AfaLoggerFunc.tradeFatal('批量管理表操作异常:'+AfaDBFunc.sqlErrMsg)
            return TipsFunc.ExitThisFlow( 'A0027', '数据库错，批量管理表操作异常' )
        elif(len(Records)>0):
            if Records[0][0]=='2': #重复包，且正在处理
                AfaLoggerFunc.tradeInfo( '>>>重复包，且正在处理，直接返回94052' )
                TradeContext.tradeResponse.append(['errorCode','94052'])
                TradeContext.tradeResponse.append(['errorMsg','包重复'])
                return True
            elif Records[0][0]=='0' : #已处理完成，成功或者失败，直接回执
                #发起扣税回执交易
                AfaLoggerFunc.tradeInfo( '>>>已处理完成，成功或者失败，直接回执2111' )
                TradeContext.OriChkDate    =Records[0][1]
                TradeContext.OriChkAcctOrd =Records[0][2]
                TradeContext.OriPayBankNo  =Records[0][3]
                TradeContext.OriPayeeBankNo=Records[0][4]
                TradeContext.Result        =Records[0][5]
                TradeContext.AddWord       =Records[0][6]
                subModuleName = 'TTPS001_032111'       
                subModuleHandle=__import__( subModuleName )
                AfaLoggerFunc.tradeInfo( '执行['+subModuleName+']模块' )
                if not subModuleHandle.SubModuleMainFst( ) :
                    return TipsFunc.flowException( )
                TradeContext.tradeResponse.append(['errorCode','94052'])
                TradeContext.tradeResponse.append(['errorMsg','批次已处理完成'])
                return True
            else: #重复包，重新对账
                AfaLoggerFunc.tradeInfo( '>>>重复包，重新对账' )
                if int(TradeContext.pageSerno.strip())==1:
                    #尚未处理的重复批次，按新批次处理，删掉旧数据
                    sqlStr_d_t = "DELETE FROM  TIPS_CHECKDATA WHERE "
                    sqlStr_d_t = sqlStr_d_t +"  workDate  = '"      + TradeContext.chkDate              + "'"
                    sqlStr_d_t = sqlStr_d_t +" and Batchno   = '"   + TradeContext.chkAcctOrd           + "'"
                    sqlStr_d_t = sqlStr_d_t +" AND PAYEEBANKNO ='"  + TradeContext.payeeBankNo.strip()    + "'"   
                    sqlStr_d_t = sqlStr_d_t +" AND PAYBKCODE   ='"  + TradeContext.payBkCode.strip()  + "'"
                    sqlStr_d_t = sqlStr_d_t +" AND NOTE3   = '"     + TradeContext.CurPackNo.strip()  + "'"
                    AfaLoggerFunc.tradeInfo(sqlStr_d_t )
                    if( AfaDBFunc.DeleteSqlCmt( sqlStr_d_t ) <0 ):
                        return TipsFunc.ExitThisFlow( 'A0027', '数据库错，批量管理表操作异常' )
                    sqlStr_d_b = "DELETE FROM  TIPS_CHECKADM WHERE "
                    sqlStr_d_b =sqlStr_d_b +" WORKDATE  = '"        + TradeContext.chkDate.strip()     + "'"
                    sqlStr_d_b =sqlStr_d_b +"and BATCHNO   = '"     + TradeContext.chkAcctOrd.strip()  + "'"
                    sqlStr_d_b =sqlStr_d_b +"and PAYEEBANKNO   = '" + TradeContext.payeeBankNo.strip() + "'"
                    sqlStr_d_b =sqlStr_d_b +"and PAYBKCODE     = '" + TradeContext.payBkCode.strip()   + "'"
                    sqlStr_d_b =sqlStr_d_b +"and NOTE3     = '"     + TradeContext.CurPackNo.strip()   + "'"
                    AfaLoggerFunc.tradeInfo(sqlStr_d_b )
                    if( AfaDBFunc.DeleteSqlCmt( sqlStr_d_b ) <0 ):
                        return TipsFunc.ExitThisFlow( 'A0027', '数据库错，批量管理表操作异常' )
                else:
                    if int(TradeContext.pageSerno.strip())!=int(Records[0][7].strip())+1:
                        #页序号错误
                        TradeContext.tradeResponse.append(['errorCode','A0002'])
                        TradeContext.tradeResponse.append(['errorMsg','页序号错误'])
                        return True
            
        #新的批次，对账明细入库
        AfaLoggerFunc.tradeInfo( '>>>新的批次，对账明细入库' )
        recNum=int(TradeContext.pageNum)
        AfaLoggerFunc.tradeInfo(str(recNum))
        for i in range( 0, recNum ):
            sql="insert into TIPS_CHECKDATA(WORKDATE,BATCHNO,CORPSERIALNO,PAYEEBANKNO,PAYBKCODE,TAXVOUNO,ACCNO,AMOUNT,"
            sql=sql+"STATUS,NOTE3)"
            sql=sql+" values"
            if recNum==1:
                sql=sql+"('"+TradeContext.chkDate           +"'"
                sql=sql+",'"+TradeContext.chkAcctOrd            +"'"
                sql=sql+",'"+TradeContext.cNo            +"'"
                sql=sql+",'"+TradeContext.payeeBankNo       +"'"
                sql=sql+",'"+TradeContext.payBkCode         +"'"
                sql=sql+",'"+TradeContext.vNo          +"'"
                sql=sql+",'"+TradeContext.acc           +"'"
                sql=sql+",'"+TradeContext.amt            +"'"
                sql=sql+",'"+'9'                            +"'"
                sql=sql+",'"+TradeContext.CurPackNo         +"'"
            else:
                sql=sql+"('"+TradeContext.chkDate       +"'"
                sql=sql+",'"+TradeContext.chkAcctOrd            +"'"
                sql=sql+",'"+TradeContext.cNo[i]            +"'"
                sql=sql+",'"+TradeContext.payeeBankNo       +"'"
                sql=sql+",'"+TradeContext.payBkCode         +"'"
                sql=sql+",'"+TradeContext.vNo[i]          +"'"
                sql=sql+",'"+TradeContext.acc[i]           +"'"
                sql=sql+",'"+TradeContext.amt[i]            +"'"
                sql=sql+",'"+'9'                            +"'"
                sql=sql+",'"+TradeContext.CurPackNo         +"'"
            sql=sql+")"
            AfaLoggerFunc.tradeInfo(sql)
            if( AfaDBFunc.InsertSqlCmt(sql) == -1 ):
                AfaLoggerFunc.tradeFatal(sql)
                TipsFunc.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                raise TipsFunc.flowException( ) 
        #批量管理表写入    
        if (len(Records)>0 and Records[0][0]>0  and int(TradeContext.pageSerno.strip())!=1):
            #批量管理表更新
            sqlStr1 = "UPDATE TIPS_CHECKADM SET NOTE2=char(bigint(NOTE2)+1) WHERE "
            sqlStr1 =sqlStr1 +" WORKDATE  = '"      + TradeContext.chkDate.strip()         + "'"
            sqlStr1 =sqlStr1 +"and BATCHNO   = '"   + TradeContext.chkAcctOrd.strip()      + "'"
            sqlStr1 =sqlStr1 +"and PAYEEBANKNO = '" + TradeContext.payeeBankNo.strip()     + "'"
            sqlStr1 =sqlStr1 +"and PAYBKCODE   = '" + TradeContext.payBkCode.strip()       + "'"
            sqlStr1 =sqlStr1 +"and NOTE3   = '" + TradeContext.CurPackNo.strip()       + "'"
            AfaLoggerFunc.tradeInfo(sqlStr1 )
            records1=AfaDBFunc.UpdateSqlCmt( sqlStr1 )
            if( records1 <0 ):
                return TipsFunc.ExitThisFlow( 'A0027', '数据库错，批量管理表操作异常' )
        else:    
            sqlStr1="insert into TIPS_CHECKADM(WORKDATE,WORKTIME,BATCHNO,PAYEEBANKNO,PAYBKCODE,CHKACCTTYPE,DEALSTATUS,TOTALNUM,TOTALAMT,SUCCNUM,SUCCAMT,"
            sqlStr1=sqlStr1+"NOTE1,NOTE2,NOTE3)"
            sqlStr1=sqlStr1+" values"
            sqlStr1=sqlStr1+"('"+TradeContext.chkDate           +"'"
            sqlStr1=sqlStr1+",'"+TradeContext.workTime          +"'"
            sqlStr1=sqlStr1+",'"+TradeContext.chkAcctOrd        +"'"
            sqlStr1=sqlStr1+",'"+TradeContext.payeeBankNo       +"'"
            sqlStr1=sqlStr1+",'"+TradeContext.payBkCode         +"'"
            sqlStr1=sqlStr1+",'"+TradeContext.chkAcctType       +"'"
            sqlStr1=sqlStr1+",'"+'9'                            +"'"
            sqlStr1=sqlStr1+",'"+TradeContext.allNum            +"'"
            sqlStr1=sqlStr1+",'"+TradeContext.allAmt            +"'"
            sqlStr1=sqlStr1+",'0'"
            sqlStr1=sqlStr1+",'0'"
            sqlStr1=sqlStr1+",'"+TradeContext.priorChkAcctOrd   +"'"
            sqlStr1=sqlStr1+",'"+TradeContext.pageSerno         +"'"  #页序号（AFE与AFA传递数据包大小有限制，将包拆分，多次传递）
            sqlStr1=sqlStr1+",'"+TradeContext.CurPackNo         +"'"  #包序号（TIPS传递数据包大小有限制，将包拆分，多次传递）
            sqlStr1=sqlStr1+")"
            AfaLoggerFunc.tradeInfo(sqlStr1)
            if( AfaDBFunc.InsertSqlCmt(sqlStr1) == -1 ):
                AfaLoggerFunc.tradeFatal(sqlStr1)
                return TipsFunc.ExitThisFlow( 'A0027', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
            
        TradeContext.tradeResponse.append(['errorCode','0000'])
        TradeContext.tradeResponse.append(['errorMsg','交易成功'])
        
        #20100113  关彬捷  增加  判断CHECKDATA登记簿中记录条数与报文中交易数是否相等,若相等则允许进行下一步对账操作
        sqlstr = "select count(*) from TIPS_CHECKDATA where "
        sqlstr = sqlstr + ""
        sqlstr = sqlstr +" WORKDATE  = '"        + TradeContext.chkDate.strip()     + "'"
        sqlstr = sqlstr +"and BATCHNO   = '"     + TradeContext.chkAcctOrd.strip()  + "'"
        sqlstr = sqlstr +"and PAYEEBANKNO   = '" + TradeContext.payeeBankNo.strip() + "'"
        sqlstr = sqlstr +"and PAYBKCODE     = '" + TradeContext.payBkCode.strip()   + "'"
        AfaLoggerFunc.tradeInfo(sqlstr)
        records = AfaDBFunc.SelectSql(sqlstr)
        if records == None:
            AfaLoggerFunc.tradeFatal(sqlstr)
            return TipsFunc.ExitThisFlow( 'A0027','数据库操作异常:' + AfaDBFunc.sqlErrMsg)
        else:
            AfaLoggerFunc.tradeInfo(">>>allNum=[" + TradeContext.allNum + "],COUNT=[" + str(records[0][0]) + "]")
            #如果TIPS_CHECKDATA记录条数与allNum相符,则允许进入下一对账流程
            if (int(TradeContext.allNum) == records[0][0]):
                TradeContext.tradeResponse.append(['nextStep','1'])  #对账流程标识:1-允许进入下一流程;2-禁止进入下一流程
                AfaLoggerFunc.tradeDebug(">>>所有包数据登记结束,进入下一对账流程")
            else:
                TradeContext.tradeResponse.append(['nextStep','2'])  #对账流程标识:1-允许进入下一流程;2-禁止进入下一流程
                AfaLoggerFunc.tradeDebug(">>>包数据未登记结束,不进入下一对账流程")
        #20100113  关彬捷  修改结束

        AfaLoggerFunc.tradeInfo('财税库行_TIPS发起明细对账_前处理结束[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        return True
    except Exception, e:
        TipsFunc.exitMainFlow(str(e))
        
