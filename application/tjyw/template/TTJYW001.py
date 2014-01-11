# -*- coding: gbk -*-
################################################################################
#   银保通.缴费模板.只去主机
#===============================================================================
#   模板文件:   TZHHF001.py
#   修改时间:   2011-01-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaFlowControl,TransBillFunc,AfaTransDtlFunc
import AfaTjFunc,AfaHostFunc

from types import *

def main( ):
    AfaLoggerFunc.tradeInfo('******统缴业务缴费模板['+TradeContext.TemplateCode+']进入******')
    try:
        #=====================初始化返回报文变量================================
        TradeContext.tradeResponse=[]
        
        #获取当前系统时间
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )
        
        #=====================判断应用系统状态==================================
    
        if not AfaFunc.ChkSysStatus( ) :
            raise AfaFlowControl.flowException( ) 
    
        
    #20120711陈浩注释，添加 
    #begin      
        #添加 
        #=====================判断单位状态======================================
        if not AfaTjFunc.ChkUnitInfo( ):
            raise AfaFlowControl.flowException( )
        
        
        
        #=====================外调接口(处理)==================================                       
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
        if( not AfaFunc.Pay_ChkVariableExist( ) ):
            raise AfaFlowControl.flowException( )
            
        #=====================判断单位状态======================================   
    #    if not AfaFunc.ChkUnitStatus( ) :
    #        raise AfaFlowControl.flowException( )
    #
    #    #=====================判断渠道状态======================================
    #    if not AfaFunc.ChkChannelStatus( ) :
    #        raise AfaFlowControl.flowException( )
    #        
    #    #=====================判断介质状态=====================================
    #    if not AfaFunc.ChkActStatus( ) :
    #        raise AfaFlowControl.flowException( )
    
        #=====================判断单位状态======================================
        if not AfaTjFunc.ChkUnitInfo( ):
            raise AfaFlowControl.flowException( )
        
        #======================================================================
        TradeContext.__agentEigen__ = "00000000"
        
   #end      
        #=====================获取平台流水号====================================
        if AfaFunc.GetSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )
              
        #=====================插入流水表========================================
        if not AfaTransDtlFunc.InsertDtl( ) :
            raise AfaFlowControl.flowException( )
            
        #=====================与主机通讯========================================
        
        AfaHostFunc.CommHost()
        
        #=====================更新主机返回状态==================================
        if( not AfaTransDtlFunc.UpdateDtl( 'TRADE' ) ):
            if( TradeContext.__status__=='2' ):
                TradeContext.accMsg = TradeContext.errorMsg
                raise AfaFlowControl.accException( )
            raise AfaFlowControl.flowException( )
                   
        #=====================发票信息处理======================================
        if TradeContext.errorCode=='0000' and TradeContext.existVariable( "billData" ):
            if not ( TransBillFunc.InsertBill( TradeContext.billData ) ) :
                raise AfaFlowControl.flowException( )
        
        TradeContext.errorCode='0000'
        #=====================自动打包==========================================
        
        AfaFunc.autoPackData()
        
        #=====================退出模板==========================================
        AfaLoggerFunc.tradeInfo('******统缴业务缴费模板['+TradeContext.TemplateCode+']退出******')
    
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )

    except AfaFlowControl.accException,e:
    
        AfaLoggerFunc.tradeInfo('冲正异常信息: ' + str(e))
        AfaLoggerFunc.tradeInfo('自动冲正')

        TradeContext.__autoRevTranCtl__ = "1"      #允许自动冲账

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
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            
            AfaFlowControl.exitMainFlow( )
        else:
            AfaFlowControl.exitMainFlow( )
            
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
