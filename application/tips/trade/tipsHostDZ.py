# -*- coding: gbk -*-
################################################################################
#   财税库行系统：系统调度类.TIPS与核心进行对账
#===============================================================================
#   交易文件:   tipsHostDZ.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2009-11-09
#   修 改 者：  刘雨龙
#   修改日期：  2011-5-16
#   修改内容：  与主机对账时，新增查询主流水表第三方对账状态，判断第三方是否已
#               对账，如第三方已对账，主机参与对账直接修改状态为记账成功；
#               如未对账，主机已记账，则需要发起冲正
################################################################################
import TradeContext
TradeContext.sysType = 'tips'
TradeContext.TransCode = 'tipsHostDZ'
import AfaUtilTools,AfaDBFunc,os,sys,AfaFtpFunc
import TipsHostFunc,TipsFunc
from types import *
from tipsConst import *

if __name__ == '__main__':
    
    try:
        TipsFunc.WrtLog("***财税库行系统: 系统调度类.TIPS与核心进行对账[tipsHostDZ]进入***")
        
        if(len(sys.argv)==2):
            TradeContext.chkDate=sys.argv[1]
        else:
            #=============获取当前系统时间====================
            #TradeContext.workDate='20110713'
            TradeContext.workDate=AfaUtilTools.GetSysDate( )
            TradeContext.chkDate =TradeContext.workDate
        
        #==========主机交易前处理==============================================
        TradeContext.sBrNo    = TIPS_SBNO_QS                    #交易机构号
        TradeContext.sTeller  = TIPS_TELLERNO_AUTO              #交易柜员号
        TradeContext.sTermId  = '123456'                        #终端号  
        TradeContext.sOpeFlag = '2'                            #操作标志0-	生成日间批量记账回盘文件 1-生成日间对账文件 2-生成日切对账报文
        TradeContext.entrustDate = TradeContext.chkDate        #对账日期 
            
        
        #申请生成主机对账文件===========================================================================
        TipsFunc.WrtLog('>>>8833申请生成主机对账文件')
        if not TipsHostFunc.CommHost('8833'):
            TipsFunc.exitMainFlow()
        TipsFunc.WrtLog("errorMsg = [" + TradeContext.errorMsg + "]")
        if TradeContext.errorCode != '0000':
            TipsFunc.exitMainFlow()
        
        #下载主机对账文件===========================================================================
        TipsFunc.WrtLog('>>>下载主机对账文件')
        #if(not TipsFunc.getHost('TPRZA','BANKMDS')):
        if (not AfaFtpFunc.getFile("TIPS_DZ","TPRZA","TPRZA")):
            TradeContext.errorCode, TradeContext.errorMsg = "S999","下载主机对账文件异常"
            TipsFunc.exitMainFlow()
        
        sFileName = '/home/maps/afa/data/batch/tips/TPRZA'
        dFileName = '/home/maps/afa/data/batch/tips/TIPS_DZ_' + TradeContext.chkDate+ '.txt'
        fFileFld = 'tprza.fld'
           
        #转码=======================================================================================
        TipsFunc.WrtLog('>>>转码')
        if not TipsFunc.FormatFile("0",sFileName,dFileName,fFileFld):
            TradeContext.errorCode, TradeContext.errorMsg= "S999","转换对账文件编码异常"
            TipsFunc.exitMainFlow()
            
        #匹配对账明细
        TipsFunc.WrtLog('>>>匹配对账明细')
        
        t_sum=0   #总笔数
        t_amt=0.00 #总金额
        s_sum=0   #对账相符总笔数
        s_amt=0.00 #对账相符总金额
        u_sum=0    #对账不符总笔数
        u_amt=0.00 #对账不符总金额
        
        file_name = 'TIPS_DZ_' + TradeContext.chkDate+'.txt'
        file_path = os.environ['AFAP_HOME'] + "/data/batch/tips/"
        rb = open(file_path + file_name , 'r')
        #读取一行
        lineBuf = rb.readline()
        iLine=0
        while ( len(lineBuf) > 87 ):
            iLine=iLine+1
            sItemBuf = lineBuf.split('<fld>')         
            
            if ( len(sItemBuf) < 7 ):
                rb.close() 
                TipsFunc.ExitThisFlow( '9000', '数据文件格式错误(' + file_name + ')')    
                TradeContext.errorCode, TradeContext.errorMsg= "S999",'数据文件格式错误(' + file_name + ')'
                TipsFunc.exitMainFlow()
            
            
            workdate =   sItemBuf[0].strip()    #工作日期
            serialno =   sItemBuf[1].strip()    #流水号
            daccno   =   sItemBuf[2].strip()    #借方帐号
            caccno   =   sItemBuf[3].strip()    #贷方帐号	
            amount   =   sItemBuf[4].strip()    #发生额
            wlbz     =   sItemBuf[5].strip()    #往来标志
            status   =   sItemBuf[6].strip()    #记录状态
            
            if status != "0":
                lineBuf = rb.readline()
                continue
            
            t_sum=t_sum+1
            t_amt=t_amt+float(amount)
                
            #匹配中间业务明细
            #===== modify by liu.yl at 2011/5/16 ====
            #===== 新增查询字段corpchkflg ====
            #sql_s = "select taxpaycode,amount,serialno,zoneno,brno,tellerno,bankstatus from tips_maintransdtl where workdate='"+workdate+"' and serialno='"+serialno+"'"
            sql_s = "select taxpaycode,amount,serialno,zoneno,brno,tellerno,bankstatus,corpchkflag from tips_maintransdtl "
            sql_s = sql_s + "where workdate='"+workdate+"' and serialno='"+serialno+"'"            
            #===== end of modify ====
            
            sql_s = sql_s + " and revtranf='0'"
            records_s=AfaDBFunc.SelectSql(sql_s)
            if records_s==None:
                TipsFunc.WrtLog(sql_s)
                TradeContext.errorCode, TradeContext.errorMsg= "S999",'数据库异常'
                TipsFunc.exitMainFlow()
            elif(len(records_s)==0):
               TipsFunc.WrtLog('中间业务平台无此交易流水'+serialno+',无法自动冲账')
               u_sum=u_sum+1
               u_amt=u_amt+float(records_s[0][1])
               
               lineBuf = rb.readline()
               continue
            else:
                if records_s[0][6] != "0":
                    TipsFunc.WrtLog("此交易流水"+serialno+",中间业务平台未记账,主机已记账,判断第三方状态是否对账")
                    
                    #===== add by liu.yl at 2011/5/17 ====
                    #===== 增加判断人行是否参与对账 ====
                    #===== 如人行参与对账,主机已记账成功(参与对账表示成功),直接修改记录状态为成功 ====
                    #===== 如人行不参与对账,修改记录状态为成功,发起冲正 ====
                    if records_s[0][7] == "0":
                        TipsFunc.WrtLog("此交易流水"+serialno+",第三方参与对账，更新原交易主机状态为记账成功")
                        #更新交易主机状态为记账成功
                        sql_u="update tips_maintransdtl set bankstatus = '0',chkflag='0',errormsg = '对账时强制主机成功' "
                        sql_u=sql_u + "where workdate = '" + workdate + "' and serialno = '" + serialno + "'"
                    
                        rec = AfaDBFunc.UpdateSqlCmt(sql_u)
                        if rec < 0:
                            TipsFunc.WrtLog(sql_u)
                            TradeContext.errorCode, TradeContext.errorMsg = "S999",'数据库异常'
                            TipsFunc.exitMainFlow()

                        s_sum=s_sum+1
                        s_amt=s_amt+float(records_s[0][1])

                        lineBuf = rb.readline()
                        continue
                    else:
                        TipsFunc.WrtLog("此交易流水"+serialno+",第三方未参与对账，更新原交易主机状态为记账成功,然后自动冲账")
                    #===== end of add ====
                    
                    #更新交易主机状态为记账成功
                    sql_u = "update tips_maintransdtl set bankstatus = '0',errormsg = '对账时强制主机成功，冲正'"
                    sql_u = sql_u + "where workdate = '" + workdate + "' and serialno = '" + serialno + "'"
                    
                    rec = AfaDBFunc.UpdateSqlCmt(sql_u)
                    if rec < 0:
                        TipsFunc.WrtLog(sql_u)
                        TradeContext.errorCode, TradeContext.errorMsg = "S999",'数据库异常'
                        TipsFunc.exitMainFlow()
                    
                    #自动冲账初始化
                    TradeContext.taxPayCode     =records_s[0][0]   #用户号
                    TradeContext.amount         =records_s[0][1]   #金额
                    TradeContext.preAgentSerno  =records_s[0][2]   #原交易流水号
                    TradeContext.zoneno         =records_s[0][3]    
                    TradeContext.brno           =records_s[0][4]    
                    TradeContext.teller         =records_s[0][5] 
                    
                    TradeContext.channelCode = '007'
                    TradeContext.workDate = TradeContext.chkDate
                    TradeContext.workTime = AfaUtilTools.GetSysTime( )
                    TradeContext.appNo      ='AG2010'
                    TradeContext.busiNo     ='00000000000001'
                    
                    TradeContext.TransCode = 'tipsHostDZ'
                    
                    #============校验公共节点的有效性==================
                    if ( not TipsFunc.Cancel_ChkVariableExist( ) ):
                        TipsFunc.exitMainFlow()
                    
                    #=============判断反交易数据是否匹配原交易====================
                    if( not TipsFunc.ChkRevInfo( TradeContext.preAgentSerno ) ):
                        TipsFunc.exitMainFlow()
                    
                    #=============获取平台流水号====================
                    if( not TipsFunc.GetSerialno( ) ):
                        TipsFunc.exitMainFlow()
                    
                    #=============插入流水表====================
                    if( not TipsFunc.InsertDtl( ) ):
                        TipsFunc.exitMainFlow()
                    
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
                        TipsFunc.exitMainFlow()
                    
                    #===== add by liu.yl at 2011/5/16 ====
                    #===== 更新交易主机状态为冲正成功 ====
                    if TradeContext.errorCode == '0000':
                        sql_u = "update tips_maintransdtl set bankstatus = '3',chkflag='9',errormsg = '对账时成功冲正'"
                        sql_u = sql_u + "where workdate = '" + workdate + "' and serialno = '" + serialno + "'"
                    
                        rec = AfaDBFunc.UpdateSqlCmt(sql_u)
                        if rec < 0:
                            TipsFunc.WrtLog(sql_u)
                            TradeContext.errorCode, TradeContext.errorMsg = "S999",'数据库异常'
                            TipsFunc.exitMainFlow()
                    #===== end of add ====
                        
                    u_sum=u_sum+1
                    u_amt=u_amt+float(records_s[0][1])
                else:
                    TipsFunc.WrtLog("此交易流水"+serialno+",对账成功")

                    s_sum=s_sum+1
                    s_amt=s_amt+float(records_s[0][1])
                    
                    #更改主机对账状态
                    sql_u = "update tips_maintransdtl set chkflag = '0' where workdate = '" + workdate + "' and serialno = '" + serialno + "'"
                    rec = AfaDBFunc.UpdateSqlCmt(sql_u)
                    if rec < 0:
                        TipsFunc.WrtLog(sql_u)
                        TradeContext.errorCode, TradeContext.errorMsg = "S999",'数据库异常'
                        TipsFunc.exitMainFlow()

            #读取下一行
            lineBuf = rb.readline()
        
        TipsFunc.WrtLog('>>>对账结束')
        TipsFunc.WrtLog('>>>    对账日期:' + TradeContext.chkDate)
        TipsFunc.WrtLog('>>>      总笔数:' + str(t_sum) + '          总金额:' + str(t_amt))   
        TipsFunc.WrtLog('>>>对账相符笔数:' + str(s_sum) + '    对账相符金额:' + str(s_amt))  
        TipsFunc.WrtLog('>>>对账不符笔数:' + str(u_sum) + '    对账不符金额:' + str(u_amt))  
        
        TipsFunc.WrtLog("***财税库行系统: 系统调度类.TIPS与核心进行对账[tipsHostDZ]进入***")
    
    except Exception, e:
        #所有异常

        if( not TradeContext.existVariable( "errorCode" ) or str(e) ):
            TradeContext.errorCode = 'A9999'
            TradeContext.errorMsg = '系统错误['+ str(e) +']'

        if TradeContext.errorCode != '0000' :
            TipsFunc.WrtLog( 'errorCode=['+TradeContext.errorCode+']' )
            TipsFunc.WrtLog( 'errorMsg=['+TradeContext.errorMsg+']' )
            TipsFunc.WrtLog('tipsHostDZ交易中断')

        sys.exit(-1)
