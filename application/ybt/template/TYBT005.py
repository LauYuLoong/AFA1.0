# -*- coding: gbk -*-
################################################################################
#   银保通.冲正模板.不去第三方，只去主机
#===============================================================================
#   模板文件:   YBT005.py
#   修改时间:   2010-08-18
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,Party3Context,AfaTransDtlFunc,AfaAfeFunc,AfaFlowControl,AfaHostFunc,TransBillFunc
from types import *

def main( ):
    AfaLoggerFunc.tradeInfo('******银保通行内冲正模板['+TradeContext.TemplateCode+']进入******')
    try:

        #=====================初始化返回报文变量================================
        TradeContext.tradeResponse=[]

        #获取当前系统时间
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )

        #=====================判断应用系统状态==================================
        if not AfaFunc.ChkSysStatus( ) :
            raise AfaFlowControl.flowException( )
                
        #=====================外调接口(前处理)==================================
        subModuleExistFlag = 0
        subModuleName = 'T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode
        try:
            subModuleHandle=__import__( subModuleName )
        except Exception, e:
            AfaLoggerFunc.tradeInfo( e)
        else:
            AfaLoggerFunc.tradeInfo( '执行['+subModuleName+']模块' )
            subModuleExistFlag=1
            if not subModuleHandle.SubModuleDoFst( ) :
                raise AfaFlowControl.flowException( )
                

        #=====================校验公共节点的有效性==============================
        if( not AfaFunc.Cancel_ChkVariableExist( ) ):
            raise AfaFlowControl.flowException( )

        #=====================判断商户状态======================================
        if not AfaFunc.ChkUnitStatus( ) :
            raise AfaFlowControl.flowException( )

        #=====================判断渠道状态======================================
        if not AfaFunc.ChkChannelStatus( ) :
            raise AfaFlowControl.flowException( )
        
        #=====================判断反交易数据是否匹配原交易======================
        if( not AfaFunc.ChkRevInfo( ) ):
            raise AfaFlowControl.flowException( )

        #=====================获取平台流水号====================================
        if AfaFunc.GetSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )

        #=====================插入流水表========================================
        if( not AfaTransDtlFunc.InsertDtl( ) ):
            raise AfaFlowControl.flowException( )

        #=====================与主机交换========================================
        AfaHostFunc.CommHost()

        #=====================更新交易流水======================================
        if( not AfaTransDtlFunc.UpdateDtl( 'TRADE' ) ):
            if TradeContext.errorCode == '0000':
                TradeContext.errorMsg='取消交易成功 '+TradeContext.errorMsg
                
            raise AfaFlowControl.flowException( )

        #=====================自动打包==========================================
        AfaFunc.autoPackData()

        #=====================程序退出==========================================
        AfaLoggerFunc.tradeInfo('******银保通行内冲正模板['+TradeContext.TemplateCode+']退出******')

    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
        
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
        
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
