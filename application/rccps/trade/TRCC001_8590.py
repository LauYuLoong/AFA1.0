# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.本地类操作(1.本地操作).通存通兑错帐处理标识维护
#===============================================================================
#   模板文件:   TRCC001_8590.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘振东
#   修改时间:   2008-12-30
################################################################################

import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools
import os,time,rccpsDBTrcc_tddzcz
from types import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统: 往账.本地类操作交易[RCC001_8590]通存通兑错帐处理标识维护进入***' )
    
    AfaLoggerFunc.tradeInfo('个性化处理(本地操作)')
    
    #=====判断接口变量是否存在====
    if not TradeContext.existVariable("SNDBNKCO"):
        return AfaFlowControl.ExitThisFlow('A099','发送行号不能为空' )
        
    if not TradeContext.existVariable("TRCDAT"):
        return AfaFlowControl.ExitThisFlow('A009','委托日期不能为空')
        
    if not TradeContext.existVariable("TRCNO"):
        return AfaFlowControl.ExitThisFlow('A009','交易流水号不能为空')
        
    if not TradeContext.existVariable("BJEDTE"):
        return AfaFlowControl.ExitThisFlow('A009','报单日期不能为空')
        
    if not TradeContext.existVariable("BSPSQN"):
        return AfaFlowControl.ExitThisFlow('A009','报单序号不能为空')
    
    AfaLoggerFunc.tradeInfo('个性化处理结束(本地操作)') 
       
    #=====给修改字典赋值====
    update_dict = {'ISDEAL':'1','NOTE3':'本行未做账务处理,直接修改错账处理标识为已处理'}
                    
    where_dict = {'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO,\
                  'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}
    
#    #=====判断处理标识类型====                                     
#    if( TradeContext.ISDEAL == '1' ):                              
#        return AfaFlowControl.ExitThisFlow('S999','此处理标识非零')
#    else:                                                          
#        pass                                                       

    tddzcz_dict = {}
    tddzcz_dict = rccpsDBTrcc_tddzcz.selectu(where_dict)
    if tddzcz_dict == None:
        return AfaFlowControl.ExitThisFlow('S999','查询此错账信息异常')
        
    if len(tddzcz_dict) <= 0:
        return AfaFlowControl.ExitThisFlow('S999','错账登记簿中无此错账')
        
    if tddzcz_dict['ISDEAL'] == '1':
        return AfaFlowControl.ExitThisFlow('S999','此错账错账处理标识为已处理,禁止提交')

    #=====修改数据库中的数据====
    AfaLoggerFunc.tradeInfo("通存通兑错帐处理标识修改")
    res = rccpsDBTrcc_tddzcz.updateCmt(update_dict,where_dict)
    if( res == -1 ):
        return AfaFlowControl.ExitThisFlow('A099','修改通存通兑错帐处理标识失败')
    elif( res == 0 ):
        return AfaFlowControl.ExitThisFlow('A099','交易记录不存在')
    
    #=====给输出接口赋值====
    TradeContext.errorCode = "0000"
    TradeContext.errorMsg  = "修改通存通兑错帐处理标识成功"
    TradeContext.ISDEAL    = '1'

    AfaLoggerFunc.tradeInfo( '***农信银系统: 往账.本地类操作交易[RCC001_8590]通存通兑错帐处理标识维护退出***' )
    
    return True      