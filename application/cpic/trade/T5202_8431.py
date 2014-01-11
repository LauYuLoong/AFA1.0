# -*- coding: gbk -*-
##################################################################
#   中间业务平台.
#=================================================================
#   程序文件:   004202_8202.py
#   程序说明:   [8431--6000113]新保承保
#   修改时间:   2006-04-06
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,HostContext,AfaAhAdb
import AfaHostFunc
from types import *

def SubModuleDoFst( ):

    #begin  20091120  蔡永贵  增加
    #校验保险公司代码和凭证种类是否合法
    if not AfaAhAdb.ADBCheckCert( ):
        return False
    #end

    AfaLoggerFunc.tradeInfo( '初始化交易变量' )
    TradeContext.note1,TradeContext.note2,TradeContext.note4 = "","",""
    #交易代码
    TradeContext.tradeCode = TradeContext.TransCode
    # 贷款合同编号+贷款凭证编号
    if( TradeContext.existVariable( "CreBarNo" ) ):
        TradeContext.note4 = TradeContext.note4 + TradeContext.CreBarNo +"|"
    if ( TradeContext.existVariable( "CreVouNo" ) ):
        TradeContext.note4 = TradeContext.note4 + TradeContext.CreVouNo
    #借款日期+借款到期日
    if( TradeContext.existVariable( "LoanDate" ) ):
        TradeContext.note2 = TradeContext.note2 + TradeContext.LoanDate +"|"
    if ( TradeContext.existVariable( "LoanEndDate" ) ):
        TradeContext.note2 = TradeContext.note2 + TradeContext.LoanEndDate
    #单证号
    if( TradeContext.existVariable( "CpciPNo" ) ):
        TradeContext.note1 = TradeContext.note1 + TradeContext.CpciPNo
    #用户编号(投保单号)
    if( not TradeContext.existVariable( "CpicNo" ) and len(TradeContext.CpicNo.strip()) > 0 ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '用户编号投保单号[CpicNo]值不存在!' )
    else:
        TradeContext.userno = TradeContext.CpicNo
    #缴费金额
    if( not TradeContext.existVariable( "Amount" ) and len(TradeContext.Amount.strip()) > 0):
        return AfaFlowControl.ExitThisFlow( 'A0001', '缴费金额[Amount]值不存在!' )
    else:
        TradeContext.amount = TradeContext.Amount
    #用户姓名
    if( TradeContext.existVariable( "UserName" ) and len(TradeContext.UserName.strip()) > 0 ):
        TradeContext.userName = TradeContext.UserName
    #终端标识
    if( TradeContext.existVariable( "termid" ) and len(TradeContext.termid.strip()) > 0 ):
        TradeContext.termId = TradeContext.termid
    #保单单证号
    if( TradeContext.existVariable( "CpciPNo" ) and len(TradeContext.CpciPNo.strip()) > 0 ):
        TradeContext.CpciPNo = TradeContext.CpciPNo[2:15]
    #账户类型
    if TradeContext.AccType == "0":
        TradeContext.accType = "000"
    else:
        TradeContext.accno = TradeContext.AccNo
        if TradeContext.PyiTp == "0":
            TradeContext.accType = "003"
        else:
            TradeContext.accType = "001"
    #支付条件
    if TradeContext.TradeType == '0':                                    #凭密码
        TradeContext.accPwd = TradeContext.PassWd
        TradeContext.vouhType = TradeContext.iCreno[:2]
        TradeContext.vouhNo = TradeContext.iCreno[2:]
    elif TradeContext.TradeType == '1':                                  #凭证件
        TradeContext.idType = TradeContext.GovtIDTC
        TradeContext.idno = TradeContext.GovtID
        TradeContext.vouhType = TradeContext.iCreno[:2]
        TradeContext.vouhNo = TradeContext.iCreno[2:]
    elif TradeContext.TradeType == "2":                                  #凭单折
        TradeContext.vouhType = TradeContext.iCreno[:2]
        TradeContext.vouhNo = TradeContext.iCreno[2:]
    
    #关彬捷 20091124 根据单位编码获取保险公司信息
    AfaAhAdb.ADBGetInfoByUnitno()
    ##险种代码
    #if( TradeContext.existVariable( "ProCode" ) and len(TradeContext.ProCode.strip()) > 0 ):
    #    if ( TradeContext.ProCode == "1"):
    #        TradeContext.ProCodeStr = "EL5612"
    #        TradeContext.PlanName   = "安贷宝B"
    #    elif ( TradeContext.ProCode == "2"):
    #        TradeContext.ProCodeStr = "211610"
    #        TradeContext.PlanName   = "华夏借款人意外伤害保险"
    
    
    AfaLoggerFunc.tradeDebug("TradeContext.accType = [" + TradeContext.accType + "]")
    AfaLoggerFunc.tradeInfo( 'TradeContext.note1 = [' + str(TradeContext.note1) + ']')
    AfaLoggerFunc.tradeInfo( 'TradeContext.note2 = [' + str(TradeContext.note2) + ']')
    AfaLoggerFunc.tradeInfo( 'TradeContext.note4 = [' + str(TradeContext.note4) + ']')
    return True
def SubModuleDoSnd( ):
    return True
def SubModuleDoTrd( ):
    AfaLoggerFunc.tradeInfo('进入缴费交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']与第三方通讯后处理' )
#    try:
    #AfaLoggerFunc.tradeInfo('status='+TradeContext.__status__+'autoRevTranCtl='+TradeContext.__autoRevTranCtl__)
 
    Party3Context.agentSerialno = TradeContext.agentSerialno
    Party3Context.workDate      = TradeContext.workDate
    Party3Context.workTime      = TradeContext.workTime
    Party3Context.amount        = TradeContext.amount
    Party3Context.ProCode       = TradeContext.ProCode
    Party3Context.ProCodeStr    = TradeContext.ProCodeStr
    Party3Context.PlanName      = TradeContext.PlanName  

    if not Party3Context.existVariable('CpicTeller'):
        AfaLoggerFunc.tradeInfo( '>>>保险公司未返回业务员编号，系统自动冲正' )
        TradeContext.errorCode, TradeContext.errorMsg = 'A0100', '保险公司未返回业务员编号'
        return False
 
    names = Party3Context.getNames( )
    for name in names:
        value = getattr( Party3Context, name )
        if ( not name.startswith( '__' ) and type(value) is StringType) :
            setattr( TradeContext, name, value )
        #AfaLoggerFunc.tradeInfo("字段名称  ["+str(name)+"] =  "+str(value))
    if( TradeContext.errorCode == '0000' ):
        TradeContext.errorMsg = '交易成功'
        if ( TradeContext.existVariable( "EffDate" ) and len(str(TradeContext.EffDate)) == 14):
            TradeContext.EffDate = TradeContext.EffDate[0:4] + TradeContext.EffDate[6:8] + TradeContext.EffDate[10:12]
        if ( TradeContext.existVariable( "TermDate" ) and len(str(TradeContext.TermDate)) == 14):
            TradeContext.TermDate = TradeContext.TermDate[0:4] + TradeContext.TermDate[6:8] + TradeContext.TermDate[10:12]
        if not AfaAhAdb.ADBUpdateTransdtl( ):
            #raise AfaFlowControl.accException()
            return False
    else:
        AfaLoggerFunc.tradeInfo('与第三方交易失败')
        return False
 
    #AfaLoggerFunc.tradeInfo("贷款合同和凭证编号 "+TradeContext.CreBarNo+"$$$$$$$"+TradeContext.CreVouNo)
    #AfaLoggerFunc.tradeInfo("核心流水"+ str(TradeContext.bankSerno))
    #TradeContext.CreBarNo = TradeContext.CreBarNo
    #TradeContext.CreVouNo = TradeContext.CreVouNo
    #TradeContext.bankSerno = TradeContext.bankSerno
    AfaLoggerFunc.tradeInfo('退出缴费交易与第三方通讯后处理' )
    return True
#    except Exception, e:
#        AfaFlowControl.exitMainFlow(str(e))
    
