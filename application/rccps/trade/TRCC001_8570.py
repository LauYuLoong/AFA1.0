# -*- coding: gbk -*-
##################################################################
#   农信银.查询打印业务.通存通兑业务费率维护
#=================================================================
#   程序文件:   TRCC001_8570.py
#   修改时间:   2008-10-20
#   作者：      潘广通
##################################################################

import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools
import os,time,rccpsDBTrcc_chgtbl
from types import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统: 往账.本地类操作交易[RCC001_8570]进入***' )
    
    AfaLoggerFunc.tradeInfo('个性化处理(本地操作)')
    
    #=====判断接口变量是否存在====
    if not TradeContext.existVariable("BPSBNO"):
        return AfaFlowControl.ExitThisFlow('A099','法人机构号不能为空' )
        
    if not TradeContext.existVariable("OPRFLG"):
        return AfaFlowControl.ExitThisFlow('A009','操作类型不能为空')
        
    if not TradeContext.existVariable("CHGTYP"):
        return AfaFlowControl.ExitThisFlow('A009','费率代码不能为空')
        
    if not TradeContext.existVariable("TRCCO"):
        return AfaFlowControl.ExitThisFlow('A009','交易代码不能为空')

    #=====获得当前系统时间====
    TradeContext.NOW_TIME = str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
    
    #=====判断操作类型====
    if( TradeContext.OPRFLG == '0' ):
        AfaLoggerFunc.tradeInfo("通存通兑费率查询")
        
        #=====生成查询字典====
        select_dict = {'BPSBNO':TradeContext.BPSBNO,'TRCCO':TradeContext.TRCCO,'CHGTYP':TradeContext.CHGTYP}
        
        #=====查询数据库中的数据====
        AfaLoggerFunc.tradeInfo("通存通兑费率查询")
        res = rccpsDBTrcc_chgtbl.selectu(select_dict)
        if( len(res) == 0 ):
            return AfaFlowControl.ExitThisFlow('A099','查询通存通兑费率结果为空')
            
        elif( res == None ):
            return AfaFlowControl.ExitThisFlow('A099','查询通存通兑费率失败')
        
        else:    
            #=====给输出接口赋值====
            TradeContext.errorCode = "0000"
            TradeContext.errorMsg = "查询通存通兑费率成功"
            TradeContext.TRCCO    = res['TRCCO']
            TradeContext.CHGTYP   = res['CHGTYP']
            TradeContext.CHGNAM   = res['CHGNAM']
            TradeContext.CHGDATA  = res['CHGDATA']
            TradeContext.EFCTDAT  = res['EFCTDAT']
            TradeContext.INVDATE  = res['INVDATE']
            TradeContext.BPSBNO   = res['BPSBNO']
            
            
    elif( TradeContext.OPRFLG == '1' ):
        AfaLoggerFunc.tradeInfo("通存通兑费率增加")
    
        #=====判断要添加的交易的费率是否已经存在====
        AfaLoggerFunc.tradeInfo("判断要添加的交易的费率是否已经存在")
        where_dict = {}
        select_dict = {'BPSBNO':TradeContext.BPSBNO,'TRCCO':TradeContext.TRCCO,'CHGTYP':TradeContext.CHGTYP}
        res = rccpsDBTrcc_chgtbl.selectu(select_dict)
        if( len(res) != 0 ):
            return AfaFlowControl.ExitThisFlow('A099','要添加的费率种类已经存在')
    
        AfaLoggerFunc.tradeInfo("判断要添加的交易的费率不存在")
        #=====给插入字典赋值====
        insert_dict = {'BESBNO':TradeContext.BESBNO,'BPSBNO':TradeContext.BPSBNO,'TRCCO':TradeContext.TRCCO,\
                       'CHGTYP':TradeContext.CHGTYP,'CHGNAM':TradeContext.CHGNAM,'CHGDATA':TradeContext.CHGDATA,\
                       'EFCTDAT':TradeContext.EFCTDAT,'INVDATE':TradeContext.INVDATE} 
       
                       
        #=====向数据库中插入记录====
        AfaLoggerFunc.tradeInfo("通存通兑费率增加")   
        res = rccpsDBTrcc_chgtbl.insertCmt(insert_dict)
        if( res == -1 ):
            return AfaFlowControl.ExitThisFlow('A099','增加通存通兑费率失败')
            
        #=====给输出接口赋值====
        TradeContext.errorCode = "0000"
        TradeContext.errorMsg = "增加通存通兑费率成功"
        
    elif( TradeContext.OPRFLG == '2' ):
        AfaLoggerFunc.tradeInfo("通存通兑费率修改")
        
        #=====给修改字典赋值====
        update_dict = {'BESBNO':TradeContext.BESBNO,'CHGNAM':TradeContext.CHGNAM,\
                       'CHGDATA':TradeContext.CHGDATA,'EFCTDAT':TradeContext.EFCTDAT,\
                       'INVDATE':TradeContext.INVDATE,'UPDTIME':TradeContext.NOW_TIME}
                        
        where_dict = {'BPSBNO':TradeContext.BPSBNO,'TRCCO':TradeContext.TRCCO,'CHGTYP':TradeContext.CHGTYP}

        #=====修改数据库中的数据====
        AfaLoggerFunc.tradeInfo("通存通兑费率修改")
        res = rccpsDBTrcc_chgtbl.updateCmt(update_dict,where_dict)
        if( res == -1 ):
            return AfaFlowControl.ExitThisFlow('A099','修改通存通兑费率失败')
            
        #=====给输出接口赋值====
        TradeContext.errorCode = "0000"
        TradeContext.errorMsg = "修改通存通兑费率成功"

    AfaLoggerFunc.tradeInfo('个性化处理(本地操作) 退出')
    
    AfaLoggerFunc.tradeInfo( '***农信银系统: 往账.本地类操作交易[RCC001_8570]退出***' )
    
    return True      
    
        