# -*- coding: gbk -*-
##################################################################
#   代收代付平台.财税库行横向联网.柜面缴费冲正
#=================================================================
#   程序文件:   TPS001_8454.py
#   修改时间:   2007-10-23
##################################################################

import TradeContext, UtilTools, AfaFlowControl
#, os, AfaLoggerFunc，LoggerHandler, 
import AfaAfeFunc,TipsFunc

def SubModuleMainFst( ):
    TradeContext.appNo  =   'AG2010'
    TradeContext.busiNo =   '00000000000001'
    TradeContext.__agentEigen__='0'
    try:
        #=============初始化返回报文变量====================
        TradeContext.tradeResponse=[]
        
        #=============获取当前系统时间====================
        TradeContext.workDate = UtilTools.GetSysDate( )
        TradeContext.workTime = UtilTools.GetSysTime( )

        #============校验公共节点的有效性==================
        if ( not TipsFunc.Cancel_ChkVariableExist( ) ):
            raise AfaFlowControl.flowException( )

        #=============判断应用状态====================
        if( not TipsFunc.ChkAppStatus( ) ):
            raise AfaFlowControl.flowException( )
        
        ##检查征收机关，获取贷方信息
        #if not TipsFunc.ChkTaxOrgCode():
        #    return False
        
        #=============判断反交易数据是否匹配原交易====================
        if( not TipsFunc.ChkRevInfo( TradeContext.preAgentSerno ) ):
            raise AfaFlowControl.flowException( )
        
        #=============获取平台流水号====================
        if( not TipsFunc.GetSerialno( ) ):
            raise AfaFlowControl.flowException( )

        #=============插入流水表====================
        if( not TipsFunc.InsertDtl( ) ):
            raise AfaFlowControl.flowException( )

        #=============与第三方通讯====================
        AfaAfeFunc.CommAfe( )

        #=============更新交易流水====================
        if( not TipsFunc.UpdateDtl( 'CORP' ) ):
            raise AfaFlowControl.flowException( )

        #=============与主机通讯====================
        TipsFunc.CommHost( )
        #TradeContext.errorCode, TradeContext.errorMsg = '0000', '主机成功'
        #TradeContext.bankSerno = '10000000'        #柜员流水号
        #TradeContext.bankCode  = 'AAAAAAA'        #主机返回代码
        #TradeContext.__status__='0'
        
        errorCode=TradeContext.errorCode

        #=============更新交易流水====================
        if( not TipsFunc.UpdateDtl( 'BANK' ) ):
            if errorCode == '0000':
                TradeContext.errorMsg='取消交易成功 '+TradeContext.errorMsg
            raise AfaFlowControl.flowException( )

        #=============更新发票信息为作废====================
        if( not TransBillFunc.UpdateBill( ) ):
            TradeContext.errorMsg='取消交易成功 '+TradeContext.errorMsg
            raise AfaFlowControl.flowException( )

    except AfaFlowControl.flowException, e:
        return False
    except Exception, e:
        return AfaFlowControl.ExitThisFlow('A9999','系统异常'+str(e) )
    return True
 
def SubModuleMainSnd ():
    return True
