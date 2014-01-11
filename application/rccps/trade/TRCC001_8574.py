# -*- coding: gbk -*-
##################################################################
#   农信银.查询打印业务.手续费联动查询交易
#=================================================================
#   程序文件:   TRCC001_8574.py
#   修改时间:   2008-10-20
#   作者：      潘广通
##################################################################

import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools
import os,rccpsDBTrcc_chgtbl
from types import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统: 往账.本地类操作交易[RCC001_8574]进入***' )
    
    AfaLoggerFunc.tradeInfo('个性化处理(本地操作)')
    
    #=====判断接口变量是否存在====
    if not TradeContext.existVariable("BPSBNO"):
        return AfaFlowControl.ExitThisFlow('A099','法人机构号不能为空' )
        
    if not TradeContext.existVariable("TRCCO"):
        return AfaFlowControl.ExitThisFlow('A099','交易代码不能为空' )
        
    #=====定义变量====
    FeiLv = 0
    ShangXian = 0
    XiaXian = 0
    
    #=====查询费率====
    AfaLoggerFunc.tradeInfo("开始查询费率")
    
    #=====组织查询字典====
    where_dict = {'BPSBNO':TradeContext.BPSBNO,'TRCCO':TradeContext.TRCCO,'CHGTYP':'0'}
    
    #=====查询数据库====
    AfaLoggerFunc.tradeInfo("查询费率维护表，得到费率")
    res = rccpsDBTrcc_chgtbl.selectu(where_dict)
    if( len(res) == 0 ):
        return AfaFlowControl.ExitThisFlow('A099','查询通存通兑费率结果为空')
            
    elif( res == None ):
        return AfaFlowControl.ExitThisFlow('A099','查询通存通兑费率失败')
        
    else:  
        FeiLv = float(res['CHGDATA']) * float(TradeContext.OCCAMT)  
        
        AfaLoggerFunc.tradeInfo("费率为：" + str(FeiLv))
        
    #=====查询费率上限====
    AfaLoggerFunc.tradeInfo("开始查询费率上限")
    
    #=====组织查询字典====
    where_dict = {'BPSBNO':TradeContext.BPSBNO,'TRCCO':TradeContext.TRCCO,'CHGTYP':'1'}
    
    #=====查询数据库====
    AfaLoggerFunc.tradeInfo("查询费率维护表，得到费率上限")
    res = rccpsDBTrcc_chgtbl.selectu(where_dict)
    if( len(res) == 0 ):
        return AfaFlowControl.ExitThisFlow('A099','查询通存通兑费率上限结果为空')
            
    elif( res == None ):
        return AfaFlowControl.ExitThisFlow('A099','查询通存通兑费率上限失败')
        
    else: 
        ShangXian = float(res['CHGDATA']) 
        AfaLoggerFunc.tradeInfo("上限为：" + str(ShangXian))
        
        
    #=====查询费率下限====
    AfaLoggerFunc.tradeInfo("开始查询费率下限")
    
    #=====组织查询字典====
    where_dict = {'BPSBNO':TradeContext.BPSBNO,'TRCCO':TradeContext.TRCCO,'CHGTYP':'2'}
    
    #=====查询数据库====
    AfaLoggerFunc.tradeInfo("查询费率维护表，得到费率下限")
    res = rccpsDBTrcc_chgtbl.selectu(where_dict)
    if( len(res) == 0 ):
        return AfaFlowControl.ExitThisFlow('A099','查询通存通兑费率下限结果为空')
            
    elif( res == None ):
        return AfaFlowControl.ExitThisFlow('A099','查询通存通兑费率下限失败')
        
    else: 
        XiaXian = float(res['CHGDATA']) 
        AfaLoggerFunc.tradeInfo("下限为：" + str(XiaXian))      
        
    #=====通过比较得出费率====
    AfaLoggerFunc.tradeInfo("通过比较得出费率")
    
    if( FeiLv >= ShangXian ):
        Commission = ShangXian
        
    elif( FeiLv <= XiaXian ):
        Commission = XiaXian
        
    else:
        Commission = FeiLv
        
    #=====给输出接口赋值====
    TradeContext.CUSCHRG = str(Commission)
    AfaLoggerFunc.tradeInfo("CUSCHRG=" + TradeContext.CUSCHRG)
    
    TradeContext.errorCode = "0000"
    TradeContext.errorMsg = "查询成功"
    
    AfaLoggerFunc.tradeInfo('个性化处理(本地操作) 退出')
    
    AfaLoggerFunc.tradeInfo( '***农信银系统: 往账.本地类操作交易[RCC001_8574]退出***' )
    
    return True