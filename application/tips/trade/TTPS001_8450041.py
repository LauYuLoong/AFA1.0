# -*- coding: gbk -*-
##################################################################
#   中间业务平台.TIPS发起明细对账
#      9  初始
#      2  处理中
#      3  第三方对帐完成
#      4  核心对帐完成
#      0  处理成功
#      1  处理失败
#
#=================================================================
#   程序文件:   TTPS001_8450041.py
#   修改时间:   2007-5-28 10:28
#   修 改 者：  刘雨龙
#   修改时间：  2011-5-17
#   修改内容：  删除原有大批注释
#               批量冲正成功时,修改原交易状态为3-冲正
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools,TipsFunc
import AfaDBFunc,ConfigParser,os
#,HostContext,HostComm
#import time,AfaUtilTools,TipsHostFunc,tipsConst,rccpsHostFunc,rccpsCronFunc
from types import *
#from tipsConst import *

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
    AfaLoggerFunc.tradeInfo('财税库行_对账处理开始[TTPS001_8450041]' )
    try:
        #=============获取当前系统时间====================
        #TradeContext.workDate=UtilTools.GetSysDate( )
        TradeContext.workTime=UtilTools.GetSysTime( )
        #============变量值的有效性校验============
        if( not TradeContext.existVariable( "chkAcctOrd" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '[chkAcctOrd]值不存在!' )
        if( not TradeContext.existVariable( "chkDate" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '[chkDate]值不存在!' )
        if( not TradeContext.existVariable( "chkAcctType" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '[chkAcctType]值不存在!' )
        if( not TradeContext.existVariable( "payeeBankNo" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '[payeeBankNo]值不存在!' )
        if( not TradeContext.existVariable( "payBkCode" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '[payBkCode]值不存在!' )
        #TradeContext.workDate=TradeContext.chkDate
        AfaLoggerFunc.tradeInfo('>>>对帐日期：'+TradeContext.chkDate+'对账批次：'+TradeContext.chkAcctOrd)
        
        #====判断应用状态=======
        if not TipsFunc.ChkAppStatus():
            return False
        #====获取清算信息=======
        if not TipsFunc.ChkLiquidStatus():
            return False
        
        #开始处理批次
        if not UpdateBatchAdm('2','','正在与国库数据进行对账') :
            return TipsFunc.ExitThisFlow( 'A0001', '更新批次状态失败!' )
        
        totalnum_succ=0
        totalamt_succ=0

        #逐笔流水与中间业务对账
        AfaLoggerFunc.tradeInfo('>>>逐笔流水与中间业务对账')
        sqlStr = "SELECT accno,amount,status,corpserialno FROM TIPS_CHECKDATA WHERE "
        sqlStr =sqlStr +" workDate = '"         + TradeContext.chkDate              + "'"
        sqlStr =sqlStr +" AND BATCHNO = '"      + TradeContext.chkAcctOrd           + "'"
        sqlStr =sqlStr +" AND PAYEEBANKNO ='"   + TradeContext.payeeBankNo.strip()    + "'"   
        sqlStr =sqlStr +" AND PAYBKCODE ='"     + TradeContext.payBkCode.strip()  + "'"
        sqlStr =sqlStr +" order by corpserialno"
        Records = AfaDBFunc.SelectSql( sqlStr )
        AfaLoggerFunc.tradeInfo(sqlStr)
        if( Records == None ):
            AfaLoggerFunc.tradeFatal('对账明细表操作异常:'+AfaDBFunc.sqlErrMsg)
            UpdateBatchAdm('1','','对账失败:数据库异常(TIPS_CHECKDATA)')
            return TipsFunc.ExitThisFlow( 'A0027', '数据库错，批量管理表操作异常' )
        else:
            AfaLoggerFunc.tradeInfo('第三方笔数:'+str(len(Records)))
            for i in range(0, len(Records)):
                if (Records[i][2]=='0' ): #已成功
                    continue
                if (Records[i][2]=='1' ): #已成功
                    continue
                elif Records[i][2]=='9':    #流水尚未处理
                    #准备与中间业务对账
                    ChkFlag = '*'
                    #先查询数据库中记录是否存在
                    sqlstr_m = "SELECT AMOUNT,DRACCNO,SERIALNO,CORPCHKFLAG,BANKSTATUS FROM TIPS_MAINTRANSDTL WHERE"
                    sqlstr_m = sqlstr_m + " CORPTIME='"  + TradeContext.chkDate.strip()  + "'"
                    sqlstr_m = sqlstr_m + " AND CORPSERNO='"  + Records[i][3].strip()        + "'"
                    sqlstr_m = sqlstr_m + " AND NOTE3 = '" + TradeContext.payBkCode.strip() + "'"
                    sqlstr_m = sqlstr_m + " AND NOTE4 = '" + TradeContext.payeeBankNo.strip() + "'"
                    sqlstr_m = sqlstr_m + " AND BANKSTATUS = '0' AND REVTRANF='0'"
                    AfaLoggerFunc.tradeInfo(sqlstr_m)
                    records_m = AfaDBFunc.SelectSql( sqlstr_m )
                    if ( records_m==None ):
                        AfaLoggerFunc.tradeFatal('数据库异常:查询业务流水表。'+AfaDBFunc.sqlErrMsg)
                        UpdateBatchAdm('1','','对账失败:数据库异常(TIPS_MAINTRANSDTL)')
                        return TipsFunc.ExitThisFlow( 'A0027', '中间业务流水表操作异常' )
                    if (len(records_m) == 0 ):
                        AfaLoggerFunc.tradeInfo(Records[i])
                        UpdateBatchAdm('1','','对账失败:国库比本行多付款记录')
                        #发起对账回执交易
                        TradeContext.OriPayBankNo  =TradeContext.payBkCode
                        TradeContext.OriChkDate    =TradeContext.chkDate
                        TradeContext.OriChkAcctOrd =TradeContext.chkAcctOrd
                        TradeContext.OriPayeeBankNo=TradeContext.payeeBankNo
                        TradeContext.Result        ='24030'
                        TradeContext.AddWord       ='对帐不符，TIPS比商业银行多付款记录'
                        subModuleName = 'TTPS001_032111'
                        subModuleHandle=__import__( subModuleName )
                        AfaLoggerFunc.tradeInfo( '执行['+subModuleName+']模块' )
                        if not subModuleHandle.SubModuleMainFst( ) :
                            return False
                        return TipsFunc.ExitThisFlow( '24030', '对帐不符，TIPS比商业银行多付款记录' )
                    else:
                        if (records_m[0][3]=='0' ): #已成功
                            continue
                        if (records_m[0][3]=='1' ): #已成功
                            continue
                        elif records_m[0][3]=='9':    #流水尚未处理
                            c_tradeamt = (long)((float)(Records[i][1].strip())*100 + 0.1)
                            m_tradeamt = (long)((float)(records_m[0][0].strip())*100 + 0.1)
                            if ( c_tradeamt != m_tradeamt ):
                                UpdateBatchAdm('1','','对账失败:流水金额不符')
                                #发起对账回执交易
                                TradeContext.OriPayBankNo  =TradeContext.payBkCode
                                TradeContext.OriChkDate    =TradeContext.chkDate
                                TradeContext.OriChkAcctOrd =TradeContext.chkAcctOrd
                                TradeContext.OriPayeeBankNo=TradeContext.payeeBankNo
                                TradeContext.Result        ='24030'
                                TradeContext.AddWord       ='对帐失败,金额不符'
                                subModuleName = 'TTPS001_032111'
                                subModuleHandle=__import__( subModuleName )
                                AfaLoggerFunc.tradeInfo( '执行['+subModuleName+']模块' )
                                if not subModuleHandle.SubModuleMainFst( ) :
                                    return False
                                return TipsFunc.ExitThisFlow( '24030', '对帐失败,金额不符' )
                        ChkFlag = '0'
                        totalnum_succ = totalnum_succ+1
                        totalamt_succ = totalamt_succ + c_tradeamt
                
                    #修改记录对账状态,对账日期和场次
                    sqlstr_m = "UPDATE TIPS_MAINTRANSDTL SET CORPCHKFLAG='" + ChkFlag + "',NOTE1='"+TradeContext.chkDate+"',NOTE2='"+TradeContext.chkAcctOrd+"'"
                    #sqlstr_m = sqlstr_m + " ,CHKFLAG = '0'"
                    #sqlstr_m = sqlstr_m + " ,NOTE3 = '" + TradeContext.payBkCode + "',NOTE4 = '" + TradeContext.payeeBankNo + "' WHERE"
                    sqlstr_m = sqlstr_m + " WHERE"
                    sqlstr_m = sqlstr_m + " CORPTIME='"  + TradeContext.chkDate.strip()  + "'"
                    sqlstr_m = sqlstr_m + " AND CORPSERNO='"  + Records[i][3].strip()        + "'"
                    sqlstr_m = sqlstr_m + " AND NOTE3 = '" + TradeContext.payBkCode.strip() + "'"
                    sqlstr_m = sqlstr_m + " AND NOTE4 = '" + TradeContext.payeeBankNo.strip() + "'"
                    sqlstr_m = sqlstr_m + " AND BANKSTATUS = '0' AND REVTRANF='0'"
                    AfaLoggerFunc.tradeInfo(sqlstr_m)
                    retcode = AfaDBFunc.UpdateSqlCmt( sqlstr_m )
                    if (retcode==None or retcode <= 0):
                        UpdateBatchAdm('1','','对账失败:数据库异常(对账明细表)2')
                        return TipsFunc.ExitThisFlow( 'A0027', '修改记录对帐状态,数据库异常' )
        
        #更新批次状态
        if not UpdateBatchAdm('3','0000','与国库对帐完成') :
            return TipsFunc.ExitThisFlow( 'A0001', '更新批次状态失败!' )
        
        #读取配置文件中信息
        GetLappConfig( )
        
        #日切对账
        if(TradeContext.chkAcctType=='1'):
            #冲正 银行比TIPS多的流水
            if not rev_proc():
                return TipsFunc.ExitThisFlow( 'A0027', '冲正异常' )            
        
        #发起对账回执交易
        TradeContext.OrMsgRef  =TradeContext.MsgRef
        TradeContext.OriPayBankNo  =TradeContext.payBkCode
        TradeContext.OriChkDate    =TradeContext.chkDate
        TradeContext.OriChkAcctOrd =TradeContext.chkAcctOrd
        TradeContext.OriPayeeBankNo=TradeContext.payeeBankNo
        TradeContext.Result        ='90000'
        TradeContext.AddWord       ='对帐完成'
        subModuleName = 'TTPS001_032111'
        subModuleHandle=__import__( subModuleName )
        AfaLoggerFunc.tradeInfo( '执行['+subModuleName+']模块' )
        if not subModuleHandle.SubModuleMainFst( ) :
            UpdateBatchAdm('1','','对账失败:发送对账回执失败')
            return False
        if not UpdateBatchAdm('5','0000','人行对账回执发送完成') :
            return TipsFunc.ExitThisFlow( 'A0001', '更新批次状态失败!' )
   
        #对账完成
        TradeContext.errorCode='0000'
        TradeContext.errorMsg='交易成功'
        
        AfaLoggerFunc.tradeInfo('财税库行_对账处理结束[TTPS001_8450041]' )
        return True
    except Exception, e:
        TipsFunc.exitMainFlow(str(e))

#更新批次状态
def UpdateBatchAdm(status,errorCode,errMsg):
    AfaLoggerFunc.tradeInfo('>>>更新批次状态['+status+']'+errorCode+errMsg)
    sqlStr = "UPDATE TIPS_CHECKADM SET DEALSTATUS='"+status+"',errorcode='"+errorCode+"',ERRORMSG='"+errMsg+"'"
    sqlStr =sqlStr +" WHERE  workDate  = '" + TradeContext.chkDate         + "'"
    sqlStr =sqlStr +" AND BATCHNO = '"      + TradeContext.chkAcctOrd      + "'"
    sqlStr =sqlStr +" AND PAYBKCODE ='"     + TradeContext.payBkCode.strip()  + "'"
    sqlStr =sqlStr +" AND PAYEEBANKNO ='"   + TradeContext.payeeBankNo.strip()    + "'"   
    AfaLoggerFunc.tradeInfo(sqlStr )
    records=AfaDBFunc.UpdateSqlCmt( sqlStr )
    if( records <0 ):
        return TipsFunc.ExitThisFlow( 'A0027', '数据库错误' )
    return True

#批量冲正  银行端比TIPS多的流水
def rev_proc():
    #查询需要冲正的明细
    AfaLoggerFunc.tradeInfo('>>>查询需要冲正的明细')
    sql_m="select taxpaycode,amount,serialno,zoneno,brno,tellerno,bankstatus,corpstatus from tips_maintransdtl "
    sql_m=sql_m+" where corpTime='"+TradeContext.chkDate +"' and  revtranf='0' and bankstatus='0' and corpchkflag='9' "
    sql_m=sql_m+" and note3='"+TradeContext.payBkCode.strip()+"' and note4='"+TradeContext.payeeBankNo.strip()+"'"
    AfaLoggerFunc.tradeInfo(sql_m)
    records_m=AfaDBFunc.SelectSql(sql_m)
    if records_m==None:
        return TipsFunc.ExitThisFlow( 'A0027', '数据库异常' )
    elif(len(records_m)==0):
        AfaLoggerFunc.tradeInfo('>>>没有需要冲正的明细')
        return True
    else:
        records_m=UtilTools.ListFilterNone( records_m )
        for i in range(0,len(records_m)):
            TradeContext.taxPayCode     =records_m[i][0]   #用户号
            TradeContext.amount         =records_m[i][1]   #金额
            TradeContext.preAgentSerno  =records_m[i][2]   #原交易流水号
            TradeContext.zoneno         =records_m[i][3]    
            TradeContext.brno           =records_m[i][4]    
            TradeContext.teller         =records_m[i][5] 
            
            TradeContext.channelCode = '007'
            TradeContext.workDate = TradeContext.chkDate
            TradeContext.workTime = UtilTools.GetSysTime( )
            TradeContext.appNo      ='AG2010'
            TradeContext.busiNo     ='00000000000001'
            
            TradeContext.TransCode = '8450041'
            
            #============校验公共节点的有效性==================
            if ( not TipsFunc.Cancel_ChkVariableExist( ) ):
                raise TipsFunc.flowException( )
            
            #=============判断应用状态====================
            #if( not TipsFunc.ChkAppStatus( ) ):
            #    raise TipsFunc.flowException( )
            
            #=============判断反交易数据是否匹配原交易====================
            if( not TipsFunc.ChkRevInfo( TradeContext.preAgentSerno ) ):
                raise TipsFunc.flowException( )
            
            #=============获取平台流水号====================
            if( not TipsFunc.GetSerialno( ) ):
                raise TipsFunc.flowException( )
            
            #=============插入流水表====================
            if( not TipsFunc.InsertDtl( ) ):
                raise TipsFunc.flowException( )
            
            #=============与主机通讯====================
            TipsFunc.CommHost( )
            
            errorCode=TradeContext.errorCode
            if TradeContext.errorCode=='SXR0010' :  #原交易主机已冲正，当成成功处理
                TradeContext.__status__='0'
                TradeContext.errorCode, TradeContext.errorMsg = '0000', '主机成功'
            
            #=============更新交易流水====================
            if( not TipsFunc.UpdateDtl( 'TRADE' ) ):
                if errorCode == '0000':
                    TradeContext.errorMsg='取消交易成功 '+TradeContext.errorMsg
                raise TipsFunc.flowException( )
                
            #===== add by liu.yl at 2011/5/17 ====
            #===== 新增更新原交易状态为3-冲正 ====
            if TradeContext.errorCode == '0000':
                sql_u = "update tips_maintransdtl set bankstatus='3', errormsg='人行对账冲正成功' "
                sql_u = sql_u + " where corpTime='" + TradeContext.chkDate
                sql_u = sql_u + "' and serialno='" + TradeContext.preAgentSerno               #原交易流水号
                sql_u = sql_u + "' and note3='"+TradeContext.payBkCode.strip()
                sql_u = sql_u + "' and note4='"+TradeContext.payeeBankNo.strip()+"'"
                
                rec = AfaDBFunc.UpdateSqlCmt(sql_u)
                if rec < 0:
                    TipsFunc.WrtLog(sql_u)
                    TradeContext.errorCode, TradeContext.errorMsg = "S999",'数据库异常'
                    TipsFunc.exitMainFlow()
                AfaLoggerFunc.tradeInfo('>>>交易流水号:' + TradeContext.preAgentSerno + '冲正成功')
    return True