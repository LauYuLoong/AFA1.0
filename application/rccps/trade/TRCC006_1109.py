# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.中心类操作(1.本地操作 2.中心回执).清算回执报文接收
#===============================================================================
#   交易文件:   TRCC004_1109.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,time
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsHostFunc,rccpsDBTrcc_bilinf,rccpsEntries
import rccpsMap0000Dout_context2CTradeContext


#=====================回执个性化处理(本地操作)==================================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(1.本地操作).清算回执报文接收[TRCC006_1109]进入***' )
    #=================初始化返回信息============================================
    if AfaUtilTools.trim(TradeContext.STRINFO) == "":
        TradeContext.STRINFO = rccpsDBFunc.getErrInfo(TradeContext.PRCCO)
    
    AfaLoggerFunc.tradeDebug("TradeContext.STRINFO=" + TradeContext.STRINFO)
    
    #==========检查业务类型====================================================
    if TradeContext.ROPRTPNO == "20":
        AfaLoggerFunc.tradeInfo(">>>原业务类型为20,汇兑业务")

        #==========根据发送行号,委托日期,交易流水号查询原交易信息==============
        AfaLoggerFunc.tradeError(">>>开始根据发送行号,委托日期,交易流水号查询交易信息")
        ORSNDMBRCO = TradeContext.ORMFN[:10]
        ORTRCDAT   = TradeContext.ORMFN[10:18]
        ORTRCNO    = TradeContext.ORMFN[18:]

        trc_dict = {}
        if not rccpsDBFunc.getTransTrcPK(ORSNDMBRCO,ORTRCDAT,ORTRCNO,trc_dict):
            return False
        
        AfaLoggerFunc.tradeError(">>>结束根据发送行号,委托日期,交易流水号查询交易信息")

        #==========检查原业务是否MFE收妥=======================================
        tmp_stat_dict = {}
        if not rccpsState.getTransStateSet(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_MFERCV,PL_BDWFLG_SUCC,tmp_stat_dict):
            return AfaFlowControl.ExitThisFlow("S999","原汇兑业务MFE尚未收妥,停止处理")
        
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
            #==========中心返回表示成功的处理码,开始设置状态为清算=============
            AfaLoggerFunc.tradeInfo(">>>开始设置状态为清算")
            
            if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_MFESTL,PL_BDWFLG_WAIT):
                return False
                
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit异常")
            AfaLoggerFunc.tradeInfo(">>>Commit成功")
            
            stat_dict['BCSTAT']  = PL_BCSTAT_MFESTL
            stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
            
            if not rccpsState.setTransState(stat_dict):
                return False
                
            AfaLoggerFunc.tradeInfo(">>>结束设置状态为清算")
            
            #==========若此交易为退汇,设置原交易为退汇状态=====================
            if trc_dict['TRCCO'] == '2000004':
                AfaLoggerFunc.tradeInfo(">>>退汇交易,开始设置原交易为退汇状态")
                
                if not rccpsState.newTransState(trc_dict['BOJEDT'],trc_dict['BOSPSQ'],PL_BCSTAT_QTR,PL_BDWFLG_WAIT):
                    return False
                
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    return AfaFlowControl.ExitThisFlow("S999","Commit异常")
                AfaLoggerFunc.tradeInfo(">>>Commit成功")
                
                th_stat_dict = {}
                th_stat_dict['BJEDTE'] = trc_dict['BOJEDT']
                th_stat_dict['BSPSQN'] = trc_dict['BOSPSQ']
                th_stat_dict['BESBNO'] = trc_dict['BESBNO']
                th_stat_dict['BETELR'] = trc_dict['BETELR']
                th_stat_dict['BCSTAT'] = PL_BCSTAT_QTR
                th_stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
                
                if not rccpsState.setTransState(th_stat_dict):
                    return False
                    
                AfaLoggerFunc.tradeInfo(">>>退汇交易,结束设置原交易为退汇状态")
            
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
            
            #==========设置当前机构为原机构====================================
            TradeContext.BESBNO = trc_dict['BESBNO']
            TradeContext.BETELR = trc_dict['BETELR']
            TradeContext.TERMID = '9999999999'
            
            #==========设置原交易状态为抹账处理中==============================
            AfaLoggerFunc.tradeInfo(">>>开始设置状态为抹账处理中")
            
            TradeContext.NOTE3 = "中心拒绝,行内自动抹账"
            
            if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_HCAC,PL_BDWFLG_WAIT):
                return False
            
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit异常")
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
            
            #=====设置记账函数接口====
            rccpsHostFunc.CommHost( TradeContext.HostCode )
            
            AfaLoggerFunc.tradeInfo(">>>结束主机抹账")
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
        AfaLoggerFunc.tradeInfo(">>>原业务类型为21,汇票业务")
        
        #==========根据发送行号,委托日期,交易流水号查询原交易信息==============
        AfaLoggerFunc.tradeError(">>>开始根据发送行号,委托日期,交易流水号查询交易信息及汇票信息")
        ORSNDMBRCO = TradeContext.ORMFN[:10]
        ORTRCDAT   = TradeContext.ORMFN[10:18]
        ORTRCNO    = TradeContext.ORMFN[18:]
    
        trc_dict = {}
        if not rccpsDBFunc.getTransBilPK(ORSNDMBRCO,ORTRCDAT,ORTRCNO,trc_dict):
            return False
            
        if not rccpsDBFunc.getInfoBil(trc_dict['BILVER'],trc_dict['BILNO'],trc_dict['BILRS'],trc_dict):
            return False

        AfaLoggerFunc.tradeInfo('trc_dict=' + str(trc_dict))
        
        TradeContext.ORTRCCO = trc_dict['TRCCO']
        TradeContext.BJEDTE  = trc_dict['BJEDTE']
        TradeContext.BSPSQN  = trc_dict['BSPSQN']
        
        AfaLoggerFunc.tradeError(">>>结束根据发送行号,委托日期,交易流水号查询交易信息及汇票信息")

        #==========检查原业务是否MFE收妥=======================================
        tmp_stat_dict = {}
        if not rccpsState.getTransStateSet(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_MFERCV,PL_BDWFLG_SUCC,tmp_stat_dict):
            return AfaFlowControl.ExitThisFlow("S999","原汇票业务MFE尚未收妥,停止处理")
        
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
            
            #===========原交易代码=============================================
            AfaLoggerFunc.tradeInfo("TradeContext.ORTRCCO=[" + TradeContext.ORTRCCO + "]")
            
            #===========如果原交易代码为汇票签发,设置汇票状态为签发============
            if TradeContext.ORTRCCO == '2100001':
                AfaLoggerFunc.tradeInfo(">>>原交易代码为签发")
                
                #=======新增业务状态为清算处理中=============================
                AfaLoggerFunc.tradeInfo(">>>开始设置原交易状态为清算处理中")
                
                if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_MFESTL,PL_BDWFLG_WAIT):
                    return AfaFlowControl.ExitThisFlow("S999","设置业务状态为清算处理中异常")
                
                AfaLoggerFunc.tradeInfo(">>>结束设置原交易状态为清算处理中")
                
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    return AfaFlowControl.ExitThisFlow("S999","Commit异常")
                AfaLoggerFunc.tradeInfo(">>>Commit成功")
                
                #=======设置汇票状态为签发=====================================
                AfaLoggerFunc.tradeInfo(">>>开始设置汇票状态为签发")
                
                if not rccpsState.newBilState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_HPSTAT_SIGN):
                    return AfaFlowControl.ExitThisFlow("S999","设置汇票状态异常")
                
                AfaLoggerFunc.tradeInfo(">>>结束设置汇票状态为签发")
                
                #==========设置原交易状态为清算成功
                AfaLoggerFunc.tradeInfo(">>>开始设置状态为清算成功")
                
                stat_dict['BCSTAT'] = PL_BCSTAT_MFESTL
                stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
                stat_dict['PRCCO']  = TradeContext.PRCCO
                stat_dict['STRINFO']= TradeContext.STRINFO
                
                if not rccpsState.setTransState(stat_dict):
                    return False
                
                AfaLoggerFunc.tradeInfo(">>>结束设置状态为清算成功")
                
            #===========如果原交易代码为汇票解付,发起主机记账,成功后设置汇票状态为解付
            elif TradeContext.ORTRCCO == '2100100':
                #=======原交易代码为汇票解付===================================
                AfaLoggerFunc.tradeInfo(">>>原交易代码为解付")
                #===========设置原交易业务状态为记账处理中=====================
                AfaLoggerFunc.tradeInfo(">>>开始设置原交易状态为主机记账处理中")
                
                if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_ACC,PL_BDWFLG_WAIT):
                    return AfaFlowControl.ExitThisFlow("S999","设置原交易状态为主机记账处理中异常")
                
                AfaLoggerFunc.tradeInfo(">>>结束设置原交易状态为主机记账处理中")
                
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    return AfaFlowControl.ExitThisFlow("S999","Commit异常")
                AfaLoggerFunc.tradeInfo(">>>Commit成功")
                
                #===========主机记账初始化=====================================
                AfaLoggerFunc.tradeInfo(">>>开始主机记账初始化")
                
                TradeContext.BESBNO   = trc_dict['BESBNO']
                TradeContext.BETELR   = trc_dict['BETELR']
                TradeContext.TERMID   = trc_dict['TERMID']
                TradeContext.BEAUUS   = trc_dict['BEAUUS']
                TradeContext.BEAUPS   = trc_dict['BEAUPS']
                
                TradeContext.HostCode = '8813'
                TradeContext.RCCSMCD  = PL_RCCSMCD_HPJF                        #主机摘要码:汇票解付
                TradeContext.OCCAMT   = str(trc_dict['OCCAMT'])
                TradeContext.SBAC     = TradeContext.BESBNO + PL_ACC_NXYDQSWZ  #借农信银待清算往账
                TradeContext.ACNM     = "农信银待清算往账"
                TradeContext.RBAC     = trc_dict['PYHACC']                     #贷持票人账号
                TradeContext.OTNM     = trc_dict['PYHNAM']                   
                TradeContext.REAC     = TradeContext.BESBNO + PL_ACC_NXYDXZ    #挂账账户
                
                #=====开始调函数拼贷方账号第25位校验位====
                TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
                TradeContext.REAC = rccpsHostFunc.CrtAcc(TradeContext.REAC, 25)
                
                AfaLoggerFunc.tradeInfo( '借方账号:' + TradeContext.SBAC )
                AfaLoggerFunc.tradeInfo( '贷方账号:' + TradeContext.RBAC )
                AfaLoggerFunc.tradeInfo( '挂账账号:' + TradeContext.REAC )
                
                AfaLoggerFunc.tradeInfo(">>>结束主机记账初始化")
                #===========发起主机记账=======================================
                AfaLoggerFunc.tradeInfo(">>>开始发起主机记账")
                
                rccpsHostFunc.CommHost( TradeContext.HostCode )
                
                AfaLoggerFunc.tradeInfo(">>>结束发起主机记账")
                
                if TradeContext.errorCode == '0000':
                    #=======设置原业务状态为记账成功===========================
                    AfaLoggerFunc.tradeInfo(">>>开始设置原交易状态为主机记账成功")
                    
                    stat_dict = {}
                    stat_dict['BJEDTE'] = TradeContext.BJEDTE
                    stat_dict['BSPSQN'] = TradeContext.BSPSQN
                    stat_dict['BESBNO'] = TradeContext.BESBNO              #机构号
                    stat_dict['BETELR'] = TradeContext.BETELR              #柜员号
                    stat_dict['TERMID'] = TradeContext.TERMID              #终端号
                    stat_dict['BCSTAT'] = PL_BCSTAT_ACC                    #流水状态
                    stat_dict['BDWFLG'] = PL_BDWFLG_SUCC                   #流转处理标识
                    if TradeContext.existVariable('TRDT'):
                        stat_dict['TRDT']   = TradeContext.TRDT            #主机日期
                    if TradeContext.existVariable('TLSQ'):
                        stat_dict['TLSQ']   = TradeContext.TLSQ            #主机流水
                    if TradeContext.existVariable('DASQ'):
                        stat_dict['DASQ']   = TradeContext.DASQ            #代销账序号
                    stat_dict['SBAC']   = TradeContext.SBAC                #借方账号
                    stat_dict['RBAC']   = TradeContext.RBAC                #贷方账号
                    stat_dict['MGID']   = TradeContext.errorCode           #主机错误码
                    stat_dict['STRINFO']= TradeContext.errorMsg            #主机错误信息
                    stat_dict['PRTCNT']  = 1
                    
                    if not rccpsState.setTransState(stat_dict):
                        return False
                    
                    AfaLoggerFunc.tradeInfo(">>>结束设置原交易状态为主机记账成功")
                    
                    if not AfaDBFunc.CommitSql( ):
                        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
                    AfaLoggerFunc.tradeInfo(">>>Commit成功")
                    
                    #=======新增业务状态为清算处理中=============================
                    AfaLoggerFunc.tradeInfo(">>>开始设置原交易状态为清算处理中")
                    
                    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_MFESTL,PL_BDWFLG_WAIT):
                        return AfaFlowControl.ExitThisFlow("S999","设置业务状态为清算处理中异常")
                    
                    AfaLoggerFunc.tradeInfo(">>>结束设置原交易状态为清算处理中")
                    
                    if not AfaDBFunc.CommitSql( ):
                        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
                    AfaLoggerFunc.tradeInfo(">>>Commit成功")
                    
                    #=======设置汇票状态为解付=================================
                    AfaLoggerFunc.tradeInfo(">>>开始设置汇票状态为解付")
                    
                    if not rccpsState.newBilState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_HPSTAT_PAYC):
                        return AfaFlowControl.ExitThisFlow("S999","设置汇票状态异常")
                    
                    AfaLoggerFunc.tradeInfo(">>>结束设置汇票状态为解付")
                    
                    #=======设置原业务状态为清算成功===========================
                    AfaLoggerFunc.tradeInfo(">>>开始设置原交易状态为清算成功")
                    
                    #stat_dict = {}
                    #stat_dict['BJEDTE']  = TradeContext.BJEDTE
                    #stat_dict['BSPSQN']  = TradeContext.BSPSQN
                    #stat_dict['BESBNO']  = TradeContext.BESBNO              #机构号
                    #stat_dict['BETELR']  = TradeContext.BETELR              #柜员号
                    #stat_dict['TERMID']  = TradeContext.TERMID              #终端号
                    stat_dict['BCSTAT']  = PL_BCSTAT_MFESTL                 #流水状态
                    stat_dict['BDWFLG']  = PL_BDWFLG_SUCC                   #流转处理标识
                    stat_dict['PRCCO']   = TradeContext.PRCCO               #中心返回码
                    stat_dict['STRINFO'] = TradeContext.STRINFO             #中心返回信息
                    
                    if not rccpsState.setTransState(stat_dict):
                        return False
                    
                    AfaLoggerFunc.tradeInfo(">>>结束设置原交易状态为清算成功")
                    
                else:
                    #=======设置原业务状态为记账失败=====================
                    AfaLoggerFunc.tradeInfo(">>>开始设置原交易状态为主机记账失败")
                    
                    #stat_dict = {}
                    #stat_dict['BJEDTE'] = TradeContext.BJEDTE
                    #stat_dict['BSPSQN'] = tradeContext.BSPSQN
                    #stat_dict['BESBNO'] = TradeContext.BESBNO              #机构号                         
                    #stat_dict['BETELR'] = TradeContext.BETELR              #柜员号        
                    #stat_dict['TERMID'] = TradeContext.TERMID              #终端号         
                    stat_dict['BCSTAT'] = PL_BCSTAT_ACC                    #流水状态         
                    stat_dict['BDWFLG'] = PL_BDWFLG_FAIL                   #流转处理标识     
                    if TradeContext.existVariable('TRDT'):                                 
                        stat_dict['TRDT']   = TradeContext.TRDT            #主机日期     
                    if TradeContext.existVariable('TRDT'):                                 
                        stat_dict['TLSQ']   = TradeContext.TLSQ            #主机流水     
                    if TradeContext.existVariable('DASQ'):                                
                        stat_dict['DASQ']   = TradeContext.DASQ            #代销账序号     
                    stat_dict['MGID']   = TradeContext.errorCode           #主机错误码    
                    stat_dict['STRINFO']= TradeContext.errorMsg            #主机错误信息
                    
                    if not rccpsState.setTransState(stat_dict):
                        return False
                    
                    AfaLoggerFunc.tradeInfo(">>>结束设置原交易状态为主机记账失败")
                    
            #===========如果原交易代码为汇票撤销,发起主机抹账,成功后设置汇票状态为撤销
            if TradeContext.ORTRCCO == '2100101':
                AfaLoggerFunc.tradeInfo(">>>原交易代码撤销")
                
                #=======设置原交易状态为抹账处理中=============================
                AfaLoggerFunc.tradeInfo(">>>开始设置原交易状态为主机抹账处理中")
                
                if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_HCAC,PL_BDWFLG_WAIT):
                    return AfaFlowControl.ExitThisFlow("S999","设置原交易状态为主机抹账处理中异常")
                
                AfaLoggerFunc.tradeInfo(">>>结束设置原交易状态为主机抹账处理中")
                
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    return AfaFlowControl.ExitThisFlow("S999","Commit异常")
                AfaLoggerFunc.tradeInfo(">>>Commit成功")
                
                #=======主机抹账初始化=========================================
                AfaLoggerFunc.tradeInfo(">>>开始主机抹账初始化")
                
                TradeContext.BESBNO   = trc_dict['BESBNO']
                TradeContext.BETELR   = trc_dict['BETELR']
                TradeContext.TERMID   = trc_dict['TERMID']
                TradeContext.BEAUUS   = trc_dict['BEAUUS']
                TradeContext.BEAUPS   = trc_dict['BEAUPS']
                
                #=====如果资金来源为待销账，使用8813红字冲销====
                if trc_dict['BBSSRC'] == '3':                                              #待销账
                    TradeContext.BJEDTE   = trc_dict['BJEDTE']                              #trc_dict[NOTE1]为签发交易的报单日期
                    TradeContext.BSPSQN   = trc_dict['BSPSQN']                              #trc_dict[NOTE2]为签发交易的报单序号
                    TradeContext.OCCAMT   = str(trc_dict['BILAMT'])                        #抹账金额为出票金额
                    TradeContext.HostCode = '8813'
                    TradeContext.RCCSMCD  = PL_RCCSMCD_HPCX                                #主机摘要码:汇票撤销
                    TradeContext.DASQ     = ''
                    TradeContext.RVFG     = '0'                                            #红蓝字标志 0
                    TradeContext.SBAC     =  TradeContext.BESBNO  +  PL_ACC_HCHK           #借方账号(汇票撤销,借汇出汇款)
                    TradeContext.RBAC     =  TradeContext.BESBNO  +  PL_ACC_NXYDXZ         #贷方账号(贷农信银待销账)
                    #=====开始调函数拼贷方账号第25位校验位====
                    TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
                    TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC, 25)
                    AfaLoggerFunc.tradeInfo( '借方账号:' + TradeContext.SBAC )
                    AfaLoggerFunc.tradeInfo( '贷方账号:' + TradeContext.RBAC )
                else:
                    #TradeContext.BOJEDT  = trc_dict['NOTE1']                               #trc_dict[NOTE1]为签发交易的报单日期
                    #TradeContext.BOSPSQ  = trc_dict['NOTE2']                               #trc_dict[NOTE2]为签发交易的报单序号
                    #TradeContext.HostCode='8820'
                    
                    #关彬捷 20080922 撤销,非待销账,用8813记红字账
                    TradeContext.BJEDTE   = trc_dict['BJEDTE']                             #报单日期
                    TradeContext.BSPSQN   = trc_dict['BSPSQN']                             #报单序号
                    TradeContext.OCCAMT   = "-" + str(trc_dict['BILAMT'])                  #抹账金额为出票金额
                    TradeContext.HostCode = '8813'
                    TradeContext.DASQ     = ''
                    TradeContext.SBAC     = trc_dict['PYRACC']                             #借方账号(汇票撤销,借客户账(红字))
                    TradeContext.ACNM     = trc_dict['PYRNAM']                             #借方户名(汇票撤销,借客户账(红字))
                    TradeContext.RBAC     = TradeContext.BESBNO  +  PL_ACC_HCHK            #贷方账号(贷汇出汇款(红字))
                    TradeContext.OTNM     = "汇出汇款"                                     #贷方户名(贷汇出汇款(红字))
                    #=====开始调函数拼贷方账号第25位校验位====
                    TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC, 25)
                    
                    AfaLoggerFunc.tradeInfo( '借方账号:' + TradeContext.SBAC )
                    AfaLoggerFunc.tradeInfo( '贷方账号:' + TradeContext.RBAC )
                
                AfaLoggerFunc.tradeInfo(">>>结束主机抹账初始化")
                
                #=======发起主机抹账===========================================
                rccpsHostFunc.CommHost( TradeContext.HostCode )
                
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
                    stat_dict['PRTCNT']  = 1
                    
                    if not rccpsState.setTransState(stat_dict):
                        return False
                    
                    AfaLoggerFunc.tradeInfo(">>>结束设置状态为抹账成功")
                    
                    if not AfaDBFunc.CommitSql( ):
                        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
                    AfaLoggerFunc.tradeInfo(">>>Commit成功")
                    
                    #==========设置原交易状态为清算处理中======================
                    AfaLoggerFunc.tradeInfo(">>>开始设置原交易状态为清算处理中")
                    
                    if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_MFESTL,PL_BDWFLG_WAIT):
                        return AfaFlowControl.ExitThisFlow("S999","设置原交易状态为主机清算处理中异常")
                    
                    AfaLoggerFunc.tradeInfo(">>>结束设置原交易状态为清算处理中")
                    
                    
                    
                    #=======设置汇票状态为撤销=====================================
                    AfaLoggerFunc.tradeInfo(">>>开始设置汇票状态为撤销")
                        
                    if not rccpsState.newBilState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_HPSTAT_CANC):
                        return AfaFlowControl.ExitThisFlow("S999","设置汇票状态异常")
                    
                    AfaLoggerFunc.tradeInfo(">>>结束设置汇票状态为撤销")
                    
                    #==========设置原交易状态为清算成功
                    AfaLoggerFunc.tradeInfo(">>>开始设置状态为清算成功")
                    
                    stat_dict['BCSTAT'] = PL_BCSTAT_MFESTL
                    stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
                    stat_dict['PRCCO']  = TradeContext.PRCCO
                    stat_dict['STRINFO']= TradeContext.STRINFO
                    
                    if not rccpsState.setTransState(stat_dict):
                        return False
                    
                    AfaLoggerFunc.tradeInfo(">>>结束设置状态为清算成功")
                    
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
                
            #===========如果原交易代码为汇票挂失,设置汇票状态为挂失
            if TradeContext.ORTRCCO == '2100102':
                AfaLoggerFunc.tradeInfo(">>>原交易代码为挂失")
                
                #==========设置原交易状态为清算处理中======================
                AfaLoggerFunc.tradeInfo(">>>开始设置原交易状态为清算处理中")
                
                if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_MFESTL,PL_BDWFLG_WAIT):
                    return AfaFlowControl.ExitThisFlow("S999","设置原交易状态为主机清算处理中异常")
                
                AfaLoggerFunc.tradeInfo(">>>结束设置原交易状态为清算处理中")
                
                #COMMIT
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    return AfaFlowControl.ExitThisFlow("S999","Commit异常")
                AfaLoggerFunc.tradeInfo(">>>Commit成功")
                
                #=======设置汇票状态为挂失=====================================
                AfaLoggerFunc.tradeInfo(">>>开始设置汇票状态为挂失")
                    
                if not rccpsState.newBilState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_HPSTAT_HANG):
                    return AfaFlowControl.ExitThisFlow("S999","设置汇票状态异常")
                
                AfaLoggerFunc.tradeInfo(">>>结束设置汇票状态为挂失")
                
                #==========设置原交易状态为清算成功============================
                AfaLoggerFunc.tradeInfo(">>>开始设置状态为清算成功")
                
                stat_dict['BCSTAT'] = PL_BCSTAT_MFESTL
                stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
                stat_dict['PRCCO']  = TradeContext.PRCCO
                stat_dict['STRINFO']= TradeContext.STRINFO
                
                if not rccpsState.setTransState(stat_dict):
                    return False
                
                AfaLoggerFunc.tradeInfo(">>>结束设置状态为清算成功")
                
            #===========如果原交易代码为退票,设置汇票状态为退票================
            if TradeContext.ORTRCCO == '2100103':
                AfaLoggerFunc.tradeInfo(">>>原交易代码为退票")
                
                #=======设置原交易状态为记账处理中=============================
                AfaLoggerFunc.tradeInfo(">>>开始设置原交易状态为记账处理中")
                
                if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_ACC,PL_BDWFLG_WAIT):
                    return AfaFlowControl.ExitThisFlow("S999","设置原交易状态为主机记账处理中异常")
                
                AfaLoggerFunc.tradeInfo(">>>结束设置原交易状态为记账处理中")
                
                #COMMIT
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    return AfaFlowControl.ExitThisFlow("S999","Commit异常")
                AfaLoggerFunc.tradeInfo(">>>Commit成功")
                
                #=======主机记账初始化=========================================
                AfaLoggerFunc.tradeInfo(">>>开始主机记账初始化")
                
                TradeContext.BESBNO   = trc_dict['BESBNO']
                TradeContext.BETELR   = trc_dict['BETELR']
                TradeContext.TERMID   = trc_dict['TERMID']
                TradeContext.BEAUUS   = trc_dict['BEAUUS']
                TradeContext.BEAUPS   = trc_dict['BEAUPS']
                
                TradeContext.HostCode = '8813'
                TradeContext.RCCSMCD  = PL_RCCSMCD_HPTK                        #主机摘要码:汇票退票
                TradeContext.OCCAMT   = str(trc_dict['OCCAMT'])
                TradeContext.SBAC     = TradeContext.BESBNO + PL_ACC_HCHK      #借汇出汇款
                TradeContext.ACNM     = "汇出汇款"
                TradeContext.RBAC     = trc_dict['PYIACC']                     #贷退票入账账号
                TradeContext.OTNM     = trc_dict['PYINAM']
                TradeContext.REAC     = TradeContext.BESBNO + PL_ACC_NXYDXZ    #挂账账户
                
                #=====开始调函数拼贷方账号第25位校验位====
                TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
                TradeContext.REAC = rccpsHostFunc.CrtAcc(TradeContext.REAC, 25)
                
                AfaLoggerFunc.tradeInfo( '借方账号1:' + TradeContext.SBAC )
                AfaLoggerFunc.tradeInfo( '贷方账号1:' + TradeContext.RBAC )
                AfaLoggerFunc.tradeInfo( '挂账账号1:' + TradeContext.REAC )
                
                AfaLoggerFunc.tradeInfo(">>>开始判断是否存在多余款操作")
                #=====判断记账次数====
                AfaLoggerFunc.tradeInfo("trc_dict['RMNAMT']=" + str(trc_dict['RMNAMT']))
                if float(trc_dict['RMNAMT']) > 0.001:
                    AfaLoggerFunc.tradeInfo(">>>第二次记账赋值操作")
                    
                    TradeContext.ACUR   = '2'   #记账循环次数
                    TradeContext.TRFG   = '9'   #凭证处理标识'
                    TradeContext.I2CETY = ''    #凭证种类
                    TradeContext.I2SMCD = PL_RCCSMCD_HPTK                      #主机摘要码:汇票退款
                    TradeContext.I2TRAM = str(trc_dict['RMNAMT'])              #结余金额
                    TradeContext.I2SBAC = TradeContext.BESBNO + PL_ACC_HCHK    #借汇出汇款
                    TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_DYKJQ   #贷农信银多余款
                    TradeContext.I2REAC = TradeContext.BESBNO + PL_ACC_NXYDXZ  #挂账账号
                    
                    #=====生成账号校验位====
                    TradeContext.I2SBAC = rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
                    TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
                    TradeContext.I2REAC = rccpsHostFunc.CrtAcc(TradeContext.I2REAC,25)
                    
                    AfaLoggerFunc.tradeInfo( '借方账号2:' + TradeContext.I2SBAC )
                    AfaLoggerFunc.tradeInfo( '贷方账号2:' + TradeContext.I2RBAC )
                    AfaLoggerFunc.tradeInfo( '挂账账号2:' + TradeContext.I2REAC )
                    
                AfaLoggerFunc.tradeInfo(">>>结束判断是否存在多余款操作")
                
                AfaLoggerFunc.tradeInfo(">>>结束主机记账初始化")
                
                #=======发起主机记账===========================================
                AfaLoggerFunc.tradeInfo(">>>开始发起主机记账")
                
                rccpsHostFunc.CommHost( TradeContext.HostCode )
                
                AfaLoggerFunc.tradeInfo(">>>开始发起主机记账")
                
                if TradeContext.errorCode == '0000':
                    #===主机记账成功,设置原交易状态为记账成功==================
                    AfaLoggerFunc.tradeInfo(">>>主机记账成功")
                    AfaLoggerFunc.tradeInfo(">>>开始设置原交易状态为记账成功")
                    
                    stat_dict['BCSTAT'] = PL_BCSTAT_ACC
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
                    stat_dict['PRTCNT']  = 1
                    
                    if not rccpsState.setTransState(stat_dict):
                        return False
                    
                    AfaLoggerFunc.tradeInfo(">>>结束设置原交易状态为记账成功")
                    
                    #COMMIT
                    if not AfaDBFunc.CommitSql( ):
                        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
                    AfaLoggerFunc.tradeInfo(">>>Commit成功")
                    
                    #=======设置汇票业务状态为清算处理中=======================
                    AfaLoggerFunc.tradeInfo(">>>开始设置原交易状态为清算处理中")
                    
                    if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_MFESTL,PL_BDWFLG_WAIT):
                        return AfaFlowControl.ExitThisFlow("S999","设置原交易状态为清算处理中异常")
                    
                    AfaLoggerFunc.tradeInfo(">>>结束设置原交易状态为清算处理中")
                    
                    #COMMIT
                    if not AfaDBFunc.CommitSql( ):
                        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
                    AfaLoggerFunc.tradeInfo(">>>Commit成功")
                    
                    #=======设置汇票状态为退票=====================================
                    AfaLoggerFunc.tradeInfo(">>>开始设置汇票状态为退票")
                    
                    if not rccpsState.newBilState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_HPSTAT_RETN):
                        return AfaFlowControl.ExitThisFlow("S999","设置汇票状态异常")
                    
                    AfaLoggerFunc.tradeInfo(">>>结束设置汇票状态为退票")
                    
                    #=======设置汇票业务状态为清算成功=========================
                    AfaLoggerFunc.tradeInfo(">>>开始设置原交易状态为清算成功")
                    
                    stat_dict['BCSTAT'] = PL_BCSTAT_MFESTL
                    stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
                    stat_dict['PRCCO']  = TradeContext.PRCCO
                    stat_dict['STRINFO']= TradeContext.STRINFO
                    
                    if not rccpsState.setTransState(stat_dict):
                        return False
                    
                    AfaLoggerFunc.tradeInfo(">>>结束设置原交易状态为清算成功")
                
                else:
                    #===主机记账失败,设置原交易状态为记账失败==================
                    AfaLoggerFunc.tradeInfo(">>>主机记账失败")
                    AfaLoggerFunc.tradeInfo(">>>开始设置原交易状态为记账失败")
                    
                    stat_dict['BCSTAT'] = PL_BCSTAT_ACC
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
                    
                    AfaLoggerFunc.tradeInfo(">>>结束设置原交易状态为记账失败")
                    
            #===========如果原交易代码为解挂,设置汇票状态为解挂=========
            if TradeContext.ORTRCCO == '2100104':
                AfaLoggerFunc.tradeInfo(">>>原交易代码为解挂")
                
                #==========设置原交易状态为清算处理中======================
                AfaLoggerFunc.tradeInfo(">>>开始设置原交易状态为清算处理中")
                
                if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_MFESTL,PL_BDWFLG_WAIT):
                    return AfaFlowControl.ExitThisFlow("S999","设置原交易状态为主机清算处理中异常")
                
                AfaLoggerFunc.tradeInfo(">>>结束设置原交易状态为清算处理中")
                
                #COMMIT
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    return AfaFlowControl.ExitThisFlow("S999","Commit异常")
                AfaLoggerFunc.tradeInfo(">>>Commit成功")
                
                #=======设置汇票状态为解挂===============================
                AfaLoggerFunc.tradeInfo(">>>开始设置汇票状态为解挂")
                
                if not rccpsState.newBilState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_HPSTAT_DEHG):
                    return AfaFlowControl.ExitThisFlow("S999","设置汇票状态异常")
                
                AfaLoggerFunc.tradeInfo(">>>结束设置汇票状态为解挂")
                
                #==========设置原交易状态为清算成功============================
                AfaLoggerFunc.tradeInfo(">>>开始设置状态为清算成功")
                
                stat_dict['BCSTAT'] = PL_BCSTAT_MFESTL
                stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
                stat_dict['PRCCO']  = TradeContext.PRCCO
                stat_dict['STRINFO']= TradeContext.STRINFO
                
                if not rccpsState.setTransState(stat_dict):
                    return False
                
                AfaLoggerFunc.tradeInfo(">>>结束设置状态为清算成功")
                
        elif TradeContext.PRCCO == "RCCO1078" or TradeContext.PRCCO == "RCCO1079":
            #==========中心返回表示排队的处理码,开始设置状态为排队======
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
            #==========中心返回表示拒绝的处理码,开始设置状态为拒绝======
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
                    stat_dict['PRTCNT']  = 1
                    
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

    else:
        #==========原业务类型非法==============================================
        return AfaFlowControl.ExitThisFlow("S999", "业务类型[" + TradeContext.ROPRTPNO + "]非法")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
    AfaLoggerFunc.tradeInfo(">>>Commit成功")
    
    #================为通讯回执报文赋值========================================
    AfaLoggerFunc.tradeInfo(">>>开始为通讯回执报文赋值")
    
    #======为通讯回执报文赋值==================================================
    out_context_dict = {}
    out_context_dict['sysType']  = 'rccpst'
    out_context_dict['TRCCO']    = '9900503'
    out_context_dict['MSGTYPCO'] = 'SET008'
    out_context_dict['RCVMBRCO'] = TradeContext.SNDMBRCO
    out_context_dict['SNDMBRCO'] = TradeContext.RCVMBRCO
    out_context_dict['SNDBRHCO'] = TradeContext.BESBNO
    out_context_dict['SNDCLKNO'] = TradeContext.BETELR
    out_context_dict['SNDTRDAT'] = TradeContext.BJEDTE
    out_context_dict['SNDTRTIM'] = TradeContext.BJETIM
    out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
    out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
    out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
    out_context_dict['OPRTYPNO'] = '99'
    out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
    out_context_dict['TRANTYP']  = '0'
    out_context_dict['ORTRCCO']  = TradeContext.TRCCO
    out_context_dict['PRCCO']    = 'RCCI0000'
    out_context_dict['STRINFO']  = '成功'
    
    rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
    
    AfaLoggerFunc.tradeInfo(">>>结束为通讯回执报文赋值")
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(1.本地操作).清算回执报文接收[TRCC006_1109]退出***' )
    return True


#=====================交易后处理================================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(2.中心回执).清算回执报文接收[TRCC006_1109]进入***' )
    
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(errorCode,errorMsg)
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(2.中心回执).清算回执报文接收[TRCC006_1109]退出***' )
    return True
