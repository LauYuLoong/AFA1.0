# -*- coding: gbk -*-
##################################################################
#   农信银.通存通兑来账.柜台冲销来账
#=================================================================
#   程序文件:   TRCC006_1145.py
#   修改时间:   2008-11-05
#   作者：      刘雨龙
##################################################################

import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaAfeFunc,AfaDBFunc
import rccpsDBTrcc_mpcbka,rccpsDBTrcc_wtrbka,rccpsState,rccpsDBTrcc_spbsta,rccpsHostFunc,HostContext
import rccpsMap1145CTradeContext2Dmpcbka_dict,rccpsDBTrcc_atcbka,rccpsDBTrcc_sstlog
from types import *
from rccpsConst import *
import time

def SubModuleDoFst():
    #time.sleep(60)
        
    AfaLoggerFunc.tradeInfo("农信银系统：来账.中心类操作(1.本地操作).柜台冲销来账接收[TRCC006_1145]进入")
    
    #=====判断是否为重复交易====
    AfaLoggerFunc.tradeInfo(">>>判断是否为重复交易")

    where_dict = {}
    where_dict = {'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO,'SNDBNKCO':TradeContext.SNDBNKCO}
    record = rccpsDBTrcc_mpcbka.selectu(where_dict)

    if( record == None ):
        AfaLoggerFunc.tradeDebug(">>>查找冲销登记簿异常,抛弃报文,等待中心发送自动冲正报文")
        return AfaFlowControl.ExitThisFlow('A099',"查找冲销登记簿异常")
    elif( len(record) > 0 ):    #重复交易
        AfaLoggerFunc.tradeDebug(">>>冲销交易重复")
    else:
        AfaLoggerFunc.tradeDebug(">>>非重复交易")
        
        #=====开始登记柜台冲销登记簿====
        AfaLoggerFunc.tradeDebug(">>>开始登记冲销登记簿")

        #TradeContext.ORMFN    = TradeContext.MSGFLGNO    #参考报文标示号
        TradeContext.ORTRCDAT = TradeContext.TRCDAT

        mpcbka_insert_dict = {}
        if not rccpsMap1145CTradeContext2Dmpcbka_dict.map(mpcbka_insert_dict):
            AfaLoggerFunc.tradeDebug("为冲销登记簿字典赋值失败")
            return AfaFlowControl.ExitThisFlow('S999','为字典赋值失败,抛弃报文,等待中心自动冲正')
            
        res = rccpsDBTrcc_mpcbka.insertCmt(mpcbka_insert_dict)      
        if( res == -1):
            AfaLoggerFunc.tradeDebug(">>>登记冲销登记簿失败")
            return AfaFlowControl.ExitThisFlow('S999','插入数据库失败,抛弃报文,等待中心自动冲正')
        
        #=====commit数据====
        AfaDBFunc.CommitSql()

    #=====查找自动冲正登记簿是否存在记录====
    AfaLoggerFunc.tradeDebug(">>>判断是否存在自动冲正报文")

    atcbka_where = {'ORMFN':TradeContext.MSGFLGNO}
    atcbka_dict  = rccpsDBTrcc_atcbka.selectu(atcbka_where)

    if( len(atcbka_dict) > 0 ):
        #=====冲销业务存在自动冲正报文,更新表数据为冲销失败,回复冲销失败报文====
        AfaLoggerFunc.tradeDebug('>>>已存在自动冲正报文,拒绝冲销,回复拒绝报文')
        
        #=====为返回冲销成功发送拒绝回执====
        TradeContext.MSGTYPCO = 'SET010'                 #报文类代码
        TradeContext.PRCCO    = 'NN1IA999'               #中心返回码
        TradeContext.ORMFN    = TradeContext.MSGFLGNO    #参考报文标示号
        TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #发送成员行号
        TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #接收成员行号
        TradeContext.STRINFO  = '原交易已自动冲正,不允许再次冲销'               #附言

        return True
    else:
        AfaLoggerFunc.tradeDebug('>>>未查找到针对冲销报文的自动冲正报文,流程继续')

    #=====查找原交易是否存在====
    AfaLoggerFunc.tradeDebug(">>>查找原交易是否存在")

    where_dict = {'TRCDAT':TradeContext.ORMFN[10:18],'TRCNO':TradeContext.ORTRCNO,'SNDBNKCO':TradeContext.SNDBNKCO}
    wtrbka_dict = rccpsDBTrcc_wtrbka.selectu(where_dict)

    if( wtrbka_dict == -1 ):
        AfaLoggerFunc.tradeInfo(">>>查找原交易失败,原业务中心流水号["+str(TradeContext.ORTRCNO)+"]")
        return AfaFlowControl.ExitThisFlow('A099',"查找原交易失败,抛弃报文,等待中心自动冲正")
        
    if( len(wtrbka_dict) == 0 ):
        #=====未查找到原交易====
        AfaLoggerFunc.tradeDebug(">>>查找原交易失败,未收到原交易,直接回复拒绝报文")
     
        #=====为返回冲销成功发送成功回执====
        TradeContext.MSGTYPCO = 'SET010'                 #报文类代码
        TradeContext.ORMFN    = TradeContext.MSGFLGNO    #参考报文标示号
        TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #发送成员行号
        TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #接收成员行号
        #关彬捷  20081222  修改:如果未找到原业务,则返回拒绝应答
        TradeContext.PRCCO    = 'NN1IA999'               #中心返回码
        TradeContext.STRINFO  = '无此交易'               #附言

        return True
    else:
        #=====查找原交易成功====
        AfaLoggerFunc.tradeInfo(">>>查找原交易成功")

        #=====将原报单序号 原交易日期更新到冲销登记簿中====
        AfaLoggerFunc.tradeInfo('>>>更新原报单序号\原交易日期')

        mpcbka_where={}
        mpcbka_where['BSPSQN'] = TradeContext.BSPSQN      #报单序号
        mpcbka_where['BJEDTE'] = TradeContext.BJEDTE      #交易日期

        mpcbka_dict ={}
        mpcbka_dict['BOJEDT']  = wtrbka_dict['BJEDTE']    #原交易日期
        mpcbka_dict['BOSPSQ']  = wtrbka_dict['BSPSQN']    #原报单序号
        mpcbka_dict['BESBNO']  = wtrbka_dict['BESBNO']    #原机构号
        mpcbka_dict['STRINFO'] = TradeContext.STRINFO     #附言 
        mpcbka_dict['OPRNO']   = PL_TDOPRNO_CX            #业务类型

        ret = rccpsDBTrcc_mpcbka.update(mpcbka_dict,mpcbka_where)

        if ret <= 0:
            AfaDBFunc.RollBackSql( )
            return AfaFlowControl.ExitThisFlow('S999', "更新冲销登记簿原报单序号和原交易日期异常,抛弃报文")
        else:
            AfaDBFunc.CommitSql( )

        AfaLoggerFunc.tradeInfo(">>>结束更新冲销登记簿原交易日期和原报单序号")
        
        #=====查找原来账业务业务状态====
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
            
        #关彬捷  20081226  新增若交易当前状态为自动扣款,自动入账,冲销,冲正处理中状态,则直接拒绝此冲销
        if (spbsta_dict['BCSTAT'] == PL_BCSTAT_AUTO or spbsta_dict['BCSTAT'] == PL_BCSTAT_AUTOPAY or spbsta_dict['BCSTAT'] == PL_BCSTAT_CANC or spbsta_dict['BCSTAT'] == PL_BCSTAT_CANCEL) and  spbsta_dict['BDWFLG'] == PL_BDWFLG_WAIT:
            #=====为返回冲销成功发送拒绝回执====
            TradeContext.MSGTYPCO = 'SET010'                 #报文类代码
            TradeContext.PRCCO    = 'RCCO1006'               #中心返回码
            TradeContext.ORMFN    = TradeContext.MSGFLGNO    #参考报文标示号
            TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #发送成员行号
            TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #接收成员行号
            TradeContext.STRINFO  = '原交易账务状态未知'     #附言

            return True
        
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
                AfaLoggerFunc.tradeInfo(">>>主机返回原交易记账失败,继续冲销")
                
            else:
                AfaLoggerFunc.tradeInfo(">>>查询原交易账务状态异常,返回拒绝应答")
                #=====为返回冲销成功发送拒绝回执====
                TradeContext.MSGTYPCO = 'SET010'                 #报文类代码
                TradeContext.PRCCO    = 'RCCO1006'               #中心返回码
                TradeContext.ORMFN    = TradeContext.MSGFLGNO    #参考报文标示号
                TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #发送成员行号
                TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #接收成员行号
                TradeContext.STRINFO  = '原交易账务状态未知'     #附言
                
                return True

        #=====根据来往帐标识进行冲销状态判断====
        if( wtrbka_dict['BRSFLG'] == PL_BRSFLG_RCV ):
            #=====来账业务====
            AfaLoggerFunc.tradeDebug(">>>来账业务")

            #=====PL_BCSTAT_AUTOPAY  自动扣款====
            #=====PL_BCSTAT_AUTO     自动入账====
            #=====PL_BCSTAT_CONFPAY   确认付款====
            #=====PL_BCSTAT_CONFACC   确认入账====
            #=====PL_BCSTAT_MFERFE   拒绝====
            #=====PL_BCSTAT_CANC     冲销====
            #=====PL_BCSTAT_CANCEL   冲正====
            if( ((spbsta_dict['BCSTAT']==PL_BCSTAT_AUTO or spbsta_dict['BCSTAT']==PL_BCSTAT_AUTOPAY) and spbsta_dict['BDWFLG']==PL_BDWFLG_FAIL) \
                or (spbsta_dict['BCSTAT'] == PL_BCSTAT_MFERFE and spbsta_dict['BDWFLG'] == PL_BDWFLG_SUCC) \
                or (spbsta_dict['BCSTAT'] == PL_BCSTAT_CANC   and spbsta_dict['BDWFLG'] == PL_BDWFLG_SUCC) \
                or (spbsta_dict['BCSTAT'] == PL_BCSTAT_CANCEL and spbsta_dict['BDWFLG'] == PL_BDWFLG_SUCC) \
                or (spbsta_dict['BCSTAT'] == PL_BCSTAT_CONFPAY and spbsta_dict['BDWFLG'] == PL_BDWFLG_SUCC) \
                or (spbsta_dict['BCSTAT'] == PL_BCSTAT_CONFACC and spbsta_dict['BDWFLG'] == PL_BDWFLG_SUCC)):
                #=====不允许冲销====
                AfaLoggerFunc.tradeDebug(">>>原业务["+str(spbsta_dict['BSPSQN'])+"]记账失败或被拒绝,发送成功报文")

                #=====根据交易状态新增冲销-成功状态====
                if spbsta_dict['BCSTAT'] not in (PL_BCSTAT_MFERFE,PL_BCSTAT_CANC,PL_BCSTAT_CANCEL):
                    #=====新增原业务状态为冲销-成功====
                    AfaLoggerFunc.tradeDebug('>>>新增原业务状态为冲销-成功')

                    if not rccpsState.newTransState(spbsta_dict['BJEDTE'],spbsta_dict['BSPSQN'],PL_BCSTAT_CANC,PL_BDWFLG_SUCC):
                        AfaDBFunc.RollBackSql()
                        return AfaFlowControl.ExitThisFlow('S999','设置业务状态为冲销-成功异常')
                    else:
                        AfaDBFunc.CommitSql()
                else:
                    AfaLoggerFunc.tradeDebug('>>>原业务状态为[拒绝/冲销/冲正],不需要新增状态')
    
                #=====为返回冲销成功发送拒绝回执====
                TradeContext.MSGTYPCO = 'SET010'                 #报文类代码
                TradeContext.PRCCO    = 'RCCI0000'               #中心返回码
                TradeContext.ORMFN    = TradeContext.MSGFLGNO    #参考报文标示号
                TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #发送成员行号
                TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #接收成员行号
                TradeContext.STRINFO  = '原业务冲销成功'         #附言

                return True
            else:
        
                #=====直接调用8820冲销原业务====
                status={}
                if not rccpsState.getTransStateCur(spbsta_dict['BJEDTE'],spbsta_dict['BSPSQN'],status):
                    return AfaFlowControl.ExitThisFlow('S999','取原业务主机流水号和日期失败,抛弃报文')

                TradeContext.BOSPSQ   = status['RBSQ']    #原报单序号
                TradeContext.BOJEDT   = status['FEDT']    #原交易日期
                TradeContext.HostCode = '8820'                   #主机交易码
                
                #=====新增原业务状态为冲销-处理中====
                AfaLoggerFunc.tradeDebug('>>>新增原业务状态为冲销-处理中')

                if not rccpsState.newTransState(spbsta_dict['BJEDTE'],spbsta_dict['BSPSQN'],PL_BCSTAT_CANC,PL_BDWFLG_WAIT):
                    AfaDBFunc.RollBackSql()
                    return AfaFlowControl.ExitThisFlow('S999','设置业务状态为冲销-处理中异常')
                else:
                    AfaDBFunc.CommitSql()

                #=====向主机发起8820抹账处理==== 
                AfaLoggerFunc.tradeDebug('>>>向主机发起8820抹账处理')

                rccpsHostFunc.CommHost( TradeContext.HostCode ) 

                #=====判断主机返回====
                sstlog_dict={}
                sstlog_dict['BJEDTE']  =  spbsta_dict['BJEDTE']
                sstlog_dict['BSPSQN']  =  spbsta_dict['BSPSQN']
                sstlog_dict['BCSTAT']  =  PL_BCSTAT_CANC
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
                    sstlog_dict['STRINFO']   =  '来账冲销成功'       #附言
                    TradeContext.PRCCO       =  'RCCI0000'
                    TradeContext.STRINFO     =  '原业务冲销成功'
                else:
                    sstlog_dict['BDWFLG']    =  PL_BDWFLG_FAIL       #流转标识 PL_BDWFLG_FAIL 失败
                    sstlog_dict['MGID']      =  TradeContext.errorCode #主机返回码
                    sstlog_dict['STRINFO']   =  TradeContext.errorMsg  #主机返回信息
                    TradeContext.PRCCO       =  'NN1IA999'
                    TradeContext.STRINFO     =  '原业务冲销失败 ' + TradeContext.errorMsg

                #=====修改原业务状态====
                AfaLoggerFunc.tradeDebug('>>>修改原业务状态')

                res = rccpsState.setTransState(sstlog_dict)

                if( res == False ):
                    AfaDBFunc.RollbackSql()
                    return AfaFlowControl.ExitThisFlow('A099', '更改被冲正的交易状态失败')

                AfaDBFunc.CommitSql( )
                
                #关彬捷 20081226  修改如果冲销失败则回滚冲销前状态
                if TradeContext.errorCode not in ('0000','SXR0010'):
                    #冲销失败,回滚状态为冲销前状态
                    if not rccpsState.newTransState(spbsta_dict['BJEDTE'],spbsta_dict['BSPSQN'],spbsta_dict['BCSTAT'],spbsta_dict['BDWFLG']):
                        AfaDBFunc.RollBackSql()
                        return AfaFlowControl.ExitThisFlow('S999','回滚状态为冲销前状态异常')
                    else:
                        AfaDBFunc.CommitSql()
                        
                    sstlog_dict = {}
                    sstlog_dict['BJEDTE']    =  spbsta_dict['BJEDTE']
                    sstlog_dict['BSPSQN']    =  spbsta_dict['BSPSQN']
                    sstlog_dict['BCSTAT']    =  spbsta_dict['BCSTAT']
                    sstlog_dict['BDWFLG']    =  spbsta_dict['BDWFLG']
                    sstlog_dict['NOTE3']     =  '原业务冲销失败,回滚为冲销前状态'
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
                        return AfaFlowControl.ExitThisFlow('S999','回滚状态为冲销前状态详细信息异常')
                    else:
                        AfaDBFunc.CommitSql()

                #=====发送回执====
                AfaLoggerFunc.tradeDebug('>>>发送成功回执到对方行')
           
                #=====为返回冲销成功发送成功回执====
                TradeContext.MSGTYPCO = 'SET010'                 #报文类代码
                #TradeContext.PRCCO    = 'RCCI0000'               #中心返回码
                #TradeContext.STRINFO  = '原业务冲销成功'         #附言
                TradeContext.ORMFN    = TradeContext.MSGFLGNO    #参考报文标示号
                TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #发送成员行号
                TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #接收成员行号
        else:
            #=====往帐业务====
            AfaLoggerFunc.tradeDebug(">>>往帐业务")

            #=====发送回执====
            AfaLoggerFunc.tradeDebug('>>>发送成功回执到对方行')
           
            #=====为返回冲销成功发送成功回执====
            TradeContext.MSGTYPCO = 'SET010'                 #报文类代码
            TradeContext.PRCCO    = 'RCCO1006'               #中心返回码
            TradeContext.ORMFN    = TradeContext.MSGFLGNO    #参考报文标示号
            TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #发送成员行号
            TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #接收成员行号
            TradeContext.STRINFO  = '往帐业务只能受理方冲销'     #附言

    AfaLoggerFunc.tradeInfo("农信银系统：来账.中心类操作(1.本地操作).柜台冲销来账接收[TRCC006_1145]退出")
    
    return True
                         

def SubModuleDoSnd( ):
    AfaLoggerFunc.tradeInfo("农信银系统：来账.中心类操作(2.中心回执).柜台冲销来账接收[TRCC006_1145]进入")
    AfaLoggerFunc.tradeInfo("errorCode为：" + TradeContext.errorCode)
    
    #=====判断afe返回结果====
    if TradeContext.errorCode == '0000':
        AfaLoggerFunc.tradeInfo('>>>发送回执报文成功')
    else:
        AfaLoggerFunc.tradeInfo('>>>发送回执报文失败')
    
    AfaLoggerFunc.tradeInfo("交易后处理  退出")
    
    AfaLoggerFunc.tradeInfo("农信银系统：来账.中心类操作(2.中心回执).柜台冲销来账接收[TRCC006_1145]退出")
    
    return True                                 
