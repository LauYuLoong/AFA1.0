# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.本地类操作(1.本地操作).通存通兑错帐手工结转
#===============================================================================
#   模板文件:   TRCC001_8591.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘振东
#   修改时间:   2008-12-16
################################################################################
#   修改者：    潘广通
#   修改时间：  20081225
#   修改内容：  增加对清算状态调整的处理
#################################################################################

import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,rccpsState,AfaDBFunc,rccpsHostFunc,rccpsFunc,rccpsDBFunc,rccpsGetFunc
import rccpsDBTrcc_tddzcz,rccpsDBTrcc_wtrbka,rccpsDBTrcc_spbsta,rccpsDBTrcc_notbka
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统: 往账.本地类操作交易[RCC001_8591]通存通兑错帐处理标识维护进入***' )
    
    AfaLoggerFunc.tradeInfo('个性化处理(本地操作)')
    
    #=====判断接口变量是否存在====
    if not TradeContext.existVariable("SNDBNKCO"):
        return AfaFlowControl.ExitThisFlow('A099','发送行号不能为空' )
        
    if not TradeContext.existVariable("TRCDAT"):
        return AfaFlowControl.ExitThisFlow('A009','委托日期不能为空')
        
    if not TradeContext.existVariable("TRCNO"):
        return AfaFlowControl.ExitThisFlow('A009','交易流水号不能为空')
        
    if not TradeContext.existVariable("BJEDTE"):
        return AfaFlowControl.ExitThisFlow('A009','报单日期不能为空')
        
    if not TradeContext.existVariable("BSPSQN"):
        return AfaFlowControl.ExitThisFlow('A009','报单序号不能为空')
    
    AfaLoggerFunc.tradeInfo('个性化处理结束(本地操作)') 
    
    #=====得到nccwkdat====
    if not rccpsFunc.GetNCCDate( ) :                   #NCCworkDate
        raise AfaFlowControl.flowException( )
    
    #=====查询错账登记簿====
    where_dict = {}
    where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN,'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO}
    tddzcz_record = rccpsDBTrcc_tddzcz.selectu(where_dict)
    if(tddzcz_record == None):
        return AfaFlowControl.ExitThisFlow('A009','查询错账登记簿失败')
        
    elif(len(tddzcz_record) == 0):
        return AfaFlowControl.ExitThisFlow('A009','查询错账登记簿为空')
        
    else:
        AfaLoggerFunc.tradeInfo("查询错账登记簿成功")
    
    #=====查询原业务的信息====
    AfaLoggerFunc.tradeInfo('查询原业务信息')
    where_dict = {}
    where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}
    wtrbka_record = rccpsDBTrcc_wtrbka.selectu(where_dict)
    if(wtrbka_record == None):
        return AfaFlowControl.ExitThisFlow('A009','查询业务登记簿失败')
        
    elif(len(wtrbka_record) == 0):
        return AfaFlowControl.ExitThisFlow('A009','查询业务登记簿为空')   
        
    else:
        AfaLoggerFunc.tradeInfo('查询业务登记簿成功') 
        
    #=====查询业务的当前信息====
    wtr_dict = {}
    if not rccpsDBFunc.getTransWtr(TradeContext.BJEDTE,TradeContext.BSPSQN,wtr_dict):
        return AfaFlowControl.ExitThisFlow('A009','查询业务的当前信息失败')
        
    if(wtr_dict['BRSFLG'] == PL_BRSFLG_SND):
        sstlog_dict = {}
        if not rccpsState.getTransStateSet(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_ACC,PL_BDWFLG_SUCC,sstlog_dict):
            return AfaFlowControl.ExitThisFlow('A009','查询业务状态信息失败')
            
        wtr_dict['FEDT'] = sstlog_dict['FEDT']
        wtr_dict['RBSQ'] = sstlog_dict['RBSQ']
        
    TradeContext.CLDT = wtr_dict['FEDT']
    TradeContext.UNSQ = wtr_dict['RBSQ']
    if rccpsGetFunc.GetRBSQ(PL_BRSFLG_SND) == -1 :   #RBSQ
        return AfaFlowControl.ExitThisFlow('A099','产生前置流水号失败')
    TradeContext.FEDT=AfaUtilTools.GetHostDate( )    #FEDT
    
    #=====判断当前业务是否已经结转====
    if(wtr_dict['BCSTAT'] == PL_BCSTAT_TRAS and wtr_dict['BDWFLG'] == PL_BDWFLG_SUCC):
        return AfaFlowControl.ExitThisFlow('A009','该账务已经结转')
        
        
    #=====判断业务的往来标示====
    AfaLoggerFunc.tradeInfo('<<<<<<判断业务的往来标示')
    if(wtrbka_record['BRSFLG'] == PL_BRSFLG_SND):
        AfaLoggerFunc.tradeInfo('<<<<<<业务为往账')
        acc    = 0    
        hcac   = 0   
        canc   = 0
        cancel = 0
        
        #=====查询是否有记账成功的状态====
        sstlog_list = []
        if rccpsState.getTransStateSetm(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_ACC,PL_BDWFLG_SUCC,sstlog_list):
            acc = len(sstlog_list)
        #=====查询是否有抹账的状态====
        sstlog_list = []
        if rccpsState.getTransStateSetm(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_HCAC,PL_BDWFLG_SUCC,sstlog_list):
            hcac = len(sstlog_list)
        #=====查询是否有冲销的状态====
        sstlog_list = []
        if rccpsState.getTransStateSetm(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_CANC,PL_BDWFLG_SUCC,sstlog_list):
            canc = len(sstlog_list)
        #=====查询是否有冲正的状态====
        ssltog_list = []
        if rccpsState.getTransStateSetm(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_CANCEL,PL_BDWFLG_SUCC,sstlog_list):
            cancel = len(sstlog_list)
        
        #=====判断是否需要清算状态调整====
        AfaLoggerFunc.tradeInfo('<<<<<<判断是否需要清算状态调整')
        if(acc - (hcac + canc + cancel) >= 0):
            AfaLoggerFunc.tradeInfo('<<<<<<需要进行清算状态调整')
                
            TradeContext.BETELR   = PL_BETELR_AUTO
            TradeContext.BRSFLG   = wtrbka_record['BRSFLG']    
            TradeContext.CHRGTYP  = wtrbka_record['CHRGTYP']
            TradeContext.BESBNO   = wtrbka_record['BESBNO'] 
            #=====卡折存现/本转异地====
            if(wtrbka_record['TRCCO'] in ('3000002','3000003','3000004','3000005')):
                AfaLoggerFunc.tradeInfo('卡折存现/本转异地')
                TradeContext.HostCode = '8813' 
                TradeContext.ACUR     = '1'
                TradeContext.RCCSMCD  = PL_RCCSMCD_DZBJ
                TradeContext.SBAC     = wtrbka_record['BESBNO'] + PL_ACC_NXYDQSWZ          #借方账号
                TradeContext.SBAC     = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
                TradeContext.ACNM     = '农信银待清算往账'                                 #借方户名
                TradeContext.RBAC     = wtrbka_record['BESBNO'] + PL_ACC_NXYWZ             #贷方账号
                TradeContext.RBAC     = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
                TradeContext.OTNM     = '农信银往账'                                       #贷方户名
                TradeContext.OCCAMT   = str(wtrbka_record['OCCAMT'])                       #发生额
                TradeContext.PKFG     = 'W'
                TradeContext.CTFG     = '7'
                    
            #=====卡折取现/异地转本地====
            elif(wtrbka_record['TRCCO'] in ('3000102','3000103','3000104','3000105')): 
                AfaLoggerFunc.tradeInfo('卡折取现/异地转本地')
                if(wtrbka_record['CHRGTYP'] == '1'):    #转收           
                    AfaLoggerFunc.tradeInfo("<<<<<转收手续费")
                    TradeContext.HostCode = '8813' 
                    TradeContext.ACUR     = '1'
                    TradeContext.RCCSMCD  = PL_RCCSMCD_DZBJ
                    TradeContext.SBAC     = wtrbka_record['BESBNO'] + PL_ACC_NXYWZ    #借方账号
                    TradeContext.SBAC     = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25) 
                    TradeContext.ACNM     = '农信银往账'
                    TradeContext.RBAC     = wtrbka_record['BESBNO'] + PL_ACC_NXYDQSWZ #贷方账号 
                    TradeContext.RBAC     = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
                    TradeContext.OTNM     = '农信银待清算往账'
                    TradeContext.OCCAMT   = str(wtrbka_record['OCCAMT'] + wtrbka_record['CUSCHRG'])
                    TradeContext.PKFG     = 'W'
                    TradeContext.CTFG     = '9'
                    
                else:    #现收
                    AfaLoggerFunc.tradeInfo("<<<<<现收手续费，或不收")
                    TradeContext.HostCode = '8813' 
                    TradeContext.ACUR     = '1'
                    TradeContext.RCCSMCD  = PL_RCCSMCD_DZBJ
                    TradeContext.SBAC     = wtrbka_record['BESBNO'] + PL_ACC_NXYWZ    #借方账号
                    TradeContext.SBAC     = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25) 
                    TradeContext.ACNM     = '农信银往账'
                    TradeContext.RBAC     = wtrbka_record['BESBNO'] + PL_ACC_NXYDQSWZ #贷方账号 
                    TradeContext.RBAC     = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
                    TradeContext.OTNM     = '农信银待清算往账'
                    TradeContext.OCCAMT   = str(wtrbka_record['OCCAMT'])
                    TradeContext.PKFG     = 'W'
                    TradeContext.CTFG     = '9'
                
            else:
                return AfaFlowControl.ExitThisFlow('A099','原交易交易代码非法')
                
            #=====增加原交易的状态--结转====
            if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_TRAS,PL_BDWFLG_WAIT):
                AfaDBFunc.RollbackSql()
                return AfaFlowControl.ExitThisFlow('A099','增加原交易的状态--结转，失败')
            else:
                AfaDBFunc.CommitSql()  
                
            #=====调用主机交易====
            rccpsHostFunc.CommHost( TradeContext.HostCode )
            
            #=====判断主机交易是否成功====
            if(TradeContext.errorCode != '0000'):
                AfaLoggerFunc.tradeInfo("主机交易失败")
                #=====更改原交易状态====
                state_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN,'BCSTAT':PL_BCSTAT_TRAS,'BDWFLG':PL_BDWFLG_FAIL}
                state_dict['STRINFO'] = TradeContext.errorMsg
                if not rccpsState.setTransState(state_dict):
                    AfaDBFunc.RollbackSql()
                    return AfaFlowControl.ExitThisFlow('A099','更改原交易状态失败')
                else:
                    AfaDBFunc.CommitSql()   
                    
                return AfaFlowControl.ExitThisFlow('A099','主机记账失败')
                
            else:
                AfaLoggerFunc.tradeInfo('主机记账成功')
                #=====更改原交易状态====
                state_dict = {}
                state_dict['BJEDTE'] = TradeContext.BJEDTE
                state_dict['BSPSQN'] = TradeContext.BSPSQN
                state_dict['BCSTAT'] = PL_BCSTAT_TRAS
                state_dict['BDWFLG'] = PL_BDWFLG_SUCC
                if(TradeContext.existVariable("SBAC")):
                    state_dict['SBAC'] = TradeContext.SBAC
                if(TradeContext.existVariable("RBAC")):
                    state_dict['RBAC'] = TradeContext.RBAC
                state_dict['STRINFO'] = '主机成功'
                if(TradeContext.existVariable('TRDT')):
                    state_dict['TRDT'] = TradeContext.TRDT
                if(TradeContext.existVariable('TLSQ')):
                    state_dict['TLSQ'] = TradeContext.TLSQ
                if not rccpsState.setTransState(state_dict):
                    AfaDBFunc.RollbackSql()
                    return AfaFlowControl.ExitThisFlow('A099','更改原交易状态失败')
                else:
                    AfaDBFunc.CommitSql()   
                     
        else:
            return AfaFlowControl.ExitThisFlow('A009','原交易不能进行清算调整')
        
    else:
        AfaLoggerFunc.tradeInfo('<<<<<<业务为来账')
        autopay = 0    
        auto    = 0
        hcac    = 0   
        canc    = 0
        cancel  = 0
        #=====查询是否有记账成功的状态====
        sstlog_list = []
        if rccpsState.getTransStateSetm(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_AUTO,PL_BDWFLG_SUCC,sstlog_list):
            auto = len(sstlog_list)
        sstlog_list = []
        if rccpsState.getTransStateSetm(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_AUTOPAY,PL_BDWFLG_SUCC,sstlog_list):
            autopay = len(sstlog_list)      
        #=====查询是否有抹账的状态====
        sstlog_list = []
        if rccpsState.getTransStateSetm(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_HCAC,PL_BDWFLG_SUCC,sstlog_list):
            hcac = len(sstlog_list)
        #=====查询是否有冲销的状态====
        sstlog_list = []
        if rccpsState.getTransStateSetm(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_CANC,PL_BDWFLG_SUCC,sstlog_list):
            canc = len(sstlog_list)
        #=====查询是否有冲正的状态====
        ssltog_list = []
        if rccpsState.getTransStateSetm(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_CANCEL,PL_BDWFLG_SUCC,sstlog_list):
            cancel = len(sstlog_list)
            
        #=====判断原业务是否需要进行清算状态调整====
        AfaLoggerFunc.tradeInfo("判断原业务是否需要进行清算状态调整")
        if((auto + autopay) - (hcac + canc + cancel) >= 0):
            AfaLoggerFunc.tradeInfo("原业务需要进行清算状态调整")
            
            TradeContext.BETELR   = PL_BETELR_AUTO
            TradeContext.BRSFLG   = wtrbka_record['BRSFLG']    
            TradeContext.CHRGTYP  = wtrbka_record['CHRGTYP']
            TradeContext.BESBNO   = wtrbka_record['BESBNO']  
            #=====卡折存现/本转异地====
            if(wtrbka_record['TRCCO'] in ('3000002','3000003','3000004','3000005')):
                AfaLoggerFunc.tradeInfo('卡折存现/本转异地')
                TradeContext.HostCode = '8813' 
                TradeContext.ACUR     = '1'
                TradeContext.RCCSMCD  = PL_RCCSMCD_DZBJ
                TradeContext.SBAC     = wtrbka_record['BESBNO'] + PL_ACC_NXYLZ
                TradeContext.SBAC     = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25) 
                TradeContext.ACNM     = '农信银来账'
                TradeContext.RBAC     = wtrbka_record['BESBNO'] + PL_ACC_NXYDQSLZ 
                TradeContext.RBAC     = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
                TradeContext.OTNM     = '农信银待清算来账'
                TradeContext.OCCAMT   = str(wtrbka_record['OCCAMT'])
                TradeContext.PKFG     = 'W'
                TradeContext.CTFG     = '7'
            
            #=====卡折取现/异地转本地====    
            elif(wtrbka_record['TRCCO'] in ('3000102','3000103','3000104','3000105')):
                AfaLoggerFunc.tradeInfo('卡折存现/本转异地')
                TradeContext.HostCode = '8813'
                TradeContext.ACUR     = '1'
                TradeContext.RCCSMCD  = PL_RCCSMCD_DZBJ
                TradeContext.SBAC     = wtrbka_record['BESBNO'] + PL_ACC_NXYDQSLZ 
                TradeContext.SBAC     = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25) 
                TradeContext.ACNM     = '农信银待清算来账'
                TradeContext.RBAC     = wtrbka_record['BESBNO'] + PL_ACC_NXYLZ 
                TradeContext.RBAC     = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
                TradeContext.OTNM     = '农信银来账'
                TradeContext.OCCAMT   = str(wtrbka_record['OCCAMT'] + wtrbka_record['CUSCHRG'])
                TradeContext.PKFG     = 'W'
                TradeContext.CTFG     = '9'
                
            else:
                return AfaFlowControl.ExitThisFlow('A099','原交易交易代码非法')
                
            #=====增加原交易的状态--结转====
            if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_TRAS,PL_BDWFLG_WAIT):
                AfaDBFunc.RollbackSql()
                return AfaFlowControl.ExitThisFlow('A099','增加原交易的状态--结转，失败')
            else:
                AfaDBFunc.CommitSql()  
                
            #=====调用主机交易====
            rccpsHostFunc.CommHost( TradeContext.HostCode )
            
            #=====判断主机交易是否成功====
            if(TradeContext.errorCode != '0000'):
                AfaLoggerFunc.tradeInfo("主机交易失败")
                #=====更改原交易状态====
                state_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN,'BCSTAT':PL_BCSTAT_TRAS,'BDWFLG':PL_BDWFLG_FAIL}
                state_dict['STRINFO'] = TradeContext.errorMsg
                if not rccpsState.setTransState(state_dict):
                    AfaDBFunc.RollbackSql()
                    return AfaFlowControl.ExitThisFlow('A099','更改原交易状态失败')
                else:
                    AfaDBFunc.CommitSql()   
                    
                return AfaFlowControl.ExitThisFlow('A099','主机记账失败')
                
            else:
                AfaLoggerFunc.tradeInfo('主机记账成功')
                #=====更改原交易状态====
                state_dict = {}
                state_dict['BJEDTE'] = TradeContext.BJEDTE
                state_dict['BSPSQN'] = TradeContext.BSPSQN
                state_dict['BCSTAT'] = PL_BCSTAT_TRAS
                state_dict['BDWFLG'] = PL_BDWFLG_SUCC
                state_dict['STRINFO'] = '主机成功'
                if(TradeContext.existVariable("SBAC")):
                    state_dict['SBAC'] = TradeContext.SBAC
                if(TradeContext.existVariable("RBAC")):
                    state_dict['RBAC'] = TradeContext.RBAC
                if(TradeContext.existVariable('TRDT')):
                    state_dict['TRDT'] = TradeContext.TRDT
                if(TradeContext.existVariable('TLSQ')):
                    state_dict['TLSQ'] = TradeContext.TLSQ
                if not rccpsState.setTransState(state_dict):
                    AfaDBFunc.RollbackSql()
                    return AfaFlowControl.ExitThisFlow('A099','更改原交易状态失败')
                else:
                    AfaDBFunc.CommitSql()   
            
        else:
            return AfaFlowControl.ExitThisFlow('A009','原交易不能进行清算调整')
       
    #=====给修改字典赋值====
    update_dict = {}
    update_dict = {'ISDEAL':'1','NOTE3':'此笔错账已结转'}
    where_dict = {}               
    where_dict = {'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO,\
                  'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}                                               

    #=====修改数据库中的数据====
    AfaLoggerFunc.tradeInfo("通存通兑错帐处理标识修改")
    res = rccpsDBTrcc_tddzcz.updateCmt(update_dict,where_dict)
    if( res == -1 ):
        return AfaFlowControl.ExitThisFlow('A099','修改通存通兑错帐处理标识失败')
    elif( res == 0 ):
        return AfaFlowControl.ExitThisFlow('A099','交易记录不存在')
        
    #=====向下发的通知表中插入数据====
    AfaLoggerFunc.tradeInfo("<<<<<<向通知表中插入数据")
    insert_dict = {}
    insert_dict['NOTDAT']  = AfaUtilTools.GetHostDate( )
    insert_dict['BESBNO']  = wtrbka_record['BESBNO']
    if(wtrbka_record['BRSFLG'] == PL_BRSFLG_RCV):
        insert_dict['STRINFO'] = "此笔错账["+wtrbka_record['BSPSQN']+"]["+wtrbka_record['BJEDTE']+"]已做手工结转处理"
    else:
        insert_dict['STRINFO'] = "此笔错账["+wtrbka_record['BSPSQN']+"]["+wtrbka_record['BJEDTE']+"]已做手工结转处理 请用8522补打往账凭证"
    if not rccpsDBTrcc_notbka.insertCmt(insert_dict):
        return AfaFlowControl.ExitThisFlow('S999','向下发的通知表中插入数据失败')
    AfaLoggerFunc.tradeInfo("<<<<<<向通知表中插入数据成功")
    
    #=====给输出接口赋值====
    TradeContext.errorCode = "0000"
    TradeContext.errorMsg  = "修改通存通兑错帐处理标识成功"
    TradeContext.ISDEAL    = '1'
#    TradeContext.TLSQ      = TradeContext.TLSQ
#    TradeContext.RBSQ      = TradeContext.RBSQ
#    TradeContext.TRDT      = TradeContext.TRDT

    AfaLoggerFunc.tradeInfo( '***农信银系统: 往账.本地类操作交易[RCC001_8591]通存通兑错帐处理标识维护退出***' )
    
    return True      