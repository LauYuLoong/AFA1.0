# -*- coding: gbk -*-
##################################################################
#   农信银.通存通兑来账接收交易.卡 余额查询
#=================================================================
#   程序文件:   TRCC005_1133.py
#   修改时间:   2008-10-21
#   作者：      潘广通
##################################################################

import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaAfeFunc,HostContext,AfaUtilTools
import AfaFunc,rccpsDBFunc
import AfaDBFunc,rccpsState,rccpsGetFunc,rccpsHostFunc
import rccpsDBTrcc_balbka
from types import *
from rccpsConst import *
import jiami

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("'***农信银系统：通存通兑来账接收交易.卡 余额查询[1133] 进入")
    
    #=================初始化返回信息============================================
    if AfaUtilTools.trim(TradeContext.STRINFO) == "":
        TradeContext.STRINFO = rccpsDBFunc.getErrInfo(TradeContext.PRCCO)
        
    AfaLoggerFunc.tradeDebug("TradeContext.STRINFO=" + TradeContext.STRINFO)
    
    AfaLoggerFunc.tradeInfo("交易前处理(登记流水,主机前处理)")
    
    #=====判断是否存在重复交易====
    AfaLoggerFunc.tradeInfo("判断是否存在重复交易")
    balbka_dict = {'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO,'SNDBNKCO':TradeContext.SNDBNKCO}
    record_balbka = rccpsDBTrcc_balbka.selectu(balbka_dict)
    if( record_balbka == None ):
        return AfaFlowControl.ExitThisFlow('A009','判断重复交易时查询余额登记簿失败')
        
    if( len(record_balbka) > 0 ):    #存在重复交易
        AfaLoggerFunc.tradeInfo("存在重复交易")
        
        #====组织应答报文====
        Rcvmbrco = TradeContext.SNDMBRCO
        Sndmbrco = TradeContext.RCVMBRCO
        Ormfn    = TradeContext.MSGFLGNO
                
        #=====报文头====
        TradeContext.MSGTYPCO = 'SET010' #报文类代码
        TradeContext.RCVMBRCO = Rcvmbrco #接受方成员行号
        TradeContext.SNDMBRCO = Sndmbrco #发送方成员行号
        TradeContext.SNDBRHCO = TradeContext.BESBNO         #发起行网点号
        TradeContext.SNDCLKNO = TradeContext.BETELR         #发起行柜员号
        TradeContext.SNDTRDAT = TradeContext.BJEDTE         #发起行交易日期
        TradeContext.SNDTRTIM = TradeContext.BJETIM         #发起行交易时间
        TradeContext.MSGFLGNO = Rcvmbrco+TradeContext.BJEDTE + TradeContext.SerialNo  #报文标示号
        TradeContext.ORMFN    = Ormfn          #参考报文标示号
        TradeContext.NCCWKDAT = TradeContext.NCCworkDate   #中心工作日期
        TradeContext.OPRTYPNO = '30'     #业务类型
        TradeContext.ROPRTPNO = '30'     #参考业务类型
        TradeContext.TRANTYP  = '0'      #传输类型
        #=====业务要素集====
        TradeContext.CURPIN   = "" #异地客户密码   
        TradeContext.PRCCO    = "RCCS1105"  #返回码
        TradeContext.STRINFO  = "重复报文"  #附言
        TradeContext.AVLBAL   = record_balbka['AVLBAL'] #可用余额
        TradeContext.ACCBAL   = record_balbka['ACCBAL'] #账面余额
        
        #=====直接向AFE发送通讯回执====
        AfaLoggerFunc.tradeInfo("直接向AFE发送通讯回执")
        AfaAfeFunc.CommAfe()
        
        AfaLoggerFunc.tradeInfo("重复报文，做丢弃处理")
        
        return AfaFlowControl.ExitThisFlow('A009','重复报文做丢弃处理')
    
##############非重复交易#################################################################
    AfaLoggerFunc.tradeInfo("非重复交易") 
        
    #=====组织登记余额查询查询登记簿的插入字典====
    AfaLoggerFunc.tradeInfo("组织登记余额查询查询登记簿的插入字典")
    insert_dict = {}
    insert_dict['BJEDTE']      = TradeContext.BJEDTE
    insert_dict['BSPSQN']      = TradeContext.BSPSQN
    insert_dict['BRSFLG']      = PL_BRSFLG_RCV
    insert_dict['BESBNO']      = TradeContext.BESBNO  
    insert_dict['BEACSB']      = ""                    #账务机构号
    insert_dict['BETELR']      = TradeContext.BETELR  
    insert_dict['BEAUUS']      = ""                    #授权柜员号
    insert_dict['BEAUPS']      = ""                    #授权柜员密码
    insert_dict['TERMID']      = ""                    #终端号
    insert_dict['OPRNO']       = TradeContext.OPRTYPNO #业务类型
    insert_dict['OPRATTNO']    = ""                    #业务属性
    insert_dict['NCCWKDAT']    = TradeContext.NCCWKDAT #中心工作日期
    insert_dict['TRCCO']       = TradeContext.TRCCO    #交易代码
    insert_dict['TRCDAT']      = TradeContext.TRCDAT   #委托日期
    insert_dict['TRCNO']       = TradeContext.TRCNO    #交易流水号
    insert_dict['MSGFLGNO']    = TradeContext.MSGFLGNO #报文标示号
    insert_dict['SNDMBRCO']    = TradeContext.SNDMBRCO #发送方成员行号
    insert_dict['RCVMBRCO']    = TradeContext.RCVMBRCO #接受方成员行号
    insert_dict['SNDBNKCO']    = TradeContext.SNDBNKCO #发送方行号
    insert_dict['SNDBNKNM']    = TradeContext.SNDBNKNM #发送方行名
    insert_dict['RCVBNKCO']    = TradeContext.RCVBNKCO #接受方行号
    insert_dict['RCVBNKNM']    = TradeContext.RCVBNKNM #接受方行名
    insert_dict['CUR']         = '01'                  #币种
    insert_dict['CHRGTYP']     = ""                    #手续费收取方式
    insert_dict['LOCCUSCHRG']  = ""                    #本地客户手续费
    insert_dict['CUSCHRG']     = TradeContext.CUSCHRG  #异地客户手续费
    insert_dict['PYRACC']      = TradeContext.PYRACC   #付款人账号
    insert_dict['PYEACC']      = TradeContext.PYEACC   #收款人账号
    insert_dict['STRINFO']     = TradeContext.STRINFO  #附言
    insert_dict['CERTTYPE']    = ""                    #证件类型
    insert_dict['CERTNO']      = ""                    #证件号码
    insert_dict['BNKBKNO']     = ""                    #存折号码
    insert_dict['AVLBAL']      = ""                    #可用余额
    insert_dict['ACCBAL']      = ""                    #账面余额
    insert_dict['PRCCO']       = ""                    #返回码
    #insert_dict['PRCINFO']     = ""                    #返回信息
    
    #=====登记查询登记簿====
    AfaLoggerFunc.tradeInfo("开始登记余额查询登记簿")
    res = rccpsDBTrcc_balbka.insertCmt(insert_dict)
    if( res == -1 ):
        return AfaFlowControl.ExitThisFlow('A009','登记余额查询登记簿失败')
        
    #解密客户密码
    MIMA = '      '
    PIN  = TradeContext.CURPIN
    ACC  = TradeContext.PYEACC
    AfaLoggerFunc.tradeDebug('密码[' + PIN + ']')
    AfaLoggerFunc.tradeDebug('账号[' + ACC + ']')
    ret = jiami.secDecryptPin(PIN,ACC,MIMA)
    if ret != 0:
        AfaLoggerFunc.tradeDebug("ret=[" + str(ret) + "]")
        AfaLoggerFunc.tradeDebug('调用加密服务器失败')
    else:
        TradeContext.CURPIN = MIMA
        AfaLoggerFunc.tradeDebug('密码new[' + TradeContext.CURPIN + ']')
    
    #=====调用主机交易，组织调用主机交易所需要的参数====
    AfaLoggerFunc.tradeInfo("为主机交易赋参数")
    TradeContext.HostCode = '8810'
    TradeContext.ACCNO = TradeContext.PYEACC
    TradeContext.PASSWD = TradeContext.CURPIN
    TradeContext.CFFG = '1'
    TradeContext.WARNTNO = TradeContext.PYEACC[6:18]
    
    AfaLoggerFunc.tradeInfo("交易前处理(登记流水,主机前处理)  结束")
    
    return True    
                                 
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo("交易中处理(修改流水,主机后处理,中心前处理)")
    
    AfaLoggerFunc.tradeInfo("errorCode<<<<<<<<<<<"+TradeContext.errorCode)
    AfaLoggerFunc.tradeInfo("errorMsg<<<<<<<<<<"+TradeContext.errorMsg)
    
    #=====判断主机交易是否成功====
    if( TradeContext.errorCode != '0000' ):
        AfaLoggerFunc.tradeInfo("主机交易失败")
        
        TradeContext.PRCCO    = "NN1CA999"  #返回码
        TradeContext.STRINFO  = "主机失败 "+TradeContext.errorMsg[7:]+" "  #附言 
        TradeContext.AVLBAL   = "0.00" #可用余额
        TradeContext.ACCBAL   = "0.00" #账面余额
        
        #=====更新余额查询登记簿====
        AfaLoggerFunc.tradeInfo("组织更新字典")
        where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}
        update_dict = {'STRINFO':TradeContext.STRINFO,'PRCCO':TradeContext.PRCCO}
            
        AfaLoggerFunc.tradeInfo("开始更新余额查询登记簿")
        res = rccpsDBTrcc_balbka.updateCmt(update_dict,where_dict)
        
        if( res == -1 ):
            return AfaFlowControl.ExitThisFlow('A009','更新余额查询登记簿失败')

    else:
        AfaLoggerFunc.tradeInfo("主机交易成功")
        AfaLoggerFunc.tradeDebug("<<<<<<ACCBAL=" + str(HostContext.O1ACBL))
        AfaLoggerFunc.tradeDebug("<<<<<<AVLBAL=" + str(HostContext.O1CUBL))
        TradeContext.PRCCO = "RCCI0000"  #返回码
        TradeContext.STRINFO = "查询成功"  #附言
        TradeContext.ACCBAL = HostContext.O1ACBL #帐户余额
        TradeContext.AVLBAL = HostContext.O1CUBL #可用余额 
        
        ##=====判断是否跨法人====
        #if( TradeContext.BESBNO != PL_BESBNO_BCLRSB ):
        #    if( TradeContext.BESBNO[:6] != TradeContext.ACCSO[:6] ):
        #        AfaLoggerFunc.tradeInfo(">>>不许跨法人做此交易")
        #        TradeContext.PRCCO = 'NN1IO999'
        #        TradeContext.STRINFO = "接收行与账户开户行不属于同一法人"
        #        TradeContext.ACCBAL = '0.00'     #帐户余额
        #        TradeContext.AVLBAL = '0.00'     #可用余额
        
        #=====判断开户机构有无通存通兑权限====
        if not rccpsDBFunc.chkTDBESAuth(TradeContext.ACCSO):
            AfaLoggerFunc.tradeInfo(">>>本账户开户机构无通存通兑业务权限")
            TradeContext.PRCCO = 'NN1IO999'
            TradeContext.STRINFO = "本账户开户机构无通存通兑业务权限"
            TradeContext.ACCBAL = '0.00'     #帐户余额
            TradeContext.AVLBAL = '0.00'     #可用余额
        
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
    
        #=====判断账号与户名是否相符====
        if(TradeContext.PYENAM != HostContext.O1CUNM):
            #唐斌新增#
            if(records[0][0]=='1'):
                TradeContext.PRCCO   = 'NN1IA102'
                TradeContext.STRINFO = "户名与账号不符"
                TradeContext.ACCBAL  = '0.00' #帐户余额
                TradeContext.AVLBAL  = '0.00' #可用余额
        
        #=====判断账户的状态====
        AfaLoggerFunc.tradeInfo("判断账户的状态")
        if( TradeContext.ACCST != "0" ):
            TradeContext.PRCCO = 'NN1IA999'
            TradeContext.STRINFO = "账户状态不正常"
            TradeContext.ACCBAL = '0.00' #帐户余额
            TradeContext.AVLBAL = '0.00' #可用余额
            
        #=====判断是否为个人结算账户====
        if not (TradeContext.ACCCD == '0428' and TradeContext.ACCEM == '21111'):
            AfaLoggerFunc.tradeInfo(">>>此账户非个人结算户")
            TradeContext.PRCCO    = 'NN1IA999'
            TradeContext.STRINFO  = '此账户非个人结算户'
            TradeContext.ACCBAL = '0.00' #帐户余额
            TradeContext.AVLBAL = '0.00' #可用余额
        
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
            
            TradeContext.WARNTNO = TradeContext.PYEACC[6:18]
            
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
                TradeContext.ACCBAL = '0.00' #帐户余额
                TradeContext.AVLBAL = '0.00' #可用余额
        
        #=====更新余额查询登记簿====
        AfaLoggerFunc.tradeInfo("组织更新字典")
        where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}
        update_dict = {'AVLBAL':TradeContext.AVLBAL,'ACCBAL':TradeContext.ACCBAL,\
                       'STRINFO':TradeContext.STRINFO,'PRCCO':TradeContext.PRCCO}
         
        AfaLoggerFunc.tradeInfo("开始更新余额查询登记簿")
        res = rccpsDBTrcc_balbka.updateCmt(update_dict,where_dict)
        
        if( res == -1 ):
            return AfaFlowControl.ExitThisFlow('A009','更新余额查询登记簿失败')
            
    #=====开始给卡余额查询应答报文赋值====
    AfaLoggerFunc.tradeInfo("开始给卡余额查询应答报文赋值")
    
    Rcvmbrco = TradeContext.SNDMBRCO
    Sndmbrco = TradeContext.RCVMBRCO
    Ormfn    = TradeContext.MSGFLGNO
         
    #=====报文头====
    TradeContext.MSGTYPCO = 'SET010' #报文类代码
    TradeContext.RCVSTLBIN = Rcvmbrco #接受方成员行号
    TradeContext.SNDSTLBIN = Sndmbrco #发送方成员行号
    TradeContext.SNDBRHCO = TradeContext.BESBNO         #发起行网点号
    TradeContext.SNDCLKNO = TradeContext.BETELR         #发起行柜员号
    TradeContext.SNDTRDAT = TradeContext.BJEDTE         #发起行交易日期
    TradeContext.SNDTRTIM = TradeContext.BJETIM         #发起行交易时间
    TradeContext.MSGFLGNO = Rcvmbrco+TradeContext.BJEDTE + TradeContext.SerialNo        #报文标示号
    TradeContext.ORMFN    = Ormfn          #参考报文标示号
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate   #中心工作日期
    TradeContext.OPRTYPNO = '30'     #业务类型
    TradeContext.ROPRTPNO = '30'     #参考业务类型
    TradeContext.TRANTYP  = '0'      #传输类型
    #=====业务要素集====
    TradeContext.CURPIN = ""  #异地客户密码

    AfaLoggerFunc.tradeInfo("TradeContext.AVLBAL<<<<<<" + TradeContext.AVLBAL)
    AfaLoggerFunc.tradeInfo("TradeContext.ACCBAL<<<<<<" + TradeContext.ACCBAL)
        
    AfaLoggerFunc.tradeInfo("交易中处理(修改流水,主机后处理,中心前处理)  结束")
    
    return True    
    
def SubModuleDoTrd():
    AfaLoggerFunc.tradeInfo("交易后处理")
    
    AfaLoggerFunc.tradeInfo("errorCode<<<<<<<<<<<"+TradeContext.errorCode)
    AfaLoggerFunc.tradeInfo("errorMsg<<<<<<<<<<"+TradeContext.errorMsg)
    
    #=====判断afe返回结果====
    if TradeContext.errorCode == '0000':
        AfaLoggerFunc.tradeInfo('>>>发送成功')
    else:
        AfaLoggerFunc.tradeInfo('>>>发送失败')

    AfaLoggerFunc.tradeInfo("交易后处理 结束")
    
    AfaLoggerFunc.tradeInfo("'***农信银系统：通存通兑来账接收交易.卡 余额查询[1133] 退出")

    return True  
        
        
        
        
        
        
        
