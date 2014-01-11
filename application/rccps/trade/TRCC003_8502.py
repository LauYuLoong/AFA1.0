# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.中心类操作(1.本地操作 2.中心操作).汇票解付
#===============================================================================
#   交易文件:   TRCC003_8502.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-06-17
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsHostFunc,miya
import rccpsDBTrcc_bilbka
import rccpsMap8502CTradeContext2Dbilbka,rccpsMap8502CTradeContext2Dbilinf

#=====================交易前处理(本地操作,中心前处理)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.主机类操作(1.本地操作).汇票解付[TRCC003_8502]进入***' )
    
    #====begin 蔡永贵 20110215 增加====
    #新票据号是16位，需要取后8位，版本号为02，同时要兼容老票据号8位，版本号为01
    if TradeContext.BILVER == '02':
        TradeContext.TMP_BILNO = TradeContext.BILNO[-8:]
    else:
        TradeContext.TMP_BILNO = TradeContext.BILNO
    #============end============
    
    #置代理付款行为本机构行号
    TradeContext.PAYBNKCO = TradeContext.SNDBNKCO
    TradeContext.PAYBNKNM = TradeContext.SNDBNKNM
    
    if TradeContext.BILTYP == PL_BILTYP_CASH:
        #=================现金汇票置持票人账号为2431账号科目========================
        TradeContext.PYHACC = TradeContext.BESBNO + PL_ACC_NXYDXZ
        TradeContext.PYHACC = rccpsHostFunc.CrtAcc(TradeContext.PYHACC,25)
        
    AfaLoggerFunc.tradeInfo("TradeContext.PYHACC=" + TradeContext.PYHACC)
    AfaLoggerFunc.tradeInfo("TradeContext.PYHNAM=" + TradeContext.PYHNAM)
    
    #=================交易必要性检查============================================
    AfaLoggerFunc.tradeInfo(">>>开始交易必要性检查")
    
    if abs(float(TradeContext.BILAMT) - float(TradeContext.OCCAMT) - float(TradeContext.RMNAMT)) >= 0.001:
        return AfaFlowControl.ExitThisFlow("S999","多余金额非出票金额与实际结算金额之差")
    
    AfaLoggerFunc.tradeInfo(">>>结束交易必要性检查")
    
    #=================检验是否重复交易==========================================
    AfaLoggerFunc.tradeInfo(">>>开始校验重复交易")
    
    bilbka_where_dict = {}
    bilbka_where_dict['BILRS']   = PL_BILRS_OUT
    bilbka_where_dict['BILVER']  = TradeContext.BILVER
    bilbka_where_dict['BILNO']   = TradeContext.BILNO
    bilbka_where_dict['HPSTAT']  = PL_HPSTAT_PAYC
    
    bilbka_dict = rccpsDBTrcc_bilbka.selectu(bilbka_where_dict)
    if bilbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","查询原汇票信息异常,校验重复交易失败")
        
    if len(bilbka_dict) > 0:
        return AfaFlowControl.ExitThisFlow("S999","此汇票已被解付,重复交易,禁止提交")
    
    AfaLoggerFunc.tradeInfo(">>>结束校验重复交易")
    
    if TradeContext.BILTYP != PL_BILTYP_CASH:
        #=================校验入账账号户名======================================
        AfaLoggerFunc.tradeInfo(">>>开始校验入账账号户名")
        
        TradeContext.HostCode = '8810'
        
        TradeContext.ACCNO = TradeContext.PYHACC
        
        AfaLoggerFunc.tradeDebug("gbj test :" + TradeContext.ACCNO)
        
        rccpsHostFunc.CommHost( TradeContext.HostCode )
        
        if TradeContext.errorCode != '0000':
            return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
        
        AfaLoggerFunc.tradeDebug("gbj test :" + TradeContext.ACCNM)
        
        if TradeContext.ACCNM != TradeContext.PYHNAM:
            return AfaFlowControl.ExitThisFlow('S999',"账号户名不符")
            
        if TradeContext.ACCST != '0' and TradeContext.ACCST != '2':
            return AfaFlowControl.ExitThisFlow('S999','入账账号状态不正常')
        
        AfaLoggerFunc.tradeInfo(">>>结束校验入账账号户名")
    
    #=================校验汇票密押==============================================
    AfaLoggerFunc.tradeInfo(">>>开始校验汇票密押")
    
    if TradeContext.BILTYP == PL_BILTYP_CASH:
        TYPE = PL_TYPE_XJHP
    elif TradeContext.BILTYP == PL_BILTYP_TRAN:
        TYPE = PL_TYPE_ZZHP
    else:
        return AfaFlowControl.ExitThisFlow("S999","汇票类型非法")
    
    AfaLoggerFunc.tradeDebug('TradeContext密押:' + TradeContext.SEAL )
    
    MIYA = TradeContext.SEAL
    TRCDAT = TradeContext.BILDAT
    TRCNO = TradeContext.BILNO
    REMBNKCO  = TradeContext.REMBNKCO                  #签发行
    PAYBNKCO  = TradeContext.PAYBNKCO                  #代理付款行
    REMBNKCO  = REMBNKCO.rjust(12,'0')
    PAYBNKCO  = PAYBNKCO.rjust(12,'0')
    AMOUNT = str(TradeContext.BILAMT).split('.')[0] + str(TradeContext.BILAMT).split('.')[1]
    AMOUNT = AMOUNT.rjust(15,'0')
    INFO   = ""
    
    AfaLoggerFunc.tradeDebug('处理类型(0-编押 1-核押):' + str(PL_SEAL_DEC) )
    AfaLoggerFunc.tradeDebug('业务种类(1-现金汇票 2-转账汇票 3-电子汇兑业务):' + TYPE )
    AfaLoggerFunc.tradeDebug('出票日期:' + TRCDAT )
    AfaLoggerFunc.tradeDebug('汇票号码:' + TRCNO )
    AfaLoggerFunc.tradeDebug('出票金额:' + str(AMOUNT) )
    AfaLoggerFunc.tradeDebug('出票行号:' + str(REMBNKCO) )
    AfaLoggerFunc.tradeDebug('代理付款行号:' + str(PAYBNKCO) )
    AfaLoggerFunc.tradeDebug('汇票密押:' + MIYA )
    AfaLoggerFunc.tradeDebug('OTHERINFO[' + str(INFO) + ']')
    
    AfaLoggerFunc.tradeDebug('TradeContext密押:' + TradeContext.SEAL )
    
    #====begin 蔡永贵 20110215 修改====
    #ret = miya.DraftEncrypt(PL_SEAL_DEC,TYPE,TRCDAT,TRCNO,AMOUNT,REMBNKCO,PAYBNKCO,INFO,MIYA)
    ret = miya.DraftEncrypt(PL_SEAL_DEC,TYPE,TRCDAT,TradeContext.TMP_BILNO,AMOUNT,REMBNKCO,PAYBNKCO,INFO,MIYA)
    #============end============
    
    AfaLoggerFunc.tradeDebug('TradeContext密押:' + TradeContext.SEAL )
    
    AfaLoggerFunc.tradeDebug( 'ret=' + str(ret) )
    
    if ret == 9005:
        return AfaFlowControl.ExitThisFlow('S999','密押错,请检查业务要素和密押')
    elif ret > 0:
        return AfaFlowControl.ExitThisFlow('S999','调用密押服务器失败')
    
    AfaLoggerFunc.tradeInfo(">>>结束校验汇票密押")
    
    #=================登记汇票登记簿========================================
    AfaLoggerFunc.tradeInfo(">>>开始登记汇票登记簿")
    
    #=================为汇票业务登记簿赋值==================================
    TradeContext.OPRNO    = PL_HPOPRNO_JF                #业务类型解付
    TradeContext.DCFLG    = PL_DCFLG_CRE
    TradeContext.BILRS    = PL_BILRS_OUT
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.TRCNO    = TradeContext.SerialNo
    TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN
    TradeContext.RCVMBRCO = '1000000000'
    
    bilbka_dict = {}
    if not rccpsMap8502CTradeContext2Dbilbka.map(bilbka_dict):
        return AfaFlowControl.ExitThisFlow('S999','为汇票业务登记簿赋值异常')
    
    #=================登记汇票业务登记簿====================================
    
    if not rccpsDBFunc.insTransBil(bilbka_dict):
        if not AfaDBFunc.RollbackSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeError(">>>Rollback异常")
        AfaLoggerFunc.tradeInfo(">>>Rollback成功")
        return AfaFlowControl.ExitThisFlow('S999','登记汇票业务登记簿异常')
    
    #=================为汇票信息登记簿赋值==================================
    
    bilinf_dict = {}
    if not rccpsMap8502CTradeContext2Dbilinf.map(bilinf_dict):
        if not AfaDBFunc.RollbackSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeError(">>>Rollback异常")
        AfaLoggerFunc.tradeInfo(">>>Rollback成功")
        return AfaFlowControl.ExitThisFlow('S999','为汇票信息登记簿赋值异常')
        
    bilinf_dict['NOTE3'] = TradeContext.BESBNO    #将交易机构赋值到汇票信息登记簿中note3字段
    
    #=================登记汇票信息登记簿====================================
    
    if not rccpsDBFunc.insInfoBil(bilinf_dict):
        if not AfaDBFunc.RollbackSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeError(">>>Rollback异常")
        AfaLoggerFunc.tradeInfo(">>>Rollback成功")
        return AfaFlowControl.ExitThisFlow('S999','登记汇票信息登记簿异常')
    
    AfaLoggerFunc.tradeInfo(">>>结束登记汇票登记簿")
    
    #=================设置状态为发送处理中======================================
    AfaLoggerFunc.tradeInfo(">>>开始设置业务状态为发送处理中")
    
    stat_dict = {}
    stat_dict['BJEDTE'] = TradeContext.BJEDTE
    stat_dict['BSPSQN'] = TradeContext.BSPSQN
    stat_dict['BCSTAT'] = PL_BCSTAT_SND
    stat_dict['BDWFLG'] = PL_BDWFLG_WAIT
    if not rccpsState.setTransState(stat_dict):
        if not AfaDBFunc.RollbackSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeError(">>>Rollback异常")
        AfaLoggerFunc.tradeInfo(">>>Rollback成功")
        return AfaFlowControl.ExitThisFlow('S999','设置状态为发送处理中异常')
    
    AfaLoggerFunc.tradeInfo(">>>结束设置业务状态为发送处理中")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
    AfaLoggerFunc.tradeInfo(">>>Commit成功")
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.主机类操作(1.本地操作).汇票解付[TRCC003_8502]结束***' )
    
    #=================为汇票解付报文赋值========================================
    AfaLoggerFunc.tradeInfo(">>>开始为解付报文赋值")
    
    TradeContext.MSGTYPCO = "SET008"
    TradeContext.SNDBRHCO = TradeContext.BESBNO
    TradeContext.SNDCLKNO = TradeContext.BETELR
    TradeContext.SNDTRDAT = TradeContext.BJEDTE
    TradeContext.SNDTRTIM = TradeContext.BJETIM
    TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO = "21"
    TradeContext.ROPRTPNO = ""
    TradeContext.TRANTYP  = "0"
    TradeContext.ORTRCCO  = ""
    
    TradeContext.TRCCO     = '2100100'
    TradeContext.TRCNO     = TradeContext.SerialNo
    TradeContext.RCVSTLBIN = TradeContext.RCVMBRCO
    TradeContext.OPRATTNO  = ""
    
    AfaLoggerFunc.tradeInfo(">>>结束为解付报文赋值")
    
    return True

#=====================交易后处理================================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.主机类操作(2.中心操作).汇票解付[TRCC003_8502]进入***' )
    
    #=================判断afe是否发送成功=======================================
    if TradeContext.errorCode != '0000':
        #=============AFE发送失败,设置状态为发送失败============================
        AfaLoggerFunc.tradeInfo('>>>AFE发送失败,开始设置状态为发送失败')
        
        stat_dict = {}
        stat_dict['BJEDTE']  = TradeContext.BJEDTE
        stat_dict['BSPSQN']  = TradeContext.BSPSQN
        stat_dict['BESBNO']  = TradeContext.BESBNO
        stat_dict['BETELR']  = TradeContext.BETELR
        stat_dict['BCSTAT']  = PL_BCSTAT_SND
        stat_dict['BDWFLG']  = PL_BDWFLG_FAIL
        stat_dict['PRCCO']   = TradeContext.errorCode
        stat_dict['STRINFO'] = TradeContext.errorMsg
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999','设置状态为发送失败异常')
            
        AfaLoggerFunc.tradeInfo('>>>结束设置状态为发送失败')
    else:
        #=============AFE发送成功,设置状态为发送成功============================
        AfaLoggerFunc.tradeInfo('>>>AFE发送成功,开始设置状态为发送成功')
        
        stat_dict = {}
        stat_dict['BJEDTE']  = TradeContext.BJEDTE
        stat_dict['BSPSQN']  = TradeContext.BSPSQN
        stat_dict['BESBNO']  = TradeContext.BESBNO
        stat_dict['BETELR']  = TradeContext.BETELR
        stat_dict['BCSTAT']  = PL_BCSTAT_SND
        stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
        stat_dict['PRCCO']   = TradeContext.errorCode
        stat_dict['STRINFO'] = TradeContext.errorMsg
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999','设置状态为发送成功异常')
            
        AfaLoggerFunc.tradeInfo('>>>结束设置状态为发送成功')
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
    AfaLoggerFunc.tradeInfo(">>>Commit成功")
    
    TradeContext.errorCode = '0000'
    TradeContext.errorMsg  = '发送农信银中心成功'
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.主机类操作(2.中心操作).汇票解付[TRCC003_8502]结束***' )
    
    return True
    
