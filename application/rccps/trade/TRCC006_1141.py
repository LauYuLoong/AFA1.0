# -*- coding: gbk -*-
###############################################################################
#   农信银系统：来账.中心类操作(1.本地操作 2.中心回执).卡异转本来帐
#==============================================================================
#   交易文件:   TRCC006_1141.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  liyj 
#   修改时间:   2008-11-05
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc,jiami
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_wtrbka
import rccpsDBFunc,rccpsState,rccpsHostFunc,rccpsUtilTools,rccpsDBTrcc_pamtbl
import rccpsMap1141CTradeContext2Dwtrbka_dict,rccpsDBTrcc_atcbka


#=====================交易前处理(登记流水,中心前处理)==========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：来账.中心类操作(1.本地操作).卡异转本来帐请求报文接收[TRCC006_1141]进入***' )
    #初始化返回码
    TradeContext.PRCCO = 'RCCI0000'
    TradeContext.STRINFO = "成功"
    
    #判断是否重复报文
    AfaLoggerFunc.tradeInfo(">>>开始判断是否重复报文")
    
    sel_dict = {'COTRCNO':TradeContext.TRCNO,'COTRCDAT':TradeContext.TRCDAT,'SNDBNKCO':TradeContext.SNDBNKCO}
    record = rccpsDBTrcc_wtrbka.selectu(sel_dict)
    
    if record == None:
        AfaLoggerFunc.tradeDebug('>>>判断是否重复扣款确认报文,查询通存通兑业务登记簿相同报文异常')
        TradeContext.PRCCO    = "NN1ID999"
        TradeContext.STRINFO  = "数据库其他错误"
        
    elif len(record) > 0:
        AfaLoggerFunc.tradeInfo('通存通兑业务登记簿中存在相同数据,重复报文,返回拒绝应答报文')
        TradeContext.PRCCO    = 'NN1ISO999'
        TradeContext.STRINFO  = "重复报文"

    AfaLoggerFunc.tradeInfo(">>>结束判断是否重复报文")
    
    
    #登记通存通兑登记簿
    AfaLoggerFunc.tradeInfo(">>>开始登记通存通兑业务登记簿")
    
    #=====币种转换====
    if TradeContext.CUR == 'CNY':
        TradeContext.CUR  = '01'
        
    #=====手续费收取方式=====
    if float(TradeContext.CUSCHRG) > 0.001:
        TradeContext.CHRGTYP = '1'
    else:
        TradeContext.CHRGTYP = '0'    
    
    #====开始向字典赋值====
    if TradeContext.PRCCO == 'RCCI0000':
        wtrbka_dict = {}
        if not rccpsMap1141CTradeContext2Dwtrbka_dict.map(wtrbka_dict):
            AfaLoggerFunc.tradeDebug('>>>字典赋值出错')
            TradeContext.PRCCO    = "NN1ID999"
            TradeContext.STRINFO  = "数据库其他错误"
    
    wtrbka_dict['DCFLG'] = PL_DCFLG_DEB                  #借贷标识
    wtrbka_dict['OPRNO'] = PL_TDOPRNO_YZB                 #业务种类
    
    #=====开始插入数据库====
    if TradeContext.PRCCO == 'RCCI0000':
        if not rccpsDBFunc.insTransWtr(wtrbka_dict):
            AfaLoggerFunc.tradeDebug('>>>登记通存通兑业务登记簿异常')
            TradeContext.PRCCO    = "NN1ID999"
            TradeContext.STRINFO  = "数据库其他错误"
        
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        TradeContext.PRCCO    = "NN1ID999"
        TradeContext.STRINFO  = "数据库其他错误"
        
    AfaLoggerFunc.tradeInfo(">>>结束登记通存通兑业务登记簿")
    
    #设置业务状态为行内收妥成功
    AfaLoggerFunc.tradeInfo(">>>开始设置业务状态为收妥成功")
    
    stat_dict   = {}
    stat_dict['BSPSQN']   = TradeContext.BSPSQN
    stat_dict['BJEDTE']   = TradeContext.BJEDTE
    stat_dict['BCSTAT']   = PL_BCSTAT_BNKRCV
    stat_dict['BDWFLG']   = PL_BDWFLG_SUCC
    
    if TradeContext.PRCCO == 'RCCI0000':
        if not rccpsState.setTransState(stat_dict):
            AfaLoggerFunc.tradeDebug('>>>设置业务状态收妥成功异常')
            TradeContext.PRCCO    = "NN1ID999"
            TradeContext.STRINFO  = "数据库其他错误"
        
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        TradeContext.PRCCO    = "NN1ID999"
        TradeContext.STRINFO  = "数据库其他错误"
        
    AfaLoggerFunc.tradeInfo(">>>结束设置业务状态为收妥成功")
    
    #设置业务状态为自动扣款处理中
    AfaLoggerFunc.tradeInfo(">>>开始设置业务状态为自动扣款处理中")
    
    if TradeContext.PRCCO == 'RCCI0000':
       if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_AUTOPAY,PL_BDWFLG_WAIT):
            AfaLoggerFunc.tradeDebug('>>>设置业务状态为自动扣款处理中异常')
            TradeContext.PRCCO    = "NN1ID999"
            TradeContext.STRINFO  = "数据库其他错误"
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        TradeContext.PRCCO    = "NN1ID999"
        TradeContext.STRINFO  = "数据库其他错误"
        
    AfaLoggerFunc.tradeInfo(">>>开始设置业务状态为自动扣款处理中")
    
    TradeContext.BCSTAT = PL_BCSTAT_AUTOPAY #状态:自动扣款
    TradeContext.BCSTATNM = "自动扣款"
    #进行必要性检查,若校验通过,则返回成功应答报文,若校验未通过,则返回拒绝应答报文
    AfaLoggerFunc.tradeInfo(">>>开始必要性检查")

    #检查冲正登记簿中是否有此笔业务的冲正业务,存在则返回拒绝应答报文,并设置业务状态为冲正处理中
    if TradeContext.PRCCO == 'RCCI0000':
        atcbka_where_dict = {}
        atcbka_where_dict['ORMFN'] = TradeContext.MSGFLGNO

        atcbka_dict = rccpsDBTrcc_atcbka.selectu(atcbka_where_dict)
        
        if atcbka_dict == None:
            AfaLoggerFunc.tradeInfo(">>>查询冲正登记簿异常")
            TradeContext.PRCCO = 'NN1ID999'
            TradeContext.STRINFO = "查询冲正登记簿异常"
            TradeContext.BCSTAT = PL_BCSTAT_MFERFE
            TradeContext.BCSTATNM = "拒绝"
        
        else:
            if len(atcbka_dict) <= 0:
                AfaLoggerFunc.tradeInfo(">>>此交易未被冲正,继续校验")

            else:
                AfaLoggerFunc.tradeInfo(">>>此交易已被冲正,返回拒绝应答报文")
                TradeContext.PRCCO = 'NN1IO307'
                TradeContext.STRINFO = "此交易已被冲正"
                TradeContext.BCSTAT = PL_BCSTAT_MFERFE
                TradeContext.BCSTATNM = "拒绝"
                
    #解密客户密码
    if TradeContext.PRCCO == 'RCCI0000':
        MIMA = '      '
        PIN  = TradeContext.CURPIN
        ACC  = TradeContext.PYRACC
        AfaLoggerFunc.tradeDebug('密码[' + PIN + ']')
        AfaLoggerFunc.tradeDebug('账号[' + ACC + ']')
        ret = jiami.secDecryptPin(PIN,ACC,MIMA)
        if ret != 0:
            AfaLoggerFunc.tradeDebug("ret=[" + str(ret) + "]")
            AfaLoggerFunc.tradeDebug('调用加密服务器失败')
            TradeContext.PRCCO = 'NN1IS999'
            TradeContext.STRINFO = "解密密码失败"
            TradeContext.BCSTAT = PL_BCSTAT_MFERFE
            TradeContext.BCSTATNM = "拒绝"
        else:
            TradeContext.CURPIN = MIMA
            AfaLoggerFunc.tradeDebug('密码new[' + TradeContext.CURPIN + ']')
    
    
    #唐斌新增#
    sql = "SELECT ischkactname,ischklate FROM rcc_chlabt where transcode='"+TradeContext.TransCode+"' and channelno= '"+(TradeContext.SNDCLKNO)[6:8]+"'"
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql( sql)
    if (records == None):
        return False
    elif (len(records) == 0):
        AfaLoggerFunc.tradeDebug("查询结果为空,查询条件[" + sql + "]")
        return False
    AfaLoggerFunc.tradeDebug(str(records))
    
    #校验账户状态是否正常和账号户名是否相符
    if TradeContext.PRCCO == 'RCCI0000':
    
        #调用主机接口查询账户信息
        TradeContext.HostCode = '8810'
        
        TradeContext.ACCNO = TradeContext.PYRACC
        
        AfaLoggerFunc.tradeDebug("gbj test :" + TradeContext.ACCNO)
        
        rccpsHostFunc.CommHost( TradeContext.HostCode )
        
        if TradeContext.errorCode != '0000':
            #return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
            AfaLoggerFunc.tradeInfo("查询账户信息异常,主机返回码[" + TradeContext.errorCode + "],主机返回信息[" + TradeContext.errorMsg +"]")
            TradeContext.PRCCO = rccpsDBFunc.HostErr2RccErr(TradeContext.errorCode)
            TradeContext.STRINFO = TradeContext.errorMsg
            TradeContext.BCSTAT = PL_BCSTAT_MFERFE
            TradeContext.BCSTATNM = "拒绝"
        
        else:
            #查询成功,更新通存通兑登记簿账务机构号
            AfaLoggerFunc.tradeInfo(">>>查询主机账户成功")
            
            #if( TradeContext.BESBNO != PL_BESBNO_BCLRSB ):
            #    AfaLoggerFunc.tradeInfo(">>>" + TradeContext.BESBNO + ">>>" + TradeContext.ACCSO)
            #    if( TradeContext.BESBNO[:6] != TradeContext.ACCSO[:6] ):
            #        AfaLoggerFunc.tradeInfo(">>>不许跨法人做此交易")
            #        TradeContext.PRCCO = 'NN1IO999'
            #        TradeContext.STRINFO = "接收行与账户开户行不属于同一法人"
            #        TradeContext.BCSTAT = PL_BCSTAT_MFERFE
            #        TradeContext.BCSTATNM = "拒绝"
            
            #检查本机构是否有通存通兑业务权限
            if not rccpsDBFunc.chkTDBESAuth(TradeContext.ACCSO):
                TradeContext.PRCCO = 'NN1IO999'
                TradeContext.STRINFO = "本账户开户机构无通存通兑业务权限"
                TradeContext.BCSTAT = PL_BCSTAT_MFERFE
                TradeContext.BCSTATNM = "拒绝"
            
            AfaLoggerFunc.tradeInfo(">>>开始更新机构号为开户机构")
            TradeContext.BESBNO = TradeContext.ACCSO
            wtrbka_update_dict = {'BESBNO':TradeContext.ACCSO}
            wtrbka_where_dict  = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}
            ret = rccpsDBTrcc_wtrbka.updateCmt(wtrbka_update_dict,wtrbka_where_dict)
            
            if ret <= 0:
                AfaLoggerFunc.tradeInfo(">>>更新机构号为开户机构异常")
                TradeContext.PRCCO = 'NN1ID006'
                TradeContext.STRINFO = "更新账务机构号异常"
                TradeContext.BCSTAT = PL_BCSTAT_MFERFE
                TradeContext.BCSTATNM = "拒绝"
            
            else:
                AfaLoggerFunc.tradeInfo(">>>更新机构号为开户机构成功")
                AfaLoggerFunc.tradeDebug("主机返回户名ACCNM :[" + TradeContext.ACCNM + "]")
                AfaLoggerFunc.tradeDebug("报文接收户名PYRNAM:[" + TradeContext.PYRNAM + "]")
                AfaLoggerFunc.tradeDebug("主机返回账户状态ACCST:[" + TradeContext.ACCST + "]")
                AfaLoggerFunc.tradeDebug("证件类型ACITY:[" + TradeContext.ACITY + "]")
                AfaLoggerFunc.tradeDebug("证件号码ACINO:[" + TradeContext.ACINO + "]")
                
                
                if TradeContext.ACCNM != TradeContext.PYRNAM:
                    #唐斌新增#
                    if(records[0][0]=='1'):
                        AfaLoggerFunc.tradeInfo(">>>账号户名不符")
                        TradeContext.PRCCO = 'NN1IA102'
                        TradeContext.STRINFO = '账号户名不符'
                        TradeContext.BCSTAT = PL_BCSTAT_MFERFE
                        TradeContext.BCSTATNM = "拒绝"
                
                elif TradeContext.ACCST != '0' and TradeContext.ACCST != '2':
                    AfaLoggerFunc.tradeInfo(">>>账户状态不正常")
                    TradeContext.PRCCO = 'NN1IA999'
                    TradeContext.STRINFO = '账户状态不正常'
                    TradeContext.BCSTAT = PL_BCSTAT_MFERFE
                    TradeContext.BCSTATNM = "拒绝"
                    
                elif not (TradeContext.ACCCD == '0428' and TradeContext.ACCEM == '21111'):
                    AfaLoggerFunc.tradeInfo(">>>此账户非个人结算户")
                    TradeContext.PRCCO    = 'NN1IA999'
                    TradeContext.STRINFO  = '此账户非个人结算户'
                    TradeContext.BCSTAT   = PL_BCSTAT_MFERFE
                    TradeContext.BCSTATNM = "拒绝"
                    
                #=====交易金额判断====
                chk_dict = {}
                chk_dict['BPARAD'] = 'TD001'    #通存通兑凭证金额校验
                
                dict = rccpsDBTrcc_pamtbl.selectu(chk_dict) 
                AfaLoggerFunc.tradeInfo('dict='+str(dict))
                
                if dict == None:
                    AfaLoggerFunc.tradeInfo(">>>校验交易金额失败")
                    TradeContext.PRCCO    = 'NN1ID003'
                    TradeContext.STRINFO  = '校验交易金额失败'
                    TradeContext.BCSTAT   = PL_BCSTAT_MFERFE
                    TradeContext.BCSTATNM = "拒绝"
                if len(dict) == 0:
                    AfaLoggerFunc.tradeInfo(">>>查询PAMTBL校验交易金额表记录错误")
                    TradeContext.PRCCO    = 'NN1ID010'
                    TradeContext.STRINFO  = '查询PAMTBL校验交易金额表记录错误'
                    TradeContext.BCSTAT   = PL_BCSTAT_MFERFE
                    TradeContext.BCSTATNM = "拒绝"
                
                #=====判断农信银中心规定校验凭证上线====
                if float(TradeContext.OCCAMT) > float(dict['BPADAT']):
                    #=====交易金额大于农信银中心规定金额，需要输入证件====
                    if TradeContext.existVariable('CERTTYPE') and len(TradeContext.CERTTYPE) == 0:
                        AfaLoggerFunc.tradeInfo(">>>请选择证件类型")
                        TradeContext.PRCCO    = 'NN1IA999'
                        TradeContext.STRINFO  = '请选择证件类型'
                        TradeContext.BCSTAT   = PL_BCSTAT_MFERFE
                        TradeContext.BCSTATNM = "拒绝"
                    elif(TradeContext.CERTTYPE == '06'):
                        if( TradeContext.ACITY != '06' and TradeContext.ACITY != '07' and TradeContext.ACITY != '08' and TradeContext.ACITY != '09'):
                            AfaLoggerFunc.tradeInfo(">>>证件类型错误")
                            TradeContext.PRCCO    = 'NN1IA999'
                            TradeContext.STRINFO  = '证件类型错误'
                            TradeContext.BCSTAT   = PL_BCSTAT_MFERFE
                            TradeContext.BCSTATNM = "拒绝"
                    elif( TradeContext.CERTTYPE != TradeContext.ACITY ):
                        AfaLoggerFunc.tradeInfo(">>>证件类型错误")
                        TradeContext.PRCCO    = 'NN1IA999'
                        TradeContext.STRINFO  = '证件类型错误'
                        TradeContext.BCSTAT   = PL_BCSTAT_MFERFE
                        TradeContext.BCSTATNM = "拒绝"
                        
                    if TradeContext.existVariable('CERTNO')   and len(TradeContext.CERTNO)   == 0:
                        AfaLoggerFunc.tradeInfo(">>>请输入证件号码")
                        TradeContext.PRCCO    = 'NN1IA999'
                        TradeContext.STRINFO  = '请输入证件号码'
                        TradeContext.BCSTAT   = PL_BCSTAT_MFERFE
                        TradeContext.BCSTATNM = "拒绝"
                    elif( TradeContext.CERTNO != TradeContext.ACINO ):
                        AfaLoggerFunc.tradeInfo(">>>证件号码错误")
                        TradeContext.PRCCO    = 'NN1IA999'
                        TradeContext.STRINFO  = '证件号码错误'
                        TradeContext.BCSTAT   = PL_BCSTAT_MFERFE
                        TradeContext.BCSTATNM = "拒绝"
    
    
    #校验交易金额是否超当日限额
    if not rccpsDBFunc.chkLimited(TradeContext.BJEDTE,TradeContext.PYRACC,TradeContext.OCCAMT):
        AfaLoggerFunc.tradeInfo(">>>交易金额超限")
        TradeContext.PRCCO    = 'NN1IA999'
        TradeContext.STRINFO  = '交易金额超限'
        TradeContext.BCSTAT   = PL_BCSTAT_MFERFE
        TradeContext.BCSTATNM = "拒绝"
    
    #校验磁道信息
    if TradeContext.PRCCO == 'RCCI0000':
        #唐斌新增#
        if(records[0][1]=='1'):
            if (TradeContext.SCTRKINF == ''.rjust(37,'0') or TradeContext.SCTRKINF == ''):
                AfaLoggerFunc.tradeInfo("校验磁道信息异常,该业务必须产生磁道信息")
                TradeContext.PRCCO = 'NN1IA141'
                TradeContext.STRINFO = "校验磁道信息失败 :无磁道信息" 
                TradeContext.BCSTAT = PL_BCSTAT_MFERFE
                TradeContext.BCSTATNM = "拒绝"
        if TradeContext.SCTRKINF != ''.rjust(37,'0') and TradeContext.SCTRKINF != '':
            #磁道信息非空或37个零,则调用主机接口校验磁道信息
            TradeContext.HostCode = '0652'
            
            TradeContext.WARNTNO = TradeContext.PYRACC[6:18]
            
            AfaLoggerFunc.tradeDebug("WARNTNO :" + TradeContext.WARNTNO)
            AfaLoggerFunc.tradeDebug("SCTRKINF :" + TradeContext.SCTRKINF)
            AfaLoggerFunc.tradeDebug("THTRKINF :" + TradeContext.THTRKINF)
            if TradeContext.THTRKINF == ''.rjust(37,'0'):
                TradeContext.THTRKINF = ''
                AfaLoggerFunc.tradeDebug("THTRKINF :" + TradeContext.THTRKINF)
            
            rccpsHostFunc.CommHost( TradeContext.HostCode )
            
            if TradeContext.errorCode != '0000':
                #return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
                AfaLoggerFunc.tradeInfo("校验磁道信息异常,主机返回码[" + TradeContext.errorCode + "],主机返回信息[" + TradeContext.errorMsg +"]")
                TradeContext.PRCCO = 'NN1IA141'
                TradeContext.STRINFO = "校验磁道信息失败 " + TradeContext.errorMsg
                TradeContext.BCSTAT = PL_BCSTAT_MFERFE
                TradeContext.BCSTATNM = "拒绝"
                
    AfaLoggerFunc.tradeInfo(">>>结束必要性检查")
    
    #发起主机记账
    AfaLoggerFunc.tradeInfo(">>>开始发起主机记账")
    
    TradeContext.sCertType = TradeContext.CERTTYPE
    TradeContext.sCertNo   = TradeContext.CERTNO
    TradeContext.sOccamt  = TradeContext.OCCAMT
    TradeContext.sCuschrg = TradeContext.CUSCHRG
    
    if TradeContext.PRCCO == 'RCCI0000':
        TradeContext.HostCode = '8813'                               #调用8813主机接口
        #来账对方现金收取手续费
        if( TradeContext.CHRGTYP != '1' ):
        
            TradeContext.RCCSMCD  = PL_RCCSMCD_YZBWZ                      #主机摘要代码
            TradeContext.SBAC = TradeContext.PYRACC                       #借方账户:付款人账户
            TradeContext.ACNM = TradeContext.PYRNAM                       #借方户名 付款人户名
            TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ     #贷方账户:农信银待清算来账
            TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC, 25)
            TradeContext.OTNM = '农信银待清算来账'                        #贷方户名:
            TradeContext.CTFG =  '7'                                      #本金 手续费标识  7 本金 8手续费 9 本金＋手续费 
            TradeContext.PKFG =  'T'                                      #通存通兑标识                                   
            TradeContext.WARNTNO = TradeContext.SBAC[6:18]
            TradeContext.CERTTYPE = ''
            TradeContext.CERTNO = ''
            TradeContext.PASSWD = TradeContext.CURPIN                     #密码
            AfaLoggerFunc.tradeInfo( '借方账号:' + TradeContext.SBAC )
            AfaLoggerFunc.tradeInfo( '贷方账号:' + TradeContext.RBAC )
            AfaLoggerFunc.tradeInfo( '凭证号码:' + TradeContext.WARNTNO )
        else:
            #对方转账收取手续费时s
            TradeContext.ACUR    =  '3'                                           #记账次数
        
            #=========交易金额============
            TradeContext.RCCSMCD  =  PL_RCCSMCD_YZBWZ                               #摘要代码
            TradeContext.SBAC  =  TradeContext.PYRACC                           #借方账号
            TradeContext.ACNM  =  TradeContext.PYRNAM                           #借方户名
            TradeContext.RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
            TradeContext.RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
            TradeContext.OTNM  =  '待解临时款项'                                #贷方户名
            TradeContext.OCCAMT  =  str(TradeContext.sOccamt)                       #发生额
            TradeContext.CTFG  = '7'                                            #本金 手续费标识  7 本金 8手续费 9 本金＋手续费 
            TradeContext.PKFG  = 'T'                                            #通存通兑标识                                   
            TradeContext.WARNTNO = TradeContext.SBAC[6:18]
            TradeContext.PASSWD = TradeContext.CURPIN                     #密码
            TradeContext.sCertType = TradeContext.CERTTYPE
            TradeContext.sCertNo   = TradeContext.CERTNO
            TradeContext.CERTTYPE = ''
            TradeContext.CERTNO = ''
            AfaLoggerFunc.tradeInfo( '>>>交易金额:借方账号' + TradeContext.SBAC )
            AfaLoggerFunc.tradeInfo( '>>>交易金额:贷方账号' + TradeContext.RBAC )
            AfaLoggerFunc.tradeInfo( '>>>交易金额:凭证号码:' + TradeContext.WARNTNO )
            #=========结算手续费收入户===========
            TradeContext.I2SMCD  =  PL_RCCSMCD_SXF                                #摘要代码
            TradeContext.I2SBAC  =  TradeContext.PYRACC                           #借方账号
            TradeContext.I2ACNM  =  TradeContext.PYRNAM                           #借方户名
            TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
            TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
            TradeContext.I2OTNM  =  '待解临时款项'                                #贷方户名
            TradeContext.I2TRAM  =  str(TradeContext.sCuschrg)                      #发生额
            TradeContext.I2CTFG  = '8'                                            #本金 手续费标识  7 本金 8手续费 9 本金＋手续费 
            TradeContext.I2PKFG  = 'T'                                            #通存通兑标识                                   
            TradeContext.I2WARNTNO = TradeContext.I2SBAC[6:18]
            TradeContext.I2PASSWD = TradeContext.CURPIN                     #密码
            AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:借方账号' + TradeContext.I2SBAC )
            AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:贷方账号' + TradeContext.I2RBAC )
            AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:凭证号码:' + TradeContext.WARNTNO )
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
            AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:借方账号' + TradeContext.I3SBAC )
            AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:贷方账号' + TradeContext.I3RBAC )
        
        rccpsHostFunc.CommHost( TradeContext.HostCode )
        
        AfaLoggerFunc.tradeInfo(">>>结束发起主机记账")
        
        #TradeContext.errorCode, TradeContext.errorMsg = '0000', '主机成功'
        
        #根据主机返回码,设置业务状态为自动入账成功或失败
        AfaLoggerFunc.tradeInfo(">>>开始根据主机放回码,设置业务状态为自动入账成功或失败")
        
        stat_dict = {}
        stat_dict['BJEDTE']  = TradeContext.BJEDTE
        stat_dict['BSPSQN']  = TradeContext.BSPSQN
        stat_dict['BESBNO']  = TradeContext.BESBNO
        stat_dict['BETELR']  = TradeContext.BETELR
        stat_dict['SBAC']    = TradeContext.SBAC
        stat_dict['ACNM']    = TradeContext.ACNM
        stat_dict['RBAC']    = TradeContext.RBAC
        stat_dict['OTNM']    = TradeContext.OTNM
        #=====modify by pgt 1129====
        stat_dict['MGID']   = TradeContext.errorCode
        if TradeContext.existVariable('TRDT'):
    	    stat_dict['TRDT'] = TradeContext.TRDT
    	if TradeContext.existVariable('TLSQ'):
    		stat_dict['TLSQ'] = TradeContext.TLSQ
        stat_dict['STRINFO'] = TradeContext.errorMsg
        
        AfaLoggerFunc.tradeInfo("主机返回码[" + TradeContext.errorCode + "],主机返回信息[" + TradeContext.errorMsg +"]")
        if TradeContext.errorCode == '0000':
            #=====发送农信银成功,设置状态为自动入账成功====
            stat_dict['BCSTAT']  = PL_BCSTAT_AUTOPAY
            stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
            TradeContext.PRCCO = 'RCCI0000'
            TradeContext.STRINFO = '成功'
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999', "设置业务状态为自动入账成功异常")
            
            AfaLoggerFunc.tradeInfo(">>>设置业务状态为自动入账成功完成")
        else:
            #=====发送农信银失败,设置状态为拒绝成功====       
            stat_dict['BCSTAT']  = PL_BCSTAT_MFERFE
            stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
            TradeContext.PRCCO = rccpsDBFunc.HostErr2RccErr(TradeContext.errorCode)
            TradeContext.STRINFO = TradeContext.errorMsg
            
            if not rccpsState.setTransState(stat_dict):
                AfaLoggerFunc.tradeFatal( '设置业务状态为拒绝成功异常' )
                TradeContext.PRCCO    = "NN1ID999"
                TradeContext.STRINFO  = "数据库其他错误"
            
            AfaLoggerFunc.tradeInfo(">>>设置业务状态为自动入账失败完成")
    
    else:
        stat_dict = {}
        stat_dict['BJEDTE']  = TradeContext.BJEDTE
        stat_dict['BSPSQN']  = TradeContext.BSPSQN
        stat_dict['BESBNO']  = TradeContext.BESBNO
        stat_dict['BETELR']  = TradeContext.BETELR
        stat_dict['PRCCO']   = TradeContext.PRCCO
        stat_dict['STRINFO'] = TradeContext.STRINFO
        stat_dict['BCSTAT']  = PL_BCSTAT_MFERFE
        stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
        
        if not rccpsState.setTransState(stat_dict):
            AfaLoggerFunc.tradeFatal( '设置业务状态为拒绝成功异常' )
            TradeContext.PRCCO    = "NN1ID999"
            TradeContext.STRINFO  = "数据库其他错误"
            
        AfaLoggerFunc.tradeInfo(">>>设置业务状态为拒绝成功完成")
        
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        TradeContext.PRCCO    = "NN1ID999"
        TradeContext.STRINFO  = "数据库其他错误"
    
    AfaLoggerFunc.tradeInfo(">>>开始根据主机放回码,设置业务状态为自动入账成功或失败")
        
    #为存款确认应答报文赋值
    TradeContext.sysType  = 'rccpst'
    TradeContext.MSGTYPCO = 'SET007'                                          #报文类代码
    #TradeContext.RCVMBRCO = TradeContext.SNDMBRCO                             #接收方成员行号
    TradeContext.RCVSTLBIN = TradeContext.SNDMBRCO                            #收款方成员行号
    TradeContext.SNDSTLBIN = TradeContext.RCVMBRCO                            #付款方成员行号
    TradeContext.SNDBRHCO = TradeContext.BESBNO                               #发起行网点号
    TradeContext.SNDCLKNO = TradeContext.BETELR                               #发起行柜员号
    TradeContext.SNDTRDAT = TradeContext.BJEDTE                               #发起行交易日期
    TradeContext.SNDTRTIM = TradeContext.BJETIM                               #发起行交易时间
    TradeContext.ORMFN    = TradeContext.MSGFLGNO                             #参考报文标识号
    TradeContext.MSGFLGNO = TradeContext.SNDMBRCO + TradeContext.BJEDTE + TradeContext.SerialNo       #报文标识号
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate                          #中心工作日期
    TradeContext.OPRTYPNO = '30'                                              #业务类型
    TradeContext.ROPRTPNO = TradeContext.OPRTYPNO                             #参考业务类型
    TradeContext.TRANTYP  = '0'                                               #传输类型
    TradeContext.CERTTYPE = TradeContext.sCertType
    TradeContext.CERTNO   = TradeContext.sCertNo
    TradeContext.OCCAMT   = TradeContext.sOccamt
    TradeContext.CUSCHRG  = TradeContext.sCuschrg 
    TradeContext.CUR      = 'CNY'                                             #货币符号
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：来账.中心类操作(1.本地操作).卡异转本来帐请求报文接收[TRCC006_1141]退出***' )
    return True


#=====================交易后处理===============================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***农信银系统：来账.中心类操作(2.中心回执).卡异转本来帐请求报文接收[TRCC006_1141]进入***' )
    
    #根据afe返回码判断应答报文是否发送成功,并设置相应业务状态
    AfaLoggerFunc.tradeInfo("TradeContext.errorCode = [" + TradeContext.errorCode + "]")
    if TradeContext.errorCode == '0000':
        AfaLoggerFunc.tradeInfo('>>>发送回执报文成功')
    else:
        AfaLoggerFunc.tradeInfo('>>>发送回执报文失败')
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：来账.中心类操作(2.中心回执).卡异转本来帐请求报文接收[TRCC006_1141]退出***' )
    return True
    
