# -*- coding: gbk -*-
##################################################################
#   农信银.通存通兑往账交易.通存通兑差错账补记
#=================================================================
#   程序文件:   TRCC001_8572.py
#   修改时间:   2008-12-09
#   作者：      潘广通
##################################################################

import TradeContext,AfaFlowControl,AfaLoggerFunc,AfaUtilTools,rccpsState,AfaDBFunc,rccpsEntriesErr,rccpsHostFunc,rccpsFunc,rccpsGetFunc,rccpsState
import rccpsDBTrcc_tddzcz,rccpsDBTrcc_wtrbka,rccpsDBTrcc_sstlog,rccpsDBTrcc_tddzmx,rccpsDBTrcc_notbka,rccpsDBTrcc_spbsta
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("'***农信银系统：通存通兑往账交易.差错账补记[8572] 进入")
    
    AfaLoggerFunc.tradeInfo("<<<<<<<个性化处理(本地操作) 进入")
    #=====校验变量的合法性====
    AfaLoggerFunc.tradeInfo("<<<<<<校验变量的合法性")   
    if not TradeContext.existVariable("SNDBNKCO"):
        return AfaFlowControl.ExitThisFlow('A099','没有发起行号')
        
    if not TradeContext.existVariable("TRCNO"):
        return AfaFlowControl.ExitThisFlow('A099','没有交易流水号')
        
    if not TradeContext.existVariable("TRCDAT"):
        return AfaFlowControl.ExitThisFlow('A099','没有委托日期')
        
    AfaLoggerFunc.tradeInfo("<<<<<<校验变量的合法性结束")
    
    #=====生成RBSQ,FEDT,BJEDTE,NCCworkDate,BSPSQN====
    TradeContext.FEDT=AfaUtilTools.GetHostDate( )      #FEDT
    
    TradeContext.BJEDTE=AfaUtilTools.GetHostDate( )    #BJEDTE 
    
    if not rccpsFunc.GetNCCDate( ) :                   #NCCworkDate
        raise AfaFlowControl.flowException( )
    
    if rccpsGetFunc.GetRBSQ(PL_BRSFLG_RCV) == -1 :     #RBSQ
        return AfaFlowControl.ExitThisFlow('S999','重新生成前置流水号失败,抛弃报文')
        
    if rccpsGetFunc.GetSerialno(PL_BRSFLG_RCV) == -1 : #BSPSQN
        raise AfaFlowControl.flowException( )
        
    #=====判断原业务是来账还是往账====
    AfaLoggerFunc.tradeInfo("<<<<<<判断原业务的往来标示")
    if(TradeContext.SNDBNKCO == '1340000008'):
        AfaLoggerFunc.tradeInfo("<<<<<<原业务为往账")
        #=====查询原业务信息====
        where_dict = {}
        where_dict = {'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO}
        wtrbka_record_dict = rccpsDBTrcc_wtrbka.selectu(where_dict)
        if(wtrbka_record_dict == None):
            return AfaFlowControl.ExitThisFlow('A099','查询通存通兑登记簿失败')
        
        elif(len(wtrbka_record_dict) == 0):
            return AfaFlowControl.ExitThisFlow('A099','查询通存通兑登记簿为空')
            
        else:
            AfaLoggerFunc.tradeInfo("<<<<<<查询原业务信息成功")
            
        #=====查询错账登记簿====
        where_dict = {}
        where_dict = {'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO}
        tddzcz_record_dict = rccpsDBTrcc_tddzcz.selectu(where_dict)
        if(tddzcz_record_dict == None):
            return AfaFlowControl.ExitThisFlow('A099','查询错账登记簿失败')
        
        elif(len(tddzcz_record_dict) == 0):
            AfaLoggerFunc.tradeInfo("查询错账登记簿结果为空,应向其中插入相应的记录")
            #=====给插入错账登记簿的字典赋值====
            insert_dict = {}           
            insert_dict['NCCWKDAT']   = wtrbka_record_dict['NCCWKDAT']
            insert_dict['SNDBNKCO']   = wtrbka_record_dict['SNDBNKCO']
            insert_dict['TRCDAT']     = wtrbka_record_dict['TRCDAT']
            insert_dict['TRCNO']      = wtrbka_record_dict['TRCNO']
            insert_dict['RCVBNKCO']   = wtrbka_record_dict['RCVBNKCO']
            insert_dict['SNDMBRCO']   = wtrbka_record_dict['SNDMBRCO']
            insert_dict['RCVMBRCO']   = wtrbka_record_dict['RCVMBRCO']
            insert_dict['TRCCO']      = wtrbka_record_dict['TRCCO']
            if(wtrbka_record_dict['DCFLG'] == '0'):
                insert_dict['DCFLG'] = '1'
            else:
                insert_dict['DCFLG'] = '2'
            insert_dict['PYRACC']     = wtrbka_record_dict['PYRACC']
            insert_dict['PYEACC']     = wtrbka_record_dict['PYEACC']
            insert_dict['CUR']        = 'CNY'
            insert_dict['OCCAMT']     = wtrbka_record_dict['OCCAMT']
            insert_dict['LOCOCCAMT']  = wtrbka_record_dict['OCCAMT']
            if(wtrbka_record_dict['TRCCO'] in ('3000102','3000103','3000104','3000105') and wtrbka_record_dict['CHRGTYP'] == '1'):
                insert_dict['CUSCHRG']    = wtrbka_record_dict['CUSCHRG']
                insert_dict['LOCCUSCHRG'] = wtrbka_record_dict['CUSCHRG']
            else:
                insert_dict['CUSCHRG']    = 0.00
                insert_dict['LOCCUSCHRG'] = 0.00
            insert_dict['ORTRCNO']    = ""
            insert_dict['BJEDTE']     = wtrbka_record_dict['BJEDTE']
            insert_dict['BSPSQN']     = wtrbka_record_dict['BSPSQN']
            insert_dict['EACTYP']     = '02'
            insert_dict['EACINF']     = '中心有成员行无'
            insert_dict['LOCEACTYP']  = '03'
            insert_dict['LOCEACINF']  = '往账中心清算，行内未清算'
            insert_dict['ISDEAL']     = '0'
            insert_dict['NOTE1']      = ""
            insert_dict['NOTE2']      = ""
            insert_dict['NOTE3']      = ""
            insert_dict['NOTE4']      = ""
            
            #=====向错账登记簿中补记此笔交易====
            if not rccpsDBTrcc_tddzcz.insertCmt(insert_dict):
                return AfaFlowControl.ExitThisFlow('A099','向错账登记簿中补记交易失败')
                
            #=====补查错账登记簿，将刚插入的数据查出来====
            where_dict = {}
            where_dict = {'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO}
            tddzcz_record_dict = rccpsDBTrcc_tddzcz.selectu(where_dict)
            if(tddzcz_record_dict == None):
                return AfaFlowControl.ExitThisFlow('A099','查询错账登记簿失败')
            elif(len(tddzcz_record_dict) == 0):
                return AfaFlowControl.ExitThisFlow('A099','查询通错账登记簿结果为空')
            else:
                AfaLoggerFunc.tradeInfo("<<<<<<补查错账登记簿成功")
                 
        else:
            AfaLoggerFunc.tradeInfo("<<<<<<查询错账登记簿成功")
                
    else:
        AfaLoggerFunc.tradeInfo("<<<<<<原业务为来账")
        #=====查询对账明细登记簿====
        AfaLoggerFunc.tradeInfo("<<<<<<开始查询对账明细登记簿")
        where_dict = {}
        where_dict = {'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO}
        tddzmx_record_dict = rccpsDBTrcc_tddzmx.selectu(where_dict)
        if(tddzmx_record_dict == None):
            return AfaFlowControl.ExitThisFlow('A099','查询对账明细登记簿失败')
            
        elif(len(tddzmx_record_dict) == 0):
            return AfaFlowControl.ExitThisFlow('A099','查询对账明细登记簿为空')
            
        else:
            AfaLoggerFunc.tradeInfo("<<<<<<查询对账明细登记簿成功")
        
        #=====查询错账登记簿====
        AfaLoggerFunc.tradeInfo("<<<<<<开始查询错账登记簿")
        where_dict = {}
        where_dict = {'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO}
        tddzcz_record_dict = rccpsDBTrcc_tddzcz.selectu(where_dict)
        if(tddzcz_record_dict == None):
            return AfaFlowControl.ExitThisFlow('A099','查询错账登记簿失败')
        
        elif(len(tddzcz_record_dict) == 0):
            AfaLoggerFunc.tradeInfo("查询错账登记簿结果为空,应向其中插入相应的记录")
            #=====给插入错账登记簿的字典赋值====
            insert_dict = {}
            insert_dict['NCCWKDAT']   = tddzmx_record_dict['NCCWKDAT']
            insert_dict['SNDBNKCO']   = tddzmx_record_dict['SNDBNKCO']
            insert_dict['TRCDAT']     = tddzmx_record_dict['TRCDAT']
            insert_dict['TRCNO']      = tddzmx_record_dict['TRCNO']
            insert_dict['RCVBNKCO']   = tddzmx_record_dict['RCVBNKCO']
            insert_dict['SNDMBRCO']   = tddzmx_record_dict['SNDMBRCO']
            insert_dict['RCVMBRCO']   = tddzmx_record_dict['RCVMBRCO']
            insert_dict['TRCCO']      = tddzmx_record_dict['TRCCO']
            insert_dict['DCFLG']      = tddzmx_record_dict['DCFLG']
            insert_dict['PYRACC']     = tddzmx_record_dict['PYRACC']
            insert_dict['PYEACC']     = tddzmx_record_dict['PYEACC']
            insert_dict['CUR']        = tddzmx_record_dict['CUR']
            insert_dict['OCCAMT']     = tddzmx_record_dict['OCCAMT']
            insert_dict['LOCOCCAMT']  = tddzmx_record_dict['OCCAMT']
            insert_dict['CUSCHRG']    = tddzmx_record_dict['CUSCHRG']
            insert_dict['LOCCUSCHRG'] = tddzmx_record_dict['CUSCHRG']
            insert_dict['ORTRCNO']    = ""
            insert_dict['BJEDTE']     = tddzmx_record_dict['BJEDTE']
            insert_dict['BSPSQN']     = tddzmx_record_dict['BSPSQN']
            insert_dict['EACTYP']     = "02"
            insert_dict['EACINF']     = "中心有成员行无"
            insert_dict['LOCEACTYP']  = "08"
            insert_dict['LOCEACINF']  = "来账中心清算，行内未清算"
            insert_dict['ISDEAL']     = "0"
            insert_dict['NOTE1']      = ""
            insert_dict['NOTE2']      = ""
            insert_dict['NOTE3']      = ""
            insert_dict['NOTE4']      = ""
            
            #=====向错账登记簿中补记此笔交易====
            if not rccpsDBTrcc_tddzcz.insertCmt(insert_dict):
                return AfaFlowControl.ExitThisFlow('A099','向错账登记簿中补记交易失败')
                
            #=====补查错账登记簿，将刚插入的数据查出来====
            where_dict = {}
            where_dict = {'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO}
            tddzcz_record_dict = rccpsDBTrcc_tddzcz.selectu(where_dict)
            if(tddzcz_record_dict == None):
                return AfaFlowControl.ExitThisFlow('A099','查询错账登记簿失败')
            elif(len(tddzcz_record_dict) == 0):
                return AfaFlowControl.ExitThisFlow('A099','查询通错账登记簿结果为空')
            else:
                AfaLoggerFunc.tradeInfo("<<<<<<补查错账登记簿成功")
             
        else:
            AfaLoggerFunc.tradeInfo("<<<<<<查询错账登记簿成功")
             
        AfaLoggerFunc.tradeInfo("<<<<<<结束查询错账明细登记簿")
        
        #=====查询原交易信息====
        AfaLoggerFunc.tradeInfo("<<<<<<开始查询原交易信息")
        where_dict = {}
        where_dict = {'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO}
        wtrbka_record_dict = rccpsDBTrcc_wtrbka.selectu(where_dict)
        if(wtrbka_record_dict == None):
            return AfaFlowControl.ExitThisFlow('A099','查询通存通兑业务登记簿失败')
        
        elif(len(wtrbka_record_dict) == 0):    #通存通兑登记簿结果为空，应向其中插入相应记录
            AfaLoggerFunc.tradeInfo("<<<<<<通存通兑业务登记簿结果为空")
            #=====开始登记通存通兑业务登记簿====
            AfaLoggerFunc.tradeInfo("<<<<<<开始登记通存通兑业务登记簿")
            
            #=====调用主机交易得到机构号====
            AfaLoggerFunc.tradeInfo("<<<<<<查询账户开户机构")
            TradeContext.HostCode = '8810'
            if(tddzmx_record_dict['TRCCO'] in ('3000002','3000003','3000004','3000005')):
                TradeContext.ACCNO = tddzmx_record_dict['PYEACC']
            else:
                TradeContext.ACCNO = tddzmx_record_dict['PYRACC']
            
            rccpsHostFunc.CommHost( TradeContext.HostCode )
            if(TradeContext.errorCode != '0000'):
                return AfaFlowControl.ExitThisFlow('A099','查询账户开户行信息失败')
            
            AfaLoggerFunc.tradeInfo("<<<<<<查询账户开户信息成功")
            
            #=====给插入通存通兑业务登记簿的字典赋值====
            insert_dict = {}
            insert_dict['BJEDTE']     = tddzmx_record_dict['BJEDTE']
            insert_dict['BSPSQN']     = tddzmx_record_dict['BSPSQN']
            if(tddzmx_record_dict['SNDMBRCO'] == '1340000008'):
                insert_dict['BRSFLG'] = PL_BRSFLG_SND
            else:
                insert_dict['BRSFLG'] = PL_BRSFLG_RCV
            insert_dict['BESBNO']     = TradeContext.ACCSO
            insert_dict['BEACSB']     = ""
            insert_dict['BETELR']     = PL_BETELR_AUTO
            insert_dict['BEAUUS']     = ""
            insert_dict['BEAUPS']     = ""
            insert_dict['TERMID']     = ""
            insert_dict['BBSSRC']     = ""
            insert_dict['DASQ']       = ""
            insert_dict['DCFLG']      = tddzmx_record_dict['DCFLG']
            if(tddzmx_record_dict['TRCCO'] in ('3000002','3000004')):
                insert_dict['OPRNO']  = PL_TDOPRNO_TC
            elif(tddzmx_record_dict['TRCCO'] in ('3000102','3000104')):
                insert_dict['OPRNO']  = PL_TDOPRNO_TD
            elif(tddzmx_record_dict['TRCCO'] in ('3000003','3000005')):
                insert_dict['OPRNO']  = PL_TDOPRNO_BZY
            else:
                insert_dict['OPRNO']  = PL_TDOPRNO_YZB
            insert_dict['OPRATTNO']   = ""
            insert_dict['NCCWKDAT']   = TradeContext.NCCworkDate
            insert_dict['TRCCO']      = tddzmx_record_dict['TRCCO']
            insert_dict['TRCDAT']     = tddzmx_record_dict['TRCDAT']
            insert_dict['TRCNO']      = tddzmx_record_dict['TRCNO']
            insert_dict['MSGFLGNO']   = tddzmx_record_dict['MSGFLGNO']
            insert_dict['COTRCDAT']   = ""
            insert_dict['COTRCNO']    = ""
            insert_dict['COMSGFLGNO'] = ""
            insert_dict['SNDMBRCO']   = tddzmx_record_dict['SNDMBRCO']
            insert_dict['RCVMBRCO']   = tddzmx_record_dict['RCVMBRCO']
            insert_dict['SNDBNKCO']   = tddzmx_record_dict['SNDBNKCO']
            insert_dict['SNDBNKNM']   = tddzmx_record_dict['SNDBNKNM']
            insert_dict['RCVBNKCO']   = tddzmx_record_dict['RCVBNKCO']
            insert_dict['RCVBNKNM']   = tddzmx_record_dict['RCVBNKNM']
            insert_dict['CUR']        = tddzmx_record_dict['CUR']
            insert_dict['OCCAMT']     = tddzmx_record_dict['OCCAMT']
            if(tddzmx_record_dict['CUSCHRG'] == 0.00):
                insert_dict['CHRGTYP']= PL_CHRG_CASH
            else:
                insert_dict['CHRGTYP']= PL_CHRG_TYPE  
            insert_dict['LOCCUSCHRG'] = ""
            insert_dict['CUSCHRG']    = tddzmx_record_dict['CUSCHRG']
            insert_dict['PYRTYP']     = ""
            insert_dict['PYRACC']     = tddzmx_record_dict['PYRACC']
            insert_dict['PYRNAM']     = ""
            insert_dict['PYRADDR']    = ""
            insert_dict['PYETYP']     = ""
            insert_dict['PYEACC']     = tddzmx_record_dict['PYEACC']
            insert_dict['PYENAM']     = ""
            insert_dict['PYEADDR']    = ""
            insert_dict['STRINFO']    = tddzmx_record_dict['STRINFO']
            insert_dict['CERTTYPE']   = ""
            insert_dict['CERTNO']     = ""
            insert_dict['BNKBKNO']    = ""
            insert_dict['BNKBKBAL']   = ""
            
            if not rccpsDBTrcc_wtrbka.insertCmt(insert_dict):
                return AfaFlowControl.ExitThisFlow('A099','登记通存通兑业务登记簿失败')
            
            AfaLoggerFunc.tradeInfo("<<<<<<结束登记通存通兑业务登记簿")
            
            #=====补查通存通兑业务登记簿，将刚才插入的数据查出来====
            where_dict = {}
            where_dict = {'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO}
            wtrbka_record_dict = rccpsDBTrcc_wtrbka.selectu(where_dict)
            if(wtrbka_record_dict == None):
                return AfaFlowControl.ExitThisFlow('A099','查询通存通兑业务登记簿失败')
            elif(len(wtrbka_record_dict) == 0):
                return AfaFlowControl.ExitThisFlow('A099','查询通存通兑业务登记簿结果为空')
            else:
                AfaLoggerFunc.tradeInfo("<<<<<<补查通存通兑业务登记簿成功")
            
        else:
            AfaLoggerFunc.tradeInfo("<<<<<<查询通存通兑业务登记簿成功")
        
    #=====判断此笔业务是否已经处理====
    if(tddzcz_record_dict['ISDEAL'] == PL_ISDEAL_ISDO):
        return AfaFlowControl.ExitThisFlow('A099','此笔账务已经处理过')
        
    #=====开始行内补记====
    AfaLoggerFunc.tradeInfo("<<<<<<开始行内补记")
    #=====判断原交易的往来标示====
    AfaLoggerFunc.tradeInfo("<<<<<<判断原交易的往来标示")
    if(wtrbka_record_dict['BRSFLG'] == PL_BRSFLG_RCV):
        AfaLoggerFunc.tradeInfo("<<<<<<原交易为来账")
        
#        if(TradeContext.existVariable("BSPSQN")):
#            TradeContext.BSPSQN = wtrbka_record_dict['BSPSQN']    
        TradeContext.BESBNO   = wtrbka_record_dict['BESBNO']
        TradeContext.BRSFLG   = wtrbka_record_dict['BRSFLG']
        TradeContext.CHRGTYP  = wtrbka_record_dict['CHRGTYP']
        TradeContext.BETELR   = PL_BETELR_AUTO
        input_dict = {}
        input_dict['FEDT']    = TradeContext.FEDT
        input_dict['RBSQ']    = TradeContext.RBSQ
        input_dict['PYRACC']  = wtrbka_record_dict['PYRACC']
        input_dict['PYRNAM']  = wtrbka_record_dict['PYRNAM']
        input_dict['PYEACC']  = wtrbka_record_dict['PYEACC']
        input_dict['PYENAM']  = wtrbka_record_dict['PYENAM']
        input_dict['CHRGTYP'] = wtrbka_record_dict['CHRGTYP']
        input_dict['OCCAMT']  = wtrbka_record_dict['OCCAMT']
        input_dict['CUSCHRG'] = wtrbka_record_dict['CUSCHRG']
        
        if(wtrbka_record_dict['TRCCO'] in ('3000002','3000004')):  
            AfaLoggerFunc.tradeDebug("<<<<<<卡折现金通存来账记账")
            input_dict['RCCSMCD'] = PL_RCCSMCD_XJTCLZ
            rccpsEntriesErr.KZTCLZJZ(input_dict)
            
        elif(wtrbka_record_dict['TRCCO'] in ('3000003','3000005')):
            AfaLoggerFunc.tradeDebug("<<<<<<卡折本转异来账记账")
            input_dict['RCCSMCD'] = PL_RCCSMCD_BZYLZ
            rccpsEntriesErr.KZBZYLZJZ(input_dict)
            
        elif(wtrbka_record_dict['TRCCO'] in ('3000102','3000104')):
            AfaLoggerFunc.tradeDebug("<<<<<<卡折现金通兑来账记账")
            input_dict['RCCSMCD'] = PL_RCCSMCD_XJTDLZ
            rccpsEntriesErr.KZTDLZJZ(input_dict)
            
        elif(wtrbka_record_dict['TRCCO'] in ('3000103','3000105')):
            AfaLoggerFunc.tradeDebug("<<<<<<卡折异转本来账记账")
            input_dict['RCCSMCD'] = PL_RCCSMCD_YZBLZ
            rccpsEntriesErr.KZYZBLZJZ(input_dict)
            
        else:
            return AfaFlowControl.ExitThisFlow('A099','交易代码非法')
    
    elif(wtrbka_record_dict['BRSFLG'] == PL_BRSFLG_SND):
        AfaLoggerFunc.tradeInfo("<<<<<<原交易为往账")
         
#        if(TradeContext.existVariable("BSPSQN")):
#            TradeContext.BSPSQN = wtrbka_record_dict['BSPSQN']
        TradeContext.BESBNO   = wtrbka_record_dict['BESBNO']   
        TradeContext.CHRGTYP  = wtrbka_record_dict['CHRGTYP']
        TradeContext.BRSFLG   = wtrbka_record_dict['BRSFLG']    
        TradeContext.BETELR   = PL_BETELR_AUTO
        input_dict = {}
        input_dict['FEDT']    = TradeContext.FEDT
        input_dict['RBSQ']    = TradeContext.RBSQ
        input_dict['PYRACC']  = wtrbka_record_dict['PYRACC']
        input_dict['PYRNAM']  = wtrbka_record_dict['PYRNAM']
        input_dict['PYEACC']  = wtrbka_record_dict['PYEACC']
        input_dict['PYENAM']  = wtrbka_record_dict['PYENAM']
        input_dict['CHRGTYP'] = wtrbka_record_dict['CHRGTYP']
        input_dict['OCCAMT']  = wtrbka_record_dict['OCCAMT']
        input_dict['CUSCHRG'] = wtrbka_record_dict['CUSCHRG']
        
        if(wtrbka_record_dict['TRCCO'] in ('3000002','3000004')):  
            AfaLoggerFunc.tradeDebug("<<<<<<卡折现金通存往账记账")
            input_dict['RCCSMCD'] = PL_RCCSMCD_XJTCWZ
            rccpsEntriesErr.KZTCWZJZ(input_dict)
            
        elif(wtrbka_record_dict['TRCCO'] in ('3000003','3000005')):
            AfaLoggerFunc.tradeDebug("<<<<<<卡折本转异往账记账")
            input_dict['RCCSMCD'] = PL_RCCSMCD_BZYWZ
            rccpsEntriesErr.KZBZYWZJZ(input_dict)
            
        elif(wtrbka_record_dict['TRCCO'] in ('3000102','3000104')):
            AfaLoggerFunc.tradeDebug("<<<<<<卡折现金通兑往账记账")
            input_dict['RCCSMCD'] = PL_RCCSMCD_XJTDWZ
            rccpsEntriesErr.KZTDWZJZ(input_dict)
            
        elif(wtrbka_record_dict['TRCCO'] in ('3000103','3000105')):
            AfaLoggerFunc.tradeDebug("<<<<<<卡折异转本往账记账")
            input_dict['RCCSMCD'] = PL_RCCSMCD_YZBWZ
            rccpsEntriesErr.KZYZBWZJZ(input_dict)
        
        else:
            return AfaFlowControl.ExitThisFlow('A099','交易代码非法')
        
    else:
        return AfaFlowControl.ExitThisFlow('A099','往来标示非法')
        
    #=====主机前设置原交易的状态====
    bcstat = ''    #状态变量
    if(wtrbka_record_dict['BRSFLG'] == PL_BRSFLG_SND):    #往账
        bcstat = PL_BCSTAT_ACC
    elif(wtrbka_record_dict['BRSFLG'] == PL_BRSFLG_RCV and wtrbka_record_dict['TRCCO'] in ('3000002','3000003','3000004','3000005')):    #来账通存
        bcstat = PL_BCSTAT_AUTO
    else:    #来账通兑
        bcstat = PL_BCSTAT_AUTOPAY
    
    #=====判断原交易是否有成功的账务状态====
    AfaLoggerFunc.tradeInfo("<<<<<<判断原交易是是否有成功的交易状态")
    isaccount = 0    #调用主机交易标示，0不调用，1调用
    acc = 0    
    hcac = 0    
    canc = 0
    cancel = 0
    if(wtrbka_record_dict['BRSFLG'] == PL_BRSFLG_SND):
        #=====原业务为往账====
        #=====查询是否有记账成功的状态====
        sstlog_list = []
        if rccpsState.getTransStateSetm(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],PL_BCSTAT_ACC,PL_BDWFLG_SUCC,sstlog_list):
            acc = len(sstlog_list)
        #=====查询是否有抹账的状态====
        sstlog_list = []
        if rccpsState.getTransStateSetm(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],PL_BCSTAT_HCAC,PL_BDWFLG_SUCC,sstlog_list):
            hcac = len(sstlog_list)
        #=====查询是否有冲销的状态====
        sstlog_list = []
        if rccpsState.getTransStateSetm(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],PL_BCSTAT_CANC,PL_BDWFLG_SUCC,sstlog_list):
            canc = len(sstlog_list)
        #=====查询是否有冲正的状态====
        ssltog_list = []
        if rccpsState.getTransStateSetm(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],PL_BCSTAT_CANCEL,PL_BDWFLG_SUCC,sstlog_list):
            cancel = len(sstlog_list)
        
        if(acc - (hcac + canc + cancel) <= 0):
            isaccount = 1
            
    else:
        #======原业务为来账====
        stat_dict = {}
        res = rccpsState.getTransStateCur(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],stat_dict)
        if(res == False):
            return AfaFlowControl.ExitThisFlow('A099','查询业务的当前状态失败')
        else:
            AfaLoggerFunc.tradeInfo("查询业务当前状态成功")
            
        if(stat_dict['BCSTAT'] in (PL_BCSTAT_AUTO,PL_BCSTAT_AUTOPAY) and stat_dict['BDWFLG'] == PL_BDWFLG_SUCC):
            isaccount = 0
        else:
            isaccount = 1
            
    AfaLoggerFunc.tradeInfo("<<<<<<结束判断原交易是是否有成功的交易状态")
            
    #=====判断业务是否需要进行主机记账====
    if(isaccount == 0):
        return AfaFlowControl.ExitThisFlow('S999','原业务已记账，禁止提交')
    
    #=====主机前设置原交易状态====  
    AfaLoggerFunc.tradeInfo("<<<<<<主机前设置原交易状态")  
    if not rccpsState.newTransState(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],bcstat,PL_BDWFLG_WAIT):
        return AfaFlowControl.ExitThisFlow('S999','设置业务状态为记账处理中异常')
    else:
        AfaDBFunc.CommitSql()
        
    #=====开始调用主机交易====
    AfaLoggerFunc.tradeInfo("<<<<<<开始调用主机交易")
    rccpsHostFunc.CommHost( TradeContext.HostCode )
    AfaLoggerFunc.tradeInfo("<<<<<<结束调用主机交易")   
        
    AfaLoggerFunc.tradeInfo("<<<<<<结束行内补记")
    
    #=====给状态字典赋值====
    state_dict = {}
    state_dict['BJEDTE'] = wtrbka_record_dict['BJEDTE']
    state_dict['BSPSQN'] = wtrbka_record_dict['BSPSQN']
    state_dict['BCSTAT'] = bcstat
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
        if not rccpsState.setTransState(state_dict):
            return AfaFlowControl.ExitThisFlow('S999','设置业务状态为失败异常')
        else:
            AfaDBFunc.CommitSql()
       
        return AfaFlowControl.ExitThisFlow('S999','主机交易失败')
        
    else:
        AfaLoggerFunc.tradeInfo("调用主机交易成功")
        #=====主机后更改原交易状态为成功====
        state_dict['BDWFLG'] = PL_BDWFLG_SUCC
        state_dict['STRINFO'] = '主机成功'
        if(TradeContext.existVariable("SBAC")):
            state_dict['SBAC'] = TradeContext.SBAC
        if(TradeContext.existVariable("RBAC")):
            state_dict['RBAC'] = TradeContext.RBAC
        if not rccpsState.setTransState(state_dict):
            return AfaFlowControl.ExitThisFlow('S999','设置业务状态为失败成功')
        else:
            AfaDBFunc.CommitSql()
            
        #=====如果是往账要将状态设置为清算成功====
        if(wtrbka_record_dict['BRSFLG'] == PL_BRSFLG_SND):    #往账
            if not rccpsState.newTransState(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],PL_BCSTAT_MFESTL,PL_BDWFLG_SUCC):
                return AfaFlowControl.ExitThisFlow('S999','设置业务状态为清算成功异常')
            else:
                AfaDBFunc.CommitSql()
        
    #=====更改错账登记簿中的处理标示====
    AfaLoggerFunc.tradeInfo("<<<<<<更改错账登记簿中的处理标示")
    where_dict = {}
    where_dict = {'BJEDTE':tddzcz_record_dict['BJEDTE'],'BSPSQN':tddzcz_record_dict['BSPSQN']}
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
    insert_dict['NOTDAT']  = TradeContext.BJEDTE
    insert_dict['BESBNO']  = wtrbka_record_dict['BESBNO']
    if(wtrbka_record_dict['BRSFLG'] == PL_BRSFLG_RCV):
        insert_dict['STRINFO'] = "此笔错账["+wtrbka_record_dict['BSPSQN']+"]["+wtrbka_record_dict['BJEDTE']+"]已做补记处理"
    else:
        insert_dict['STRINFO'] = "此笔错账["+wtrbka_record_dict['BSPSQN']+"]["+wtrbka_record_dict['BJEDTE']+"]已做补记处理 请用8522补打往账凭证"
    if not rccpsDBTrcc_notbka.insertCmt(insert_dict):
        return AfaFlowControl.ExitThisFlow('S999','向下发的通知表中插入数据失败')
    AfaLoggerFunc.tradeInfo("<<<<<<向通知表中插入数据成功")
    
    
    #=====给输出接口赋值====
    AfaLoggerFunc.tradeInfo("<<<<<<开始给输出接口赋值")
    TradeContext.BOSPSQ     = wtrbka_record_dict['BSPSQN']
    TradeContext.BOJEDT     = wtrbka_record_dict['BJEDTE']
    TradeContext.TLSQ       = TradeContext.TLSQ
    TradeContext.TRCCO      = wtrbka_record_dict['TRCCO']
    TradeContext.BRSFLG     = wtrbka_record_dict['BRSFLG']
    TradeContext.BEACSB     = wtrbka_record_dict['BESBNO']
    TradeContext.OROCCAMT   = str(wtrbka_record_dict['OCCAMT'])
    TradeContext.ORCUR      = wtrbka_record_dict['CUR']
    TradeContext.ORSNDBNK   = wtrbka_record_dict['SNDBNKCO']
    TradeContext.ORSNDBNKNM = wtrbka_record_dict['SNDBNKNM']
    TradeContext.ORRCVBNK   = wtrbka_record_dict['RCVBNKCO']
    TradeContext.ORRCVBNKNM = wtrbka_record_dict['RCVBNKNM']
    TradeContext.ORPYRACC   = wtrbka_record_dict['PYRACC']
    TradeContext.ORPYRNAM   = wtrbka_record_dict['PYRNAM']
    TradeContext.ORPYEACC   = wtrbka_record_dict['PYEACC']
    TradeContext.ORPYENAM   = wtrbka_record_dict['PYENAM']
#    TradeContext.SBAC       = 
#    TradeContext.RBAC       = 
    
    AfaLoggerFunc.tradeInfo("<<<<<<结束给输出接口赋值")
    
    AfaLoggerFunc.tradeInfo("<<<<<<<个性化处理(本地操作) 退出")
    
    AfaLoggerFunc.tradeInfo("'***农信银系统：通存通兑往账交易.差错账补记[8572] 退出")
    
    return True
