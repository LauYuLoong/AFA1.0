# -*- coding: gbk -*-
##################################################################
#   中间业务平台.
#=================================================================
#   程序文件:   TYB001_8610.py
#   程序说明:   [8610--8000112]续期查询
#
#   修改时间:   2010-07-28
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl
import AfaHostFunc
from types import *

def SubModuleDoFst( ):

    AfaLoggerFunc.tradeInfo( '初始化续期查询交易变量' )
    
    #交易代码（8612）
    TradeContext.tradeCode = TradeContext.TransCode
    
    #保险公司代码
    if not( TradeContext.existVariable( "unitno" ) and len(TradeContext.unitno.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "不存在保险公司代码"
        raise AfaFlowControl.flowException( ) 
   
    #保险单号
    if not( TradeContext.existVariable( "policy" ) and len(TradeContext.policy.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "不存在保险单号"
        raise AfaFlowControl.flowException( )
   
    return True

def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('进入续期查询交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']与第三方通讯后处理' )
    
    try:
        names = Party3Context.getNames( )
        for name in names:
            value = getattr( Party3Context, name )
            if ( not name.startswith( '__' ) and type(value) is StringType) :
                setattr( TradeContext, name, value )
          
        if(TradeContext.errorCode=='0000'):
            TradeContext.errorMsg="续期查询成功"
        
        
        #TradeContext.syr_name1 = ''
        #syr_name = []
        #if TradeContext.existVariable('syr_name1'):
        #    syr_name.append('xiaozhang')
        #    syr_name.append('xig')
        TradeContext.O1ACUR = '1'
        #    TradeContext.syr_name = syr_name 
     
        AfaLoggerFunc.tradeInfo('退出续期查询交易与第三方通讯后处理' )    
        return True
        
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
