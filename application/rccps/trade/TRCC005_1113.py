# -*- coding: gbk -*-
################################################################################
#   农信银系统：来账.主机类操作模板(1.本地操作 2.主机记账 3.中心回执).汇票解付接收
#===============================================================================
#   交易文件:   TRCC005_1113.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘雨龙
#   修改时间:   2008-08-12
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc
import AfaAfeFunc
import rccpsDBFunc,rccpsState,rccpsDBTrcc_bilbka,rccpsMap0000Dout_context2CTradeContext
import rccpsMap1113CTradeContext2Dbilbka,rccpsDBFunc,rccpsHostFunc,AfaFlowControl
import rccpsDBTrcc_bilinf

from types import *
from rccpsConst import *

#=====================交易前处理(登记流水,主机前处理)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( "====开始汇票解付接收处理====" )

    #=====判断是否重复交易====
    sel_dict = {'TRCNO':TradeContext.TRCNO,'TRCDAT':TradeContext.TRCDAT,'SNDBNKCO':TradeContext.SNDBNKCO}
    record = rccpsDBTrcc_bilbka.selectu(sel_dict)
    if record == None:
        return AfaFlowControl.ExitThisFlow('S999','判断是否重复报文，查询汇兑业务登记簿相同报文异常')
    elif len(record) > 0:
        AfaLoggerFunc.tradeInfo('汇票业务登记簿中存在相同数据,重复报文,进入下一流程')
        #=====为通讯回执报文赋值====
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
        out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
        out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
        out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
        out_context_dict['OPRTYPNO'] = '99'
        out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
        out_context_dict['TRANTYP']  = '0'
        out_context_dict['ORTRCCO']  = TradeContext.TRCCO
        out_context_dict['PRCCO']    = 'RCCI0000'
        out_context_dict['STRINFO']  = '重复报文'

        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)

        #=====发送afe====
        AfaAfeFunc.CommAfe()

        return AfaFlowControl.ExitThisFlow('S999','重复报文，退出处理流程')

    AfaLoggerFunc.tradeInfo(">>>结束判断是否重复报文")
    

    #=====币种转换====
    if TradeContext.CUR == 'CNY':
        TradeContext.CUR  = '01'
    
    TradeContext.DCFLG = '1'
    TradeContext.HPSTAT= PL_HPSTAT_PAYC     #解付 02
    TradeContext.OPRNO = PL_HPOPRNO_JF
    
    #=====插入数据库====
    AfaLoggerFunc.tradeInfo(">>>开始记录数据库操作")
    
    bilbka_dict = {}
    if not rccpsMap1113CTradeContext2Dbilbka.map(bilbka_dict):
        return AfaFlowControl.ExitThisFlow("S999","为汇票业务登记簿赋值异常")
        
    if not rccpsDBFunc.insTransBil(bilbka_dict):
        return AfaFlowControl.ExitThisFlow('S999','登记汇票业务登记簿异常')
    
    AfaDBFunc.CommitSql()    
    AfaLoggerFunc.tradeInfo(">>>结束记录数据库操作")     
    
    #=====设置状态为收妥====
    sstlog   = {}
    sstlog['BSPSQN']   = TradeContext.BSPSQN
    sstlog['BJEDTE']   = TradeContext.BJEDTE
    sstlog['BCSTAT']   = PL_BCSTAT_BNKRCV
    sstlog['BDWFLG']   = PL_BDWFLG_SUCC

    #=====设置状态为 收妥-成功 ====
    if not rccpsState.setTransState(sstlog):
        #=====RollBack操作====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    else:
        #=====commit操作====
        AfaDBFunc.CommitSql()
        AfaLoggerFunc.tradeInfo('>>>commit成功')
        
    #=====设置汇票业务登记簿和信息登记簿状态====
    #=====设置汇票状态为解付====
    AfaLoggerFunc.tradeInfo(">>>开始设置汇票状态为解付")
    
    if not rccpsState.newBilState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_HPSTAT_PAYC):
        return AfaFlowControl.ExitThisFlow("S999","设置汇票状态异常")
    
    AfaLoggerFunc.tradeInfo(">>>结束设置汇票状态为解付")
    
    #=====commit操作====
    AfaDBFunc.CommitSql()
    
    #=====设置汇票解付金额====
    bil_dict = {}
    bil_dict['BILNO']  = TradeContext.BILNO
    bil_dict['BILVER'] = TradeContext.BILVER
    bil_dict['BILRS']  = TradeContext.BILRS
    bil_end = {}
    bil_end['OCCAMT']  = TradeContext.OCCAMT
    bil_end['RMNAMT']  = TradeContext.RMNAMT
    bil_end['PAYBNKCO']= TradeContext.SNDBNKCO
    bil_end['PAYBNKNM']= TradeContext.SNDBNKNM
    
    ret = rccpsDBTrcc_bilinf.update(bil_end,bil_dict)
    if (ret <= 0):
        return AfaFlowControl.ExitThisFlow("S999","更新汇票信息异常")
    AfaDBFunc.CommitSql() 
    
    AfaLoggerFunc.tradeInfo('>>>commit成功')
    
    AfaLoggerFunc.tradeInfo(">>>开始判断是否存在多余款操作")
    
    if float(TradeContext.RMNAMT) != 0.00:
        AfaLoggerFunc.tradeInfo(">>>第二次记账赋值操作")
        
        TradeContext.ACUR   = '2'   #记账循环次数
        TradeContext.TRFG   = '9'   #凭证处理标识'
        TradeContext.I2CETY = ''    #凭证种类
        TradeContext.I2TRAM = TradeContext.RMNAMT   #结余金额
        TradeContext.I2SMCD = PL_RCCSMCD_HPJF       #摘要代码
        TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_DYKJQ   #贷方账号
        TradeContext.I2SBAC = TradeContext.BESBNO + PL_ACC_HCHK    #借方账号
        TradeContext.I2REAC = TradeContext.BESBNO + PL_ACC_NXYDXZ  #挂账账号
        
        #=====生成账号校验位====
        TradeContext.I2SBAC = rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2REAC = rccpsHostFunc.CrtAcc(TradeContext.I2REAC,25)
        
    AfaLoggerFunc.tradeInfo(">>>结束判断是否存在多余款操作")
    
    AfaLoggerFunc.tradeInfo(">>>开始组织报文上送主机记账操作")
    #=====组织报文发送主机记账====
    TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ #贷方账号
    TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_HCHK     #借方账号
    TradeContext.REAC    =  TradeContext.BESBNO + PL_ACC_NXYDXZ   #挂账账号
  
    #=====生成账号校验位====
    TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
    TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
    TradeContext.REAC = rccpsHostFunc.CrtAcc(TradeContext.REAC,25)
    
    TradeContext.HostCode = '8813'
    #关彬捷 20081007
    #TradeContext.NOTE3    = '主机记账'
    TradeContext.NOTE3    = ''
    TradeContext.RCCSMCD = PL_RCCSMCD_HPJF       #摘要代码
        
    AfaLoggerFunc.tradeInfo(">>>结束组织报文上送主机记账操作")
    AfaLoggerFunc.tradeInfo(">>>开始更新登记簿状态") 
    
    #关彬捷 20081007 改记账状态为自动入账
    #TradeContext.BCSTAT  = PL_BCSTAT_ACC    #记账
    TradeContext.BCSTAT  = PL_BCSTAT_AUTO    #自动入账
    TradeContext.BDWFLG  = PL_BDWFLG_WAIT   #处理中
    
    #=====新增sstlog表状态记录====
    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,TradeContext.BCSTAT,TradeContext.BDWFLG):
        #=====RollBack操作====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow('M999', '设置状态['+TradeContext.BCSTAT+']['+TradeContext.BDWFLG+']失败,系统自动回滚')
    else:
        #=====commit操作====
        AfaDBFunc.CommitSql()
    
    AfaLoggerFunc.tradeInfo(">>>结束更新登记簿状态") 
    
    return True
#=====================交易中处理(修改流水,主机后处理,中心前处理)================
def SubModuleDoSnd():
    #=====开始向字典赋值====
    AfaLoggerFunc.tradeInfo('>>>主机记账后处理')
    sst_dict = {}
    sst_dict['BSPSQN']  = TradeContext.BSPSQN            #报单序号
    AfaLoggerFunc.tradeDebug('>>>test by lyl as BSPSQN=['+TradeContext.BSPSQN+']')
    sst_dict['BJEDTE']  = TradeContext.BJEDTE            #交易日期
    AfaLoggerFunc.tradeDebug('>>>test by lyl as BJEDTE=['+TradeContext.BJEDTE+']')
    sst_dict['SBAC']    = TradeContext.SBAC              #借方账号
    AfaLoggerFunc.tradeDebug('>>>test by lyl as SBAC=['+TradeContext.SBAC+']')
    sst_dict['NOTE3']   = TradeContext.NOTE3             #备注3
    AfaLoggerFunc.tradeDebug('>>>test by lyl as NOTE3 =['+TradeContext.NOTE3 +']')
    sst_dict['BJETIM']  = TradeContext.BJETIM            #交易时间
    AfaLoggerFunc.tradeDebug('>>>test by lyl as BJETIM=['+TradeContext.BJETIM+']')
    sst_dict['MGID']   = TradeContext.errorCode           #主机返回信息
    AfaLoggerFunc.tradeDebug('>>>test by lyl as MGID =['+str(sst_dict['MGID']) +']')
    sst_dict['STRINFO']  = TradeContext.errorMsg         #主机返回信息
    AfaLoggerFunc.tradeDebug('>>>test by lyl as STRINFO =['+str(sst_dict['STRINFO']) +']')
    sst_dict['BETELR']  = TradeContext.BETELR            #柜员号
    AfaLoggerFunc.tradeDebug('>>>test by lyl as BETELR=['+TradeContext.BETELR+']')
    sst_dict['RBAC']    = TradeContext.RBAC              #贷方账号
    AfaLoggerFunc.tradeDebug('>>>test by lyl as RBAC  =['+TradeContext.RBAC +']')
    sst_dict['BCSTAT']  = PL_BCSTAT_AUTO                 #自动入账成功
    AfaLoggerFunc.tradeDebug('>>>test by lyl as BCSTAT=['+str(sst_dict['BCSTAT']) +']')
    sst_dict['BESBNO']  = TradeContext.BESBNO            #机构号
    AfaLoggerFunc.tradeDebug('>>>test by lyl as BESBNO=['+TradeContext.BESBNO+']')

    #=====开始判断主机返回结果====
    out_context_dict = {}
    if TradeContext.errorCode == '0000':
        if( TradeContext.existVariable('DASQ') and len(TradeContext.DASQ) != 0 ):
            sst_dict['DASQ']    = TradeContext.DASQ              #销账序号
            AfaLoggerFunc.tradeDebug('>>>test by lyl as DASQ  =['+TradeContext.DASQ +']')
            sst_dict['RBAC']    = TradeContext.REAC              #挂账账号
            AfaLoggerFunc.tradeDebug('>>>test by lyl as RBAC  =['+TradeContext.RBAC +']')
            sst_dict['BCSTAT']  = PL_BCSTAT_HANG                 #自动挂账 71
            AfaLoggerFunc.tradeDebug('>>>test by lyl as BCSTAT=['+str(sst_dict['BCSTAT']) +']')
            if len(sst_dict['NOTE3']) == 0:
                sst_dict['NOTE3'] = "主机方挂账"
        else:
            sst_dict['RBAC']    = TradeContext.RBAC              #贷方账号
            AfaLoggerFunc.tradeDebug('>>>test by lyl as RBAC  =['+TradeContext.RBAC +']')
            sst_dict['BCSTAT']  = PL_BCSTAT_AUTO                 #自动入账 70
            AfaLoggerFunc.tradeDebug('>>>test by lyl as BCSTAT=['+str(sst_dict['BCSTAT']) +']')

        sst_dict['BDWFLG']  = PL_BDWFLG_SUCC         #成功
        AfaLoggerFunc.tradeDebug('>>>test by lyl as BDWFLG=['+str(sst_dict['BDWFLG']) +']')
        sst_dict['TRDT']    = TradeContext.TRDT             #主机日期
        AfaLoggerFunc.tradeDebug('>>>test by lyl as TRDT  =['+TradeContext.TRDT   +']')
        sst_dict['TLSQ']    = TradeContext.TLSQ             #主机流水
        AfaLoggerFunc.tradeDebug('>>>test by lyl as TLSQ  =['+TradeContext.TLSQ   +']')
        out_context_dict['PRCCO']    = 'RCCI0000'
        out_context_dict['STRINFO']  = '成功'
    else:
        sst_dict['BDWFLG']  = PL_BDWFLG_FAIL         #失败
        out_context_dict['PRCCO']    = 'RCCI1056'
        out_context_dict['STRINFO']  = '其它错误'
            
    AfaLoggerFunc.tradeDebug('>>>当前业务状态[' + str(sst_dict['BCSTAT']) + ']')
    AfaLoggerFunc.tradeDebug('>>>当前流转标志[' + str(sst_dict['BDWFLG']) + ']')
    
    #=====设置状态为 记账/挂账-成功 ====
    if not rccpsState.setTransState(sst_dict):
        #=====RollBack操作====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    else:
        #=====commit操作====
        AfaDBFunc.CommitSql()
        AfaLoggerFunc.tradeDebug('>>>commit成功')


    #=====开始设置通讯回执报文信息====
    AfaLoggerFunc.tradeInfo('>>>开始组织通讯回执报文')

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

    rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
    
    return True
#=====================交易后处理================================================
def SubModuleDoTrd():
    #=====判断afe返回结果====
    if TradeContext.errorCode == '0000':
        AfaLoggerFunc.tradeInfo('>>>发送回执报文成功')
    else:
        AfaLoggerFunc.tradeInfo('>>>发送回执报文失败')
        
    return True
