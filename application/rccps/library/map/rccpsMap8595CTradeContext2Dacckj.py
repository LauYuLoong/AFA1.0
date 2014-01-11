# -*- coding: gbk -*-
##################################################################
#   农信银系统 TradeContext 字典到 acckj 字典映射函数
#
#   作    者：  曾照泰
#   程序文件:   rccpsMap8595CTradeContext2Dacckj.py
#   修改时间:   20110511
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(to_dict):
    if TradeContext.existVariable('TRCDAT'):     #委托日期                            
        to_dict['TRCDAT'] = TradeContext.TRCDAT                                       
        AfaLoggerFunc.tradeDebug('acckj[TRCDAT] = ' + str(to_dict['TRCDAT']))         
    else:                                                                             
        AfaLoggerFunc.tradeDebug("TradeContext.OPRATTNO不存在")                       
                                                                                      
    if TradeContext.existVariable('BSPSQN'):        #委托流水号(报文标识)
        to_dict['BSPSQN'] = TradeContext.BSPSQN
        AfaLoggerFunc.tradeDebug('acckj[BSPSQN] = ' + str(to_dict['BSPSQN']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BSPSQN不存在")
        
    if TradeContext.existVariable('MSGFLGNO'):  #报文标识号            
        to_dict['MSGFLGNO'] = TradeContext.MSGFLGNO
        AfaLoggerFunc.tradeDebug('acckj[MSGFLGNO] = ' + str(to_dict['MSGFLGNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.MSGFLGNO不存在")
        
    if TradeContext.existVariable('ORMFN'):  #参考报文标识号            
        to_dict['ORMFN'] = TradeContext.ORMFN
        AfaLoggerFunc.tradeDebug('acckj[ORMFN] = ' + str(to_dict['ORMFN']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORMFN不存在")

    if TradeContext.existVariable('TRCCO'):        #交易码  
        to_dict['TRCCO'] = TradeContext.TRCCO
        AfaLoggerFunc.tradeDebug('acckj[TRCCO] = ' + str(to_dict['TRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCCO不存在")
        
    if TradeContext.existVariable('BRSFLG'):        #来往帐标识
        to_dict['BRSFLG'] = TradeContext.BRSFLG
        AfaLoggerFunc.tradeDebug('acckj[BRSFLG] = ' + str(to_dict['BRSFLG']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BRSFLG不存在")

    if TradeContext.existVariable('BESBNO'):        #机构号
        to_dict['BESBNO'] = TradeContext.BESBNO
        AfaLoggerFunc.tradeDebug('acckj[BESBNO] = ' + str(to_dict['BESBNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BESBNO不存在")

    if TradeContext.existVariable('BEACSB'):        #财务机构号  
        to_dict['BEACSB'] = TradeContext.BEACSB
        AfaLoggerFunc.tradeDebug('acckj[BEACSB] = ' + str(to_dict['BEACSB']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BEACSB不存在")

    if TradeContext.existVariable('BETELR'):        #柜员号
        to_dict['BETELR'] = TradeContext.BETELR
        AfaLoggerFunc.tradeDebug('acckj[BETELR] = ' + str(to_dict['BETELR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BETELR不存在")

    if TradeContext.existVariable('BEAUUS'):        #授权柜员
        to_dict['BEAUUS'] = TradeContext.BEAUUS
        AfaLoggerFunc.tradeDebug('acckj[BEAUUS] = ' + str(to_dict['BEAUUS']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BEAUUS不存在")

    if TradeContext.existVariable('BEAUPS'):       #授权柜员密码  
        to_dict['BEAUPS'] = TradeContext.BEAUPS
        AfaLoggerFunc.tradeDebug('acckj[BEAUPS] = ' + str(to_dict['BEAUPS']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BEAUPS不存在")

    if TradeContext.existVariable('TERMID'):       #终端号 
        to_dict['TERMID'] = TradeContext.TERMID
        AfaLoggerFunc.tradeDebug('acckj[TERMID] = ' + str(to_dict['TERMID']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TERMID不存在")

    if TradeContext.existVariable('OPTYPE'):        #操作类型
        to_dict['OPTYPE'] = TradeContext.OPTYPE
        AfaLoggerFunc.tradeDebug('acckj[OPTYPE] = ' + str(to_dict['OPTYPE']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.OPTYPE不存在")

    if TradeContext.existVariable('NCCWKDAT'):     #农信银中心日期   
        to_dict['NCCWKDAT'] = TradeContext.NCCWKDAT
        AfaLoggerFunc.tradeDebug('acckj[NCCWKDAT] = ' + str(to_dict['NCCWKDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NCCWKDAT不存在")

    if TradeContext.existVariable('TRCNO'):        #交易流水号
        to_dict['TRCNO'] = TradeContext.TRCNO
        AfaLoggerFunc.tradeDebug('acckj[TRCNO] = ' + str(to_dict['TRCNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCNO不存在")

    if TradeContext.existVariable('SNDMBRCO'):      #发送成员行行号
        to_dict['SNDMBRCO'] = TradeContext.SNDMBRCO
        AfaLoggerFunc.tradeDebug('acckj[SNDMBRCO] = ' + str(to_dict['SNDMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDMBRCO不存在")

    if TradeContext.existVariable('RCVMBRCO'):        #接受成员行行号
        to_dict['RCVMBRCO'] = TradeContext.RCVMBRCO
        AfaLoggerFunc.tradeDebug('acckj[RCVMBRCO] = ' + str(to_dict['RCVMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVMBRCO不存在")

    if TradeContext.existVariable('SNDBNKCO'):         #发送行号
        to_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
        AfaLoggerFunc.tradeDebug('acckj[SNDBNKCO] = ' + str(to_dict['SNDBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDBNKCO不存在")

    if TradeContext.existVariable('SNDBNKNM'):         #发送行名
        to_dict['SNDBNKNM'] = TradeContext.SNDBNKNM
        AfaLoggerFunc.tradeDebug('acckj[SNDBNKNM] = ' + str(to_dict['SNDBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDBNKNM不存在")

    if TradeContext.existVariable('RCVBNKCO'):          #接受行号
        to_dict['RCVBNKCO'] = TradeContext.RCVBNKCO
        AfaLoggerFunc.tradeDebug('acckj[RCVBNKCO] = ' + str(to_dict['RCVBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVBNKCO不存在")

    if TradeContext.existVariable('RCVBNKNM'):          #接受行名
        to_dict['RCVBNKNM'] = TradeContext.RCVBNKNM
        AfaLoggerFunc.tradeDebug('acckj[RCVBNKNM] = ' + str(to_dict['RCVBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVBNKNM不存在")

    if TradeContext.existVariable('ORTRCDAT'):          #原委托日期
        to_dict['ORTRCDAT'] = TradeContext.ORTRCDAT
        AfaLoggerFunc.tradeDebug('acckj[ORTRCDAT] = ' + str(to_dict['ORTRCDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORTRCDAT不存在")
        
    if TradeContext.existVariable('ORTRCCO'):          #原交易代码
        to_dict['ORTRCCO'] = TradeContext.ORTRCCO
        AfaLoggerFunc.tradeDebug('acckj[ORTRCCO] = ' + str(to_dict['ORTRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORTRCCO不存在")
        
    if TradeContext.existVariable('ORTRCNO'):          #原交易流水号 
        to_dict['ORTRCNO'] = TradeContext.ORTRCNO
        AfaLoggerFunc.tradeDebug('acckj[ORTRCNO] = ' + str(to_dict['ORTRCNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORTRCNO不存在")
        
    if TradeContext.existVariable('ORSNDSUBBNK'):          #原发起行成员行号
        to_dict['ORSNDSUBBNK'] = TradeContext.ORSNDSUBBNK
        AfaLoggerFunc.tradeDebug('acckj[ORSNDSUBBNK] = ' + str(to_dict['ORSNDSUBBNK']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORSNDSUBBNK不存在")
        
    if TradeContext.existVariable('ORSNDBNK'):          #原发起行行号 
        to_dict['ORSNDBNK'] = TradeContext.ORSNDBNK
        AfaLoggerFunc.tradeDebug('acckj[ORSNDBNK] = ' + str(to_dict['ORSNDBNK']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORSNDBNK不存在")
        
    if TradeContext.existVariable('ORRCVSUBBNK'):          #原接收行成员行号
        to_dict['ORRCVSUBBNK'] = TradeContext.ORRCVSUBBNK
        AfaLoggerFunc.tradeDebug('acckj[ORRCVSUBBNK] = ' + str(to_dict['ORRCVSUBBNK']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORRCVSUBBNK不存在")
        
    if TradeContext.existVariable('ORRCVBNK'):          #原接收行行号 
        to_dict['ORRCVBNK'] = TradeContext.ORRCVBNK
        AfaLoggerFunc.tradeDebug('acckj[ORRCVBNK] = ' + str(to_dict['ORRCVBNK']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORRCVBNK不存在")
        
    if TradeContext.existVariable('ORPYRACC'):          #原付款人账号 
        to_dict['ORPYRACC'] = TradeContext.ORPYRACC
        AfaLoggerFunc.tradeDebug('acckj[ORPYRACC] = ' + str(to_dict['ORPYRACC']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORPYRACC不存在")
        
    if TradeContext.existVariable('ORPYRNAM'):          #原付款人名称
        to_dict['ORPYRNAM'] = TradeContext.ORPYRNAM
        AfaLoggerFunc.tradeDebug('acckj[ORPYRNAM] = ' + str(to_dict['ORPYRNAM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORPYRNAM不存在")
        
    if TradeContext.existVariable('ORPYEACC'):          #原收款人账号
        to_dict['ORPYEACC'] = TradeContext.ORPYEACC
        AfaLoggerFunc.tradeDebug('acckj[ORPYEACC] = ' + str(to_dict['ORPYEACC']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORPYEACC不存在")
        
    if TradeContext.existVariable('ORPYENAM'):          #原收款人名称
        to_dict['ORPYENAM'] = TradeContext.ORPYENAM
        AfaLoggerFunc.tradeDebug('acckj[ORPYENAM] = ' + str(to_dict['ORPYENAM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CERTNO不存在")
                
    if TradeContext.existVariable('CUR'):               #币种
        to_dict['CUR'] = TradeContext.CUR
        AfaLoggerFunc.tradeDebug('acckj[CUR] = ' + str(to_dict['CUR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CUR不存在")

    if TradeContext.existVariable('OCCAMT'):          #原交易金额
        to_dict['OCCAMT'] = str((long)(((float)(TradeContext.OCCAMT)) * 100 + 0.1))
        AfaLoggerFunc.tradeDebug('acckj[OCCAMT] = ' + str(to_dict['OCCAMT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.OCCAMT不存在") 
        
    if TradeContext.existVariable('CHRG'):          #手续费
        to_dict['CHRG'] = str((long)(((float)(TradeContext.CHRG)) * 100 + 0.1))
        AfaLoggerFunc.tradeDebug('acckj[CHRG] = ' + str(to_dict['CHRG']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CHRG不存在")     
    
    if TradeContext.existVariable('ERRCONBAL'):         #错帐控制金额
        to_dict['ERRCONBAL'] = TradeContext.ERRCONBAL
        AfaLoggerFunc.tradeDebug('acckj[ERRCONBAL] = ' + str(to_dict['ERRCONBAL']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ERRCONBAL不存在")
    
    if TradeContext.existVariable('BALANCE'):         #账户实际金额
        to_dict['BALANCE'] = TradeContext.BALANCE
        AfaLoggerFunc.tradeDebug('acckj[BALANCE] = ' + str(to_dict['BALANCE']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BALANCE不存在")
   
    if TradeContext.existVariable('UNCONRST'):         #解控处理结果
        to_dict['UNCONRST'] = TradeContext.UNCONRST
        AfaLoggerFunc.tradeDebug('acckj[UNCONRST] = ' + str(to_dict['UNCONRST']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.UNCONRST不存在")


    if TradeContext.existVariable('STRINFO'):         #附言
        to_dict['STRINFO'] = TradeContext.STRINFO
        AfaLoggerFunc.tradeDebug('acckj[STRINFO] = ' + str(to_dict['STRINFO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.STRINFO不存在")

    if TradeContext.existVariable('PRCCO'):       #中心返回码
        to_dict['PRCCO'] = TradeContext.PRCCO
        AfaLoggerFunc.tradeDebug('acckj[PRCCO] = ' + str(to_dict['PRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PRCCO不存在")
    
    if TradeContext.existVariable('CONSTS'):       #控制状态
        to_dict['CONSTS'] = TradeContext.CONSTS
        AfaLoggerFunc.tradeDebug('acckj[CONSTS] = ' + str(to_dict['CONSTS']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CONSTS不存在")
    
    if TradeContext.existVariable('NOTE1'):
        to_dict['NOTE1'] = TradeContext.NOTE1
        AfaLoggerFunc.tradeDebug('acckj[NOTE1] = ' + str(to_dict['NOTE1']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE1不存在")

    if TradeContext.existVariable('NOTE2'):
        to_dict['NOTE2'] = TradeContext.NOTE2
        AfaLoggerFunc.tradeDebug('acckj[NOTE2] = ' + str(to_dict['NOTE2']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE2不存在")

    if TradeContext.existVariable('NOTE3'):
        to_dict['NOTE3'] = TradeContext.NOTE3
        AfaLoggerFunc.tradeDebug('acckj[NOTE3] = ' + str(to_dict['NOTE3']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE3不存在")

    if TradeContext.existVariable('NOTE4'):
        to_dict['NOTE4'] = TradeContext.NOTE4
        AfaLoggerFunc.tradeDebug('acckj[NOTE4] = ' + str(to_dict['NOTE4']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE4不存在")
        
    if TradeContext.existVariable('NOTE5'):
        to_dict['NOTE5'] = TradeContext.NOTE5
        AfaLoggerFunc.tradeDebug('acckj[NOTE5] = ' + str(to_dict['NOTE5']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE5不存在")

    return True

