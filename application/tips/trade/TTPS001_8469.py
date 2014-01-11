# -*- coding: gbk -*-
##################################################################
#   中间业务平台.批量扣款回执处理
#=================================================================
#   程序文件:   003001_032102.py
#   修改时间:   2007-5-28 10:28
##################################################################
import TradeContext, AfaLoggerFunc, AfaAfeFunc,TipsFunc
#UtilTools,TipsFunc,time
import AfaDBFunc,os
from types import *

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('财税库行_批量扣款回执处理_前处理[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:

        #====判断应用状态=======
        if not TipsFunc.ChkAppStatus( ):
            return False
        #=============获取平台流水号====================
        if TipsFunc.GetSerialno( ) == -1 :
            AfaLoggerFunc.tradeInfo('>>>处理结果:获取平台流水号异常' )
            return TipsFunc.ExitThisFlow( 'A0027', '获取流水号失败' )

        #===张恒增加NOTE4字段 20100412===
        sqlStr = "SELECT TOTALNUM,TOTALAMT,SUCCNUM,SUCCAMT,ERRORCODE,ERRORMSG,PAYBKCODE,DEALSTATUS,PAYBKCODE,note3,note4 FROM TIPS_BATCHADM "
        sqlStr =sqlStr +" WHERE WORKDATE = '" + TradeContext.EntrustDate     + "'"
        sqlStr =sqlStr +" and BATCHNO = '"     + TradeContext.PackNo          + "'"
        sqlStr =sqlStr +" and TAXORGCODE = '"  + TradeContext.TaxOrgCode      + "'"
        Records = AfaDBFunc.SelectSql( sqlStr )
        AfaLoggerFunc.tradeInfo(sqlStr)
        if( Records == None or Records < 0):
            AfaLoggerFunc.tradeFatal('批量管理表操作异常:'+AfaDBFunc.sqlErrMsg)
            return TipsFunc.ExitThisFlow( 'A0027', '数据库错，批量管理表操作异常' )
        if( len(Records)==0 ):
            AfaLoggerFunc.tradeFatal('无此批次:'+AfaDBFunc.sqlErrMsg)
            return TipsFunc.ExitThisFlow( 'A0027', '无此批次' )
        elif(len(Records)>0):
            if not(Records[0][7]=='0' or Records[0][7]=='1'):
                AfaLoggerFunc.tradeFatal('批次尚未处理完,不能发送回执')
                return TipsFunc.ExitThisFlow( 'A0027', '批次尚未处理完,不能发送回执' )
            elif(Records[0][7]=='1'):
                AfaLoggerFunc.tradeFatal('该批次处理失败,不能发送回执')
                return TipsFunc.ExitThisFlow( 'A0027', '该批次处理失败,不能发送回执' )
            else: #该批次处理成功，获取流水
                iBatchPage=0
                TradeContext.AllNum      =Records[0][0]
                TradeContext.AllAmt      =Records[0][1]
                TradeContext.SuccNum     =Records[0][2]
                TradeContext.SuccAmt     =Records[0][3]
                TradeContext.Tot_Result    =Records[0][4]
                TradeContext.Tot_AddWord   =Records[0][5]
                TradeContext.PayBkCode     =Records[0][8]
                TradeContext.OrMsgRef      = Records[0][9]

                #===张恒增加NOTE4字段 20100412===
                TradeContext.OrEntrustDate = Records[0][10]

                AfaLoggerFunc.tradeInfo("payBkCode=" + TradeContext.PayBkCode)
                #流水
                sqlStr = "SELECT CORPSERIALNO,AMOUNT,TAXPAYCODE,WORKDATE,ERRORCODE,ERRORMSG FROM TIPS_BATCHDATA WHERE "
                sqlStr =sqlStr +" workDate = '"         + TradeContext.EntrustDate     + "'"
                sqlStr =sqlStr +"and Batchno = '"       + TradeContext.PackNo          + "'"
                sqlStr =sqlStr +"and TAXORGCODE = '"    + TradeContext.TaxOrgCode      + "'"
                sqlStr =sqlStr +" order by SERIALNO"
                Records = AfaDBFunc.SelectSql( sqlStr )
                AfaLoggerFunc.tradeInfo(sqlStr)
                if( Records == None ):
                    AfaLoggerFunc.tradeFatal('批量管理表操作异常:'+AfaDBFunc.sqlErrMsg)
                    return TipsFunc.ExitThisFlow( 'A0027', '数据库错，批量管理表操作异常' )
                elif(len(Records)>0):
#                    TradeContext.OriTraNo=[]
#                    TradeContext.TraAmt  =[]
#                    TradeContext.TaxVouNo=[]
#                    TradeContext.TaxDate =[]
#                    TradeContext.Result  =[]
#                    TradeContext.AddWord =[]
#                    for i in range(0, len(Records)):
#                        TradeContext.OriTraNo.append(Records[i][0])
#                        TradeContext.TraAmt  .append(Records[i][1])
#                        TradeContext.TaxVouNo.append(Records[i][2])
#                        TradeContext.TaxDate .append(Records[i][3])
#                        TradeContext.Result  .append(Records[i][4])
#                        TradeContext.AddWord .append(Records[i][5])
                    TradeContext.FilePath = os.environ['AFAP_HOME'] + '/data/batch/tips/2102_' + TradeContext.EntrustDate + TradeContext.PackNo
                    fp = open(TradeContext.FilePath,"w")
                    for i in range(0, len(Records)):
                        fp.write(Records[i][0] + '|')
                        fp.write(Records[i][1] + '|')
                        fp.write(Records[i][2] + '|')
                        fp.write(Records[i][3] + '|')
                        fp.write(Records[i][4] + '|')
                        fp.write(Records[i][5] + '|')
                    fp.close()
                #TradeContext.TransCode='2102'
                #=============与第三方通讯====================
                AfaAfeFunc.CommAfe()

        #TradeContext.errorCode='0000'
        #TradeContext.errorMsg='交易成功'
        AfaLoggerFunc.tradeInfo('财税库行_批量扣款处理_前处理结束[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        return True
    except Exception, e:
        TipsFunc.exitMainFlow(str(e))
