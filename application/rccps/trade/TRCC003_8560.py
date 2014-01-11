# -*- coding: gbk -*-
##################################################################
#   农信银.通存通兑往账交易.余额查询
#=================================================================
#   程序文件:   TRCC003_8560.py
#   修改时间:   2008-10-21
#   作者：      潘广通
##################################################################

import TradeContext,AfaFlowControl,AfaLoggerFunc
import rccpsDBTrcc_balbka,rccpsDBTrcc_paybnk,rccpsDBTrcc_subbra
import rccpsMap8560CTradeContext2Dbalbka
from types import *
from rccpsConst import *
import jiami

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("'***农信银系统：通存通兑往账交易.余额查询[8560] 进入")
    
    AfaLoggerFunc.tradeInfo("交易前处理(本地操作,中心前处理)")
    
    #=====校验必输变量是否存在====
    if not TradeContext.existVariable("PYITYP"):
        return AfaFlowControl.ExitThisFlow('A099','帐户类型不能为空')
        
    #=====得到成员行号====
    TradeContext.RCVMBRCO = TradeContext.RCVSTLBIN
    TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN
    
    #加密客户密码
    MIMA = '                '
    #PIN = '888888'
    #ACC = '12311111111111111111111111111111'
    PIN  = TradeContext.CURPIN
    ACC  = TradeContext.PYEACC
    AfaLoggerFunc.tradeDebug('密码[' + PIN + ']')
    AfaLoggerFunc.tradeDebug('账号[' + ACC + ']')
    ret = jiami.secEncryptPin(PIN,ACC,MIMA)
    if ret != 0:
        AfaLoggerFunc.tradeDebug("ret=[" + str(ret) + "]")
        return AfaFlowControl.ExitThisFlow('M9999','调用加密服务器失败')
    else:
        TradeContext.CURPIN = MIMA
        AfaLoggerFunc.tradeDebug('密码new[' + TradeContext.CURPIN + ']')
    
    #=====组织余额查询请求报文====
    AfaLoggerFunc.tradeInfo("开始组织余额查询请求报文")
    
    #=====报文头====
    TradeContext.MSGTYPCO = 'SET009'
#    TradeContext.RCVMBRCO = 
#    TradeContext.SNDMBRCO = 
    TradeContext.SNDBRHCO = TradeContext.BESBNO
    TradeContext.SNDCLKNO = TradeContext.BETELR
    TradeContext.SNDTRDAT = TradeContext.BJEDTE
    TradeContext.SNDTRTIM = TradeContext.BJETIM
    TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
    TradeContext.ORMFN    = ""
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO = "30"
    TradeContext.ROPRTPNO = ""
    TradeContext.TRANTYP  = "0"
    #=====业务要素集====
#    TradeContext.TRCCO    =  
#    TradeContext.SNDBNKCO =
#    TradeContext.SNDBNKNM =
#    TradeContext.RCVBNKCO =
#    TradeContext.RCVBNKNM =
#    TradeContext.TRCDAT   =  
    TradeContext.TRCNO    =  TradeContext.SerialNo
    TradeContext.ORTRCCO  = ""
    TradeContext.ORTRCNO  = ""
    TradeContext.CUR      = "CNY" 
    TradeContext.OCCAMT   = "0.00"
#    TradeContext.CUSCHRG  = 
    TradeContext.PYRACC   = ""
#    TradeContext.PYEACC   = 
#    TradeContext.CURPIN   =
    TradeContext.STRINFO  = ""
    TradeContext.PRCCO    = ""           
            
    #=====判断帐户类型====
    if( TradeContext.PYITYP == '0' ): #银行卡
        AfaLoggerFunc.tradeInfo("进入银行卡操作处理")
        TradeContext.TRCCO = '3000501'     
        #=====扩展数据====
#        TradeContext.PYENAM = 
#        TradeContext.SCTRKINF =
#        TradeContext.THTRKINF =
        
    elif( TradeContext.PYITYP == '1' ): #存折
        AfaLoggerFunc.tradeInfo("进入存折操作处理")
        TradeContext.TRCCO = '3000502'    
        #=====扩展数据====
#        TradeContext.PYENAM
#        TradeContext.BNKBKNO
        
    else:
        return AfaFlowControl.ExitThisFlow("S999", "非法的操作类型")
        
    #=====登记余额查询登记簿====
    AfaLoggerFunc.tradeInfo('给登记字典赋值')
    insert_dict = {}
    rccpsMap8560CTradeContext2Dbalbka.map(insert_dict)
    insert_dict['OPRNO']    = '30'
    insert_dict['CUR']      = '01'
    insert_dict['MSGFLGNO'] = TradeContext.MSGFLGNO
    insert_dict['BRSFLG']   = PL_BRSFLG_SND
    
    
    AfaLoggerFunc.tradeInfo('开始登记余额查询登记簿')
    res = rccpsDBTrcc_balbka.insertCmt(insert_dict)
    if( res == -1 ):
        return AfaFlowControl.ExitThisFlow('A009','登记余额查询登记簿失败')
        
    AfaLoggerFunc.tradeInfo("交易前处理(本地操作,中心前处理) 结束")
    
    return True    
        
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('交易后处理')
    
    AfaLoggerFunc.tradeInfo('errorCode:' + TradeContext.errorCode)
    AfaLoggerFunc.tradeInfo('errorMsg:' + TradeContext.errorMsg)
    
    #=====判断AFE是否发送成功====
    if TradeContext.errorCode != '0000':
        #=====更改中心返回码，和附言====
        AfaLoggerFunc.tradeInfo("开始更新余额查询登记簿")
        update_dict = {'PRCCO':'RCCS1105','STRINFO':'AFE发送失败'}
        where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}
        res = rccpsDBTrcc_balbka.updateCmt(update_dict,where_dict)
        if( res == -1 ):
            return AfaFlowControl.ExitThisFlow('A009','更新余额查询登记簿失败')
           
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,'向中心发送余额查询请求报文失败')
    
    else:
        AfaLoggerFunc.tradeInfo('发送成功')
        
        TradeContext.errorCode = '0000'
        TradeContext.errorMsg  = '交易成功'
        
    AfaLoggerFunc.tradeInfo('交易后处理 结束')
    
    AfaLoggerFunc.tradeInfo("'***农信银系统：通存通兑往账交易.余额查询[8560] 退出")
    
    return True
    