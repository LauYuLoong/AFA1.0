# -*- coding: gbk -*-
################################################################################
#   农信银系统.公共方法类
#===============================================================================
#   程序文件:   RccpsFunc.py
#   修改时间:   2006-09-26
################################################################################
import exceptions,TradeContext,AfaDBFunc,TradeException,AfaUtilTools,ConfigParser,Party3Context,AfaLoggerFunc,AfaFlowControl,os,time
import rccpsDBTrcc_mbrifa,rccpsDBTrcc_subbra,rccpsDBTrcc_paybnk

from rccpsConst import *
from types import *

#========================================================================
#
#  程序名称：ChkPubInfo
#  入口参数： 
#  出口参数： Ture False
#  作    者： 刘雨龙
#  日    期： 20080610
#  功    能： 校验交易变量是否存在
#
#========================================================================
def ChkPubInfo(BRSFLG):

    AfaLoggerFunc.tradeInfo( '>>>交易变量值的有效性校验' )
    if( not TradeContext.existVariable( "sysId" ) ):
        TradeContext.sysId = 'RCC01'

    AfaLoggerFunc.tradeInfo('平台代码：' + TradeContext.sysId)
        
    if BRSFLG == PL_BRSFLG_SND:
        if( not TradeContext.existVariable( "BESBNO" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '机构号[BESBNO]值不存在!' )

        if( not TradeContext.existVariable( "BETELR" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '柜员号[BETELR]值不存在!' )
    else:    #PL_BRSFLG_RCV   来账
        if( not TradeContext.existVariable( "TRCCO" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '交易代码[TRCCO]值不存在!' )
        if( not TradeContext.existVariable( "BRSFLG" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '往来标识[BRSFLG]值不存在!' )

    return True
#========================================================================
#
#  程序名称：ChkSysInfo
#  入口参数： AFA:中间业务平台  RCCPS:中间业务平台&农信银系统 
#  出口参数： Ture False
#  作    者： 刘雨龙
#  日    期： 20080610
#  功    能： 输入参数为AFA时：只校验中间业务平台状态是否正常
#             输入参数RCCPS时：校验中间业务平台状态正常后，要
#             继续校验农信银系统状态是否为日间状态
#
#========================================================================
def ChkSysInfo( flag ):
   
    AfaLoggerFunc.tradeInfo( '>>>系统平台状态有效性校验' )
    sql = "select status from afa_system where sysid='"
    sql = sql + TradeContext.sysId + "'"
    records=AfaDBFunc.SelectSql( sql )
    if( records == None ):
        return AfaFlowControl.ExitThisFlow('A0025', "中间业务平台数据库操作失败" )
    elif( len( records ) == 0 ):
        return AfaFlowControl.ExitThisFlow('A0025', "中间业务平台农信银系统无记录" )
    elif( records[0][0] != '1' ):
        return AfaFlowControl.ExitThisFlow('A0025', "中间业务平台_农信银系统已关闭" )
    else:
        if flag == 'RCCPS':
            AfaLoggerFunc.tradeInfo( '>>>农信银系统状态有效性校验' )
            if ((not TradeContext.existVariable("TRCCO")) or len(TradeContext.TRCCO) == 0):
                return AfaFlowControl.ExitThisFlow('M999', "字段[TRCCO]为空错误")

            #=====查询农信银系统状态====
            if((TradeContext.TRCCO[0:2] == PL_TRCCO_HD) or (TradeContext.TRCCO == PL_TRCCO_HP)):
                dict = {'OPRTYPNO':PL_TRCCO_HD}
            #elif((TradeContext.TRCCO[0:2] == PL_TRCCO_TCTD) or (TradeContext.TRCCO == PL_TRCCO_QT)):
            else:
                dict = {'OPRTYPNO':PL_TRCCO_TCTD}

            records=rccpsDBTrcc_mbrifa.selectu( dict )
            AfaLoggerFunc.tradeInfo( 'record=' + str(records) )
            if( records == None ):
                return AfaFlowControl.ExitThisFlow('A0025', "农信银系统操作数据库失败" )
            if( len(records) <= 0 ):
                return AfaFlowControl.ExitThisFlow('A0025', "农信银系统没有开始营业" )
            elif( records['NWSYSST'] != '10' ):
                return AfaFlowControl.ExitThisFlow('A0025', "农信银系统没有开始营业" )
            else:
                AfaLoggerFunc.tradeInfo( '>>>农信银系统状态正常' )

    AfaLoggerFunc.tradeInfo( '>>>系统状态校验正常' )
    return True
#========================================================================
#
#  程序名称： ChkUnitInfo
#  入口参数： BRSFLG 
#  出口参数： Ture False
#  作    者： 刘雨龙
#  日    期： 20080610
#  功    能： 如果BRSFLG ＝ 1 表示来账，需要通过接收行号取机构号
#                 BRSFLG ＝ 0 表示往账，需要根据机构号取发送行号
#                 SUBFLG = PL_SUBFLG_AGE   表示代理
#                 SUBFLG = PL_SUBFLG_SUB   表示被代理
#
#========================================================================
def ChkUnitInfo( BRSFLG ):
    if BRSFLG == PL_BRSFLG_SND:
        AfaLoggerFunc.tradeInfo( '>>>开始通过机构号取行号' )
        #=====通存通兑业务直接使用清算中心行号====
        if TradeContext.existVariable('TRCCO') and TradeContext.TRCCO[:2] == '30':
            subbra = {'BESBNO':PL_BESBNO_BCLRSB}
        else:            
            #=====开始向字典赋值==== 
            subbra = {'BESBNO':TradeContext.BESBNO}
            
        #=====查询发送行号====
        sub = rccpsDBTrcc_subbra.selectu(subbra)
        if sub == None:
            return AfaFlowControl.ExitThisFlow('M999','数据库错误')
        if len(sub) <= 0:
            #return AfaFlowControl.ExitThisFlow('M999','机构号取发送行号无对应记录')
            return AfaFlowControl.ExitThisFlow('M999','非法机构')
        else:
            AfaLoggerFunc.tradeDebug('>>>BTOPSB['+sub['BTOPSB']+']')
            #=====刘雨龙 2008-07-25 新增代理机构查询====
            if sub['SUBFLG'] == PL_SUBFLG_SUB :     #被代理,'0' 张恒20091201 替换0 
                sel_sub = {'BESBNO':sub['BTOPSB']}
                                
                sel = rccpsDBTrcc_subbra.selectu(sel_sub)
                if sel == None:
                    return AfaFlowControl.ExitThisFlow('M999','数据库错误')
                if len(sel) <= 0:
                    return AfaFlowControl.ExitThisFlow('M999','非法机构')
                else:
                    TradeContext.SNDBNKCO = sel['BANKBIN']
            else:
                TradeContext.SNDBNKCO = sub['BANKBIN']

            AfaLoggerFunc.tradeInfo( '发送行号[SNDBNKCO]:' + TradeContext.SNDBNKCO )
            #====通过发送行号取行名====
            paybnk = {'BANKBIN':TradeContext.SNDBNKCO}
            pyb = rccpsDBTrcc_paybnk.selectu(paybnk)
            if pyb == None:
                return AfaFlowControl.ExitThisFlow('M999','数据库操作错误')
            if len(pyb) <= 0:
                #return AfaFlowControl.ExitThisFlow('M999','行号取发送行名无相应记录')
                return AfaFlowControl.ExitThisFlow('M999','非法机构')
            else:
                #if( (TradeContext.BJEDTE < pyb['EFCTDAT'] or pyb['BANKSTATUS'] != '1') and len(TradeContext.SNDBNKCO) == 10 ):
                #关彬捷  20081222 修改行号生效失效判断
                if( pyb['NOTE1'] != '1' ):
                    return AfaFlowControl.ExitThisFlow('M999','发送行号未生效')
                else:
                    TradeContext.SNDBNKNM = pyb['BANKNAM'] 
                    TradeContext.SNDSTLBIN = pyb['STLBANKBIN']
                    AfaLoggerFunc.tradeDebug( '发送行名[SNDBNKNM]:' + TradeContext.SNDBNKNM )
                    AfaLoggerFunc.tradeDebug( '发送成员行号[SNDSTLBIN]:' + TradeContext.SNDSTLBIN )

            #=====通过接收行号取接收行成员行号====
            if (TradeContext.existVariable("RCVBNKCO") and len(TradeContext.RCVBNKCO) == 10):
            #if len(TradeContext.RCVBNKCO) == 10:
                AfaLoggerFunc.tradeDebug('>>>普通汇兑行号')
                rcvstl = {'BANKBIN':TradeContext.RCVBNKCO}
                rcvpyb = rccpsDBTrcc_paybnk.selectu(rcvstl)
                if rcvpyb == None:
                    return AfaFlowControl.ExitThisFlow('M999','数据库操作错误')
                if len(rcvpyb) <= 0:
                    return AfaFlowControl.ExitThisFlow('M999','接收行号取接收成员行号无相应记录')
                else:
                    TradeContext.RCVSTLBIN = rcvpyb['STLBANKBIN'] 
                    TradeContext.RCVBNKNM  = rcvpyb['BANKNAM'] 
                    AfaLoggerFunc.tradeDebug('>>>接收行名['+TradeContext.RCVBNKNM+']')
                    AfaLoggerFunc.tradeDebug('>>>接收成员行号['+TradeContext.RCVSTLBIN+']')

                #=====通过OPRTYPNO判断发起行权限和接收行权限====
                if TradeContext.TRCCO[0:2] == '20':
                    #=====判断接收行号====
                    if rcvpyb['PRIVILEGE'][0:1] != '1':
                        return AfaFlowControl.ExitThisFlow('M999','此接收行号尚未开汇兑业务')
                elif TradeContext.TRCCO[0:2] == '21':
                    #=====判断接收行号====
                    if rcvpyb['PRIVILEGE'][1:2] != '1':
                        return AfaFlowControl.ExitThisFlow('M999','此接收行号尚未开通汇票业务')
                elif TradeContext.TRCCO[0:2] == '30':
                    #=====判断接收行号====
                    if rcvpyb['PRIVILEGE'][2:3] != '1':
                        return AfaFlowControl.ExitThisFlow('M999','此接收行号尚未开通通存通兑业务')
                AfaLoggerFunc.tradeDebug('>>>接收成员行号权限判断完成')
            #elif len(TradeContext.RCVBNKCO) < 10:
            else:
                if not TradeContext.existVariable('RCVBNKCO'):
                    TradeContext.RCVBNKCO = '1000000000'  
                                                                         
                    #=====通过行号找行名====
                    paybnk_dict = {'BANKBIN':TradeContext.RCVBNKCO}
                    pyba = rccpsDBTrcc_paybnk.selectu(paybnk_dict)
                    if pyba == None:
                        return AfaFlowControl.ExitThisFlow('M999','数据库操作错误')
                    if len(pyba) <= 0:
                        return AfaFlowControl.ExitThisFlow('M999','行号取发送行名无相应记录')
                    else:
                        TradeContext.RCVBNKNM = pyba['BANKNAM']
                        AfaLoggerFunc.tradeInfo( '接收行名[RCVBNKNM]:' + TradeContext.RCVBNKNM )
                         
                        if len(str(pyba['STLBANKBIN'])) == 0:
                            TradeContext.RCVSTLBIN = '9999999997' 
                        else:
                            TradeContext.RCVSTLBIN = pyba['STLBANKBIN']
                        
                        AfaLoggerFunc.tradeInfo( '接收成员行号[RCVSTLBIN]:' + TradeContext.RCVSTLBIN )
                elif len(TradeContext.RCVBNKCO) == 0:
                    TradeContext.RCVBNKCO = ' '
                elif len(TradeContext.RCVBNKCO) == 7:
                    #=====通过行号找行名====
                    paybnk_dict = {'BANKBIN':TradeContext.RCVBNKCO}
                    pyba = rccpsDBTrcc_paybnk.selectu(paybnk_dict)
                    if pyba == None:
                        return AfaFlowControl.ExitThisFlow('M999','数据库操作错误')
                    if len(pyba) <= 0:
                        return AfaFlowControl.ExitThisFlow('M999','行号取发送行名无相应记录')
                    else:
                        TradeContext.RCVBNKNM = pyba['BANKNAM']
                        AfaLoggerFunc.tradeInfo( '接收行名[RCVBNKNM]:' + TradeContext.RCVBNKNM )
                         
                        if len(str(pyba['STLBANKBIN'])) == 0:
                            TradeContext.RCVSTLBIN = '9999999997' 
                        else:
                            TradeContext.RCVSTLBIN = pyba['STLBANKBIN']
                        
                        AfaLoggerFunc.tradeInfo( '接收成员行号[RCVSTLBIN]:' + TradeContext.RCVSTLBIN )
                

            #=====通过OPRTYPNO判断发起行权限和接收行权限====
            if TradeContext.TRCCO[0:2] == '20':
                #=====判断发起行号====
                if pyb['PRIVILEGE'][0:1] != '1':
                    return AfaFlowControl.ExitThisFlow('M999','此发送行号尚未开通汇兑业务')
            #=====刘雨龙 20081013 新增“汇票解付”同汇兑业务权限====
            elif (TradeContext.TRCCO[0:2] == '21'  and TradeContext.TRCCO != '2100100'):
                #=====判断发起行号====
                if pyb['PRIVILEGE'][1:2] != '1':
                    return AfaFlowControl.ExitThisFlow('M999','此发送行号尚未开通汇票业务')
            elif TradeContext.TRCCO[0:2] == '30':
                #=====判断发起行号====
                if pyb['PRIVILEGE'][2:3] != '1':
                    return AfaFlowControl.ExitThisFlow('M999','此发送行号尚未开通通存通兑业务')
            AfaLoggerFunc.tradeDebug('>>>发起成员行号权限判断完成')
           
    elif BRSFLG == PL_BRSFLG_RCV:
        AfaLoggerFunc.tradeInfo( '>>>开始通过行号取机构号' )
        #=====判断接收行号是否存在====
        if not TradeContext.existVariable( "RCVBNKCO" ):
            TradeContext.BESBNO = PL_BESBNO_BCLRSB
            TradeContext.BETELR = PL_BETELR_AUTO
            AfaLoggerFunc.tradeInfo( '机构号[BESBNO]:' + TradeContext.BESBNO )
            return True

        #====开始向字典赋值====
        suba = {'BANKBIN':TradeContext.RCVBNKCO}
        suba['SUBFLG'] = PL_SUBFLG_AGE     #代理
        subd = rccpsDBTrcc_subbra.selectu(suba)
        if subd == None:
            return AfaFlowControl.ExitThisFlow('M999','数据库操作错误')
        if len(subd) <= 0:
            TradeContext.BESBNO = PL_BESBNO_BCLRSB
            TradeContext.BETELR = PL_BETELR_AUTO
            AfaLoggerFunc.tradeInfo( '机构号[BESBNO]:' + TradeContext.BESBNO )
        else:
            TradeContext.BESBNO = subd['BESBNO']
            TradeContext.BETELR = PL_BETELR_AUTO
            AfaLoggerFunc.tradeInfo( '机构号[BESBNO]:' + TradeContext.BESBNO )
    else:
        return AfaFlowControl.ExitThisFlow('M999','机构参数错误')
    AfaLoggerFunc.tradeInfo('>>>函数结束')

    return True
#========================================================================
#
#  程序名称： ChkNCCDate
#  入口参数： 
#  出口参数： Ture False
#  作    者： 刘雨龙
#  日    期： 20080610
#  功    能： 通过交易类型取中心日期
#
#========================================================================
def GetNCCDate():
    #=====查询农信银系统状态====
    AfaLoggerFunc.tradeInfo( '>>>查询NCC工作日期' )
    if((TradeContext.TRCCO[0:2] == PL_TRCCO_HD) or (TradeContext.TRCCO[0:2] == PL_TRCCO_HP)):
        dict = {'OPRTYPNO':PL_TRCCO_HD}
    #elif((TradeContext.TRCCO[0:2] == PL_TRCCO_TCTD) or (TradeContext.TRCCO == PL_TRCCO_QT)):
    else:
        dict = {'OPRTYPNO':PL_TRCCO_TCTD}

    records=rccpsDBTrcc_mbrifa.selectu( dict )
    
    if( records == None ):
        return AfaFlowControl.ExitThisFlow('A0025', "操作数据库失败" )
    elif(len(records) <= 0 ):
        return AfaFlowControl.ExitThisFlow('A0025', "取农信银中心日期失败" )
    else:
        TradeContext.NCCworkDate = records['NWWKDAT']
        AfaLoggerFunc.tradeInfo( '中心日期：' + TradeContext.NCCworkDate )

    return TradeContext.NCCworkDate
