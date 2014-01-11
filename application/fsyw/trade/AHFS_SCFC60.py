###############################################################################
# -*- coding: gbk -*-
# 文件标识：
# 摘    要：非税实时上传余额信息
#
# 当前版本：1.0
# 作    者：WJJ
# 完成日期：2007年10月15日
###############################################################################
import TradeContext

TradeContext.sysType = 'cron'

import AfaUtilTools, sys, AfaDBFunc, AfaFsFunc
import os, HostContext, HostComm, AfaAfeFunc, AfaLoggerFunc, time
from types import *



def ChkAppStatus():
    sqlstr  =   "select status from abdt_unitinfo where appno='" + TradeContext.appNo + "' and busino ='" + TradeContext.busiNo + "'"
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None or len( records)==0 ):
        AfaLoggerFunc.tradeInfo('查找应用状态库失败')
        return False
    elif len( records ) == 1:
        if records[0][0].strip() == '1':
            return True
        else:
            AfaLoggerFunc.tradeInfo('应用状态没有开启')
            return False
    else:
        AfaLoggerFunc.tradeInfo('应用签约异常')
        return False
        
###########################################主函数###########################################
if __name__=='__main__':
    AfaLoggerFunc.tradeInfo('**********安徽非税实时上传余额信息开始**********')
    
    
    TradeContext.sysId = "AG2008"
    
    #列出所有单位所有单位编号
    #begin 20100527 蔡永贵修改 
    #sqlstr  = "select distinct busino,accno from abdt_unitinfo where appno='AG2008'"
    #sqlstr  = "select distinct busino,accno,appno from abdt_unitinfo where appno in ('AG2008','AG2012')"
    sqlstr  = " select busino,accno,bankno from fs_businoinfo "
    #end
    
    fsrecords = AfaDBFunc.SelectSql( sqlstr )
    if fsrecords == None or len(fsrecords)==0 :
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","查找单位信息表异常"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        sys.exit(1)
        
    AfaLoggerFunc.tradeInfo( fsrecords ) 
    for item in fsrecords :  
        
        AfaLoggerFunc.tradeInfo( item[0] )
        AfaLoggerFunc.tradeInfo( item[1] )
        AfaLoggerFunc.tradeInfo( item[2] )

        #begin 20100527 蔡永贵修改 
        #TradeContext.appNo          =   'AG2008'
        TradeContext.bankbm         =   item[2].strip()
        
        if( TradeContext.bankbm == '012' ):
            TradeContext.appNo = 'AG2008';
        else:
            TradeContext.appNo = 'AG2012';
        #end
        
        TradeContext.busiNo         =   item[0].strip()
        TradeContext.workDate       =   AfaUtilTools.GetSysDate( )
        TradeContext.workTime       =   AfaUtilTools.GetSysTime( )
        TradeContext.zoneno         =   ""
        TradeContext.brno           =   ""
        TradeContext.teller         =   ""
        TradeContext.authPwd        =   ""
        TradeContext.termId         =   ""
        TradeContext.TransCode      =   "8449"                  #实时上传余额信息
        
        #=============判断应用状态========================
        if not ChkAppStatus( ) :
            AfaLoggerFunc.tradeInfo('**********安徽非税单位编号%s应用状态不正常**********' %TradeContext.busiNo)
            continue
        
        #联动主机程序查询账户余额
        HostContext.I1TRCD = '8810'                        #交易码
        HostContext.I1SBNO = ''                            #交易机构号
        HostContext.I1USID = '999986'                      #交易柜员号
        HostContext.I1AUUS = ""                            #授权柜员
        HostContext.I1AUPS = ""                            #授权柜员密码
        HostContext.I1WSNO = ""                            #终端号
        HostContext.I1ACNO = item[1].strip()               #对公活期帐号
        HostContext.I1CYNO = ""                            #币种        
        HostContext.I1CFFG = ""                            #密码校验标志
        HostContext.I1PSWD = ""                            #密码        
        HostContext.I1CETY = ""                            #凭证种类    
        HostContext.I1CCSQ = ""                            #凭证号码    


        HostTradeCode = "8810".ljust(10,' ')
        HostComm.callHostTrade( os.environ['AFAP_HOME'] + '/conf/hostconf/AH8810.map', HostTradeCode, "0002" )
        if( HostContext.host_Error ):
            AfaLoggerFunc.tradeInfo('>>>主机交易失败=[' + str(HostContext.host_ErrorType) + ']:' +  HostContext.host_ErrorMsg)
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   HostContext.host_ErrorMsg
            continue
            
        else:
            if ( HostContext.O1MGID == "AAAAAAA" ):
                AfaLoggerFunc.tradeInfo('返回结果:账户余额     = ' + HostContext.O1ACBL)        #账户余额 
            else:
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "主机交易不成功"
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                continue
        
        
        
        #-----------------------根据单位编码配置获取财政信息----------------------------
        
        #begin 20100527 蔡永贵修改 增加银行编码字段（bankno）作为sql的查询条件
        #sqlstr      =   "select aaa010,bankno from fs_businoinfo where busino='" + TradeContext.busiNo + "'"
        sqlstr      =   "select aaa010,bankno from fs_businoinfo where busino='" + TradeContext.busiNo + "'" + " and bankno='" + TradeContext.bankbm + "'"
        #end
        
        AfaLoggerFunc.tradeInfo( sqlstr )
            
        records = AfaDBFunc.SelectSql( sqlstr )
        if records == None or len(records)==0 :
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","查找单位信息表失败"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            continue
        
        elif len(records) > 1:
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","单位信息表异常:一个单位编号对应了多个财政信息"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            AfaLoggerFunc.tradeInfo( sqlstr )
            continue

        #拼成第三方报文
        TradeContext.TemplateCode   =   "3001"
        TradeContext.AAA010         =   records[0][0].strip()       #财政区划内码
        TradeContext.AFA101         =   records[0][1].strip()       #代理银行外码
        #TradeContext.AAA010         =   "0000000000"
        #TradeContext.AFA101         =   "011"
        TradeContext.AFA103         =   item[1].strip()             #帐号
        TradeContext.AFC601         =   HostContext.O1ACBL          #余额
        
        
        #=============与第三方通讯通讯====================
        TradeContext.__respFlag__='0'
        AfaAfeFunc.CommAfe()
        if( TradeContext.errorCode != '0000' ):
            AfaLoggerFunc.tradeInfo( TradeContext.errorCode + TradeContext.errorMsg )
            continue

    AfaLoggerFunc.tradeInfo('**********安徽非税实时上传余额信息结束**********')
    sys.exit(0)
