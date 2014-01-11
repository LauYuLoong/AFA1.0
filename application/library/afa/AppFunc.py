# -*- coding: gbk -*-
##################################################################
#   中间业务平台.应用参数检查类
#=================================================================
#   程序文件:   AppFunc.py
#   修改时间:   2006-09-26
##################################################################
from types import *
import ConfigParser, time, Party3Context,AfaLoggerFunc,AfaFlowControl
import exceptions, TradeContext, AfaDBFunc, TradeException, AfaUtilTools
import AfaFunc
import os

#===========================================================================
#   功能描述：    交易参数检查
#   参数说明:    ChkCode    8位
#        每一位表示一种检查类型，1表示检查,0表示不检查；目前定义如下
#        第1位：表示是否检查应用系统状态
#        第2位：表示是否检查商户状态
#        第3位：表示是否检查应用状态
#        第4位：表示是否检查交易状态
#        第5位：表示是否检查渠道状态
#        第6位：表示是否检查缴费介质状态
#        第7位：备用
#        第8位：备用
#    检查结果：检查通过共产生以下关键参数：
#        TradeContext.sysEName    系统英文简称
#        TradeContext.sysCName    系统中文名称
#        TradeContext.__type__    系统类型
#        TradeContext.__sysMaxAmount__     单笔交易额度
#        TradeContext.__sysTotalamount__   日累计交易额度
#        TradeContext.__channelMode__      渠道管理模式
#        TradeContext.__actnoMode__        缴费介质管理模式
#    
#        TradeContext.unitName     商户名称
#        TradeContext.unitSName    商户简称
#        TradeContext.__bankMode__    银行角色
#        TradeContext.__busiMode__    业务模式
#        TradeContext.__accMode__     账户模式
#        TradeContext.bankCode        银行编码
#        TradeContext.__agentEigen__  商户特征码
#        TradeContext.__signFlag__    签到标志
#        TradeContext.bankUnitno      银行商户代码（商户号）
#        TradeContext.mainZoneno      主办分行号
#        TradeContext.mainBrno        主办网点号
#        
#        TradeContext.subUnitName     商户分支单位名称
#        TradeContext.subUnitSName    商户分支单位简称
#        
#        TradeContext.__abstract__    交易摘要码(note1)
#        TradeContext.__prtAbs__      SASB打印摘要码(note2)
#        
#        TradeContext.__tradeMode__       交易模式
#        TradeContext.__bankReq__         银行发起标志
#        TradeContext.__unitReq__         商户发起标志
#        TradeContext.__accPwdFlag__      密码校验标志
#        TradeContext.__tradePwdFlag__    交易密码校验标志
#        TradeContext.__channelCode__     渠道掩码
#        TradeContext.__errType__         错误处理类型0：不处理,1：重发,2：冲正
#        
#        TradeContext.__agentBrno__        外围系统网点号
#        TradeContext.__agentTeller__      外围系统出纳员号
#        TradeContext.__chanlMaxAmount__   渠道单笔交易额度
#        TradeContext.__chanlTotalAmount__ 渠道日累计交易额度
#        TradeContext.__billSaveCtl__      发票保存标志
#        TradeContext.__autoRevTranCtl__   自动冲帐标志
#        TradeContext.__errChkCtl__        异常交易检测标志
#        TradeContext.__autoChkAcct__      自动检查帐户类型
#        TradeContext.__chkAccPwdCtl__     校验帐户密码标志
#        TradeContext.__enpAccPwdCtl__     帐户密码加密标志
#        TradeContext.__hostType__         主机标志

#==========================================================================   
def ChkParam(ChkCode='11111111'):

    if ChkCode[0]=='1':
    	#===============判断应用系统状态======================
    	if not AfaFunc.ChkSysStatus( ) :
    		raise AfaFlowControl.flowException( )
    		    
    if ChkCode[1]=='1':
    	#===============判断商户状态======================
    	if not AfaFunc.ChkUnitStatus( ) :
    		raise AfaFlowControl.flowException( )

    if ChkCode[2]=='1':
        #=============判断交易状态=====================
        if not AfaFunc.ChkTradeStatus( ) :
            raise AfaFlowControl.flowException( )

    if ChkCode[3]=='1':
    	#=============判断渠道状态====================
    	if not AfaFunc.ChkChannelStatus( ) :
    		raise AfaFlowControl.flowException( )

    if ChkCode[4]=='1':
    	#=============判断缴费介质状态====================
    	if not AfaFunc.ChkActStatus( ) :
    		raise AfaFlowControl.flowException( )

    return True
