# -*- coding: gbk -*-
##################################################################
#   中间业务平台.TIPS发起银行端缴款明细状态查询
#=================================================================
#   程序文件:   TPS001_845005.py
#   修改时间:   2008-9-16 16:05
##################################################################
import TradeContext, AfaLoggerFunc
#, UtilTools,TipsFunc
#import AfaDBFunc,datetime,ConfigParser,os
from types import *

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('财税库行_TIPS发起银行端缴款明细状态查询_前处理[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    
    try:
        #============变量值的有效性校验============
        if( not TradeContext.existVariable( "PackNo" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '[PackNo]值不存在!' )
        if( not TradeContext.existVariable( "chkDate" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '[chkDate]值不存在!' )
            
        #查询是否重复包
        AfaLoggerFunc.tradeInfo( '>>>查询是否重复包' )
        sqlStr = "SELECT DEALSTATUS,WORKDATE,PACKNO,PAYBKCODE,ERRORCODE,ERRORMSG,NOTE2 FROM TIPS_STATCHECKADM WHERE "
        sqlStr =sqlStr +"  WORKDATE  = '"       + TradeContext.ChkDate.strip()        + "'"
        sqlStr =sqlStr +"and PACKNO   = '"      + TradeContext.PackNo.strip()         + "'"
        sqlStr =sqlStr +"and PAYBKCODE   = '"   + TradeContext.PayBkCode.strip()      + "'"
        
        Records = AfaDBFunc.SelectSql( sqlStr )
        AfaLoggerFunc.tradeInfo(sqlStr)
        if( Records == None ):
            AfaLoggerFunc.tradeFatal('包管理表操作异常:'+AfaDBFunc.sqlErrMsg)
            return TipsFunc.ExitThisFlow( 'A0027', '数据库错，包管理表操作异常' )
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
                TradeContext.tradeResponse.append(['errorMsg','包已处理完成'])
                return True
            else: #重复包，重新登记
                AfaLoggerFunc.tradeInfo( '>>>重复包，重新登记' )
                if int(TradeContext.pageSerno.strip())==1:
                    #尚未处理的重复批次，按新批次处理，删掉旧数据
                    sqlStr_d_t = "DELETE FROM  TIPS_STATCHECKDATA WHERE "
                    sqlStr_d_t = sqlStr_d_t +"  workDate  = '"      + TradeContext.ChkDate              + "'"
                    sqlStr_d_t = sqlStr_d_t +" and PACKNO   = '"    + TradeContext.PackNo               + "'"   
                    sqlStr_d_t = sqlStr_d_t +" AND PAYBKCODE   ='"  + TradeContext.payBkCode.strip()  + "'"
                    AfaLoggerFunc.tradeInfo(sqlStr_d_t )
                    if( AfaDBFunc.DeleteSqlCmt( sqlStr_d_t ) <0 ):
                        return TipsFunc.ExitThisFlow( 'A0027', '数据库错，包管理表操作异常' )
                    sqlStr_d_b = "DELETE FROM  TIPS_STATCHECKADM WHERE "
                    sqlStr_d_b =sqlStr_d_b +" WORKDATE  = '"        + TradeContext.chkDate.strip()     + "'"
                    sqlStr_d_b =sqlStr_d_b +"and PACKNO   = '"     + TradeContext.PackNo.strip()       + "'"
                    sqlStr_d_b =sqlStr_d_b +"and PAYBKCODE     = '" + TradeContext.payBkCode.strip()   + "'"
                    AfaLoggerFunc.tradeInfo(sqlStr_d_b )
                    if( AfaDBFunc.DeleteSqlCmt( sqlStr_d_b ) <0 ):
                        return TipsFunc.ExitThisFlow( 'A0027', '数据库错，包管理表操作异常' )
                else:
                    if int(TradeContext.pageSerno.strip())!=int(Records[0][6].strip())+1:
                        #页序号错误
                        TradeContext.tradeResponse.append(['errorCode','A0002'])
                        TradeContext.tradeResponse.append(['errorMsg','页序号错误'])
                        return True
    
    AfaLoggerFunc.tradeInfo('财税库行_TIPS发起银行端缴款明细状态查询_前处理结束[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )