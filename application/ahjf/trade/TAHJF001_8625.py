# -*- coding: gbk -*-
##################################################################
#   中间业务平台.
#=================================================================
#   程序文件:   TAHJF001_8625.py
#   程序说明:   安徽交罚查询交易
#
#   修改时间:   2011-01-20
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl
import AfaHostFunc
from types import *

def SubModuleDoFst( ):

    AfaLoggerFunc.tradeInfo( '初始化处罚决定书查询交易变量' )
    
    #交易代码（8625）
    TradeContext.tradeCode = TradeContext.TransCode
    
    #处罚决定书编号
    if not( TradeContext.existVariable( "punishNo" ) and len(TradeContext.punishNo.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "处罚决定书编号不存在"
        raise AfaFlowControl.flowException( ) 
   
    return True

def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('进入安徽交罚查询交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']与第三方通讯后处理' )
    
    try:
        names = Party3Context.getNames( )
        for name in names:
            value = getattr( Party3Context, name )
            if ( not name.startswith( '__' ) and type(value) is StringType) :
                setattr( TradeContext, name, value )
          
        if(TradeContext.errorCode=='0000'):
            TradeContext.errorMsg="安徽交罚查询成功"
        
        AfaLoggerFunc.tradeInfo(TradeContext.errorMsg)
        AfaLoggerFunc.tradeInfo('退出安徽交罚查询交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']与第三方通讯后处理' )    
        return True
        
    except Exception, e:
        AfaFlowControl.ExitThisFlow( "E0001", str(e) )
