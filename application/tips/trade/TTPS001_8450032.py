# -*- coding: gbk -*-
###############################################################################
# 文件名称：TTPS001_8450032.py
# 文件标识：
# 摘    要：批量回盘处理进程
#       9 - 初始状态，待处理
#       1 - 失败
#       2 - 批量扣款中
#       0 - 扣款成功
# 当前版本：2.0
# 作    者：liyj
# 完成日期：2008年09月10日
#
# 取代版本：
# 原 作 者：
# 完成日期：
###############################################################################
import TradeContext
TradeContext.sysType = 'tips'
import AfaDBFunc,os,TipsFunc,HostContext,TipsHostFunc,ConfigParser
from types import *
from tipsConst import *
#time,AfaAfeFunc,AfaUtilTools,

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

        return True

    except Exception, e:
        print str(e)
        return False

######################################逐笔勾兑流水#####################################
def MatchData():

    #读取配置文件中信息
    TipsFunc.WrtLog('>>>读取配置文件中信息')
    if(not GetLappConfig( )):
        return TipsFunc.ExitThisFlow( 'A0027', '读取配置文件中信息异常' )
        
    TipsFunc.WrtLog('>>>逐笔勾兑流水')

    try:
        totalnum = 0
        totalamt = 0
        
        succnum = 0
        succamt = 0

        #打开主机下载文件
        #sFileName = TradeContext.HOST_LDIR + '/' + 'batch/tips/TIPS_down_' + TradeContext.packNo + '.txt'
        sFileName = '/home/maps/afa/data/batch/tips/JD' + TradeContext.packNo + '.JD'+ TradeContext.packNo
        hFp = open(sFileName, "r")
        #读取一行
        linebuf = hFp.readline()

        while ( len(linebuf) > 0 ):

            #拆分对帐流水
            swapbuf = linebuf.split('<fld>')

            if swapbuf[10].strip() == 'AAAAAAA':
                errorCode = '90000'
                errorMsg = '成功'
                TradeContext.errorCode='0000'
                TradeContext.errorMsg='主机成功'
                TradeContext.__status__='0'
                TradeContext.bankSerno = swapbuf[5]
            else:
                errorCode,errorMsg = TipsFunc.SelCodeMsg(swapbuf[10]) 
                TradeContext.errorCode=errorCode
                TradeContext.errorMsg=errorMsg
                #TradeContext.errorCode=swapbuf[10]
                #TradeContext.errorMsg="主机失败"
                TradeContext.__status__='1'
                TradeContext.bankSerno = swapbuf[5]
            
            #查询是否有记录与之匹配   20090908 wqs
            sql_s="select workdate,corpserialno,note6,note2,serialno from tips_batchdata where workdate='"+ TradeContext.entrustDate + "'"\
                  " and batchno='"+ TradeContext.packNo + "' and TAXORGCODE='"+ TradeContext.taxOrgCode + "' and SERIALNO ='" + swapbuf[3].strip() + "'"
            records_s=AfaDBFunc.SelectSql(sql_s)
            if records_s==None:
                TipsFunc.WrtLog(sql_s )
                TipsFunc.WrtLog('数据库异常'+AfaDBFunc.sqlErrMsg )
                return False
            elif(len(records_s)==0):
                TipsFunc.WrtLog('表tips_batchdata没有匹配的记录' )
                return False
            else:
                TradeContext.corpTime=records_s[0][0]
                TradeContext.corpSerno=records_s[0][1]
                TradeContext.note3=records_s[0][2]
                TradeContext.note4=records_s[0][3]
                TradeContext.agentSerialno=records_s[0][4]
                TradeContext.workDate=TradeContext.corpTime
                TradeContext.revTranF='0'
                TradeContext.TransCode = '845003'
                
                
            
            
            #修改与数据库进行匹配
            updSql = "UPDATE TIPS_BATCHDATA SET ERRORCODE='" + errorCode + "',ERRORMSG = '" + errorMsg + "' WHERE"
            updSql = updSql + " WORKDATE ='" + TradeContext.entrustDate + "'"
            updSql = updSql + " AND BATCHNO ='" + TradeContext.packNo + "'"
            updSql = updSql + " AND TAXORGCODE ='" + TradeContext.taxOrgCode + "'"
            updSql = updSql + " AND SERIALNO ='" + swapbuf[3].strip() + "'"

            TipsFunc.WrtLog(updSql)

            result = AfaDBFunc.UpdateSqlCmt( updSql )
            if ( result <= 0 ):
                TipsFunc.WrtLog( AfaDBFunc.sqlErrMsg )
                TipsFunc.WrtLog('>>>处理结果:修改与匹配流水状态,数据库异常')
                return False
            
            #=============更新主机返回状态====================
            if( not TipsFunc.UpdateDtl( 'TRADE' ) ):
                raise TipsFunc.exitMainFlow( )
            
            if swapbuf[10].strip() == 'AAAAAAA':
                succnum = succnum + 1
                succamt = succamt + float(swapbuf[9].strip()) 

            totalnum = totalnum + 1
            totalamt = totalamt + float(swapbuf[9].strip())
            
            #读取一行
            linebuf = hFp.readline()

        hFp.close()

        TipsFunc.WrtLog( '匹配记录数=' + str(totalnum) + ",匹配总金额=" + str(totalamt) )
        
        #TradeContext.succNum = str(totalnum)
        #TradeContext.succAmt = str(totalamt)
        TradeContext.succNum = str(succnum)
        TradeContext.succAmt = str(succamt)
        
        #更新批次状态--5-处理提回文件===========================================================================
        TipsFunc.WrtLog(">>>更新批次状态--5-处理提回文件")
        if( not TipsFunc.UpdateBatchAdm('5','0000','处理提回文件')):
            TipsFunc.WrtLog( ">>>[" + TradeContext.errorCode + "]" + TradeContext.errorMsg)
            raise Exception,TradeContext.errorMsg

        TipsFunc.WrtLog( '>>>逐笔勾兑流水 ---> 成功' )

        return True

    except Exception, e:
        TipsFunc.WrtLog(str(e))
        TipsFunc.WrtLog('>>>逐笔勾兑流水 ---> 异常')
        return False


###########################################主函数###########################################
if __name__=='__main__':

    TipsFunc.WrtLog('********************批量回盘文件处理开始********************')

    #查询已提交、未提回的批量文件=================================================================
    TipsFunc.WrtLog('>>>查询已提交、未提回的批量文件')
    sql = "select WORKDATE,BATCHNO,TAXORGCODE,NOTE2,PAYEEBANKNO,PAYBKCODE,NOTE3 from TIPS_BATCHADM where DEALSTATUS  = '2' "
    TipsFunc.WrtLog( 'sql=' + sql )
    res = AfaDBFunc.SelectSql( sql )
    if( res == None ):
        TipsFunc.WrtLog('批量管理表操作异常:'+AfaDBFunc.sqlErrMsg)
        TipsFunc.ExitThisFlow( 'A0027', '数据库错，批量管理表操作异常' )    
    elif( len(res) == 0):
        TipsFunc.WrtLog('>>>没有需要处理的数据')
        TipsFunc.ExitThisFlow( 'A0027', '没有需要处理的数据' ) 
    for i in range(len(res)):
        TradeContext.entrustDate = res[i][0]      #批量委托日期
        TradeContext.packNo = res[i][1]           #批量委托号
        TradeContext.taxOrgCode = res[i][2]       #征收机关代码
        TradeContext.sFileName = res[i][3]         #文件名
        TradeContext.payeeBankNo = res[i][4]       #收款行行号
        TradeContext.payBkCode = res[i][5]         #付款行行号
        
        TradeContext.sBrNo = TIPS_SBNO_QS                      #交易机构号
        TradeContext.sTeller = TIPS_TELLERNO_AUTO              #交易柜员号
        TradeContext.sTermId = '123456'                        #终端号  
        TradeContext.sOpeFlag = '0'                            #操作标志0-	生成日间批量记账回盘文件 1-	生成日间对账文件

        #查询批量记账结果===============================================================================
        TipsFunc.WrtLog('>>>8834查询批量记账结果')
        if not TipsHostFunc.CommHost('8834'):
            TipsFunc.WrtLog( ">>>[" + TradeContext.errorCode + "]" + TradeContext.errorMsg)
            continue
            #raise Exception,TradeContext.errorMsg
            
        if(HostContext.O1STCD !='2'):
            continue
                  
        if TradeContext.errorCode == "0000":
            TradeContext.sFileName = 'JD' + TradeContext.packNo    #文件名
            
            #生成批量回盘文件===========================================================================
            TipsFunc.WrtLog('>>>8833生成批量回盘文件')
            if not TipsHostFunc.CommHost('8833'):
                TipsFunc.WrtLog( ">>>[" + TradeContext.errorCode + "]" + TradeContext.errorMsg)
                continue
                #raise Exception,TradeContext.errorMsg
                
            #下载批量回盘文件===========================================================================
            TipsFunc.WrtLog('>>>下载批量回盘文件')
            #if(not TipsFunc.getHost('TPXCA','BANKMDS')):
            #if(not TipsFunc.getHost('NXSCA','BANKMDS')):
            if(not TipsFunc.getHost('JD'+ TradeContext.packNo + '.JD'+ TradeContext.packNo,'TIPSLIB')):
                TradeContext.errorCode, TradeContext.errorMsg= "S999","下载批量文件异常"
                TipsFunc.WrtLog( ">>>[" + TradeContext.errorCode + "]" + TradeContext.errorMsg)
                #continue
                raise Exception,TradeContext.errorMsg
                
            #sFileName = '/home/maps/afa/data/batch/tips/JD' + TradeContext.packNo + '.JD'+ TradeContext.packNo
            #dFileName = '/home/maps/afa/data/batch/tips/TIPS_JD_' + TradeContext.packNo + '.txt'
            #fFileFld = 'tpxca.fld'
                
            #转码=======================================================================================
            #TipsFunc.WrtLog('>>>转码')
            #if not TipsFunc.FormatFile("0",sFileName,dFileName,fFileFld):
            #    TradeContext.errorCode, TradeContext.errorMsg= "S999","转换批量下载文件编码异常"
            #    raise Exception,TradeContext.errorMsg
            
            #匹配批量回盘结果===========================================================================
            TipsFunc.WrtLog('>>>匹配批量回盘结果')
            if(not MatchData()):
                TipsFunc.WrtLog( ">>>[" + TradeContext.errorCode + "]" + TradeContext.errorMsg)
                continue
                #raise Exception,TradeContext.errorMsg
                
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
                #raise Exception,TradeContext.errorMsg

    TipsFunc.WrtLog('********************批量回盘文件处理结束********************')
