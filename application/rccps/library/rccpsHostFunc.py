# -*- coding: gbk -*-
##################################################################
#   代收代付平台.与主机通讯函数
#=================================================================
#   程序文件:   rccpsHostFunc.py
#   修改时间:   2006-09-12
#
##################################################################
import TradeContext,AfaFunc,UtilTools,HostComm,HostContext,HostDataHandler,AfaLoggerFunc,os,AfaFlowControl
from types import *

def InitHostReq(hostType ):
    #初始化函数返回值变量
    AfaLoggerFunc.tradeInfo('初始化map文件信息[InitHostReq]')
    
    #关彬捷 20081105 移动InitHostReq函数中初始化8810主机接口相关程序至此处
    if (hostType == '8810'):

        AfaLoggerFunc.tradeInfo('>>>查询账户信息')

        HostContext.I1TRCD = TradeContext.HostCode              #主机码

        HostContext.I1SBNO = TradeContext.BESBNO                  #网点号

        HostContext.I1USID = TradeContext.BETELR              #柜员号

        if TradeContext.existVariable ( 'BEAUUS') and TradeContext.BEAUUS != '' and TradeContext.existVariable('BEAUPS') and TradeContext.BEAUPS != '':
            HostContext.I1AUUS = TradeContext.BEAUUS        #授权柜员
            HostContext.I1AUPS = TradeContext.BEAUPS           #授权密码
        else:
            HostContext.I1AUUS = ''
            HostContext.I1AUPS = ''

        if TradeContext.existVariable('TERMID') and TradeContext.TERMID != '':
            HostContext.I1WSNO = TradeContext.TERMID                #终端号
        else:
            HostContext.I1WSNO = '1234567890'                #终端号

        HostContext.I1ACNO = TradeContext.ACCNO                 #帐号
        HostContext.I1CYNO = '01'                              #币种

        if TradeContext.existVariable('PASSWD') and TradeContext.PASSWD != '':
            HostContext.I1CFFG = '0'
            HostContext.I1PSWD = TradeContext.PASSWD
        else:
            HostContext.I1CFFG = '1'                               #密码校验标志
            HostContext.I1PSWD = ''                                #密码
        if TradeContext.existVariable('WARNTNO') and TradeContext.WARNTNO != '':     #凭证种类
            HostContext.I1CETY = TradeContext.WARNTNO[0:2]

            HostContext.I1CCSQ = TradeContext.WARNTNO[2:]
        else:
            HostContext.I1CETY = ''                                #凭证种类
            HostContext.I1CCSQ = ''                             #凭证号码

        AfaLoggerFunc.tradeInfo("I1CETY=[" + HostContext.I1CETY + "]")
        AfaLoggerFunc.tradeInfo("I1CCSQ=[" + HostContext.I1CCSQ + "]")

        HostContext.I1CTFG = '0'                               #钞汇标志

    #关彬捷  20081215  新增校验磁道信息
    if (hostType == '0652'):

        AfaLoggerFunc.tradeInfo('>>>验证磁道信息')

        HostContext.I1TRCD = TradeContext.HostCode             #主机码

        HostContext.I1SBNO = TradeContext.BESBNO                  #网点号

        HostContext.I1USID = TradeContext.BETELR              #柜员号

        if TradeContext.existVariable ( 'BEAUUS') and TradeContext.BEAUUS != '' and TradeContext.existVariable('BEAUPS') and TradeContext.BEAUPS != '':
            HostContext.I1AUUS = TradeContext.BEAUUS        #授权柜员
            HostContext.I1AUPS = TradeContext.BEAUPS           #授权密码
        else:
            HostContext.I1AUUS = ''
            HostContext.I1AUPS = ''

        if TradeContext.existVariable('TERMID') and TradeContext.TERMID != '':
            HostContext.I1WSNO = TradeContext.TERMID                #终端号
        else:
            HostContext.I1WSNO = '1234567890'                #终端号

        if TradeContext.existVariable('WARNTNO') and TradeContext.WARNTNO != '':     #凭证种类
            HostContext.I1CARD = TradeContext.WARNTNO
        else:
            HostContext.I1CARD = ''                                #凭证种类
        
        if TradeContext.existVariable('SCTRKINF') and TradeContext.SCTRKINF != '':   #二磁道信息
            HostContext.I1AMTT = TradeContext.SCTRKINF
        else:
            HostContext.I1AMTT = TradeContext.SCTRKINF
        
        if TradeContext.existVariable('THTRKINF') and TradeContext.THTRKINF != '':   #三磁道信息
            HostContext.I1AMST = TradeContext.THTRKINF
        else:
            HostContext.I1AMST = TradeContext.THTRKINF

    if (hostType =='8813'): # 正交易

        AfaLoggerFunc.tradeInfo('>>>正交易')

        HostContext.I1TRCD = '8813'

        HostContext.I1SBNO = TradeContext.BESBNO

        HostContext.I1USID = TradeContext.BETELR

        if TradeContext.existVariable ( 'BEAUUS') and TradeContext.BEAUUS != '' and TradeContext.existVariable('BEAUPS') and TradeContext.BEAUPS != '':
            HostContext.I1AUUS = TradeContext.BEAUUS  #授权柜员
            HostContext.I1AUPS = TradeContext.BEAUPS  #授权密码
        else:
            HostContext.I1AUUS = ''
            HostContext.I1AUPS = ''

        if TradeContext.existVariable('TERMID') and TradeContext.TERMID != '':
            HostContext.I1WSNO = TradeContext.TERMID    #终端号
        else:
            HostContext.I1WSNO = '1234567890'
        
        #=====刘雨龙 20080804 新增重复次数====
        if TradeContext.existVariable('ACUR') and TradeContext.ACUR != '':
            HostContext.I1ACUR  = TradeContext.ACUR
        else:
            HostContext.I1ACUR  =  '1'
            
        HostContext.I2NBBH = []                             #代理业务号
        HostContext.I2NBBH.append('RCC')

        #关彬捷 20081230 增加CLDT,UNSQ存放原前置日期和前置流水号
        HostContext.I2CLDT = []                             #批量委托日期
        if TradeContext.existVariable('CLDT') and TradeContext.CLDT != '':
            HostContext.I2CLDT.append(TradeContext.CLDT)
        else:
            HostContext.I2CLDT.append('')

        HostContext.I2UNSQ = []                             #批量委托号
        if TradeContext.existVariable('UNSQ') and TradeContext.UNSQ != '':
            HostContext.I2UNSQ.append(TradeContext.UNSQ)
        else:
            HostContext.I2UNSQ.append('')

        HostContext.I2FEDT = []                             #前置日期
        if TradeContext.existVariable('FEDT') and TradeContext.FEDT != '':
            HostContext.I2FEDT.append(TradeContext.FEDT)
        else:
            HostContext.I2FEDT.append(TradeContext.BJEDTE)

        HostContext.I2RBSQ = []                             #前置流水号
        if TradeContext.existVariable('RBSQ') and TradeContext.RBSQ != '':
            HostContext.I2RBSQ.append(TradeContext.RBSQ)
        else:
            HostContext.I2RBSQ.append(TradeContext.BSPSQN)

        HostContext.I2DATE = []                             #外系统帐务日期
        HostContext.I2DATE.append(TradeContext.NCCworkDate)

        HostContext.I2RVFG = []                             #蓝红字标志
        if TradeContext.existVariable( 'RVFG' ) and TradeContext.RVFG != '':
            HostContext.I2RVFG.append(TradeContext.RVFG)
        else:
            HostContext.I2RVFG.append('')

        HostContext.I2SBNO = []                             #交易机构
        HostContext.I2SBNO.append(TradeContext.BESBNO)

        HostContext.I2TELR = []                             #交易柜员
        HostContext.I2TELR.append(TradeContext.BETELR)

        HostContext.I2TRSQ = []                             #组号
        HostContext.I2TRSQ.append('1')

        HostContext.I2TINO = []                             #组内序号
        HostContext.I2TINO.append('1')


        HostContext.I2CYNO = []                             #币种
        HostContext.I2CYNO.append('01')

        HostContext.I2WLBZ = []                             #往来帐标志
        HostContext.I2WLBZ.append(TradeContext.BRSFLG)

        HostContext.I2TRAM = []                             #发生额
        HostContext.I2TRAM.append(TradeContext.OCCAMT)

        HostContext.I2SMCD = []                             #摘要代码
        if TradeContext.existVariable ('RCCSMCD') and TradeContext.RCCSMCD != '':
            HostContext.I2SMCD.append(TradeContext.RCCSMCD)
        else:
            HostContext.I2SMCD.append('')

        HostContext.I2NMFG = []                             #户名校验标志
        if TradeContext.existVariable ('NMCKFG') and TradeContext.NMCKFG != '':
            HostContext.I2NMFG.append(TradeContext.NMCKFG)
        else:
            HostContext.I2NMFG.append('0')

        #=====新增销账序号  刘雨龙 20080609====
        HostContext.I2DASQ = []
        if TradeContext.existVariable( 'DASQ' ) and TradeContext.DASQ != '':
            HostContext.I2DASQ.append(TradeContext.DASQ)
        else:
            HostContext.I2DASQ.append('')

        HostContext.I2APX1 = []                             #附加信息1(单位编码)
        HostContext.I2APX1.append('')

        HostContext.I2RBAC = []        #贷方账号
        if TradeContext.existVariable( 'RBAC' ) and TradeContext.RBAC != '':
            HostContext.I2RBAC.append(TradeContext.RBAC)
        else:
            HostContext.I2RBAC.append('')

        HostContext.I2OTNM = []        #贷方户名
        if TradeContext.existVariable( 'OTNM' ) and TradeContext.OTNM != '':
            HostContext.I2OTNM.append(TradeContext.OTNM)
        else:
            HostContext.I2OTNM.append('')

        HostContext.I2SBAC = []        #借方账号
        if TradeContext.existVariable('SBAC') and TradeContext.SBAC != '':
            HostContext.I2SBAC.append(TradeContext.SBAC)
        else:
            HostContext.I2SBAC.append('')

        HostContext.I2ACNM = []        #借方户名
        if TradeContext.existVariable('ACNM') and TradeContext.ACNM != '':
            HostContext.I2ACNM.append(TradeContext.ACNM)
        else:
            HostContext.I2ACNM.append('')

        HostContext.I2REAC = []        #挂账账号
        if TradeContext.existVariable('REAC') and TradeContext.REAC != '':
            HostContext.I2REAC.append(TradeContext.REAC)
        else:
            HostContext.I2REAC.append('')

        if TradeContext.existVariable('PASSWD') and TradeContext.PASSWD != '':
            HostContext.I2CFFG = []
            HostContext.I2CFFG.append('Y')              #密码校验方式
            AfaLoggerFunc.tradeDebug('>>>密码校验方式:'+str(HostContext.I2CFFG))

            HostContext.I2PSWD = []
            HostContext.I2PSWD.append(TradeContext.PASSWD)
            AfaLoggerFunc.tradeDebug('>>>密码:'+str(TradeContext.PASSWD))
        else:
            HostContext.I2CFFG = []
            HostContext.I2CFFG.append('N')              #密码校验方式

            HostContext.I2PSWD = []
            HostContext.I2PSWD.append('')
            AfaLoggerFunc.tradeDebug('>>>密码['+str(HostContext.I2PSWD)+']')

        if TradeContext.existVariable('CERTTYPE') and TradeContext.CERTTYPE != '' and TradeContext.existVariable('CERTNO') and TradeContext.CERTNO != '':
            HostContext.I2OPTY = []                     #证件校验标志
            HostContext.I2OPTY.append('1')

            HostContext.I2IDTY = []                     #证件种类
            HostContext.I2IDTY.append(TradeContext.CERTTYPE)

            HostContext.I2IDNO = []                     #证件号码
            HostContext.I2IDNO.append(TradeContext.CERTNO)
        else:
            HostContext.I2OPTY = []                             #证件校验标志
            HostContext.I2OPTY.append('0')

            HostContext.I2IDTY = []                     #证件种类
            HostContext.I2IDTY.append('')

            HostContext.I2IDNO = []                     #证件号码
            HostContext.I2IDNO.append('')

        if TradeContext.existVariable('WARNTNO') and TradeContext.WARNTNO != '':     #凭证种类
            HostContext.I2CETY = []
            HostContext.I2CETY.append(TradeContext.WARNTNO[0:2])

            HostContext.I2CCSQ = []
            HostContext.I2CCSQ.append(TradeContext.WARNTNO[2:])

            #=====刘雨龙 20080805 上移====
            HostContext.I2TRFG = []#凭证处理标志
            HostContext.I2TRFG.append('9')

            if (TradeContext.existVariable('BBSSRC') and TradeContext.BBSSRC=='2' ):     #资金来源为 2-对公活期
                HostContext.I2CFFG = []
                HostContext.I2CFFG.append('N')          #密码校验方式：支票不校验密码

                HostContext.I2TRFG = []#凭证处理标志
                HostContext.I2TRFG.append('0')
        else:
            HostContext.I2CETY = []                     #凭证类型
            HostContext.I2CETY.append('')

            HostContext.I2CCSQ = []                     #凭证号码
            HostContext.I2CCSQ.append('')

            HostContext.I2TRFG = []                     #凭证处理标志
            HostContext.I2TRFG.append('9')

        HostContext.I2CATR = []
        if TradeContext.existVariable('CATR') and TradeContext.CATR != '':        #现转标志
            HostContext.I2CATR.append(TradeContext.CATR)
        else:
            HostContext.I2CATR.append('1')
        
        AfaLoggerFunc.tradeDebug('>>>现转标志['+str(HostContext.I2CATR)+']')
            
        HostContext.I2PKFG = []
        if TradeContext.existVariable('PKFG') and TradeContext.PKFG != '':    #通存通兑标识
            HostContext.I2PKFG.append(TradeContext.PKFG)
        else:
            HostContext.I2PKFG.append('')
        
        HostContext.I2CTFG = []
        if TradeContext.existVariable('CTFG') and TradeContext.CTFG != '':     #通存通兑本金标志
            HostContext.I2CTFG.append(TradeContext.CTFG)
        else:
            HostContext.I2CTFG.append('')

        #=====刘雨龙 20080804 新增汇票签发关于凭证的处理====
        if int(HostContext.I1ACUR) >=2:
            AfaLoggerFunc.tradeDebug('>>>开始添加第二条记录')
            if TradeContext.existVariable('PKFG') and TradeContext.PKFG != '':    #通存通兑标识
                HostContext.I2PKFG.append(TradeContext.PKFG)
            else:
                HostContext.I2PKFG.append('')
                
            #=====代理业务号 RCC-农信银====
            HostContext.I2NBBH.append('RCC')

            #关彬捷 20081230 增加CLDT,UNSQ存放原前置日期和前置流水号
            #=====批量委托日期=====
            if TradeContext.existVariable('CLDT') and TradeContext.CLDT != '':
                HostContext.I2CLDT.append(TradeContext.CLDT)
            else:
                HostContext.I2CLDT.append('')
            #=====批量委托号=====
            if TradeContext.existVariable('UNSQ') and TradeContext.UNSQ != '':
                HostContext.I2UNSQ.append(TradeContext.UNSQ)
            else:
                HostContext.I2UNSQ.append('')

            #=====前置日期====
            if TradeContext.existVariable('FEDT') and TradeContext.FEDT != '':
                HostContext.I2FEDT.append(TradeContext.FEDT)
            else:
                HostContext.I2FEDT.append(TradeContext.BJEDTE)
            #=====前置流水号====
            if TradeContext.existVariable('RBSQ') and TradeContext.RBSQ != '':
                HostContext.I2RBSQ.append(TradeContext.RBSQ)
            else:
                HostContext.I2RBSQ.append(TradeContext.BSPSQN)
            #HostContext.I2RBSQ.append(TradeContext.BSPSQN)
            HostContext.I2DATE.append(TradeContext.NCCworkDate)
            #=====红蓝字标志====
            if TradeContext.existVariable('I2RVFG') and TradeContext.I2RVFG != '':
                HostContext.I2RVFG.append(TradeContext.I2RVFG)
            else:
                HostContext.I2RVFG.append('')
            #=====交易机构====
            HostContext.I2SBNO.append(TradeContext.BESBNO)
            #=====交易柜员====
            HostContext.I2TELR.append(TradeContext.BETELR)
            #=====组号====
            HostContext.I2TRSQ.append('1')
            #=====组内序号====
            HostContext.I2TINO.append('2')
            #=====币种====
            HostContext.I2CYNO.append('01')
            #=====往来账标志====
            HostContext.I2WLBZ.append(TradeContext.BRSFLG)
            #=====销账序号====
            HostContext.I2DASQ.append('')
            #=====附加信息1====
            HostContext.I2APX1.append('')
            #=====户名校验标志====
            if TradeContext.existVariable('I2NMFG') and TradeContext.I2NMFG != '':
                HostContext.I2NMFG.append(TradeContext.I2NMFG)
            else:
                HostContext.I2NMFG.append('0')
            #=====贷方账号====
            if TradeContext.existVariable('I2RBAC') and TradeContext.I2RBAC != '':
                HostContext.I2RBAC.append(TradeContext.I2RBAC)
            else:
                HostContext.I2RBAC.append('')
            #=====贷方户名====
            if TradeContext.existVariable('I2OTNM') and TradeContext.I2OTNM != '':
                HostContext.I2OTNM.append(TradeContext.I2OTNM)
            else:
                HostContext.I2OTNM.append('')
            #=====借方账号====
            if TradeContext.existVariable('I2SBAC') and TradeContext.I2SBAC != '':
                HostContext.I2SBAC.append(TradeContext.I2SBAC)
            else:
                HostContext.I2SBAC.append('')
            #=====借方户名====
            if TradeContext.existVariable('I2ACNM') and TradeContext.I2ACNM != '':
                HostContext.I2ACNM.append(TradeContext.I2ACNM)
            else:
                HostContext.I2ACNM.append('')
            #=====挂账账号====
            if TradeContext.existVariable('I2REAC') and TradeContext.I2REAC != '':
                HostContext.I2REAC.append(TradeContext.I2REAC)
            else:
                HostContext.I2REAC.append('')
            if TradeContext.existVariable('I2PSWD') and TradeContext.I2PSWD != '':
                #=====密码校验方式====
                HostContext.I2CFFG.append('Y')              #密码校验方式
                #=====密码====
                HostContext.I2PSWD.append(TradeContext.I2PSWD)
            else:
                #=====密码校验方式====
                HostContext.I2CFFG.append('N')              #密码校验方式
                #=====密码====
                HostContext.I2PSWD.append('')
            
            #关彬捷  20081117 修改第二笔分录证件校验相关处理
            #=====证件校验标志====
            #HostContext.I2OPTY.append('')
            #=====证件种类====
            #HostContext.I2IDTY.append('')
            #HostContext.I2IDTY.append('')
            #=====证件号码====
            #HostContext.I2IDNO.append('')
            
            if TradeContext.existVariable('I2IDTY') and TradeContext.I2IDTY != '' and TradeContext.existVariable('I2IDNO') and TradeContext.I2IDNO != '':
                HostContext.I2OPTY.append('1')
            
                HostContext.I2IDTY.append(TradeContext.I2IDTY)
            
                HostContext.I2IDNO.append(TradeContext.I2IDNO)
            else:
                HostContext.I2OPTY.append('0')
            
                HostContext.I2IDTY.append('')
            
                HostContext.I2IDNO.append('')
            
            #=====现转标志====
            if TradeContext.existVariable('I2CATR') and TradeContext.I2CATR != '':
                HostContext.I2CATR.append(TradeContext.I2CATR)
            else:
                HostContext.I2CATR.append('1')
                
            
            if TradeContext.existVariable('I2CTFG') and TradeContext.I2CTFG != '':     #通存通兑本金标志
                HostContext.I2CTFG.append(TradeContext.I2CTFG)
            else:
                HostContext.I2CTFG.append('')
                
            if TradeContext.existVariable('PKFG') and TradeContext.PKFG in ('T','E','W'): #通存通兑标识:T-通存通兑,W-手工结转,E-错账补记
                #通存通兑第二笔分录特殊处理   关彬捷
                if TradeContext.existVariable('I2WARNTNO') and TradeContext.I2WARNTNO != '':
                    #=====凭证处理标志====
                    HostContext.I2TRFG.append('9')
                    #=====凭证种类====
                    HostContext.I2CETY.append(TradeContext.I2WARNTNO[0:2])
                    #=====凭证号码====
                    HostContext.I2CCSQ.append(TradeContext.I2WARNTNO[2:])
                else:
                    HostContext.I2TRFG.append('9')
                    HostContext.I2CETY.append('')
                    HostContext.I2CCSQ.append('')
                    
                #=====发生额====
                HostContext.I2TRAM.append(TradeContext.I2TRAM)
                #=====摘要代码====
                if TradeContext.existVariable('I2SMCD') and TradeContext.I2SMCD != '':
                    HostContext.I2SMCD.append(TradeContext.I2SMCD)
                else:
                    HostContext.I2SMCD.append('')

            elif TradeContext.existVariable('TRCTYP') and TradeContext.TRCTYP == '20': #汇兑标识
                #关彬捷 20091123 汇兑第二笔分录特殊处理
                if TradeContext.existVariable('I2WARNTNO') and TradeContext.I2WARNTNO != '':
                    #=====凭证处理标志====
                    HostContext.I2TRFG.append('9')
                    #=====凭证种类====
                    HostContext.I2CETY.append(TradeContext.I2WARNTNO[0:2])
                    #=====凭证号码====
                    HostContext.I2CCSQ.append(TradeContext.I2WARNTNO[2:])
                else:
                    HostContext.I2TRFG.append('9')
                    HostContext.I2CETY.append('')
                    HostContext.I2CCSQ.append('')
                    
                #=====发生额====
                HostContext.I2TRAM.append(TradeContext.I2TRAM)
                #=====摘要代码====
                if TradeContext.existVariable('I2SMCD') and TradeContext.I2SMCD != '':
                    HostContext.I2SMCD.append(TradeContext.I2SMCD)
                else:
                    HostContext.I2SMCD.append('')

            else:
                #汇票第二笔分录特殊处理
                #=====凭证处理标志====
                if TradeContext.existVariable('TRFG') and TradeContext.TRFG != '':
                    HostContext.I2TRFG.append(TradeContext.TRFG)
                else:
                    HostContext.I2TRFG.append('9')
                #=====凭证种类====
                #=====汇票解付来账时种类为空====
                if TradeContext.existVariable('I2CETY'):
                    HostContext.I2CETY.append(TradeContext.I2CETY)
                else:
                    HostContext.I2CETY.append('68')
                #=====凭证号码====
                #=====汇票解付来账时号码为空====
                #=====begin 蔡永贵 20110215 修改=====
                #if TradeContext.existVariable('BILNO'):                
                #    HostContext.I2CCSQ.append(TradeContext.BILNO)
                #else:
                #    HostContext.I2CCSQ.append('')
                if TradeContext.existVariable('BILNO'):                
                    if len(TradeContext.BILNO) == 16:
                        HostContext.I2CCSQ.append(TradeContext.BILNO[-8:])
                        HostContext.I2AMTT = []
                        HostContext.I2AMTT.append('')
                        HostContext.I2AMTT.append(TradeContext.BILNO)
                    else:
                        HostContext.I2CCSQ.append(TradeContext.BILNO)
                else:
                    HostContext.I2CCSQ.append('')
                #===========end============
                
                #=====发生额====
                if TradeContext.existVariable('I2TRAM') and TradeContext.I2TRAM != '':
                    HostContext.I2TRAM.append(TradeContext.I2TRAM)
                else:
                    HostContext.I2TRAM.append('1.00')
                
                #=====摘要代码====
                if TradeContext.existVariable('I2SMCD') and TradeContext.I2SMCD != '':
                    HostContext.I2SMCD.append(TradeContext.I2SMCD)
                else:
                    HostContext.I2SMCD.append('610')
                
        #=====刘雨龙 20081105 新增通存通兑记账的处理====
        if int(HostContext.I1ACUR) >= 3:
            AfaLoggerFunc.tradeDebug('>>>开始添加第三条记录')
            if TradeContext.existVariable('PKFG') and TradeContext.PKFG != '':    #通存通兑标识
                HostContext.I2PKFG.append(TradeContext.PKFG)
            else:
                HostContext.I2PKFG.append('')
            if TradeContext.existVariable('I3WARNTNO') and TradeContext.I3WARNTNO != '':
                #=====凭证处理标志====
                HostContext.I2TRFG.append('9')
                #=====凭证种类====
                HostContext.I2CETY.append(TradeContext.I2WARNTNO)
                #=====凭证号码====
                HostContext.I2CCSQ.append(TradeContext.I2WARNTNO)
            else:
                HostContext.I2TRFG.append('9')
                HostContext.I2CETY.append('')
                HostContext.I2CCSQ.append('')

            #=====发生额====
            HostContext.I2TRAM.append(TradeContext.I3TRAM)
            #=====代理业务号 RCC-农信银====
            HostContext.I2NBBH.append('RCC')

            #关彬捷  增加CLDT,UNSQ存放原前置日期前置流水号
            #=====批量委托日期=====
            if TradeContext.existVariable('CLDT') and TradeContext.CLDT != '':
                HostContext.I2CLDT.append(TradeContext.CLDT)
            else:
                HostContext.I2CLDT.append('')
            #=====批量委托流水号=====
            if TradeContext.existVariable('UNSQ') and TradeContext.UNSQ != '':
                HostContext.I2UNSQ.append(TradeContext.UNSQ)
            else:
                HostContext.I2UNSQ.append('')

            #=====前置日期====
            if TradeContext.existVariable('FEDT') and TradeContext.FEDT != '':
                HostContext.I2FEDT.append(TradeContext.FEDT)
            else:
                HostContext.I2FEDT.append(TradeContext.BJEDTE)
            #=====前置流水号====
            if TradeContext.existVariable('RBSQ') and TradeContext.RBSQ != '':
                HostContext.I2RBSQ.append(TradeContext.RBSQ)
            else:
                HostContext.I2RBSQ.append(TradeContext.BSPSQN)
            #HostContext.I2RBSQ.append(TradeContext.BSPSQN)
            HostContext.I2DATE.append(TradeContext.NCCworkDate)
            #=====红蓝字标志====
            if TradeContext.existVariable('I3RVFG') and TradeContext.I3RVFG != '':
                HostContext.I2RVFG.append(TradeContext.I3RVFG)
            else:
                HostContext.I2RVFG.append('')
            #=====交易机构====
            HostContext.I2SBNO.append(TradeContext.BESBNO)
            #=====交易柜员====
            HostContext.I2TELR.append(TradeContext.BETELR)
            #=====组号====
            HostContext.I2TRSQ.append('1')
            #=====组内序号====
            HostContext.I2TINO.append('3')
            #=====币种====
            HostContext.I2CYNO.append('01')
            #=====往来账标志====
            HostContext.I2WLBZ.append(TradeContext.BRSFLG)
            #=====摘要代码====
            if TradeContext.existVariable('I3SMCD') and TradeContext.I3SMCD != '':
                HostContext.I2SMCD.append(TradeContext.I3SMCD)
            else:
                HostContext.I2SMCD.append('')
            #=====户名校验标志====
            HostContext.I2NMFG.append('0')
            #=====销账序号====
            HostContext.I2DASQ.append('')
            #=====附加信息1====
            HostContext.I2APX1.append('')
            #=====贷方账号====
            if TradeContext.existVariable('I3RBAC') and TradeContext.I3RBAC != '':
                HostContext.I2RBAC.append(TradeContext.I3RBAC)
            else:
                HostContext.I2RBAC.append('')
            #=====贷方户名====
            if TradeContext.existVariable('I3OTNM') and TradeContext.I3OTNM != '':
                HostContext.I2OTNM.append(TradeContext.I3OTNM)
            else:
                HostContext.I2OTNM.append('')
            #=====借方账号====
            if TradeContext.existVariable('I3SBAC') and TradeContext.I3SBAC != '':
                HostContext.I2SBAC.append(TradeContext.I3SBAC)
            else:
                HostContext.I2SBAC.append('')
            #=====借方户名====
            if TradeContext.existVariable('I3ACNM') and TradeContext.I3ACNM != '':
                HostContext.I2ACNM.append(TradeContext.I3ACNM)
            else:
                HostContext.I2ACNM.append('')
            #=====挂账账号====
            if TradeContext.existVariable('I3REAC') and TradeContext.I3REAC != '':
                HostContext.I2REAC.append(TradeContext.I3REAC)
            else:
                HostContext.I2REAC.append('')
            #=====密码校验方式====
            if TradeContext.existVariable('I3PSWD') and TradeContext.I3PSWD != '':
                HostContext.I2CFFG.append('Y')   #密码校验方式
                #=====密码====
                HostContext.I2PSWD.append(TradeContext.I3PSWD)
            else:
                HostContext.I2CFFG.append('N')
                #=====密码====
                HostContext.I2PSWD.append('')
            
            #关彬捷  20081117  修改第三笔分录证件校验相关处理
            #=====证件校验标志====
            #HostContext.I2OPTY.append('')
            #=====证件种类====
            #HostContext.I2IDTY.append('')
            #HostContext.I2IDTY.append('')
            #=====证件号码====
            #HostContext.I2IDNO.append('')

            if TradeContext.existVariable('I3IDTY') and TradeContext.I3IDTY != '' and TradeContext.existVariable('I3IDNO') and TradeContext.I3IDNO != '':
                HostContext.I2OPTY.append('1')

                HostContext.I2IDTY.append(TradeContext.I3IDTY)

                HostContext.I2IDNO.append(TradeContext.I3IDNO)
            else:
                HostContext.I2OPTY.append('0')

                HostContext.I2IDTY.append('')

                HostContext.I2IDNO.append('')

            #=====现转标志====
            if TradeContext.existVariable('I3CATR') and TradeContext.I3CATR != '':
                HostContext.I2CATR.append(TradeContext.I3CATR)
            else:
                HostContext.I2CATR.append('1')
            
            if TradeContext.existVariable('I3CTFG') and TradeContext.I3CTFG != '':     #通存通兑本金标志
                HostContext.I2CTFG.append(TradeContext.I3CTFG)
            else:
                HostContext.I2CTFG.append('')

    elif (hostType =='8820'):   #反交易

        AfaLoggerFunc.tradeInfo('>>>反交易')

        HostContext.I1TRCD = '8820'

        HostContext.I1SBNO = TradeContext.BESBNO

        HostContext.I1USID = TradeContext.BETELR

        if TradeContext.existVariable ( 'BEAUUS') and TradeContext.BEAUUS != '' and TradeContext.existVariable('BEAUPS') and TradeContext.BEAUPS != '':
            HostContext.I1AUUS = TradeContext.BEAUUS
            HostContext.I1AUPS = TradeContext.BEAUPS
        else:
            HostContext.I1AUUS = ''
            HostContext.I1AUPS = ''

        if TradeContext.existVariable ( 'TERMID' ) and TradeContext.TERMID != '':
            HostContext.I1WSNO = TradeContext.TERMID
        else:
            HostContext.I1WSNO = ''

        HostContext.I1NBBH = 'RCC'
        HostContext.I1FEDT = TradeContext.BOJEDT
        HostContext.I1DATE = TradeContext.BOJEDT
        HostContext.I1RBSQ = TradeContext.BOSPSQ
        HostContext.I1TRDT = TradeContext.BOJEDT
        HostContext.I1UNSQ = TradeContext.BOSPSQ
        HostContext.I1OPTY = ''
        HostContext.I1OPFG = '0'       #(0.当日,1.隔日)
        HostContext.I1RVSB = '0'       #(0不回补-NO, 1	回补-YES)

    AfaLoggerFunc.tradeInfo('初始化map文件信息[InitHostReq]完成')

    return True

#====================初始化管理类主机接口===========================
def InitGLHostReq( ):

    #公共部分
    HostContext.I1TRCD = TradeContext.HostCode              #主机码

    HostContext.I1SBNO = TradeContext.BESBNO                  #网点号

    HostContext.I1USID = TradeContext.BETELR              #柜员号

    if TradeContext.existVariable ( 'BEAUUS') and TradeContext.BEAUUS != '' and TradeContext.existVariable('BEAUPS') and TradeContext.BEAUPS != '':
        HostContext.I1AUUS = TradeContext.BEAUUS        #授权柜员
        HostContext.I1AUPS = TradeContext.BEAUPS           #授权密码
    else:
        HostContext.I1AUUS = ''
        HostContext.I1AUPS = ''

    if TradeContext.existVariable('TERMID') and TradeContext.TERMID != '':
        HostContext.I1WSNO = TradeContext.TERMID                #终端号
    else:
        HostContext.I1WSNO = '1234567890'                #终端号

    #私有部分
    #关彬捷 20081105 移动8810输入接口初始化程序至InitHostReq函数中
    #if (TradeContext.HostCode == '8810'):
    #    #查询帐户信息
    #    HostContext.I1ACNO = TradeContext.ACCNO                 #帐号
    #    HostContext.I1CYNO = '01'    		                #币种
    #    HostContext.I1CFFG = '1'         	                #密码校验标志
    #    HostContext.I1PSWD = ''          	                #密码
    #    HostContext.I1CETY = ''          	                #凭证种类
    #    HostContext.I1CCSQ = ''                             #凭证号码
    #    HostContext.I1CTFG = '0'	                        #钞汇标志
    #    return True

    if (TradeContext.HostCode == '8811'):
        #查询凭证信息
        AfaLoggerFunc.tradeDebug('>>>开始查询凭证信息')
        HostContext.I1ACCN = TradeContext.ACCNO                 #帐号
        HostContext.I1CETY = TradeContext.WARNTNO[0:2]         #凭证种类
        HostContext.I1CCSQ = TradeContext.WARNTNO[2:]       #凭证号码
        return True




    if (TradeContext.HostCode == '8812'):
        #外联关联帐户登记交易
        HostContext.I1TRFG = ''	    	                    #处理标志(0-登记 1-取消)
        HostContext.I1ACCN = ''	    	                    #帐号
        HostContext.I1PRCD = ''                             #代理标志
        return True


    if (TradeContext.HostCode == '8814'):
        #批量申请
        HostContext.I1CLDT = ''	    	                    #批量委托日期
        HostContext.I1UNSQ = ''	    	                    #批量委托号
        HostContext.I1NBBH = ''	    	                    #代理业务号
        HostContext.I1OPFG = '2'	                        #事务标志
        HostContext.I1TRFG = '1'	                        #处理标志
        HostContext.I1RPTF = '0'	                        #重复标志
        HostContext.I1STDT = ''	                            #批量起始日期
        HostContext.I1ENDT = ''	                            #批量截止日期
        HostContext.I1COUT = ''	                            #委托总笔数
        HostContext.I1TOAM = ''	                            #委托总金额
        HostContext.I1FINA = ''	                            #上送文件名称
        return True


    if (TradeContext.HostCode == '8815'):
        #批量查询
        HostContext.I1NBBH = 'RCC'                        #代理业务号
        HostContext.I1CLDT = ''	                            #批量委托日期
        HostContext.I1UNSQ = ''	                            #批量委托号
        HostContext.I1FINA = ''	                            #下传文件名
        HostContext.I1DWFG = '2'	                        #下传标志
        return True

    #=====刘雨龙 20081129 新增8816查询主机账务====
    if (TradeContext.HostCode == '8816'):
        #主机账务查询
        if TradeContext.existVariable('OPFG') and TradeContext.OPFG != '':
            HostContext.I1OPFG = TradeContext.OPFG
        else:
            HostContext.I1OPFG = '1'                       #查询类型
        
        if TradeContext.existVariable('NBBH') and TradeContext.NBBH != '':
            HostContext.I1NBBH = TradeContext.NBBH
        else:
            HostContext.I1NBBH = 'RCC'                      #代理业务号
        HostContext.I1FEDT = TradeContext.FEDT              #原前置日期
        HostContext.I1RBSQ = TradeContext.RBSQ              #原前置流水
        
        if TradeContext.existVariable('DATE') and TradeContext.DATE != '':
            HostContext.I1DATE = TradeContext.DATE
        else:
            HostContext.I1DATE = ''                         #原主机日期
            
        if TradeContext.existVariable('I1TLSQ'):
            HostContext.I1TLSQ = TradeContext.I1TLSQ
        else:
            HostContext.I1TLSQ = ''                         #原主机日期
        
        if TradeContext.existVariable('I1TRDT'):
            HostContext.I1TRDT = TradeContext.I1TRDT
        else:
            HostContext.I1TRDT = ''                         #原创建日期
        
        if TradeContext.existVariable('I1RGSQ'):
            HostContext.I1RGSQ = TradeContext.I1RGSQ
        else:
            HostContext.I1RGSQ = ''                         #创建流水
        
        if TradeContext.existVariable('DAFG'):
            HostContext.I1DAFG = TradeContext.DAFG
        else:
            HostContext.I1DAFG = '1'                        #抹/记账标志
        
        return True

    if (TradeContext.HostCode == '8818'):
        #对帐明细申请
        HostContext.I1CLDT = ''	                            #批量委托日期
        HostContext.I1UNSQ = ''	                            #批量委托号
        HostContext.I1NBBH = ''	                            #代理业务号
        HostContext.I1DATE = ''	                            #外系统日期
        HostContext.I1FINA = ''	                            #下传文件名称
        return True


    if (TradeContext.HostCode == '8819'):
        #检查文件是否生成
        HostContext.I1NBBH = ''	    	                    #代理业务号
        HostContext.I1CLDT = ''	   	 	                    #原批量日期
        HostContext.I1UNSQ = ''	    	                    #原批量委托号
        HostContext.I1FILE = ''	    	                    #删除文件名
        HostContext.I1OPFG = ''	    	                    #操作标志(0-查询 1-删除上传文件 2-删除下传文件)
        return True


    if (TradeContext.HostCode == '8847'):
        #检查文件是否生成
        HostContext.I1ACCN = ''	            #对公活期帐号
        HostContext.I1STDT = ''	            #起始日期
        HostContext.I1EDDT = ''	            #终止日期
        HostContext.I1FINA = ''	            #文件名称
        return True

    #=====刘雨龙 20081205 新增下载主机对账文件====
    if (TradeContext.HostCode == '8825'):
        if TradeContext.existVariable('STRDAT'):
            HostContext.I1STDT = TradeContext.STRDAT
        else:
            HostContext.I1STDT = '' 

        if TradeContext.existVariable('ENDDAT'):
            HostContext.I1EDDT = TradeContext.ENDDAT
        else:
            HostContext.I1EDDT = '' 
        return True

    if (TradeContext.HostCode == '8826'):
        #对账请求
        if TradeContext.existVariable('NBBH'):
            HostContext.I1NBBH = TradeContext.NBBH  #代理标识
        else:
            HostContext.I1NBBH = ''	            #代理标识

        if TradeContext.existVariable('COUT'):
            HostContext.I1COUT = TradeContext.COUT  #总笔数
        else:
            HostContext.I1COUT = ''	            #总笔数

        if TradeContext.existVariable('TOAM'):
            HostContext.I1TOAM = TradeContext.TOAM  #总金额
        else:
            HostContext.I1TOAM = ''	            #总金额

        if TradeContext.existVariable('FINA'):
            HostContext.I1FINA = TradeContext.FINA  #上传文件名称
        else:
            HostContext.I1FINA = ''	            #上传文件名称

        return True
    
    #=====刘雨龙 20081128 新增关于手续费清单文件上传====
    if (TradeContext.HostCode == '8823'):
        #手续费请求
        if TradeContext.existVariable('CONT'):
            HostContext.I1COUT = TradeContext.CONT  #总笔数
        else:
            HostContext.I1COUT = ''	                #总金额

        if TradeContext.existVariable('OCCAMT'):
            HostContext.I1TOAM = TradeContext.OCCAMT  #总金额
        else:
            HostContext.I1TOAM = ''	                  #总金额

        if TradeContext.existVariable('fileName'):
            HostContext.I1FINA = TradeContext.fileName  #上传文件名称
        else:
            HostContext.I1FINA = ''	                    #上传文件名称

        return True
    
    #曾照泰 20110520 新增关于错帐控制和解控交易====
    if (TradeContext.HostCode == '0061'):
        #错帐控制解控标识位请求
        if TradeContext.existVariable('kjflag'):
            HostContext.I1CLFG = TradeContext.kjflag  #控制解控标识位
        else:
            HostContext.I1CLFG = ''	
        AfaLoggerFunc.tradeInfo(">>>>>>"+"test1")
        if TradeContext.existVariable('ACCNO'):               #被控制或解控的账号  
            AfaLoggerFunc.tradeInfo(">>>>>>"+"test2")
            AfaLoggerFunc.tradeInfo(">>>>>>"+"test((((("+TradeContext.ACCNO)
            AfaLoggerFunc.tradeInfo(len(TradeContext.ACCNO.strip()))
            AfaLoggerFunc.tradeInfo((TradeContext.ACCNO)[0:1])
            AfaLoggerFunc.tradeInfo(">>>>>>"+"test3")
            if (len(TradeContext.ACCNO.strip())==19 and ((TradeContext.ACCNO)[0:1]=='6')): #卡
                
                HostContext.I1CCTY ='1'                          #客户类别 对私
                HostContext.I1CARD = (TradeContext.ACCNO)[6:18]       #卡号
            else:
                AfaLoggerFunc.tradeInfo(">>>>>>"+"test4")
                HostContext.I1CARD = ''                          #卡号
            
            if (len(TradeContext.ACCNO.strip())==19 and (TradeContext.ACCNO)[0:1]!='6'):  #旧账号
                HostContext.I1CCTY ='1'                                                 #客户类别 对私 旧账号全是对私
                HostContext.I1OLAC =TradeContext.ACCNO                               #旧账号
            else:
                HostContext.I1OLAC =''      
           
            if (len(TradeContext.ACCNO.strip())==23 and (TradeContext.ACCNO)[0:1]=='1'): #对私账号
                HostContext.I1CCTY ='1'                                                #客户类别   1对私 2对公
                HostContext.I1SVAC = TradeContext.ACCNO                             #对私账号
            else:
                HostContext.I1SVAC = ''     
            
            if (len(TradeContext.ACCNO.strip())==23 and (TradeContext.ACCNO)[0:1]=='2'): #对公账号
                HostContext.I1CCTY ='2'                                                #客户类别   1对私 2对公
                HostContext.I1ACCN = TradeContext.ACCNO                             #客户账号
            else:
                HostContext.I1ACCN =''
        HostContext.I1CYNO = '01'                      #币种
        HostContext.I1SBSQ = ''                        #顺序号
         
        if TradeContext.existVariable('ERRCONBAL'):    #控制金额
            HostContext.I1NGAM = TradeContext.ERRCONBAL 
        else:
            HostContext.I1NGAM= '' 
        HostContext.I1YSQM = ''                        #预授权码
        
        return True    

#====================与主机数据交换=============================
def CommHost( result = '' ):

    AfaLoggerFunc.tradeInfo('>>>主机通讯函数[CommHost]')

    #根据正反交易标志TradeContext.BRSFLG判断具体选择哪个map文件和主机接口方式
    #===================初始化=======================
    if not InitHostReq(result) :
        TradeContext.__status__='1'
        return False
    if (result == '8813'):
        AfaLoggerFunc.tradeInfo('>>>单笔记帐')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8813.map'

    elif (result == '8820' ):
        AfaLoggerFunc.tradeInfo('>>>单笔抹帐')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8820.map'
        TradeContext.HostCode = '8820'

    elif (result == '8810'):
        AfaLoggerFunc.tradeInfo('>>>查询帐户信息')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8810.map'
        TradeContext.HostCode = '8810'

        #关彬捷 20081105 将8810主机输入接口初始化程序从InitGLHostReq函数移动至InitHostReq函数中
        #InitGLHostReq()

    elif (result == '8811'):
        AfaLoggerFunc.tradeInfo('>>>查询凭证信息')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8811.map'
        TradeContext.HostCode = '8811'
        InitGLHostReq()

    elif (result == '8812'):
        AfaLoggerFunc.tradeInfo('>>>外联关联帐户登记交易')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8812.map'
        TradeContext.HostCode = '8812'
        InitGLHostReq()

    elif (result == '8814'):
        AfaLoggerFunc.tradeInfo('>>>批量申请')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8814.map'
        TradeContext.HostCode = '8814'
        InitGLHostReq()

    elif (result == '8815'):
        AfaLoggerFunc.tradeInfo('>>>批量查询')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8815.map'
        TradeContext.HostCode = '8815'
        InitGLHostReq()
    
    #=====刘雨龙 20081129 新增查询主机账务信息====
    elif (result == '8816'):
        AfaLoggerFunc.tradeInfo('>>>查询主机账务信息')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8816.map'
        TradeContext.HostCode = '8816'
        InitGLHostReq()

    #=====刘雨龙 20081129 新增查询主机账务信息====
    elif (result == '8825'):
        AfaLoggerFunc.tradeInfo('>>>查询主机账务信息')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8825.map'
        TradeContext.HostCode = '8825'
        InitGLHostReq()

    elif (result == '8818'):
        AfaLoggerFunc.tradeInfo('>>>对帐明细申请')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8818.map'
        TradeContext.HostCode = '8818'
        InitGLHostReq()

    elif (result == '8819'):
        AfaLoggerFunc.tradeInfo('>>>检查文件是否生成')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8819.map'
        TradeContext.HostCode = '8819'
        InitGLHostReq()

    elif (result == '8847'):
        AfaLoggerFunc.tradeInfo('>>>对公帐号流水明细查询')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8847.map'
        TradeContext.HostCode = '8847'
        InitGLHostReq()

    elif (result == '8826'):
        AfaLoggerFunc.tradeInfo('>>>对账请求')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8826.map'
        TradeContext.HostCode = '8826'
        InitGLHostReq()
        
    #关彬捷 20081215  新增0652校验磁道信息接口
    elif (result == '0652' ):
        AfaLoggerFunc.tradeInfo('>>>校验磁道信息')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH0652.map'
        TradeContext.HostCode = '0652'
        
    #=====刘雨龙 20081128 新增8823关于农信银手续费接口====
    elif (result == '8823'):
        AfaLoggerFunc.tradeInfo('>>>手续费清单文件上传')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8823.map'
        TradeContext.HostCode = '8823'
        InitGLHostReq()
    
    #曾照泰20110520 新增0061 错帐控制解控交易
    elif (result == '0061'):
        AfaLoggerFunc.tradeInfo('>>>错帐控制解控')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH0061.map'
        TradeContext.HostCode = '0061'
        InitGLHostReq()
    else:
        TradeContext.errorCode = 'A9999'
        TradeContext.errorMsg  = '主机代码错误'
        return False
    
    #此处交易代码要求10位,右补空格
    HostComm.callHostTrade( mapfile, UtilTools.Rfill(TradeContext.HostCode,10,' ') ,'0002' )
    
    AfaLoggerFunc.tradeInfo( 'host_Error:'+str( HostContext.host_ErrorType )+':'+HostContext.host_ErrorMsg )
    if HostContext.host_Error:
        AfaLoggerFunc.tradeFatal( 'host_Error:'+str( HostContext.host_ErrorType )+':'+HostContext.host_ErrorMsg )
        AfaLoggerFunc.tradeInfo('5')

        if HostContext.host_ErrorType != 5 :
            TradeContext.__status__='1'
            TradeContext.errorCode='A0101'
            TradeContext.errorMsg=HostContext.host_ErrorMsg
        else :
            TradeContext.__status__='2'
            TradeContext.errorCode='A0102'
            TradeContext.errorMsg=HostContext.host_ErrorMsg
        return False

    #================分析主机返回包====================
    return HostParseRet(result )


#================分析主机返回包====================
def HostParseRet( hostType ):
    AfaLoggerFunc.tradeInfo(HostContext.O1MGID)
    if (HostContext.host_Error == True):    #主机通讯错误
        AfaLoggerFunc.tradeInfo('4')
        TradeContext.__status__='2'
        TradeContext.errorCode, TradeContext.errorMsg = 'A9998', '主机通讯错误'
        TradeContext.MGID  = HostContext.host_ErrorType    #通讯错误代码
        return False
    
    if( HostContext.O1MGID == 'AAAAAAA' ): #成功
        TradeContext.__status__='0'
        TradeContext.errorCode, TradeContext.errorMsg = '0000', '主机成功'
        TradeContext.MGID  = HostContext.O1MGID  #主机返回代码

        #=====根据交易码不同选择不同的信息返回====
        if TradeContext.HostCode == '8813':
            TradeContext.TRDT   = HostContext.O1TRDT  #主机日期
            TradeContext.TLSQ   = HostContext.O1TLSQ  #主机流水号
            TradeContext.DASQ   = str(HostContext.O2DASQ[0])   #代销帐序号
            AfaLoggerFunc.tradeInfo('销账序号[' + TradeContext.DASQ +']')
        elif TradeContext.HostCode == '8820':
            TradeContext.TRDT   = HostContext.O1TRDT  #主机日期
            TradeContext.TLSQ   = HostContext.O1TLSQ  #主机流水号
        elif TradeContext.HostCode == '8810':
            TradeContext.ACCNM  = UtilTools.trim(HostContext.O1CUNM)  #账号名称
            TradeContext.ACCSO  = HostContext.O1OPNT  #开户机构
            TradeContext.ACCST  = HostContext.O1ACST  #账户状态
            TradeContext.ACCCD  = HostContext.O1ITCD  #业务代号
            TradeContext.ACCEM  = HostContext.O1ITEM  #科目代号
            TradeContext.ACITY  = HostContext.O1IDTY  #证件类型
            TradeContext.ACINO  = HostContext.O1IDNO  #证件号码
        elif TradeContext.HostCode == '8811':
            TradeContext.HPAYTYP = HostContext.O1WDTP
            TradeContext.ACCSTCD = HostContext.O1STCD #凭证状态
            AfaLoggerFunc.tradeDebug('>>>查询凭证信息完成')
        #===========关彬捷 20080725 增加8820接口返回信息解析===================
        elif TradeContext.HostCode == '8820':
            TradeContext.TRDT   = HostContext.O1TRDT  #主机日期
            TradeContext.TLSQ   = HostContext.O1TLSQ  #主机流水号
        else:
            AfaLoggerFunc.tradeDebug('>>>主机记账完成')

        AfaLoggerFunc.tradeDebug('>>>主机成功返回')
        return True

    else:                                  #失败
        TradeContext.__status__='1'
        AfaLoggerFunc.tradeInfo('8')

        TradeContext.errorCode, TradeContext.errorMsg = HostContext.O1MGID, HostContext.O1INFO
        return False
##############################################################################################
#
#  程序名称： CrtAcc
#  入口参数： accno  lenacc
#  出口参数： accno  False
#  作    者： 刘雨龙
#  日    期： 20080610
#  程序功能： 计算账号校验位
#
##############################################################################################
def CrtAcc( no, lenacc ):
    AfaLoggerFunc.tradeInfo( '>>>开始计算账号校验位' )
    #=====判断传入的参数长度是否正确====
    if len(no) != 24:
        return AfaFlowControl.ExitThisFlow('M999','账号长度不正确')
    if int(lenacc) != 25:
        return AfaFlowControl.ExitThisFlow('M999','传入长度不正确')

    #====开始校验账号====
    total = 10
    for i in range(0, lenacc-1):
        if( not no[i].isdigit() ):
            return AfaFlowControl.ExitThisFlow('M999', '账号必须为数字')
        total = (total + int(no[i]) -0)%10
        if total == 0:
            total = 10
        else:
            total = total
        total =  (total + total)%11
    no = no + str((11 - total)%10)
    AfaLoggerFunc.tradeInfo( '账号：' + no )
    AfaLoggerFunc.tradeInfo( '>>>结束计算账号校验位' )
    return str(no)
