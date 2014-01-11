# -*- coding: gbk -*-
##################################################################
#   中间业务平台.
#=================================================================
#   程序文件:   TAHJF002_8627.py
#   程序说明:   安徽交罚交款交易
#   修改时间:   2011—01-20
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,HostContext
import AfaHostFunc
from types import *

def SubModuleDoFst( ):

    AfaLoggerFunc.tradeInfo( '初始化安徽交罚交易变量,保存在afa_maintransdel的note字段中' )
    #note1保存财政区划编码
    TradeContext.note1 = TradeContext.finiceCode
    #用户号保存处罚交款书编号
    TradeContext.userno = TradeContext.punishNo
    #note3保存缴款书号
    TradeContext.note3 = TradeContext.posNo
    #note4保存罚款金额
    TradeContext.note4 = TradeContext.punishAmt
    #note5保存滞纳金
    TradeContext.note5 = TradeContext.forfeit
    #note6保存付款人银行
    TradeContext.note6 = TradeContext.payBank
    #note7保存缴费日期
    TradeContext.note7 = TradeContext.paymDate
    #缴款人名称
    TradeContext.username = TradeContext.payName
    
    #曾照泰20110412修改，缴费金额不能为0.00
    #如果缴费金额是0.00，则不让缴费
    if not( TradeContext.existVariable( "amount" ) and len(TradeContext.amount.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E0001', "缴费金额不存在"
        raise AfaFlowControl.flowException( )
    else:
        AfaLoggerFunc.tradeInfo("缴费金额：" + TradeContext.amount )
        if TradeContext.amount.strip( ) == "0.00":
            TradeContext.errorCode,TradeContext.errorMsg = 'E0001', "缴费金额不能为零"
            raise AfaFlowControl.flowException( )
    
    #paymethod1付费方式(0现金，1转账)  accType缴费介质代码（000:现金，001：对私账号，002：借记卡，
    #003：贷记卡，004：对公账号，005：公务卡）  payacc账号  paycard卡号
    TradeContext.accType = ''
    
    if TradeContext.paymethod1=="0":
        TradeContext.accType="000"
        AfaLoggerFunc.tradeInfo('现金缴费')
    else:
        TradeContext.accno = TradeContext.payacc                           #账号
        AfaLoggerFunc.tradeInfo("缴费账号：" + TradeContext.payacc)
        if TradeContext.falg == "0":                                       #vouchtype 49：存储存折
            TradeContext.accType="001"
        elif TradeContext.falg == "1":                                     #vouchtype 81：金农借记卡
            TradeContext.accType="002"
     
        #paytype支付条件（0凭密码，1凭证件，2凭单折）vouchno凭证号码  tbr_idno身份证号码
        if TradeContext.paytype == '0':                                    
            TradeContext.accPwd = TradeContext.password                    #凭密码
            TradeContext.vouhType = TradeContext.vouchno[:2]               #凭证种类
            TradeContext.vouhNo = TradeContext.vouchno[2:]                 #凭证号码
        elif TradeContext.paytype == '1':                                  #凭证件
            TradeContext.idType = TradeContext.zjtype                      #证件种类
            TradeContext.idno = TradeContext.zjno                          #证件号码
            TradeContext.vouhType = TradeContext.vouchno[:2]               #凭证种类 
            TradeContext.vouhNo = TradeContext.vouchno[2:]                 #凭证号码
        elif TradeContext.paytype == "2":                                  #凭单折
            TradeContext.vouhType = TradeContext.vouchno[:2]               #凭证种类 
            TradeContext.vouhNo = TradeContext.vouchno[2:]                 #凭证号码
            
    return True

def SubModuleDoSnd( ):
    return True

def SubModuleDoTrd( ):
    
    AfaLoggerFunc.tradeInfo('进入缴费交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']与第三方通讯后处理' )
    
    names = Party3Context.getNames( )
   
    for name in names:
        value = getattr( Party3Context, name )
        if ( not name.startswith( '__' ) and type(value) is StringType or type(value) is ListType) :
            setattr( TradeContext,name, value )
    
    if( TradeContext.errorCode == '0000' ):
        TradeContext.errorMsg = '交易成功'
    else:
        AfaLoggerFunc.tradeInfo('与第三方交易失败')
        return False

    AfaLoggerFunc.tradeInfo('退出缴费交易与第三方通讯后处理' )
    
    return True


