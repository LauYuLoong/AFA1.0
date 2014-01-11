# -*- coding: gbk -*-
##################################################################
#   财税库行横向联网.取消缴费交易模板（只冲主机）.
#=================================================================
#   程序文件:   TPS003.py
#   修改时间:   2008-5-2 10:24
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools, TipsFunc
from types import *

def main( ):
    AfaLoggerFunc.tradeInfo( '======进入取消缴费交易模板['+TradeContext.TemplateCode+']=====' )
    try:
        #=============初始化返回报文变量====================
        TradeContext.tradeResponse=[]
        
        #=============获取当前系统时间====================
        if not (TradeContext.existVariable( "workDate" ) and len(TradeContext.workDate)>0):
            TradeContext.workDate = UtilTools.GetSysDate( )
        TradeContext.workTime = UtilTools.GetSysTime( )
        TradeContext.appNo      ='AG2010'
        TradeContext.busiNo     ='00000000000001'
        
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
                raise TipsFunc.flowException( )

        #============校验公共节点的有效性==================
        if ( not TipsFunc.Cancel_ChkVariableExist( ) ):
            raise TipsFunc.flowException( )

        #=============判断应用状态====================
        if( not TipsFunc.ChkAppStatus( ) ):
            raise TipsFunc.flowException( )

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

        #=============外调接口3====================
        if subModuleExistFlag==1 :
            if( not subModuleHandle.SubModuleDealSnd( ) ):
                TradeContext.errorMsg='取消交易成功 '+TradeContext.errorMsg
                raise TipsFunc.flowException( )

        #=============自动打包====================
        TipsFunc.autoPackData()
        
        AfaLoggerFunc.tradeInfo( '退出取消缴费交易模板['+TradeContext.TemplateCode+']' )
        
    except TipsFunc.flowException, e:
        # print e
        TipsFunc.exitMainFlow( )
    except TipsFunc.accException:
        # print e
        TipsFunc.exitMainFlow( )
    except Exception, e:
        # print e
        TipsFunc.exitMainFlow( str( e ) )
