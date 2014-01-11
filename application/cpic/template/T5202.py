# -*- coding: gbk -*-
################################################################################
#   代收代付.模板2.缴费模板(1.主机 2.企业)
#===============================================================================
#   模板文件:   004202.py
#   修改时间:   2006-04-06
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaAfeFunc,AfaFlowControl,TransBillFunc,AfaTransDtlFunc,Party3Context,AfaHostFunc
from types import *

def main( ):
    AfaLoggerFunc.tradeInfo('******太保缴费模板['+TradeContext.TemplateCode+']进入******')
    try:
        #=====================初始化返回报文变量================================
        TradeContext.tradeResponse=[]
        #获取当前系统时间
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )
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
                
        #=====================判断应用系统状态==================================
        if not AfaFunc.ChkSysStatus( ) :
            raise AfaFlowControl.flowException( )

        #=====================校验公共节点的有效性==============================
        if( not AfaFunc.Pay_ChkVariableExist( ) ):
            raise AfaFlowControl.flowException( )
            
        #=====================判断单位状态======================================
        if not AfaFunc.ChkUnitStatus( ) :
            raise AfaFlowControl.flowException( )
            
        #=====================判断渠道状态======================================
        if not AfaFunc.ChkChannelStatus( ) :
            raise AfaFlowControl.flowException( )
            
        #=====================判断介质状态==================================
        if not AfaFunc.ChkActStatus( ) :
            raise AfaFlowControl.flowException( )
            
        #=====================获取平台流水号====================================
        if AfaFunc.GetSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )
            
        #=====================插入流水表========================================
        if not AfaTransDtlFunc.InsertDtl( ) :
            raise AfaFlowControl.flowException( )
            
        #=====================与主机通讯========================================
        
        AfaHostFunc.CommHost()
        
        #TradeContext.__status__, TradeContext.errorCode, TradeContext.errorMsg, TradeContext.bankCode = '0','0000', '主机成功','0'
        
        #=====================更新主机返回状态==================================
        if( not AfaTransDtlFunc.UpdateDtl( 'BANK' ) ):
            if( TradeContext.__status__=='2' ):
                TradeContext.accMsg = TradeContext.errorMsg
                raise AfaFlowControl.accException( )
            raise AfaFlowControl.flowException( )
        AfaLoggerFunc.tradeInfo("更新交易状态完成")
        #=====================外调接口(中处理)==================================
        if subModuleExistFlag==1 :
            if not subModuleHandle.SubModuleDoSnd( ) :
                raise AfaFlowControl.flowException( )

        #=====================与通讯前置交换====================================
        
        AfaAfeFunc.CommAfe()
        
        #=====================更新第三方返回状态================================
        if( not AfaTransDtlFunc.UpdateDtl( 'CORP' ) ):
            if( TradeContext.__status__=='2' and TradeContext.__autoRevTranCtl__=='2' ):
                raise AfaFlowControl.flowException( )
            else:
                TradeContext.accMsg = TradeContext.errorMsg
                raise AfaFlowControl.accException( )

        #=====================外调接口(后处理)==================================
        if subModuleExistFlag==1 :
            if not subModuleHandle.SubModuleDoTrd():
                if( TradeContext.__status__=='2' and TradeContext.__autoRevTranCtl__=='2' ):
                    raise AfaFlowControl.flowException( )
                else:
                    TradeContext.accMsg = TradeContext.errorMsg
                    raise AfaFlowControl.accException( )
        
        #=====================发票信息处理======================================
        if TradeContext.errorCode=='0000' and TradeContext.existVariable( "billData" ):
            if not ( TransBillFunc.InsertBill( TradeContext.billData ) ) :
                raise AfaFlowControl.flowException( )

        #=====================自动打包==========================================
        
        AfaFunc.autoPackData()
        
        #=====================退出模板==========================================
        AfaLoggerFunc.tradeInfo('******太保缴费模板['+TradeContext.TemplateCode+']退出******')

    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )

    except AfaFlowControl.accException,e:
    
        AfaLoggerFunc.tradeInfo('自动冲正')

        #=====================自动冲正==========================================
        if ( TradeContext.__autoRevTranCtl__=='1' or TradeContext.__autoRevTranCtl__=='2' ) :
            TradeContext.revTranF='2'
            TradeContext.preAgentSerno=TradeContext.agentSerialno

            #=====================获取冲正流水号================================
            if AfaFunc.GetSerialno( ) == -1 :
                raise AfaFlowControl.exitMainFlow( )
                
            #=====================插入流水表====================================
            if not AfaTransDtlFunc.InsertDtl( ) :
                raise AfaFlowControl.exitMainFlow( )

            #=====================与主机通讯====================================
            AfaHostFunc.CommHost( )

            #=====================更新主机返回状态==============================
            if( not AfaTransDtlFunc.UpdateDtl( 'BANK' ) ):
                raise AfaFlowControl.exitMainFlow( )
                
            TradeContext.errorCode = 'A0048'
            TradeContext.errorMsg  = '[' + TradeContext.accMsg + ']交易失败,系统自动冲正成功'
            AfaFlowControl.exitMainFlow( )
        else:
            AfaFlowControl.exitMainFlow( )
            
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
