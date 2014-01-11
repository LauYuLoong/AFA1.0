# -*- coding: gbk -*-
##################################################################
#   代收代付平台.取消缴费交易模板（只冲主机）.
#=================================================================
#   程序文件:   4103.py
#   修改时间:   2007-10-17 
#   作    者：  ZZH
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, FSTransDtlFunc, AfaFlowControl, AfaFsFunc
import TransBillFunc, AfaHostFunc
from types import *

def main( ):
    
    AfaLoggerFunc.tradeInfo( '======进入取消缴费交易模板['+TradeContext.TemplateCode+']=====' )
        
    try:
        #=============初始化返回报文变量====================
        TradeContext.tradeResponse=[]


        #=============获取当前系统时间====================
        TradeContext.workDate = AfaUtilTools.GetSysDate( )
        TradeContext.workTime = AfaUtilTools.GetSysTime( )

        #begin 20100625 蔡永贵修改
        #TradeContext.sysId       = "AG2008"
        TradeContext.sysId       = TradeContext.appNo
        #end

        TradeContext.agentFlag   = "01"
        TradeContext.__respFlag__='0'

        #=============外调接口1====================
        subModuleExistFlag=0
        subModuleName = 'T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode
        try:
            subModuleHandle=__import__( subModuleName )
        except Exception, e:
            AfaLoggerFunc.tradeInfo( e)
        else:
            AfaLoggerFunc.tradeInfo( '执行['+subModuleName+']模块' )
            subModuleExistFlag=1
            if( not subModuleHandle.SubModuleDealFst( ) ):
                raise AfaFlowControl.flowException( )

        
        #============校验公共节点的有效性==================
        if ( not AfaFsFunc.Cancel_ChkVariableExist( ) ):
            raise AfaFlowControl.flowException( )


        #=============判断应用状态====================
        if( not AfaFsFunc.ChkAppStatus( ) ):
            raise AfaFlowControl.flowException( )


        #=============判断反交易数据是否匹配原交易====================
        if( not AfaFsFunc.ChkRevInfo( TradeContext.preAgentSerno ) ):
            raise AfaFlowControl.flowException( )


        #=============获取平台流水号====================
        if( not AfaFunc.GetSerialno( ) ):
            raise AfaFlowControl.flowException( )


        #=============转换====================
        TradeContext.channelCode = "005"
        TradeContext.userno    = TradeContext.userNo
        TradeContext.tellerno  = TradeContext.teller
        TradeContext.cashTelno = TradeContext.teller
        TradeContext.unitno    = "00000001"
        TradeContext.subUnitno = "00000000"
        if (TradeContext.catrFlag == '0'):    #现金
            TradeContext.accType = "000"
        else:
            TradeContext.accType = "001"

        #=============插入流水表====================
        if( not FSTransDtlFunc.InsertDtl( ) ):
            raise AfaFlowControl.flowException( )


        #=============与主机通讯====================
        AfaHostFunc.CommHost( )
       
        errorCode=TradeContext.errorCode


        #=============更新交易流水====================
        if( not FSTransDtlFunc.UpdateDtl( 'TRADE' ) ):
            if errorCode == '0000':
                TradeContext.errorMsg='取消交易成功 '+TradeContext.errorMsg
                
            raise AfaFlowControl.flowException( )


        #=============外调接口3====================
        if subModuleExistFlag==1 :
            if( not subModuleHandle.SubModuleDealSnd( ) ):
                TradeContext.errorMsg='取消交易成功 '+TradeContext.errorMsg
                raise AfaFlowControl.flowException( )


        #=============自动打包====================
        AfaFunc.autoPackData()

        AfaLoggerFunc.tradeInfo( '退出取消缴费交易模板['+TradeContext.TemplateCode+']' )

    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )

    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )

    except Exception, e:
        AfaFlowControl.exitMainFlow( str( e ) )
