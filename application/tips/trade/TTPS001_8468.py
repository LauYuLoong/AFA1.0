# -*- coding: gbk -*-
##################################################################
#   代收代付平台.财税库行横向联网.上线行（社）数据维护
#       opType  0 查询
#       opType  1 新增
#       opType  2 修改
#       opType  3 删除
#=================================================================
#   程序文件:   T3001_8466.py
#   修改时间:   2007-10-23
##################################################################

import TradeContext, AfaLoggerFunc,  AfaFlowControl, AfaDBFunc
#, UtilTools,os,TradeFunc,HostContext
#import HostComm,TipsFunc

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('>>>上线行（社）数据维护')
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
        if( TradeContext.existVariable( "BRNO" ) and len(TradeContext.BRNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[分行行号]:不能为空')
        sql="SELECT BRNO,PAYBKCODE,BANKNO,BANKACCT,BANKNAME,PAYEEBANKNO,STATUS,ACCNO,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5 "
        sql=sql+" FROM TIPS_BRANCH_ADM WHERE 1=1 "
        sql=sql+"AND BRNO='"+ TradeContext.BRNO+"'"
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.SelectSql(sql)
        if( records == None ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
        elif( len( records )==0 ):
            return AfaFlowControl.ExitThisFlow( 'A0027', '未定义信息' )
        elif( len( records )>1 ):
            return AfaFlowControl.ExitThisFlow( 'A0027', 'TIPS_BRANCH_ADM表配置错误' )
        else:
            #if records[0][5]=='0':
               # return AfaFlowControl.ExitThisFlow( 'A0027', '业务已停止' )
          #  if records[0][5]=='2':
           #     return AfaFlowControl.ExitThisFlow( 'A0027', '业务已暂停' )
            TradeContext.BRNO        = records[0][0]
            TradeContext.PAYBKCODE   = records[0][1]
            TradeContext.BANKNO      = records[0][2]
            TradeContext.BANKACCT    = records[0][3]
            TradeContext.BANKNAME    = records[0][4]
            TradeContext.PAYEEBANKNO = records[0][5]
            TradeContext.STATUS      = records[0][6]
            TradeContext.ACCNO       = records[0][7]
            TradeContext.ACCNAME     = records[0][10]
            
        return True
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return AfaFlowControl.ExitThisFlow('9999', '程序处理异常'+str(e))
#新增
def Insert():
    try:
        if( TradeContext.existVariable( "BRNO" ) and len(TradeContext.BRNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[分行行号]:不能为空')
        if( TradeContext.existVariable( "PAYBKCODE" ) and len(TradeContext.PAYBKCODE)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[清算行行号]:不能为空')
        if( TradeContext.existVariable( "STATUS" ) and len(TradeContext.STATUS)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[是否为清算行]:不能为空')
        if( TradeContext.existVariable( "ACCNO" ) and len(TradeContext.ACCNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[财税库款帐号]:不能为空')
        if( TradeContext.existVariable( "PAYEEBANKNO" ) and len(TradeContext.PAYEEBANKNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[清算国库支付系统行号]:不能为空')

        sql="SELECT BRNO,PAYBKCODE,BANKNO,BANKACCT,BANKNAME,PAYEEBANKNO,STATUS,ACCNO,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5 "
        sql=sql+" FROM TIPS_BRANCH_ADM WHERE 1=1 "
        #sql=sql+"AND BRNO='"+ TradeContext.BRNO+"'"
        #guanbinjie 20090901 设置清算行号为唯一值
        sql=sql+"AND PAYBKCODE='"+ TradeContext.PAYBKCODE +"'"
        #修改完成
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.SelectSql(sql)
        if( records == None ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
        elif( len( records ) > 0 ):
            return AfaFlowControl.ExitThisFlow( 'A0027', '已存在此上线行信息' )

        sql="INSERT INTO  TIPS_BRANCH_ADM(BRNO,PAYBKCODE,BANKNO,BANKACCT,BANKNAME,PAYEEBANKNO,STATUS,ACCNO,NOTE3) "
        sql=sql+" VALUES "
        sql=sql+"('"+ TradeContext.BRNO          +"'"
        sql=sql+",'"+ TradeContext.PAYBKCODE     +"'"
        sql=sql+",'"+ TradeContext.BANKNO        +"'"
        sql=sql+",'"+ TradeContext.BANKACCT      +"'"
        sql=sql+",'"+ TradeContext.BANKNAME      +"'"
        sql=sql+",'"+ TradeContext.PAYEEBANKNO   +"'"
        sql=sql+",'"+ TradeContext.STATUS        +"'"
        sql=sql+",'"+ TradeContext.ACCNO         +"'"
        sql=sql+",'"+ TradeContext.ACCNAME         +"'"
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
        if( TradeContext.existVariable( "BRNO" ) and len(TradeContext.BRNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[分行行号]:不能为空')
        if( TradeContext.existVariable( "PAYBKCODE" ) and len(TradeContext.PAYBKCODE)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[清算行行号]:不能为空')
        if( TradeContext.existVariable( "STATUS" ) and len(TradeContext.STATUS)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[是否为清算行]:不能为空')
        if( TradeContext.existVariable( "ACCNO" ) and len(TradeContext.ACCNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[待结算财税库款]:不能为空')
        if( TradeContext.existVariable( "PAYEEBANKNO" ) and len(TradeContext.PAYEEBANKNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[清算国库支付系统行号]:不能为空')

        sql="SELECT BRNO,PAYBKCODE,BANKNO,BANKACCT,BANKNAME,PAYEEBANKNO,STATUS,ACCNO,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5 "
        sql=sql+" FROM TIPS_BRANCH_ADM WHERE 1=1 "
        sql=sql+"AND BRNO='"+ TradeContext.BRNO+"'"
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.SelectSql(sql)
        if( records == None ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
        elif( len( records ) == 0 ):
            return AfaFlowControl.ExitThisFlow( 'A0027', '不存在此上线行信息' )

            
        sql="UPDATE TIPS_BRANCH_ADM SET "
        sql=sql+"PAYBKCODE='"+ TradeContext.PAYBKCODE+"',"
        sql=sql+"BANKNO='"+ TradeContext.BANKNO+"',"
        sql=sql+"BANKACCT='"+ TradeContext.BANKACCT+"',"
        sql=sql+"BANKNAME='"+ TradeContext.BANKNAME+"',"
        sql=sql+"PAYEEBANKNO='"+ TradeContext.PAYEEBANKNO+"',"
        sql=sql+"STATUS='"+ TradeContext.STATUS+"',"
        sql=sql+"ACCNO='"+ TradeContext.ACCNO+"',"
        sql=sql+"NOTE3='"+ TradeContext.ACCNAME+"',"
        sql=sql+"BRNO='"+ TradeContext.BRNO+"' "
        sql=sql+"WHERE "
        sql=sql+"BRNO = '"+ TradeContext.BRNO+"'"
                
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.UpdateSqlCmt(sql)
                 
        if( records <=0  ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0027', '未发现信息:'+AfaDBFunc.sqlErrMsg )
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
        if( TradeContext.existVariable( "BRNO" ) and len(TradeContext.BRNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[分行行号]:不能为空')

        sql="SELECT BRNO,PAYBKCODE,BANKNO,BANKACCT,BANKNAME,PAYEEBANKNO,STATUS,ACCNO,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5 "
        sql=sql+" FROM TIPS_BRANCH_ADM WHERE 1=1 "
        sql=sql+"AND BRNO='"+ TradeContext.BRNO+"'"
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.SelectSql(sql)
        if( records == None ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
        elif( len( records ) == 0 ):
            return AfaFlowControl.ExitThisFlow( 'A0027', '不存在此上线行信息' )

            
        sql="DELETE "
        sql=sql+" FROM TIPS_BRANCH_ADM WHERE 1=1 "
        if( TradeContext.existVariable( "BRNO" ) and len(TradeContext.BRNO)>0):
            sql=sql+"AND BRNO='"+ TradeContext.BRNO+"'"
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.DeleteSqlCmt(sql)
        if( records == None or records <=0 ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
        return True
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return AfaFlowControl.ExitThisFlow('9999', '程序处理异常'+str(e))
