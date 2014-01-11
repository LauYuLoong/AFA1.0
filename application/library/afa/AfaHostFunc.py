# -*- coding: gbk -*-
##################################################################
#   代收代付平台.与主机通讯函数
#=================================================================
#   程序文件:   AfaHostFunc.py
#   修改时间:   2006-09-12
#
##################################################################
import TradeContext,AfaFunc,UtilTools,HostComm,HostContext,HostDataHandler,AfaLoggerFunc,os
from types import *

def InitHostReq(hostType ):
    #初始化函数返回值变量
    AfaLoggerFunc.tradeInfo('初始化map文件信息[InitHostReq]')

    if (hostType =='0'): # 正交易

        AfaLoggerFunc.tradeInfo('>>>正交易')

        HostContext.I1TRCD = '8813'
       
        HostContext.I1SBNO = TradeContext.brno
       
        HostContext.I1USID = TradeContext.tellerno
       
        if TradeContext.existVariable ( 'authTeller'):
            HostContext.I1AUUS = TradeContext.authTeller
            HostContext.I1AUPS = TradeContext.authPwd
        else:
            HostContext.I1AUUS = ''
            HostContext.I1AUPS = ''

        HostContext.I1WSNO = TradeContext.termId            #终端号

        HostContext.I2NBBH = []                             #代理业务号
        HostContext.I2NBBH.append(TradeContext.sysId)

        HostContext.I2FEDT = []                             #前置日期
        HostContext.I2FEDT.append(TradeContext.workDate)

        HostContext.I2RBSQ = []                             #前置流水号
        HostContext.I2RBSQ.append(TradeContext.agentSerialno)

        HostContext.I2DATE = []                             #外系统帐务日期
        HostContext.I2DATE.append(TradeContext.workDate)

        HostContext.I2RVFG = []                             #蓝红字标志
        HostContext.I2RVFG.append('0')

        HostContext.I2SBNO = []                             #交易机构
        HostContext.I2SBNO.append(TradeContext.brno)

        HostContext.I2TELR = []                             #交易柜员
        HostContext.I2TELR.append(TradeContext.tellerno)

        HostContext.I2TRSQ = []                             #组号
        HostContext.I2TRSQ.append('000')
        
        HostContext.I2TINO = []                             #组内序号
        HostContext.I2TINO.append('00')

        HostContext.I2OPTY = []                             #证件校验标志
        HostContext.I2OPTY.append('0')

        HostContext.I2CYNO = []                             #币种
        HostContext.I2CYNO.append('01')

        HostContext.I2WLBZ = []                             #往来帐标志
        HostContext.I2WLBZ.append('0')

        HostContext.I2TRAM = []                             #发生额
        HostContext.I2TRAM.append(TradeContext.amount.strip())

        HostContext.I2SMCD = []                             #摘要代码
        if TradeContext.existVariable ( '__summaryCode__'):
            HostContext.I2SMCD.append(TradeContext.__summaryCode__)
        else:
            HostContext.I2SMCD.append('')

        HostContext.I2NMFG = []                             #户名校验标志
        HostContext.I2NMFG.append('0')

        HostContext.I2PKFG = []                             #存折支票标志(0-不是 1-支票户 2-本票户 3-汇票户)
        HostContext.I2PKFG.append('0')

        HostContext.I2TRFG = []                             #凭证处理标志(0-销号 1-控制 2-解控 3-恢复凭证 4-记表外帐 9-不处理 汇票签发交易记表外凭证时填=4)
        HostContext.I2TRFG.append('9')

        HostContext.I2CETY = []                             #凭证种类         
        if TradeContext.existVariable('vouhType'):      
            HostContext.I2CETY.append(TradeContext.vouhType)
        else:
            HostContext.I2CETY.append('')

        HostContext.I2CCSQ = []                             #凭证号
        if TradeContext.existVariable('vouhNo'):      
            HostContext.I2CCSQ.append(TradeContext.vouhNo)
        else:
            HostContext.I2CCSQ.append('')

        HostContext.I2PS16 = []                             #支付密码
        HostContext.I2PS16.append('')
            
        if (TradeContext.existVariable('idType') and len(TradeContext.idType)!=0):
            HostContext.I2OPTY = []                         #证件校验标志
            HostContext.I2OPTY.append('1')

            HostContext.I2IDTY = []                         #证件种类
            HostContext.I2IDTY.append(TradeContext.idType)

            HostContext.I2IDNO = []                         #证件号码
            HostContext.I2IDNO.append(TradeContext.idno)
        else:
            HostContext.I2OPTY = []                         #证件校验标志
            HostContext.I2OPTY.append('0')

            HostContext.I2IDTY = []                         #证件种类
            HostContext.I2IDTY.append('')

            HostContext.I2IDNO = []                         #证件号码
            HostContext.I2IDNO.append('')
        
        HostContext.I2APX1 = []                             #附加信息1(单位编码)
        if TradeContext.existVariable ( 'subUnitno'):
            HostContext.I2APX1.append(TradeContext.unitno + TradeContext.subUnitno)
        else:
            HostContext.I2APX1.append(TradeContext.unitno)


        #判断现金转帐标志,以便填充不同的数据通讯区
        if (TradeContext.accType == '000'):

            AfaLoggerFunc.tradeInfo('>>>现金')

            HostContext.I2CFFG = []                         #密码校验标志
            HostContext.I2CFFG.append('N')

            HostContext.I2PSWD = []                         #密码
            HostContext.I2PSWD.append('')

            HostContext.I2CATR = []                         #现转标志
            HostContext.I2CATR.append('0')

            #业务方式(01-代收 02-代付 03-批扣 04-批付)
            if (TradeContext.agentFlag=='01' or TradeContext.agentFlag=='03' ):
                HostContext.I2RBAC = []                                             #贷方账号
                HostContext.I2RBAC.append(TradeContext.__agentAccno__)
            else:
                HostContext.I2SBAC = []
                HostContext.I2SBAC.append(TradeContext.__agentAccno__)              #借方账号

        else:
            AfaLoggerFunc.tradeInfo('>>>转帐')


            #业务方式(01-代收 02-代付 03-批扣 04-批付)
            if (TradeContext.agentFlag=='01' or TradeContext.agentFlag=='03' ):
                HostContext.I2RBAC = []                                             #贷方账号
                HostContext.I2RBAC.append(TradeContext.__agentAccno__)

                HostContext.I2SBAC = []                                             #借方账号
                HostContext.I2SBAC.append(TradeContext.accno)                       
            else:
                HostContext.I2RBAC = []                                             #贷方账号
                HostContext.I2RBAC.append(TradeContext.accno)

                HostContext.I2SBAC = []                                             #借方账号
                HostContext.I2SBAC.append(TradeContext.__agentAccno__)              


            if (TradeContext.existVariable('accPwd') and len(TradeContext.accPwd)!=0):
                HostContext.I2CFFG = []
                HostContext.I2CFFG.append('Y')              #密码校验方式

                HostContext.I2PSWD = []
                HostContext.I2PSWD.append(TradeContext.accPwd)
            else:
                HostContext.I2CFFG = []
                HostContext.I2CFFG.append('N')              #密码校验方式

            HostContext.I2CATR = []                         #现转标志
            HostContext.I2CATR.append('1')

    else:   #反交易

        AfaLoggerFunc.tradeInfo('>>>反交易')

        HostContext.I1TRCD = '8820'

        AfaLoggerFunc.tradeInfo(TradeContext.brno)

        HostContext.I1SBNO = TradeContext.brno

        AfaLoggerFunc.tradeInfo(TradeContext.tellerno)

        HostContext.I1USID = TradeContext.tellerno

        if TradeContext.existVariable ( 'authTeller'):
            HostContext.I1AUUS = TradeContext.authTeller
            HostContext.I1AUPS = TradeContext.authPwd
        else:
            HostContext.I1AUUS = ''
            HostContext.I1AUPS = ''

        AfaLoggerFunc.tradeInfo(TradeContext.termId)
        AfaLoggerFunc.tradeInfo(TradeContext.sysId)
        AfaLoggerFunc.tradeInfo(TradeContext.workDate)
        AfaLoggerFunc.tradeInfo(TradeContext.agentSerialno)
        AfaLoggerFunc.tradeInfo(TradeContext.preAgentSerno)

        HostContext.I1WSNO = TradeContext.termId
        HostContext.I1NBBH = TradeContext.sysId
        HostContext.I1FEDT = TradeContext.workDate
        HostContext.I1DATE = TradeContext.workDate
        HostContext.I1RBSQ = TradeContext.agentSerialno
        HostContext.I1TRDT = TradeContext.workDate
        HostContext.I1UNSQ = TradeContext.preAgentSerno
        HostContext.I1OPTY = ''
        HostContext.I1OPFG = '0'                                        #(0.当日,1.隔日)
        HostContext.I1RVSB = '0'                                        #(0不回补-NO, 1	回补-YES)

    AfaLoggerFunc.tradeInfo('初始化map文件信息[InitHostReq]完成')

    return True

#====================初始化管理类主机接口===========================
def InitGLHostReq( ):

    if (TradeContext.HostCode == '8808'):
        #查询主机日期
        return True
        
    if (TradeContext.HostCode == '8810'):
        #查询帐户信息
        return True


    if (TradeContext.HostCode == '8812'):
        #外联关联帐户登记交易
        return True                                         
                                                            
                                                            
    if (TradeContext.HostCode == '8814'):                   
        #批量申请                                           
        return True                                         
                                                            
                                                            
    if (TradeContext.HostCode == '8815'):                   
        #批量查询                                           
        return True                                         
                                                            
                                                            
    if (TradeContext.HostCode == '8818'):                   
        #对帐明细申请                                       
        return True                                         
                                                            
                                                            
    if (TradeContext.HostCode == '8819'):                   
        #检查文件是否生成                                   
        return True

        
    if (TradeContext.HostCode == '8847'):
        #检查文件是否生成
        return True
    
    

#====================与主机数据交换=============================
def CommHost( result = None ):

    AfaLoggerFunc.tradeInfo('>>>主机通讯函数[CommHost]')
        
    TradeContext.errorCode = 'H999'
    TradeContext.errorMsg  = '系统异常(与主机通讯)'

    #根据正反交易标志TradeContext.revTranF判断具体选择哪个map文件和主机接口方式
    if not result:
        result=TradeContext.revTranF
        #===================初始化=======================
        if not InitHostReq(result) :
            TradeContext.__status__='1'
            return False

    if (result == '0'):
        AfaLoggerFunc.tradeInfo('>>>单笔记帐')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8813.map'
        TradeContext.HostCode = '8813'

    elif (result == '1' or result == '2' ):
        AfaLoggerFunc.tradeInfo('>>>单笔抹帐')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8820.map'
        TradeContext.HostCode = '8820'

    elif (result == '8808'):
        AfaLoggerFunc.tradeInfo('>>>查询主机日期')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8808.map'
        TradeContext.HostCode = '8808'
        InitGLHostReq()
            
    elif (result == '8810'):
        AfaLoggerFunc.tradeInfo('>>>查询帐户信息')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8810.map'
        TradeContext.HostCode = '8810'
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

    else:
        TradeContext.errorCode = 'A9999'
        TradeContext.errorMsg  = '主机代码错误'
        return False

    #此处交易代码要求10位,右补空格
    HostComm.callHostTrade( mapfile, UtilTools.Rfill(TradeContext.HostCode,10,' ') ,'0002' )

    if HostContext.host_Error:
        AfaLoggerFunc.tradeFatal( 'host_Error:'+str( HostContext.host_ErrorType )+':'+HostContext.host_ErrorMsg )

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

    if (HostContext.host_Error == True):    #主机通讯错误
        TradeContext.__status__='2'
        TradeContext.errorCode, TradeContext.errorMsg = 'A9998', '主机通讯错误'
        TradeContext.bankCode  = HostContext.host_ErrorType                       #通讯错误代码
        return False

    if( HostContext.O1MGID == 'AAAAAAA' ): #成功
        TradeContext.__status__='0'
        TradeContext.errorCode, TradeContext.errorMsg = '0000', '主机成功'
        TradeContext.bankSerno = HostContext.O1TLSQ                               #柜员流水号
        TradeContext.bankCode  = HostContext.O1MGID                               #主机返回代码
        return True

    else:                                  #失败
        TradeContext.__status__='1'
        TradeContext.errorCode, TradeContext.errorMsg = HostContext.O1MGID, HostContext.O1INFO
        return False
