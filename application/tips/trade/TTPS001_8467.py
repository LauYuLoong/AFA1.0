# -*- coding: gbk -*-
##################################################################
#   代收代付平台.财税库行横向联网.清算信息维护
#       opType  0 查询
#       opType  1 新增
#       opType  2 修改
#       opType  3 删除
#=================================================================
#   程序文件:   TTPS001_8467.py
#   修改时间:   2008-10-23
##################################################################

import TradeContext, AfaLoggerFunc,  AfaFlowControl, AfaDBFunc
#import HostComm,TipsFunc,UtilTools, os,TradeFunc,HostContext

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('>>>清算信息维护')
    if TradeContext.opType=='0':
        AfaLoggerFunc.tradeInfo('>>>查询')
        if not Query():
            return False
    elif TradeContext.opType=='1': 
        AfaLoggerFunc.tradeInfo('>>>新增')
        if not Insert():
            return False
    elif TradeContext.opType=='2': 
        AfaLoggerFunc.tradeInfo('>>>修改')
        if not Update():
            return False
    elif TradeContext.opType=='3': 
        AfaLoggerFunc.tradeInfo('>>>删除')
        if not Delete():
            return False
    else:
        return AfaFlowControl.ExitThisFlow('0001', '未定义该操作类型')    

    TradeContext.errorCode='0000'
    TradeContext.errorMsg='交易处理成功'
    return True

#查询
def Query():
    try:
        if( TradeContext.existVariable( "PAYEEBANKNO" ) and len(TradeContext.PAYEEBANKNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[清算国库支付系统行号]:不能为空')
        if( TradeContext.existVariable( "PAYBKCODE" ) and len(TradeContext.PAYBKCODE)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[国库关联行行号]:不能为空')
        
        sql="SELECT PAYEEBANKNO,TRECODE,TRENAME,PAYEEACCT,PAYEEACCTNAME,PAYBKCODE,PAYBKNAME,LIQUIDATEMODE,STATUS,BRNO,TELLERNO,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5 "
        sql=sql+" FROM TIPS_LIQUIDATE_ADM WHERE 1=1 "
        sql=sql+"AND PAYEEBANKNO='"+ TradeContext.PAYEEBANKNO+"'"
        sql=sql+"AND PAYBKCODE='"+ TradeContext.PAYBKCODE+"'"
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.SelectSql(sql)
        if( records == None ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
        elif( len(records) ==0 ):
            return AfaFlowControl.ExitThisFlow( 'A0027', '未此清算信息' )
        elif( len(records) > 1 ):
            return AfaFlowControl.ExitThisFlow( 'A0027', 'TIPS_LIQUIDATE_ADM表配置错误' )
        else:
            if records[0][7]=='0':
                return AfaFlowControl.ExitThisFlow( 'A0027', '业务已停止' )
            if records[0][7]=='2':
                return AfaFlowControl.ExitThisFlow( 'A0027', '业务已暂停' )
            TradeContext.PAYEEBANKNO    = records[0][0]
            TradeContext.TRECODE        = records[0][1]
            TradeContext.TRENAME        = records[0][2]
            TradeContext.PAYEEACCT      = records[0][3]
            TradeContext.PAYEEACCTNAME  = records[0][4]
            TradeContext.PAYBKCODE      = records[0][5]
            TradeContext.PAYBKNAME      = records[0][6]
            TradeContext.LIQUIDATEMODE  = records[0][7]
            TradeContext.BRNO           = records[0][8]
            TradeContext.TELLERNO       = records[0][10]
            
            
        return True
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return AfaFlowControl.ExitThisFlow('9999', '程序处理异常'+str(e))
        
#新增
def Insert():
    try:
        if( TradeContext.existVariable( "PAYEEBANKNO" ) and len(TradeContext.PAYEEBANKNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[清算国库支付系统行号]:不能为空')
        if( TradeContext.existVariable( "TRECODE" ) and len(TradeContext.TRECODE)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[清算国库代码]:不能为空')
        if( TradeContext.existVariable( "TRENAME" ) and len(TradeContext.TRENAME)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[清算国库名称]:不能为空')
        if( TradeContext.existVariable( "PAYEEACCT" ) and len(TradeContext.PAYEEACCT)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[清算国库收款账号]:不能为空')
        if( TradeContext.existVariable( "PAYEEACCTNAME" ) and len(TradeContext.PAYEEACCTNAME)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[清算国库收款账户名称]:不能为空')
        if( TradeContext.existVariable( "PAYBKCODE" ) and len(TradeContext.PAYBKCODE)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[国库关联行行号]:不能为空')
        if( TradeContext.existVariable( "PAYBKNAME" ) and len(TradeContext.PAYBKNAME)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[国库关联行名称]:不能为空')
        if( TradeContext.existVariable( "LIQUIDATEMODE" ) and len(TradeContext.LIQUIDATEMODE)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[清算模式]:不能为空')
        if( TradeContext.existVariable( "BRNO" ) and len(TradeContext.BRNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[机构代码]:不能为空')
        if( TradeContext.existVariable( "TELLERNO" ) and len(TradeContext.TELLERNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[交易柜员]:不能为空')

        sql="SELECT PAYEEBANKNO,TRECODE,TRENAME,PAYEEACCT,PAYEEACCTNAME,PAYBKCODE,PAYBKNAME,LIQUIDATEMODE,STATUS,BRNO,TELLERNO,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5 "
        sql=sql+" FROM TIPS_LIQUIDATE_ADM WHERE 1=1 "
        sql=sql+"AND PAYEEBANKNO='"+ TradeContext.PAYEEBANKNO+"'"
        sql=sql+"AND PAYBKCODE='"+ TradeContext.PAYBKCODE+"'"
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.SelectSql(sql)
        if( records == None ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
        elif( len(records) > 0 ):
            return AfaFlowControl.ExitThisFlow( 'A0027', '已存在此清算信息' )

            
        sql="INSERT INTO  TIPS_LIQUIDATE_ADM(PAYEEBANKNO,TRECODE,TRENAME,PAYEEACCT,PAYEEACCTNAME,PAYBKCODE,PAYBKNAME,LIQUIDATEMODE,STATUS,BRNO,TELLERNO) "
        sql=sql+" VALUES "
        sql=sql+"('"+ TradeContext.PAYEEBANKNO  +"'"
        sql=sql+",'"+ TradeContext.TRECODE      +"'"
        sql=sql+",'"+ TradeContext.TRENAME      +"'"
        sql=sql+",'"+ TradeContext.PAYEEACCT    +"'"
        sql=sql+",'"+ TradeContext.PAYEEACCTNAME+"'"
        sql=sql+",'"+ TradeContext.PAYBKCODE    +"'"
        sql=sql+",'"+ TradeContext.PAYBKNAME    +"'"
        sql=sql+",'"+ TradeContext.LIQUIDATEMODE+"'"
        sql=sql+",'"+ '1'                       +"'"
        sql=sql+",'"+ TradeContext.BRNO         +"'"
        sql=sql+",'"+ TradeContext.TELLERNO     +"'"
        sql=sql+" ) "              
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.InsertSqlCmt(sql)
        
        if( records == None or records <=0  ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
        return True
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return AfaFlowControl.ExitThisFlow('9999', '程序处理异常'+str(e))
        
                
#修改
def Update():
    try:
        if( TradeContext.existVariable( "PAYEEBANKNO" ) and len(TradeContext.PAYEEBANKNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[清算国库支付系统行号]:不能为空')
        if( TradeContext.existVariable( "TRECODE" ) and len(TradeContext.TRECODE)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[清算国库代码]:不能为空')
        if( TradeContext.existVariable( "TRENAME" ) and len(TradeContext.TRENAME)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[清算国库名称]:不能为空')
        if( TradeContext.existVariable( "PAYEEACCT" ) and len(TradeContext.PAYEEACCT)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[清算国库收款账号]:不能为空')
        if( TradeContext.existVariable( "PAYEEACCTNAME" ) and len(TradeContext.PAYEEACCTNAME)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[清算国库收款账户名称]:不能为空')
        if( TradeContext.existVariable( "PAYBKCODE" ) and len(TradeContext.PAYBKCODE)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[国库关联行行号]:不能为空')
        if( TradeContext.existVariable( "PAYBKNAME" ) and len(TradeContext.PAYBKNAME)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[国库关联行名称]:不能为空')
        if( TradeContext.existVariable( "LIQUIDATEMODE" ) and len(TradeContext.LIQUIDATEMODE)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[清算模式]:不能为空')
        if( TradeContext.existVariable( "BRNO" ) and len(TradeContext.BRNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[机构代码]:不能为空')
        if( TradeContext.existVariable( "TELLERNO" ) and len(TradeContext.TELLERNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[交易柜员]:不能为空')
            
        sql="SELECT PAYEEBANKNO,TRECODE,TRENAME,PAYEEACCT,PAYEEACCTNAME,PAYBKCODE,PAYBKNAME,LIQUIDATEMODE,STATUS,BRNO,TELLERNO,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5 "
        sql=sql+" FROM TIPS_LIQUIDATE_ADM WHERE 1=1 "
        sql=sql+"AND PAYEEBANKNO='"+ TradeContext.PAYEEBANKNO+"'"
        sql=sql+"AND PAYBKCODE='"+ TradeContext.PAYBKCODE+"'"
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.SelectSql(sql)
        if( records == None ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
        elif( len(records) == 0 ):
            return AfaFlowControl.ExitThisFlow( 'A0027', '不存在此清算信息' )

        sql="UPDATE TIPS_LIQUIDATE_ADM SET "
        sql=sql+"TRECODE='"+ TradeContext.TRECODE+"',"
        sql=sql+"TRENAME='"+ TradeContext.TRENAME+"',"
        sql=sql+"PAYEEACCT='"+ TradeContext.PAYEEACCT+"',"
        sql=sql+"PAYEEACCTNAME='"+ TradeContext.PAYEEACCTNAME+"',"
        sql=sql+"LIQUIDATEMODE='"+ TradeContext.LIQUIDATEMODE+"',"
        sql=sql+"BRNO='"+ TradeContext.BRNO+"',"
        sql=sql+"TELLERNO='"+ TradeContext.TELLERNO+"',"
        sql=sql+"PAYEEBANKNO='"+ TradeContext.PAYEEBANKNO+"',"
        sql=sql+"PAYBKCODE='"+ TradeContext.PAYBKCODE+"' ,"
        sql=sql+"PAYBKNAME='"+ TradeContext.PAYBKNAME+"' "
        sql=sql+"WHERE "
        sql=sql+"(PAYEEBANKNO = '"+ TradeContext.PAYEEBANKNO+"') AND "
        sql=sql+"(PAYBKCODE = '"+ TradeContext.PAYBKCODE+"') "
                
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.UpdateSqlCmt(sql)
                 
        if( records <=0  ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0027', '未发现清算信息:'+AfaDBFunc.sqlErrMsg )
        if( records == None ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return AfaFlowControl.ExitThisFlow('9999', '程序处理异常'+str(e))

        
        


#删除
def Delete():
    try:
        if( TradeContext.existVariable( "PAYEEBANKNO" ) and len(TradeContext.PAYEEBANKNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[清算国库支付系统行号]:不能为空')
        if( TradeContext.existVariable( "PAYBKCODE" ) and len(TradeContext.PAYBKCODE)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[国库关联行行号]:不能为空')
            
        sql="SELECT PAYEEBANKNO,TRECODE,TRENAME,PAYEEACCT,PAYEEACCTNAME,PAYBKCODE,PAYBKNAME,LIQUIDATEMODE,STATUS,BRNO,TELLERNO,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5 "
        sql=sql+" FROM TIPS_LIQUIDATE_ADM WHERE 1=1 "
        sql=sql+"AND PAYEEBANKNO='"+ TradeContext.PAYEEBANKNO+"'"
        sql=sql+"AND PAYBKCODE='"+ TradeContext.PAYBKCODE+"'"
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.SelectSql(sql)
        if( records == None ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
        elif( len(records) == 0 ):
            return AfaFlowControl.ExitThisFlow( 'A0027', '不存在此清算信息' )

        sql="DELETE "
        sql=sql+" FROM TIPS_LIQUIDATE_ADM WHERE 1=1 "
        sql=sql+"AND PAYEEBANKNO='"+ TradeContext.PAYEEBANKNO+"'"
        sql=sql+"AND PAYBKCODE='"+ TradeContext.PAYBKCODE+"'"
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.DeleteSqlCmt(sql)
        
        if( records <=0  ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0027', '无此清算信息:'+AfaDBFunc.sqlErrMsg )
        if( records == None ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
        return True
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return AfaFlowControl.ExitThisFlow('9999', '程序处理异常'+str(e))
