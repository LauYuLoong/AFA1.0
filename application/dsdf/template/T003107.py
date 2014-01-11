# -*- coding: gbk -*-
################################################################################
#   代收代付.客户维护模板
#===============================================================================
#   模板文件:   003107.py
#   修改时间:   2006-04-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaFlowControl,AfaDBFunc,AfaHostFunc,AfaAfeFunc
from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('******代收代付.客户维护模板[' + TradeContext.TemplateCode + ']进入******')
    
    try:
    
        #=====================初始化返回报文变量================================
        TradeContext.tradeResponse=[]


        #=====================获取当前系统时间==================================
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )
        
        #=====================判断应用系统状态==================================
        if not AfaFunc.ChkSysStatus( ) :
            raise AfaFlowControl.flowException( )
                
        #=====================外调接口(前处理)==================================
        subModuleExistFlag=0
        subModuleName = 'T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode
        try:
            subModuleHandle=__import__( subModuleName )

        except Exception, e:
            AfaLoggerFunc.tradeInfo( e )

        else:
            AfaLoggerFunc.tradeInfo( '执行['+subModuleName+']模块' )
            subModuleExistFlag=1
            if not subModuleHandle.SubModuleDoFst( ) :
                raise AfaFlowControl.flowException( )
           
                        
        #=====================判断商户状态======================================
        if not AfaFunc.ChkUnitStatus( ) :
            raise AfaFlowControl.flowException( )
            
                        
        #=====================判断渠道状态======================================
        if not AfaFunc.ChkChannelStatus( ) :
            raise AfaFlowControl.flowException( )


        #=====================获取平台流水号====================================
        if AfaFunc.GetSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )


        #校验客户信息合法性(主机)
        if( TradeContext.existVariable( "hostFlag" ) ):
            if ( TradeContext.hostFlag == '1' ):

                #判断主机接口代码是否存在
                if( not TradeContext.existVariable( "hostCode" ) ):
                    return AfaFlowControl.ExitThisFlow( 'A0001', '主机代码[hostCode]值不存在,交易失败' )

                #与主机交换
                AfaHostFunc.CommHost(TradeContext.hostCode)

                #外调接口(后处理)
                if subModuleExistFlag==1 :
                    if not subModuleHandle.SubModuleDoSnd():
                        raise AfaFlowControl.flowException( )

        #校验客户信息合法性(企业/查询/同步)
        if( TradeContext.existVariable( "corpFlag" ) ):
            if ( TradeContext.corpFlag == '1' ):

                #与通讯前置交换
                AfaAfeFunc.CommAfe()

                #外调接口(后处理)
                if subModuleExistFlag==1 :
                    if not subModuleHandle.SubModuleDoTrd():
                        raise AfaFlowControl.flowException( )

        #客户信息维护
        if ( TradeContext.existVariable( "custFlag" ) and TradeContext.custFlag=='1') :
            if ( not TradeContext.existVariable( "procType" ) ) :
                return AfaFlowControl.ExitThisFlow( 'A0001', '操作类型[procType]值不存在,交易失败' )

            if TradeContext.procType == '1' :
                #查询
                QueryCustInfo( )
                
            if TradeContext.procType == '2' :
                #新增
                AddCustInfo( )

            if TradeContext.procType == '3' :
                #修改
                UpdateCustInfo( )

            if TradeContext.procType == '4' :
                #注销
                DeleteCustInfo( )

        #=====================外调接口(后处理)==================================
        if subModuleExistFlag==1 :
            if not subModuleHandle.SubModuleDoFth():
                raise AfaFlowControl.flowException( )
                
                
        #=====================自动打包==========================================
        AfaFunc.autoPackData()

        #=====================程序退出==========================================
        AfaLoggerFunc.tradeInfo('******代收代付.客户维护模板[' + TradeContext.TemplateCode + ']退出******')
        
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )


################################################################################
def QueryCustInfo():
    AfaLoggerFunc.tradeInfo('>>>查询客户信息-协议查询')
    return True
    
def AddCustInfo():
    AfaLoggerFunc.tradeInfo('>>>新增客户信息-客户签约')
    return True

def UpdateCustInfo():
    AfaLoggerFunc.tradeInfo('>>>修改客户信息-修改协议')
    return True

def DeleteCustInfo():
    AfaLoggerFunc.tradeInfo('>>>注销客户信息-客户解约')
    return True
