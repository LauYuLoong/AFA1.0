# -*- coding: gbk -*-
###############################################################################
#   农信银系统：往账.回执类操作模板(1.回执操作).通兑_折应答
#==============================================================================
#   交易文件:   TRCC004_1157.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘雨龙
#   修改时间:   2008-11-04
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsDBTrcc_atcbka,rccpsHostFunc

#=====================回执个性化处理(本地操作)=================================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作).个人现金通兑_折应答[TRCC004_1157]进入***' )

    #=================初始化返回信息============================================
    if AfaUtilTools.trim(TradeContext.STRINFO) == "":
        TradeContext.STRINFO = rccpsDBFunc.getErrInfo(TradeContext.PRCCO)
        
    AfaLoggerFunc.tradeDebug("TradeContext.STRINFO=" + TradeContext.STRINFO)

    #=====根据参考报文标识号查找原交易====
    TradeContext.ORSNDBNKCO = TradeContext.ORMFN[:10]                #原发送行号
    TradeContext.BOJEDT     = TradeContext.ORMFN[10:18]              #原交易日期
    TradeContext.ORTRCNO    = TradeContext.ORMFN[18:]                #原交易流水号

    wtr_dict = {}
    if not rccpsDBFunc.getTransWtrAK(TradeContext.ORSNDBNKCO,TradeContext.BOJEDT,TradeContext.ORTRCNO,wtr_dict):
        #=====查询原交易失败，等待前台超时发起冲正，抛弃此报文====       
        return AfaFlowControl.ExitThisFlow('S999','等待前台发起冲正，抛弃报文') 

    AfaLoggerFunc.tradeInfo( '>>>查询原交易结束' )

    #=================若应答报文回复拒绝,则设置状态为拒绝,停止处理=============
    if TradeContext.PRCCO != 'RCCI0000':
        AfaLoggerFunc.tradeInfo(">>>对方返回拒绝应答")
        
        #=============设置业务状态为拒绝处理中=================================
        
        if not rccpsState.newTransState(wtr_dict['BJEDTE'],wtr_dict['BSPSQN'],PL_BCSTAT_MFERFE,PL_BDWFLG_WAIT):
            return AfaFlowControl.ExitThisFlow('S999',"设置业务状态为拒绝成功异常")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit异常")
            
        #=============设置业务状态为拒绝成功===================================
        stat_dict = {}
        stat_dict['BJEDTE']  = wtr_dict['BJEDTE']
        stat_dict['BSPSQN']  = wtr_dict['BSPSQN']
        stat_dict['BCSTAT']  = PL_BCSTAT_MFERFE
        stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
        stat_dict['PRCCO']   = TradeContext.PRCCO
        stat_dict['STRINFO'] = TradeContext.STRINFO
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "设置业务状态为拒绝成功异常")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit异常")
            
        return AfaFlowControl.ExitThisFlow('S999',"对方拒绝，交易终止")
            
    #====查找自动冲正登记簿是否存在本交易的冲正====
    wheresql = ''
    wheresql = wheresql + "BOJEDT = '" + wtr_dict['BJEDTE'] + "'"                #报单日期
    wheresql = wheresql + "AND BOSPSQ = '" + wtr_dict['BSPSQN'] + "'"                #报单序号
    
    ret = rccpsDBTrcc_atcbka.count(wheresql)
    if ret == -1:
        return AfaFlowControl.ExitThisFlow('S999','查找自动冲正登记簿异常') 
    elif ret > 0:
        #=====原交易已自动冲正，抛弃报文====
        return AfaFlowControl.ExitThisFlow('S999','原交易已冲正，抛弃报文') 

    AfaLoggerFunc.tradeInfo( '>>>查询冲正登记簿结束' )

    #=====主机记账前处理====
    TradeContext.BESBNO  =  wtr_dict['BESBNO']      #机构号
    TradeContext.BETELR  =  wtr_dict['BETELR']      #柜员号
    TradeContext.BEAUUS  =  wtr_dict['BEAUUS']      #授权柜员
    TradeContext.BEAUPS  =  wtr_dict['BEAUPS']      #授权密码
    TradeContext.TERMID  =  wtr_dict['TERMID']      #终端号
    TradeContext.BJEDTE  =  wtr_dict['BJEDTE']      #交易日期
    TradeContext.BSPSQN  =  wtr_dict['BSPSQN']      #报单序号
    TradeContext.BRSFLG  =  wtr_dict['BRSFLG']      #往来账标志
    TradeContext.HostCode=  '8813'                  #主机交易码

    AfaLoggerFunc.tradeInfo( '>>>主机前处理赋值结束' )

    #=====开始更新原交易,新增状态记账－处理中====
    if not rccpsState.newTransState(wtr_dict['BJEDTE'],wtr_dict['BSPSQN'],PL_BCSTAT_ACC,PL_BDWFLG_WAIT):
        #=====RollBack操作====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow('M999', '设置状态失败,系统自动回滚')
    else:
        #=====commit操作====
        AfaDBFunc.CommitSql()
    
    AfaLoggerFunc.tradeInfo( '>>>设置状态记账-处理中结束' )
    
    #=====根据原记录中的手续费收取方式，判断账务处理模式====
    if wtr_dict['CHRGTYP'] == '1':
        #=====转账====
        TradeContext.ACUR    =  '3'                                           #记账次数
        
        #=========交易金额+手续费===================
        TradeContext.RCCSMCD =  PL_RCCSMCD_XJTDWZ                              #摘要代码 
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  '农信银往账'                                  #借方户名
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS           #贷方账号
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '应解汇款'                                    #贷方户名
        TradeContext.OCCAMT  =  str(wtr_dict['OCCAMT'] + wtr_dict['CUSCHRG']) #发生额
        TradeContext.PKFG    = 'T'                                            #存折支票标志
        TradeContext.CTFG    = '9'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:借方账号' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:贷方账号' + TradeContext.RBAC )
        #=========交易金额============
        TradeContext.I2SMCD  =  PL_RCCSMCD_XJTDWZ                              #摘要代码
        TradeContext.I2SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #借方账号
        TradeContext.I2SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM  =  '应解汇款'                                    #借方户名
        TradeContext.I2RBAC  =  ''                                            #贷方账号
        TradeContext.I2OTNM  =  ''                                            #贷方户名
        TradeContext.I2TRAM  =  str(wtr_dict['OCCAMT'])                       #发生额
        TradeContext.I2CTFG  = '7'                                            #结转标志 0 结转 1 不结转
        TradeContext.I2PKFG  = 'T'                                            #存折支票标志
        #TradeContext.I2WARNTNO = ''
        #TradeContext.I2CERTTYPE = ''
        #TradeContext.I2CERTNO = ''
        TradeContext.I2CATR  =  '0'                                           #现转标志
        AfaLoggerFunc.tradeInfo( '>>>交易金额:借方账号' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额:贷方账号' + TradeContext.I2RBAC )
        #=========结算手续费收入户===========
        TradeContext.I3SMCD  =  PL_RCCSMCD_SXF                                #摘要代码
        TradeContext.I3SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #借方账号
        TradeContext.I3SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
        TradeContext.I3ACNM  =  '应解汇款'                                    #借方户名
        TradeContext.I3RBAC  =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #贷方账号
        TradeContext.I3RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
        TradeContext.I3OTNM  =  '结算手续费'                                  #贷方户名
        TradeContext.I3TRAM  =  str(wtr_dict['CUSCHRG'])                      #发生额
        TradeContext.I3CTFG  = '8'                                            #结转标志 0 结转 1 不结转
        TradeContext.I3PKFG  = 'T'                                            #存折支票标志
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:借方账号' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:贷方账号' + TradeContext.I3RBAC )

    elif wtr_dict['CHRGTYP'] == '0':
        #=====本金====
        TradeContext.ACUR    =  '2'                                           #记账次数
        TradeContext.RCCSMCD =  PL_RCCSMCD_XJTDWZ                              #摘要代码
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
        TradeContext.SBAC    = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  '农信银往账'                                  #借方户名
        TradeContext.RBAC    =  ''                                            #贷方账号
        TradeContext.OTNM    =  ''                                            #贷方户名
        TradeContext.OCCAMT  =  str(wtr_dict['OCCAMT'])                       #金额
        TradeContext.CTFG  = '7'
        TradeContext.PKFG  = 'T'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
        TradeContext.CATR  =  '0'                                           #现转标志
        AfaLoggerFunc.tradeInfo( '>>>交易金额:借方账号' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额:贷方账号' + TradeContext.RBAC )
        
        #=====手续费记账赋值====
        TradeContext.I2SMCD  =  PL_RCCSMCD_SXF                                #摘要代码
        TradeContext.I2SBAC  =  ''                                            #借方账号
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #贷方账号
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  '手续费科目'                                  #贷方户名
        TradeContext.I2TRAM  =  str(wtr_dict['CUSCHRG'])                      #金额
        TradeContext.I2CTFG  =  '8'
        TradeContext.I2PKFG  =  'T'
        TradeContext.I2CATR  =  '0'                                           #现转标志
        AfaLoggerFunc.tradeInfo( '>>>交易金额:借方账号' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额:贷方账号' + TradeContext.I2RBAC )
    elif wtr_dict['CHRGTYP'] == '2':
        #=====不收费====
        TradeContext.ACUR    =  '1'                                           #记账次数
        TradeContext.RCCSMCD =  PL_RCCSMCD_XJTDWZ                                #摘要代码
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.RBAC    =  ''                                            #贷方账号
        TradeContext.OTNM    =  ''                                            #贷方户名
        TradeContext.OCCAMT  =  str(wtr_dict['OCCAMT'])                       #金额
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    =  'T'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
        TradeContext.CATR  =  '0'                                             #现转标志
    else:
        #=====出错====
        return AfaFlowControl.ExitThisFlow('S999','手续费收费方式错，抛弃报文') 
    
    AfaLoggerFunc.tradeInfo( '>>>根据手续费收取方式记账赋值处理结束' )
    
    #=====主机记账处理====
    rccpsHostFunc.CommHost(TradeContext.HostCode)
    
    #=====主机后处理====
    set_dict = {}
    set_dict['BSPSQN']  =  TradeContext.BSPSQN
    set_dict['BJEDTE']  =  TradeContext.BJEDTE
    set_dict['BCSTAT']  =  PL_BCSTAT_ACC
    set_dict["SBAC"]    =  TradeContext.SBAC          #借方账号
    set_dict["RBAC"]    =  TradeContext.RBAC          #贷方账号
    set_dict["OTNM"]    =  TradeContext.OTNM          #贷方户名
    set_dict['MGID']    =  TradeContext.errorCode     #主机返回码
    set_dict["STRINFO"]= TradeContext.errorMsg    #主机返回信息
    if TradeContext.errorCode == '0000':
        #=====主机记账成功====
        set_dict['BDWFLG'] = PL_BDWFLG_SUCC
        set_dict['TRDT']   = TradeContext.TRDT
        set_dict['TLSQ']   = TradeContext.TLSQ
    else:
        set_dict['BDWFLG'] = PL_BDWFLG_FAIL
    
    if not rccpsState.setTransState(set_dict):
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    else:
        #=====commit操作====
        AfaDBFunc.CommitSql()
    AfaLoggerFunc.tradeInfo('>>>设置主机返回状态成功') 
    
    if TradeContext.errorCode == '0000':
        #=====开始更新原交易,新增状态清算成功====
        if not rccpsState.newTransState(wtr_dict['BJEDTE'],wtr_dict['BSPSQN'],PL_BCSTAT_MFESTL,PL_BDWFLG_SUCC):
            #=====RollBack操作====
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('M999', '设置状态失败,系统自动回滚')
        else:
            #=====commit操作====
            AfaDBFunc.CommitSql()

    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作).个人现金通兑_折应答[TRCC004_1157]退出***' )
    
    return True
