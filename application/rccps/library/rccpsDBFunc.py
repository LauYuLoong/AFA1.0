# -*- coding: gbk -*-
################################################################################
#   农信银系统.公共数据库操作模块
#===============================================================================
#   程序文件:   rccpsDBFunc.py
#   作    者:   关彬捷
#   修改时间:   2006-03-31
################################################################################

import TradeContext,AfaLoggerFunc,AfaDBFunc,AfaUtilTools,TradeContext,AfaFlowControl
from types import *
from rccpsConst import *
import rccpsDBTrcc_trcbka,rccpsDBTrcc_bilbka,rccpsDBTrcc_bilinf,rccpsDBTrcc_errinf,rccpsDBTrcc_wtrbka,rccpsDBTrcc_mpcbka,rccpsDBTrcc_pamtbl
import rccpsState
import rccpsMap0000Dtrcbka2Dtrc_dict,rccpsMap0000Dstat_dict2Dtrc_dict
import rccpsMap0000Dtrc_dict2Dtrcbka
import rccpsMap0000Dbilbka2Dbil_dict,rccpsMap0000Dstat_dict2Dbil_dict
import rccpsMap0000Dbil_dict2Dbilbka    
import rccpsMap0000Dbilinf2Dbil_dict
import rccpsMap0000Dbil_dict2Dbilinf
import rccpsMap0000Dwtrbka2Dwtr_dict,rccpsMap0000Dstat_dict2Dwtr_dict,rccpsMap0000Dwtr_dict2Dwtrbka,rccpsMap0000Dmpcbka2Dmpc_dict

################################################################################
# 函数名:    getTransTrc                                             
# 参数:      BJEDTE:交易日期(必输),BSPSQN:报单序号(必输)             
# 返回值：   成功    trc_dict(汇兑业务交易详细信息,即trcbka表内容+sstlog表内容)
#            失败    False                                           
# 函数说明： 查询汇兑业务登记簿及当前状态相关信息                    
################################################################################
                                                                     
def getTransTrc(BJEDTE,BSPSQN,trc_dict):
    AfaLoggerFunc.tradeInfo( ">>>开始查询汇兑业务登记簿[" + BJEDTE + "][" + BSPSQN + "]交易信息" )
                                                                     
    #==========组织查询条件=====================================================
    trcbka_where_dict = {'BJEDTE':BJEDTE,'BSPSQN':BSPSQN}            
                                                                     
    #==========查询汇兑登记簿相关业务信息=======================================
    trcbka_dict = rccpsDBTrcc_trcbka.selectu(trcbka_where_dict)  
    
    if trcbka_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '查询汇兑业务登记簿交易信息异常' )
        
    if len(trcbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow( 'S999', '汇兑业务登记簿中无此交易信息' )
    
    #==========将查询出的汇兑登记簿相关业务信息赋值到输出字典===================
    if not rccpsMap0000Dtrcbka2Dtrc_dict.map(trcbka_dict,trc_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的汇兑登记簿相关业务信息赋值到输出字典异常' )
        
    #==========查询当前业务状态=================================================
    AfaLoggerFunc.tradeInfo( ">>>开始查询交易[" + BJEDTE + "][" + BSPSQN + "]当前状态" )
    
    stat_dict = {}
    
    if not rccpsState.getTransStateCur(BJEDTE,BSPSQN,stat_dict):
        return False
        
    AfaLoggerFunc.tradeInfo( ">>>结束查询交易[" + BJEDTE + "][" + BSPSQN + "]当前状态" )

    #==========将查询出的业务状态详细信息赋值到输出字典=========================
    if not rccpsMap0000Dstat_dict2Dtrc_dict.map(stat_dict,trc_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的业务状态详细信息赋值到输出字典异常' )
    
    AfaLoggerFunc.tradeInfo( ">>>结束查询汇兑业务登记簿[" + BJEDTE + "][" + BSPSQN + "]交易信息" )
    return True

################################################################################
# 函数名:    insTransTrc
# 参数:      trc_dict(汇兑业务交易详细信息)
# 返回值：   成功    True
#            失败    False
# 函数说明： 登记汇兑业务登记簿及状态相关信息
################################################################################
def insTransTrc(trc_dict):
    
    AfaLoggerFunc.tradeInfo( ">>>开始登记汇兑业务登记簿[" + trc_dict["BJEDTE"] + "][" + trc_dict["BSPSQN"] + "]交易信息及相关状态" )
    
    if not trc_dict.has_key("BJEDTE"):
        return AfaFlowControl.ExitThisFlow( 'S999',"登记汇兑业务登记簿,BJEDTE不能为空")
        
    if not trc_dict.has_key("BSPSQN"):
        return AfaFlowControl.ExitThisFlow( 'S999',"登记汇兑业务登记簿,BSPSQN不能为空")
        
    
    #==========将输入字典赋值到汇兑业务登记簿字典==============================
    trcbka_dict = {}
    
    if not rccpsMap0000Dtrc_dict2Dtrcbka.map(trc_dict,trcbka_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '将输入字典赋值到汇兑业务登记簿字典异常' )
        
    #==========登记信息到汇兑登记簿============================================
    ret = rccpsDBTrcc_trcbka.insert(trcbka_dict)
    
    if ret <= 0:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '登记汇兑业务详细信息到汇兑业务登记簿异常' )
        
    AfaLoggerFunc.tradeInfo("插入成功")
    #==========登记初始状态====================================================
    if not rccpsState.newTransState(trc_dict["BJEDTE"],trc_dict["BSPSQN"],PL_BCSTAT_INIT,PL_BDWFLG_SUCC):
        return False
    
    AfaLoggerFunc.tradeInfo( ">>>结束登记汇兑业务登记簿[" + trc_dict["BJEDTE"] + "][" + trc_dict["BSPSQN"] + "]交易信息及相关状态" )
    return True
    
    
################################################################################
# 函数名:    GetTransBil
# 参数:      BJEDTE:交易日期(必输),BSPSQN:报单序号(必输)
# 返回值：   成功    bil_dict(汇票业务交易详细信息,即bilbka表内容+sstlog表内容)
#            失败    False
# 函数说明： 查询汇票业务登记簿及当前状态相关信息
################################################################################

def getTransBil(BJEDTE,BSPSQN,bil_dict):
    AfaLoggerFunc.tradeInfo( ">>>开始查询汇票业务登记簿[" + BJEDTE + "][" + BSPSQN + "]交易信息" )
    
    #==========组织查询条件=====================================================
    bilbka_where_dict = {'BJEDTE':BJEDTE,'BSPSQN':BSPSQN}

    #==========查询汇票业务登记簿相关业务信息===================================
    bilbka_dict = rccpsDBTrcc_bilbka.selectu(bilbka_where_dict)
    
    if bilbka_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '获取汇票业务登记簿详细信息异常' )
        
    if len(bilbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow( 'S999', '汇兑业务登记簿中无此交易详细信息' )
        
    AfaLoggerFunc.tradeInfo( ">>>结束查询汇票业务登记簿[" + BJEDTE + "][" + BSPSQN + "]交易信息" )

    #==========将查询出的汇票业务登记簿相关业务信息赋值到输出字典===============
    if not rccpsMap0000Dbilbka2Dbil_dict.map(bilbka_dict,bil_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的汇票业务登记簿相关业务信息赋值到输出字典异常' )

    #==========查询当前业务状态=================================================
    AfaLoggerFunc.tradeInfo( ">>>开始查询交易[" + BJEDTE + "][" + BSPSQN + "]当前业务状态" )
    
    stat_dict = {}
    if not rccpsState.getTransStateCur(BJEDTE,BSPSQN,stat_dict):
        return False
    
    AfaLoggerFunc.tradeInfo( ">>>结束查询交易[" + BJEDTE + "][" + BSPSQN + "]当前业务状态" )

    #==========将查询出的业务状态详细信息赋值到输出字典=========================
    if not rccpsMap0000Dstat_dict2Dbil_dict.map(stat_dict,bil_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的业务状态详细信息赋值到输出字典异常' )
    
    AfaLoggerFunc.tradeInfo( ">>>结束查询汇票业务登记簿[" + BJEDTE + "][" + BSPSQN + "]交易信息" )
    return True

################################################################################
# 函数名:    insTransBil
# 参数:      bil_dict(汇票业务交易详细信息)
# 返回值：   成功    True
#            失败    False
# 函数说明： 登记汇票业务登记簿及状态相关信息
################################################################################
def insTransBil(bil_dict):
    
    AfaLoggerFunc.tradeInfo( ">>>开始登记汇票业务登记簿[" + bil_dict["BJEDTE"] + "][" + bil_dict["BSPSQN"] + "]交易信息及相关状态" )
    if not bil_dict.has_key("BJEDTE"):
        return AfaFlowControl.ExitThisFlow( 'S999',"登记汇票业务登记簿,BJEDTE不能为空")
        
    if not bil_dict.has_key("BSPSQN"):
        return AfaFlowControl.ExitThisFlow( 'S999',"登记汇票业务登记簿,BSPSQN不能为空")
        
    
    #==========将输入字典赋值到汇票业务登记簿字典===============================
    bilbka_dict = {}
    
    if not rccpsMap0000Dbil_dict2Dbilbka.map(bil_dict,bilbka_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '将输入字典赋值到汇票业务登记簿字典异常' )
        
    #==========登记信息到汇票业务登记簿=========================================
    ret = rccpsDBTrcc_bilbka.insert(bilbka_dict)
    
    if ret <= 0:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '登记汇票业务登记簿汇票业务详细信息异常' )
    
    #==========登记初始状态=====================================================
    if not rccpsState.newTransState(bil_dict["BJEDTE"],bil_dict["BSPSQN"],PL_BCSTAT_INIT,PL_BDWFLG_SUCC):
        return False
        
    AfaLoggerFunc.tradeInfo( ">>>结束登记汇票业务登记簿[" + bil_dict["BJEDTE"] + "][" + bil_dict["BSPSQN"] + "]交易信息及相关状态" )
    return True


################################################################################
# 函数名:    getInfoBil
# 参数:      BILVER:汇票版本号,BILNO:汇票号码,BILRS:汇票行内行外标识
# 返回值：   成功    bilinf_dict(汇兑信息交易详细信息,即bilinf表内容)
#            失败    False
# 函数说明： 查询汇票信息登记簿相关信息
################################################################################
def getInfoBil(BILVER,BILNO,BILRS,bil_dict):
    AfaLoggerFunc.tradeInfo( ">>>开始查询汇票信息登记簿[" + BILVER + "][" + BILNO + "][" + BILRS + "]交易信息" )
    
    #===========组织查询条件=====================================================
    bilinf_where_dict = {'BILVER':BILVER,'BILNO':BILNO,'BILRS':BILRS}

    #===========查询汇票信息登记簿相关信息=======================================
    bilinf_dict = rccpsDBTrcc_bilinf.selectu(bilinf_where_dict)
    
    if bilinf_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '获取汇票信息登记簿汇票信息异常' )
    
    if len(bilinf_dict) <= 0:
        return AfaFlowControl.ExitThisFlow( 'S999', '汇票信息登记簿中无此汇票信息' )
        
    AfaLoggerFunc.tradeInfo( ">>>结束查询汇票信息登记簿[" + BILVER + "][" + BILNO + "][" + BILRS + "]交易信息" )

    #===========将查询出的汇票信息登记簿相关信息赋值到输出字典===================
    if not rccpsMap0000Dbilinf2Dbil_dict.map(bilinf_dict,bil_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的汇票信息登记簿相关信息赋值到输出字典异常' )
    
    return True
    
    
################################################################################
# 函数名:    insInfoBil
# 参数:      bil_dict(汇票信息详细信息)
# 返回值：   成功    True
#            失败    False
# 函数说明： 登记汇票信息登记簿相关信息
################################################################################
def insInfoBil(bil_dict):
    
    AfaLoggerFunc.tradeInfo( ">>>开始登记汇票信息登记簿[" + bil_dict["BILVER"] + "][" + bil_dict["BILNO"] + "][" + bil_dict["BILRS"] + "]交易信息及相关状态" )
    if not bil_dict.has_key("BILVER"):
        return AfaFlowControl.ExitThisFlow("S999","登记汇票信息登记簿,BILVER不能为空")
        
    if not bil_dict.has_key("BILNO"):
        return AfaFlowControl.ExitThisFlow("S999","登记汇票信息登记簿,BILNO不能为空")
    
    if not bil_dict.has_key("BILRS"):
        return AfaFlowControl.ExitThisFlow("S999","登记汇票信息登记簿,BILRS不能为空")
        
    
    
    #===========将输入字典赋值到汇票信息登记簿字典==============================
    bilinf_dict = {}
    
    if not rccpsMap0000Dbil_dict2Dbilinf.map(bil_dict,bilinf_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '将输入字典赋值到汇票信息登记簿字典异常' )
    
    
    bilinf_where_dict = {}
    bilinf_where_dict['BILRS']  = bil_dict['BILRS']
    bilinf_where_dict['BILVER'] = bil_dict['BILVER']
    bilinf_where_dict['BILNO']  = bil_dict['BILNO']
    
    tmp_bilinf_dict = rccpsDBTrcc_bilinf.selectu(bilinf_where_dict)
    if tmp_bilinf_dict == None:
        return AfaFlowControl.ExitThisFlow( 'S999', '校验汇票信息登记簿是否存在相同汇票异常' )
    
    if len(tmp_bilinf_dict) <= 0:
        AfaLoggerFunc.tradeError("汇票信息登记簿不存在此汇票,插入汇票信息")
    
        #===========登记信息到汇票信息登记簿========================================
        ret = rccpsDBTrcc_bilinf.insert(bilinf_dict)
        if ret <= 0:
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow( 'S999', '登记汇票详细信息异常' )
        
        return True
    else:
        AfaLoggerFunc.tradeError("汇票信息登记簿存在此汇票,更新汇票信息")
    
        #===========登记信息到汇票信息登记簿========================================
        ret = rccpsDBTrcc_bilinf.update(bilinf_dict,bilinf_where_dict)
        if ret <= 0:
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow( 'S999', '登记汇票详细信息异常' )
        
        return True
    
################################################################################
# 函数名:    getTransTrcPK
# 参数:      SNDMBRCO:发送成员行号,TRCDAT:委托日期,TRCNO:交易流水号,trc_dict(汇兑业务交易详细信息,即trcbka表内容+sstlog表内容)
# 返回值：   成功    True
#            失败    False
# 函数说明： 根据发送成员行号,委托日期,交易流水号查询汇兑业务登记簿及当前状态相关信息
################################################################################
def getTransTrcPK(SNDMBRCO,TRCDAT,TRCNO,trc_dict):
    AfaLoggerFunc.tradeInfo( ">>>开始查询汇兑业务登记簿[" + SNDMBRCO + "][" + TRCDAT + "][" + TRCNO + "]交易信息" )
    
    #===========组织查询条件====================================================
    trcbka_where_dict = {'SNDMBRCO':SNDMBRCO,'TRCDAT':TRCDAT,'TRCNO':TRCNO}

    #===========查询汇兑登记簿相关业务信息======================================
    trcbka_dict = rccpsDBTrcc_trcbka.selectu(trcbka_where_dict)
    
    if trcbka_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '获取汇兑业务详细信息异常' )
    
    if len(trcbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow( 'S999', '汇兑业务登记簿中无此汇兑业务详细信息' )
        
    AfaLoggerFunc.tradeInfo( ">>>结束查询汇兑业务登记簿[" + SNDMBRCO + "][" + TRCDAT + "][" + TRCNO + "]交易信息" )

    #==========将查询出的汇兑登记簿相关业务信息赋值到输出字典===================
    if not rccpsMap0000Dtrcbka2Dtrc_dict.map(trcbka_dict,trc_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的汇兑登记簿相关业务信息赋值到输出字典异常' )

    BJEDTE = trcbka_dict["BJEDTE"]
    BSPSQN = trcbka_dict["BSPSQN"]
    
    #==========查询当前业务状态=================================================
    AfaLoggerFunc.tradeInfo( ">>>开始查询交易[" + BJEDTE + "][" + BSPSQN + "]当前状态" )
    
    stat_dict = {}
    if not rccpsState.getTransStateCur(BJEDTE,BSPSQN,stat_dict):
        return False
    
    AfaLoggerFunc.tradeInfo( ">>>结束查询交易[" + BJEDTE + "][" + BSPSQN + "]当前状态" )

    #==========将查询出的业务状态详细信息赋值到输出字典=========================
    if not rccpsMap0000Dstat_dict2Dtrc_dict.map(stat_dict,trc_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的业务状态详细信息赋值到输出字典异常' )
    
    AfaLoggerFunc.tradeInfo( ">>>结束查询汇兑业务登记簿[" + BJEDTE + "][" + BSPSQN + "]交易信息" )
    return True
    
################################################################################
# 函数名:    GetTransBilPK
# 参数:      SNDMBRCO:发送成员行号,TRCDAT:委托日期,TRCNO:交易流水号,bil_dict(汇票业务交易详细信息,即bilbka表内容+sstlog表内容)
# 返回值：   成功    True
#            失败    False
# 函数说明： 根据发送成员行号,委托日期,交易流水号查询汇票业务登记簿及当前状态相关信息
################################################################################

def getTransBilPK(SNDMBRCO,TRCDAT,TRCNO,bil_dict):
    AfaLoggerFunc.tradeInfo( ">>>开始查询汇票业务登记簿[" + SNDMBRCO + "][" + TRCDAT + "][" + TRCNO + "]交易信息" )
    
    #==========组织查询条件=====================================================
    bilbka_where_dict = {'SNDMBRCO':SNDMBRCO,'TRCDAT':TRCDAT,'TRCNO':TRCNO}

    #==========查询汇票业务登记簿相关业务信息===================================
    bilbka_dict = rccpsDBTrcc_bilbka.selectu(bilbka_where_dict)
    
    if bilbka_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '获取汇票业务详细信息异常' )
        
    if len(bilbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow( 'S999', '汇票业务登记簿中无此汇票业务详细信息' )
        
    AfaLoggerFunc.tradeInfo( ">>>结束查询汇票业务登记簿[" + SNDMBRCO + "][" + TRCDAT + "][" + TRCNO + "]交易信息" )

    #==========将查询出的汇票业务登记簿相关业务信息赋值到输出字典===============
    if not rccpsMap0000Dbilbka2Dbil_dict.map(bilbka_dict,bil_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的汇票业务登记簿相关业务信息赋值到输出字典异常' )

    BJEDTE = bilbka_dict["BJEDTE"]
    BSPSQN = bilbka_dict["BSPSQN"]
    
    #==========查询当前业务状态=================================================
    AfaLoggerFunc.tradeInfo( ">>>开始查询交易[" + BJEDTE + "][" + BSPSQN + "]当前业务状态" )
    
    stat_dict = {}
    if not rccpsState.getTransStateCur(BJEDTE,BSPSQN,stat_dict):
        return False
    
    AfaLoggerFunc.tradeInfo( ">>>结束查询交易[" + BJEDTE + "][" + BSPSQN + "]当前业务状态" )

    #==========将查询出的业务状态详细信息赋值到输出字典=========================
    if not rccpsMap0000Dstat_dict2Dbil_dict.map(stat_dict,bil_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的业务状态详细信息赋值到输出字典异常' )
    
    AfaLoggerFunc.tradeInfo( ">>>结束查询汇票业务登记簿[" + BJEDTE + "][" + BSPSQN + "]交易信息" )
    return True

################################################################################
# 函数名:    getTransTrcAK
# 参数:      SNDBNKCO:发送行号,TRCDAT:委托日期,TRCNO:交易流水号,trc_dict(汇兑业务交易详细信息,即trcbka表内容+sstlog表内容)
# 返回值：   成功    True
#            失败    False
# 函数说明： 根据发送行号,委托日期,交易流水号查询汇兑业务登记簿及当前状态相关信息
################################################################################
def getTransTrcAK(SNDBNKCO,TRCDAT,TRCNO,trc_dict):
    AfaLoggerFunc.tradeInfo( ">>>开始查询汇兑业务登记簿[" + SNDBNKCO + "][" + TRCDAT + "][" + TRCNO + "]交易信息" )
    
    #===========组织查询条件====================================================
    trcbka_where_dict = {'SNDBNKCO':SNDBNKCO,'TRCDAT':TRCDAT,'TRCNO':TRCNO}

    #===========查询汇兑登记簿相关业务信息======================================
    trcbka_dict = rccpsDBTrcc_trcbka.selectu(trcbka_where_dict)
    
    if trcbka_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '获取汇兑业务详细信息异常' )
    
    if len(trcbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow( 'S999', '汇兑业务登记簿中无此汇兑业务详细信息' )
        
    AfaLoggerFunc.tradeInfo( ">>>结束查询汇兑业务登记簿[" + SNDBNKCO + "][" + TRCDAT + "][" + TRCNO + "]交易信息" )

    #==========将查询出的汇兑登记簿相关业务信息赋值到输出字典===================
    if not rccpsMap0000Dtrcbka2Dtrc_dict.map(trcbka_dict,trc_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的汇兑登记簿相关业务信息赋值到输出字典异常' )

    BJEDTE = trcbka_dict["BJEDTE"]
    BSPSQN = trcbka_dict["BSPSQN"]
    
    #==========查询当前业务状态=================================================
    AfaLoggerFunc.tradeInfo( ">>>开始查询交易[" + BJEDTE + "][" + BSPSQN + "]当前状态" )
    
    stat_dict = {}
    if not rccpsState.getTransStateCur(BJEDTE,BSPSQN,stat_dict):
        return False
    
    AfaLoggerFunc.tradeInfo( ">>>结束查询交易[" + BJEDTE + "][" + BSPSQN + "]当前状态" )

    #==========将查询出的业务状态详细信息赋值到输出字典=========================
    if not rccpsMap0000Dstat_dict2Dtrc_dict.map(stat_dict,trc_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的业务状态详细信息赋值到输出字典异常' )
    
    AfaLoggerFunc.tradeInfo( ">>>结束查询汇兑业务登记簿[" + BJEDTE + "][" + BSPSQN + "]交易信息" )
    return True
    
################################################################################
# 函数名:    getTransBilAK
# 参数:      SNDBNKCO:发送成员行号,TRCDAT:委托日期,TRCNO:交易流水号,bil_dict(汇票业务交易详细信息,即bilbka表内容+sstlog表内容)
# 返回值：   成功    True
#            失败    False
# 函数说明： 根据发送成员行号,委托日期,交易流水号查询汇票业务登记簿及当前状态相关信息
################################################################################

def getTransBilAK(SNDBNKCO,TRCDAT,TRCNO,bil_dict):
    AfaLoggerFunc.tradeInfo( ">>>开始查询汇票业务登记簿[" + SNDBNKCO + "][" + TRCDAT + "][" + TRCNO + "]交易信息" )
    
    #==========组织查询条件=====================================================
    bilbka_where_dict = {'SNDBNKCO':SNDBNKCO,'TRCDAT':TRCDAT,'TRCNO':TRCNO}

    #==========查询汇票业务登记簿相关业务信息===================================
    bilbka_dict = rccpsDBTrcc_bilbka.selectu(bilbka_where_dict)
    
    if bilbka_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '获取汇票业务详细信息异常' )
        
    if len(bilbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow( 'S999', '汇票业务登记簿中无此汇票业务详细信息' )
        
    AfaLoggerFunc.tradeInfo( ">>>结束查询汇票业务登记簿[" + SNDBNKCO + "][" + TRCDAT + "][" + TRCNO + "]交易信息" )

    #==========将查询出的汇票业务登记簿相关业务信息赋值到输出字典===============
    if not rccpsMap0000Dbilbka2Dbil_dict.map(bilbka_dict,bil_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的汇票业务登记簿相关业务信息赋值到输出字典异常' )

    BJEDTE = bilbka_dict["BJEDTE"]
    BSPSQN = bilbka_dict["BSPSQN"]
    
    #==========查询当前业务状态=================================================
    AfaLoggerFunc.tradeInfo( ">>>开始查询交易[" + BJEDTE + "][" + BSPSQN + "]当前业务状态" )
    
    stat_dict = {}
    if not rccpsState.getTransStateCur(BJEDTE,BSPSQN,stat_dict):
        return False
    
    AfaLoggerFunc.tradeInfo( ">>>结束查询交易[" + BJEDTE + "][" + BSPSQN + "]当前业务状态" )

    #==========将查询出的业务状态详细信息赋值到输出字典=========================
    if not rccpsMap0000Dstat_dict2Dbil_dict.map(stat_dict,bil_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的业务状态详细信息赋值到输出字典异常' )
    
    AfaLoggerFunc.tradeInfo( ">>>结束查询汇票业务登记簿[" + BJEDTE + "][" + BSPSQN + "]交易信息" )
    return True
    
###############################################################################
# 函数名:    getErrInfo
# 参数:      ERRKEY:错误代码
# 返回值:    成功:ERRSTR:错误信息
#            失败:False
# 函数说明:  根据错误代码查询对应的错误信息
###############################################################################

def getErrInfo(ERRKEY):
    AfaLoggerFunc.tradeInfo(">>>开始获取中心返回代码[" + ERRKEY + "]对应信息")
    
    errinf_where_dict = {}
    if ERRKEY[:2] != 'NN':
        errinf_where_dict['MBRTYP'] = '1'
        errinf_where_dict['ERRKEY'] = ERRKEY[:8]
    else:
        errinf_where_dict['MBRTYP'] = '2'
        errinf_where_dict['ERRKEY'] = ERRKEY[4:8]
    
    ERRSTR = ""
    
    errinf_dict = rccpsDBTrcc_errinf.selectu(errinf_where_dict)
    
    if errinf_dict == None:
        AfaLoggerFunc.tradeInfo("查询中心返回信息数据库异常")
        
    if len(errinf_dict) <= 0:
        ERRSTR = "未知错误"
        AfaLoggerFunc.tradeInfo("无此返回代码对应信息,返回中心返回信息[未知错误]")
    else:
        ERRSTR = errinf_dict['ERRSTR']
        AfaLoggerFunc.tradeInfo("找到此返回代码对应信息,返回中心返回信息[" + ERRSTR + "]")
    
    AfaLoggerFunc.tradeInfo(">>>结束获取中心返回代码[" + ERRKEY + "]对应信息")
    
    return ERRSTR
    
    
###############################################################################
# 函数名:    HostErr2RccErr
# 参数:      HostErr:主机错误代码
# 返回值:    RccErr: 中心错误代码
# 函数说明:  根据主机错误代码查询对应的中心错误代码
###############################################################################

def HostErr2RccErr(HostErr):
    AfaLoggerFunc.tradeInfo(">>>开始获取主机错误码[" + HostErr + "]对应的中心返回码")
    
    errinf_where_dict = {}
    errinf_where_dict['NOTE3'] = "%" + HostErr + "%"
    
    errinf_dict = rccpsDBTrcc_errinf.selectu(errinf_where_dict)
    
    RccErr = ""
    
    if errinf_dict == None:
        RccErr = "NN1IA999"
        AfaLoggerFunc.tradeInfo("查询中心返回信息数据库异常")
        
    if len(errinf_dict) <= 0:
        RccErr = "NN1IA999"
        AfaLoggerFunc.tradeInfo("无此主机错误码对应信息,返回中心错误码[NN1IA999]")
    else:
        RccErr = "NN1I" + errinf_dict['ERRKEY']
        AfaLoggerFunc.tradeInfo("找到此主机错误码对应信息,返回中心错误码[" + RccErr + "]")
    
    AfaLoggerFunc.tradeInfo(">>>结束获取主机错误码[" + HostErr + "]对应的中心返回码")
    
    return RccErr

################################################################################
# 函数名:    getTransWtr                                             
# 参数:      BJEDTE:交易日期(必输),BSPSQN:报单序号(必输)             
# 返回值：   成功    wtr_dict(通存通兑业务交易详细信息,即wtrbka表内容+sstlog表内容)
#            失败    False                                           
# 函数说明： 查询通存通兑业务登记簿及当前状态相关信息                    
################################################################################
                                                                     
def getTransWtr(BJEDTE,BSPSQN,wtr_dict):
    AfaLoggerFunc.tradeDebug( ">>>开始查询通存通兑业务登记簿[" + BJEDTE + "][" + BSPSQN + "]交易信息" )
                                                                     
    #==========组织查询条件=====================================================
    wtrbka_where_dict = {'BJEDTE':BJEDTE,'BSPSQN':BSPSQN}            
                                                                     
    #==========查询汇兑登记簿相关业务信息=======================================
    wtrbka_dict = rccpsDBTrcc_wtrbka.selectu(wtrbka_where_dict)  
    
    if wtrbka_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '查询通存通兑业务登记簿交易信息异常' )
        
    if len(wtrbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow( 'S999', '通存通兑业务登记簿中无此交易信息' )
    
    #==========将查询出的通存通兑登记簿相关业务信息赋值到输出字典==============
    if not rccpsMap0000Dwtrbka2Dwtr_dict.map(wtrbka_dict,wtr_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的通存通兑登记簿相关业务信息赋值到输出字典异常' )
        
    #==========查询当前业务状态================================================
    AfaLoggerFunc.tradeDebug( ">>>开始查询交易[" + BJEDTE + "][" + BSPSQN + "]当前状态" )
    
    stat_dict = {}
    
    if not rccpsState.getTransStateCur(BJEDTE,BSPSQN,stat_dict):
        return False
        
    AfaLoggerFunc.tradeDebug( ">>>结束查询交易[" + BJEDTE + "][" + BSPSQN + "]当前状态" )

    #==========将查询出的业务状态详细信息赋值到输出字典========================
    if not rccpsMap0000Dstat_dict2Dwtr_dict.map(stat_dict,wtr_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的业务状态详细信息赋值到输出字典异常' )
    
    AfaLoggerFunc.tradeDebug( ">>>结束查询通存通兑业务登记簿[" + BJEDTE + "][" + BSPSQN + "]交易信息" )
    return True

###############################################################################
# 函数名:    insTransWtr
# 参数:      trc_dict(通存通兑业务交易详细信息)
# 返回值：   成功    True
#            失败    False
# 函数说明： 登记通存通兑业务登记簿及状态相关信息
###############################################################################
def insTransWtr(wtr_dict):
    
    AfaLoggerFunc.tradeInfo( ">>>开始登记通存通兑业务登记簿[" + wtr_dict["BJEDTE"] + "][" + wtr_dict["BSPSQN"] + "]交易信息及相关状态" )
    
    if not wtr_dict.has_key("BJEDTE"):
        return AfaFlowControl.ExitThisFlow( 'S999',"登记通存通兑业务登记簿,BJEDTE不能为空")
        
    if not wtr_dict.has_key("BSPSQN"):
        return AfaFlowControl.ExitThisFlow( 'S999',"登记通存通兑业务登记簿,BSPSQN不能为空")
        
    
    #==========将输入字典赋值到通存通兑业务登记簿字典==========================
    wtrbka_dict = {}
    
    if not rccpsMap0000Dwtr_dict2Dwtrbka.map(wtr_dict,wtrbka_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '将输入字典赋值到通存通兑业务登记簿字典异常' )
        
    #==========登记信息到汇兑登记簿============================================
    AfaLoggerFunc.tradeInfo(wtrbka_dict)
    ret = rccpsDBTrcc_wtrbka.insert(wtrbka_dict)
    
    if ret <= 0:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '登记通存通兑业务详细信息到通存通兑业务登记簿异常' )
        
    AfaLoggerFunc.tradeInfo("插入成功")
    #==========登记初始状态====================================================
    if not rccpsState.newTransState(wtr_dict["BJEDTE"],wtr_dict["BSPSQN"],PL_BCSTAT_INIT,PL_BDWFLG_SUCC):
        return False
    
    AfaLoggerFunc.tradeInfo( ">>>结束登记通存通兑业务登记簿[" + wtr_dict["BJEDTE"] + "][" + wtr_dict["BSPSQN"] + "]交易信息及相关状态" )
    return True
    
################################################################################
# 函数名:    getTransWtrPK
# 参数:      SNDMBRCO:发送成员行号,TRCDAT:委托日期,TRCNO:交易流水号,wtr_dict(汇兑业务交易详细信息,即wtrbka表内容+sstlog表内容)
# 返回值：   成功    True
#            失败    False
# 函数说明： 根据发送成员行号,委托日期,交易流水号查询通存通兑业务登记簿及当前状态相关信息
################################################################################
def getTranswtrPK(SNDMBRCO,TRCDAT,TRCNO,wtr_dict):
    AfaLoggerFunc.tradeInfo( ">>>开始查询通存通兑业务登记簿[" + SNDMBRCO + "][" + TRCDAT + "][" + TRCNO + "]交易信息" )
    
    #===========组织查询条件====================================================
    wtrbka_where_dict = {'SNDMBRCO':SNDMBRCO,'TRCDAT':TRCDAT,'TRCNO':TRCNO}

    #===========查询汇兑登记簿相关业务信息======================================
    wtrbka_dict = rccpsDBTrcc_wtrbka.selectu(wtrbka_where_dict)
    
    if wtrbka_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '获取通存通兑业务详细信息异常' )
    
    if len(wtrbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow( 'S999', '通存通兑业务登记簿中无此通存通兑业务详细信息' )
        
    AfaLoggerFunc.tradeInfo( ">>>结束查询通存通兑业务登记簿[" + SNDMBRCO + "][" + TRCDAT + "][" + TRCNO + "]交易信息" )

    #==========将查询出的通存通兑登记簿相关业务信息赋值到输出字典===================
    if not rccpsMap0000Dwtrbka2Dwtr_dict.map(wtrbka_dict,wtr_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的通存通兑登记簿相关业务信息赋值到输出字典异常' )

    BJEDTE = wtrbka_dict["BJEDTE"]
    BSPSQN = wtrbka_dict["BSPSQN"]
    
    #==========查询当前业务状态=================================================
    AfaLoggerFunc.tradeInfo( ">>>开始查询交易[" + BJEDTE + "][" + BSPSQN + "]当前状态" )
    
    stat_dict = {}
    if not rccpsState.getTransStateCur(BJEDTE,BSPSQN,stat_dict):
        return False
    
    AfaLoggerFunc.tradeInfo( ">>>结束查询交易[" + BJEDTE + "][" + BSPSQN + "]当前状态" )

    #==========将查询出的业务状态详细信息赋值到输出字典=========================
    if not rccpsMap0000Dstat_dict2Dwtr_dict.map(stat_dict,wtr_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的业务状态详细信息赋值到输出字典异常' )
    
    AfaLoggerFunc.tradeInfo( ">>>结束查询汇兑业务登记簿[" + BJEDTE + "][" + BSPSQN + "]交易信息" )
    return True
    
###############################################################################
# 函数名:    getTransWtrAK
# 参数:      SNDBNKCO:发送行号,TRCDAT:委托日期,TRCNO:交易流水号,wtr_dict(通存通兑业务交易详细信息,即wtrbka表内容+sstlog表内容)
# 返回值：   成功    True
#            失败    False
# 函数说明： 根据发送行号,委托日期,交易流水号查询通存通兑业务登记簿及当前状态相关信息
###############################################################################
def getTransWtrAK(SNDBNKCO,TRCDAT,TRCNO,wtr_dict):
    AfaLoggerFunc.tradeInfo( ">>>开始查询通存通兑业务登记簿[" + SNDBNKCO + "][" + TRCDAT + "][" + TRCNO + "]交易信息" )
    
    #===========组织查询条件===================================================
    wtrbka_where_dict = {'SNDBNKCO':SNDBNKCO,'TRCDAT':TRCDAT,'TRCNO':TRCNO}

    #===========查询通存通兑登记簿相关业务信息=================================
    wtrbka_dict = rccpsDBTrcc_wtrbka.selectu(wtrbka_where_dict)
    
    if wtrbka_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '获取通存通兑业务详细信息异常' )
    
    if len(wtrbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow( 'S999', '通存通兑业务登记簿中无此通存通兑业务详细信息' )
        
    AfaLoggerFunc.tradeInfo( ">>>结束查询通存通兑业务登记簿[" + SNDBNKCO + "][" + TRCDAT + "][" + TRCNO + "]交易信息" )

    #==========将查询出的通存通兑登记簿相关业务信息赋值到输出字典==============
    if not rccpsMap0000Dwtrbka2Dwtr_dict.map(wtrbka_dict,wtr_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的通存通兑登记簿相关业务信息赋值到输出字典异常' )

    BJEDTE = wtrbka_dict["BJEDTE"]
    BSPSQN = wtrbka_dict["BSPSQN"]
    
    #==========查询当前业务状态=================================================
    AfaLoggerFunc.tradeInfo( ">>>开始查询交易[" + BJEDTE + "][" + BSPSQN + "]当前状态" )
    
    stat_dict = {}
    if not rccpsState.getTransStateCur(BJEDTE,BSPSQN,stat_dict):
        return False
    
    AfaLoggerFunc.tradeInfo( ">>>结束查询交易[" + BJEDTE + "][" + BSPSQN + "]当前状态" )

    #==========将查询出的业务状态详细信息赋值到输出字典=========================
    if not rccpsMap0000Dstat_dict2Dwtr_dict.map(stat_dict,wtr_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的业务状态详细信息赋值到输出字典异常' )
    
    AfaLoggerFunc.tradeInfo( ">>>结束查询通存通兑业务登记簿[" + BJEDTE + "][" + BSPSQN + "]交易信息" )
    return True
    
###############################################################################
# 函数名:    getTransWtrCK
# 参数:      SNDBNKCO:发送行号,COTRCDAT:存款确认委托日期,COTRCNO:存款确认交易流水号,wtr_dict(通存通兑业务交易详细信息,即wtrbka表内容+sstlog表内容)
# 返回值：   成功    True
#            失败    False
# 函数说明： 根据发送行号,存款确认委托日期,存款确认交易流水号查询通存通兑业务登记簿及当前状态相关信息
###############################################################################
def getTransWtrCK(SNDBNKCO,COTRCDAT,COTRCNO,wtr_dict):
    AfaLoggerFunc.tradeInfo( ">>>开始查询通存通兑业务登记簿[" + SNDBNKCO + "][" + COTRCDAT + "][" + COTRCNO + "]交易信息" )
    
    #===========组织查询条件===================================================
    wtrbka_where_dict = {'SNDBNKCO':SNDBNKCO,'COTRCDAT':COTRCDAT,'COTRCNO':COTRCNO}

    #===========查询通存通兑登记簿相关业务信息=================================
    wtrbka_dict = rccpsDBTrcc_wtrbka.selectu(wtrbka_where_dict)
    
    if wtrbka_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '获取通存通兑业务详细信息异常' )
    
    if len(wtrbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow( 'S999', '通存通兑业务登记簿中无此通存通兑业务详细信息' )
        
    AfaLoggerFunc.tradeInfo( ">>>结束查询通存通兑业务登记簿[" + SNDBNKCO + "][" + COTRCDAT + "][" + COTRCNO + "]交易信息" )

    #==========将查询出的通存通兑登记簿相关业务信息赋值到输出字典==============
    if not rccpsMap0000Dwtrbka2Dwtr_dict.map(wtrbka_dict,wtr_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的通存通兑登记簿相关业务信息赋值到输出字典异常' )

    BJEDTE = wtrbka_dict["BJEDTE"]
    BSPSQN = wtrbka_dict["BSPSQN"]
    
    #==========查询当前业务状态=================================================
    AfaLoggerFunc.tradeInfo( ">>>开始查询交易[" + BJEDTE + "][" + BSPSQN + "]当前状态" )
    
    stat_dict = {}
    if not rccpsState.getTransStateCur(BJEDTE,BSPSQN,stat_dict):
        return False
    
    AfaLoggerFunc.tradeInfo( ">>>结束查询交易[" + BJEDTE + "][" + BSPSQN + "]当前状态" )

    #==========将查询出的业务状态详细信息赋值到输出字典=========================
    if not rccpsMap0000Dstat_dict2Dwtr_dict.map(stat_dict,wtr_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的业务状态详细信息赋值到输出字典异常' )
    
    AfaLoggerFunc.tradeInfo( ">>>结束查询通存通兑业务登记簿[" + BJEDTE + "][" + BSPSQN + "]交易信息" )
    return True

################################################################################
# 函数名:    getTransMpc                                             
# 参数:      BJEDTE:交易日期(必输),BSPSQN:报单序号(必输)             
# 返回值：   成功    mpc_dict(通存通兑冲销交易详细信息,即mpcbka表内容)
#            失败    False                                           
# 函数说明： 查询通存通兑冲销登记簿
################################################################################
                                                                     
def getTransMpc(BJEDTE,BSPSQN,mpc_dict):
    AfaLoggerFunc.tradeInfo( ">>>开始查询通存通兑冲销登记簿[" + BJEDTE + "][" + BSPSQN + "]交易信息" )
                                                                     
    #==========组织查询条件=====================================================
    mpcbka_where_dict = {'BJEDTE':BJEDTE,'BSPSQN':BSPSQN}            
                                                                     
    #==========查询冲销登记簿相关业务信息=======================================
    mpcbka_dict = rccpsDBTrcc_mpcbka.selectu(mpcbka_where_dict)  
    
    if mpcbka_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '查询通存通兑冲销登记簿交易信息异常' )
        
    if len(mpcbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow( 'S999', '通存通兑冲销登记簿中无此交易信息' )
    
    #==========将查询出的通存通兑冲销登记簿相关信息赋值到输出字典==============
    if not rccpsMap0000Dmpcbka2Dmpc_dict.map(mpcbka_dict,mpc_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的通存通兑冲销登记簿相关信息赋值到输出字典异常' )
    
    AfaLoggerFunc.tradeInfo( ">>>结束查询通存通兑冲销登记簿[" + BJEDTE + "][" + BSPSQN + "]交易信息" )
    return True

################################################################################
# 函数名:    chkTDBESAuth                                             
# 参数:      BESBNO 机构号
# 返回值：   成功    True
#            失败    False                                           
# 函数说明： 检查机构是否有通存通兑权限
################################################################################
def chkTDBESAuth(BESBNO):
    AfaLoggerFunc.tradeInfo(">>>开始检查机构[" + BESBNO + "]是否有通存通兑业务权限")
    
    where_sql = "BPATPE = '3' and BPARAD = '" + BESBNO + "'"
    
    ret = rccpsDBTrcc_pamtbl.count(where_sql)
    
    if ret < 0:
        return AfaFlowControl.ExitThisFlow("S999","查询机构[" + BESBNO + "]通存通兑业务权限异常")
        
    if ret > 0:
        return AfaFlowControl.ExitThisFlow("S999","机构[" + BESBNO + "]无通存通兑业务权限")
    
    AfaLoggerFunc.tradeInfo(">>>结束检查机构[" + BESBNO + "]是否有通存通兑业务权限")
    
    return True
    
################################################################################
# 函数名:    chkLimited
# 参数:      BJEDTE 交易日期,PYRACC 付款人账号,OCCAMT 当前交易金额
# 返回值：   成功    True
#            失败    False                                           
# 函数说明： 检查当前交易金额是否超限额
################################################################################
def chkLimited(BJEDTE,PYRACC,OCCAMT):
    AfaLoggerFunc.tradeInfo(">>>开始检查当前交易金额是否超限额")
    
    pamtbl_where_dict = {'BPATPE':'4','BPARAD':'TDLZXE'}
    
    pamtbl_dict = {}
    pamtbl_dict = rccpsDBTrcc_pamtbl.selectu(pamtbl_where_dict)
    
    if pamtbl_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","查询通兑来账交易限额异常")
        
    if len(pamtbl_dict) <= 0:
        return AfaFlowControl.ExitThisFlow("S999","参数表中无通兑来账参数")
    else:
        AfaLoggerFunc.tradeInfo("交易金额限额为[" + str(pamtbl_dict['BPADAT'])+ "]")
    
    where_sql = "select count(*),sum(a.occamt) from rcc_wtrbka as a,rcc_spbsta as b where a.bjedte = b.bjedte and a.bspsqn = b.bspsqn and a.PYRACC = '" + PYRACC + "' and a.BJEDTE = '" + BJEDTE + "' and b.bcstat in ('70','72') and b.bdwflg = '1'"
    
    records = AfaDBFunc.SelectSql(where_sql)
    
    if records == None:
        return AfaFlowControl.ExitThisFlow('S999','统计账户今日交易总金额异常')
    
    else:
        rec_count = records[0][0]
        rec_sum   = records[0][1] 
        
    if records[0][0] <= 0:
        rec_count = 0
        rec_sum   = 0.00
    
    AfaLoggerFunc.tradeInfo("今日历史交易金额总和为[" + str(rec_sum) + "],本次交易金额为[" + str(OCCAMT) + "]")
    
    if float(rec_sum) + float(OCCAMT) > float(pamtbl_dict['BPADAT']):
        return AfaFlowControl.ExitThisFlow("S999","本账户交易金额超限")
    
    AfaLoggerFunc.tradeInfo(">>>结束检查当前交易金额是否超限额")
    
    return True
