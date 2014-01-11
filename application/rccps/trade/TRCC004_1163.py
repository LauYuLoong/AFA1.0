# -*- coding: gbk -*-
###############################################################################
#   农信银系统：往账.回执类操作模板(1.回执操作).补正应答报文
#==============================================================================
#   交易文件:   TRCC004_1163.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘雨龙
#   修改时间:   2008-12-04
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsDBTrcc_atcbka,rccpsDBTrcc_spbsta,rccpsDBTrcc_wtrbka
import rccpsHostFunc,rccpsGetFunc,rccpsUtilTools,AfaAfeFunc

#=====================回执个性化处理(本地操作)=================================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统: 往账.本地类操作交易[RCC004_1163]进入***' )

    #=====判断是否存在自动冲正报文====
    AfaLoggerFunc.tradeDebug('>>>判断是否存在自动冲正报文')

    atcbka_where={'ORMFN':TradeContext.MSGFLGNO}
    atcbka_dict  = rccpsDBTrcc_atcbka.selectu(atcbka_where)

    if( len(atcbka_dict) > 0 ):
        #=====冲销业务存在自动冲正报文,更新表数据为冲销失败,回复冲销失败报文====
        AfaLoggerFunc.tradeDebug('>>>已存在自动冲正报文,抛弃报文')
        return AfaFlowControl.ExitThisFlow('S999','存在自动冲正报文，抛弃报文')
    else:
        AfaLoggerFunc.tradeDebug('>>>未查找到针对补正报文的自动冲正报文,流程继续')

    #=====判断原补正交易是否存在====
    AfaLoggerFunc.tradeDebug('>>>判断是否存在原补正报文')

    wtrbka_where={'MSGFLGNO':TradeContext.ORMFN}
    wtrbka_dict = rccpsDBTrcc_wtrbka.selectu(wtrbka_where)

    wtrbka_temp_dict = wtrbka_dict

    if len(wtrbka_dict) <= 0:
        AfaLoggerFunc.tradeDebug('>>>未找到原补正报文，抛弃报文，不做任何处理')
        return AfaFlowControl.ExitThisFlow('S999','未找到原补正报文，抛弃报文，不做任何处理')
    else:
        AfaLoggerFunc.tradeDebug('>>>找到原补正报文，继续流程处理')

    #=====查找原业务====
    AfaLoggerFunc.tradeDebug('>>>查询原业务')

    wtrbka_where={'BJEDTE':wtrbka_dict['NOTE1'],'BSPSQN':wtrbka_dict['NOTE2']}
    wtrbka_dict = rccpsDBTrcc_wtrbka.selectu(wtrbka_where)

    if len(wtrbka_dict) <= 0:
        AfaLoggerFunc.tradeDebug('>>>未找到原业务，抛弃报文，不做任何处理')
        return AfaFlowControl.ExitThisFlow('S999','未找到原业务，抛弃报文，不做任何处理')
    else:
        AfaLoggerFunc.tradeDebug('>>>找到原业务，继续流程处理')

    #=====查找原业务状态====
    AfaLoggerFunc.tradeDebug('>>>查找原业务状态')

    spb_where = {'BJEDTE':wtrbka_dict['BJEDTE'],'BSPSQN':wtrbka_dict['BSPSQN']}
    spb_dict  = rccpsDBTrcc_spbsta.selectu(spb_where)

    if len(spb_dict) <= 0:
        AfaLoggerFunc.tradeDebug('>>>查找原业务状态失败，抛弃报文，不做任何处理')
        return AfaFlowControl.ExitThisFlow('S999','查找原业务状态失败，抛弃报文，不做任何处理')
    else:
        AfaLoggerFunc.tradeDebug('>>>查找原业务状态成功，继续流程处理')

    #=====判断原业务状态是否允许进行补正账务补录====
    if spb_dict['BCSTAT'] != PL_BCSTAT_CANC and spb_dict['BDWFLG'] != PL_BDWFLG_SUCC:
        AfaLoggerFunc.tradeDebug('>>>原业务状态['+str(spbsta_dict['BCSTAT'])+'不允许补正，抛弃报文，不做任何处理')
        return AfaFlowControl.ExitThisFlow('S999','原业务不允许补正，抛弃报文，不做任何处理')
    else:
        AfaLoggerFunc.tradeDebug('>>>原业务进入补正账务流程处理')
        
    #=================若应答报文回复拒绝,则设置状态为拒绝,停止处理=============
    if TradeContext.PRCCO != 'RCCI0000':
        AfaLoggerFunc.tradeInfo(">>>对方返回拒绝应答")
        
        #=============设置业务状态为拒绝处理中=================================
        
        if not rccpsState.newTransState(wtrbka_temp_dict['BJEDTE'],wtrbka_temp_dict['BSPSQN'],PL_BCSTAT_MFERFE,PL_BDWFLG_SUCC):
            return AfaFlowControl.ExitThisFlow('S999',"设置业务状态为拒绝处理中异常")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit异常")
            
        return AfaFlowControl.ExitThisFlow("S999","对方拒绝,停止处理")
    else:
        AfaLoggerFunc.tradeInfo(">>>对方返回成功应答")

    #=====记账接口8813I1赋值操作====
    TradeContext.HostCode  =  '8813'
    TradeContext.BESBNO    =  wtrbka_dict['BESBNO']          #机构号
    TradeContext.BETELR    =  wtrbka_dict['BETELR']          #柜员号
    TradeContext.TERMID    =  wtrbka_dict['TERMID']          #终端号
    TradeContext.BJEDTE    =  wtrbka_dict['BJEDTE']          #交易日期
    TradeContext.BSPSQN    =  wtrbka_dict['BSPSQN']          #报单序号

    #=====判断交易代码，进行账务补正====
    if TradeContext.ORTRCCO in ('3000002','3000004'):
        #=====通存====
        AfaLoggerFunc.tradeDebug('>>>通存业务补正')
    elif TradeContext.ORTRCCO in ('3000102','3000104'):
        #=====通兑====
        AfaLoggerFunc.tradeDebug('>>>通兑业务补正')

        if( wtrbka_dict['CHRGTYP'] != '1'):
            TradeContext.RCCSMCD  = PL_RCCSMCD_XJTDWZ                     #主机摘要代码
            TradeContext.RBAC =  ''                       #借方账户:付款人账户
            TradeContext.RBNM =  '现金'                       #借方户名 付款人户名
            TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_NXYDQSWZ     #贷方账户:农信银待清算来账
            TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
            TradeContext.ACNM = '农信银待清算来账'                        #贷方户名:
            TradeContext.CTFG =  '7'                                      #本金 手续费标识  7 本金 8手续费 9 本金＋手续费
            TradeContext.PKFG =  'T'                                      #通存通兑标识
            TradeContext.CATR =  '0'                                      #现金

            AfaLoggerFunc.tradeInfo( '借方账号:' + TradeContext.SBAC )
            AfaLoggerFunc.tradeInfo( '贷方账号:' + TradeContext.RBAC )

        else:
            #=====转账====
            TradeContext.ACUR    =  '3'                                           #记账次数
            TradeContext.I3TRAM  =  str(TradeContext.CUSCHRG)                       #发生额
            TradeContext.I2TRAM  =  str(TradeContext.OCCAMT)                       #发生额
            TradeContext.OCCAMT  =  rccpsUtilTools.AddDot(TradeContext.OCCAMT,TradeContext.CUSCHRG) #发生额

            #=========交易金额+手续费===================
            TradeContext.RCCSMCD    =  PL_RCCSMCD_XJTDWZ                               #摘要代码
            TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
            TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
            TradeContext.ACNM    =  '待解临时款项'                                #借方户名
            TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
            TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
            TradeContext.OTNM    =  '农信银来账'                                  #贷方户名
            TradeContext.CTFG  = '9'                                              #本金 手续费标识  7 本金 8手续费 9 本金＋手续费
            TradeContext.PKFG  = 'T'                                              #通存通兑标识
            AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:借方账号' + TradeContext.SBAC )
            AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:贷方账号' + TradeContext.RBAC )
            #=========交易金额============
            TradeContext.I2SMCD  =  PL_RCCSMCD_XJTDWZ                               #摘要代码
            TradeContext.I2RBAC  =  ''                           #借方账号
            TradeContext.I2ACNM  =  TradeContext.PYRNAM                           #借方户名
            TradeContext.I2SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
            TradeContext.I2SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
            TradeContext.I2CTFG  = '7'                                            #本金 手续费标识  7 本金 8手续费 9 本金＋手续费
            TradeContext.I2PKFG  = 'T'                                            #通存通兑标识
            TradeContext.I2CATR =  '0'                                      #现金
            AfaLoggerFunc.tradeInfo( '>>>交易金额:借方账号' + TradeContext.I2SBAC )
            AfaLoggerFunc.tradeInfo( '>>>交易金额:贷方账号' + TradeContext.I2RBAC )
            #=========结算手续费收入户===========
            TradeContext.I3SMCD  =  PL_RCCSMCD_SXF                                #摘要代码
            TradeContext.I3SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #借方账号
            TradeContext.I3ACNM  =  TradeContext.PYRNAM                           #借方户名
            TradeContext.I3RBAC  =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #贷方账号
            TradeContext.I3RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
            TradeContext.I3SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
            TradeContext.I3OTNM  =  '待解临时款项'                                #贷方户名
            TradeContext.I3CTFG  = '8'                                              #本金 手续费标识  7 本金 8手续费 9 本金＋手续费
            TradeContext.I3PKFG  = 'T'                                              #通存通兑标识
            AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:借方账号' + TradeContext.I3SBAC )
            AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:贷方账号' + TradeContext.I3RBAC )

    elif TradeContext.ORTRCCO in ('3000003','3000005'):
        #=====本转异====
        AfaLoggerFunc.tradeDebug('>>>本转异业务补正')
    elif TradeContext.ORTRCCO in ('3000103','3000105'):
        #=====异转本====
        AfaLoggerFunc.tradeDebug('>>>异转本业务补正')

        #=====判断手续费收取方式====
        if wtrbka_dict['CHRGTYP'] == '1':
            #=====转账====
            TradeContext.ACUR    =  '3'                                     #记账次数
            TradeContext.I3TRAM  =  str(TradeContext.CUSCHRG)                      #发生额 手续费
            TradeContext.I2TRAM  =  str(TradeContext.OCCAMT)                       #发生额 本金
            TradeContext.OCCAMT  =  str(float(TradeContext.OCCAMT) + float(TradeContext.CUSCHRG)) #发生额
            #=========交易金额+手续费===================
            TradeContext.RCCSMCD =  PL_RCCSMCD_YZBWZ                              #摘要代码  PL_RCCSMCD_YZBWZ 异转本
            TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
            TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
            TradeContext.ACNM    =  '农信银往账'                                  #借方户名
            TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS           #贷方账号
            TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
            TradeContext.OTNM    =  '应解汇款'                                    #贷方户名
            TradeContext.CTFG  = '9'                                              #本金 手续费标识  7 本金 8手续费 9 本金＋手续费
            TradeContext.PKFG  = 'T'                                              #通存通兑标识
            AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:借方账号' + TradeContext.SBAC )
            AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:贷方账号' + TradeContext.RBAC )
            #=========交易金额============
            TradeContext.I2SMCD  =  PL_RCCSMCD_YZBWZ                              #摘要代码
            TradeContext.I2SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #借方账号
            TradeContext.I2SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
            TradeContext.I2ACNM  =  '应解汇款'                                    #借方户名
            TradeContext.I2RBAC  =  TradeContext.PYEACC                           #贷方账号
            TradeContext.I2OTNM  =  TradeContext.PYENAM                           #贷方户名
            TradeContext.I2CTFG  = '7'                                              #本金 手续费标识  7 本金 8手续费 9 本金＋手续费
            TradeContext.I2PKFG  = 'T'                                              #通存通兑标识
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
            TradeContext.I3CTFG  = '8'                                              #本金 手续费标识  7 本金 8手续费 9 本金＋手续费
            TradeContext.I3PKFG  = 'T'                                              #通存通兑标识
        else:
            #=====不收费或者现金====
            TradeContext.ACUR    =  '1'                                           #记账次数
            TradeContext.RCCSMCD =  PL_RCCSMCD_YZBWZ                                #摘要代码
            TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
            TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
            TradeContext.RBAC    =  TradeContext.PYEACC                           #贷方账号
            TradeContext.OTNM    =  TradeContext.PYENAM                           #贷方户名
            TradeContext.CTFG  = '7'                                              #本金 手续费标识  7 本金 8手续费 9 本金＋手续费
            TradeContext.PKFG  = 'T'                                              #通存通兑标识
    else:
        #=====原交易代码错，抛弃报文====
        AfaLoggerFunc.tradeDebug('>>>原交易代码错，抛弃报文')
        return AfaFlowControl.ExitThisFlow('S999','原交易代码错，抛弃报文')

    #=====重新生成前置流水号====
    if rccpsGetFunc.GetRBSQ(PL_BRSFLG_SND) == -1 :
        return AfaFlowControl.ExitThisFlow('S999','重新生成前置流水号失败,抛弃报文')

    #=====modify  by pgt 12-8====
    if wtrbka_temp_dict['DCFLG'] == PL_DCFLG_DEB:
#    if TradeContext.ORTRCCO in ('3000102','3000104','3000103','3000105'):
        #=====通兑、异转本====
        if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_AUTOPAY,PL_BDWFLG_WAIT):
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('S999','新增自动扣款－处理中失败，抛弃报文')
        else:
            AfaDBFunc.CommitSql()

        #=====向主机发起记账====
        rccpsHostFunc.CommHost( TradeContext.HostCode )

        #=====判断主机返回====
        sstlog_dict={}
        sstlog_dict['BJEDTE']  =  TradeContext.BJEDTE
        sstlog_dict['BSPSQN']  =  TradeContext.BSPSQN
        sstlog_dict['BCSTAT']  =  PL_BCSTAT_AUTOPAY
        if TradeContext.errorCode == '0000':
            sstlog_dict['BDWFLG'] =  PL_BDWFLG_SUCC
            sstlog_dict['RBSQ']   =  TradeContext.RBSQ
            sstlog_dict['TLSQ']   =  TradeContext.TLSQ
            sstlog_dict['TRDT']   =  TradeContext.TRDT
            sstlog_dict['MGID']   =  TradeContext.errorCode
            sstlog_dict['STRINFO']=  '主机补正记账成功'
            AfaLoggerFunc.tradeInfo('>>>补正记账成功')
        else:
            sstlog_dict['BDWFLG'] =  PL_BDWFLG_FAIL
            sstlog_dict['MGID']   =  TradeContext.errorCode
            sstlog_dict['STRINFO']=  TradeContext.errorMsg
            AfaLoggerFunc.tradeInfo('>>>补正记账失败')

        if not rccpsState.setTransState(sstlog_dict):
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('S999','修改自动扣款－成功中失败，抛弃报文')
        else:
            AfaDBFunc.CommitSql()
    else:
        #====通存、本转异====
        AfaLoggerFunc.tradeDebug('>>>新增确认付款－处理中')

        if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_CONFACC,PL_BDWFLG_SUCC):
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('S999','新增确认付款－处理中失败，抛弃报文')
        else:
            AfaDBFunc.CommitSql()

        #=================为存款确认请求报文做准备=================================
        AfaLoggerFunc.tradeInfo(">>>开始为存款确认请求报文做准备")

        #=====================获取中心流水号====================================
        if rccpsGetFunc.GetRccSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )

        TradeContext.MSGTYPCO = 'SET009'
        TradeContext.SNDSTLBIN = TradeContext.RCVMBRCO
        TradeContext.RCVSTLBIN = TradeContext.SNDMBRCO
        TradeContext.SNDBRHCO = TradeContext.BESBNO
        TradeContext.SNDCLKNO = TradeContext.BETELR
        TradeContext.ORMFN    = TradeContext.ORMFN 
        TradeContext.OPRTYPNO = '30'
        TradeContext.ROPRTPNO = '30'
        TradeContext.TRANTYP  = '0'
        TradeContext.ORTRCCO  = '3000505' 
        TradeContext.ORTRCNO  = TradeContext.TRCNO
        TradeContext.TRCCO    = '3000503'
        TradeContext.TRCNO    = TradeContext.SerialNo
        TradeContext.CURPIN   = ""
        TradeContext.STRINFO  = '收到补正应答,自动发送存款确认'

        AfaLoggerFunc.tradeInfo(">>>交易代码["+str(TradeContext.TRCCO)+"]")
        AfaLoggerFunc.tradeInfo(">>>结束为存款确认请求报文做准备")
 
        #=====更新原记录的存款确认字段====
        #=====modify by pgt 12-8====
        wtr_up_where = {'BJEDTE':wtrbka_temp_dict['BJEDTE'],'BSPSQN':wtrbka_temp_dict['BSPSQN']}
#        wtr_up_where = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}
        wtr_end_dict = {}
        wtr_end_dict['COTRCDAT']  = TradeContext.TRCDAT
        wtr_end_dict['COTRCNO']   = TradeContext.TRCNO
        wtr_end_dict['TRCNO']     = TradeContext.ORTRCNO
        wtr_end_dict['COMSGFLGNO']= TradeContext.SNDBNKCO+TradeContext.TRCDAT+TradeContext.TRCNO
        wtr_end_dict['MSGFLGNO']  = TradeContext.MSGFLGNO

        rccpsDBTrcc_wtrbka.update(wtr_end_dict,wtr_up_where)
        AfaDBFunc.CommitSql()

        AfaAfeFunc.CommAfe()
 
        if TradeContext.errorCode == '0000':
            AfaLoggerFunc.tradeInfo('>>>发送成功')
        else:
            AfaLoggerFunc.tradeInfo('>>>发送失败')

    return True
