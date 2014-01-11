# -*- coding: gbk -*-
###############################################################################
#   农信银系统 状态相关函数
#==============================================================================
#   作    者：  关彬捷
#   程序文件:   rccpsStat.py
#   修改时间:   2008-06-05
###############################################################################

import AfaLoggerFunc,AfaDBFunc,AfaUtilTools,TradeContext,AfaFlowControl
from types import *
import rccpsDBTrcc_spbsta,rccpsDBTrcc_sstlog
import rccpsMap0000Dstat_dict2Dsstlog,rccpsMap0000Dstat_dict2Dspbsta
import rccpsDBTrcc_bilbka,rccpsDBTrcc_bilinf
import rccpsMap0000Dsstlog2Dstat_dict

################################################################################
# 函数名:    setTransState
# 参数:      stat_dict:状态字典
#            {BJEDTE:交易日期(必输),BSPSQN:报单序号(必输),BCSTAT:业务状态(必输),BDWFLG:流转处理标识(必输),
#             BESBNO:机构号,BEACSB:账务机构,BETELR:柜员号,BEAUUS:授权柜员,EFDT:前置日期,RBSQ:前置流水号,TRDT:主机日期,TLSQ:主机流水号,
#             SBAC:借方账号,ACNM:借方户名,RBAC:贷方账号,OTNM:贷方户名,DASQ:销账序号,MGID:主机返回码,PRCCO:中心返回码,}
# 返回值：   True  成功    False  失败
# 函数说明： 设置单笔交易当前业务状态及相关信息
################################################################################
def setTransState(stat_dict):
    AfaLoggerFunc.tradeInfo(">>>进入setTransState")
    
    AfaLoggerFunc.tradeDebug("stat_dict = " + str(stat_dict))
    #==========检查表spbsta中是否存在此业务状态=================================
    spbsta_where_dict = {}
    if stat_dict.has_key("BJEDTE"):
        spbsta_where_dict["BJEDTE"] = stat_dict["BJEDTE"]
        
    if stat_dict.has_key("BSPSQN"):
        spbsta_where_dict["BSPSQN"] = stat_dict["BSPSQN"]
        
    spbsta_dict = rccpsDBTrcc_spbsta.selectu(spbsta_where_dict)
    if spbsta_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("获取交易[" + stat_dict['BJEDTE'] + "][" + stat_dict['BSPSQN'] + "]当前状态异常")
        return AfaFlowControl.ExitThisFlow( 'S999', '获取交易当前状态异常' )
        
    elif len(spbsta_dict) <= 0:
        AfaLoggerFunc.tradeFatal("当前状态登记簿中无交易[" + stat_dict['BJEDTE'] + "][" + stat_dict['BSPSQN'] + "]状态信息")
        return AfaFlowControl.ExitThisFlow( 'S999', '当前状态登记簿中无此交易状态' )
    
    #===========检查表sstlog中是否存在此业务状态================================
    sstlog_where_dict = {}
    if spbsta_dict.has_key("BJEDTE"):
        sstlog_where_dict["BJEDTE"] = spbsta_dict["BJEDTE"]
        
    if spbsta_dict.has_key("BSPSQN"):
        sstlog_where_dict["BSPSQN"] = spbsta_dict["BSPSQN"]
        
    if spbsta_dict.has_key("BCURSQ"):
        sstlog_where_dict["BCURSQ"] = str(spbsta_dict["BCURSQ"])
    
    sstlog_dict = rccpsDBTrcc_sstlog.selectu(sstlog_where_dict)
    
    if sstlog_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("获取交易[" + stat_dict['BJEDTE'] + "][" + stat_dict['BSPSQN'] + "]当前状态详细信息异常")
        return AfaFlowControl.ExitThisFlow( 'S999', '获取交易当前状态详细信息异常' )
        
    elif len(sstlog_dict) == 0:
        AfaLoggerFunc.tradeFatal("流水状态登记簿中无交易[" + stat_dict['BJEDTE'] + "][" + stat_dict['BSPSQN'] + "]当前状态详细信息")
        return AfaFlowControl.ExitThisFlow( 'S999', '流水状态登记簿中无此交易当前状态详细信息' )
    
    #============设置默认值=====================================================
    stat_dict["PRTCNT"] = 0
    stat_dict["NOTE2"] = AfaUtilTools.GetSysDate() + AfaUtilTools.GetSysTime()
    #AfaLoggerFunc.tradeInfo(stat_dict["NOTE2"])
    #============更新表sstlog===================================================
    sstlog_update_dict = {}
    
    if not rccpsMap0000Dstat_dict2Dsstlog.map(stat_dict,sstlog_update_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '为交易当前状态详细信息赋值异常' )
        
    sstlog_where_dict = {}
    if spbsta_dict.has_key("BJEDTE"):
        sstlog_where_dict["BJEDTE"] = spbsta_dict["BJEDTE"]
        
    if spbsta_dict.has_key("BSPSQN"):
        sstlog_where_dict["BSPSQN"] = spbsta_dict["BSPSQN"]
        
    if spbsta_dict.has_key("BCURSQ"):
        sstlog_where_dict["BCURSQ"] = str(spbsta_dict["BCURSQ"])
        
    #AfaLoggerFunc.tradeInfo("update_dict = " + str(sstlog_update_dict))
    #AfaLoggerFunc.tradeInfo("where_dict = " + str(sstlog_where_dict))
    
    ret = rccpsDBTrcc_sstlog.update(sstlog_update_dict,sstlog_where_dict)
    
    if ret <= 0:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("登记交易[" + stat_dict['BJEDTE'] + "][" + stat_dict['BSPSQN'] + "]")
        return AfaFlowControl.ExitThisFlow( 'S999', '登记交易当前状态详细信息异常' )
    
    #============更新表spbsta===================================================
    spbsta_update_dict = {}
    
    if not rccpsMap0000Dstat_dict2Dspbsta.map(stat_dict,spbsta_update_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '为交易当前状态赋值异常' )
    
    spbsta_where_dict = {}
    if stat_dict.has_key("BJEDTE"):
        spbsta_where_dict["BJEDTE"] = stat_dict["BJEDTE"]
    if stat_dict.has_key("BSPSQN"):
        spbsta_where_dict["BSPSQN"] = stat_dict["BSPSQN"]
    
    ret = rccpsDBTrcc_spbsta.update(spbsta_update_dict,spbsta_where_dict)
    if (ret <= 0):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("登记交易[" + stat_dict['BJEDTE'] + "][" + stat_dict['BSPSQN'] + "]当前状态异常")
        return AfaFlowControl.ExitThisFlow( 'S999', '登记交易当前状态异常' )
        
    AfaLoggerFunc.tradeInfo(">>>结束setTransState")
    
    return True

################################################################################
# 函数名:    newTransState
# 参数:      BJEDTE:交易日期(必输),BSPSQN:报单序号(必输),BCSTAT:业务状态(必输),BDWFLG:流转处理标识(必输)
# 返回值：   True  成功    False  失败
# 函数说明： 新建单笔交易业务状态及相关信息
################################################################################
def newTransState(BJEDTE,BSPSQN,BCSTAT,BDWFLG):
    AfaLoggerFunc.tradeInfo(">>>进入newTransState")
    
    stat_dict = {}
    stat_dict["BJEDTE"] = BJEDTE;
    stat_dict["BSPSQN"] = BSPSQN;
    stat_dict["BCSTAT"] = BCSTAT;
    stat_dict["BDWFLG"] = BDWFLG;
    
    #==========检查表spbsta中是否存在此业务状态=================================
    spbsta_where_dict = {}
    if stat_dict.has_key("BJEDTE"):
        spbsta_where_dict["BJEDTE"] = stat_dict["BJEDTE"]
    if stat_dict.has_key("BSPSQN"):
        spbsta_where_dict["BSPSQN"] = stat_dict["BSPSQN"]
        
    spbsta_dict = rccpsDBTrcc_spbsta.selectu(spbsta_where_dict)
    
    if spbsta_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("查询交易[" + BJEDTE + "][" + BSPSQN + "]当前状态异常")
        return AfaFlowControl.ExitThisFlow( 'S999', '查询交易当前状态异常' )
        
    elif len(spbsta_dict) <= 0:
        AfaLoggerFunc.tradeInfo("当前状态登记簿中无此业务状态,需新增一条业务状态")
        MaxBCURSQ = 1
        
    else:
        MaxBCURSQ = int(spbsta_dict["BCURSQ"]) + 1
            
    #===========设置默认值======================================================
    if TradeContext.existVariable('BESBNO'):            #机构号
        stat_dict["BESBNO"] = TradeContext.BESBNO
        
    if TradeContext.existVariable('BEACSB'):            #账务机构号
        stat_dict["BEACSB"] = TradeContext.BEACSB
        
    if TradeContext.existVariable('BETELR'):            #柜员号
        stat_dict["BETELR"] = TradeContext.BETELR
        
    if TradeContext.existVariable('BEAUUS'):            #授权柜员号
        stat_dict["BEAUUS"] = TradeContext.BEAUUS
        
    if TradeContext.existVariable('TERMID'):            #终端号
        stat_dict['TERMID'] = TradeContext.TERMID
        
    if TradeContext.existVariable('NOTE3'):             #挂账原因
        stat_dict['NOTE3']  = TradeContext.NOTE3
        
    if TradeContext.existVariable('FEDT') and TradeContext.FEDT != '' and TradeContext.existVariable('HostCode') and TradeContext.HostCode != '8820':              #前置日期
        stat_dict['FEDT'] = TradeContext.FEDT
    else:
        stat_dict['FEDT'] = BJEDTE

    if TradeContext.existVariable('RBSQ') and TradeContext.RBSQ != '' and TradeContext.existVariable('HostCode') and TradeContext.HostCode != '8820':              #前置流水号
        stat_dict['RBSQ']  = TradeContext.RBSQ
    else:
        stat_dict['RBSQ'] = BSPSQN
    
    stat_dict["PRTCNT"] = 0
    stat_dict["BJETIM"] = AfaUtilTools.GetSysDate() + AfaUtilTools.GetSysTime()
    #AfaLoggerFunc.tradeInfo(">>>>time:" + stat_dict["BJETIM"])
    
    #===========在表sstlog中新增一条业务状态====================================
    sstlog_insert_dict = {}
    stat_dict["BCURSQ"] = MaxBCURSQ
    
    if not rccpsMap0000Dstat_dict2Dsstlog.map(stat_dict,sstlog_insert_dict):
        AfaLoggerFunc.tradeFatal("为交易[" + BJEDTE + "][" + BSPSQN + "]当前状态详细信息赋值异常")
        return AfaFlowControl.ExitThisFlow( 'S999', '为交易当前状态详细信息赋值异常' )
    
    ret = rccpsDBTrcc_sstlog.insert(sstlog_insert_dict)
    
    if ret <= 0:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("登记交易[" + BJEDTE + "][" + BSPSQN + "]当前状态详细信息异常")
        return AfaFlowControl.ExitThisFlow( 'S999', '登记交易当前状态详细信息异常' )
        
    if MaxBCURSQ == 1:    
        #========表spbsta中新增一条业务状态=====================================
        spbsta_insert_dict = {}
        stat_dict["BCURSQ"] = MaxBCURSQ
        
        if not rccpsMap0000Dstat_dict2Dspbsta.map(stat_dict,spbsta_insert_dict):
            AfaLoggerFunc.tradeFatal("为交易[" + BJEDTE + "][" + BSPSQN + "]当前状态赋值异常")
            return AfaFlowControl.ExitThisFlow( 'S999', '为交易当前状态赋值异常' )
            
        ret = rccpsDBTrcc_spbsta.insert(spbsta_insert_dict)
        if ret <= 0:
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeFatal("登记交易[" + BJEDTE + "][" + BSPSQN + "]当前状态异常")
            return AfaFlowControl.ExitThisFlow( 'S999', '登记交易当前状态异常' )
    else:
        #========修改spbsta中对应业务状态=======================================
        spbsta_update_dict = {}
        stat_dict["BCURSQ"] = MaxBCURSQ
        
        if not rccpsMap0000Dstat_dict2Dspbsta.map(stat_dict,spbsta_update_dict):
            AfaLoggerFunc.tradeFatal("为交易[" + BJEDTE + "][" + BSPSQN + "]当前状态赋值异常")
            return AfaFlowControl.ExitThisFlow( 'S999', '为交易当前状态赋值异常' )
        
        spbsta_where_dict = {}
        spbsta_where_dict["BJEDTE"] = stat_dict["BJEDTE"]
        spbsta_where_dict["BSPSQN"] = stat_dict["BSPSQN"]
        
        ret = rccpsDBTrcc_spbsta.update(spbsta_update_dict,spbsta_where_dict)
        if (ret <= 0):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeFatal("登记交易[" + BJEDTE + "][" + BSPSQN + "]当前状态异常")
            return AfaFlowControl.ExitThisFlow( 'S999', '登记交易当前状态异常' )
    AfaLoggerFunc.tradeInfo(">>>结束newTransState")
    return True
    
################################################################################
# 函数名:    getTransStateCur
# 参数:      BJEDTE:交易日期(必输),BSPSQN:报单序号(必输),stat_dict(业务状态详细信息)
# 返回值：   成功    True
#            失败    False
# 函数说明： 查询交易当前业务状态及相关信息
################################################################################
def getTransStateCur(BJEDTE,BSPSQN,stat_dict):
    AfaLoggerFunc.tradeDebug(">>>进入getTransStateCur")
    
    #==========获取spbsta当前状态信息及编号=====================================
    spbsta_where_dict = {}
    spbsta_where_dict["BJEDTE"] = BJEDTE
    spbsta_where_dict["BSPSQN"] = BSPSQN
    
    spbsta_dict = rccpsDBTrcc_spbsta.selectu(spbsta_where_dict)
    
    if spbsta_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("获取交易[" + BJEDTE + "][" + BSPSQN + "]当前状态异常")
        return AfaFlowControl.ExitThisFlow( 'S999', '获取交易当前状态异常' )
        
    elif len(spbsta_dict) <= 0:
        AfaLoggerFunc.tradeFatal("当前状态登记簿中无此交易[" + BJEDTE + "][" + BSPSQN + "]状态")
        return AfaFlowControl.ExitThisFlow( 'S999', '当前状态登记簿中无此交易状态' )
        return False
        
    #===========获取sstlog对应状态及信息========================================
    sstlog_where_dict = {}
    sstlog_where_dict["BJEDTE"] = spbsta_dict["BJEDTE"]
    sstlog_where_dict["BSPSQN"] = spbsta_dict["BSPSQN"]
    sstlog_where_dict["BCURSQ"] = str(spbsta_dict["BCURSQ"])
    
    sstlog_dict = rccpsDBTrcc_sstlog.selectu(sstlog_where_dict)
    
    if sstlog_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("获取交易[" + BJEDTE + "][" + BSPSQN + "]当前状态详细信息异常")
        return AfaFlowControl.ExitThisFlow( 'S999', '获取交易当前状态详细信息异常' )
        
    if len(sstlog_dict) <= 0:
        AfaLoggerFunc.tradeFatal("流水状态登记簿中无此交易[" + BJEDTE + "][" + BSPSQN + "]当前状态详细信息")
        return AfaFlowControl.ExitThisFlow( 'S999', '流水状态登记簿中无此交易当前状态详细信息' )
        
    if not rccpsMap0000Dsstlog2Dstat_dict.map(sstlog_dict,stat_dict):
        AfaLoggerFunc.tradeFatal("将查询出的交易[" + BJEDTE + "][" + BSPSQN + "]业务状态详细信息赋值到输出字典异常")
        return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的业务状态详细信息赋值到输出字典异常' )
        
    AfaLoggerFunc.tradeDebug(">>>结束getTransStateCur")
    return True

################################################################################
# 函数名:    getTransStateSet
# 参数:      BJEDTE:交易日期,BSPSQN:报单序号,BCSTAT:当前业务状态,BDWFLG:当前流转处理标识,sstlog_dict(业务状态详细信息)
# 返回值：   成功    True
#            失败    False
# 函数说明： 查询交易指定业务状态及相关信息
################################################################################
def getTransStateSet(BJEDTE,BSPSQN,BCSTAT,BDWFLG,stat_dict):
    AfaLoggerFunc.tradeInfo(">>>进入getTransStateSet")
    
    #==========获取sstlog对应状态及信息=========================================
    sstlog_where_dict = {}
    sstlog_where_dict["BJEDTE"] = BJEDTE
    sstlog_where_dict["BSPSQN"] = BSPSQN
    sstlog_where_dict["BCSTAT"] = BCSTAT
    sstlog_where_dict["BDWFLG"] = BDWFLG
    
    sstlog_dict = rccpsDBTrcc_sstlog.selectu(sstlog_where_dict)
    
    if sstlog_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("获取交易[" + BJEDTE + "][" + BSPSQN + "]指定状态详细信息异常")
        return AfaFlowControl.ExitThisFlow( 'S999', '获取交易指定状态详细信息异常' )
        
    if len(sstlog_dict) <= 0:
        AfaLoggerFunc.tradeFatal("流水状态登记簿中无此交易" + BJEDTE + "][" + BSPSQN + "]指定状态[" + BCSTAT + "][" + BDWFLG + "]详细信息")
        return AfaFlowControl.ExitThisFlow( 'S999', '流水状态登记簿中无此交易指定状态详细信息' )
        
    if not rccpsMap0000Dsstlog2Dstat_dict.map(sstlog_dict,stat_dict):
        AfaLoggerFunc.tradeFatal("将查询出的业务状态详细信息赋值到输出字典异常")
        return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的业务状态详细信息赋值到输出字典异常' )
    
    AfaLoggerFunc.tradeInfo(">>>结束getTransStateSet")
    return True
    
################################################################################
# 函数名:    getTransStateAll
# 参数:      BJEDTE:交易日期(必输),BSPSQN:报单序号(必输),sstlog_list(业务状态详细信息)
# 返回值：   成功    True
#            失败    False
# 函数说明： 查询交易所有业务状态及相关信息
################################################################################
def getTransStateAll(BJEDTE,BSPSQN,stat_list):
    AfaLoggerFunc.tradeInfo(">>>进入getTransStateAll")
    #===========获取sstlog所有状态及相关信息====================================
    sstlog_where_sql = "BJEDTE = '" + BJEDTE + "' and BSPSQN = '" + BSPSQN + "'"
    sstlog_order_sql = " order by BCURSQ desc "
    
    sstlog_list = rccpsDBTrcc_sstlog.selectm(1,0,sstlog_where_sql,sstlog_order_sql)
    
    if sstlog_list == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("获取交易[" + BJEDTE + "][" + BSPSQN + "]所有状态详细信息异常")
        return AfaFlowControl.ExitThisFlow( 'S999', '获取交易所有状态详细信息异常' )
        
    if len(sstlog_list) <= 0:
        AfaLoggerFunc.tradeFatal("流水状态登记簿中无此交易[" + BJEDTE + "][" + BSPSQN + "]状态详细信息")
        return AfaFlowControl.ExitThisFlow( 'S999', '流水状态登记簿中无此交易状态详细信息' )
    
    
    for i in xrange(0,len(sstlog_list)):
        stat_dict = {}
        if not rccpsMap0000Dsstlog2Dstat_dict.map(sstlog_list[i],stat_dict):
            AfaLoggerFunc.tradeFatal("将查询出的业务状态详细信息赋值到输出字典异常")
            return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的业务状态详细信息赋值到输出字典异常' )
        stat_list.append(stat_dict)
    
    AfaLoggerFunc.tradeInfo(">>>结束getTransStateAll")
    return True

################################################################################
# 函数名:    newBilState
# 参数:      BJEDTE:交易日期(必输),BSPSQN:报单序号(必输),HPSTAT:业务状态(必输)}
# 返回值：   False  失败    True  成功
# 函数说明： 新建汇票状态
################################################################################
def newBilState(BJEDTE,BSPSQN,HPSTAT):
    AfaLoggerFunc.tradeInfo(">>>进入newBilState")
    #===========检查表bilbka中是否存在此业务====================================
    bilbka_where_dict = {}
    bilbka_where_dict["BJEDTE"] = BJEDTE
    bilbka_where_dict["BSPSQN"] = BSPSQN
        
    bilbka_dict = rccpsDBTrcc_bilbka.selectu(bilbka_where_dict)
    
    if bilbka_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("获取汇票业务登记簿中交易[" + BJEDTE + "][" + BSPSQN + "]详细信息异常")
        return AfaFlowControl.ExitThisFlow( 'S999', '获取汇票业务登记簿中交易详细信息异常' )
        
    elif len(bilbka_dict) <= 0:
        AfaLoggerFunc.tradeFatal("汇票业务登记簿中无此交易[" + BJEDTE + "][" + BSPSQN + "]详细信息")
        return AfaFlowControl.ExitThisFlow( 'S999', '汇票业务登记簿中无此交易详细信息' )
        
    else:
        MaxHPCUSQ = int(bilbka_dict["HPCUSQ"]) + 1
    
    #===========更新表bilbka中业务对应汇票状态===================================
    bilbka_update_dict = {}
    bilbka_update_dict["HPCUSQ"] = MaxHPCUSQ
    bilbka_update_dict["HPSTAT"] = HPSTAT
    
    bilbka_where_dict = {}
    bilbka_where_dict["BJEDTE"] = BJEDTE
    bilbka_where_dict["BSPSQN"] = BSPSQN
    
    ret = rccpsDBTrcc_bilbka.update(bilbka_update_dict,bilbka_where_dict)
    if ret <= 0:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("登记汇票业务登记簿中交易[" + BJEDTE + "][" + BSPSQN + "]对应当前汇票状态[" + HPSTAT + "]异常")
        return AfaFlowControl.ExitThisFlow( 'S999', '登记汇票业务登记簿中当前汇票状态异常' )
    
    #===========更新表bilinf中汇票对应状态========================================
    bilinf_update_dict = {}
    bilinf_update_dict["HPCUSQ"] = MaxHPCUSQ
    bilinf_update_dict["HPSTAT"] = HPSTAT
    
    bilinf_where_dict = {}
    bilinf_where_dict["BILVER"] = bilbka_dict["BILVER"]
    bilinf_where_dict["BILNO"] = bilbka_dict["BILNO"]
    bilinf_where_dict["BILRS"] = bilbka_dict["BILRS"]
    
    ret = rccpsDBTrcc_bilinf.update(bilinf_update_dict,bilinf_where_dict)
    if ret <= 0:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("登记汇票业务登记簿中当前汇票[" + bilbka_dict['BILVER'] + "][" + bilbka_dict['BILVER'] + "]状态[" + HPSTAT + "]异常")
        return AfaFlowControl.ExitThisFlow( 'S999', '登记汇票信息登记簿中当前汇票状态异常' )
    
    AfaLoggerFunc.tradeInfo(">>>结束newBilState")
    return True


################################################################################
# 函数名:    getTransStateDes
# 参数:      BJEDTE:交易日期,BSPSQN:报单序号,sstlog_dict(业务状态详细信息),Number:倒序条数(默认为0,即当前状态)
# 返回值：   成功    True
#            失败    False
# 函数说明： 查询交易当前业务状态前第N条业务及相关信息
################################################################################
def getTransStateDes(BJEDTE,BSPSQN,stat_dict,DesNumber=0):
    AfaLoggerFunc.tradeInfo(">>>进入getTransStateDes")
    
    if not DesNumber:
        Number = 0
    else:
        Number = int(DesNumber)
        
    #==========获取当前业务状态及信息==========================================
    cur_stat_dict = {}
    if not getTransStateCur(BJEDTE,BSPSQN,cur_stat_dict):
        return AfaFlowControl.ExitThisFlow("S999","获取交易[" + BJEDTE + "][" + BSPSQN + "]当前状态详细信息异常")
    
    BCURSQ = cur_stat_dict['BCURSQ'] - Number
    
    if BCURSQ <= 0:
        return AfaFlowControl.ExitThisFlow("S999","当前交易无前第[" + str(Number) + "]条状态")
        
    #==========获取sstlog对应状态及信息=========================================
    sstlog_where_dict = {}
    sstlog_where_dict["BJEDTE"] = BJEDTE
    sstlog_where_dict["BSPSQN"] = BSPSQN
    sstlog_where_dict["BCURSQ"] = BCURSQ
    
    sstlog_dict = rccpsDBTrcc_sstlog.selectu(sstlog_where_dict)
    
    if sstlog_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("获取交易[" + BJEDTE + "][" + BSPSQN + "]指定状态详细信息异常")
        return AfaFlowControl.ExitThisFlow( 'S999', '获取交易第[' + str(BCURSQ) + ']状态详细信息异常' )
        
    if len(sstlog_dict) <= 0:
        AfaLoggerFunc.tradeFatal("流水状态登记簿中无此交易" + BJEDTE + "][" + BSPSQN + "]指定状态[" + BCSTAT + "][" + BDWFLG + "]详细信息")
        return AfaFlowControl.ExitThisFlow( 'S999', '流水状态登记簿中无此交易第[' + str(BCURSQ) + ']条状态详细信息' )
        
    if not rccpsMap0000Dsstlog2Dstat_dict.map(sstlog_dict,stat_dict):
        AfaLoggerFunc.tradeFatal("将查询出的业务状态详细信息赋值到输出字典异常")
        return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的业务状态详细信息赋值到输出字典异常' )
    
    AfaLoggerFunc.tradeInfo(">>>结束getTransStateDes")
    return True
    
################################################################################
# 函数名:    getTransStateSetm
# 参数:      BJEDTE:交易日期,BSPSQN:报单序号,BCSTAT:当前业务状态,BDWFLG:当前流转处理标识,sstlog_list(业务状态详细信息)
# 返回值：   成功    True
#            失败    False
# 函数说明： 查询交易指定业务状态及相关信息
################################################################################
def getTransStateSetm(BJEDTE,BSPSQN,BCSTAT,BDWFLG,stat_list):
    AfaLoggerFunc.tradeInfo(">>>进入getTransStateSetm")
    
    #==========获取sstlog对应状态及信息=========================================
    sstlog_where_sql = "BJEDTE LIKE '" + BJEDTE + "' and BSPSQN LIKE '" + BSPSQN + "' and BCSTAT LIKE '" + BCSTAT + "' and BDWFLG LIKE '" + BDWFLG + "'"
    
    sstlog_order_sql = 'order by BCURSQ desc'
    
    sstlog_list = rccpsDBTrcc_sstlog.selectm(1,0,sstlog_where_sql,sstlog_order_sql)
    
    if sstlog_list == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("获取交易[" + BJEDTE + "][" + BSPSQN + "]指定状态详细信息异常")
        return AfaFlowControl.ExitThisFlow( 'S999', '获取交易指定状态详细信息异常' )
        
    if len(sstlog_list) <= 0:
        AfaLoggerFunc.tradeFatal("流水状态登记簿中无此交易" + BJEDTE + "][" + BSPSQN + "]指定状态[" + BCSTAT + "][" + BDWFLG + "]详细信息")
        return AfaFlowControl.ExitThisFlow( 'S999', '流水状态登记簿中无此交易指定状态详细信息' )
        
    for i in xrange(0,len(sstlog_list)):
        stat_dict = {}
        if not rccpsMap0000Dsstlog2Dstat_dict.map(sstlog_list[i],stat_dict):
            AfaLoggerFunc.tradeFatal("将查询出的业务状态详细信息赋值到输出字典异常")
            return AfaFlowControl.ExitThisFlow( 'S999', '将查询出的业务状态详细信息赋值到输出字典异常' )
        stat_list.append(stat_dict)
    
    AfaLoggerFunc.tradeInfo(">>>结束getTransStateSetm")
    return True
