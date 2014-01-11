# -*- coding: gbk -*-
###################################################################
#    农信银系统.汇兑来账接收交易.委托收款接收
#==================================================================
#    程序文件：  TRCC005_1102.py
#    修改时间：  2008-6-5
#    作    者：  刘雨龙
#==================================================================
#    修改时间：  20080730
#    修改者  ：  关彬捷
#    修改内容:   因屏蔽掉模板中TRCDAT时间,所有外发的委托日期从BJEDTE取
#==================================================================
#    功    能：  收到汇兑来账交易后，进行必要性检查、记录到数据库内
#		 ，向主机发起记账，调用afe发送通讯回执
###################################################################
import TradeContext,AfaLoggerFunc, AfaFlowControl,miya,AfaAfeFunc,HostContext
import TransBillFunc, AfaFunc, rccpsDBFunc,rccpsHostFunc,rccpsEntries
import rccpsMap1101CTradeContext2Dtrcbka_dict,rccpsMap0000Dout_context2CTradeContext
import rccpsDBTrcc_trcbka,AfaDBFunc,rccpsState,rccpsGetFunc,rccpsDBTrcc_subbra

from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( "====开始汇兑来账接收处理====" )

    #=====判断是否重复交易====
    sel_dict = {'TRCNO':TradeContext.TRCNO,'TRCDAT':TradeContext.TRCDAT,'SNDBNKCO':TradeContext.SNDBNKCO}
    record = rccpsDBTrcc_trcbka.selectu(sel_dict)
    if record == None:
        return AfaFlowControl.ExitThisFlow('S999','判断是否重复报文，查询汇兑业务登记簿相同报文异常')
    elif len(record) > 0:
        AfaLoggerFunc.tradeInfo('汇兑业务登记簿中存在相同数据,重复报文,进入下一流程')
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

    #====开始向字典赋值====
    trcbka_dict = {}
    if not rccpsMap1101CTradeContext2Dtrcbka_dict.map(trcbka_dict):
        return AfaFlowControl.ExitThisFlow('M999', '字典赋值出错')

    trcbka_dict['DCFLG'] = PL_DCFLG_CRE                  #借贷标识
    trcbka_dict['OPRNO'] = '01'                          #业务属性

    #=====开始插入数据库====
    if not rccpsDBFunc.insTransTrc(trcbka_dict):
        #=====RollBack操作====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow('D002', '插入数据库出错,RollBack成功')
    else:
        #=====commit操作====
        AfaDBFunc.CommitSql()
        AfaLoggerFunc.tradeInfo('插入汇兑业务登记簿，COMMIT成功')

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
        
    ##========================= START 张恒 增加于20091011 来帐落机构及入帐挂账处理  =====================##
    #初始化记挂账标识,记账.0,挂账.1,默认记账
    accflag = 0
    #接收机构暂存
    TradeContext.BESBNOFIRST = TradeContext.BESBNO
    
    if accflag == 0:
        AfaLoggerFunc.tradeInfo(">>>开始校验密押")
        #=====开始调用密押服务器进行核押====
        SNDBANKCO  = TradeContext.SNDBNKCO
        RCVBANKCO  = TradeContext.RCVBNKCO
        SNDBANKCO = SNDBANKCO.rjust(12,'0')
        RCVBANKCO = RCVBANKCO.rjust(12,'0')
        AMOUNT = TradeContext.OCCAMT.split('.')[0] + TradeContext.OCCAMT.split('.')[1]
        AMOUNT = AMOUNT.rjust(15,'0')
        
        AfaLoggerFunc.tradeDebug('AMOUNT=' + str(AMOUNT) )
        AfaLoggerFunc.tradeDebug('SNDBANKCO=' + str(SNDBANKCO) )
        AfaLoggerFunc.tradeDebug('RCVBANKCO=' + str(RCVBANKCO) )

        ret = miya.DraftEncrypt(PL_SEAL_DEC,PL_TYPE_DZHD,TradeContext.TRCDAT,TradeContext.TRCNO,AMOUNT,SNDBANKCO,RCVBANKCO,'',TradeContext.SEAL)

        if ret != 0:
            #密押错,挂账
            AfaLoggerFunc.tradeInfo("密押校验未通过,ret=[" + str(ret) + "]")
            accflag = 1
            TradeContext.NOTE3 = "密押错,挂账!"
        else:
            #密押校验通过
            AfaLoggerFunc.tradeInfo("密押校验通过")
            
        AfaLoggerFunc.tradeInfo(">>>结束校验密押")
        
    #校验账号是否非法
    if accflag == 0:
        AfaLoggerFunc.tradeInfo("开始校验账号是否非法")  
        
        if (len(TradeContext.PYEACC) != 23) and (len(TradeContext.PYEACC) != 19) :
            accflag = 1
            TradeContext.NOTE3 = '此账号不是对公或对私账号,挂账!'
            
        AfaLoggerFunc.tradeInfo("结束校验账号是否非法")

    #调用主机接口查询账户信息
    if accflag == 0:
        #调用8810查询账户信息
        AfaLoggerFunc.tradeInfo("开始查询账户信息")
        
        TradeContext.ACCNO = TradeContext.PYEACC      
        TradeContext.HostCode = '8810'                  
        rccpsHostFunc.CommHost( '8810' )   
        
        if TradeContext.errorCode != '0000':
            accflag = 1
            TradeContext.NOTE3 = '查询收款人信息失败,挂账!'
        elif TradeContext.errorCode == '0000' and len(TradeContext.ACCSO) == 0 :
            accflag = 1
            TradeContext.NOTE3 = '查询收款人开户机构失败,挂账!'
            
        AfaLoggerFunc.tradeInfo("结束查询账户信息")
        
    #校验账户状态是否正常
    if accflag == 0:
        AfaLoggerFunc.tradeInfo("开始校验是否跨法人")     
         
        if TradeContext.ACCSO[0:6] != TradeContext.BESBNO[0:6] :
            accflag = 1
            TradeContext.NOTE3 = '接收行与账户开户行跨法人,挂账!'
            
        AfaLoggerFunc.tradeInfo("结束校验是否跨法人")
        
    #校验开户机构是否建立代理关系
    if accflag == 0:
        AfaLoggerFunc.tradeInfo("开始校验接收行与开户机构是否为同一机构")
        
        if TradeContext.ACCSO != TradeContext.BESBNOFIRST:
            khjg = {}
            khjg['BESBNO'] = TradeContext.ACCSO
            khjg['BTOPSB'] = TradeContext.BESBNOFIRST
            khjg['SUBFLG'] = PL_SUBFLG_SUB                                 
            rec = rccpsDBTrcc_subbra.selectu(khjg)
            if rec == None:
                accflag = 1
                TradeContext.NOTE3 = '查询账户代理关系失败,挂账!'
            elif len(rec) <= 0:
                accflag = 1
                TradeContext.NOTE3 = '账户未建立代理关系,挂账!'
            else:
                #接收机构与开户机构存在代理关系,设置机构号为开户机构号
                TradeContext.BESBNO  =  TradeContext.ACCSO
                
        AfaLoggerFunc.tradeInfo("结束校验接收行与开户机构是否为同一机构")
        
    #校验账号状态是否正常
    if accflag == 0:
        AfaLoggerFunc.tradeInfo("开始校验账号状态是否正常")
        
        if TradeContext.ACCST != '0' and  TradeContext.ACCST != '2':
           accflag = 1
           TradeContext.NOTE3 = '账户状态不正常,挂账!'
           
           #在建立代理关系的情况下,账户状态不正常,同样挂账
           TradeContext.BESBNO  = TradeContext.BESBNOFIRST
           
        AfaLoggerFunc.tradeInfo("结束校验账号状态是否正常")

    #校验收款人户名是否一致
    if accflag == 0:
        AfaLoggerFunc.tradeInfo("开始校验收款人户名是否一致")
        
        if TradeContext.ACCNM != TradeContext.PYENAM :
             accflag = 1
             TradeContext.NOTE3 = '收款人户名不符,挂账!'
             
             #在建立代理关系的情况下,账户状态不正常,同样挂账
             TradeContext.BESBNO  = TradeContext.BESBNOFIRST
           
        AfaLoggerFunc.tradeInfo("结束校验收款人户名是否一致")

    if (TradeContext.existVariable( "PYEACC" ) and len(TradeContext.PYEACC) != 0):       #收款人名称
        TradeContext.PYEACC      = TradeContext.PYEACC
    else:
        TradeContext.PYEACC      = ''
         
    if (TradeContext.existVariable( "PYENAM" ) and len(TradeContext.PYENAM) != 0):       #收款人名称
        TradeContext.OTNM      = TradeContext.PYENAM
    else:
        TradeContext.OTNM      = ''
        
    #汇兑往帐记帐字典赋值
    input_dict = {}
    
    if (TradeContext.existVariable( "PYRNAM" ) and len(TradeContext.PYRNAM) != 0):          #付款人户名
        TradeContext.SBACACNM      =      TradeContext.PYRNAM
        
    input_dict['accflag']     = str(accflag)                                #记挂标志
    input_dict['OCCAMT']      = TradeContext.OCCAMT                         #交易金额
    input_dict['PYEACC']      = TradeContext.PYEACC                         #收款人账号
    input_dict['OTNM']        = TradeContext.OTNM                           #收款人名称
    input_dict['BESBNO']      = TradeContext.BESBNO
        
    #调用汇兑记账接口
    rccpsEntries.HDLZJZ(input_dict)
    
    TradeContext.accflag    = accflag                                    #代理标志

    #=====开始调函数拼贷方账号第25位校验位====
    TradeContext.HostCode = '8813'                                   #调用8813主机接口
    TradeContext.RCCSMCD  = PL_RCCSMCD_HDLZ                          #主机摘要代码：汇兑来账
    TradeContext.ACUR = '1'
    ##========================= END 张恒 增加于20091011 来帐落机构及入帐挂账处理  =====================##

    #=====新增sstlog表状态记录====
    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,TradeContext.BCSTAT,TradeContext.BDWFLG):
        #=====RollBack操作====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow('M999', '设置状态['+TradeContext.BCSTAT+']['+TradeContext.BDWFLG+']失败,系统自动回滚')
    else:
        #=====commit操作====
        AfaDBFunc.CommitSql()

    return True
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('>>>主机记账后处理')
   
    #=====开始向字典赋值====
    sst_dict = {}
    sst_dict['BSPSQN']  = TradeContext.BSPSQN            #报单序号
    sst_dict['BJEDTE']  = TradeContext.BJEDTE            #交易日期
    sst_dict['SBAC']    = TradeContext.SBAC              #借方账号
    sst_dict['BESBNO']  = TradeContext.BESBNO            #机构号
    if (TradeContext.existVariable( "NOTE3" ) and len(TradeContext.NOTE3) != 0):  
        sst_dict['NOTE3']   = TradeContext.NOTE3         #备注3
        AfaLoggerFunc.tradeDebug('>>>test  NOTE3 =['+TradeContext.NOTE3 +']')
    sst_dict['BJETIM']  = TradeContext.BJETIM            #交易时间
    sst_dict['MGID']     = TradeContext.errorCode         #主机返回代码
    sst_dict['STRINFO']  = TradeContext.errorMsg          #主机返回信息
    sst_dict['BETELR']  = TradeContext.BETELR            #柜员号

    #=====开始判断主机返回结果====
    out_context_dict = {}
    
    if TradeContext.errorCode == '0000' :
        AfaLoggerFunc.tradeDebug('>>>主机通讯成功,更新表状态开始')
        trcbka_jgh = {}
        trcbka_where = {}
        trcbka_jgh['BESBNO'] = TradeContext.BESBNO  
        trcbka_where['BSPSQN'] = TradeContext.BSPSQN 
        trcbka_where['BJEDTE'] = TradeContext.BJEDTE
        
        if not rccpsDBTrcc_trcbka.updateCmt( trcbka_jgh,trcbka_where ):
            #=====RollBack操作====
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('D002', '更新数据库出错,RollBack成功')
        else:
            #=====commit操作====
            AfaDBFunc.CommitSql()
            AfaLoggerFunc.tradeInfo('更新登记簿，COMMIT成功')
            
        if (TradeContext.existVariable( "RBAC" ) and len(TradeContext.RBAC) != 0):  
            sst_dict['RBAC']   = TradeContext.RBAC                 
            AfaLoggerFunc.tradeDebug('>>>test  RBAC =['+TradeContext.RBAC +']')
        if (TradeContext.existVariable( "REAC" ) and len(TradeContext.REAC) != 0):  
            sst_dict['REAC']   = TradeContext.REAC                 
            AfaLoggerFunc.tradeDebug('>>>test  REAC =['+TradeContext.REAC +']')

        #自动挂账
        if TradeContext.accflag == 1 :
            sst_dict['BCSTAT']  = PL_BCSTAT_HANG                #自动挂账
            AfaLoggerFunc.tradeDebug('>>>test  BCSTAT=['+str(sst_dict['BCSTAT']) +']')
        #自动入账
        elif TradeContext.accflag == 0 :
            sst_dict['BCSTAT']  = PL_BCSTAT_AUTO                 #自动入账 
            AfaLoggerFunc.tradeDebug('>>>test  BCSTAT=['+str(sst_dict['BCSTAT']) +']')
        if (TradeContext.existVariable( "DASQ" ) and len(TradeContext.DASQ) != 0):  
           sst_dict['DASQ']    = TradeContext.DASQ              #销账序号
           AfaLoggerFunc.tradeDebug('>>>test  DASQ  =['+TradeContext.DASQ +']')
        sst_dict['BDWFLG']  = PL_BDWFLG_SUCC                 #成功
        AfaLoggerFunc.tradeDebug('>>>test  BDWFLG=['+str(sst_dict['BDWFLG']) +']')
        sst_dict['TRDT']    = TradeContext.TRDT              #主机日期
        AfaLoggerFunc.tradeDebug('>>>test  TRDT  =['+TradeContext.TRDT   +']')
        sst_dict['TLSQ']    = TradeContext.TLSQ              #主机流水
        AfaLoggerFunc.tradeDebug('>>>test  TLSQ  =['+TradeContext.TLSQ   +']')
        
        AfaLoggerFunc.tradeDebug('>>>主机通讯成功,更新表状态结束')
        
        out_context_dict['PRCCO']    = 'RCCI0000'
        out_context_dict['STRINFO']  = '成功'
        
    else :    
        if TradeContext.accflag == 1 :
            sst_dict['BCSTAT']  = PL_BCSTAT_HANG                            #自动挂账
            sst_dict['BDWFLG']  = PL_BDWFLG_FAIL                            #处理失败
            
            out_context_dict['PRCCO']    = 'RCCI1056'
            out_context_dict['STRINFO']  = '挂账失败,交易失败'
        
        elif TradeContext.accflag == 0 :
            #记账失败,挂代理机构账
            TradeContext.BESBNO = TradeContext.BESBNOFIRST
            #汇兑来帐挂帐字典赋值
            input_dict = {}
            input_dict['accflag']     = str(TradeContext.accflag)                   #记挂标志
            input_dict['OCCAMT']      = TradeContext.OCCAMT                         #交易金额
            input_dict['BESBNO']      = TradeContext.BESBNOFIRST
                
            #调用汇兑记账接口
            rccpsEntries.HDLZGZ(input_dict)
            
            rccpsHostFunc.CommHost( '8813' )
            
            sst_dict = {}
            sst_dict['BSPSQN']  = TradeContext.BSPSQN            #报单序号
            AfaLoggerFunc.tradeDebug('>>>test  BSPSQN=['+TradeContext.BSPSQN+']')
            sst_dict['BJEDTE']  = TradeContext.BJEDTE            #交易日期
            AfaLoggerFunc.tradeDebug('>>>test  BJEDTE=['+TradeContext.BJEDTE+']')
            sst_dict['SBAC']    = TradeContext.SBAC              #借方账号
            AfaLoggerFunc.tradeDebug('>>>test  SBAC=['+TradeContext.SBAC+']')
            sst_dict['BESBNO']  = TradeContext.BESBNO            #机构号
            AfaLoggerFunc.tradeDebug('>>>test  BESBNO=['+TradeContext.BESBNO+']')
            if (TradeContext.existVariable( "NOTE3" ) and len(TradeContext.NOTE3) != 0):  
                sst_dict['NOTE3']   = TradeContext.NOTE3         #备注3
                AfaLoggerFunc.tradeDebug('>>>test  NOTE3 =['+TradeContext.NOTE3 +']')
            sst_dict['BJETIM']  = TradeContext.BJETIM            #交易时间
            AfaLoggerFunc.tradeDebug('>>>test  BJETIM=['+TradeContext.BJETIM+']')
            sst_dict['MGID']     = TradeContext.errorCode        #主机返回代码
            sst_dict['STRINFO']  = TradeContext.errorMsg         #主机返回信息
            sst_dict['BETELR']  = TradeContext.BETELR            #柜员号
            
            if TradeContext.errorCode == '0000':
                AfaLoggerFunc.tradeDebug(">>>SubModuleDoSnd--挂帐成功")            
                sst_dict['BCSTAT']  = PL_BCSTAT_HANG          
                sst_dict['BDWFLG']  = PL_BDWFLG_SUCC
                
                out_context_dict['PRCCO']    = 'RCCI0000'
                out_context_dict['STRINFO']  = '成功'
                
            else:
                AfaLoggerFunc.tradeDebug(">>>SubModuleDoSnd--挂帐失败")
                sst_dict['BCSTAT']  = PL_BCSTAT_HANG             
                sst_dict['BDWFLG']  = PL_BDWFLG_FAIL
                out_context_dict['PRCCO']    = 'RCCI1056'
                out_context_dict['STRINFO']  = '挂账失败,交易失败'


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
def SubModuleDoTrd():
    #=====判断afe返回结果====
    if TradeContext.errorCode == '0000':
        AfaLoggerFunc.tradeInfo('>>>发送回执报文成功')
    else:
        AfaLoggerFunc.tradeInfo('>>>发送回执报文失败')

    return True
