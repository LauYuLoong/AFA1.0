# -*- coding: gbk -*-                                             
##################################################################
#   农信银.通存通兑往账交易.特殊差错账补记                    
#=================================================================
#   程序文件:   TRCC001_8593.py                                   
#   修改时间:   20089-01-04                                        
#   作者：      潘广通                                            
##################################################################

import TradeContext,AfaFlowControl,AfaLoggerFunc,AfaUtilTools,rccpsState,AfaDBFunc,rccpsEntriesErr,rccpsHostFunc,rccpsFunc,rccpsGetFunc,rccpsState,rccpsEntriesErr
import rccpsDBTrcc_tddzcz,rccpsDBTrcc_wtrbka,rccpsDBTrcc_sstlog,rccpsDBTrcc_paybnk,rccpsDBTrcc_notbka,rccpsDBTrcc_spbsta,rccpsDBTrcc_subbra
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("'***农信银系统：通存通兑往账交易.特殊差错账补记[8593] 进入")
    
    #=====判断必输变量是否存在====
    if not TradeContext.existVariable("BESBNO"):
        return AfaFlowControl.ExitThisFlow('A099','没有机构号')
        
    if not TradeContext.existVariable("TRCCO"):
        return AfaFlowControl.ExitThisFlow('A099','没有交易代码')
        
    if not TradeContext.existVariable("CUSCHRG"):
        return AfaFlowControl.ExitThisFlow('A099','没有手续费金额')
        
    if not TradeContext.existVariable("OCCAMT"):
        return AfaFlowControl.ExitThisFlow('A099','没有交易金额')
        
    #=====得到账户的开户机构====
    AfaLoggerFunc.tradeInfo("<<<<<<查询账户开户机构")
    
    TradeContext.HostCode = '8810'
    TradeContext.BETELR   = PL_BETELR_AUTO
    
    if(TradeContext.TRCCO in ('3000102','3000103','3000104','3000105')):
        TradeContext.ACCNO = TradeContext.PYRACC
        AfaLoggerFunc.tradeDebug("ACCNO<<<<<<" + TradeContext.ACCNO)
    else:
        TradeContext.ACCNO = TradeContext.PYEACC
        AfaLoggerFunc.tradeDebug("ACCNO<<<<<<" + TradeContext.ACCNO)
        
    rccpsHostFunc.CommHost( TradeContext.HostCode )
    
    AfaLoggerFunc.tradeDebug("errorCode<<<<<<" + TradeContext.errorCode)
    AfaLoggerFunc.tradeDebug("errorMsg<<<<<<" + TradeContext.errorMsg)
    
    AfaLoggerFunc.tradeInfo("<<<<<<判断主机8810交易是否成功")
    if(TradeContext.errorCode != '0000'):
        return AfaFlowControl.ExitThisFlow('S999',TradeContext.errorMsg)
    else:
        AfaLoggerFunc.tradeInfo("<<<<<<8810交易成功")
        TradeContext.BESBNO = TradeContext.ACCSO
        
    AfaLoggerFunc.tradeInfo("<<<<<<结束查询账户开户机构")
    
    #=====生成保单序号,成员行号，接收行号，接收行名,前置日期，前置流水号====
#    if not rccpsFunc.GetNCCDate( ) :                      #NCCWKDAT
#        raise AfaFlowControl.flowException( )
#    TradeContext.NCCWKDAT = TradeContext.NCCworkDate

    TradeContext.NCCworkDate = TradeContext.NCCWKDAT
   
    where_dict = {}                                       #发送成员行号
    where_dict['BANKBIN'] = TradeContext.SNDBNKCO
    record = rccpsDBTrcc_paybnk.selectu(where_dict)
    if(record == None):
        return AfaFlowControl.ExitThisFlow('A099','查询行名行号表失败')
    elif(len(record) == 0):
        return AfaFlowControl.ExitThisFlow('A099','查询行名行号表结果为空')
    else:
        TradeContext.STLBANKBIN = record['STLBANKBIN']    
    
#    where_dict = {}                                       #接收行号，接收行名
#    where_dict['BESBNO'] = TradeContext.BESBNO
#    record_tmp = rccpsDBTrcc_subbra.selectu(where_dict)
#    if(record_tmp == None):
#        return AfaFlowControl.ExitThisFlow('A099','查询机构表失败')
#    elif(len(record_tmp) == 0):
#        return AfaFlowControl.ExitThisFlow('A099','查询机构表结果为空')
#    else:
#        TradeContext.BANKBIN = record_tmp['BANKBIN']
#        where_dict = {}
#        where_dict['BANKBIN'] = TradeContext.BANKBIN
#        record = None
#        record = rccpsDBTrcc_paybnk.selectu(where_dict)
#        if(record == None):
#            return AfaFlowControl.ExitThisFlow('A099','查询行名行号表失败')
#        elif(len(record) == 0):
#            AfaLoggerFunc.tradeInfo("此机构无行号")
#            TradeContext.RCVBNKNM = ""
#            TradeContext.RCVBNKCO = ""
#        else:
#            TradeContext.RCVBNKNM = record['BANKNAM']
#            TradeContext.RCVBNKCO = record['BANKBIN']
    
    TradeContext.BJEDTE = AfaUtilTools.GetHostDate( )  #BJEDTE
    
    TradeContext.FEDT = AfaUtilTools.GetHostDate( )      #FEDT
    
    if rccpsGetFunc.GetRBSQ(PL_BRSFLG_RCV) == -1 :     #RBSQ
        return AfaFlowControl.ExitThisFlow('S999','重新生成前置流水号失败,抛弃报文')
        
    TradeContext.BSPSQN = TradeContext.RBSQ
       
    #=====向通存通兑业务登记簿插入数据====
    AfaLoggerFunc.tradeInfo("<<<<<<登记通存通兑业务登记簿")
    insert_dict = {}
    insert_dict['BJEDTE']     = TradeContext.BJEDTE
    insert_dict['BSPSQN']     = TradeContext.BSPSQN
    insert_dict['BRSFLG']     = "1"
    insert_dict['BEACSB']     = ""
    insert_dict['BETELR']     = TradeContext.BETELR
    insert_dict['BEAUUS']     = TradeContext.BEAUUS
    insert_dict['BEAUPS']     = TradeContext.BEAUPS
    insert_dict['TERMID']     = TradeContext.TERMID
    insert_dict['BESBNO']     = TradeContext.BESBNO
    insert_dict['BBSSRC']     = ""
    insert_dict['DASQ']       = ""
    if(TradeContext.TRCCO in ('3000002','3000003','3000004','3000005')):
        insert_dict['DCFLG']  = PL_DCFLG_DEB
    else:
        insert_dict['DCFLG']  = PL_DCFLG_CRE
        
    if(TradeContext.TRCCO in ('3000002','3000004')):
        insert_dict['OPRNO']  = PL_TDOPRNO_TC
    elif(TradeContext.TRCCO in ('3000003','3000005')):
        insert_dict['OPRNO']  = PL_TDOPRNO_BZY
    elif(TradeContext.TRCCO in ('3000102','3000104')):
        insert_dict['OPRNO']  = PL_TDOPRNO_TD
    else:
        insert_dict['OPRNO']  = PL_TDOPRNO_YZB
    insert_dict['OPRATTNO']   = ""
    insert_dict['NCCWKDAT']   = TradeContext.NCCWKDAT
    insert_dict['TRCCO']      = TradeContext.TRCCO
    insert_dict['TRCDAT']     = TradeContext.TRCDAT
    insert_dict['TRCNO']      = TradeContext.TRCNO
    insert_dict['MSGFLGNO']   = ""
    insert_dict['COTRCDAT']   = ""
    insert_dict['COTRCNO']    = ""
    insert_dict['COMSGFLGNO'] = ""
    insert_dict['SNDMBRCO']   = TradeContext.STLBANKBIN
    insert_dict['RCVMBRCO']   = "1340000008"
    insert_dict['SNDBNKCO']   = TradeContext.SNDBNKCO
    insert_dict['SNDBNKNM']   = TradeContext.SNDBNKNM
    insert_dict['RCVBNKCO']   = TradeContext.RCVBNKCO
    insert_dict['RCVBNKNM']   = TradeContext.RCVBNKNM
    insert_dict['CUR']        = "01"
    insert_dict['OCCAMT']     = TradeContext.OCCAMT
    if(float(TradeContext.CUSCHRG) != 0.00 and TradeContext.CUSCHRG != ""):
        insert_dict['CHRGTYP']= PL_CHRG_TYPE 
        chrgtyp = 1
    else:
        insert_dict['CHRGTYP']= PL_CHRG_CASH
        chrgtyp = 0
    insert_dict['LOCCUSCHRG'] = ""
    insert_dict['CUSCHRG']    = TradeContext.CUSCHRG
    insert_dict['PYRTYP']     = ""
    insert_dict['PYRACC']     = TradeContext.PYRACC 
    insert_dict['PYRNAM']     = TradeContext.PYRNAM  
    insert_dict['PYRADDR']    = "" 
    insert_dict['PYETYP']     = ""
    insert_dict['PYEACC']     = TradeContext.PYEACC
    insert_dict['PYENAM']     = TradeContext.PYENAM 
    insert_dict['PYEADDR']    = "" 
    insert_dict['STRINFO']    = TradeContext.STRINFO
    insert_dict['CERTTYPE']   = ""
    insert_dict['CERTNO']     = ""
    insert_dict['BNKBKNO']    = "" 
    insert_dict['BNKBKBAL']   = ""
    insert_dict['NOTE1']      = "" 
    insert_dict['NOTE2']      = "" 
    insert_dict['NOTE3']      = "" 
    insert_dict['NOTE4']      = "" 
    
    if not rccpsDBTrcc_wtrbka.insertCmt(insert_dict):
        return AfaFlowControl.ExitThisFlow('A099','登记通存通兑登记簿失败')
    
    AfaLoggerFunc.tradeInfo("<<<<<<结束登记通存通兑业务登记簿")    
    
    #=====查询刚刚插入到业务登记簿中的数据====
    where_dict = {}
    where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}
    wtrbka_record = rccpsDBTrcc_wtrbka.selectu(where_dict)
    if(wtrbka_record == None):
        return AfaFlowControl.ExitThisFlow('A099','查询通存通兑业务登记簿失败')
    elif(len(wtrbka_record) == 0):
        return AfaFlowControl.ExitThisFlow('A099','登记通存通兑业务登记簿结果为空')
    else:
        AfaLoggerFunc.tradeInfo("查询通存通兑业务登记簿成功")
    
    
    #=====向错账登记簿插入数据====
    AfaLoggerFunc.tradeInfo("<<<<<<登记错账登记簿")
    insert_dict = {}
    insert_dict['NCCWKDAT']   = TradeContext.NCCWKDAT 
    insert_dict['SNDBNKCO']   = TradeContext.SNDBNKCO
    insert_dict['TRCDAT']     = TradeContext.TRCDAT
    insert_dict['TRCNO']      = TradeContext.TRCNO
    insert_dict['RCVBNKCO']   = TradeContext.RCVBNKCO
    insert_dict['SNDMBRCO']   = TradeContext.STLBANKBIN
    insert_dict['RCVMBRCO']   = "1340000008"
    insert_dict['TRCCO']      = TradeContext.TRCCO
    if(TradeContext.TRCCO in ('3000002','3000003','3000004','3000005')):
        insert_dict['DCFLG']  = PL_DCFLG_DEB
    else:
        insert_dict['DCFLG']  = PL_DCFLG_CRE
    insert_dict['PYRACC']     = TradeContext.PYRACC
    insert_dict['PYEACC']     = TradeContext.PYEACC
    insert_dict['CUR']        = "01"
    insert_dict['OCCAMT']     = TradeContext.OCCAMT
    insert_dict['LOCOCCAMT']  = TradeContext.OCCAMT
    if(TradeContext.TRCCO in ('3000102','3000103','3000104','3000105') and wtrbka_record['CHRGTYP'] == PL_CHRG_TYPE ):
        insert_dict['CUSCHRG']    = TradeContext.CUSCHRG
        insert_dict['LOCCUSCHRG'] = TradeContext.CUSCHRG
    else:
        insert_dict['CUSCHRG']    = 0.00
        insert_dict['LOCCUSCHRG'] = 0.00
    insert_dict['ORTRCNO']    = ""
    insert_dict['BJEDTE']     = AfaUtilTools.GetHostDate( )
    insert_dict['BSPSQN']     = TradeContext.BSPSQN
    insert_dict['EACTYP']     = "11"
    insert_dict['EACINF']     = "中心无，行内无"
    insert_dict['LOCEACTYP']  = "11"
    insert_dict['LOCEACINF']  = "中心无，行内无"
    insert_dict['ISDEAL']     = PL_ISDEAL_UNDO
    insert_dict['NOTE1']      = ""
    insert_dict['NOTE2']      = ""
    insert_dict['NOTE3']      = ""
    insert_dict['NOTE4']      = ""
    
    if not rccpsDBTrcc_tddzcz.insertCmt(insert_dict):
        return AfaFlowControl.ExitThisFlow('A099','登记通存通兑登记簿失败')

    AfaLoggerFunc.tradeInfo("<<<<<<结束登记错账登记簿")
    
    #=====查询刚刚插入到业务登记簿中的数据====
    where_dict = {}
    where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}
    tddzcz_record = rccpsDBTrcc_tddzcz.selectu(where_dict)
    if(tddzcz_record == None):
        return AfaFlowControl.ExitThisFlow('A099','查询错账登记簿失败')
    elif(len(tddzcz_record) == 0):
        return AfaFlowControl.ExitThisFlow('A099','登记错账登记簿结果为空')
    else:
        AfaLoggerFunc.tradeInfo("查询错账登记簿成功")
    
    #=====开始给会计分录赋值====
    AfaLoggerFunc.tradeInfo("<<<<<<开始给会计分录赋值")
    TradeContext.BRSFLG   = PL_BRSFLG_RCV
    TradeContext.BETELR   = PL_BETELR_AUTO
    AfaLoggerFunc.tradeInfo("<<<<<<BETELR==" + TradeContext.BETELR)
    input_dict = {}
    input_dict['FEDT']    = TradeContext.FEDT
    input_dict['RBSQ']    = TradeContext.RBSQ
    input_dict['PYRACC']  = wtrbka_record['PYRACC']
    input_dict['PYRNAM']  = wtrbka_record['PYRNAM']
    input_dict['PYEACC']  = wtrbka_record['PYEACC']
    input_dict['PYENAM']  = wtrbka_record['PYENAM']
    input_dict['CHRGTYP'] = wtrbka_record['CHRGTYP']
    input_dict['OCCAMT']  = wtrbka_record['OCCAMT']
    input_dict['CUSCHRG'] = wtrbka_record['CUSCHRG']
    
    if(wtrbka_record['TRCCO'] in ('3000002','3000004')):  
        AfaLoggerFunc.tradeDebug("<<<<<<卡折现金通存来账记账")
        input_dict['RCCSMCD'] = PL_RCCSMCD_XJTCLZ
        rccpsEntriesErr.KZTCLZJZ(input_dict)
        
    elif(wtrbka_record['TRCCO'] in ('3000003','3000005')):
        AfaLoggerFunc.tradeDebug("<<<<<<卡折本转异来账记账")
        input_dict['RCCSMCD'] = PL_RCCSMCD_BZYLZ
        rccpsEntriesErr.KZBZYLZJZ(input_dict)
        
    elif(wtrbka_record['TRCCO'] in ('3000102','3000104')):
        AfaLoggerFunc.tradeDebug("<<<<<<卡折现金通兑来账记账")
        input_dict['RCCSMCD'] = PL_RCCSMCD_XJTDLZ
        rccpsEntriesErr.KZTDLZJZ(input_dict)
        
    elif(wtrbka_record['TRCCO'] in ('3000103','3000105')):
        AfaLoggerFunc.tradeDebug("<<<<<<卡折异转本来账记账")
        input_dict['RCCSMCD'] = PL_RCCSMCD_YZBLZ
        rccpsEntriesErr.KZYZBLZJZ(input_dict)
    
    else:
        return AfaFlowControl.ExitThisFlow('A099','交易代码非法')
        
    AfaLoggerFunc.tradeInfo("<<<<<<给会计分录赋值结束") 
    
    #=====主机前设置原交易状态====  
    AfaLoggerFunc.tradeInfo("<<<<<<主机前设置原交易状态")  
    if not rccpsState.newTransState(wtrbka_record['BJEDTE'],wtrbka_record['BSPSQN'],PL_BCSTAT_ACC,PL_BDWFLG_WAIT):
        return AfaFlowControl.ExitThisFlow('S999','设置业务状态为记账处理中异常')
    else:
        AfaDBFunc.CommitSql()
        
    #=====调用主机交易====
    AfaLoggerFunc.tradeInfo("<<<<<<开始调用主机交易")
    rccpsHostFunc.CommHost( TradeContext.HostCode )
    AfaLoggerFunc.tradeInfo("<<<<<<结束调用主机交易") 
    
    AfaLoggerFunc.tradeDebug("errorCode<<<<<<" + TradeContext.errorCode)
    AfaLoggerFunc.tradeDebug("errorMsg<<<<<<" + TradeContext.errorMsg)
    
    #=====给状态字典赋值====
    state_dict = {}
    state_dict['BJEDTE'] = wtrbka_record['BJEDTE']
    state_dict['BSPSQN'] = wtrbka_record['BSPSQN']
    state_dict['MGID']   = TradeContext.errorCode
    if TradeContext.existVariable('TRDT'):
        state_dict['TRDT']   = TradeContext.TRDT
    if TradeContext.existVariable('TLSQ'):
        state_dict['TLSQ']   = TradeContext.TLSQ
    if TradeContext.existVariable('RBSQ'): 
        state_dict['RBSQ'] = TradeContext.RBSQ
    if TradeContext.existVariable('FEDT'):
        state_dict['FEDT'] = TradeContext.FEDT
    
    #=====判断主机交易是否成功====
    AfaLoggerFunc.tradeInfo("<<<<<<判断主机交易是否成功")
    AfaLoggerFunc.tradeDebug("<<<<<<errorCode=" + TradeContext.errorCode)
    if(TradeContext.errorCode != '0000'):
        AfaLoggerFunc.tradeInfo("调用主机交易失败")
        #=====主机后更改原交易状态为失败====
        state_dict['BDWFLG'] = PL_BDWFLG_FAIL
        state_dict['STRINFO'] = TradeContext.errorMsg
        state_dict['NOTE3'] = "特殊差错账补记失败"
        state_dict['BCSTAT'] = PL_BCSTAT_ACC
        if not rccpsState.setTransState(state_dict):
            return AfaFlowControl.ExitThisFlow('S999','设置业务状态为失败异常')
        else:
            AfaDBFunc.CommitSql()
       
        return AfaFlowControl.ExitThisFlow('S999',TradeContext.errorMsg)
        
    else:
        #=====主机后更改原交易状态为成功====
        state_dict['BDWFLG'] = PL_BDWFLG_SUCC
        state_dict['STRINFO'] = '主机成功'
        state_dict['NOTE3'] = "特殊差错账补记成功"
        if(TradeContext.TRCCO in('3000002','3000004','3000005','3000003')):    #通存
            state_dict['BCSTAT'] = PL_BCSTAT_AUTO 
        else:
            state_dict['BCSTAT'] = PL_BCSTAT_AUTOPAY
        if(TradeContext.existVariable("SBAC")):
            state_dict['SBAC'] = TradeContext.SBAC
        if(TradeContext.existVariable("RBAC")):
            state_dict['RBAC'] = TradeContext.RBAC
        if not rccpsState.setTransState(state_dict):
            return AfaFlowControl.ExitThisFlow('S999','设置业务状态失败')
        else:
            AfaDBFunc.CommitSql()
            
#        bcsata = ""    #状态标识
#        if(TradeContext.TRCCO in('3000002','3000004','3000005','3000003')):    #通存
#            bcstat = PL_BCSTAT_AUTO 
#        else:
#            bcstat = PL_BCSTAT_AUTOPAY       
#        if not rccpsState.newTransState(wtrbka_record['BJEDTE'],wtrbka_record['BSPSQN'],bcstat,PL_BDWFLG_SUCC):
#            return AfaFlowControl.ExitThisFlow('S999','设置业务状态异常')
#        else:
#            AfaDBFunc.CommitSql()
        
    #=====更改错账登记簿中的处理标示====
    AfaLoggerFunc.tradeInfo("<<<<<<更改错账登记簿中的处理标示")
    where_dict = {}
    where_dict = {'BJEDTE':tddzcz_record['BJEDTE'],'BSPSQN':tddzcz_record['BSPSQN']}
    update_dict = {}
    update_dict['ISDEAL'] = PL_ISDEAL_ISDO
    update_dict['NOTE3']  = '此笔错账已补记'
    res = rccpsDBTrcc_tddzcz.updateCmt(update_dict,where_dict)
    if(res == -1):
        return AfaFlowControl.ExitThisFlow('S999','主机记账已成功，但更新处理标示失败，请手动更改处理标示')
        
    else:
        AfaLoggerFunc.tradeInfo("<<<<<<更改错账登记簿中的处理标示成功")

    #=====向下发的通知表中插入数据====
    AfaLoggerFunc.tradeInfo("<<<<<<向通知表中插入数据")
    insert_dict = {}
    insert_dict['NOTDAT']  = AfaUtilTools.GetHostDate( )
    insert_dict['BESBNO']  = wtrbka_record['BESBNO']
    if(wtrbka_record['BRSFLG'] == PL_BRSFLG_RCV):
        insert_dict['STRINFO'] = "此笔错账["+wtrbka_record['BSPSQN']+"]["+wtrbka_record['BJEDTE']+"]已处理"
    else:
        insert_dict['STRINFO'] = "此笔错账["+wtrbka_record['BSPSQN']+"]["+wtrbka_record['BJEDTE']+"]已处理 请用8522补打往账凭证"
    if not rccpsDBTrcc_notbka.insertCmt(insert_dict):
        return AfaFlowControl.ExitThisFlow('S999','向下发的通知表中插入数据失败')
    AfaLoggerFunc.tradeInfo("<<<<<<向通知表中插入数据成功")
    
    
    #=====给输出接口赋值====
    AfaLoggerFunc.tradeInfo("<<<<<<开始给输出接口赋值")
    TradeContext.TRCCO      = wtrbka_record['TRCCO']
    TradeContext.BRSFLG     = wtrbka_record['BRSFLG']
    TradeContext.BEACSB     = wtrbka_record['BESBNO']
    TradeContext.OCCAMT     = str(wtrbka_record['OCCAMT'])
    TradeContext.BSPSQN     = state_dict['TLSQ']
    TradeContext.BJEDTE     = wtrbka_record['BJEDTE']
    
    AfaLoggerFunc.tradeInfo("<<<<<<结束给输出接口赋值")
    
    AfaLoggerFunc.tradeInfo("<<<<<<<个性化处理(本地操作) 退出")
    
    AfaLoggerFunc.tradeInfo("'***农信银系统：通存通兑往账交易.特殊差错账补记[8593] 退出")
    return True
    
    