# -*- coding: gbk -*-
##################################################################
#   中间业务平台.TIPS发起批量记账
#       9 - 初始状态，待处理
#       1 - 失败
#       2 - 批量扣款中
#       0 - 扣款成功
#=================================================================
#   程序文件:   TTPS001_8450031.py
#   程 序 员:   liyj
#   修改时间:   2008-5-12 10:28
##################################################################
import TradeContext
TradeContext.sysType = 'tips'
import TipsFunc ,AfaUtilTools
import AfaDBFunc,ConfigParser,os,TipsHostFunc
from tipsConst import *
#import time
from types import *
#UtilTools,AfaLoggerFunc,HostContext,HostComm,

#读取批量配置文件中信息
def GetLappConfig( CfgFileName = None ):

    try:
        config = ConfigParser.ConfigParser( )

        if( CfgFileName == None ):
            CfgFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'

        config.readfp( open( CfgFileName ) )

        TradeContext.HOST_HOSTIP   = config.get('HOST_DZ', 'HOSTIP')
        TradeContext.HOST_USERNO   = config.get('HOST_DZ', 'USERNO')
        TradeContext.HOST_PASSWD   = config.get('HOST_DZ', 'PASSWD')
        TradeContext.HOST_LDIR     = config.get('HOST_DZ', 'LDIR')
        TradeContext.HOST_RDIR     = config.get('HOST_DZ', 'RDIR')
        TradeContext.CORP_CDIR     = config.get('HOST_DZ', 'CDIR')
        TradeContext.BANK_CDIR     = config.get('HOST_DZ', 'BDIR')
        TradeContext.TRACE         = config.get('HOST_DZ', 'TRACE')

        return 0

    except Exception, e:
        print str(e)
        return -1

def SubModuleMainFst( ):
    TipsFunc.WrtLog('财税库行_批量记账处理开始[TTPS001_8450031]' )
    try:
        #读取配置文件中信息
        TipsFunc.WrtLog('>>>读取配置文件中信息')
        GetLappConfig( )
        
        TradeContext.sTellerNo = TIPS_TELLERNO_AUTO      #交易柜员号
        TradeContext.sDAccNo = ''                        #贷方帐号
        TradeContext.sDAccName = ''                      #贷方户名
        
        #拼sql语句,本日本批次号的数据写到文件里=================================================================
        TipsFunc.WrtLog('>>>本日本批次数据写入文件')
        
        #20110711 曾照泰修改 只能上传当天没有处理的批扣文件
        sql = "select workdate from tips_adm where status='1'"
        TipsFunc.WrtLog('查询当天日期的sql=' + sql )
        rec = AfaDBFunc.SelectSql(sql)
        if (rec == None):
            TipsFunc.WrtLog('tips系统日期表操作异常:'+AfaDBFunc.sqlErrMsg)
            return TipsFunc.ExitThisFlow( 'A0027', '数据库错，系统日期表操作异常' )
        elif ( len(rec) <= 0 ):
            TipsFunc.WrtLog( "没有当天的日期，请联系技术人员")
        else:
            TradeContext.TipsDate = rec[0][0]
            TipsFunc.WrtLog("tips当天日期为"+ TradeContext.TipsDate)
        #sql = "select WORKDATE,BATCHNO,TAXORGCODE,PAYEEBANKNO,PAYBKCODE,TOTALNUM,TOTALAMT,DEALSTATUS from TIPS_BATCHADM where DEALSTATUS = '9' "
        sql = "select WORKDATE,BATCHNO,TAXORGCODE,PAYEEBANKNO,PAYBKCODE,TOTALNUM,TOTALAMT,DEALSTATUS from TIPS_BATCHADM where DEALSTATUS = '9' and WORKDATE = '" + TradeContext.TipsDate + "' "
        #end 曾照泰修改
        
        TipsFunc.WrtLog( 'sql=' + sql )
        res = AfaDBFunc.SelectSql( sql )
        if( res == None ):
            TipsFunc.WrtLog('批量管理表操作异常:'+AfaDBFunc.sqlErrMsg)
            return TipsFunc.ExitThisFlow( 'A0027', '数据库错，批量管理表操作异常' )
        elif ( len(res) <= 0 ):
            TipsFunc.WrtLog("无需要处理的批次")
        else:
            for j in range(len(res)):
                TradeContext.entrustDate = res[j][0]       #委托日期
                TradeContext.packNo = res[j][1]            #包流水号
                TradeContext.taxOrgCode = res[j][2]        #征收机关代码
                TradeContext.payeeBankNo = res[j][3]       #收款行行号
                TradeContext.payBkCode = res[j][4]         #付款行行号
                TradeContext.sTotal = res[j][5]            #总笔数
                TradeContext.sAmount = res[j][6]           #总金额
                TradeContext.sStatus = res[j][7]           #处理状态
                
                TradeContext.sBrNo = TIPS_SBNO_QS                      #交易机构号
                TradeContext.sTeller = TIPS_TELLERNO_AUTO              #交易柜员号
                TradeContext.sTermId = '123456'                        #终端号
                TradeContext.sOpeFlag = '0'                             #操作标志
                TradeContext.sFileName = "JU" + TradeContext.packNo      #文件名
                
                #查询批量扣税所需数据============================================================================
                TipsFunc.WrtLog('>>>查询批量扣税所需数据')
                #sql = "select t2.SERIALNO,t1.ACCNO,t1.HandOrgName,t1.AMOUNT,t1.NOTE7 from TIPS_BATCHDATA t1,tips_maintransdtl t2 where "
                #sql = sql + " t1.workdate ='" + TradeContext.entrustDate + "'"
                #sql = sql + " and t2.workdate ='" + TradeContext.entrustDate + "'"
                #sql = sql + " and t1.CORPSERIALNO =t2.CORPSERNO"
                #sql = sql + " and t1.batchno = '" + TradeContext.packNo + "'"
                #sql = sql + " and t1.taxorgcode = '" + TradeContext.taxOrgCode + "'"
                #sql = sql + " and t1.status  = '9'"
                sql = "select t1.SERIALNO,t1.ACCNO,t1.HandOrgName,t1.AMOUNT,t1.NOTE7 from TIPS_BATCHDATA t1 where "
                sql = sql + " t1.workdate ='" + TradeContext.entrustDate + "'"
                sql = sql + " and t1.batchno = '" + TradeContext.packNo + "'"
                sql = sql + " and t1.taxorgcode = '" + TradeContext.taxOrgCode + "'"
                sql = sql + " and t1.status  = '9'"
                
                TipsFunc.WrtLog( 'sql=' + sql )
                records = AfaDBFunc.SelectSql( sql )
                
                if len( records ) > 0:
                    TipsFunc.WrtLog( '>>>此批次存在未处理的批量明细数据,提交主机批量记账')
                    #生成主机记账批量文件============================================================================
                    TipsFunc.WrtLog( '>>>生成主机记账批量文件')
                    filename = os.environ['AFAP_HOME'] + '/data/batch/tips/TIPS_' + TradeContext.packNo + '.txt'
                    rfp = open( filename, 'w' )
                    
                    Total  = 0
                    Amount = 0
                    records = AfaUtilTools.ListFilterNone(records)
                    for i in range( len( records ) ):
                        TradeContext.accno      = records[i][1]           #付款帐号
                        TradeContext.SerialNo   = records[i][0]           #流水号
                        TradeContext.brno       = records[i][4]           #开户行机构号
                        
                        #获取贷方帐号、贷方户名==========================================================================
                        TipsFunc.WrtLog('>>>获取贷方帐号、贷方户名')
                        #====查询收款帐号=======
                        if not TipsFunc.SelectAcc():
                            TipsFunc.WrtLog( ">>>查询收款帐号异常")
                            return TipsFunc.ExitThisFlow( '99090', '查询收款帐号异常' )
                            
                        TradeContext.sDAccNo = TradeContext.__agentAccno__             #贷方帐号
                        TradeContext.sDAccName = TradeContext.__agentAccname__         #贷方户名
                            
                        wbuffer = ''
                        wbuffer = wbuffer +((TradeContext.entrustDate).strip()).ljust(8,' ') + "<fld>"
                        wbuffer = wbuffer +((TradeContext.packNo).strip()).ljust(12,' ') + "<fld>"
                        wbuffer = wbuffer +((TradeContext.entrustDate).strip()).ljust(8,' ') + "<fld>"
                        wbuffer = wbuffer +(records[i][0].strip()).ljust(12,' ') + "<fld>"
                        wbuffer = wbuffer +(TradeContext.brno).ljust(10,' ') + "<fld>"
                        wbuffer = wbuffer +(TradeContext.sTellerNo).ljust(6,' ') + "<fld>"
                        wbuffer = wbuffer +(records[i][1].strip()).ljust(25,' ') + "<fld>"
                        wbuffer = wbuffer +(records[i][2].strip()).ljust(60,' ') + "<fld>"
                        wbuffer = wbuffer +(TradeContext.sDAccNo).ljust(25,' ') + "<fld>"
                        wbuffer = wbuffer +(TradeContext.sDAccName).ljust(60,' ') + "<fld>"
                        wbuffer = wbuffer + "1".ljust(1,' ') + "<fld>"
                        wbuffer = wbuffer +(records[i][3].strip()).ljust(15,' ') + "<fld>"
                        wbuffer = wbuffer + "0".ljust(1,' ')+ "<fld>"
                        #写入报表文件
                        rfp.write(wbuffer + '\n')
                        
                        Total = Total + 1
                        Amount = Amount + (long)((float)(records[i][3].strip())*100 + 0.1)
                    
                    #关闭文件=========================================================================
                    rfp.close()
            
                    sFileName = '/home/maps/afa/data/batch/tips/TIPS_' + TradeContext.packNo + '.txt'
                    dFileName = '/home/maps/afa/data/batch/tips/TPMPFILE.JU' + TradeContext.packNo
                    fFileFld = 'tpmpa.fld'
                    
                    #转码=============================================================================
                    TipsFunc.WrtLog(">>>批量文件转码")
                    if not TipsFunc.FormatFile("1",sFileName,dFileName,fFileFld):
                        TipsFunc.WrtLog("转换批量上传文件编码异常")
                        continue
                        #return TipsFunc.ExitThisFlow( '99090', '转换批量上传文件编码异常' )
                    
                    #上传批量文件=====================================================================
                    TipsFunc.WrtLog(">>>上传批量文件")
                    if not TipsFunc.putHost('TPMPFILE.JU' + TradeContext.packNo,"TEXTLIB"):
                        TipsFunc.WrtLog("上传批量文件异常")
                        continue
                        #return TipsFunc.ExitThisFlow( '99090', '上传批量文件异常' )
                    
                    #发送批量上传交易=================================================================
                    TradeContext.sTotal = Total            #总笔数
                    if Amount <= 0 :
                        TradeContext.sAmount   = '0'
                   
                    #begin 20110722 曾照泰修改 处理金额的单位为分和毛的情况
                    elif (len(str(Amount)) == 1 ):            #以分为单位
                        TradeContext.sAmount  = '0.0' + str(Amount)
                    
                    elif (len(str(Amount)) == 2 ):           #以毛为单位
                        TradeContext.sAmount  = '0.' + str(Amount)
                    #end        
                    else:
                        TradeContext.sAmount   = str(Amount)[:-2] + '.' + str(Amount)[-2:]       #总金额
                    TipsFunc.WrtLog(">>>发送批量上传交易8830")
                    if not TipsHostFunc.CommHost('8830'):
                        TipsFunc.WrtLog( ">>>[" + TradeContext.errorCode + "]" + TradeContext.errorMsg)
                        continue
                        #return TipsFunc.ExitThisFlow( '99090', '其它错误' )
            
                    #发送批量记账申请===============================================================
                    TipsFunc.WrtLog( ">>>发送批量记账申请8831")
                    if not TipsHostFunc.CommHost('8831'):
                        TipsFunc.WrtLog( ">>>[" + TradeContext.errorCode + "]" + TradeContext.errorMsg)
                        continue
                        #return TipsFunc.ExitThisFlow( '99090', '其它错误' )
                            
                    #更新批次状态--2 - 批量扣款中================================================
                    TipsFunc.WrtLog(">>>更新批次状态--2 - 批量扣款中")
                    if(not TipsFunc.UpdateBatchAdm('2','0000','批量扣款中')):
                        TipsFunc.WrtLog( ">>>[" + TradeContext.errorCode + "]" + TradeContext.errorMsg)
                        continue
                        #return TipsFunc.ExitThisFlow( '99003', '数据库错误' )
                else:
                    TipsFunc.WrtLog( '>>>此批次不存在未处理的批量明细数据,直接发送批量记账结果')
                    #更新批次状态--0 - 扣款成功===========================================================================
                    TipsFunc.WrtLog(">>>更新批次状态--0 - 扣款成功")
                    if( not TipsFunc.UpdateBatchAdm('0','0000','扣款成功')):
                        TipsFunc.WrtLog( ">>>[" + TradeContext.errorCode + "]" + TradeContext.errorMsg)
                        continue
                        #raise Exception,TradeContext.errorMsg
                    
                    #发送批量记账结果===========================================================================
                    TipsFunc.WrtLog('>>>发送批量记账结果')
                    TradeContext.TemplateCode = 'TPS001'
                    TradeContext.TransCode = '8469'
                    TradeContext.__respFlag__ = '0'
                    subModuleName = 'TTPS001_8469'
                    TradeContext.EntrustDate = TradeContext.entrustDate      #批量委托日期
                    TradeContext.PackNo = TradeContext.packNo           #批量委托号
                    TradeContext.TaxOrgCode = TradeContext.taxOrgCode       #征收机关代码
                    TradeContext.sysId      ='AG2010'
                    TradeContext.busiNo     ='00000000000001'
                    subModuleHandle=__import__( subModuleName )
                    TipsFunc.WrtLog( '执行['+subModuleName+']模块' )
                    if not subModuleHandle.SubModuleMainFst( ) :
                        TipsFunc.WrtLog( ">>>[" + TradeContext.errorCode + "]" + TradeContext.errorMsg)
                        continue
               
        #TradeContext.errorCode='0000'
        #TradeContext.errorMsg='交易成功'
        
        TipsFunc.WrtLog('财税库行_批量记账处理结束[TTPS001_8450031]' )
        return True
    except Exception, e:
        TipsFunc.exitMainFlow(str(e))
        
###########################################主函数###########################################
if __name__=='__main__':

    TipsFunc.WrtLog('********************批量扣税文件上传开始********************')
    
    TradeContext.TransCode = 'TTPS001_8450031'
    SubModuleMainFst( )


    TipsFunc.WrtLog('********************批量扣税文件上传结束********************')

