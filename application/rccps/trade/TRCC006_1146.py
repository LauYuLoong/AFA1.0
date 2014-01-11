# -*- coding: gbk -*-
##################################################################
#   农信银.通存通兑来账.补正来账
#=================================================================
#   程序文件:   TRCC006_1146.py
#   修改时间:   2008-11-04
#   作者：      潘广通
##################################################################

import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools
import rccpsDBTrcc_jstbka,rccpsMap1146CTradeContext2Dwtrbka_dict,rccpsDBTrcc_wtrbka,rccpsUtilTools
import rccpsDBTrcc_spbsta,AfaDBFunc,rccpsGetFunc,rccpsState,rccpsHostFunc,rccpsDBTrcc_atcbka
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("农信银.通存通兑来账.补正来账[T" + TradeContext.TemplateCode + '_' + TradeContext.TransCode+"]进入")
    
    AfaLoggerFunc.tradeInfo("交易前处理(登记流水,中心前处理)  进入")
    
    #==============================组织应答报文===========================================
    AfaLoggerFunc.tradeInfo("组织应答报文开始")
    Ormfn = TradeContext.MSGFLGNO
    Rcvmbrco = TradeContext.SNDMBRCO
    Sndmbrco = TradeContext.RCVMBRCO
    #=====报文头====
    TradeContext.MSGTYPCO = 'SET010' #报文类代码
    TradeContext.RCVSTLBIN = Rcvmbrco #接受方成员行号
    TradeContext.SNDSTLBIN = Sndmbrco #发送方成员行号
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
    TradeContext.CURPIN   = ""  #异地客户密码
    
    TradeContext.PRCCO    = "NN1IA999"
    TradeContext.STRINFO  = "本交易无法补正" 
    
    AfaLoggerFunc.tradeInfo("组织应答报文结束")
    
    AfaLoggerFunc.tradeInfo("交易前处理(登记流水,中心前处理)  退出")
    
    return True
    
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo("交易后处理 进入")
    
    #=====判断afe是否发送成功====
    if TradeContext.errorCode == '0000':
        AfaLoggerFunc.tradeInfo('>>>发送回执报文成功')
    else:
        AfaLoggerFunc.tradeInfo('>>>发送回执报文失败')
        
    AfaLoggerFunc.tradeInfo("交易后处理 退出")
    
    AfaLoggerFunc.tradeInfo("农信银.通存通兑来账.补正来账[T" + TradeContext.TemplateCode + '_' + TradeContext.TransCode+"]退出")
    
    return True
