# -*- coding: gbk -*-
##################################################################
#   农信银.通存通兑来账.自动冲正来账
#=================================================================
#   程序文件:   TRCC006_1144.py
#   修改时间:   2008-11-05
#   作者：      刘雨龙
#   功    能:   收到自动冲正登记簿,根据原交易代码判断是冲正原来账
#               业务还是冲正来账冲销报文.
#               如果冲原来账业务,直接调用8820冲即可,同冲销来账
#               如果冲来账冲销报文,要判断原业务是否已被冲销,如果原
#               业务已被冲销,需要调用8813重新记账,如果原业务尚未被
#               冲销,根据原业务状态考虑是否需要重新设置状态或者直接
#               返回成功报文                
##################################################################

import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaAfeFunc,AfaDBFunc,HostContext
import rccpsDBTrcc_atcbka,rccpsDBTrcc_wtrbka,rccpsState,rccpsDBTrcc_spbsta,rccpsHostFunc,rccpsGetFunc
import rccpsMap1144CTradeContext2Datcbka_dict,rccpsDBTrcc_mpcbka,rccpsUtilTools,rccpsDBTrcc_wtrbka
import rccpsEntries,rccpsDBTrcc_sstlog
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("农信银系统：来账.中心类操作(1.本地操作).柜台冲正来账接收[TRCC006_1144]进入")
    AfaLoggerFunc.tradeDebug(">>>BJEDTE==" + TradeContext.BJEDTE)
    AfaLoggerFunc.tradeDebug(">>>BSPSQN==" + TradeContext.BSPSQN)
    #=====判断是否为重复交易====
    AfaLoggerFunc.tradeInfo(">>>判断是否为重复交易")
    
    where_dict = {}
    where_dict = {'MSGFLGNO':TradeContext.MSGFLGNO}

    record = rccpsDBTrcc_atcbka.selectu(where_dict)
    if( record == None ):
        AfaLoggerFunc.tradeDebug(">>>查找冲正登记簿异常,抛弃报文,等待中心重新发送自动冲正报文")
        return AfaFlowControl.ExitThisFlow('A099',"查找冲正登记簿异常,抛弃报文,等待中心重新发送自动冲正报文")    
    elif( len(record) > 0 ):    #重复交易
        AfaLoggerFunc.tradeDebug(">>>自动冲正交易重复") 
        #=====为返回自动冲正成功发送成功回执====
        #TradeContext.MSGTYPCO = 'SET010'                 #报文类代码
        #TradeContext.PRCCO    = 'RCCI0000'               #中心返回码
        #TradeContext.ORMFN    = TradeContext.MSGFLGNO    #参考报文标示号
        #TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #发送成员行号
        #TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #接收成员行号
        #TradeContext.STRINFO  = '自动冲正交易重复'       #附言
        #
        #return True        
        TradeContext.BJEDTE = record['BJEDTE']
        TradeContext.BSPSQN = record['BSPSQN']
    else:       
        #TradeContext.OR_BJEDTE = TradeContext.BJEDTE #为下面更新atcbka表时的字典赋值
        #TradeContext.OR_BSPSQN = TradeContext.BSPSQN #为下面更新atcbka表时的字典赋值      
        #=====开始登记自动冲正登记簿====
        AfaLoggerFunc.tradeDebug(">>>登记自动冲正登记簿")
        
        atcbka_dict = {}
        if not rccpsMap1144CTradeContext2Datcbka_dict.map(atcbka_dict):
            AfaLoggerFunc.tradeDebug(">>>自动冲正登记簿字典赋值失败,抛弃报文,等待自动冲正报文下次来得")
            return AfaFlowControl.ExitThisFlow('A099',"自动冲正登记簿字典赋值失败")     
            
        res = rccpsDBTrcc_atcbka.insertCmt(atcbka_dict)      
        if( res == -1):
            AfaLoggerFunc.tradeDebug(">>>自动冲正登记簿插入数据失败,数据库会滚,抛弃报文")
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('A099',"冲正登记簿插入数据失败") 
        else:
            AfaDBFunc.CommitSql()
    
    #=====判断中心日期是否相同====
    if TradeContext.NCCWKDAT != TradeContext.NCCworkDate:
        AfaLoggerFunc.tradeDebug(">>>查找原交易失败,未收到原交易,直接回复成功报文")
         
        #=====为返回自动冲正成功发送成功回执====
        TradeContext.MSGTYPCO = 'SET010'                 #报文类代码
        TradeContext.PRCCO    = 'RCCI0006'               #中心返回码
        TradeContext.ORMFN    = TradeContext.MSGFLGNO    #参考报文标示号
        TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #发送成员行号
        TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #接收成员行号
        TradeContext.STRINFO  = '冲正日期不合法'         #附言
        
        return True        
            
    #=====判断原交易代码====
    if TradeContext.ORTRCCO == '3000504':
        #=====3000504 柜台冲销报文====
        AfaLoggerFunc.tradeDebug('>>>查找原冲销业务是否存在')

        mpcbka_where = {'MSGFLGNO':TradeContext.ORMFN}
        record = rccpsDBTrcc_mpcbka.selectu(mpcbka_where)

        if record == None:
            AfaLoggerFunc.tradeDebug('>>>查找原冲销业务异常,抛弃报文,等待中心再次发生自动冲正')
            return AfaFlowControl.ExitThisFlow('S999','抛弃报文')
            
        elif len(record) <= 0:
            AfaLoggerFunc.tradeDebug('>>>查找原冲销业务空,回复成功')
            #=====为返回冲正成功发送成功回执====
            TradeContext.MSGTYPCO = 'SET010'                 #报文类代码
            TradeContext.PRCCO    = 'RCCI0000'               #中心返回码
            TradeContext.ORMFN    = TradeContext.MSGFLGNO    #参考报文标示号
            TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #发送成员行号
            TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #接收成员行号
            TradeContext.STRINFO  = '原冲销业务已冲正成功'       #附言
        
            return True        
            #return AfaFlowControl.ExitThisFlow('S999','抛弃报文')
        else:
            AfaLoggerFunc.tradeDebug('>>>查找冲销业务成功')
            
        #=====将原报单序号 原交易日期更新到冲正登记簿中====
        AfaLoggerFunc.tradeInfo('>>>更新原报单序号\原交易日期')
        
        atcbka_where={}
        atcbka_where['BJEDTE'] = TradeContext.BJEDTE      #交易日期
        atcbka_where['BSPSQN'] = TradeContext.BSPSQN      #报单序号
        
        atcbka_dict ={}
        atcbka_dict['BOJEDT']  = record['BJEDTE']    #原交易日期
        atcbka_dict['BOSPSQ']  = record['BSPSQN']    #原报单序号
        atcbka_dict['STRINFO'] = TradeContext.STRINFO     #附言 
        atcbka_dict['ORTRCDAT']= record['TRCDAT']    #原委托日期
        atcbka_dict['BESBNO']  = record['BESBNO']    #原机构号
        atcbka_dict['OPRNO']   = PL_TDOPRNO_CZ            #业务类型

        ret = rccpsDBTrcc_atcbka.update(atcbka_dict,atcbka_where)
        AfaLoggerFunc.tradeDebug('>>>ret=='+str(ret))
        if ret <= 0:
            AfaDBFunc.RollbackSql( )
            return AfaFlowControl.ExitThisFlow('S999', "更新自动冲正登记簿原报单序号和原交易日期异常,抛弃报文")
        else:
            AfaDBFunc.CommitSql( )
        
        AfaLoggerFunc.tradeInfo(">>>结束更新冲销登记簿原交易日期和原报单序号")

        #=====通过冲销登记簿查找原业务====
        AfaLoggerFunc.tradeDebug('>>>通过冲销登记簿中原报单序号和原交易日期查询原业务')

        wtr_where = {'BJEDTE':record['BOJEDT'],'BSPSQN':record['BOSPSQ']}
        wtr_dict = rccpsDBTrcc_wtrbka.selectu(wtr_where)

        if wtr_dict == None:
            AfaLoggerFunc.tradeDebug('>>>通过冲销登记簿中原报单序号和原交易日期查询原交易异常,抛弃报文,等待中心再次发生自动冲正')
            return AfaFlowControl.ExitThisFlow('S999','抛弃报文')
        elif len(wtr_dict) <= 0:
            AfaLoggerFunc.tradeDebug('>>>通过冲销登记簿中原报单序号和原交易日期查询原交易败,抛弃报文,等待中心再次发生自动冲正')
            return AfaFlowControl.ExitThisFlow('S999','抛弃报文')
        else:
            AfaLoggerFunc.tradeDebug('>>>查找原业务成功')

        #=====取原业务的业务状态====
        AfaLoggerFunc.tradeDebug('>>>取原业务业务状态')

        spb_where = {'BJEDTE':wtr_dict['BJEDTE'],'BSPSQN':wtr_dict['BSPSQN']}
        spb_dict = rccpsDBTrcc_spbsta.selectu(spb_where)

        if spb_dict == None:
            AfaLoggerFunc.tradeDebug('>>>取原业务业务状态异常,抛弃报文,等待中心再次发生自动冲正')
            return AfaFlowControl.ExitThisFlow('S999','抛弃报文')
        elif len(spb_dict) <= 0:
            AfaLoggerFunc.tradeDebug('>>>取原业务业务状态失败,抛弃报文,等待中心再次发生自动冲正')
            return AfaFlowControl.ExitThisFlow('S999','抛弃报文')
        else:
            AfaLoggerFunc.tradeDebug('>>>取原业务业务状态成功')

        #关彬捷  20081226  新增查询交易当前状态详细信息
        #查询交易当前状态详细信息
        sstlog_where = {'BJEDTE':wtr_dict['BJEDTE'],'BSPSQN':wtr_dict['BSPSQN'],'BCURSQ':spb_dict['BCURSQ']}
        spb_dict = rccpsDBTrcc_sstlog.selectu(sstlog_where)
        
        if( spb_dict == None ):
            return AfaFlowControl.ExitThisFlow('S999','取原业务业务状态详细信息异常,抛弃报文,等待中心再次发生自动冲正')
        elif len(spb_dict) <= 0:
            return AfaFlowControl.ExitThisFlow('S999','取原业务业务状态详细信息失败,抛弃报文,等待中心再次发生自动冲正')
        else:
            AfaLoggerFunc.tradeDebug('>>>取原业务业务状态详细信息成功')
            
        
        #关彬捷  20081226  新增若交易当前状态为自动扣款,自动入账,冲销,冲正处理中状态,则直接拒绝此冲销
        if (spb_dict['BCSTAT'] == PL_BCSTAT_AUTO or spb_dict['BCSTAT'] == PL_BCSTAT_AUTOPAY or spb_dict['BCSTAT'] == PL_BCSTAT_CANC or spb_dict['BCSTAT'] == PL_BCSTAT_CANCEL) and  spb_dict['BDWFLG'] == PL_BDWFLG_WAIT:
            return AfaFlowControl.ExitThisFlow('S999','原业务账务状态未知,抛弃报文,等待中心再次发起自动冲正')
            
        #关彬捷  20081226  新增若交易当前状态为自动扣款,自动入账,冲销,冲正失败状态,则调用8816查询账务状态
        if (spb_dict['BCSTAT'] == PL_BCSTAT_AUTO or spb_dict['BCSTAT'] == PL_BCSTAT_AUTOPAY or spb_dict['BCSTAT'] == PL_BCSTAT_CANC or spb_dict['BCSTAT'] == PL_BCSTAT_CANCEL) and  spb_dict['BDWFLG'] == PL_BDWFLG_FAIL:
            AfaLoggerFunc.tradeDebug('>>>调用8816查找该业务[' + wtr_dict['BSPSQN'] + ']状态')

            TradeContext.HostCode = '8816'                   #主机交易码
            TradeContext.OPFG     = '1'                      #查询类型
            TradeContext.NBBH     = 'RCC'                    #代理业务标识
            TradeContext.FEDT     = spb_dict['FEDT']         #原前置日期
            TradeContext.RBSQ     = spb_dict['RBSQ']         #原前置流水号
            TradeContext.DAFG     = '1'                      #抹/记账标志  1:记  2:抹
            TradeContext.BESBNO   = spb_dict['BESBNO']       #机构号
            TradeContext.BETELR   = spb_dict['BETELR']       #柜员号
            
            rccpsHostFunc.CommHost( TradeContext.HostCode )
            
            #=====分析主机返回====
            if TradeContext.errorCode == '0000':
                #此账务已成功记主机账,修改原交易状态为记账成功
                AfaLoggerFunc.tradeInfo("此账务已成功记主机账,修改原交易状态为记账成功")
                stat_dict = {}
                stat_dict['BJEDTE'] = spb_dict['BJEDTE']
                stat_dict['BSPSQN'] = spb_dict['BSPSQN']
                stat_dict['BCSTAT'] = spb_dict['BCSTAT']
                stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
                stat_dict['TRDT']   = HostContext.O1DADT           #主机日期
                stat_dict['TLSQ']   = HostContext.O1AMTL           #主机流水
                stat_dict['MGID']   = '0000'
                stat_dict['STRINFO']= '主机成功'
                
                if not rccpsState.setTransState(stat_dict):
                    return AfaFlowControl.ExitThisFlow('S999','设置原交易业务状态为记账成功异常,抛弃报文,等待下次冲正') 
                
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    return AfaFlowControl.ExitThisFlow("S999","Commit异常")
                    
                #更新查询出交易状态
                spb_dict['BDWFLG'] = PL_BDWFLG_SUCC
                spb_dict['TRDT']   = HostContext.O1DADT
                spb_dict['TLSQ']   = HostContext.O1AMTL
            
            elif TradeContext.errorCode == 'XCR0001':
                AfaLoggerFunc.tradeInfo(">>>主机返回原交易记账失败,继续冲销")
                
            else:
                AfaLoggerFunc.tradeInfo(">>>查询原交易账务状态异常,返回拒绝应答")
                
                #回滚原被冲销交易状态为冲销前状态
                AfaLoggerFunc.tradeInfo(">>>开始回滚原被冲销交易状态为冲销前状态")
                
                spbsta_dict = {}
                if not rccpsState.getTransStateDes(spb_dict['BJEDTE'],spb_dict['BSPSQN'],spbsta_dict,1):
                    return AfaFlowControl.ExitThisFlow('S999','查询原被冲销交易冲销前状态异常')
                
                if not rccpsState.newTransState(spbsta_dict['BJEDTE'],spbsta_dict['BSPSQN'],spbsta_dict['BCSTAT'],spbsta_dict['BDWFLG']):
                    return AfaFlowControl.ExitThisFlow('S999','回滚状态为冲销前状态异常')
                else:
                    AfaDBFunc.CommitSql()
                    
                sstlog_dict = {}
                sstlog_dict['BJEDTE']    =  spbsta_dict['BJEDTE']
                sstlog_dict['BSPSQN']    =  spbsta_dict['BSPSQN']
                sstlog_dict['BCSTAT']    =  spbsta_dict['BCSTAT']
                sstlog_dict['BDWFLG']    =  spbsta_dict['BDWFLG']
                sstlog_dict['NOTE3']     =  '冲销交易被冲正,回滚为冲销前状态'
                if spbsta_dict.has_key('FEDT'):           #前置日期
                    sstlog_dict['FEDT']  =  spbsta_dict['FEDT']
                if spbsta_dict.has_key('RBSQ'):           #前置流水号
                    sstlog_dict['RBSQ']  =  spbsta_dict['RBSQ']
                if spbsta_dict.has_key('TRDT'):           #主机日期
                    sstlog_dict['TRDT']  =  spbsta_dict['TRDT']
                if spbsta_dict.has_key('TLSQ'):           #主机流水号
                    sstlog_dict['TLSQ']  =  spbsta_dict['TLSQ']
                sstlog_dict['MGID']      =  spbsta_dict['MGID'] #主机返回码
                sstlog_dict['STRINFO']   =  spbsta_dict['STRINFO']  #主机返回信息
                
                if not rccpsState.setTransState(sstlog_dict):
                    return AfaFlowControl.ExitThisFlow('S999','回滚状态为冲正前状态详细信息异常')
                else:
                    AfaDBFunc.CommitSql()
                    
                AfaLoggerFunc.tradeInfo(">>>结束回滚原被冲销交易状态为冲销前状态")
                
                #=====为返回冲销成功发送拒绝回执====
                TradeContext.MSGTYPCO = 'SET010'                 #报文类代码
                TradeContext.PRCCO    = 'RCCO1006'               #中心返回码
                TradeContext.ORMFN    = TradeContext.MSGFLGNO    #参考报文标示号
                TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #发送成员行号
                TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #接收成员行号
                TradeContext.STRINFO  = '原交易账务状态未知'     #附言
                
                return True

        #=====判断原业务业务状态====
        #=====PL_BCSTAT_CANC 冲销====
        if not (spb_dict['BCSTAT'] == PL_BCSTAT_CANC and spb_dict['BDWFLG'] == PL_BDWFLG_SUCC):
            #=====原业务未冲销,直接回复成功即可====
            AfaLoggerFunc.tradeDebug(">>>原交易未冲销成功,回复成功")
         
            #=====为返回冲销成功发送成功回执====
            TradeContext.MSGTYPCO = 'SET010'                 #报文类代码
            TradeContext.PRCCO    = 'RCCI0000'               #中心返回码
            TradeContext.ORMFN    = TradeContext.MSGFLGNO    #参考报文标示号
            TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #发送成员行号
            TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #接收成员行号
            TradeContext.STRINFO  = '原冲销业务已冲正成功'   #附言
        
            return True
        elif spb_dict['TRDT'] == '' and spb_dict['TLSQ'] == '':
            #=====原业务冲销成功,但未抹账,回滚冲销前状态,回复冲正成功====
            AfaLoggerFunc.tradeDebug(">>>原业务冲销成功,但未抹账,回滚冲销前状态,回复冲正成功")
            
            #回滚原被冲销交易状态为冲销前状态
            AfaLoggerFunc.tradeInfo(">>>开始回滚原被冲销交易状态为冲销前状态")
            
            spbsta_dict = {}
            if not rccpsState.getTransStateDes(spb_dict['BJEDTE'],spb_dict['BSPSQN'],spbsta_dict,1):
                return AfaFlowControl.ExitThisFlow('S999','查询原被冲销交易冲销前状态异常')
            
            if not rccpsState.newTransState(spbsta_dict['BJEDTE'],spbsta_dict['BSPSQN'],spbsta_dict['BCSTAT'],spbsta_dict['BDWFLG']):
                return AfaFlowControl.ExitThisFlow('S999','回滚状态为冲销前状态异常')
            else:
                AfaDBFunc.CommitSql()
                
            sstlog_dict = {}
            sstlog_dict['BJEDTE']    =  spbsta_dict['BJEDTE']
            sstlog_dict['BSPSQN']    =  spbsta_dict['BSPSQN']
            sstlog_dict['BCSTAT']    =  spbsta_dict['BCSTAT']
            sstlog_dict['BDWFLG']    =  spbsta_dict['BDWFLG']
            sstlog_dict['NOTE3']     =  '冲销交易被冲正,回滚为冲销前状态'
            if spbsta_dict.has_key('FEDT'):           #前置日期
                sstlog_dict['FEDT']  =  spbsta_dict['FEDT']
            if spbsta_dict.has_key('RBSQ'):           #前置流水号
                sstlog_dict['RBSQ']  =  spbsta_dict['RBSQ']
            if spbsta_dict.has_key('TRDT'):           #主机日期
                sstlog_dict['TRDT']  =  spbsta_dict['TRDT']
            if spbsta_dict.has_key('TLSQ'):           #主机流水号
                sstlog_dict['TLSQ']  =  spbsta_dict['TLSQ']
            sstlog_dict['MGID']      =  spbsta_dict['MGID'] #主机返回码
            sstlog_dict['STRINFO']   =  spbsta_dict['STRINFO']  #主机返回信息
            
            if not rccpsState.setTransState(sstlog_dict):
                return AfaFlowControl.ExitThisFlow('S999','回滚状态为冲正前状态详细信息异常')
            else:
                AfaDBFunc.CommitSql()
                
            AfaLoggerFunc.tradeInfo(">>>结束回滚原被冲销交易状态为冲销前状态")
         
            #=====为返回冲销成功发送成功回执====
            TradeContext.MSGTYPCO = 'SET010'                 #报文类代码
            TradeContext.PRCCO    = 'RCCI0000'               #中心返回码
            TradeContext.ORMFN    = TradeContext.MSGFLGNO    #参考报文标示号
            TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #发送成员行号
            TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #接收成员行号
            TradeContext.STRINFO  = '原冲销业务已冲正成功'   #附言
            
            return True
        else:
            AfaLoggerFunc.tradeDebug('>>>准备调用8813再次记账')

        #=====记账前赋值操作====
        AfaLoggerFunc.tradeDebug('>>>记账前赋值操作')

        if rccpsGetFunc.GetRBSQ(PL_BRSFLG_RCV) == -1 :
            return AfaFlowControl.ExitThisFlow('S999','重新生成前置流水号失败,抛弃报文')

        TradeContext.BESBNO    =  wtr_dict['BESBNO']           #机构号
        TradeContext.BETELR    =  wtr_dict['BETELR']           #柜员号
        TradeContext.BEAUUS    =  wtr_dict['BEAUUS']           #授权柜员
        TradeContext.BEAUPS    =  wtr_dict['BEAUPS']           #授权密码
        TradeContext.TERMID    =  wtr_dict['TERMID']           #终端号
        TradeContext.HostCode  =  '8813'                       #主机交易码
        TradeContext.PYRACC    =  wtr_dict['PYRACC']           #付款人账户
        TradeContext.PYRNAM    =  wtr_dict['PYRNAM']           #付款人名称
        TradeContext.OCCAMT    =  str(wtr_dict['OCCAMT'])      #金额
        TradeContext.CUSCHRG   =  str(wtr_dict['CUSCHRG'])     #手续费金额
        TradeContext.BANKNO    =  wtr_dict['BNKBKNO']          #存折号码
        
        if wtr_dict['TRCCO'] in ('3000002','3000004'):
            #=====通存====
            AfaLoggerFunc.tradeDebug('>>>通存')

            TradeContext.RCCSMCD  =  PL_RCCSMCD_XJTCLZ                       #摘要代码  PL_RCCSMCD_XJTCLZ  通存来账
            TradeContext.SBAC     = TradeContext.BESBNO + PL_ACC_NXYDQSLZ    #借方账户:农信银待清算来账
            TradeContext.SBNM     = "农信银待清算来账"
            TradeContext.RBAC     = wtr_dict['PYEACC']                       #贷方账户:收款人账户
            TradeContext.RBNM     = wtr_dict['PYENAM']                       #贷方户名:收款人户名
            TradeContext.OCCAMT = str(wtr_dict['OCCAMT'])
            #=====add by pgt 12-4====
            TradeContext.CTFG      = '7'                                    #本金 手续费标识  7 本金 8手续费 9 本金＋手续费 
            TradeContext.PKFG      = 'T'                                    #通存通兑标识                                   
            TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
        elif wtr_dict['TRCCO'] in ('3000102','3000104'):
            #=====通兑====
            AfaLoggerFunc.tradeDebug('>>>通兑')

            if float(wtr_dict['CUSCHRG']) <= 0:
                #=====对方现金收取手续费或不收费====
                AfaLoggerFunc.tradeDebug('>>>现金收取手续费')
 
                TradeContext.RCCSMCD  = PL_RCCSMCD_XJTDLZ                     #主机摘要代码
                TradeContext.SBAC = TradeContext.PYRACC                       #借方账户:付款人账户
                TradeContext.ACNM = TradeContext.PYRNAM                       #借方户名 付款人户名
                TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ     #贷方账户:农信银待清算来账
                TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC, 25)
                TradeContext.RBNM = '农信银待清算来账'                        #贷方户名
                #=====add by pgt 12-4====
                TradeContext.CTFG      = '7'                                  #本金 手续费标识  7 本金 8手续费 9 本金＋手续费 
                TradeContext.PKFG      = 'T'                                  #通存通兑标识                                   

                if wtr_dict['TRCCO'] == '3000104':
                    TradeContext.WARNTNO = '49' + TradeContext.BANKNO
                else:
                    TradeContext.WARNTNO = TradeContext.SBAC[6:18]
            else:
                #=====对方转账收取手续费====
                AfaLoggerFunc.tradeDebug('>>>转账收取手续费')

                TradeContext.ACUR    =  '3'                                         #记账次数
                #=========交易金额============
                TradeContext.RCCSMCD  =  PL_RCCSMCD_XJTDLZ                          #摘要代码
                TradeContext.SBAC  =  TradeContext.PYRACC                           #借方账号
                TradeContext.ACNM  =  TradeContext.PYRNAM                           #借方户名
                TradeContext.RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
                TradeContext.RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
                TradeContext.OTNM  =  '待解临时款项'                                #贷方户名
                TradeContext.CTFG  = '7'                                            #本金 手续费标识  7 本金 8手续费 9 本金＋手续费 
                TradeContext.PKFG  = 'T'                                            #通存通兑标识                                   

                AfaLoggerFunc.tradeInfo( '>>>交易金额:借方账号' + TradeContext.SBAC )
                AfaLoggerFunc.tradeInfo( '>>>交易金额:贷方账号' + TradeContext.RBAC )

                #=========结算手续费收入户===========
                TradeContext.I2SMCD  =  PL_RCCSMCD_SXF                                #摘要代码
                TradeContext.I2SBAC  =  TradeContext.PYRACC                           #借方账号
                TradeContext.I2ACNM  =  TradeContext.PYRNAM                           #借方户名
                TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
                TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
                TradeContext.I2OTNM  =  '待解临时款项'                                #贷方户名
                TradeContext.I2TRAM  =  str(TradeContext.CUSCHRG)                      #发生额
                TradeContext.I2CTFG  = '8'                                             #本金 手续费标识  7 本金 8手续费 9 本金＋手续费 
                TradeContext.I2PKFG  = 'T'                                             #通存通兑标识                                   

                AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:借方账号' + TradeContext.I2SBAC )
                AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:贷方账号' + TradeContext.I2RBAC )

                #=========交易金额+手续费===================
                TradeContext.I3SMCD    =  PL_RCCSMCD_XJTDLZ                               #摘要代码
                TradeContext.I3SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #借方账号
                TradeContext.I3SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
                TradeContext.I3ACNM    =  '待解临时款项'                                #借方户名
                TradeContext.I3RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ         #贷方账号
                TradeContext.I3RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
                TradeContext.I3OTNM    =  '农信银来账'                                  #贷方户名
                TradeContext.I3TRAM    =  rccpsUtilTools.AddDot(TradeContext.OCCAMT,TradeContext.CUSCHRG) #发生额
                TradeContext.I3CTFG  = '9'                                              #本金 手续费标识  7 本金 8手续费 9 本金＋手续费                                            
                TradeContext.I3PKFG  = 'T'                                              #通存通兑标识                                   

                #=====凭证号码====
                if wtr_dict['TRCCO'] ==  '3000102':
                    #=====卡====
                    TradeContext.WARNTNO = TradeContext.SBAC[6:18]
                    TradeContext.I2WARNTNO = TradeContext.I2SBAC[6:18]
                else:
                    #=====折====
                    TradeContext.WARNTNO   = '49' + TradeContext.BANKNO
                    TradeContext.I2WARNTNO = '49' + TradeContext.BANKNO
        elif wtr_dict['TRCCO'] in ('3000003','3000005'):
            #=====本转异====
            AfaLoggerFunc.tradeDebug('>>>本转异')

            TradeContext.RCCSMCD  =  PL_RCCSMCD_XJTCLZ                       #摘要代码  PL_RCCSMCD_XJTCLZ  通存来账
            TradeContext.SBAC     = TradeContext.BESBNO + PL_ACC_NXYDQSLZ    #借方账户:农信银待清算来账
            TradeContext.SBNM     = "农信银待清算来账"
            TradeContext.RBAC     = wtr_dict['PYEACC']                       #贷方账户:收款人账户
            TradeContext.RBNM     = wtr_dict['PYENAM']                       #贷方户名:收款人户名
            TradeContext.OCCAMT = str(wtr_dict['OCCAMT'])
            #=====add by pgt 12-4====
            TradeContext.CTFG      = '7'                                    #本金 手续费标识  7 本金 8手续费 9 本金＋手续费 
            TradeContext.PKFG      = 'T'                                    #通存通兑标识
            TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
        elif wtr_dict['TRCCO'] in ('3000103','3000105'):
            #=====异转本====
            AfaLoggerFunc.tradeDebug('>>>异转本')

            if( float(TradeContext.CUSCHRG) <= 0 ):
                #=====现金====
                AfaLoggerFunc.tradeDebug('>>>现金收取手续费')

                TradeContext.RCCSMCD  = PL_RCCSMCD_YZBWZ#主机摘要代码
                TradeContext.SBAC = TradeContext.PYRACC                       #借方账户:付款人账户
                TradeContext.ACNM = TradeContext.PYRNAM                       #借方户名 付款人户名
                TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ     #贷方账户:农信银待清算来账
                TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC, 25)
                TradeContext.RBNM = '农信银待清算来账'                        #贷方户名:
                TradeContext.CTFG =  '7'                                      #本金 手续费标识  7 本金 8手续费 9 本金＋手续费 
                TradeContext.PKFG =  'T'                                      #通存通兑标识                                   

                if wtr_dict['TRCCO'] == '3000103':
                    TradeContext.WARNTNO = TradeContext.SBAC[6:18]
                else:
                    TradeContext.WARNTNO = '49' + TradeContext.BANKNO

                AfaLoggerFunc.tradeDebug( '>>>借方账号:' + TradeContext.SBAC )
                AfaLoggerFunc.tradeDebug( '>>>贷方账号:' + TradeContext.RBAC )
                AfaLoggerFunc.tradeDebug( '>>>凭证号码:' + TradeContext.WARNTNO )
            else:
                #=====转账=====
                AfaLoggerFunc.tradeDebug('>>>转账收取手续费')

                TradeContext.ACUR    =  '3'                                           #记账次数
                #=========交易金额============
                TradeContext.RCCSMCD  =  PL_RCCSMCD_YZBWZ                               #摘要代码
                TradeContext.SBAC  =  TradeContext.PYRACC                           #借方账号
                TradeContext.ACNM  =  TradeContext.PYRNAM                           #借方户名
                TradeContext.RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
                TradeContext.RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
                TradeContext.OTNM  =  '待解临时款项'                                #贷方户名
                TradeContext.OCCAMT  =  str(TradeContext.OCCAMT)                       #发生额
                TradeContext.CTFG  = '7'                                            #本金 手续费标识  7 本金 8手续费 9 本金＋手续费 
                TradeContext.PKFG  = 'T'                                            #通存通兑标识                                   

                AfaLoggerFunc.tradeDebug( '>>>交易金额:借方账号' + TradeContext.SBAC )
                AfaLoggerFunc.tradeDebug( '>>>交易金额:贷方账号' + TradeContext.RBAC )

                #=========结算手续费收入户===========
                TradeContext.I2SMCD  =  PL_RCCSMCD_SXF                                #摘要代码
                TradeContext.I2SBAC  =  TradeContext.PYRACC                           #借方账号
                TradeContext.I2ACNM  =  TradeContext.PYRNAM                           #借方户名
                TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
                TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
                TradeContext.I2OTNM  =  '待解临时款项'                                #贷方户名
                TradeContext.I2TRAM  =  str(TradeContext.CUSCHRG)                      #发生额
                TradeContext.I2CTFG  = '8'                                            #本金 手续费标识  7 本金 8手续费 9 本金＋手续费 
                TradeContext.I2PKFG  = 'T'                                            #通存通兑标识                                    

                AfaLoggerFunc.tradeDebug( '>>>结算手续费收入户:借方账号' + TradeContext.I2SBAC )
                AfaLoggerFunc.tradeDebug( '>>>结算手续费收入户:贷方账号' + TradeContext.I2RBAC )

                #=========交易金额+手续费===================
                TradeContext.I3SMCD    =  PL_RCCSMCD_YZBWZ                               #摘要代码
                TradeContext.I3SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #借方账号
                TradeContext.I3SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
                TradeContext.I3ACNM    =  '待解临时款项'                                #借方户名
                TradeContext.I3RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ         #贷方账号
                TradeContext.I3RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
                TradeContext.I3OTNM    =  '农信银来账'                                  #贷方户名
                TradeContext.I3TRAM    =  rccpsUtilTools.AddDot(TradeContext.OCCAMT,TradeContext.CUSCHRG) #发生额
                TradeContext.I3CTFG    = '9'                                            #本金 手续费标识  7 本金 8手续费 9 本金＋手续费 
                TradeContext.I3PKFG    = 'T'                                            #通存通兑标识                                   
                AfaLoggerFunc.tradeDebug( '>>>交易金额+手续费:借方账号' + TradeContext.I3SBAC )
                AfaLoggerFunc.tradeDebug( '>>>交易金额+手续费:贷方账号' + TradeContext.I3RBAC )

                if wtr_dict['TRCCO'] == '3000103':
                    TradeContext.WARNTNO   = TradeContext.SBAC[6:18]
                    TradeContext.I2WARNTNO = TradeContext.I2SBAC[6:18]
                else:
                    TradeContext.WARNTNO   = '49' + TradeContext.BANKNO
                    TradeContext.I2WARNTNO = '49' + TradeContext.BANKNO
        else:
            AfaLoggerFunc.tradeInfo('>>>原交易码错误')
            return AfaFlowControl.ExitThisFlow('S999','抛弃报文')

        #=====新增状态====
        if wtr_dict['TRCCO'] in ('3000002','3000004','3000003','3000005'):
            #=====通存 本转异 状态为:自动入账====
            TradeContext.BCSTAT = PL_BCSTAT_AUTO
        else:
            #=====通兑 异转本 状态为:自动扣款====
            TradeContext.BCSTAT = PL_BCSTAT_AUTOPAY

        #=====开始设置状态====
        #if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,TradeContext.BCSTAT,PL_BDWFLG_WAIT):
        if not rccpsState.newTransState(wtr_dict['BJEDTE'],wtr_dict['BSPSQN'],TradeContext.BCSTAT,PL_BDWFLG_WAIT):
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('S999','设置业务状态为自动入账/扣款-处理中异常')
        else:
            AfaDBFunc.CommitSql()

        #=====开始与主机进行通讯====
        AfaLoggerFunc.tradeInfo('>>>准备开始与主机通讯')

        rccpsHostFunc.CommHost( TradeContext.HostCode )

        #=====分析主机返回====
        AfaLoggerFunc.tradeInfo('>>>分析主机返回')

        sstlog = {}
        sstlog['BJEDTE']  =  wtr_dict['BJEDTE']
        sstlog['BSPSQN']  =  wtr_dict['BSPSQN']
        sstlog['BCSTAT']  =  TradeContext.BCSTAT
        sstlog['MGID']    =  TradeContext.errorCode

        if TradeContext.errorCode == '0000':
            sstlog['TRDT']  =  TradeContext.TRDT             #主机日期
            sstlog['TLSQ']  =  TradeContext.TLSQ             #主机流水
            sstlog['BDWFLG']=  PL_BDWFLG_SUCC
            sstlog['STRINFO'] = '冲销交易被冲正,补记账务成功'               #附言
        else:
            sstlog['BDWFLG']=  PL_BDWFLG_FAIL
            sstlog['STRINFO'] = TradeContext.errorMsg        #附言
            
        #=====设置状态====
        if not rccpsState.setTransState(sstlog):
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('S999', "设置业务状态异常")
        else:
            AfaDBFunc.CommitSql()

        #=====主机成功后返回正确回执报文====
        AfaLoggerFunc.tradeInfo('>>>发送成功回执')

        TradeContext.MSGTYPCO = 'SET010'                 #报文类代码
        TradeContext.PRCCO    = 'RCCI0000'               #中心返回码
        TradeContext.ORMFN    = TradeContext.MSGFLGNO    #参考报文标示号
        TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #发送成员行号
        TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #接收成员行号
        TradeContext.STRINFO  = '成功'                   #附言

        return True
    elif TradeContext.ORTRCCO == '3000505':
        #=====3000505 补正业务====
        AfaLoggerFunc.tradeDebug('>>>查找原补正业务是否存在')
        
        #关彬捷  20081230  若原业务为补正,直接回复冲正成功应答
        
        AfaLoggerFunc.tradeInfo('>>>发送成功回执')

        TradeContext.MSGTYPCO = 'SET010'                 #报文类代码
        TradeContext.PRCCO    = 'RCCI0000'               #中心返回码
        TradeContext.ORMFN    = TradeContext.MSGFLGNO    #参考报文标示号
        TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #发送成员行号
        TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #接收成员行号
        TradeContext.STRINFO  = '成功'                   #附言
        
        return True
    else:
        #=====冲正原来账/往账正常业务====
     
        #=====查找原交易是否存在====
        AfaLoggerFunc.tradeDebug(">>>查找原交易是否存在")
        
        where_dict = {'MSGFLGNO':TradeContext.ORMFN}
        wtrbka_dict = rccpsDBTrcc_wtrbka.selectu(where_dict)
        
        if( wtrbka_dict == -1 ):
            AfaLoggerFunc.tradeInfo(">>>查找原交易失败,原业务中心流水号["+str(TradeContext.ORTRCNO)+"]")
            return AfaFlowControl.ExitThisFlow('A099',"查找原交易失败,抛弃报文,等待中心自动冲正")
            
        if( len(wtrbka_dict) == 0 ):
            #=====未查找到原交易====
            AfaLoggerFunc.tradeDebug(">>>查找原交易失败,未收到原交易,直接回复成功报文")
         
            #=====为返回冲销成功发送成功回执====
            TradeContext.MSGTYPCO = 'SET010'                 #报文类代码
            TradeContext.PRCCO    = 'RCCI0000'               #中心返回码
            TradeContext.ORMFN    = TradeContext.MSGFLGNO    #参考报文标示号
            TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #发送成员行号
            TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #接收成员行号
            TradeContext.STRINFO  = '成功'                   #附言
        
            return True        
        else:
            #=====查找原交易成功====
            AfaLoggerFunc.tradeInfo(">>>查找原交易成功")
            
            #=====将原报单序号 原交易日期更新到冲销登记簿中====
            AfaLoggerFunc.tradeInfo('>>>更新原报单序号\原交易日期')
            
            atcbka_where={}
            atcbka_where['BSPSQN'] = TradeContext.BSPSQN      #报单序号
            atcbka_where['BJEDTE'] = TradeContext.BJEDTE      #交易日期
            
            atcbka_dict ={}
            atcbka_dict['BOJEDT']  = wtrbka_dict['BJEDTE']    #原交易日期
            atcbka_dict['BOSPSQ']  = wtrbka_dict['BSPSQN']    #原报单序号
            #关彬捷  20081225  更新冲正登记簿中登记机构号为原交易机构号
            atcbka_dict['BESBNO']  = wtrbka_dict['BESBNO']    #原机构号
            atcbka_dict['STRINFO'] = TradeContext.STRINFO     #附言 
            atcbka_dict['ORTRCDAT']= wtrbka_dict['TRCDAT']    #原委托日期
            atcbka_dict['OPRNO']   = PL_TDOPRNO_CZ            #业务类型

            ret = rccpsDBTrcc_atcbka.update(atcbka_dict,atcbka_where)
            
            if ret <= 0:
                AfaDBFunc.RollbackSql( )
                return AfaFlowControl.ExitThisFlow('S999', "更新自动冲正登记簿原报单序号和原交易日期异常,抛弃报文")
            else:
                AfaDBFunc.CommitSql( )
            
            AfaLoggerFunc.tradeInfo(">>>结束更新冲销登记簿原交易日期和原报单序号")
            
            #=====查找原来账业务状态====
            AfaLoggerFunc.tradeInfo(">>>查找原业务状态")
            
            spbsta_where = {'BJEDTE':wtrbka_dict['BJEDTE'],'BSPSQN':wtrbka_dict['BSPSQN']}
            spbsta_dict = rccpsDBTrcc_spbsta.selectu(spbsta_where)
            
            if( spbsta_dict == None ):
                AfaLoggerFunc.tradeDebug(">>>查找原业务状态失败,发送中心失败报文")
            
                #=====为返回冲销成功发送拒绝回执====
                TradeContext.MSGTYPCO = 'SET010'                 #报文类代码
                TradeContext.PRCCO    = 'RCCO1006'               #中心返回码
                TradeContext.ORMFN    = TradeContext.MSGFLGNO    #参考报文标示号
                TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #发送成员行号
                TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #接收成员行号
                TradeContext.STRINFO  = '开户行处理失败'         #附言
            
                return True
                
            #关彬捷  20081226  新增查询交易当前状态详细信息
            #查询交易当前状态详细信息
            sstlog_where = {'BJEDTE':wtrbka_dict['BJEDTE'],'BSPSQN':wtrbka_dict['BSPSQN'],'BCURSQ':spbsta_dict['BCURSQ']}
            spbsta_dict = rccpsDBTrcc_sstlog.selectu(sstlog_where)
            
            if( spbsta_dict == None ):
                AfaLoggerFunc.tradeDebug(">>>查找原业务状态失败,发送中心失败报文")
            
                #=====为返回冲销成功发送拒绝回执====
                TradeContext.MSGTYPCO = 'SET010'                 #报文类代码
                TradeContext.PRCCO    = 'RCCO1006'               #中心返回码
                TradeContext.ORMFN    = TradeContext.MSGFLGNO    #参考报文标示号
                TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #发送成员行号
                TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #接收成员行号
                TradeContext.STRINFO  = '开户行处理失败'         #附言
            
                return True

            
            #关彬捷  20081226  新增若交易当前状态为自动扣款,自动入账,冲销,冲正处理中状态,退出,等待下个冲正报文
            if (spbsta_dict['BCSTAT'] == PL_BCSTAT_AUTO or spbsta_dict['BCSTAT'] == PL_BCSTAT_AUTOPAY or spbsta_dict['BCSTAT'] == PL_BCSTAT_CANC or spbsta_dict['BCSTAT'] == PL_BCSTAT_CANCEL) and  spbsta_dict['BDWFLG'] == PL_BDWFLG_WAIT:
                return AfaFlowControl.ExitThisFlow('S999','原业务账务状态未知,抛弃报文,等待中心再次发起自动冲正')

            #关彬捷  20081226  新增若交易当前状态为自动扣款,自动入账,冲销,冲正失败状态,则调用8816查询账务状态
            if (spbsta_dict['BCSTAT'] == PL_BCSTAT_AUTO or spbsta_dict['BCSTAT'] == PL_BCSTAT_AUTOPAY or spbsta_dict['BCSTAT'] == PL_BCSTAT_CANC or spbsta_dict['BCSTAT'] == PL_BCSTAT_CANCEL) and  spbsta_dict['BDWFLG'] == PL_BDWFLG_FAIL:
                AfaLoggerFunc.tradeDebug('>>>调用8816查找该业务[' + wtrbka_dict['BSPSQN'] + ']状态')
            
                TradeContext.HostCode = '8816'                   #主机交易码
                TradeContext.OPFG     = '1'                      #查询类型
                TradeContext.NBBH     = 'RCC'                    #代理业务标识
                TradeContext.FEDT     = spbsta_dict['FEDT']      #原前置日期
                TradeContext.RBSQ     = spbsta_dict['RBSQ']      #原前置流水号
                TradeContext.DAFG     = '1'                      #抹/记账标志  1:记  2:抹
                TradeContext.BESBNO   = spbsta_dict['BESBNO']    #机构号
                TradeContext.BETELR   = spbsta_dict['BETELR']    #柜员号
                
                rccpsHostFunc.CommHost( TradeContext.HostCode )
                
                #=====分析主机返回====
                if TradeContext.errorCode == '0000':
                    #此账务已成功记主机账,修改原交易状态为记账成功
                    AfaLoggerFunc.tradeInfo("此账务已成功记主机账,修改原交易状态为记账成功")
                    stat_dict = {}
                    stat_dict['BJEDTE'] = spbsta_dict['BJEDTE']
                    stat_dict['BSPSQN'] = spbsta_dict['BSPSQN']
                    stat_dict['BCSTAT'] = spbsta_dict['BCSTAT']
                    stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
                    stat_dict['TRDT']   = HostContext.O1DADT           #主机日期
                    stat_dict['TLSQ']   = HostContext.O1AMTL           #主机流水
                    stat_dict['MGID']   = '0000'
                    stat_dict['STRINFO']= '主机成功'
                    
                    if not rccpsState.setTransState(stat_dict):
                        return AfaFlowControl.ExitThisFlow('S999','设置原交易业务状态为记账成功异常') 
                    
                    if not AfaDBFunc.CommitSql( ):
                        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
                        
                    #更新查询出交易状态
                    spbsta_dict['BDWFLG'] = PL_BDWFLG_SUCC
                    spbsta_dict['TRDT']   = HostContext.O1DADT
                    spbsta_dict['TLSQ']   = HostContext.O1AMTL
                
                elif TradeContext.errorCode == 'XCR0001':
                    AfaLoggerFunc.tradeInfo(">>>主机返回原交易记账失败,继续冲正")
                    
                else:
                    AfaLoggerFunc.tradeInfo(">>>查询原交易账务状态异常,返回拒绝应答,等待下次冲正报文")
                    #=====为返回冲正拒绝回执赋值====
                    TradeContext.MSGTYPCO = 'SET010'                 #报文类代码
                    TradeContext.PRCCO    = 'RCCO1006'               #中心返回码
                    TradeContext.STRINFO  = '原交易账务状态未知'     #附言
                    TradeContext.ORMFN    = TradeContext.MSGFLGNO    #参考报文标示号
                    TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #发送成员行号
                    TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #接收成员行号
                    
                    return True

            #=====根据来往帐标识进行冲正状态判断====
            if( wtrbka_dict['BRSFLG'] == PL_BRSFLG_RCV ):
                #=====来账业务====
                AfaLoggerFunc.tradeDebug(">>>来账业务")

                #=====PL_BCSTAT_AUTOPAY   自动扣款====
                #=====PL_BCSTAT_CONFPAY   确认付款====
                #=====PL_BCSTAT_CONFACC   确认入账====
                #=====PL_BCSTAT_MFERFE    拒绝====
                #=====PL_BCSTAT_CANC      柜台冲销====
                #=====PL_BCSTAT_CANCEL    自动冲正====
                if( ((spbsta_dict['BCSTAT']==PL_BCSTAT_AUTO or spbsta_dict['BCSTAT']==PL_BCSTAT_AUTOPAY) and spbsta_dict['BDWFLG']==PL_BDWFLG_FAIL) \
                    or (spbsta_dict['BCSTAT'] == PL_BCSTAT_MFERFE  and spbsta_dict['BDWFLG'] == PL_BDWFLG_SUCC) \
                    or (spbsta_dict['BCSTAT'] == PL_BCSTAT_CANC    and spbsta_dict['BDWFLG'] == PL_BDWFLG_SUCC) \
                    or (spbsta_dict['BCSTAT'] == PL_BCSTAT_CANCEL  and spbsta_dict['BDWFLG'] == PL_BDWFLG_SUCC) \
                    or (spbsta_dict['BCSTAT'] == PL_BCSTAT_CONFPAY and spbsta_dict['BDWFLG'] == PL_BDWFLG_SUCC) \
                    or (spbsta_dict['BCSTAT'] == PL_BCSTAT_CONFACC and spbsta_dict['BDWFLG'] == PL_BDWFLG_SUCC)):
                    #=====不允许冲正====
                    AfaLoggerFunc.tradeDebug(">>>原业务["+str(spbsta_dict['BSPSQN'])+"]记账失败或被拒绝或冲销或自动冲正或存款确认,无需再抹账,发送成功报文")

                    if spbsta_dict['BCSTAT'] not in (PL_BCSTAT_MFERFE,PL_BCSTAT_CANC,PL_BCSTAT_CANCEL):
                        AfaLoggerFunc.tradeDebug('>>>新增原业务状态为自动冲正-成功')
                        if not rccpsState.newTransState(spbsta_dict['BJEDTE'],spbsta_dict['BSPSQN'],PL_BCSTAT_CANCEL,PL_BDWFLG_SUCC):
                            AfaDBFunc.RollbackSql()
                            return AfaFlowControl.ExitThisFlow('S999','设置业务状态为自动冲正-成功异常')
                        else:
                            AfaDBFunc.CommitSql( )
                    else:
                        AfaLoggerFunc.tradeDebug('>>>原业务状态为[拒绝/冲销/冲正],不需要新增状态')
 
                    #=====原交易无需抹账,返回冲正成功应答====
                    TradeContext.MSGTYPCO = 'SET010'                 #报文类代码
                    TradeContext.PRCCO    = 'RCCI0000'               #中心返回码
                    TradeContext.ORMFN    = TradeContext.MSGFLGNO    #参考报文标示号
                    TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #发送成员行号
                    TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #接收成员行号
                    TradeContext.STRINFO  = '原业务冲正成功'         #附言
            
                    return True
                else:
                    #=====新增原业务状态为冲正-处理中====
                    AfaLoggerFunc.tradeDebug('>>>新增原业务状态为自动冲正-处理中')
            
                    #=====直接调用8820冲正原业务====
                    TradeContext.BOSPSQ   = spbsta_dict['BSPSQN']    #原报单序号
                    TradeContext.BOJEDT   = spbsta_dict['BJEDTE']    #原交易日期
                    TradeContext.HostCode = '8820'                   #主机交易码
                    
                    if not rccpsState.newTransState(spbsta_dict['BJEDTE'],spbsta_dict['BSPSQN'],PL_BCSTAT_CANCEL,PL_BDWFLG_WAIT):
                        AfaDBFunc.RollbackSql()
                        return AfaFlowControl.ExitThisFlow('S999','设置业务状态为自动冲正处理中异常')
                    else:
                        AfaDBFunc.CommitSql( )
            
                    #=====向主机发起8820抹账处理==== 
                    AfaLoggerFunc.tradeDebug('>>>向主机发起8820抹账处理')
            
                    rccpsHostFunc.CommHost( TradeContext.HostCode ) 
            
                    #=====判断主机返回====
                    sstlog_dict={}
                    sstlog_dict['BJEDTE']  =  spbsta_dict['BJEDTE']
                    sstlog_dict['BSPSQN']  =  spbsta_dict['BSPSQN']
                    sstlog_dict['BCSTAT']  =  PL_BCSTAT_CANCEL       #冲正
                    sstlog_dict['MGID']    =  TradeContext.errorCode #主机返回码
                    if TradeContext.existVariable('BOJEDT'):           #前置日期
                        sstlog_dict['FEDT'] = TradeContext.BOJEDT
                    if TradeContext.existVariable('BOSPSQ'):           #前置流水号
                        sstlog_dict['RBSQ'] = TradeContext.BOSPSQ
                    if TradeContext.existVariable('TRDT'):           #主机日期
                        sstlog_dict['TRDT'] = TradeContext.TRDT
                    if TradeContext.existVariable('TLSQ'):           #主机流水号
                        sstlog_dict['TLSQ'] = TradeContext.TLSQ
                    
                    #关彬捷  20090219  增加冲销成功的主机错误码判断:SXR0010(此笔交易已被冲正)
                    if TradeContext.errorCode in ('0000','SXR0010'):
                        #=====更改状态====
                        sstlog_dict['BDWFLG']    =  PL_BDWFLG_SUCC       #流转标识 PL_BDWFLG_SUCC 成功
                        sstlog_dict['STRINFO']   =  '来账冲正成功'       #附言
                        TradeContext.PRCCO       =  'RCCI0000'
                        TradeContext.STRINFO     =  '原业务冲正成功'
                    else:
                        sstlog_dict['BDWFLG']    =  PL_BDWFLG_FAIL       #流转标识 PL_BDWFLG_FAIL 失败
                        sstlog_dict['STRINFO']   =  TradeContext.errorMsg  #附言
                        TradeContext.PRCCO       =  'NN1IA999'
                        TradeContext.STRINFO     =  '原业务冲正失败 ' + TradeContext.errorMsg
            
                    #=====修改原业务状态====
                    AfaLoggerFunc.tradeDebug('>>>修改原业务状态')
            
                    res = rccpsState.setTransState(sstlog_dict)
            
                    if( res == False ):
                        AfaDBFunc.RollbackSql()
                        return AfaFlowControl.ExitThisFlow('A099', '更改被冲正的交易状态失败')
                    else:
                        AfaDBFunc.CommitSql( )
                    
                    #关彬捷 20081226  修改如果冲正失败则回滚冲正前状态
                    if TradeContext.errorCode not in ('0000','SXR0010'):
                        #冲正失败,回滚状态为冲正前状态
                        if not rccpsState.newTransState(spbsta_dict['BJEDTE'],spbsta_dict['BSPSQN'],spbsta_dict['BCSTAT'],spbsta_dict['BDWFLG']):
                            AfaDBFunc.RollBackSql()
                            return AfaFlowControl.ExitThisFlow('S999','回滚状态为冲正前状态异常')
                        else:
                            AfaDBFunc.CommitSql()
                            
                        sstlog_dict = {}
                        sstlog_dict['BJEDTE']    =  spbsta_dict['BJEDTE']
                        sstlog_dict['BSPSQN']    =  spbsta_dict['BSPSQN']
                        sstlog_dict['BCSTAT']    =  spbsta_dict['BCSTAT']
                        sstlog_dict['BDWFLG']    =  spbsta_dict['BDWFLG']
                        sstlog_dict['NOTE3']     =  '原业务冲正失败,回滚为冲正前状态'
                        if spbsta_dict.has_key('FEDT'):           #前置日期
                            sstlog_dict['FEDT']  =  spbsta_dict['FEDT']
                        if spbsta_dict.has_key('RBSQ'):           #前置流水号
                            sstlog_dict['RBSQ']  =  spbsta_dict['RBSQ']
                        if spbsta_dict.has_key('TRDT'):           #主机日期
                            sstlog_dict['TRDT']  =  spbsta_dict['TRDT']
                        if spbsta_dict.has_key('TLSQ'):           #主机流水号
                            sstlog_dict['TLSQ']  =  spbsta_dict['TLSQ']
                        sstlog_dict['MGID']      =  spbsta_dict['MGID'] #主机返回码
                        sstlog_dict['STRINFO']   =  spbsta_dict['STRINFO']  #主机返回信息
                        
                        if not rccpsState.setTransState(sstlog_dict):
                            return AfaFlowControl.ExitThisFlow('S999','回滚状态为冲正前状态详细信息异常')
                        else:
                            AfaDBFunc.CommitSql()
                    
                    #=====发送回执====
                    AfaLoggerFunc.tradeDebug('>>>发送成功回执到对方行')
               
                    #=====为返回冲销成功发送成功回执====
                    TradeContext.MSGTYPCO = 'SET010'                 #报文类代码
                    #TradeContext.PRCCO    = 'RCCI0000'               #中心返回码
                    #TradeContext.STRINFO  = '原业务冲正成功'         #附言
                    TradeContext.ORMFN    = TradeContext.MSGFLGNO    #参考报文标示号
                    TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #发送成员行号
                    TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #接收成员行号
                    
                    return True
            else:
                #=====往帐业务====
                AfaLoggerFunc.tradeDebug(">>>往帐业务")
                
                #=====发送回执====
                AfaLoggerFunc.tradeDebug('>>>发送拒绝回执到对方行')
                
                #=====为返回冲销成功发送成功回执====
                TradeContext.MSGTYPCO = 'SET010'                 #报文类代码
                TradeContext.PRCCO    = 'RCCO1006'               #中心返回码
                TradeContext.STRINFO  = '往帐业务只能由受理方冲正'     #附言
                TradeContext.ORMFN    = TradeContext.MSGFLGNO    #参考报文标示号
                TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #发送成员行号
                TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #接收成员行号
                
    AfaLoggerFunc.tradeInfo("农信银系统：来账.中心类操作(1.本地操作).柜台冲正来账接收[TRCC006_1144]进入")
    
    return True
def SubModuleDoSnd( ):
    AfaLoggerFunc.tradeInfo("农信银系统：来账.中心类操作(2.中心回执).柜台冲正来账接收[TRCC006_1144]进入")
    AfaLoggerFunc.tradeDebug(">>>errorCode[" + TradeContext.errorCode + "]")
    
    #=====判断afe返回结果====
    if TradeContext.errorCode == '0000':
        AfaLoggerFunc.tradeInfo('>>>发送回执报文成功')
    else:
        AfaLoggerFunc.tradeInfo('>>>发送回执报文失败')
    
    AfaLoggerFunc.tradeInfo("农信银系统：来账.中心类操作(2.中心回执).柜台冲正来账接收[TRCC006_1144]进入")
    
    return True                                 
