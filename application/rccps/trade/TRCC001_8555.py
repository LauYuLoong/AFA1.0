# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.本地类操作模板(1.本地操作).汇票往帐联动查询
#===============================================================================
#   交易文件:   TRCC001_8555.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  潘广通
#   修改时间:   2008-08-01
################################################################################
import rccpsDBTrcc_bilinf
import TradeContext,AfaLoggerFunc,os,AfaFlowControl
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作)交易[TRC001_8555]进入***' )
    
    #=====判断接口值是否存在====
    if( not TradeContext.existVariable( "BILRS" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '他行本行标识[BILRS]不存在')
        
    if( not TradeContext.existVariable( "BILVER" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '汇票版本号[BILVER]不存在')
        
    if( not TradeContext.existVariable( "BILNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '汇票号码[BILNO]不存在')
    
    #=====开始组织查询字典====
    where_dict={'BILRS':TradeContext.BILRS,'BILVER':TradeContext.BILVER,'BILNO':TradeContext.BILNO}
    
    #=====查询汇票信息登记簿====
    AfaLoggerFunc.tradeInfo(">>>开始查询汇票信息登记簿")
    res_bilinf=rccpsDBTrcc_bilinf.selectu(where_dict)
    if( res_bilinf == None ):
        return AfaFlowControl.ExitThisFlow('A099', '查询汇票信息登记簿失败')
        
    if( len(res_bilinf) == 0 ):
        return AfaFlowControl.ExitThisFlow('A099', '无此汇票信息')
        
    #=====增加机构号判断====
    if res_bilinf['NOTE3'] != TradeContext.BESBNO:
        return AfaFlowControl.ExitThisFlow('S999', '本汇票非本机构签发,禁止提交')
        
    #=====开始为输出接口赋值====
    TradeContext.REMBNKCO = res_bilinf['REMBNKCO']
    TradeContext.REMBNKNM = res_bilinf['REMBNKNM']
    TradeContext.PAYBNKCO = res_bilinf['PAYBNKCO']
    TradeContext.PAYBNKNM = res_bilinf['PAYBNKNM']
    TradeContext.BILDAT   = res_bilinf['BILDAT'] 
    TradeContext.BILTYP   = res_bilinf['BILTYP'] 
    TradeContext.BILNO    = res_bilinf['BILNO'] 
    TradeContext.BILVER   = res_bilinf['BILVER'] 
    TradeContext.PYRACC   = res_bilinf['PYRACC'] 
    TradeContext.PYRNAM   = res_bilinf['PYRNAM'] 
    TradeContext.PYRADDR  = res_bilinf['PYRADDR'] 
    TradeContext.CUR      = res_bilinf['CUR'] 
    TradeContext.BILAMT   = str(res_bilinf['BILAMT']) 
    TradeContext.OCCAMT   = str(res_bilinf['OCCAMT']) 
    TradeContext.RMNAMT   = str(res_bilinf['RMNAMT']) 
    TradeContext.PYEACC   = res_bilinf['PYEACC'] 
    TradeContext.PYENAM   = res_bilinf['PYENAM'] 
    TradeContext.PYEADDR  = res_bilinf['PYEADDR'] 
    TradeContext.PYHACC   = res_bilinf['PYHACC'] 
    TradeContext.PYHNAM   = res_bilinf['PYHNAM'] 
    TradeContext.PYHADDR  = res_bilinf['PYHADDR'] 
    TradeContext.USE      = res_bilinf['USE'] 
    TradeContext.REMARK   = res_bilinf['REMARK'] 
    TradeContext.SEAL     = res_bilinf['SEAL'] 
    TradeContext.HPSTAT   = res_bilinf['HPSTAT'] 
    TradeContext.PAYWAY     = res_bilinf['PAYWAY'] 
    
    TradeContext.errorCode="0000"
    TradeContext.errorMsg="查询成功"
    
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作)交易[TRC001_8555]退出***' )
    return True
