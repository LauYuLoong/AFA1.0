# -*- coding: gbk -*-
################################################################################
#   农信银系统.会计分录赋值模块
#===============================================================================
#   程序文件:   rccpsEntries.py
#   作    者:   关彬捷
#   修改时间:   2008-11-30
################################################################################

import AfaLoggerFunc,AfaDBFunc,TradeContext, LoggerHandler, sys, os, time, AfaUtilTools, ConfigParser,AfaFlowControl
import rccpsDBFunc,rccpsGetFunc
from types import *
from rccpsConst import *
import rccpsHostFunc

##汇兑往帐记帐
def HDWZJZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>开始汇兑往账记账会计分录赋值")
    
    if not input_dict.has_key('CHRGTYP'):
        return AfaFLowControl.ExitThisFlow("S999","手续费收取方式不能为空")
        
    if not input_dict.has_key('PYRACC'):
        return AfaFlowControl.ExitThisFlow("S999","付款人账号不能为空")
        
    if not input_dict.has_key('ACNM'):
        return AfaFlowControl.ExitThisFlow("S999","付款人户名不能为空")
    
    if not input_dict.has_key('OTNM'):
        return AfaFlowControl.ExitThisFlow("S999","收款人户名不能为空")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","交易金额不能为空")
        
    if not input_dict.has_key('LOCCUSCHRG'):
        return AfaFlowControl.ExitThisFlow("S999","手续费不能为空")

    if not input_dict.has_key('BBSSRC'):
        return AfaFlowControl.ExitThisFlow("S999","资金来源不能为空")
        
    if not input_dict.has_key('BESBNO'):
        return AfaFlowControl.ExitThisFlow("S999","机构号不能为空")
    #=====设置记账函数接口====

    TradeContext.HostCode = '8813'
    TradeContext.BRSFLG   = PL_BRSFLG_SND                                    #往来标识:往账
    TradeContext.RCCSMCD  = PL_RCCSMCD_HDWZ                                  #主机摘要代码：汇兑往账
    
    TradeContext.BESBNO   = input_dict['BESBNO']
    TradeContext.BBSSRC   = input_dict['BBSSRC']

    #=====借方账号,资金来源为3-内部账====
    if TradeContext.BBSSRC != '3' and TradeContext.BBSSRC != '5':
        TradeContext.SBAC = input_dict['PYRACC']
    else:
        TradeContext.SBAC = ''
        
    #=====判断资金来源设置凭证号码====
    if TradeContext.BBSSRC == '0':
        TradeContext.WARNTNO = TradeContext.SBAC[6:18]
        AfaLoggerFunc.tradeInfo( '凭证号码：' + TradeContext.WARNTNO )
    #=====现金时付现转标志====
    if TradeContext.BBSSRC == '5':
        TradeContext.CATR = '0'
        
    TradeContext.CTFG     = '7'                                              #本金手续费标示
    TradeContext.TRCTYP   = '20'                                             
    TradeContext.OCCAMT   = str(input_dict['OCCAMT'])                        #金额

    TradeContext.OTNM     = input_dict['OTNM']                               #收款人户名
    TradeContext.ACNM     = input_dict['ACNM']                               #付款人户名
    
    #=====开始拼贷方账号====
    AfaLoggerFunc.tradeInfo( ">>>准备向主机发起记账" )
    TradeContext.RBAC =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ

    #=====开始调函数拼贷方账号第25位校验位====
    TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC, 25)
    
    AfaLoggerFunc.tradeInfo("借方账号1:[" + TradeContext.SBAC + "]")
    AfaLoggerFunc.tradeInfo("贷方账号1:[" + TradeContext.RBAC + "]")
    
    
    ##======张恒 增加手续费收取 20091109  ======================
    if   input_dict['CHRGTYP'] == '0' :                                      # 现金收取手续费'0' 
        TradeContext.ACUR    = '2'                                           #重复次数 
        TradeContext.I2SMCD  = PL_RCCSMCD_SXF                                #主机摘要代码：汇兑往账
        TradeContext.I2TRAM = str(input_dict['LOCCUSCHRG'])                  #手续费金额
        TradeContext.I2CATR = '0'                                            #现转标识:0-现金
        TradeContext.I2SBAC = ''                                             #借方账号  
        TradeContext.I2ACNM = ''
        TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_HDSXF             #贷方账号,手续费收入户
        TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM = "农信银手续费"
        TradeContext.I2CTFG = '8'                                             #手续费标示

        AfaLoggerFunc.tradeInfo(">>>现金收取手续费")  
        
    elif input_dict['CHRGTYP'] == '1' :                                       # 转收手续费'1'
        TradeContext.ACUR    = '2'                                            #重复次数
        TradeContext.I2SMCD  = PL_RCCSMCD_SXF                                 #主机摘要代码：汇兑往账
        TradeContext.I2TRAM  = str(input_dict['LOCCUSCHRG'])                  #手续费金额

        TradeContext.I2SBAC = input_dict['PYRACC']                            #付款人账号  
        
        TradeContext.I2ACNM = input_dict['ACNM'] 
        TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_HDSXF              #贷方账号,手续费收入户
        TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM = "农信银手续费"
        TradeContext.I2CTFG = '8'                                             #手续费标示
        
        AfaLoggerFunc.tradeInfo(">>>转收手续费")

    elif input_dict['CHRGTYP'] == '2' :                                       # 不收手续费'2'
        
        AfaLoggerFunc.tradeInfo(">>>不收取手续费")
        
    else:
        return AfaFlowControl.ExitThisFlow("S999","非法手续费收取方式")
        
    if TradeContext.existVariable("I2SBAC") and TradeContext.existVariable('I2RBAC'):
        AfaLoggerFunc.tradeInfo("借方账号2:[" + TradeContext.I2SBAC + "]")
        AfaLoggerFunc.tradeInfo("贷方账号2:[" + TradeContext.I2RBAC + "]")
    
    AfaLoggerFunc.tradeInfo(">>>结束汇兑往账记账会计分录赋值")
    return True

##汇兑往帐抹帐
def HDWZMZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>开始汇兑往账抹账会计分录赋值")
    
    if not input_dict.has_key('BJEDTE'):                                   #原正交易日期
        return AfaFlowControl.ExitThisFlow("S999","日期不能为空")
        
    if not input_dict.has_key('BSPSQN'):                                   #原正交易前置流水号
        return AfaFlowControl.ExitThisFlow("S999","报单序号不能为空")
    
    if not input_dict.has_key('PYRACC'):
        return AfaFlowControl.ExitThisFlow("S999","付款人账号不能为空")

    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","金额不能为空")

    if not input_dict.has_key('BBSSRC'):
        return AfaFlowControl.ExitThisFlow("S999","资金来源不能为空")

    if not input_dict.has_key('BESBNO'):
        return AfaFlowControl.ExitThisFlow("S999","机构号不能为空")
        
    #=====如果资金来源为代销账，使用8813红字冲销====  
    if input_dict['BBSSRC']   ==  '3':                                           #待销账
        #为抹账赋值会计分录
        input_dict['SBAC']       = TradeContext.BESBNO  +  PL_ACC_NXYDQSWZ       #借方账号
        input_dict['RBAC']       = TradeContext.BESBNO  +  PL_ACC_NXYDXZ         #贷方账号
        input_dict['CATR']       = '1' 
        TradeContext.OCCAMT      = str(input_dict['OCCAMT'])
        TradeContext.RVFG        = '0'                                           #红蓝字标识,0红冲
        #=====开始调函数拼贷方账号第25位校验位====
        input_dict['SBAC'] = rccpsHostFunc.CrtAcc(input_dict['SBAC'], 25)
        input_dict['RBAC'] = rccpsHostFunc.CrtAcc(input_dict['RBAC'], 25)
        
    elif input_dict['BBSSRC'] == '5':                                            # 现金 
        #为抹账赋值会计分录 
        input_dict['SBAC']       = TradeContext.BESBNO  +  PL_ACC_NXYDQSWZ       #借方账号
        input_dict['RBAC']       = TradeContext.BESBNO  +  PL_ACC_DYKJQ          #贷方账号,2621,多余款
        input_dict['CATR']       = '0' 
        TradeContext.RVFG        = '0'                                           #红蓝字标识,0红冲
        TradeContext.OCCAMT      = str(input_dict['OCCAMT'])
        #=====开始调函数拼贷方账号第25位校验位====
        input_dict['SBAC'] = rccpsHostFunc.CrtAcc(input_dict['SBAC'], 25)
        input_dict['RBAC'] = rccpsHostFunc.CrtAcc(input_dict['RBAC'], 25)
    else:
        #为抹账赋值会计分录
        input_dict['SBAC']       = input_dict['PYRACC'] 
        input_dict['RBAC']       = TradeContext.BESBNO  +  PL_ACC_NXYDQSWZ
        input_dict['CATR']       = '1' 
        TradeContext.OCCAMT      = "-" + str(input_dict['OCCAMT'])
        TradeContext.RVFG        = ''                                            #红蓝字标识,0红冲
        #=====开始调函数拼贷方账号第25位校验位====
        #TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
        input_dict['RBAC'] = rccpsHostFunc.CrtAcc(input_dict['RBAC'], 25)

    #主机记账接口
    TradeContext.HostCode ='8813'
    
    TradeContext.CLDT     = input_dict['BJEDTE']                           #存放原前置日期
    TradeContext.UNSQ     = input_dict['BSPSQN']                           #存放原前置流水号
    
    if rccpsGetFunc.GetRBSQ(PL_BRSFLG_SND) == -1 :                         #前置流水号new
        return AfaFlowControl.ExitThisFlow('A099','产生新前置流水号失败')
    TradeContext.FEDT=AfaUtilTools.GetHostDate( )                          #前置日期new
    
    TradeContext.ACUR     = '1'                                            #重复次数
    TradeContext.CATR     = input_dict['CATR']                             #现转标识 
    TradeContext.RCCSMCD  = PL_RCCSMCD_WCH                                 #主机摘要代码
    TradeContext.DASQ     = ''
    
    TradeContext.SBAC     = input_dict['SBAC']                             #借方账号
    TradeContext.RBAC     = input_dict['RBAC']                             #贷方账号
    
    
    AfaLoggerFunc.tradeInfo( '借方账号:' + TradeContext.SBAC )
    AfaLoggerFunc.tradeInfo( '贷方账号:' + TradeContext.RBAC )
    
    AfaLoggerFunc.tradeInfo(">>>结束汇兑往账抹账会计分录赋值")
    
    return True     

##汇兑来帐记帐
def HDLZJZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>开始汇兑来账记账会计分录赋值")
        
    if not input_dict.has_key('PYEACC'):
        return AfaFlowControl.ExitThisFlow("S999","收款人账号不能为空")
            
    if not input_dict.has_key('OTNM'):
        return AfaFlowControl.ExitThisFlow("S999","收款人户名不能为空")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","交易金额不能为空")
        
    if not input_dict.has_key('accflag'):
        return AfaFlowControl.ExitThisFlow("S999","记挂账标志不能为空")
        
    if not input_dict.has_key('BESBNO'):
        return AfaFlowControl.ExitThisFlow("S999","机构号不能为空")

    if (TradeContext.existVariable( "SBACACNM" ) and len(TradeContext.SBACACNM) != 0):       #付款人户名
          TradeContext.ACNM      =      TradeContext.SBACACNM
    else:
          TradeContext.ACNM      =      ''
    #=====设置记账函数接口====

    TradeContext.HostCode = '8813'
    TradeContext.BRSFLG   = PL_BRSFLG_RCV                                    #往来标识:往账
    TradeContext.RCCSMCD  = PL_RCCSMCD_HDLZ                                  #主机摘要代码：汇兑来账
    TradeContext.ACUR = '1'
    
    TradeContext.OCCAMT   = input_dict['OCCAMT']
    TradeContext.BESBNO   = input_dict['BESBNO']
    TradeContext.accflag  = input_dict['accflag']

    if TradeContext.accflag == '0':
        AfaLoggerFunc.tradeInfo('>>>自动入账')
        TradeContext.STRINFO = '自动入账'
        TradeContext.BCSTAT  = PL_BCSTAT_AUTO                            #自动入账
        TradeContext.BDWFLG  = PL_BDWFLG_WAIT                            #处理中
        
        TradeContext.SBAC    = TradeContext.BESBNO + PL_ACC_NXYDQSLZ     #借方账户
        TradeContext.SBAC    = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
        
        TradeContext.RBAC    = input_dict['PYEACC']                      #贷方账号
        TradeContext.OTNM    = input_dict['OTNM']                        #贷方户名
        
        AfaLoggerFunc.tradeInfo( '借方账号:' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '贷方账号:' + TradeContext.RBAC )
    else:
        AfaLoggerFunc.tradeInfo('>>>自动挂账')
        TradeContext.STRINFO = '自动挂账'
        TradeContext.BCSTAT  = PL_BCSTAT_HANG                            #自动挂账
        TradeContext.BDWFLG  = PL_BDWFLG_WAIT                            #处理中
            
        TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ        #借方账户
        TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
        
        TradeContext.REAC = TradeContext.BESBNO + PL_ACC_NXYDXZ          #挂账账号
        TradeContext.REAC = rccpsHostFunc.CrtAcc(TradeContext.REAC, 25)

        AfaLoggerFunc.tradeInfo( '借方账号:' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '挂账账号:' + TradeContext.REAC )

    AfaLoggerFunc.tradeInfo(">>>结束汇兑来账记账会计分录赋值")
    return True

##汇兑来帐挂帐
def HDLZGZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>开始汇兑来账挂账会计分录赋值")
            
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","交易金额不能为空")
        
    if not input_dict.has_key('accflag'):
        return AfaFlowControl.ExitThisFlow("S999","记挂账标志不能为空")
        
    if not input_dict.has_key('BESBNO'):
        return AfaFlowControl.ExitThisFlow("S999","机构号不能为空")

    #=====设置记账函数接口====

    TradeContext.HostCode = '8813'
    TradeContext.BRSFLG   = PL_BRSFLG_RCV                                    #往来标识:往账
    TradeContext.RCCSMCD  = PL_RCCSMCD_HDLZ                                  #主机摘要代码：汇兑来账
    TradeContext.ACUR = '1'
    
    TradeContext.OCCAMT   = input_dict['OCCAMT']
    TradeContext.BESBNO   = input_dict['BESBNO']
    TradeContext.accflag  = input_dict['accflag']
    
    if TradeContext.accflag == '0':
        AfaLoggerFunc.tradeInfo('>>>自动挂账')
        TradeContext.STRINFO = '自动挂账'
        TradeContext.NOTE3 = '主机记账失败,挂账!'
        TradeContext.BCSTAT  = PL_BCSTAT_HANG                            #自动挂账
        TradeContext.BDWFLG  = PL_BDWFLG_WAIT                            #处理中
            
        TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ        #借方账户
        TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
        
        TradeContext.REAC = TradeContext.BESBNO + PL_ACC_NXYDXZ          #挂账账号
        TradeContext.REAC = rccpsHostFunc.CrtAcc(TradeContext.REAC, 25)

        AfaLoggerFunc.tradeInfo( '借方账号:' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '挂账账号:' + TradeContext.REAC )

    AfaLoggerFunc.tradeInfo(">>>结束汇兑来账挂账会计分录赋值")
    return True


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
       
    TradeContext.PKFG = 'T'                                             #通存通兑标识
    TradeContext.CATR = '0'                                             #现转标识:0-现金
    TradeContext.RCCSMCD  = PL_RCCSMCD_XJTCWZ                           #主机摘要码:现金通存往账
    TradeContext.OCCAMT = str(input_dict['OCCAMT'])
    TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_QTYSK
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
        
        TradeContext.I2PKFG = 'T'                                       #通存通兑标识
        TradeContext.I2CATR = '0'                                       #现转标识:0-现金
        TradeContext.I2TRAM = str(input_dict['CUSCHRG'])                #手续费金额
        TradeContext.I2SMCD = PL_RCCSMCD_SXF                            #主机摘要码:手续费
        TradeContext.I2SBAC = TradeContext.BESBNO + PL_ACC_QTYSK
        TradeContext.I2SBAC = rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM = '其他应首款'
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
        
    TradeContext.PKFG = 'T'                                         #通存通兑标识
    TradeContext.RVFG = '2'                                         #红蓝字标志 2
    TradeContext.CATR = '0'                                         #现转标识:0-现金
    TradeContext.OCCAMT = str(input_dict['OCCAMT'])                 #交易金额
    TradeContext.RCCSMCD = input_dict['RCCSMCD']                    #主机摘要码:现金通存往账
    TradeContext.SBAC = ''
    TradeContext.ACNM = ''
    TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSWZ       #贷方账号
    TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
    TradeContext.OTNM = "农信银待清算往账"
    TradeContext.CTFG = '7'                                         #本金手续费标示
    
    AfaLoggerFunc.tradeInfo("借方账号1:[" + TradeContext.SBAC + "]")
    AfaLoggerFunc.tradeInfo("贷方账号1:[" + TradeContext.RBAC + "]")
    
    if input_dict['CHRGTYP'] == '0':
        #现金收取手续费
        TradeContext.ACUR   = '2'                                       #重复次数
        
        TradeContext.I2PKFG = 'T'                                       #通存通兑标识
        TradeContext.I2RVFG = '2'                                       #红蓝字标志 2
        TradeContext.I2CATR = '0'                                       #现转标识:0-现金
        TradeContext.I2TRAM = str(input_dict['CUSCHRG'])                #手续费金额
        TradeContext.I2SMCD = input_dict['RCCSMCD']                     #主机摘要码:手续费
        TradeContext.I2SBAC = ''
        TradeContext.I2ACNM = ''
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
      
    TradeContext.PKFG = 'T'                                         #通存通兑标识
    
    TradeContext.OCCAMT = str(input_dict['OCCAMT'])                 #出票金额
    TradeContext.RCCSMCD  = PL_RCCSMCD_BZYWZ                        #主机摘要码:本转异往账
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
        
        TradeContext.I2PKFG = 'T'                                       #通存通兑标识
        TradeContext.I2CATR = '0'                                       #现转标识:0-现金
        TradeContext.I2TRAM = str(input_dict['CUSCHRG'])                #手续费金额
        TradeContext.I2SMCD = PL_RCCSMCD_SXF                            #主机摘要码:手续费
        TradeContext.I2SBAC = ""                                        #借方账号:柜员尾箱
        TradeContext.I2ACNM = ""                                        
        TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_TCTDSXF      #贷方账号:通存通兑手续费
        TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM = "手续费"
        TradeContext.I2CTFG = '8'                                       #本金手续费标示
        
    elif TradeContext.CHRGTYP == '1':
        #本地账户收取
        AfaLoggerFunc.tradeInfo(">>>本地账户收取手续费")
        TradeContext.ACUR = '2'                                         #重复次数
        
        TradeContext.I2PKFG = 'T'                                       #通存通兑标识
        TradeContext.I2TRAM = str(input_dict['CUSCHRG'])                #手续费金额
        TradeContext.I2SMCD = PL_RCCSMCD_SXF                            #主机摘要码:手续费
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
    
    if input_dict['CHRGTYP'] == '0':
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
        
        TradeContext.ACUR = '2'                                         #重复次数
        
        TradeContext.PKFG = 'T'                                         #通存通兑标识
        TradeContext.OCCAMT = "-" + str(input_dict['OCCAMT'])           #交易金额
        TradeContext.RCCSMCD = input_dict['RCCSMCD']                    #主机摘要码:本转异往账
        TradeContext.SBAC = input_dict['PYRACC']                        #借方账号:客户账
        TradeContext.ACNM = input_dict['PYRNAM']                        #借方户名
        TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSWZ       #贷方账号:汇出汇款
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
        
        TradeContext.I2PKFG = 'T'                                       #通存通兑标识
        TradeContext.I2RVFG = '2'                                       #红蓝字标志 2
        TradeContext.I2CATR = '0'                                       #现转标识:0-现金
        TradeContext.I2TRAM = str(input_dict['CUSCHRG'])                #手续费金额
        TradeContext.I2SMCD = input_dict['RCCSMCD']                     #主机摘要码:手续费
        TradeContext.I2SBAC = ""                                        #借方账号:柜员尾箱
        TradeContext.I2ACNM = ""                                        
        TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_TCTDSXF      #贷方账号:通存通兑手续费
        TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM = "手续费"
        TradeContext.I2CTFG = '8'                                       #本金收学费标示
        
        AfaLoggerFunc.tradeInfo("借方账号2:[" + TradeContext.I2SBAC + "]")
        AfaLoggerFunc.tradeInfo("贷方账号2:[" + TradeContext.I2RBAC + "]")
    else:
        TradeContext.HostCode='8820'
        if not input_dict.has_key('FEDT'):
            return AfaFlowControl.ExitThisFlow("S999","原前置日期不能为空")
        if not input_dict.has_key('RBSQ'):
            return AfaFlowControl.ExitThisFlow("S999","原前置流水号不能为空")
            
        TradeContext.BOJEDT = input_dict['FEDT']
        TradeContext.BOSPSQ = input_dict['RBSQ']
        
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
        TradeContext.RCCSMCD =  PL_RCCSMCD_CX                                 #摘要代码 
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  '农信银往账'                                  #借方户名
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '应解汇款'                                    #贷方户名
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #发生额
        TradeContext.PKFG    = 'T'                                            #通存通兑标示
        TradeContext.CTFG    = '9'                                            #本金收学费标示
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:借方账号' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:贷方账号' + TradeContext.RBAC )
        #=========交易金额============
        TradeContext.I2SMCD  =  PL_RCCSMCD_CX                                 #摘要代码
        TradeContext.I2SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #借方账号
        TradeContext.I2SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM  =  '应解汇款'                                    #借方户名
        TradeContext.I2RBAC  =  ''                                            #贷方账号
        TradeContext.I2OTNM  =  ''                                            #贷方户名
        TradeContext.I2TRAM  =  str(input_dict['OCCAMT'])                       #发生额
        TradeContext.I2CTFG  = '7'
        TradeContext.I2PKFG  = 'T'
        #TradeContext.I2WARNTNO = ''
        #TradeContext.I2CERTTYPE = ''
        #TradeContext.I2CERTNO = ''
        TradeContext.I2CATR  =  '0'                                           #现转标志
        AfaLoggerFunc.tradeInfo( '>>>交易金额:借方账号' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额:贷方账号' + TradeContext.I2RBAC )
        #=========结算手续费收入户===========
        TradeContext.I3SMCD  =  PL_RCCSMCD_CX                                 #摘要代码
        TradeContext.I3SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #借方账号
        TradeContext.I3SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
        TradeContext.I3ACNM  =  '应解汇款'                                    #借方户名
        TradeContext.I3RBAC  =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #贷方账号
        TradeContext.I3RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
        TradeContext.I3OTNM  =  '结算手续费'                                  #贷方户名
        TradeContext.I3TRAM  =  str(input_dict['CUSCHRG'])                    #发生额
        TradeContext.I3CTFG  = '8'
        TradeContext.I3PKFG  = 'T'
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:借方账号' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:贷方账号' + TradeContext.I3RBAC )
    
    elif input_dict['CHRGTYP'] == '0':                                          #现金
        #=====本金====
        TradeContext.ACUR    =  '2'                                           #记账次数
        TradeContext.RCCSMCD =  PL_RCCSMCD_CX                                 #摘要代码
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  '农信银往账'                                  #借方户名
        TradeContext.RBAC    =  ''                                            #贷方账号
        TradeContext.OTNM    =  ''                                            #贷方户名
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #金额
        TradeContext.CTFG    = '7'
        TradeContext.PKFG    = 'T'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO  = ''
        TradeContext.CATR    =  '0'                                             #现转标志
        
        #=====手续费记账赋值====
        TradeContext.I2SMCD  =  PL_RCCSMCD_CX                                 #摘要代码
        TradeContext.I2SBAC  =  ''                                            #借方账号
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #贷方账号
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  '手续费科目'                                  #贷方户名
        TradeContext.I2TRAM  =  str(input_dict['CUSCHRG'])                    #金额
        TradeContext.I2CTFG  =  '8'
        TradeContext.I2PKFG  =  'T'
        TradeContext.I2CATR  =  '0'                                           #现转标志
    elif input_dict['CHRGTYP'] == '2':
        #=====不收费====
        TradeContext.ACUR    =  '1'                                           #记账次数
        TradeContext.RCCSMCD =  PL_RCCSMCD_XJTDWZ                             #摘要代码
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.RBAC    =  ''                                            #贷方账号
        TradeContext.OTNM    =  ''                                            #贷方户名
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #金额
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    =  'T'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO  = ''
        TradeContext.CATR    =  '0'                                             #现转标志
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
        TradeContext.RCCSMCD =  input_dict['RCCSMCD']                         #摘要代码
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  '应解汇款'                                    #借方户名
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #贷方账号
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '结算手续费'                                  #贷方户名
        TradeContext.OCCAMT  =  "-" + str(input_dict['CUSCHRG'])              #发生额
        TradeContext.CTFG    = '8'
        TradeContext.PKFG    = 'T'
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:借方账号' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:贷方账号' + TradeContext.RBAC )
        #=========交易金额============
        TradeContext.I2RVFG  = '0'                                            #红蓝字标志
        TradeContext.I2SMCD  =  input_dict['RCCSMCD']                         #摘要代码
        TradeContext.I2SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #借方账号
        TradeContext.I2SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM  =  '应解汇款'                                    #借方户名
        TradeContext.I2RBAC  =  ''                                            #贷方账号
        TradeContext.I2OTNM  =  ''                                            #贷方户名
        TradeContext.I2TRAM  =  str(input_dict['OCCAMT'])                     #发生额
        TradeContext.I2CTFG  = '7'
        TradeContext.I2PKFG  = 'T'
        #TradeContext.I2WARNTNO = ''
        #TradeContext.I2CERTTYPE = ''
        #TradeContext.I2CERTNO = ''
        TradeContext.I2CATR  =  '0'                                           #现转标志
        AfaLoggerFunc.tradeInfo( '>>>交易金额:借方账号' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额:贷方账号' + TradeContext.I2RBAC )
        #=========交易金额+手续费===================
        TradeContext.I3SMCD  =  input_dict['RCCSMCD']                         #摘要代码
        TradeContext.I3SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
        TradeContext.I3SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
        TradeContext.I3ACNM  =  '农信银往账'                                  #借方户名
        TradeContext.I3RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
        TradeContext.I3RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
        TradeContext.I3OTNM  =  '应解汇款'                                    #贷方户名
        TradeContext.I3TRAM  =  "-" + str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #发生额
        TradeContext.I3PKFG  = 'T'
        TradeContext.I3CTFG  = '9'
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:借方账号' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:贷方账号' + TradeContext.I3RBAC )
    
    elif input_dict['CHRGTYP'] == '0':                                        #现金
        #=====本金====
        TradeContext.RVFG    =  '0'                                           #红蓝字标志
        TradeContext.ACUR    =  '2'                                           #记账次数
        TradeContext.RCCSMCD =  input_dict['RCCSMCD']                         #摘要代码
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  '农信银往账'                                  #借方户名
        TradeContext.RBAC    =  ''                                            #贷方账号
        TradeContext.OTNM    =  ''                                            #贷方户名
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #金额
        TradeContext.CTFG    = '7'
        TradeContext.PKFG    = 'T'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO  = ''
        TradeContext.CATR    =  '0'                                           #现转标志
        
        #=====手续费记账赋值====
        TradeContext.I2RVFG  =  '2'                                           #红蓝字标志
        TradeContext.I2SMCD  =  input_dict['RCCSMCD']                         #摘要代码
        TradeContext.I2SBAC  =  ''                                            #借方账号
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #贷方账号
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  '手续费科目'                                  #贷方户名
        TradeContext.I2TRAM  =  str(input_dict['CUSCHRG'])                    #金额
        TradeContext.I2CTFG  =  '8'
        TradeContext.I2PKFG  =  'T'
        TradeContext.I2CATR  =  '0'                                           #现转标志
    elif input_dict['CHRGTYP'] == '2':
        #=====不收费====
        TradeContext.RVFG    =  '0'                                           #红蓝字标志
        TradeContext.ACUR    =  '1'                                           #记账次数
        TradeContext.RCCSMCD =  input_dict['RCCSMCD']                         #摘要代码
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.RBAC    =  ''                                            #贷方账号
        TradeContext.OTNM    =  ''                                            #贷方户名
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #金额
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    =  'T'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO  = ''
        TradeContext.CATR    =  '0'                                             #现转标志
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
        TradeContext.RCCSMCD =  PL_RCCSMCD_YZBWZ                              #摘要代码  PL_RCCSMCD_YZBWZ 异转本
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  '农信银往账'                                  #借方户名
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS           #贷方账号
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '应解汇款'                                    #贷方户名
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #发生额
        TradeContext.PKFG    = 'T'
        TradeContext.CTFG    = '9'
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:借方账号' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:贷方账号' + TradeContext.RBAC )
        #=========交易金额============
        TradeContext.I2SMCD  =  PL_RCCSMCD_YZBWZ                              #摘要代码
        TradeContext.I2SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #借方账号
        TradeContext.I2SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM  =  '应解汇款'                                    #借方户名
        TradeContext.I2RBAC  =  input_dict['PYEACC']                          #贷方账号
        TradeContext.I2OTNM  =  input_dict['PYENAM']                          #贷方户名
        TradeContext.I2TRAM  =  str(input_dict['OCCAMT'])                     #发生额
        TradeContext.I2CTFG  = '7'
        TradeContext.I2PKFG  = 'T'
        TradeContext.I2WARNTNO = ''
        TradeContext.I2CERTTYPE = ''
        TradeContext.I2CERTNO = ''
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
        TradeContext.I3TRAM  =  str(input_dict['CUSCHRG'])                    #发生额
        TradeContext.I3CTFG  = '8'
        TradeContext.I3PKFG  = 'T'
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:借方账号' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:贷方账号' + TradeContext.I3RBAC )

    elif input_dict['CHRGTYP'] == '0':
        #=====本金====
        TradeContext.ACUR    =  '2'                                           #记账次数
        TradeContext.RCCSMCD =  PL_RCCSMCD_YZBWZ                              #摘要代码
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
        TradeContext.SBAC    = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  '农信银往账'                                  #借方户名
        TradeContext.RBAC    =  input_dict['PYEACC']                          #贷方账号
        TradeContext.OTNM    =  input_dict['PYENAM']                          #贷方户名
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #金额
        TradeContext.CTFG  = '7'
        TradeContext.PKFG  = 'T'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
        
        #=====手续费记账赋值====
        TradeContext.I2SMCD  =  PL_RCCSMCD_SXF                                #摘要代码
        TradeContext.I2SBAC  =  ''                                            #借方账号
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #贷方账号
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  '手续费科目'                                  #贷方户名
        TradeContext.I2TRAM  =  str(input_dict['CUSCHRG'])                    #金额
        TradeContext.I2CTFG  =  '8'
        TradeContext.I2PKFG  =  'T'
        TradeContext.I2CATR  =  '0'                                           #现转标志
    elif input_dict['CHRGTYP'] == '2':
        #=====不收费====
        TradeContext.ACUR    =  '1'                                           #记账次数
        TradeContext.RCCSMCD =  PL_RCCSMCD_YZBWZ                              #摘要代码
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.RBAC    =  input_dict['PYEACC']                          #贷方账号
        TradeContext.OTNM    =  input_dict['PYENAM']                          #贷方户名
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #金额
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    =  'T'
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
    
    if input_dict['CHRGTYP'] == '0':
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
        
        #=====本金====
        TradeContext.ACUR    =  '2'                                           #记账次数
        TradeContext.RCCSMCD =  input_dict['RCCSMCD']                         #摘要代码
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #借方账号
        TradeContext.SBAC    = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  '农信银往账'                                  #借方户名
        TradeContext.RBAC    =  input_dict['PYEACC']                          #贷方账号
        TradeContext.OTNM    =  input_dict['PYENAM']                          #贷方户名
        TradeContext.OCCAMT  =  "-" + str(input_dict['OCCAMT'])               #金额
        TradeContext.CTFG    = '7'
        TradeContext.PKFG    = 'T'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
        
        #=====手续费记账赋值====
        TradeContext.I2RVFG  = '2'                                            #红蓝字标志 2
        TradeContext.I2SMCD  =  input_dict['RCCSMCD']                         #摘要代码
        TradeContext.I2SBAC  =  ''                                            #借方账号
        TradeContext.I2SBNM  =  ''
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #贷方账号
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  '手续费科目'                                  #贷方户名
        TradeContext.I2TRAM  =  str(input_dict['CUSCHRG'])                    #金额
        TradeContext.I2CTFG  =  '8'
        TradeContext.I2PKFG  =  'T'
        TradeContext.I2CATR  =  '0'                                           #现转标志
    else:
        TradeContext.HostCode='8820'
        if not input_dict.has_key('FEDT'):
            return AfaFlowControl.ExitThisFlow("S999","原前置日期不能为空")
        if not input_dict.has_key('RBSQ'):
            return AfaFlowControl.ExitThisFlow("S999","原前置流水号不能为空")
            
        TradeContext.BOJEDT = input_dict['FEDT']
        TradeContext.BOSPSQ = input_dict['RBSQ']
    
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
       
    TradeContext.PKFG = 'T'                                             #通存通兑标识
#    TradeContext.CATR = '0'                                             #现转标识:0-现金
    TradeContext.RCCSMCD  = PL_RCCSMCD_XJTCLZ                           #主机摘要码:现金通存来账    TradeContext.OCCAMT = str(input_dict['OCCAMT'])
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
      
    TradeContext.PKFG = 'T'                                         #通存通兑标识
    
    TradeContext.OCCAMT = str(input_dict['OCCAMT'])                 #出票金额
    TradeContext.RCCSMCD  = PL_RCCSMCD_BZYLZ                        #主机摘要码:本转异来账
    TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ       #借方账号:农信银待清算来账
    TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
    TradeContext.ACNM = "农信银待清算来账"                          #借方户名
    TradeContext.RBAC = input_dict['PYEACC']                        #贷方账号:收款人账户
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
        TradeContext.I3SMCD =  PL_RCCSMCD_XJTDLZ                                 #摘要代码 
        TradeContext.I3SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #借方账号
        TradeContext.I3SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
        TradeContext.I3ACNM    =  '农信银待解临时款'                            #借方户名
        TradeContext.I3RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ         #贷方账号
        TradeContext.I3RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
        TradeContext.I3OTNM    =  '农信银来账'                                  #贷方户名
        TradeContext.I3TRAM  =  str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #发生额
        TradeContext.I3PKFG    = 'T'                                            #通存通兑标示
        TradeContext.I3CTFG    = '9'                                            #本金收学费标示
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:借方账号' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:贷方账号' + TradeContext.I3RBAC )
        #=========交易金额============
        TradeContext.RCCSMCD =  PL_RCCSMCD_XJTDLZ                             #摘要代码
        TradeContext.SBAC  =  input_dict['PYRACC']                          #借方账号
        TradeContext.ACNM  =  input_dict['PYRNAM']                          #借方户名
        TradeContext.RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM  =  '农信银待解临时款'                            #贷方户名
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #发生额
        TradeContext.CTFG  = '7'
        TradeContext.PKFG  = 'T'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO = ''
#        TradeContext.CATR  =  '0'                                           #现转标志
        AfaLoggerFunc.tradeInfo( '>>>交易金额:借方账号' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额:贷方账号' + TradeContext.RBAC )
        #=========结算手续费收入户===========
        TradeContext.I2SMCD  =  PL_RCCSMCD_SXF                                #摘要代码
        TradeContext.I2SBAC  =  input_dict['PYRACC']                          #借方账号
        TradeContext.I2ACNM  =  input_dict['PYRNAM']                          #借方户名
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  '农信银待解临时款'                            #贷方户名
        TradeContext.I2TRAM  =  str(input_dict['CUSCHRG'])                    #发生额
        TradeContext.I2CTFG  = '8'
        TradeContext.I2PKFG  = 'T'
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:借方账号' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:贷方账号' + TradeContext.I2RBAC )
    
    elif input_dict['CHRGTYP'] == '0':                                          #现金
        #=====本金====
        TradeContext.RCCSMCD =  PL_RCCSMCD_XJTDLZ                             #摘要代码
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ         #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  '农信银待清算来账'                            #借方户名
        TradeContext.RBAC    =  input_dict['PYRACC']                          #贷方账号
        TradeContext.OTNM    =  input_dict['PYRNAM']                          #贷方户名
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #金额
        TradeContext.CTFG    = '7'
        TradeContext.PKFG    = 'T'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO  = ''
#        TradeContext.CATR    =  '0'                                             #现转标志
        
    elif input_dict['CHRGTYP'] == '2':
        #=====不收费====
        TradeContext.ACUR    =  '1'                                           #记账次数
        TradeContext.RCCSMCD =  PL_RCCSMCD_XJTDLZ                             #摘要代码
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ         #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  '农信银待清算来账'                            #借方户名
        TradeContext.RBAC    =  input_dict['PYRACC']                          #贷方账号
        TradeContext.OTNM    =  input_dict['PYRNAM']                          #贷方户名
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #金额
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    =  'T'
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
        TradeContext.I3RCCSMCD =  PL_RCCSMCD_YZBWZ                                  #摘要代码  PL_RCCSMCD_YZBWZ 异转本
        TradeContext.I3SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS              #借方账号
        TradeContext.I3SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)        
        TradeContext.I3ACNM    =  '农信银待解临时款'                                #借方户名
        TradeContext.I3RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ             #贷方账号
        TradeContext.I3RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)        
        TradeContext.I3OTNM    =  '农信银待清算来账'                                #贷方户名
        TradeContext.I3TRAM  =  str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #发生额
        TradeContext.I3PKFG    = 'T'
        TradeContext.I3CTFG    = '9'
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:借方账号' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:贷方账号' + TradeContext.I3RBAC )
        #=========交易金额============
        TradeContext.RCCSMCD  =  PL_RCCSMCD_YZBWZ                              #摘要代码
        TradeContext.SBAC  =  input_dict['PYRACC']                          #借方账号
        TradeContext.ACNM  =  input_dict['PYRNAM']                          #借方户名
        TradeContext.RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
        TradeContext.RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM  =  '农信银待解临时款'                            #贷方户名
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #发生额
        TradeContext.CTFG  = '7'
        TradeContext.PKFG  = 'T'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
        AfaLoggerFunc.tradeInfo( '>>>交易金额:借方账号' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额:贷方账号' + TradeContext.RBAC )
        #=========结算手续费收入户===========
        TradeContext.I2SMCD  =  PL_RCCSMCD_SXF                                #摘要代码
        TradeContext.I2SBAC  =  input_dict['PYRACC']          #借方账号
        TradeContext.I2ACNM  =  input_dict['PYRNAM']                                    #借方户名
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  '农信银待解临时款'                                  #贷方户名
        TradeContext.I2TRAM  =  str(input_dict['CUSCHRG'])                    #发生额
        TradeContext.I2CTFG  = '8'
        TradeContext.I2PKFG  = 'T'
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:借方账号' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:贷方账号' + TradeContext.I2RBAC )

    elif input_dict['CHRGTYP'] == '0':
        #=====本金====
        TradeContext.ACUR    =  '1'                                           #记账次数
        TradeContext.RCCSMCD =  PL_RCCSMCD_YZBWZ                              #摘要代码
        TradeContext.SBAC    =  input_dict['PYRACC']                          #借方账号
        TradeContext.ACNM    =  input_dict['PYRNAM']                          #借方户名
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ          #贷方账号
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '农信银待解临时款'                            #贷方户名
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #金额
        TradeContext.CTFG  = '7'
        TradeContext.PKFG  = 'T'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
        
    elif input_dict['CHRGTYP'] == '2':
        #=====不收费====
        TradeContext.ACUR    =  '1'                                           #记账次数
        TradeContext.RCCSMCD =  PL_RCCSMCD_YZBWZ                              #摘要代码
        TradeContext.SBAC    =  input_dict['PYRACC']                          #借方账号
        TradeContext.ACNM    =  input_dict['PYRNAM']                          #借方户名
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ          #贷方账号
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '农信银待解临时款'                            #贷方户名
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #金额
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    =  'T'
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
#    TradeContext.CATR = '0'                                             #现转标识:0-现金
    TradeContext.RCCSMCD  = input_dict['RCCSMCD']                           #主机摘要码:现金通存来账    TradeContext.OCCAMT = str(input_dict['OCCAMT'])
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
    TradeContext.RCCSMCD  = input_dict['RCCSMCD']                        #主机摘要码:本转异来账
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
        
    TradeContext.CTFG = '7'                                             #本金收学费标示
    
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
        TradeContext.I3SMCD =  input_dict['RCCSMCD']                                 #摘要代码 
        TradeContext.I3SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #借方账号
        TradeContext.I3SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
        TradeContext.I3ACNM    =  '农信银待解临时款'                            #借方户名
        TradeContext.I3RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ         #贷方账号
        TradeContext.I3RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
        TradeContext.I3OTNM    =  '农信银来账'                                  #贷方户名
        TradeContext.I3TRAM    = "-" + str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #发生额
        TradeContext.I3PKFG    = 'T'                                            #通存通兑标示
        TradeContext.I3CTFG    = '9'                                            #本金收学费标示
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:借方账号' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:贷方账号' + TradeContext.I3RBAC )
        #=========交易金额============
        TradeContext.RCCSMCD =  input_dict['RCCSMCD']                             #摘要代码
        TradeContext.SBAC  =  input_dict['PYRACC']                          #借方账号
        TradeContext.ACNM  =  input_dict['PYRNAM']                          #借方户名
        TradeContext.RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM  =  '农信银待解临时款'                            #贷方户名
        TradeContext.OCCAMT  =  "-" + str(input_dict['OCCAMT'])                     #发生额
        TradeContext.CTFG  = '7'
        TradeContext.PKFG  = 'T'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO = ''
#        TradeContext.CATR  =  '0'                                           #现转标志
        AfaLoggerFunc.tradeInfo( '>>>交易金额:借方账号' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额:贷方账号' + TradeContext.RBAC )
        #=========结算手续费收入户===========
        TradeContext.I2SMCD  =  input_dict['RCCSMCD']                                #摘要代码
        TradeContext.I2SBAC  =  input_dict['PYRACC']                          #借方账号
        TradeContext.I2ACNM  =  input_dict['PYRNAM']                          #借方户名
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  '农信银待解临时款'                            #贷方户名
        TradeContext.I2TRAM  =  "-" + str(input_dict['CUSCHRG'])                    #发生额
        TradeContext.I2CTFG  = '8'
        TradeContext.I2PKFG  = 'T'
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:借方账号' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:贷方账号' + TradeContext.I2RBAC )
    
    elif input_dict['CHRGTYP'] == '0':                                          #现金
        #=====本金====
        TradeContext.RCCSMCD =  input_dict['RCCSMCD']                             #摘要代码
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ         #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  '农信银待清算来账'                            #借方户名
        TradeContext.RBAC    =  input_dict['PYRACC']                          #贷方账号
        TradeContext.OTNM    =  input_dict['PYRNAM']                          #贷方户名
        TradeContext.OCCAMT  =  "-" + str(input_dict['OCCAMT'])                     #金额
        TradeContext.CTFG    = '7'
        TradeContext.PKFG    = 'T'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO  = ''
#        TradeContext.CATR    =  '0'                                             #现转标志
        
    elif input_dict['CHRGTYP'] == '2':
        #=====不收费====
        TradeContext.ACUR    =  '1'                                           #抹账次数
        TradeContext.RCCSMCD =  input_dict['RCCSMCD']                             #摘要代码
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ         #借方账号
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  '农信银待清算来账'                            #借方户名
        TradeContext.RBAC    =  input_dict['PYRACC']                          #贷方账号
        TradeContext.OTNM    =  input_dict['PYRNAM']                          #贷方户名
        TradeContext.OCCAMT  =  "-" + str(input_dict['OCCAMT'])                     #金额
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    =  'T'
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
        TradeContext.I3RCCSMCD =  input_dict['RCCSMCD']                                  #摘要代码  PL_RCCSMCD_YZBWZ 异转本
        TradeContext.I3SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS              #借方账号
        TradeContext.I3SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)        
        TradeContext.I3ACNM    =  '农信银待解临时款'                                #借方户名
        TradeContext.I3RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ             #贷方账号
        TradeContext.I3RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)        
        TradeContext.I3OTNM    =  '农信银待清算来账'                                #贷方户名
        TradeContext.I3TRAM    = "-" + str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #发生额
        TradeContext.I3PKFG    = 'T'
        TradeContext.I3CTFG    = '9'
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:借方账号' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额+手续费:贷方账号' + TradeContext.I3RBAC )
        #=========交易金额============
        TradeContext.RCCSMCD  =  input_dict['RCCSMCD']                              #摘要代码
        TradeContext.SBAC  =  input_dict['PYRACC']                          #借方账号
        TradeContext.ACNM  =  input_dict['PYRNAM']                          #借方户名
        TradeContext.RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
        TradeContext.RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM  =  '农信银待解临时款'                            #贷方户名
        TradeContext.OCCAMT  = "-" + str(input_dict['OCCAMT'])                     #发生额
        TradeContext.CTFG  = '7'
        TradeContext.PKFG  = 'T'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
        AfaLoggerFunc.tradeInfo( '>>>交易金额:借方账号' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>交易金额:贷方账号' + TradeContext.RBAC )
        #=========结算手续费收入户===========
        TradeContext.I2SMCD  =  input_dict['RCCSMCD']                                #摘要代码
        TradeContext.I2SBAC  =  input_dict['PYRACC']          #借方账号
        TradeContext.I2ACNM  =  input_dict['PYRNAM']                                    #借方户名
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #贷方账号
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  '农信银待解临时款'                                  #贷方户名
        TradeContext.I2TRAM  =  "-" + str(input_dict['CUSCHRG'])                    #发生额
        TradeContext.I2CTFG  = '8'
        TradeContext.I2PKFG  = 'T'
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:借方账号' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>结算手续费收入户:贷方账号' + TradeContext.I2RBAC )

    elif input_dict['CHRGTYP'] == '0':
        #=====本金====
        TradeContext.ACUR    =  '1'                                           #抹账次数
        TradeContext.RCCSMCD =  input_dict['RCCSMCD']                              #摘要代码
        TradeContext.SBAC    =  input_dict['PYRACC']                          #借方账号
        TradeContext.ACNM    =  input_dict['PYRNAM']                          #借方户名
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ          #贷方账号
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '农信银待解临时款'                            #贷方户名
        TradeContext.OCCAMT  =  "-" + str(input_dict['OCCAMT'])                     #金额
        TradeContext.CTFG  = '7'
        TradeContext.PKFG  = 'T'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
        
    elif input_dict['CHRGTYP'] == '2':
        #=====不收费====
        TradeContext.ACUR    =  '1'                                           #抹账次数
        TradeContext.RCCSMCD =  input_dict['RCCSMCD']                              #摘要代码
        TradeContext.SBAC    =  input_dict['PYRACC']                          #借方账号
        TradeContext.ACNM    =  input_dict['PYRNAM']                          #借方户名
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ          #贷方账号
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '农信银待解临时款'                            #贷方户名
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