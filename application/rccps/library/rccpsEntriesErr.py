# -*- coding: gbk -*-
################################################################################
#   农信银系统.会计分录赋值模块
#===============================================================================
#   程序文件:   rccpsEntriesErr.py
#   作    者:   潘广通
#   修改时间:   2008-11-30
################################################################################

import AfaLoggerFunc,AfaDBFunc,TradeContext, LoggerHandler, sys, os, time, AfaUtilTools, ConfigParser,AfaFlowControl
from types import *
from rccpsConst import *
import rccpsHostFunc

##卡折现金通存往账记账会计分录赋值
def KZTCWZJZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>开始卡折现金通存往账记账会计分录赋值")
        
    if not input_dict.has_key('CHRGTYP'):
        return AfaFLowControl.ExitThisFlow("S999","手续费收取方式不能为空")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","交易金额不能为空")
        
    if not input_dict.has_key('CUSCHRG'):
        return AfaFlowControl.ExitThisFlow("S999","手续费不能为空")
        
    
    TradeContext.HostCode = '8813' 
       
    TradeContext.PKFG = 'E'                                             #通存通兑标识
#    TradeContext.CATR = '0'                                             #现转标识:0-现金
    TradeContext.RCCSMCD  = PL_RCCSMCD_DZBJ                          #主机摘要码:现金通存往账
    TradeContext.OCCAMT = str(input_dict['OCCAMT'])
    TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_QTYSK             #借方账号
    TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25) 
    TradeContext.ACNM = '其他应收款'
    TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSWZ           #贷方账号
    TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
    TradeContext.OTNM = "农信银待清算往账"
    TradeContext.CTFG = '7'                                             #本金手续费标示
    
    AfaLoggerFunc.tradeInfo("借方账号1:[" + TradeContext.SBAC + "]")
    AfaLoggerFunc.tradeInfo("贷方账号1:[" + TradeContext.RBAC + "]")
    
    if input_dict['CHRGTYP'] == '0':
        #现金收取手续费
        TradeContext.ACUR = '2'                                         #重复次数 
        
        TradeContext.I2PKFG = 'E'                                       #通存通兑标识
#        TradeContext.I2CATR = '0'                                       #现转标识:0-现金
        TradeContext.I2TRAM = str(input_dict['CUSCHRG'])                #手续费金额
        TradeContext.I2SMCD = PL_RCCSMCD_DZBJ                            #主机摘要码:手续费
        TradeContext.I2SBAC = TradeContext.BESBNO + PL_ACC_QTYSK        #借方账号
        TradeContext.I2SBAC = rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM = '其他应收款'
        TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_TCTDSXF      #贷方账号:通存通兑手续费
        TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM = "农信银手续费"
        TradeContext.I2CTFG = '8'                                       #本金手续费标示 
    elif input_dict['CHRGTYP'] == '1':
        #现金通存无法收取本行账户手续费
        return AfaFlowControl.ExitThisFlow("S999","现金通存无法转账收取手续费")
    elif input_dict['CHRGTYP'] == '2':
        AfaLoggerFunc.tradeInfo(">>>不收手续费")
    else:
        return AfaFlowControl.ExitThisFlow("S999","非法手续费收取方式")
        
    if TradeContext.existVariable("I2SBAC") and TradeContext.existVariable('I2RBAC'):
        AfaLoggerFunc.tradeInfo("借方账号2:[" + TradeContext.I2SBAC + "]")
        AfaLoggerFunc.tradeInfo("贷方账号2:[" + TradeContext.I2RBAC + "]")
        
    AfaLoggerFunc.tradeInfo(">>>结束卡折现金通存往账记账会计分录赋值")
    return True
    
#卡折现金通存往账抹账会计分录赋值
def KZTCWZMZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>开始卡折现金通存往账抹账会计分录赋值")
        
    if not input_dict.has_key('CHRGTYP'):
        return AfaFLowControl.ExitThisFlow("S999","手续费收取方式不能为空")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","交易金额不能为空")
        
    if not input_dict.has_key('CUSCHRG'):
        return AfaFlowControl.ExitThisFlow("S999","手续费不能为空")
        
    if not input_dict.has_key('RCCSMCD'):
        return AfaFlowControl.ExitThisFlow("S999","摘要代码不能为空")
        
    TradeContext.HostCode='8813'
    if input_dict['CHRGTYP'] == '0':                          #现收  
        TradeContext.ACUR = '2'                                         #重复次数 
        #=====本金====
        TradeContext.PKFG = 'T'                                         #通存通兑标识
        TradeContext.RVFG = '2'                                         #红蓝字标示        
        TradeContext.OCCAMT = str(input_dict['OCCAMT'])           #交易金额
        TradeContext.RCCSMCD = PL_RCCSMCD_DZMZ                    #主机摘要码
        TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_QTYFK
        TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM = '其他应付款'
        TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSWZ       #贷方账号
        TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM = "农信银待清算往账"
        TradeContext.CTFG = '7'                                         #本金手续费标示
        AfaLoggerFunc.tradeInfo("借方账号1:[" + TradeContext.SBAC + "]")
        AfaLoggerFunc.tradeInfo("贷方账号1:[" + TradeContext.RBAC + "]")
        #=====手续费====
        TradeContext.I2PKFG = 'T'                                         #通存通兑标识
        TradeContext.I2RVFG = '2'                                         #红蓝字标示
        TradeContext.I2TRAM = str(input_dict['CUSCHRG'])                  #手续费
        TradeContext.I2SMCD = PL_RCCSMCD_DZMZ    
        TradeContext.I2SBAC = TradeContext.BESBNO + PL_ACC_QTYFK
        TradeContext.I2SBAC = rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM = '其他应付款'
        TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_TCTDSXF
        TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM = "手续费"
        TradeContext.I2CTFG = '8'                                         #本金手续费标示
        AfaLoggerFunc.tradeInfo("借方账号2:[" + TradeContext.I2SBAC + "]")
        AfaLoggerFunc.tradeInfo("贷方账号2:[" + TradeContext.I2RBAC + "]")
        
    elif input_dict['CHRGTYP'] == '2':                           #不收
        #=====本金====
        TradeContext.PKFG = 'T'                                         #通存通兑标识
        TradeContext.RVFG = '2'                                         #红蓝字标示        
        TradeContext.OCCAMT = str(input_dict['OCCAMT'])           #交易金额
        TradeContext.RCCSMCD = PL_RCCSMCD_DZMZ                    #主机摘要码
        TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_QTYFK
        TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM = '其他应付款'
        TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSWZ       #贷方账号
        TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM = "农信银待清算往账"
        TradeContext.CTFG = '7'                                         #本金手续费标示
        AfaLoggerFunc.tradeInfo("借方账号1:[" + TradeContext.SBAC + "]")
        AfaLoggerFunc.tradeInfo("贷方账号1:[" + TradeContext.RBAC + "]")
        
    AfaLoggerFunc.tradeInfo(">>>结束卡折现金通存往账抹账会计分录赋值")
    return True
        
#卡折本转异往账记账会计分录赋值
def KZBZYWZJZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>开始卡折本转异往账记账会计分录赋值")
    
    if not input_dict.has_key('CHRGTYP'):
        return AfaFLowControl.ExitThisFlow("S999","手续费收取方式不能为空")
        
    if not input_dict.has_key('PYRACC'):
        return AfaFlowControl.ExitThisFlow("S999","付款人账号不能为空")
        
    if not input_dict.has_key('PYRNAM'):
        return AfaFlowControl.ExitThisFlow("S999","付款人户名不能为空")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","交易金额不能为空")
        
    if not input_dict.has_key('CUSCHRG'):
        return AfaFlowControl.ExitThisFlow("S999","手续费不能为空")
    
    TradeContext.HostCode = '8813' 
      
    TradeContext.PKFG = 'E'                                         #通存通兑标识
    
    TradeContext.OCCAMT = str(input_dict['OCCAMT'])                 #出票金额
    TradeContext.RCCSMCD  = PL_RCCSMCD_DZBJ                        #主机摘要码:本转异往账
    TradeContext.SBAC = input_dict['PYRACC']                        #借方账号:客户账
    TradeContext.ACNM = input_dict['PYRNAM']                        #借方户名
    TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSWZ       #贷方账号:汇出汇款
    TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
    TradeContext.OTNM = "农信银待清算往账"
    if TradeContext.existVariable('PASSWD'):
        TradeContext.PASSWD = TradeContext.PASSWD                       #付款人密码
    else:
        AfaLoggerFunc.tradeInfo("======不校验密码记账======")
        
    if input_dict.has_key('WARNTNO'):
        TradeContext.WARNTNO = input_dict['WARNTNO']
    else:
        AfaLoggerFunc.tradeInfo("======不校验凭证记账======")
    
    if input_dict.has_key('CERTTYPE') and input_dict.has_key('CERTNO'):
        TradeContext.CERTTYPE = TradeContext.CERTTYPE                   #证件类型
        TradeContext.CERTNO   = TradeContext.CERTNO                     #证件号码
    else:
        AfaLoggerFunc.tradeInfo("======不校验证件记账======")
        
    TradeContext.CTFG = '7'                                             #本金收学费标示
    
    AfaLoggerFunc.tradeInfo("借方账号1:[" + TradeContext.SBAC + "]")
    AfaLoggerFunc.tradeInfo("贷方账号1:[" + TradeContext.RBAC + "]")
    
    if TradeContext.CHRGTYP == '0':
        #现金收取
        AfaLoggerFunc.tradeInfo(">>>现金收取手续费")
        TradeContext.ACUR = '2'                                         #重复次数
        
        TradeContext.I2PKFG = 'E'                                       #通存通兑标识
#        TradeContext.I2CATR = '0'                                       #现转标识:0-现金
        TradeContext.I2TRAM = str(input_dict['CUSCHRG'])                #手续费金额
        TradeContext.I2SMCD = PL_RCCSMCD_DZBJ                            #主机摘要码:手续费
        TradeContext.I2SBAC = TradeContext.BESBNO + PL_ACC_QTYSK        #借方账号
        TradeContext.I2SBAC = rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM = "其他应收款"                                        
        TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_TCTDSXF      #贷方账号:通存通兑手续费
        TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM = "手续费"
        TradeContext.I2CTFG = '8'                                       #本金手续费标示
        
    elif TradeContext.CHRGTYP == '1':
        #本地账户收取
        AfaLoggerFunc.tradeInfo(">>>本地账户收取手续费")
        TradeContext.ACUR = '2'                                         #重复次数
        
        TradeContext.I2PKFG = 'E'                                       #通存通兑标识
        TradeContext.I2TRAM = str(input_dict['CUSCHRG'])                #手续费金额
        TradeContext.I2SMCD = PL_RCCSMCD_DZBJ                            #主机摘要码:手续费
        TradeContext.I2SBAC = input_dict['PYRACC']                      #借方账号:客户账
        TradeContext.I2ACNM = input_dict['PYRNAM']
        TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_TCTDSXF      #贷方账号:通存通兑手续费
        TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM = "手续费"
        if input_dict.has_key('PASSWD'):
            TradeContext.I2PSWD = input_dict['PASSWD']                  #付款人密码
        else:
            AfaLoggerFunc.tradeInfo("======不校验密码记账======")
            
        if input_dict.has_key('WARNTNO'):
            TradeContext.I2WARNTNO = input_dict['WARNTNO']
        else:
            AfaLoggerFunc.tradeInfo("======不校验凭证记账======")
        
        if input_dict.has_key('CERTTYPE') and input_dict.has_key('CERTNO'):
            TradeContext.I2CERTTYPE = input_dict['CERTTYPE']            #证件类型
            TradeContext.I2CERTNO   = input_dict['CERTNO']              #证件号码
        else:
            AfaLoggerFunc.tradeInfo("======不校验证件记账======")
        TradeContext.I2CTFG = '8'                                       #本金手续费标示     
    else:
        AfaLoggerFunc.tradeInfo(">>>不收手续费")
    
    if TradeContext.existVariable("I2SBAC") and TradeContext.existVariable('I2RBAC'):
        AfaLoggerFunc.tradeInfo("借方账号2:[" + TradeContext.I2SBAC + "]")
        AfaLoggerFunc.tradeInfo("贷方账号2:[" + TradeContext.I2RBAC + "]")
    
    AfaLoggerFunc.tradeInfo(">>>结束卡折本转异往账记账会计分录赋值")
    return True
    
#卡折本转异往账抹账会计分录赋值
def KZBZYWZMZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>开始卡折本转异往账抹账会计分录赋值")
    
    if not input_dict.has_key('CHRGTYP'):
        return AfaFLowControl.ExitThisFlow("S999","手续费收取方式不能为空")
        
    if not input_dict.has_key('PYRACC'):
        return AfaFlowControl.ExitThisFlow("S999","付款人账号不能为空")
        
    if not input_dict.has_key('PYRNAM'):
        return AfaFlowControl.ExitThisFlow("S999","付款人户名不能为空")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","交易金额不能为空")
        
    if not input_dict.has_key('CUSCHRG'):
        return AfaFlowControl.ExitThisFlow("S999","手续费不能为空")
    
    if not input_dict.has_key('RCCSMCD'):
        return AfaFlowControl.ExitThisFlow("S999","摘要代码不能为空")
    
    #现金收取
    AfaLoggerFunc.tradeInfo(">>>现金收取手续费")
    
    TradeContext.HostCode = '8813' 
    if input_dict['CHRGTYP'] == '1':    #转收
        TradeContext.ACUR = '2'                                         #重复次数
        #=====本金====
        TradeContext.PKFG = 'T'                                         #通存通兑标识
        TradeContext.OCCAMT = "-" + str(input_dict['OCCAMT'])           #交易金额
        TradeContext.RCCSMCD = PL_RCCSMCD_DZMZ                    #主机摘要码:本转异往账
        TradeContext.SBAC = input_dict['PYRACC']                        #借方账号:客户账
        TradeContext.ACNM = input_dict['PYRNAM']                        #借方户名
        TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSWZ       #贷方账号
        TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM = "农信银待清算往账"
        if input_dict.has_key('PASSWD'):
            TradeContext.PASSWD = input_dict['PASSWD']                  #付款人密码
        else:
            AfaLoggerFunc.tradeInfo("======不校验密码记账======")
            
        if input_dict.has_key('WARNTNO'):
            TradeContext.WARNTNO = input_dict['WARNTNO']
        else:
            AfaLoggerFunc.tradeInfo("======不校验凭证记账======")
        
        if input_dict.has_key('CERTTYPE') and input_dict.has_key('CERTNO'):
            TradeContext.CERTTYPE = input_dict['CERTTYPE']              #证件类型
            TradeContext.CERTNO   = input_dict['CERTNO']                #证件号码
        else:
            AfaLoggerFunc.tradeInfo("======不校验证件记账======")
        TradeContext.CTFG = '7'                                         #本金手续费方式
        AfaLoggerFunc.tradeInfo("借方账号1:[" + TradeContext.SBAC + "]")
        AfaLoggerFunc.tradeInfo("贷方账号1:[" + TradeContext.RBAC + "]")
        #=====手续费====
        TradeContext.I2PKFG = 'T'                                       #通存通兑标识
        TradeContext.I2TRAM = "-" + str(input_dict['CUSCHRG'])          #手续费
        TradeContext.I2SMCD = PL_RCCSMCD_DZMZ                     #主机摘要码
        TradeContext.I2SBAC = input_dict['PYRACC']                        #借方账号
        TradeContext.I2ACNM = input_dict['PYRNAM']                        #借方户名
        TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_TCTDSXF        #贷方账号
        TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM = "手续费"
        TradeContext.I2CTFG = '8'                                         #本金手续费方式
        AfaLoggerFunc.tradeInfo("借方账号2:[" + TradeContext.I2SBAC + "]")
        AfaLoggerFunc.tradeInfo("贷方账号2:[" + TradeContext.I2RBAC + "]")
        
    elif input_dict['CHRGTYP'] == '0':    #现收
        TradeContext.ACUR = '2'                                         #重复次数
        #=====本金====
        TradeContext.PKFG = 'T'                                         #通存通兑标识
        TradeContext.OCCAMT = "-" + str(input_dict['OCCAMT'])           #交易金额
        TradeContext.RCCSMCD = PL_RCCSMCD_DZMZ                    #主机摘要码:本转异往账
        TradeContext.SBAC = input_dict['PYRACC']                        #借方账号:客户账
        TradeContext.ACNM = input_dict['PYRNAM']                        #借方户名
        TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSWZ       #贷方账号:汇出汇款
        TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM = "农信银待清算往账"
        TradeContext.CTFG = '7'                                         #本金手续费方式
        AfaLoggerFunc.tradeInfo("借方账号1:[" + TradeContext.SBAC + "]")
        AfaLoggerFunc.tradeInfo("贷方账号1:[" + TradeContext.RBAC + "]")
        #=====手续费====
        TradeContext.I2PKFG = 'T'                                       #通存通兑标识
        TradeContext.I2RVFG = '2'                                   #红蓝字标示
        TradeContext.I2TRAM = str(input_dict['CUSCHRG'])          #手续费
        TradeContext.I2SMCD = PL_RCCSMCD_DZMZ                     #主机摘要码
        TradeContext.I2SBAC = TradeContext.BESBNO + PL_ACC_QTYFK       #借方账号
        TradeContext.I2SBAC = rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM = "其他应付款"                       #借方户名
        TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_TCTDSXF
        TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM = "手续费"
        TradeContext.I2CTFG = '8'                                         #本金手续费方式
        AfaLoggerFunc.tradeInfo("借方账号2:[" + TradeContext.I2SBAC + "]")
        AfaLoggerFunc.tradeInfo("贷方账号2:[" + TradeContext.I2RBAC + "]")
        
    else:                            #不收                  
        #=====本金====
        TradeContext.PKFG = 'T'                                         #通存通兑标识
        TradeContext.OCCAMT = "-" + str(input_dict['OCCAMT'])           #交易金额
        TradeContext.RCCSMCD = PL_RCCSMCD_DZMZ                    #主机摘要码:本转异往账
        TradeContext.SBAC = input_dict['PYRACC']                        #借方账号:客户账
        TradeContext.ACNM = input_dict['PYRNAM']                        #借方户名
        TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSWZ       #贷方账号:汇出汇款
        TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM = "农信银待清算往账"
        TradeContext.CTFG = '7'                                         #本金手续费方式
        AfaLoggerFunc.tradeInfo("借方账号1:[" + TradeContext.SBAC + "]")
        AfaLoggerFunc.tradeInfo("贷方账号1:[" + TradeContext.RBAC + "]")
    
    
    AfaLoggerFunc.tradeInfo(">>>结束卡折本转异往账抹账会计分录赋值")
    return True
    
#卡折现金通兑往账记账会计分录赋值
def KZTDWZJZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>开始卡折现金通兑往账记账会计分录赋值")
    
    if not input_dict.has_key('CHRGTYP'):
        return AfaFLowControl.ExitThisFlow("S999","手续费收取方式不能为空")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","交易金额不能为空")
        
    if not input_dict.has_key('CUSCHRG'):
        return AfaFlowControl.ExitThisFlow("S999","手续费不能为空")
    
    TradeContext.HostCode = '8813' 
    
    if input_dict['CHRGTYP'] == '1':
        #=====转账====
        TradeContext.ACUR    =  '3'                                     #记账次数
        #=========交易金额+手续费===================
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZBJ                                 #摘要代码 
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  '农信银往账'                                  #借方户名
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '农信银待解临时款'                            #贷方户名
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #发生额
        TradeContext.PKFG    = 'E'                                            #通存通兑标示
        TradeContext.CTFG    = '9'                                            #本金收学费标示
        TradeContext.CATR    = '1'
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:借方账号' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:贷方账号' + TradeContext.RBAC )
        #=========交易金额============
        TradeContext.I2SMCD  =  PL_RCCSMCD_DZBJ                                 #摘要代码
        TradeContext.I2SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #借方账号
        TradeContext.I2SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM  =  '农信银待解临时款'                                    #借方户名
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_QTYFK            #贷方账号
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  '其他应付款'                                            #贷方户名
        TradeContext.I2TRAM  =  str(input_dict['OCCAMT'])                       #发生额
        TradeContext.I2CTFG  = '7'
        TradeContext.I2PKFG  = 'E'
        TradeContext.I2CATR    = '1'
        #TradeContext.I2WARNTNO = ''
        #TradeContext.I2CERTTYPE = ''
        #TradeContext.I2CERTNO = ''
        AfaLoggerFunc.tradeInfo( '>>>交易金额:借方账号' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额:贷方账号' + TradeContext.I2RBAC )
        #=========结算手续费收入户===========
        TradeContext.I3SMCD  =  PL_RCCSMCD_DZBJ                                 #摘要代码
        TradeContext.I3SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #借方账号
        TradeContext.I3SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
        TradeContext.I3ACNM  =  '应解汇款'                                    #借方户名
        TradeContext.I3RBAC  =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #贷方账号
        TradeContext.I3RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
        TradeContext.I3OTNM  =  '结算手续费'                                  #贷方户名
        TradeContext.I3TRAM  =  str(input_dict['CUSCHRG'])                    #发生额
        TradeContext.I3CTFG  = '8'
        TradeContext.I3PKFG  = 'E'
        TradeContext.I3CATR    = '1'
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:借方账号' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:贷方账号' + TradeContext.I3RBAC )
    
    elif input_dict['CHRGTYP'] == '0':                                          #现金
        #=====本金====
        TradeContext.ACUR    =  '2'                                           #记账次数
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZBJ                                 #摘要代码
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  '农信银往账'                                  #借方户名
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_QTYFK            #贷方账号
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '其他应付款'                                  #贷方户名
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #金额
        TradeContext.CTFG    = '7'
        TradeContext.PKFG    = 'E'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO  = ''
        TradeContext.CATR    =  '1'                                             #现转标志
        
        #=====手续费记账赋值====
        TradeContext.I2SMCD  =  PL_RCCSMCD_DZBJ                                 #摘要代码
        TradeContext.I2SBAC  =  TradeContext.BESBNO + PL_ACC_QTYSK            #借方账号
        TradeContext.I2SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM  =  '其他应收款'    
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #贷方账号
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  '手续费科目'                                  #贷方户名
        TradeContext.I2TRAM  =  str(input_dict['CUSCHRG'])                    #金额
        TradeContext.I2CTFG  =  '8'
        TradeContext.I2PKFG  =  'E'
        TradeContext.I2CATR  =  '1'                                           #现转标志
    elif input_dict['CHRGTYP'] == '2':
        #=====不收费====
        TradeContext.ACUR    =  '1'                                           #记账次数
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZBJ                             #摘要代码
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  '农信银往账'           
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_QTYFK            #贷方账号
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '其他应付款'                                            #贷方户名
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #金额
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    =  'E'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO  = ''
        TradeContext.CATR    =  '1'                                             #现转标志
    else:
        return AfaFlowControl.ExitThisFlow("原交易手续费收取方式非法")
            
    AfaLoggerFunc.tradeInfo(">>>结束卡折现金通兑往账记账会计分录赋值")
    return True
    
#卡折现金通兑往账抹账会计分录赋值
def KZTDWZMZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>开始卡折现金通兑往账抹账会计分录赋值")
    
    if not input_dict.has_key('CHRGTYP'):
        return AfaFLowControl.ExitThisFlow("S999","手续费收取方式不能为空")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","交易金额不能为空")
        
    if not input_dict.has_key('CUSCHRG'):
        return AfaFlowControl.ExitThisFlow("S999","手续费不能为空")
        
    if not input_dict.has_key('RCCSMCD'):
        return AfaFlowControl.ExitThisFlow("S999","摘要代码不能为空")
    
    TradeContext.HostCode = '8813'
    
    if input_dict['CHRGTYP'] == '1':
        #=====转账====
        TradeContext.ACUR    =  '3'                                           #记账次数
        #=========结算手续费收入户===========
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZMZ                        #摘要代码
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  '农信银待解临时款'                                    #借方户名
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #贷方账号
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '结算手续费'                                  #贷方户名
        TradeContext.OCCAMT  =  "-" + str(input_dict['CUSCHRG'])              #发生额
        TradeContext.CTFG    = '8'
        TradeContext.PKFG    = 'T'
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:借方账号' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:贷方账号' + TradeContext.RBAC )
        #=========交易金额============
        TradeContext.I2SMCD  =  PL_RCCSMCD_DZMZ                       #摘要代码
        TradeContext.I2RVFG    = '0' 
        TradeContext.I2SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #借方账号
        TradeContext.I2SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM  =  '农信银待解临时'                               #借方户名
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_QTYSK          #贷方账号
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  '其他应收款'                          #贷方户名
        TradeContext.I2TRAM  =  str(input_dict['OCCAMT'])               #发生额
        TradeContext.I2CTFG  = '7'
        TradeContext.I2PKFG  = 'T'
        #TradeContext.I2WARNTNO = ''
        #TradeContext.I2CERTTYPE = ''
        #TradeContext.I2CERTNO = ''
        AfaLoggerFunc.tradeInfo( '>>>交易金额:借方账号' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额:贷方账号' + TradeContext.I2RBAC )
        #=========交易金额+手续费===================
        TradeContext.I3SMCD  =  PL_RCCSMCD_DZMZ                         #摘要代码
        TradeContext.I3SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
        TradeContext.I3SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
        TradeContext.I3ACNM  =  '农信银往账'                                  #借方户名
        TradeContext.I3RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
        TradeContext.I3RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
        TradeContext.I3OTNM  =  '农信银待解临时款'                                    #贷方户名
        TradeContext.I3TRAM  =  "-" + str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #发生额
        TradeContext.I3PKFG  = 'T'
        TradeContext.I3CTFG  = '9'
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:借方账号' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:贷方账号' + TradeContext.I3RBAC )
    
    elif input_dict['CHRGTYP'] == '0':                                        #现金
        TradeContext.ACUR    =  '2'                                           #记账次数
        #=====本金====
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZMZ                         #摘要代码
        TradeContext.RVFG    = '0' 
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  '农信银往账'                                  #借方户名
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_QTYSK          #贷方账号
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '其他应收款'                          #贷方户名
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])               #金额
        TradeContext.CTFG    = '7'
        TradeContext.PKFG    = 'T'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO  = ''
        #=====手续费====
        TradeContext.I2SMCD    =  PL_RCCSMCD_DZMZ                         #摘要代码
        TradeContext.I2RVFG    = '2' 
        TradeContext.I2SBAC    =  TradeContext.BESBNO + PL_ACC_QTYFK         #借方账号
        TradeContext.I2SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM    =  '其他应付款'   
        TradeContext.I2RBAC    =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #贷方账号
        TradeContext.I2RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM    =  '手续费'                          #贷方户名
        TradeContext.I2TRAM    =  str(input_dict['CUSCHRG'])               #金额
        TradeContext.I2CTFG    = '8'
        TradeContext.I2PKFG    = 'T'
        
    elif input_dict['CHRGTYP'] == '2':
        #=====不收费====
        TradeContext.ACUR    =  '1'                                           #记账次数
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZMZ                         #摘要代码
        TradeContext.RVFG    = '0' 
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  '农信银往账'  
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_QTYSK          #贷方账号
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '其他应收款'                          #贷方户名
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])               #金额
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    =  'T'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO  = ''
    else:
        return AfaFlowControl.ExitThisFlow("原交易手续费收取方式非法")    
        
    AfaLoggerFunc.tradeInfo(">>>结束卡折现金通兑往账抹账会计分录赋值")
    return True
    
#卡折异转本往账记账会计分录赋值
def KZYZBWZJZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>开始卡折异转本往账记账会计分录赋值")
    
    if not input_dict.has_key('CHRGTYP'):
        return AfaFLowControl.ExitThisFlow("S999","手续费收取方式不能为空")
        
    if not input_dict.has_key('PYEACC'):
        return AfaFlowControl.ExitThisFlow("S999","收款人账号不能为空")
        
    if not input_dict.has_key('PYENAM'):
        return AfaFlowControl.ExitThisFlow("S999","收款人户名不能为空")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","交易金额不能为空")
        
    if not input_dict.has_key('CUSCHRG'):
        return AfaFlowControl.ExitThisFlow("S999","手续费不能为空")
    
    TradeContext.HostCode = '8813' 
    
    if input_dict['CHRGTYP'] == '1':
        #=====转账====
        TradeContext.ACUR    =  '3'                                     #记账次数
        #=========交易金额+手续费===================
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZBJ                              #摘要代码  PL_RCCSMCD_YZBWZ 异转本
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  '农信银往账'                                  #借方户名
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS           #贷方账号
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '应解汇款'                                    #贷方户名
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #发生额
        TradeContext.PKFG    = 'E'
        TradeContext.CTFG    = '9'
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:借方账号' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:贷方账号' + TradeContext.RBAC )
        #=========交易金额============
        TradeContext.I2SMCD  =  PL_RCCSMCD_DZBJ                              #摘要代码
        TradeContext.I2SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #借方账号
        TradeContext.I2SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM  =  '应解汇款'                                    #借方户名
        TradeContext.I2RBAC  =  input_dict['PYEACC']                          #贷方账号
        TradeContext.I2OTNM  =  input_dict['PYENAM']                          #贷方户名
        TradeContext.I2TRAM  =  str(input_dict['OCCAMT'])                     #发生额
        TradeContext.I2CTFG  = '7'
        TradeContext.I2PKFG  = 'E'
        TradeContext.I2WARNTNO = ''
        TradeContext.I2CERTTYPE = ''
        TradeContext.I2CERTNO = ''
        AfaLoggerFunc.tradeInfo( '>>>交易金额:借方账号' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额:贷方账号' + TradeContext.I2RBAC )
        #=========结算手续费收入户===========
        TradeContext.I3SMCD  =  PL_RCCSMCD_DZBJ                                #摘要代码
        TradeContext.I3SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #借方账号
        TradeContext.I3SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
        TradeContext.I3ACNM  =  '应解汇款'                                    #借方户名
        TradeContext.I3RBAC  =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #贷方账号
        TradeContext.I3RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
        TradeContext.I3OTNM  =  '结算手续费'                                  #贷方户名
        TradeContext.I3TRAM  =  str(input_dict['CUSCHRG'])                    #发生额
        TradeContext.I3CTFG  = '8'
        TradeContext.I3PKFG  = 'E'
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:借方账号' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:贷方账号' + TradeContext.I3RBAC )

    elif input_dict['CHRGTYP'] == '0':
        #=====本金====
        TradeContext.ACUR    =  '2'                                           #记账次数
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZBJ                              #摘要代码
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
        TradeContext.SBAC    = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  '农信银往账'                                  #借方户名
        TradeContext.RBAC    =  input_dict['PYEACC']                          #贷方账号
        TradeContext.OTNM    =  input_dict['PYENAM']                          #贷方户名
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #金额
        TradeContext.CTFG  = '7'
        TradeContext.PKFG  = 'E'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
        
        #=====手续费记账赋值====
        TradeContext.I2SMCD  =  PL_RCCSMCD_DZBJ                                #摘要代码
        TradeContext.I2SBAC  =  TradeContext.BESBNO + PL_ACC_QTYSK            #借方账号
        TradeContext.I2SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM  =  '其他应收款'
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #贷方账号
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  '手续费科目'                                  #贷方户名
        TradeContext.I2TRAM  =  str(input_dict['CUSCHRG'])                    #金额
        TradeContext.I2CTFG  =  '8'
        TradeContext.I2PKFG  =  'E'
#        TradeContext.I2CATR  =  '0'                                           #现转标志
    elif input_dict['CHRGTYP'] == '2':
        #=====不收费====
        TradeContext.ACUR    =  '1'                                           #记账次数
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZBJ                              #摘要代码
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.RBAC    =  input_dict['PYEACC']                          #贷方账号
        TradeContext.OTNM    =  input_dict['PYENAM']                          #贷方户名
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #金额
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    =  'E'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
    else:
        return AfaFlowControl.ExitThisFlow('S999','手续费收费方式非法') 
    
    AfaLoggerFunc.tradeInfo(">>>结束卡折异转本往账记账会计分录赋值")
    return True
    
#卡折异转本往账抹账会计分录赋值
def KZYZBWZMZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>开始卡折异转本往账抹账会计分录赋值")
    
    if not input_dict.has_key('CHRGTYP'):
        return AfaFLowControl.ExitThisFlow("S999","手续费收取方式不能为空")
        
    if not input_dict.has_key('PYEACC'):
        return AfaFlowControl.ExitThisFlow("S999","收款人账号不能为空")
        
    if not input_dict.has_key('PYENAM'):
        return AfaFlowControl.ExitThisFlow("S999","收款人户名不能为空")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","交易金额不能为空")
        
    if not input_dict.has_key('CUSCHRG'):
        return AfaFlowControl.ExitThisFlow("S999","手续费不能为空")
        
    if not input_dict.has_key('RCCSMCD'):
        return AfaFlowControl.ExitThisFlow("S999","摘要代码不能为空")
    
    TradeContext.HostCode = '8813' 
    
    if input_dict['CHRGTYP'] == '1':                  #转收
        TradeContext.ACUR    =  '3'                                           #记账次数
        #=====本金+手续费====
        TradeContext.I3SMCD    =  PL_RCCSMCD_DZMZ                        #摘要代码
        TradeContext.I3SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
        TradeContext.I3SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
        TradeContext.I3ACNM    =  '农信银往账'                                  #借方户名
        TradeContext.I3RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
        TradeContext.I3RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
        TradeContext.I3OTNM    =  "农信银待解临时款"                           #贷方户名
        TradeContext.I3TRAM    =  "-" + str(input_dict['OCCAMT'] + input_dict['CUSCHRG'])  #金额
        TradeContext.I3CTFG    =  '9'
        TradeContext.I3PKFG    = 'T'
        TradeContext.I3WARNTNO = ''
        TradeContext.I3CERTTYPE = ''
        TradeContext.I3CERTNO = ''
        #=====本金====
        TradeContext.RCCSMCD    =  PL_RCCSMCD_DZMZ                     #摘要代码
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS         #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  '农信银待解临时款'                                  #借方户名
        TradeContext.RBAC    =  input_dict['PYEACC']                          #贷方账号
        TradeContext.OTNM    =  input_dict['PYENAM']                            #贷方户名
        TradeContext.OCCAMT  =  "-" + str(input_dict['OCCAMT'])
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    = 'T'
        #=====手续费====
        TradeContext.I2SMCD    =  PL_RCCSMCD_DZMZ                         #摘要代码
        TradeContext.I2SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS         #借方账号
        TradeContext.I2SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM    =  '农信银待解临时款'                                  #借方户名
        TradeContext.I2RBAC    =  TradeContext.BESBNO + PL_ACC_TCTDSXF            #贷方账号
        TradeContext.I2RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM    =  "手续费"                            #贷方户名
        TradeContext.I2TRAM    =  "-" + str(input_dict['CUSCHRG'])
        TradeContext.I2CTFG    =  '8'
        TradeContext.I2PKFG    =  'T'
        
    elif input_dict['CHRGTYP'] == '0':     #现收
        TradeContext.ACUR    =  '2'                                           #记账次数 
        #=====本金====
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZMZ                         #摘要代码
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  '农信银往账'                                  #借方户名
        TradeContext.RBAC    =  input_dict['PYEACC']                          #贷方账号
        TradeContext.OTNM    =  input_dict['PYENAM']                          #贷方户名
        TradeContext.OCCAMT  =  "-" + str(input_dict['OCCAMT'])  #金额
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    =  'T'
        #=====手续费====
        TradeContext.I2SMCD    =  PL_RCCSMCD_DZMZ                      #摘要代码
        TradeContext.I2RVFG    = '2' 
        TradeContext.I2SBAC    =  TradeContext.BESBNO + PL_ACC_QTYFK         #借方账号
        TradeContext.I2SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM    =  '其他应付款'                                  #借方户名
        TradeContext.I2RBAC    =  TradeContext.BESBNO + PL_ACC_TCTDSXF            #贷方账号
        TradeContext.I2RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM    =  "手续费"                                     #贷方户名
        TradeContext.I2TRAM    =  str(input_dict['CUSCHRG'])
        TradeContext.I2CTFG    =  '8'
        TradeContext.I2PKFG    =  'T'
        
    else:                     #不收
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZMZ                       #摘要代码
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  '农信银往账'                                  #借方户名
        TradeContext.RBAC    =  input_dict['PYEACC']                          #贷方账号
        TradeContext.OTNM    =  input_dict['PYENAM']                          #贷方户名
        TradeContext.OCCAMT  =  "-" + str(input_dict['OCCAMT'])  #金额
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    =  'T'
        
    
    AfaLoggerFunc.tradeInfo(">>>结束卡折异转本往账抹账会计分录赋值")
    return True
 
 
##########################add by pgt 12-9################################################
#卡折现金通存来账记账会计分录赋值
def KZTCLZJZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>开始卡折现金通存来账记账会计分录赋值")

    if not input_dict.has_key('PYEACC'):
        return AfaFlowControl.ExitThisFlow("S999","收款人账号不能为空")
        
    if not input_dict.has_key('PYENAM'):
        return AfaFlowControl.ExitThisFlow("S999","收款人户名不能为空")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","交易金额不能为空")
    
    TradeContext.HostCode = '8813' 
       
    TradeContext.PKFG = 'E'                                             #通存通兑标识
#    TradeContext.CATR = '0'                                             #现转标识:0-现金
    TradeContext.RCCSMCD  = PL_RCCSMCD_DZBJ                           #主机摘要码:现金通存来账    TradeContext.OCCAMT = str(input_dict['OCCAMT'])
    TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ           #借方账号
    TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
    TradeContext.SBNM = "农信银待清算来账"                              #借方户名
    TradeContext.RBAC = input_dict['PYEACC']                            #贷方账号
    TradeContext.RBNM = input_dict['PYENAM']                            #贷方户名
    TradeContext.CTFG = '7'                                             #本金手续费标示
    TradeContext.OCCAMT = str(input_dict['OCCAMT'])
    
    AfaLoggerFunc.tradeInfo("借方账号1:[" + TradeContext.SBAC + "]")
    AfaLoggerFunc.tradeInfo("贷方账号1:[" + TradeContext.RBAC + "]")
    
    AfaLoggerFunc.tradeInfo(">>>结束卡折现金通存来账记账会计分录赋值")
    return True

    
#卡折本转异来账记账会计分录赋值
def KZBZYLZJZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>开始卡折本转异往来记账会计分录赋值")
            
    if not input_dict.has_key('PYEACC'):
        return AfaFlowControl.ExitThisFlow("S999","付款人账号不能为空")
        
    if not input_dict.has_key('PYENAM'):
        return AfaFlowControl.ExitThisFlow("S999","付款人户名不能为空")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","交易金额不能为空")
    
    TradeContext.HostCode = '8813' 
      
    TradeContext.PKFG = 'E'                                         #通存通兑标识
    TradeContext.OCCAMT = str(input_dict['OCCAMT'])                 #出票金额
    TradeContext.RCCSMCD  = PL_RCCSMCD_DZBJ                        #主机摘要码:本转异来账
    TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ       #借方账号:农信银待清算来账
    TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
    TradeContext.ACNM = "农信银待清算来账"                          #借方户名
    TradeContext.RBAC = input_dict['PYEACC']                        #贷方账号
    TradeContext.OTNM = input_dict['PYENAM']
    if TradeContext.existVariable('PASSWD'):
        TradeContext.PASSWD = TradeContext.PASSWD                       #付款人密码
    else:
        AfaLoggerFunc.tradeInfo("======不校验密码记账======")
        
    if input_dict.has_key('WARNTNO'):
        TradeContext.WARNTNO = input_dict['WARNTNO']
    else:
        AfaLoggerFunc.tradeInfo("======不校验凭证记账======")
    
    if input_dict.has_key('CERTTYPE') and input_dict.has_key('CERTNO'):
        TradeContext.CERTTYPE = TradeContext.CERTTYPE                   #证件类型
        TradeContext.CERTNO   = TradeContext.CERTNO                     #证件号码
    else:
        AfaLoggerFunc.tradeInfo("======不校验证件记账======")
        
    TradeContext.CTFG = '7'                                             #本金收学费标示
    
    AfaLoggerFunc.tradeInfo("借方账号1:[" + TradeContext.SBAC + "]")
    AfaLoggerFunc.tradeInfo("贷方账号1:[" + TradeContext.RBAC + "]")
    
    AfaLoggerFunc.tradeInfo(">>>结束卡折本转异来账记账会计分录赋值")
    return True
    

#卡折现金通兑来账记账会计分录赋值    
def KZTDLZJZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>开始卡折现金通兑来账记账会计分录赋值")
    
    if not input_dict.has_key('CHRGTYP'):
        return AfaFLowControl.ExitThisFlow("S999","手续费收取方式不能为空")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","交易金额不能为空")
        
    if not input_dict.has_key('CUSCHRG'):
        return AfaFlowControl.ExitThisFlow("S999","手续费不能为空")
        
    if not input_dict.has_key('PYRACC'):
        return AfaFlowControl.ExitThisFlow("S999","收款人账户不能为空")
        
    if not input_dict.has_key('PYRNAM'):
        return AfaFlowControl.ExitThisFlow("S999","收款人户名不能为空")
    
    TradeContext.HostCode = '8813' 
    
    if input_dict['CHRGTYP'] == '1':
        #=====转账====
        TradeContext.ACUR    =  '3'                                     #记账次数
        #=========交易金额+手续费===================
        TradeContext.I3SMCD =  PL_RCCSMCD_DZBJ                                 #摘要代码 
        TradeContext.I3SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #借方账号
        TradeContext.I3SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
        TradeContext.I3ACNM    =  '农信银待解临时款'                            #借方户名
        TradeContext.I3RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ         #贷方账号
        TradeContext.I3RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
        TradeContext.I3OTNM    =  '农信银来账'                                  #贷方户名
        TradeContext.I3TRAM    =  str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #发生额
        TradeContext.I3PKFG    = 'E'                                            #通存通兑标示
        TradeContext.I3CTFG    = '9'                                            #本金收学费标示
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:借方账号' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:贷方账号' + TradeContext.I3RBAC )
        #=========交易金额============
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZBJ                             #摘要代码
        TradeContext.SBAC  =  input_dict['PYRACC']                          #借方账号
        TradeContext.ACNM  =  input_dict['PYRNAM']                          #借方户名
        TradeContext.RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
        TradeContext.RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM  =  '农信银待解临时款'                            #贷方户名
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #发生额
        TradeContext.CTFG  = '7'
        TradeContext.PKFG  = 'E'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO = ''
#        TradeContext.CATR  =  '0'                                           #现转标志
        AfaLoggerFunc.tradeInfo( '>>>交易金额:借方账号' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额:贷方账号' + TradeContext.RBAC )
        #=========结算手续费收入户===========
        TradeContext.I2SMCD  =  PL_RCCSMCD_DZBJ                                #摘要代码
        TradeContext.I2SBAC  =  input_dict['PYRACC']                          #借方账号
        TradeContext.I2ACNM  =  input_dict['PYRNAM']                          #借方户名
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  '农信银待解临时款'                            #贷方户名
        TradeContext.I2TRAM  =  str(input_dict['CUSCHRG'])                    #发生额
        TradeContext.I2CTFG  = '8'
        TradeContext.I2PKFG  = 'E'
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:借方账号' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:贷方账号' + TradeContext.I2RBAC )
    
    elif input_dict['CHRGTYP'] in ('2','0'):                                          #现金
        #=====本金====
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZBJ                             #摘要代码
        TradeContext.SBAC    =  input_dict['PYRACC']                          #借方账号
        TradeContext.ACNM    =  input_dict['PYRNAM']                          #借方户名
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ         #贷方账号
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '农信银待清算来账'                          #贷方户名
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #金额
        TradeContext.CTFG    = '7'
        TradeContext.PKFG    = 'E'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO  = ''
#        TradeContext.CATR    =  '0'                                             #现转标志
        
    else:
        return AfaFlowControl.ExitThisFlow("原交易手续费收取方式非法")
            
    AfaLoggerFunc.tradeInfo(">>>结束卡折现金通兑来记账会计分录赋值")
    return True
    
    
#卡折异转本来账记账会计分录赋值
def KZYZBLZJZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>开始卡折异转本来账记账会计分录赋值")
    
    if not input_dict.has_key('CHRGTYP'):
        return AfaFLowControl.ExitThisFlow("S999","手续费收取方式不能为空")
        
    if not input_dict.has_key('PYRACC'):
        return AfaFlowControl.ExitThisFlow("S999","收款人账号不能为空")
        
    if not input_dict.has_key('PYRNAM'):
        return AfaFlowControl.ExitThisFlow("S999","收款人户名不能为空")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","交易金额不能为空")
        
    if not input_dict.has_key('CUSCHRG'):
        return AfaFlowControl.ExitThisFlow("S999","手续费不能为空")
    
    TradeContext.HostCode = '8813' 
    
    if input_dict['CHRGTYP'] == '1':
        #=====转账====
        TradeContext.ACUR    =  '3'                                     #记账次数
        #=========交易金额+手续费===================
        TradeContext.I3RCCSMCD =  PL_RCCSMCD_DZBJ                                  #摘要代码  PL_RCCSMCD_YZBWZ 异转本
        TradeContext.I3SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS              #借方账号
        TradeContext.I3SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)        
        TradeContext.I3ACNM    =  '农信银待解临时款'                                #借方户名
        TradeContext.I3RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ             #贷方账号
        TradeContext.I3RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)        
        TradeContext.I3OTNM    =  '农信银待清算来账'                                #贷方户名
        TradeContext.I3TRAM  =  str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #发生额
        TradeContext.I3PKFG    = 'E'
        TradeContext.I3CTFG    = '9'
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:借方账号' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:贷方账号' + TradeContext.I3RBAC )
        #=========交易金额============
        TradeContext.RCCSMCD  =  PL_RCCSMCD_DZBJ                              #摘要代码
        TradeContext.SBAC  =  input_dict['PYRACC']                          #借方账号
        TradeContext.ACNM  =  input_dict['PYRNAM']                          #借方户名
        TradeContext.RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
        TradeContext.RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM  =  '农信银待解临时款'                            #贷方户名
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #发生额
        TradeContext.CTFG  = '7'
        TradeContext.PKFG  = 'E'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
        AfaLoggerFunc.tradeInfo( '>>>交易金额:借方账号' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额:贷方账号' + TradeContext.RBAC )
        #=========结算手续费收入户===========
        TradeContext.I2SMCD  =  PL_RCCSMCD_DZBJ                                #摘要代码
        TradeContext.I2SBAC  =  input_dict['PYRACC']          #借方账号
        TradeContext.I2ACNM  =  input_dict['PYRNAM']                                    #借方户名
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  '农信银待解临时款'                                  #贷方户名
        TradeContext.I2TRAM  =  str(input_dict['CUSCHRG'])                    #发生额
        TradeContext.I2CTFG  = '8'
        TradeContext.I2PKFG  = 'E'
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:借方账号' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:贷方账号' + TradeContext.I2RBAC )

    elif input_dict['CHRGTYP'] in ('2','0'):
        #=====本金====
        TradeContext.ACUR    =  '1'                                           #记账次数
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZBJ                              #摘要代码
        TradeContext.SBAC    =  input_dict['PYRACC']                          #借方账号
        TradeContext.ACNM    =  input_dict['PYRNAM']                          #借方户名
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ          #贷方账号
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '农信银待清算来账'                            #贷方户名
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #金额
        TradeContext.CTFG  = '7'
        TradeContext.PKFG  = 'E'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
        
    else:
        return AfaFlowControl.ExitThisFlow('S999','手续费收费方式非法') 
    
    AfaLoggerFunc.tradeInfo(">>>结束卡折异转本来账记账会计分录赋值")
    return True   


#卡折现金通存来账抹账会计分录赋值    
def KZTCLZMZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>开始卡折现金通存来账抹账会计分录赋值")

    if not input_dict.has_key('PYEACC'):
        return AfaFlowControl.ExitThisFlow("S999","收款人账号不能为空")
        
    if not input_dict.has_key('PYENAM'):
        return AfaFlowControl.ExitThisFlow("S999","收款人户名不能为空")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","交易金额不能为空")
    
    TradeContext.HostCode = '8813' 
       
    TradeContext.PKFG = 'T'                                             #通存通兑标识
    TradeContext.RCCSMCD  = PL_RCCSMCD_DZMZ                          #主机摘要码:现金通存来账    
    TradeContext.OCCAMT = str(input_dict['OCCAMT'])
    TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ           #借方账号
    TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
    TradeContext.SBNM = "农信银待清算来账"                              #借方户名
    TradeContext.RBAC = input_dict['PYEACC']                            #贷方账号
    TradeContext.RBNM = input_dict['PYENAM']                            #贷方户名
    TradeContext.CTFG = '7'                                             #本金手续费标示
    TradeContext.OCCAMT = "-" + str(input_dict['OCCAMT'])
    
    AfaLoggerFunc.tradeInfo("借方账号1:[" + TradeContext.SBAC + "]")
    AfaLoggerFunc.tradeInfo("贷方账号1:[" + TradeContext.RBAC + "]")
    
    AfaLoggerFunc.tradeInfo(">>>结束卡折现金通存来账抹账会计分录赋值")
    return True    
    
#卡折本转异来账抹账会计分录赋值
def KZBZYLZMZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>开始卡折本转异往来抹账会计分录赋值")
            
    if not input_dict.has_key('PYEACC'):
        return AfaFlowControl.ExitThisFlow("S999","付款人账号不能为空")
        
    if not input_dict.has_key('PYENAM'):
        return AfaFlowControl.ExitThisFlow("S999","付款人户名不能为空")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","交易金额不能为空")
    
    TradeContext.HostCode = '8813' 
      
    TradeContext.PKFG = 'T'                                         #通存通兑标识
    
    TradeContext.OCCAMT = "-" + str(input_dict['OCCAMT'])                 #出票金额
    TradeContext.RCCSMCD  = PL_RCCSMCD_DZMZ                        #主机摘要码:本转异来账
    TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ       #借方账号:农信银待清算来账
    TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
    TradeContext.ACNM = "农信银待清算来账"                          #借方户名
    TradeContext.RBAC = input_dict['PYEACC']                        #贷方账号:收款人账户
    TradeContext.OTNM = input_dict['PYENAM']
    if TradeContext.existVariable('PASSWD'):
        TradeContext.PASSWD = TradeContext.PASSWD                       #付款人密码
    else:
        AfaLoggerFunc.tradeInfo("======不校验密码抹账======")
        
    if input_dict.has_key('WARNTNO'):
        TradeContext.WARNTNO = input_dict['WARNTNO']
    else:
        AfaLoggerFunc.tradeInfo("======不校验凭证抹账======")
    
    if input_dict.has_key('CERTTYPE') and input_dict.has_key('CERTNO'):
        TradeContext.CERTTYPE = TradeContext.CERTTYPE                   #证件类型
        TradeContext.CERTNO   = TradeContext.CERTNO                     #证件号码
    else:
        AfaLoggerFunc.tradeInfo("======不校验证件抹账======")
        
    TradeContext.CTFG = '7'                                             #本金手续费标识
    
    AfaLoggerFunc.tradeInfo("借方账号1:[" + TradeContext.SBAC + "]")
    AfaLoggerFunc.tradeInfo("贷方账号1:[" + TradeContext.RBAC + "]")
    
    AfaLoggerFunc.tradeInfo(">>>结束卡折本转异来账抹账会计分录赋值")
    return True  

#卡折现金通兑来账抹账会计分录赋值        
def KZTDLZMZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>开始卡折现金通兑来账抹账会计分录赋值")
    
    if not input_dict.has_key('CHRGTYP'):
        return AfaFLowControl.ExitThisFlow("S999","手续费收取方式不能为空")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","交易金额不能为空")
        
    if not input_dict.has_key('CUSCHRG'):
        return AfaFlowControl.ExitThisFlow("S999","手续费不能为空")
        
    if not input_dict.has_key('PYRACC'):
        return AfaFlowControl.ExitThisFlow("S999","收款人账户不能为空")
        
    if not input_dict.has_key('PYRNAM'):
        return AfaFlowControl.ExitThisFlow("S999","收款人户名不能为空")
    
    TradeContext.HostCode = '8813' 
    
    if input_dict['CHRGTYP'] == '1':
        #=====转账====
        TradeContext.ACUR    =  '3'                                     #抹账次数
        #=========交易金额+手续费===================
        TradeContext.RCCSMCD    =  PL_RCCSMCD_DZMZ                                 #摘要代码 
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  '农信银待解临时款'                            #借方户名
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ         #贷方账号
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '农信银来账'                                  #贷方户名
        TradeContext.OCCAMT   = "-" + str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #发生额
        TradeContext.PKFG    = 'T'                                            #通存通兑标示
        TradeContext.CTFG    = '9'                                            #本金收学费标示
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:借方账号' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:贷方账号' + TradeContext.RBAC )
        #=========交易金额============
        TradeContext.I2SMCD  =  PL_RCCSMCD_DZMZ                             #摘要代码
        TradeContext.I2SBAC  =  input_dict['PYRACC']                          #借方账号
        TradeContext.I2ACNM  =  input_dict['PYRNAM']                          #借方户名
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
        TradeContext.I2RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  '农信银待解临时款'                            #贷方户名
        TradeContext.I2TRAM  =  "-" + str(input_dict['OCCAMT'])                     #发生额
        TradeContext.I2CTFG  = '7'
        TradeContext.I2PKFG  = 'T'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO = ''
#        TradeContext.CATR  =  '0'                                           #现转标志
        AfaLoggerFunc.tradeInfo( '>>>交易金额:借方账号' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额:贷方账号' + TradeContext.I2RBAC )
        #=========结算手续费收入户===========
        TradeContext.I3SMCD  =  PL_RCCSMCD_DZMZ                                #摘要代码
        TradeContext.I3SBAC  =  input_dict['PYRACC']                          #借方账号
        TradeContext.I3ACNM  =  input_dict['PYRNAM']                          #借方户名
        TradeContext.I3RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
        TradeContext.I3RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
        TradeContext.I3OTNM  =  '农信银待解临时款'                            #贷方户名
        TradeContext.I3TRAM  =  "-" + str(input_dict['CUSCHRG'])                    #发生额
        TradeContext.I3CTFG  = '8'
        TradeContext.I3PKFG  = 'T'
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:借方账号' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:贷方账号' + TradeContext.I3RBAC )
    
    elif input_dict['CHRGTYP'] == '0':                                          #现金
        #=====本金====
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZMZ                             #摘要代码
        TradeContext.SBAC    =  input_dict['PYRACC']         #借方账号
        TradeContext.ACNM    =  input_dict['PYRNAM']                            #借方户名
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ                          #贷方账号
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '农信银待清算来账'                          #贷方户名
        TradeContext.OCCAMT  =  "-" + str(input_dict['OCCAMT'])                     #金额
        TradeContext.CTFG    = '7'
        TradeContext.PKFG    = 'T'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO  = ''
#        TradeContext.CATR    =  '0'                                             #现转标志
        
    elif input_dict['CHRGTYP'] == '2':
        #=====不收费====
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZMZ                            #摘要代码
        TradeContext.SBAC    =  input_dict['PYRACC']         #借方账号
        TradeContext.ACNM    =  input_dict['PYRNAM']                            #借方户名
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ                          #贷方账号
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '农信银待清算来账'                          #贷方户名
        TradeContext.OCCAMT  =  "-" + str(input_dict['OCCAMT'])                     #金额
        TradeContext.CTFG    = '7'
        TradeContext.PKFG    = 'T'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO  = ''
#        TradeContext.CATR    =  '0'                                             #现转标志
    else:
        return AfaFlowControl.ExitThisFlow("原交易手续费收取方式非法")
            
    AfaLoggerFunc.tradeInfo(">>>结束卡折现金通兑来抹账会计分录赋值")
    return True  
  
#卡折异转本来账抹账会计分录赋值
def KZYZBLZMZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>开始卡折异转本来账抹账会计分录赋值")
    
    if not input_dict.has_key('CHRGTYP'):
        return AfaFLowControl.ExitThisFlow("S999","手续费收取方式不能为空")
        
    if not input_dict.has_key('PYRACC'):
        return AfaFlowControl.ExitThisFlow("S999","收款人账号不能为空")
        
    if not input_dict.has_key('PYRNAM'):
        return AfaFlowControl.ExitThisFlow("S999","收款人户名不能为空")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","交易金额不能为空")
        
    if not input_dict.has_key('CUSCHRG'):
        return AfaFlowControl.ExitThisFlow("S999","手续费不能为空")
    
    TradeContext.HostCode = '8813' 
    
    if input_dict['CHRGTYP'] == '1':
        #=====转账====
        TradeContext.ACUR    =  '3'                                     #抹账次数
        #=========交易金额+手续费===================
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZMZ                                 #摘要代码  PL_RCCSMCD_YZBWZ 异转本
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS              #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)        
        TradeContext.ACNM    =  '农信银待解临时款'                                #借方户名
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ             #贷方账号
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)        
        TradeContext.OTNM    =  '农信银待清算来账'                                #贷方户名
        TradeContext.OCCAMT    = "-" + str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #发生额
        TradeContext.PKFG    = 'T'
        TradeContext.CTFG    = '9'
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:借方账号' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:贷方账号' + TradeContext.RBAC )
        #=========交易金额============
        TradeContext.I2SMCD  =  PL_RCCSMCD_DZMZ                             #摘要代码
        TradeContext.I2SBAC  =  input_dict['PYRACC']                          #借方账号
        TradeContext.I2ACNM  =  input_dict['PYRNAM']                          #借方户名
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  '农信银待解临时款'                            #贷方户名
        TradeContext.I2TRAM  = "-" + str(input_dict['OCCAMT'])                     #发生额
        TradeContext.I2CTFG  = '7'
        TradeContext.I2PKFG  = 'T'
        TradeContext.I2WARNTNO = ''
        TradeContext.I2CERTTYPE = ''
        TradeContext.I2CERTNO = ''
        AfaLoggerFunc.tradeInfo( '>>>交易金额:借方账号' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额:贷方账号' + TradeContext.I2RBAC )
        #=========结算手续费收入户===========
        TradeContext.I3SMCD  =  PL_RCCSMCD_DZMZ                                #摘要代码
        TradeContext.I3SBAC  =  input_dict['PYRACC']          #借方账号
        TradeContext.I3ACNM  =  input_dict['PYRNAM']                                    #借方户名
        TradeContext.I3RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
        TradeContext.I3RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
        TradeContext.I3OTNM  =  '农信银待解临时款'                                  #贷方户名
        TradeContext.I3TRAM  =  "-" + str(input_dict['CUSCHRG'])                    #发生额
        TradeContext.I3CTFG  = '8'
        TradeContext.I3PKFG  = 'T'
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:借方账号' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:贷方账号' + TradeContext.I3RBAC )

    elif input_dict['CHRGTYP'] == '0':
        #=====本金====
        TradeContext.ACUR    =  '1'                                           #抹账次数
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZMZ                              #摘要代码
        TradeContext.SBAC    =  input_dict['PYRACC']                          #借方账号
        TradeContext.ACNM    =  input_dict['PYRNAM']                          #借方户名
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ          #贷方账号
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '农信银待清算来账'                            #贷方户名
        TradeContext.OCCAMT  =  "-" + str(input_dict['OCCAMT'])                     #金额
        TradeContext.CTFG  = '7'
        TradeContext.PKFG  = 'T'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
        
    elif input_dict['CHRGTYP'] == '2':
        #=====不收费====
        TradeContext.ACUR    =  '1'                                           #抹账次数
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZMZ                               #摘要代码
        TradeContext.SBAC    =  input_dict['PYRACC']                          #借方账号
        TradeContext.ACNM    =  input_dict['PYRNAM']                          #借方户名
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ          #贷方账号
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '农信银待清算来账'                            #贷方户名
        TradeContext.OCCAMT  =  "-" + str(input_dict['OCCAMT'])                     #金额
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    =  'T'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
    else:
        return AfaFlowControl.ExitThisFlow('S999','手续费收费方式非法') 
    
    AfaLoggerFunc.tradeInfo(">>>结束卡折异转本来账抹账会计分录赋值")
    return True     