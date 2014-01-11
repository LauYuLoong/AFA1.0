# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.回执类操作(1.回执操作).通讯回执报文接收
#===============================================================================
#   交易文件:   TRCC004_1111.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,rccpsState
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsHostFunc,rccpsDBTrcc_bilinf,rccpsEntries
import rccpsDBTrcc_hdcbka,rccpsDBTrcc_hpcbka,rccpsDBTrcc_pjcbka,rccpsDBTrcc_ztcbka,rccpsDBTrcc_trccan,rccpsDBTrcc_mrqtbl,rccpsDBTrcc_existp,rccpsDBTrcc_rekbal


#=====================回执个性化处理(本地操作)==================================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.回执类操作(1.回执操作).通讯回执报文接收[TRC004_1111]进入***' )
    #=================初始化返回信息============================================
    if AfaUtilTools.trim(TradeContext.STRINFO) == "":
        TradeContext.STRINFO = rccpsDBFunc.getErrInfo(TradeContext.PRCCO)
        
    AfaLoggerFunc.tradeDebug("TradeContext.STRINFO=" + TradeContext.STRINFO)
        
    #=================检查业务类型==============================================
    if TradeContext.ROPRTPNO == "20":
        #==========实时汇兑业务=================================================
        AfaLoggerFunc.tradeInfo(">>>原业务类型为20,汇兑业务")

        #==========根据发送行号,委托日期,交易流水号查询原交易信息===============
        AfaLoggerFunc.tradeInfo(">>>开始根据发送行号,委托日期,交易流水号查询交易信息")
        ORSNDMBRCO = TradeContext.ORMFN[:10]
        ORTRCDAT   = TradeContext.ORMFN[10:18]
        ORTRCNO    = TradeContext.ORMFN[18:]
        
        trc_dict = {}
        if not rccpsDBFunc.getTransTrcPK(ORSNDMBRCO,ORTRCDAT,ORTRCNO,trc_dict):
            return False
        
        AfaLoggerFunc.tradeInfo(">>>结束根据发送行号,委托日期,交易流水号查询交易信息")

        #==========检查原业务状态是否为发送=====================================
        if trc_dict['BCSTAT'] != PL_BCSTAT_SND:
            return AfaFlowControl.ExitThisFlow("S999","当前交易状态非发送状态,停止处理")
        
        #==========根据中心返回码设置原交易状态=================================
        AfaLoggerFunc.tradeInfo(">>>中心处理码为[" + TradeContext.PRCCO + "]")
        
        stat_dict = {}
        stat_dict['BJEDTE'] = trc_dict['BJEDTE']
        stat_dict['BSPSQN'] = trc_dict['BSPSQN']
        stat_dict['BESBNO'] = trc_dict['BESBNO']
        stat_dict['BETELR'] = TradeContext.BETELR
        stat_dict['PRCCO']  = TradeContext.PRCCO
        stat_dict['STRINFO']= TradeContext.STRINFO
        if TradeContext.PRCCO == "RCCI0000":
            #==========中心返回表示成功的处理码,开始设置状态为收妥==============
            AfaLoggerFunc.tradeInfo(">>>开始设置状态为收妥")
            
            if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_MFERCV,PL_BDWFLG_WAIT):
                return False
                
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit异常")
            AfaLoggerFunc.tradeInfo(">>>Commit成功")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_MFERCV
            stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
            
            if not rccpsState.setTransState(stat_dict):
                return False
            
            AfaLoggerFunc.tradeInfo(">>>结束设置状态为收妥")
            
        elif TradeContext.PRCCO == "RCCO1078" or TradeContext.PRCCO == "RCCO1079":
            #==========中心返回表示排队的处理码,开始设置状态为排队==============
            AfaLoggerFunc.tradeInfo(">>>开始设置状态为排队")
            
            if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_MFEQUE,PL_BDWFLG_WAIT):
                return False
            
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit异常")
            AfaLoggerFunc.tradeInfo(">>>Commit成功")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_MFEQUE
            stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
            
            if not rccpsState.setTransState(stat_dict):
                return False
            
            AfaLoggerFunc.tradeInfo(">>>结束设置状态为排队")
            
        else:
            #==========中心返回表示拒绝的处理码,开始设置状态为拒绝==============
            AfaLoggerFunc.tradeInfo(">>>开始设置状态为拒绝")
            
            if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_MFERFE,PL_BDWFLG_WAIT):
                return False
            
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit异常")
            AfaLoggerFunc.tradeInfo(">>>Commit成功")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_MFERFE
            stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
            
            if not rccpsState.setTransState(stat_dict):
                return False
                
            AfaLoggerFunc.tradeInfo(">>>结束设置状态为拒绝")
            
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit异常")
            AfaLoggerFunc.tradeInfo(">>>Commit成功")
            
            #==========设置当前机构为原机构====================================
            TradeContext.BESBNO = trc_dict['BESBNO']
            TradeContext.BETELR = trc_dict['BETELR']
            TradeContext.TERMID = trc_dict['TERMID']
            
            #==========设置原交易状态为抹账处理中==============================
            AfaLoggerFunc.tradeInfo(">>>开始设置状态为抹账处理中")
            
            TradeContext.NOTE3 = "中心拒绝,行内自动抹账"
            
            if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_HCAC,PL_BDWFLG_WAIT):
                return False
            
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                AfaLoggerFunc.tradeInfo(">>>Commit异常")
            AfaLoggerFunc.tradeInfo(">>>Commit成功")
                
            AfaLoggerFunc.tradeInfo(">>>结束设置状态为抹账处理中")
            #==========发起主机抹账============================================
            AfaLoggerFunc.tradeInfo(">>>开始主机抹账")
            
            ##====== 张恒 抹账操作 增加于20091112 ==============##
            #汇兑往帐抹帐字典赋值
            input_dict = {}
            input_dict['BJEDTE']     = trc_dict['BJEDTE']
            input_dict['BSPSQN']     = trc_dict['BSPSQN']
            if len(trc_dict['PYRACC']) != 0 :       
                 input_dict['PYRACC']     = trc_dict['PYRACC']
            else:
                 input_dict['PYRACC']     = ''
            input_dict['OCCAMT']     = str(trc_dict['OCCAMT'])
            input_dict['BBSSRC']     = trc_dict['BBSSRC']
            input_dict['BESBNO']     = TradeContext.BESBNO
            
            #调用汇兑往帐抹帐
            rccpsEntries.HDWZMZ(input_dict)
            
            #=====调起主机记账接口====
            rccpsHostFunc.CommHost( TradeContext.HostCode )
            
            AfaLoggerFunc.tradeInfo(">>>结束主机抹账")
            stat_dict['PRCCO'] = ''
            if TradeContext.errorCode == '0000':
                #==========设置原交易状态为抹账成功============================
                AfaLoggerFunc.tradeInfo(">>>开始设置状态为抹账成功")
                
                stat_dict['BCSTAT'] = PL_BCSTAT_HCAC
                stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
                if TradeContext.existVariable('TRDT'):
                    AfaLoggerFunc.tradeInfo("TRDT:" + TradeContext.TRDT)
                    stat_dict['TRDT'] = TradeContext.TRDT
                if TradeContext.existVariable('TLSQ'):
                    AfaLoggerFunc.tradeInfo("TLSQ:" + TradeContext.TLSQ)
                    stat_dict['TLSQ'] = TradeContext.TLSQ
                if TradeContext.existVariable('DASQ'):
                    AfaLoggerFunc.tradeInfo("DASQ:" + TradeContext.DASQ)
                    stat_dict['DASQ']   = TradeContext.DASQ
                stat_dict['MGID']   = TradeContext.errorCode
                stat_dict['STRINFO']= TradeContext.errorMsg
                
                if not rccpsState.setTransState(stat_dict):
                    return False
                
                AfaLoggerFunc.tradeInfo(">>>结束设置状态为抹账成功")
                
                if trc_dict['TRCCO'] == '2000004':
                    #===========退汇业务,更新原交易挂账代销账序号==============
                    AfaLoggerFunc.tradeInfo(">>>开始更新原交易挂账代销账序号")
                    
                    orstat_dict = {}
                    orstat_dict['BJEDTE'] = trc_dict['BOJEDT']
                    orstat_dict['BSPSQN'] = trc_dict['BOSPSQ']
                    orstat_dict['BCSTAT'] = PL_BCSTAT_HANG
                    orstat_dict['BDWFLG'] = PL_BDWFLG_SUCC
                    if TradeContext.existVariable('DASQ'):
                        orstat_dict['DASQ']   = TradeContext.DASQ
                    
                    if not rccpsState.setTransState(orstat_dict):
                        return False
                    
                    AfaLoggerFunc.tradeInfo(">>>结束更新原交易挂账代销账序号")
                
            else:
                #==========设置原交易状态为抹账失败============================
                AfaLoggerFunc.tradeInfo(">>>开始设置状态为抹账失败")
                
                stat_dict['BCSTAT'] = PL_BCSTAT_HCAC
                stat_dict['BDWFLG'] = PL_BDWFLG_FAIL
                if TradeContext.existVariable('TRDT'):
                    AfaLoggerFunc.tradeInfo("TRDT:" + TradeContext.TRDT)
                    stat_dict['TRDT'] = TradeContext.TRDT
                if TradeContext.existVariable('TLSQ'):
                    AfaLoggerFunc.tradeInfo("TLSQ:" + TradeContext.TLSQ)
                    stat_dict['TLSQ'] = TradeContext.TLSQ 
                if TradeContext.existVariable('DASQ'):
                    AfaLoggerFunc.tradeInfo("DASQ:" + TradeContext.DASQ)
                    stat_dict['DASQ']   = TradeContext.DASQ
                stat_dict['MGID']   = TradeContext.errorCode
                stat_dict['STRINFO']= TradeContext.errorMsg
                
                if not rccpsState.setTransState(stat_dict):
                    return False
                
                AfaLoggerFunc.tradeInfo(">>>结束设置状态为抹账失败")
            
    elif TradeContext.ROPRTPNO == "21":
        #==========全国汇票业务================================================
        AfaLoggerFunc.tradeInfo(">>>原业务类型为21,汇票业务")
        
        #==========根据发送行号,委托日期,交易流水号查询原交易信息==============
        AfaLoggerFunc.tradeInfo(">>>开始根据发送行号,委托日期,交易流水号查询交易信息")
        ORSNDMBRCO = TradeContext.ORMFN[:10]
        ORTRCDAT   = TradeContext.ORMFN[10:18]
        ORTRCNO    = TradeContext.ORMFN[18:]
        
        trc_dict = {}
        if not rccpsDBFunc.getTransBilPK(ORSNDMBRCO,ORTRCDAT,ORTRCNO,trc_dict):
            return False
        
        if not rccpsDBFunc.getInfoBil(trc_dict['BILVER'],trc_dict['BILNO'],trc_dict['BILRS'],trc_dict):
            return False

        TradeContext.ORTRCCO = trc_dict['TRCCO']
        
        AfaLoggerFunc.tradeInfo(">>>结束根据发送行号,委托日期,交易流水号查询交易信息")

        #==========检查原业务状态是否为发送====================================
        if trc_dict['BCSTAT'] != PL_BCSTAT_SND:
            return AfaFlowControl.ExitThisFlow("S999","当前交易状态非发送状态,停止处理")
        
        #==========根据中心返回码设置原交易状态================================
        AfaLoggerFunc.tradeInfo(">>>中心处理码为[" + TradeContext.PRCCO + "]")
        
        stat_dict = {}
        stat_dict['BJEDTE'] = trc_dict['BJEDTE']
        stat_dict['BSPSQN'] = trc_dict['BSPSQN']
        stat_dict['BESBNO'] = trc_dict['BESBNO']
        stat_dict['BETELR'] = TradeContext.BETELR
        stat_dict['PRCCO']  = TradeContext.PRCCO
        stat_dict['STRINFO']= TradeContext.STRINFO
        
        if TradeContext.PRCCO == "RCCI0000":
            #==========中心返回表示成功的处理码,开始设置状态为收妥=============
            AfaLoggerFunc.tradeInfo(">>>开始设置状态为收妥")
            
            if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_MFERCV,PL_BDWFLG_WAIT):
                return False
                
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit异常")
            AfaLoggerFunc.tradeInfo(">>>Commit成功")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_MFERCV
            stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
            
            if not rccpsState.setTransState(stat_dict):
                return False
            
            AfaLoggerFunc.tradeInfo(">>>结束设置状态为收妥")
            
        elif TradeContext.PRCCO == "RCCO1078" or TradeContext.PRCCO == "RCCO1079":
            #==========中心返回表示排队的处理码,开始设置状态为排队=============
            AfaLoggerFunc.tradeInfo(">>>开始设置状态为排队")
            
            if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_MFEQUE,PL_BDWFLG_WAIT):
                return False
            
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit异常")
            AfaLoggerFunc.tradeInfo(">>>Commit成功")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_MFEQUE
            stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
            
            if not rccpsState.setTransState(stat_dict):
                return False
            
            AfaLoggerFunc.tradeInfo(">>>结束设置状态为排队")
            
        else:
            #==========中心返回表示拒绝的处理码,开始设置状态为拒绝=============
            AfaLoggerFunc.tradeInfo(">>>开始设置状态为拒绝")
            
            if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_MFERFE,PL_BDWFLG_WAIT):
                return False
            
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit异常")
            AfaLoggerFunc.tradeInfo(">>>Commit成功")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_MFERFE
            stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
            
            if not rccpsState.setTransState(stat_dict):
                return False
                
            AfaLoggerFunc.tradeInfo(">>>结束设置状态为拒绝")
            
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit异常")
            AfaLoggerFunc.tradeInfo(">>>Commit成功")
            
            #==========如果原交易为汇票签发,需自动抹账=========================
            if TradeContext.ORTRCCO == '2100001':
                
                #==========设置当前机构为原机构,当前柜员为原柜员===============
                TradeContext.BESBNO = trc_dict['BESBNO']
                TradeContext.BETELR = trc_dict['BETELR']
                TradeContext.TERMID = trc_dict['TERMID']
                
                #==========设置原交易状态为抹账处理中==========================
                AfaLoggerFunc.tradeInfo(">>>开始设置状态为抹账处理中")
                
                TradeContext.NOTE3 = "中心拒绝,行内自动抹账"
                
                if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_HCAC,PL_BDWFLG_WAIT):
                    return False
                
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    return AfaFlowControl.ExitThisFlow("S999","Commit异常")
                AfaLoggerFunc.tradeInfo(">>>Commit成功")
                    
                AfaLoggerFunc.tradeInfo(">>>结束设置状态为抹账处理中")
                #==========发起主机抹账========================================
                AfaLoggerFunc.tradeInfo(">>>开始主机抹账")
                
                #=====如果资金来源为代销账，使用8813红字冲销====
                if trc_dict['BBSSRC'] == '3':                                              #待销账
                    TradeContext.BJEDTE   = trc_dict['BJEDTE']
                    TradeContext.BSPSQN   = trc_dict['BSPSQN']
                    TradeContext.OCCAMT   = str(trc_dict['BILAMT'])                        #抹账金额为出票金额
                    TradeContext.HostCode = '8813'
                    TradeContext.RCCSMCD  = PL_RCCSMCD_HPQF                                #主机摘要码:汇票签发
                    TradeContext.DASQ     = ''
                    TradeContext.RVFG     = '0'                                            #红蓝字标志 0
                    TradeContext.SBAC     =  TradeContext.BESBNO  +  PL_ACC_HCHK           #借方账号(汇票签发,借汇出汇款)
                    TradeContext.RBAC     =  TradeContext.BESBNO  +  PL_ACC_NXYDXZ         #贷方账号(贷农信银代销账)
                    #=====开始调函数拼贷方账号第25位校验位====
                    TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
                    TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC, 25)
                    AfaLoggerFunc.tradeInfo( '借方账号:' + TradeContext.SBAC )
                    AfaLoggerFunc.tradeInfo( '贷方账号:' + TradeContext.RBAC )
                else:
                    TradeContext.BOJEDT  = trc_dict['BJEDTE']
                    TradeContext.BOSPSQ  = trc_dict['BSPSQN']
                    TradeContext.HostCode='8820'
                
                #=====调起主机记账接口====
                rccpsHostFunc.CommHost( TradeContext.HostCode )
                
                AfaLoggerFunc.tradeInfo(">>>结束主机抹账")
                if TradeContext.errorCode == '0000':
                    #==========设置原交易状态为抹账成功========================
                    AfaLoggerFunc.tradeInfo(">>>开始设置状态为抹账成功")
                    
                    stat_dict['BCSTAT'] = PL_BCSTAT_HCAC
                    stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
                    if TradeContext.existVariable('TRDT'):
                        AfaLoggerFunc.tradeInfo("TRDT:" + TradeContext.TRDT)
                        stat_dict['TRDT'] = TradeContext.TRDT
                    if TradeContext.existVariable('TLSQ'):
                        AfaLoggerFunc.tradeInfo("TLSQ:" + TradeContext.TLSQ)
                        stat_dict['TLSQ'] = TradeContext.TLSQ 
                    if TradeContext.existVariable('DASQ'):
                        AfaLoggerFunc.tradeInfo("DASQ:" + TradeContext.DASQ)
                        stat_dict['DASQ']   = TradeContext.DASQ
                    stat_dict['MGID']   = TradeContext.errorCode
                    stat_dict['STRINFO']= TradeContext.errorMsg
                    
                    if not rccpsState.setTransState(stat_dict):
                        return False
                    
                    AfaLoggerFunc.tradeInfo(">>>结束设置状态为抹账成功")
                else:
                    #==========设置原交易状态为抹账失败========================
                    AfaLoggerFunc.tradeInfo(">>>开始设置状态为抹账失败")
                    
                    stat_dict['BCSTAT'] = PL_BCSTAT_HCAC
                    stat_dict['BDWFLG'] = PL_BDWFLG_FAIL
                    if TradeContext.existVariable('TRDT'):
                        AfaLoggerFunc.tradeInfo("TRDT:" + TradeContext.TRDT)
                        stat_dict['TRDT'] = TradeContext.TRDT
                    if TradeContext.existVariable('TLSQ'):
                        AfaLoggerFunc.tradeInfo("TLSQ:" + TradeContext.TLSQ)
                        stat_dict['TLSQ'] = TradeContext.TLSQ
                    if TradeContext.existVariable('DASQ'):
                        AfaLoggerFunc.tradeInfo("DASQ:" + TradeContext.DASQ)
                        stat_dict['DASQ']   = TradeContext.DASQ
                    stat_dict['MGID']   = TradeContext.errorCode
                    stat_dict['STRINFO']= TradeContext.errorMsg
                    
                    if not rccpsState.setTransState(stat_dict):
                        return False
                    
                    AfaLoggerFunc.tradeInfo(">>>结束设置状态为抹账失败")
                    
            #==========如果原交易为汇票退票,需重置实际结算金额和结余金额=======
            if TradeContext.ORTRCCO == '2100103':
                AfaLoggerFunc.tradeInfo(">>>汇票退票,开始重置实际结算金额和结余金额")
                
                bilinf_update_dict = {}
                bilinf_update_dict['OCCAMT'] = "0.00"
                bilinf_update_dict['RMNAMT'] = "0.00"
                
                bilinf_where_dict = {}
                bilinf_where_dict['BILVER'] = trc_dict['BILVER']
                bilinf_where_dict['BILNO']  = trc_dict['BILNO']
                
                ret = rccpsDBTrcc_bilinf.update(bilinf_update_dict,bilinf_where_dict)
                
                if ret == None:
                    return AfaFlowControl.ExitThisFlow("S999","更新汇票信息登记簿异常")
                    
                if ret <= 0:
                    return AfaFlowControl.ExitThisFlow("S999","无对应的汇票信息")
                
                AfaLoggerFunc.tradeInfo(">>>汇票退票,结束重置实际结算金额和结余金额")
            
    elif TradeContext.ROPRTPNO == "99":
        #==========信息类业务==================================================
        AfaLoggerFunc.tradeInfo(">>>原业务类型为99,信息类业务")
        
        #==========根据发送行号,委托日期,交易流水号查询原交易信息===========
        AfaLoggerFunc.tradeInfo(">>>开始根据发送行号,委托日期,交易流水号查询交易信息")
        bka_where_dict = {}
        bka_where_dict['SNDMBRCO'] = TradeContext.ORMFN[:10]
        bka_where_dict['TRCDAT']   = TradeContext.ORMFN[10:18]
        bka_where_dict['TRCNO']    = TradeContext.ORMFN[18:]
            
        bka_update_dict = {}
        bka_update_dict['PRCCO']   = TradeContext.PRCCO
        bka_update_dict['STRINFO'] = TradeContext.STRINFO
        
        #==========查询汇兑查询查复登记簿======================================
        AfaLoggerFunc.tradeInfo(">>>开始查询汇兑查询查复登记簿")
        
        bka_dict = rccpsDBTrcc_hdcbka.selectu(bka_where_dict)
        
        if bka_dict == None:
            return AfaFlowControl.ExitThisFlow("S999", "查询汇兑查询业务登记簿异常")
            
        if len(bka_dict) > 0:
            #======汇兑查询查复登记簿中找到原交易信息,开始更新回执信息=========
            AfaLoggerFunc.tradeInfo(">>>汇兑查询查复登记簿中找到原交易信息,开始更新回执信息")
            
            ret = rccpsDBTrcc_hdcbka.updateCmt(bka_update_dict,bka_where_dict)
            
            if ret <= 0:
                return AfaFlowControl.ExitThisFlow("S999", "更新回执信息异常")
            
            AfaLoggerFunc.tradeInfo(">>>结束更新回执信息")
            
            if (bka_dict['TRCCO'] == '9900512' or bka_dict['TRCCO'] == '9900523') and TradeContext.PRCCO != 'RCCI0000':
                #======汇兑\特约汇兑查复业务,中心返回码非成功,修改原查询交易查询查复标识为未查复==
                AfaLoggerFunc.tradeInfo(">>>汇兑\特约汇兑查复业务,中心返回码非成功")
                AfaLoggerFunc.tradeInfo(">>>开始修改原汇兑\特约汇兑查询交易查询查复标识为未查复")
                
                bka_update_dict = {'ISDEAL':PL_ISDEAL_UNDO}
                bka_where_dict = {'BJEDTE':bka_dict['BOJEDT'],'BSPSQN':bka_dict['BOSPSQ']}
                
                ret = rccpsDBTrcc_hdcbka.updateCmt(bka_update_dict,bka_where_dict)
                
                if ret <= 0:
                    return AfaFlowControl.ExitThisFlow("S999", "更新原汇兑\特约汇兑查询交易查询查复标识为未查复异常")
                
                AfaLoggerFunc.tradeInfo(">>>结束修改原汇兑\特约汇兑查询交易查询查复标识为未查复")
                
        else:
            #======汇兑查询查复登记簿中未找到原交易信息,开始查询票据查询查复登记簿====
            AfaLoggerFunc.tradeInfo(">>>汇兑查询查复登记簿中未找到原交易信息,开始查询票据查询查复登记簿")
            
            bka_dict = rccpsDBTrcc_pjcbka.selectu(bka_where_dict)
            
            if bka_dict == None:
                return AfaFlowControl.ExitThisFlow("S999", "查询票据查询业务登记簿异常")
            
            if len(bka_dict) > 0:
                #======票据查询查复登记簿中找到原交易信息,开始更新回执信息====
                AfaLoggerFunc.tradeInfo(">>>票据查询查复登记簿中找到原交易信息,开始更新回执信息")
                
                ret = rccpsDBTrcc_pjcbka.updateCmt(bka_update_dict,bka_where_dict)
                
                if ret <= 0:
                    return AfaFlowControl.ExitThisFlow("S999", "更新回执信息异常")
                    
                AfaLoggerFunc.tradeInfo(">>>结束更新回执信息")
                
                if bka_dict['TRCCO'] == '9900521' and TradeContext.PRCCO != 'RCCI0000':
                    #======票据查复业务,中心返回码非成功,修改原查询交易查询查复标识为未查复==
                    AfaLoggerFunc.tradeInfo(">>>票据查复业务,中心返回码非成功")
                    AfaLoggerFunc.tradeInfo(">>>开始修改原票据查询交易查询查复标识为未查复")
                    
                    bka_update_dict = {'ISDEAL':PL_ISDEAL_UNDO}
                    bka_where_dict = {'BJEDTE':bka_dict['BOJEDT'],'BSPSQN':bka_dict['BOSPSQ']}
                    
                    ret = rccpsDBTrcc_pjcbka.updateCmt(bka_update_dict,bka_where_dict)
                    
                    if ret <= 0:
                        return AfaFlowControl.ExitThisFlow("S999", "更新原票据查询交易查询查复标识为未查复异常")
                    
                    AfaLoggerFunc.tradeInfo(">>>结束修改原票据查询交易查询查复标识为未查复")
                
            else:
                #======票据查询查复登记簿中未找到原交易信息,开始查询汇票查询查复登记簿====
                AfaLoggerFunc.tradeInfo(">>>票据查询查复登记簿中未找到原交易信息,开始查询汇票查询查复登记簿")
                
                bka_dict = rccpsDBTrcc_hpcbka.selectu(bka_where_dict)
                
                if bka_dict == None:
                    return AfaFlowControl.ExitThisFlow("S999", "查询汇票查询业务登记簿异常")
                    
                if len(bka_dict) > 0:
                    #======汇票查询查复登记簿中找到原交易信息,开始更新回执信息====
                    AfaLoggerFunc.tradeInfo(">>>汇票查询查复登记簿中找到原交易信息,开始更新回执信息")
                    
                    ret = rccpsDBTrcc_hpcbka.updateCmt(bka_update_dict,bka_where_dict)
                    
                    if ret <= 0:
                        return AfaFlowControl.ExitThisFlow("S999", "更新回执信息异常")
                        
                    AfaLoggerFunc.tradeInfo(">>>结束更新回执信息")
                    
                    if bka_dict['TRCCO'] == '9900527' and TradeContext.PRCCO != 'RCCI0000':
                        #======汇票查复业务,中心返回码非成功,修改原查询交易查询查复标识为未查复==
                        AfaLoggerFunc.tradeInfo(">>>汇票查复业务,中心返回码非成功")
                        AfaLoggerFunc.tradeInfo(">>>开始修改原汇票查询交易查询查复标识为未查复")
                        
                        bka_update_dict = {'ISDEAL':PL_ISDEAL_UNDO}
                        bka_where_dict = {'BJEDTE':bka_dict['BOJEDT'],'BSPSQN':bka_dict['BOSPSQ']}
                        
                        ret = rccpsDBTrcc_hpcbka.updateCmt(bka_update_dict,bka_where_dict)
                        
                        if ret <= 0:
                            return AfaFlowControl.ExitThisFlow("S999", "更新原汇票查询交易查询查复标识为未查复异常")
                        
                        AfaLoggerFunc.tradeInfo(">>>结束修改原汇票查询交易查询查复标识为未查复")
                    
                else:
                    #======汇票查询查复登记簿中未找到原交易信息,开始查询支付业务状态查询查复登记簿====
                    AfaLoggerFunc.tradeInfo(">>>汇票查询查复登记簿中未找到原交易信息,开始查询支付业务状态查询查复登记簿")
                    
                    bka_dict = rccpsDBTrcc_ztcbka.selectu(bka_where_dict)
                    
                    if bka_dict == None:
                        return AfaFlowControl.ExitThisFlow("S999", "查询业务状态查询业务登记簿异常")
                        
                    if len(bka_dict) > 0:
                        #======业务状态查询查复登记簿中找到原交易信息,开始更新回执信息====
                        AfaLoggerFunc.tradeInfo(">>>业务状态查询查复登记簿中找到原交易信息,开始更新回执信息")
                        
                        ret = rccpsDBTrcc_ztcbka.updateCmt(bka_update_dict,bka_where_dict)
                        
                        if ret <= 0:
                            return AfaFlowControl.ExitThisFlow("S999", "更新回执信息异常")
                            
                        AfaLoggerFunc.tradeInfo(">>>结束更新回执信息")
                        
                        if bka_dict['TRCCO'] == '9900507' and TradeContext.PRCCO != 'RCCI0000':
                            #======支付业务状态查复业务,中心返回码非成功,修改原查询交易查询查复标识为未查复==
                            AfaLoggerFunc.tradeInfo(">>>支付业务状态查复业务,中心返回码非成功")
                            AfaLoggerFunc.tradeInfo(">>>开始修改原支付业务状态查询交易查询查复标识为未查复")
                            
                            bka_update_dict = {'ISDEAL':PL_ISDEAL_UNDO}
                            bka_where_dict = {'BJEDTE':bka_dict['BOJEDT'],'BSPSQN':bka_dict['BOSPSQ']}
                            
                            ret = rccpsDBTrcc_hpcbka.updateCmt(bka_update_dict,bka_where_dict)
                            
                            if ret <= 0:
                                return AfaFlowControl.ExitThisFlow("S999", "更新原支付业务状态查询交易查询查复标识为未查复异常")
                            
                            AfaLoggerFunc.tradeInfo(">>>结束修改原支付业务状态查询交易查询查复标识为未查复")
                        
                    else:
                        #==支付业务状态查询查复登记簿中未找到原交易信息,开始查询撤销申请登记簿==
                        AfaLoggerFunc.tradeInfo(">>>支付业务状态查询查复登记簿中未找到原交易信息,开始查询撤销申请登记簿")
                        
                        bka_dict = rccpsDBTrcc_trccan.selectu(bka_where_dict)
                        
                        if bka_dict == None:
                            return AfaFlowControl.ExitThisFlow("S999", "查询资金调拨申请登记簿异常")
                            
                        if len(bka_dict) > 0:
                            #==撤销申请登记簿中找到原交易信息,开始更新回执信息=========
                            AfaLoggerFunc.tradeInfo(">>>撤销申请登记簿中找到原交易信息,开始更新回执信息")
                            
                            ret = rccpsDBTrcc_trccan.updateCmt(bka_update_dict,bka_where_dict)
                            
                            if ret <= 0:
                                return AfaFlowControl.ExitThisFlow("S999","更新回执信息异常")
                                
                            AfaLoggerFunc.tradeInfo(">>>结束更新回执信息")
                        else:
                            #==撤销申请登记簿中未找到原交易信息,开始查询紧急止付登记簿==
                            AfaLoggerFunc.tradeInfo(">>>支付业务状态查询查复登记簿中未找到原交易信息,开始查询紧急止付登记簿")
                            
                            bka_dict = rccpsDBTrcc_existp.selectu(bka_where_dict)
                            
                            if bka_dict == None:
                                return AfaFlowControl.ExitThisFlow("S999", "查询紧急止付登记簿异常")
                                
                            if len(bka_dict) > 0:
                                #==紧急止付登记簿中找到原交易信息,开始更新回执信息===========
                                AfaLoggerFunc.tradeInfo(">>>紧急止付登记簿中找到原交易信息,开始更新回执信息")
                                
                                ret = rccpsDBTrcc_existp.updateCmt(bka_update_dict,bka_where_dict)
                                
                                if ret <= 0:
                                    return AfaFlowControl.ExitThisFlow("S999","更新回执信息异常")
                                    
                                AfaLoggerFunc.tradeInfo(">>>结束更新回执信息")
                            else:
                                #==紧急止付登记簿中未找到原交易信息,开始查询资金调拨申请登记簿==
                                AfaLoggerFunc.tradeInfo(">>>紧急止付登记簿中未找到原交易信息,开始查询资金调拨申请登记簿")
                                
                                bka_dict = rccpsDBTrcc_mrqtbl.selectu(bka_where_dict)
                                
                                if bka_dict == None:
                                    return AfaFlowControl.ExitThisFlow("S999", "查询资金调拨申请登记簿异常")
                                    
                                if len(bka_dict) > 0:
                                    #==资金调拨申请登记簿中找到原交易信息,开始更新回执信息=========
                                    AfaLoggerFunc.tradeInfo(">>>资金调拨申请登记簿中找到原交易信息,开始更新回执信息")
                                    
                                    ret = rccpsDBTrcc_mrqtbl.updateCmt(bka_update_dict,bka_where_dict)
                                    
                                    if ret <= 0:
                                        return AfaFlowControl.ExitThisFlow("S999","更新回执信息异常")
                                        
                                    AfaLoggerFunc.tradeInfo(">>>结束更新回执信息")
                                else:
                                    #==资金调拨申请登记簿中未找到原交易信息,开始查询清算账户余额通知登记簿==
                                    AfaLoggerFunc.tradeInfo(">>>资金调拨申请登记簿中未找到原交易信息,开始查询清算账户余额通知登记簿")
                                    
                                    bka_dict = rccpsDBTrcc_rekbal.selectu(bka_where_dict)
                                    
                                    if bka_dict == None:
                                        return AfaFlowControl.ExitThisFlow("S999", "查询清算账户余额通知登记簿异常")
                                    
                                    if len(bka_dict) > 0:
                                        #==清算账户余额通知登记簿中找到原交易信息,开始更新回执信息==
                                        AfaLoggerFunc.tradeInfo(">>清算账户余额通知登记簿中找到原交易信息,开始更新回执信息")
                                        
                                        ret = rccpsDBTrcc_rekbal.updateCmt(bka_update_dict,bka_where_dict)
                                        
                                        if ret <= 0:
                                            return AfaFlowControl.ExitThisFlow("S999","更新回执信息异常")
                                            
                                        AfaLoggerFunc.tradeInfo(">>>结束更新回执信息")
                                        
                                    else:
                                        #==未找到原交易信息,丢弃报文===========  
                                        return AfaFlowControl.ExitThisFlow("S999", "未找到原交易信息,丢弃报文")
    
    else:
        #==========原业务类型非法==============================================
        return AfaFlowControl.ExitThisFlow("S999", "原业务类型[" + TradeContext.ROPRTPNO + "]非法")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
    AfaLoggerFunc.tradeInfo(">>>Commit成功")
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.回执类操作(1.回执操作).通讯回执报文接收[TRC004_1111]退出***' )
    return True
