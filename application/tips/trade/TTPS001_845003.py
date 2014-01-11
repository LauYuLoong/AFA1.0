# -*- coding: gbk -*-
##################################################################
#   中间业务平台.财税库行横向联网.接受TIPS批量扣款请求：将批扣明细写入表BATCH_ADM,TIPS_BATCHDATA
#=================================================================
#       9 - 初始状态，待处理
#       1 - 失败
#       2 - 批量扣款中
#       0 - 扣款成功
#   程序文件:   TTPS001_845003.py
#   修改时间:   2008-09-04 10:28
##################################################################
import TradeContext, AfaLoggerFunc, TipsFunc
import AfaDBFunc
#,os,UtilTools
from types import *
from tipsConst import *

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('财税库行_批量请求交易_前处理[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
    
        #begin 20101130 蔡永贵增加 缓存收款国库名称，用于后面登记流水
        TradeContext.note10 = TradeContext.payeeName
        #end
        
        #begin  蔡永贵增加 缓存下列各值，避免后续操作把原值覆盖而取不到所需数据
        TradeContext.tmp_projectId     = TradeContext.projectId
        TradeContext.tmp_taxTypeName   = TradeContext.taxTypeName
        TradeContext.tmp_taxStartDate  = TradeContext.taxStartDate
        TradeContext.tmp_taxEndDate    = TradeContext.taxEndDate
        TradeContext.tmp_taxTypeAmt    = TradeContext.taxTypeAmt
        #end
        
        AfaLoggerFunc.tradeInfo('>>>日期:' + TradeContext.corpTime + "  " + TradeContext.workDate)
        #=============判断应用状态====================
        if not TipsFunc.ChkAppStatus( ) :
            return False
        #====获取清算信息=======
        if not TipsFunc.ChkLiquidStatus():
            return False

        #============变量值的有效性校验============
        AfaLoggerFunc.tradeInfo('>>>变量值的有效性校验')
        if( not TradeContext.existVariable( "taxOrgCode" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '[taxOrgCode]值不存在!' )
        if( not TradeContext.existVariable( "packNo" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '[packNo]值不存在!' )
        if( not TradeContext.existVariable( "entrustDate" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '[entrustDate]值不存在!' )
        if( not TradeContext.existVariable( "corpTime" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '[corpTime]值不存在!' )

        #检查批次是否过期
        AfaLoggerFunc.tradeInfo('>>>检查批次是否过期')
        AfaLoggerFunc.tradeInfo('>>>日期:' + TradeContext.corpTime + "  " + TradeContext.workDate)
        if (TradeContext.corpTime!=TradeContext.workDate ):
            TradeContext.tradeResponse.append(['errorCode','24020'])
            TradeContext.tradeResponse.append(['errorMsg','已过期，作废'])
            AfaLoggerFunc.tradeInfo('已过期，批次作废。报文工作日期:'+TradeContext.corpTime+'系统工作日期:'+TradeContext.workDate)
            return True
        #查询是否重复批次
        AfaLoggerFunc.tradeInfo('>>>查询是否重复批次')
        sqlStr = "SELECT Dealstatus,errorcode,errormsg FROM TIPS_BATCHADM WHERE "
        sqlStr =sqlStr +" WorkDate  = '" + TradeContext.corpTime + "'"
        sqlStr =sqlStr +"and Batchno   = '" + TradeContext.packNo      + "'"
        sqlStr =sqlStr +"and TAXORGCODE= '" + TradeContext.taxOrgCode  + "'"

        Records = AfaDBFunc.SelectSql( sqlStr )
        AfaLoggerFunc.tradeInfo(sqlStr)
        if( Records == None ):
            AfaLoggerFunc.tradeFatal('批量管理表操作异常:'+AfaDBFunc.sqlErrMsg)
            return TipsFunc.ExitThisFlow( 'A0027', '数据库错，批量管理表操作异常' )
        elif(len(Records)>0):
            AfaLoggerFunc.tradeInfo('批次已存在。批次状态:'+Records[0][0]+'处理状态:'+Records[0][1])
            if (Records[0][0]=='0'): #重复包，且批次已成功
                AfaLoggerFunc.tradeInfo('>>>重复包，且批次已完成记账处理')
                TradeContext.tradeResponse.append(['dealFlag','0'])
                TradeContext.tradeResponse.append(['errorCode','0000'])
                TradeContext.tradeResponse.append(['errorMsg','交易成功'])
                return True
            elif (Records[0][0]=='1'): #重复包，且批次已失败
                AfaLoggerFunc.tradeInfo('>>>重复包，且批次已完成记账处理')
                TradeContext.tradeResponse.append(['errorCode',Records[0][1]])
                TradeContext.tradeResponse.append(['errorMsg',Records[0][2]])
                return True
            #elif  ( Records[0][0]=='9'): #尚未处理
            #    None
            #    #认为是新的批次，重新接收
            #    #else:
            #    #    if int(TradeContext.pageSerno.strip())!=int(Records[0][2].strip())+1:
            #    #        #页序号错误
            #    #        TradeContext.tradeResponse.append(['errorCode','A0002'])
            #    #        TradeContext.tradeResponse.append(['errorMsg','页序号错误'])
            #    #        return True
            else:
                AfaLoggerFunc.tradeInfo('>>>重复包，且批次已提交处理，拒绝本次请求')
                TradeContext.tradeResponse.append(['errorCode','94052'])
                TradeContext.tradeResponse.append(['errorMsg','包重复'])
                return True
        if int(TradeContext.pageSerno.strip())==1:
            AfaLoggerFunc.tradeInfo('>>>尚未处理的重复批次，按新批次处理，删掉旧数据')
            #尚未处理的重复批次，按新批次处理，删掉旧数据
            sqlStr_d_t = "DELETE FROM  TIPS_BATCHDATA WHERE "
            sqlStr_d_t =sqlStr_d_t +" WORKDATE = '"         + TradeContext.corpTime + "'"
            sqlStr_d_t =sqlStr_d_t +"and BATCHNO = '"       + TradeContext.packNo      + "'"
            sqlStr_d_t =sqlStr_d_t +"and TAXORGCODE = '"    + TradeContext.taxOrgCode  + "'"
            AfaLoggerFunc.tradeInfo(sqlStr_d_t )
            if( AfaDBFunc.DeleteSqlCmt( sqlStr_d_t ) <0 ):
                return TipsFunc.ExitThisFlow( 'A0027', '数据库错，批量明细表操作异常' )
            sqlStr_d_b = "DELETE FROM TIPS_BATCHADM WHERE "
            sqlStr_d_b =sqlStr_d_b +" workDate  = '" + TradeContext.corpTime + "'"
            sqlStr_d_b =sqlStr_d_b +"and Batchno   = '" + TradeContext.packNo      + "'"
            sqlStr_d_b =sqlStr_d_b +"and TAXORGCODE = '"    + TradeContext.taxOrgCode  + "'"
            AfaLoggerFunc.tradeInfo(sqlStr_d_b )
            if( AfaDBFunc.DeleteSqlCmt( sqlStr_d_b ) <0 ):
                return TipsFunc.ExitThisFlow( 'A0027', '数据库错，批量管理表操作异常' )

        #新的批次或页，批量明细入库
        AfaLoggerFunc.tradeInfo('>>>新的批次或页，批量明细入库')
        recNum=int(TradeContext.pageNum)
        AfaLoggerFunc.tradeInfo(str(recNum))
        
        #beging  蔡永贵增加
        localtion = 0                   #偏移量
        #end
        
        for i in range( 0, recNum ):
            TradeContext.agentSerialno = ''
            #=============获取平台流水号====================
            if TipsFunc.GetSerialno( ) == -1 :
                AfaLoggerFunc.tradeInfo('>>>处理结果:获取平台流水号异常' )
                return TipsFunc.ExitThisFlow( 'A0027', '获取流水号失败' )

            AfaLoggerFunc.tradeInfo('>>>获取平台流水号结束')
            sql="insert into TIPS_BATCHDATA(WORKDATE,BATCHNO,TAXORGCODE,CORPSERIALNO,SERIALNO,ACCNO,TAXPAYCODE,AMOUNT,"
            sql=sql+"STATUS,ERRORCODE,ERRORMSG,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5,NOTE6,NOTE7,NOTE8,NOTE9,NOTE10)"
            sql=sql+" values"

            #初始化变量
            sStatus    = '9'                              #处理状态
            sErrorCode = '99090'                          #错误码
            sErrorMsg  = '尚未处理'                       #错误信息
            TradeContext.teller         = TIPS_TELLERNO_AUTO #自动柜员
            TradeContext.catrFlag       = '1'             #现金转账标志
            TradeContext.__agentEigen__ = '0'             #从表标志
            TradeContext.revTranF       = '0'
            TradeContext.tradeType      = '8'             #交易类型
            TradeContext.errorCode      = '0000'

            if recNum==1:
                TradeContext.corpSerno  = TradeContext.tNo        #第三方流水号
                TradeContext.accno      = TradeContext.acc        #付款帐号
                TradeContext.protocolNo = TradeContext.ptlN       #协议书号
                TradeContext.taxVouNo   = TradeContext.vNo
                TradeContext.taxPayName = TradeContext.tPN
                TradeContext.amount     = TradeContext.amt
                TradeContext.brno       = TradeContext.opBk       #付款开户行

                #====检查是否签约户=======
                TipsFunc.ChkCustSign()
                AfaLoggerFunc.tradeInfo(TradeContext.errorCode)
                if(TradeContext.errorCode == '24009'):
                    sStatus    = '1'             #处理状态
                    sErrorCode = '24009'         #错误码
                    sErrorMsg  = '账户未签约'      #错误信息
                else:

                    AfaLoggerFunc.tradeInfo(TradeContext.BDt)
                    billData = (TradeContext.BDt).split('|')
                    
                    #begin 20100902 蔡永贵注释掉改部分，变量的拼接直接交给afe完成
                    #TradeContext.taxTypeNum = billData[9]
                    TradeContext.taxTypeNum = TradeContext.TaxTypeNum
                    #
                    #TradeContext.projectId     = []
                    #TradeContext.taxTypeName   = []
                    #TradeContext.taxStartDate  = []
                    #TradeContext.taxEndDate    = []
                    #TradeContext.taxTypeAmt    = []
                    #j = 1
                    #AfaLoggerFunc.tradeInfo('数据长度：' + str(len(billData[9:])))
                    #while(j < len(billData[9:])):
                    #    TradeContext.projectId.append(billData[j+9])
                    #    TradeContext.taxTypeName.append(billData[j+10])
                    #    TradeContext.taxStartDate.append(billData[j+11])
                    #    TradeContext.taxEndDate.append(billData[j+12])
                    #    TradeContext.taxTypeAmt.append(billData[j+13])
                    #    j = j + 5
                    #    i = i + 1
                    #end
                    
                sql=sql+"('"+TradeContext.corpTime          +"'"
                sql=sql+",'"+TradeContext.packNo            +"'"
                sql=sql+",'"+TradeContext.taxOrgCode        +"'"
                sql=sql+",'"+TradeContext.tNo               +"'"
                sql=sql+",'"+TradeContext.agentSerialno     +"'"
                sql=sql+",'"+TradeContext.acc               +"'"
                sql=sql+",'"+TradeContext.vNo               +"'"
                sql=sql+",'"+TradeContext.amt               +"'"
                sql=sql+",'"+sStatus                        +"'"
                sql=sql+",'"+sErrorCode                     +"'"
                sql=sql+",'"+sErrorMsg                      +"'"
                sql=sql+",'"+TradeContext.taxOrgCode        +"'"
                sql=sql+",'"+TradeContext.payeeBankNo       +"'"
                sql=sql+",'"+TradeContext.payeeOrgCode      +"'"
                sql=sql+",'"+TradeContext.payeeAcct         +"'"
                sql=sql+",'"+TradeContext.payeeName         +"'"
                sql=sql+",'"+TradeContext.payBkCode         +"'"
                sql=sql+",'"+TradeContext.opBk              +"'"
                sql=sql+",'"+TradeContext.ptlN              +"'"
                sql=sql+",'"+TradeContext.hON               +"'"
                sql=sql+",'"+TradeContext.tPN               +"'"
                #sql=sql+",'"+TradeContext.bDt               +"'"




            else:
                TradeContext.corpSerno  = TradeContext.tNo[i]        #第三方流水号
                TradeContext.accno      = TradeContext.acc[i]        #付款帐号
                TradeContext.protocolNo = TradeContext.ptlN[i]       #协议书号
                TradeContext.taxVouNo   = TradeContext.vNo[i]
                TradeContext.taxPayName = TradeContext.tPN[i]
                TradeContext.amount     = TradeContext.amt[i]
                TradeContext.brno       = TradeContext.opBk[i]       #付款开户行

                #====检查是否签约户=======
                TipsFunc.ChkCustSign()
                AfaLoggerFunc.tradeInfo(TradeContext.errorCode)
                if(TradeContext.errorCode == '24009'):
                    sStatus    = '1'             #处理状态
                    sErrorCode = '24009'         #错误码
                    sErrorMsg  = '账户未签约'    #错误信息
                    
                    #begin 蔡永贵增加
                    localtion = localtion + int(TradeContext.TaxTypeNum[i])
                    #end
                else:
                    billData = (TradeContext.BDt[i]).split('|')
                    
                    #begin 20100902 蔡永贵注释掉改部分，变量的拼接直接交给afe完成
                    #TradeContext.taxTypeNum = billData[9]
                    TradeContext.taxTypeNum = TradeContext.TaxTypeNum[i]
                    #
                    #TradeContext.projectId     = []
                    #TradeContext.taxTypeName   = []
                    #TradeContext.taxStartDate  = []
                    #TradeContext.taxEndDate    = []
                    #TradeContext.taxTypeAmt    = []
                    #
                    #j = 1
                    #while(j < len(billData[9:])):
                    #    TradeContext.projectId.append(billData[j+9])
                    #    TradeContext.taxTypeName.append(billData[j+10])
                    #    TradeContext.taxStartDate.append(billData[j+11])
                    #    TradeContext.taxEndDate.append(billData[j+12])
                    #    TradeContext.taxTypeAmt.append(billData[j+13])
                    #    j=j+ 5
                    #end
                    
                    #begin  蔡永贵增加
                    TradeContext.projectId     = TradeContext.tmp_projectId[localtion:localtion+int(TradeContext.taxTypeNum)]
                    TradeContext.taxTypeName   = TradeContext.tmp_taxTypeName[localtion:localtion+int(TradeContext.taxTypeNum)]
                    TradeContext.taxStartDate  = TradeContext.tmp_taxStartDate[localtion:localtion+int(TradeContext.taxTypeNum)]
                    TradeContext.taxEndDate    = TradeContext.tmp_taxEndDate[localtion:localtion+int(TradeContext.taxTypeNum)]
                    TradeContext.taxTypeAmt    = TradeContext.tmp_taxTypeAmt[localtion:localtion+int(TradeContext.taxTypeNum)]
                    #AfaLoggerFunc.tradeInfo( "当前偏移：" + str(localtion) )
                    #AfaLoggerFunc.tradeInfo( "当前税种条数：" + TradeContext.taxTypeNum )
                    #AfaLoggerFunc.tradeInfo( TradeContext.projectId)
                    #AfaLoggerFunc.tradeInfo( TradeContext.tmp_projectId )
                    
                    localtion = localtion + int(TradeContext.taxTypeNum)
                    #end


                sql=sql+"('"+TradeContext.corpTime       +"'"
                sql=sql+",'"+TradeContext.packNo            +"'"
                sql=sql+",'"+TradeContext.taxOrgCode        +"'"
                #AfaLoggerFunc.tradeInfo( TradeContext.tNo )
                sql=sql+",'"+TradeContext.tNo[i]            +"'"
                sql=sql+",'"+TradeContext.agentSerialno     +"'"
                sql=sql+",'"+TradeContext.acc[i]            +"'"
                sql=sql+",'"+TradeContext.vNo[i]            +"'"
                sql=sql+",'"+TradeContext.amt[i]            +"'"
                sql=sql+",'"+sStatus                        +"'"
                sql=sql+",'"+sErrorCode                     +"'"
                sql=sql+",'"+sErrorMsg                      +"'"
                sql=sql+",'"+TradeContext.taxOrgCode        +"'"
                sql=sql+",'"+TradeContext.payeeBankNo       +"'"
                sql=sql+",'"+TradeContext.payeeOrgCode      +"'"
                sql=sql+",'"+TradeContext.payeeAcct         +"'"
                sql=sql+",'"+TradeContext.payeeName         +"'"
                sql=sql+",'"+TradeContext.payBkCode         +"'"
                sql=sql+",'"+TradeContext.opBk[i]           +"'"
                sql=sql+",'"+TradeContext.ptlN[i]           +"'"
                sql=sql+",'"+TradeContext.hON[i]            +"'"
                sql=sql+",'"+TradeContext.tPN[i]            +"'"
                #sql=sql+",'"+TradeContext.bDt[i]            +"'"
            sql=sql+")"
            AfaLoggerFunc.tradeInfo(sql)
            if( AfaDBFunc.InsertSqlCmt(sql) == -1 ):
                AfaLoggerFunc.tradeFatal(sql)
                return TipsFunc.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeInfo('写入一条批量明细')

            AfaLoggerFunc.tradeInfo('errorCode = ' + TradeContext.errorCode)

            #guanbj 20091110 账户未签约则不登记主流水表
            if TradeContext.errorCode == '0000':
                #====查询收款帐号=======  20090917 wqs
                if not TipsFunc.SelectAcc():
                    return TipsFunc.ExitThisFlow( 'A0027', '查询收款账号失败' )

                #=============插入流水表====================
                if not TipsFunc.InsertDtl( ):
                    return TipsFunc.ExitThisFlow( 'A0027', '插入流水表失败' )

        if TradeContext.nextFlag=='0':

            #批量管理表写入
            sqlStr1 = "insert into TIPS_BATCHADM(WORKDATE,WORKTIME,BATCHNO,TAXORGCODE,DEALSTATUS,ERRORCODE,ERRORMSG,PAYEEBANKNO,PAYEEACCT,PAYEENAME"
            sqlStr1 = sqlStr1 + ",PAYBKCODE,RETURNTERM,TOTALNUM,TOTALAMT,SUCCNUM,SUCCAMT,"

            #===张恒 增加NOTE4字段 存放批量请求报文中的委托日期字段 START 20100412===
            sqlStr1 = sqlStr1 + "NOTE1,NOTE3,"
            sqlStr1 = sqlStr1 + "NOTE4)"
            #===张恒 增加NOTE4字段 存放批量请求报文中的委托日期字段 END  ===

            sqlStr1 = sqlStr1 + " values"
            sqlStr1 = sqlStr1 + "('"+TradeContext.corpTime          +"'"
            sqlStr1 = sqlStr1 + ",'"+TradeContext.workTime          +"'"
            sqlStr1 = sqlStr1 + ",'"+TradeContext.packNo            +"'"
            sqlStr1 = sqlStr1 + ",'"+TradeContext.taxOrgCode        +"'"
            sqlStr1 = sqlStr1 + ",'"+'9'                            +"'"
            sqlStr1 = sqlStr1 + ",'"+'99090'                        +"'"
            sqlStr1 = sqlStr1 + ",'"+'尚未处理'                     +"'"
            sqlStr1 = sqlStr1 + ",'"+TradeContext.payeeBankNo       +"'"
            sqlStr1 = sqlStr1 + ",'"+TradeContext.payeeAcct         +"'"
            sqlStr1 = sqlStr1 + ",'"+TradeContext.payeeName         +"'"
            sqlStr1 = sqlStr1 + ",'"+TradeContext.payBkCode         +"'"
            sqlStr1 = sqlStr1 + ",'"+TradeContext.returnTerm        +"'"
            sqlStr1 = sqlStr1 + ",'"+TradeContext.allNum            +"'"
            sqlStr1 = sqlStr1 + ",'"+TradeContext.allAmt            +"'"
            sqlStr1 = sqlStr1 + ",'"+'0'                            +"'"
            sqlStr1 = sqlStr1 + ",'"+'0.00'                            +"'"
            sqlStr1 = sqlStr1 + ",'"+TradeContext.pageSerno       +"'"  #页序号（AFE与AFA传递数据包大小有限制，将包拆分，多次传递）
            sqlStr1 = sqlStr1 + ",'"+TradeContext.MsgRef          +"'"  #报文参考号

            #===张恒 增加NOTE4字段 存放批量请求报文中的委托日期字段  START ===
            sqlStr1 = sqlStr1 + ",'"+TradeContext.entrustDate     +"'"  #委托日期
            #===张恒 增加NOTE4字段 存放批量请求报文中的委托日期字段 END  ===

            sqlStr1 = sqlStr1 + ")"
            AfaLoggerFunc.tradeInfo(sqlStr1)
            if( AfaDBFunc.InsertSqlCmt(sqlStr1) == -1 ):
                AfaLoggerFunc.tradeFatal(sqlStr1)
                return TipsFunc.ExitThisFlow( 'A0027', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
            #批次数据检查
            AfaLoggerFunc.tradeInfo('>>>批次数据检查')
            sqlStr_dt = "select count(*),sum(cast(amount as decimal(17,2))) FROM  TIPS_BATCHDATA WHERE "
            sqlStr_dt =sqlStr_dt +" workDate = '" + TradeContext.corpTime + "'"
            sqlStr_dt =sqlStr_dt +"and Batchno = '" + TradeContext.packNo      + "'"
            sqlStr_dt =sqlStr_dt +"and TAXORGCODE = '" + TradeContext.taxOrgCode  + "'"
            AfaLoggerFunc.tradeInfo(sqlStr_dt )
            records_dt = AfaDBFunc.SelectSql( sqlStr_dt )
            if records_dt == None :
                return TipsFunc.ExitThisFlow( 'A0027', '数据库错，批量管理表操作异常')
            if long(TradeContext.allNum)!=long(records_dt[0][0]):
                AfaLoggerFunc.tradeInfo('明细和汇总校验不符;实际明细汇总笔数：'+str(records_dt[0][0])+'  总比数：'+TradeContext.allNum)
                return TipsFunc.ExitThisFlow( '24020', '明细和汇总校验不符' )
            if float(TradeContext.allAmt)!=float(records_dt[0][1]):
                AfaLoggerFunc.tradeInfo('明细和汇总校验不符;实际明细汇总金额：'+str(records_dt[0][1])+'  总金额：'+TradeContext.allAmt)
                return TipsFunc.ExitThisFlow( '24020', '明细和汇总校验不符' )
        TradeContext.tradeResponse.append(['dealFlag','1'])
        TradeContext.tradeResponse.append(['errorCode','0000'])
        TradeContext.tradeResponse.append(['errorMsg','交易成功'])

        AfaLoggerFunc.tradeInfo('财税库行_批量请求交易_前处理结束[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        return True
    except Exception, e:
        TipsFunc.exitMainFlow(str(e))
