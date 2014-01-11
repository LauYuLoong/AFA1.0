# -*- coding: gbk -*-
##################################################################
#   中间业务平台.
#=================================================================
#   程序文件:   004202_8202.py
#   程序说明:   [8431--8000113]续期缴费
#   修改时间:   2010—08-14
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,HostContext,AfaYbtdb
import AfaHostFunc
from types import *

def SubModuleDoFst( ):

    AfaLoggerFunc.tradeInfo( '初始化续期缴费交易变量' )
    


    
    #交易代码
    TradeContext.tradeCode = TradeContext.TransCode
    
    #如果缴费金额是0.00，则不让缴费
    if not( TradeContext.existVariable( "amount" ) and len(TradeContext.amount.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "缴费金额不存在"
        raise AfaFlowControl.flowException( )
    else:
        AfaLoggerFunc.tradeInfo("缴费金额：" + TradeContext.amount )
        if TradeContext.amount.strip( ) == "0.00":
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "缴费金额不能为零"
            raise AfaFlowControl.flowException( )

    #保险公司代码
    if not( TradeContext.existVariable( "unitno" ) and len(TradeContext.unitno.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "不存在保险公司代码"
        raise AfaFlowControl.flowException( )
       
    #投保单号
    if not( TradeContext.existVariable( "policy" ) and len(TradeContext.policy.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "保险单号不存在"
        raise AfaFlowControl.flowException( )  
   
    #缴费方式
    if not( TradeContext.existVariable( "paymethod" ) and len(TradeContext.paymethod.strip()) > 0 ):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "缴费方式不存在"
        raise AfaFlowControl.flowException( )   
    
    #投保人姓名
    if not( TradeContext.existVariable( "tbr_name" ) and len(TradeContext.tbr_name.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "投保人姓名不存在"
        raise AfaFlowControl.flowException( )
    
    #缴费期次
    if not( TradeContext.existVariable( "rev_frequ" ) and len(TradeContext.rev_frequ.strip()) > 0):
        TradeContext.rev_frequ = ''
    
    #应收日期
    if not( TradeContext.existVariable( "rev_date" ) and len(TradeContext.rev_date.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "应收日期不存在"
        raise AfaFlowControl.flowException( )   
    
    #paymethod1付费方式(0现金，1转账)  accType缴费介质代码（000:现金，001：对私账号，002：借记卡，
    #003：贷记卡，004：对公账号，005：公务卡）  payacc账号  paycard卡号
    TradeContext.accType = ''
    
    if TradeContext.paymethod1=="0":
        TradeContext.accType="000"
    else:
        if TradeContext.vouchtype == "49":                                 #vouchtype 49:存储账户
            TradeContext.accType="001"
            TradeContext.accno = TradeContext.payacc                       #账号
        
        elif TradeContext.vouchtype == "81":                               #vouchtype 81:金农借记卡       
            TradeContext.accType="002"
            TradeContext.accno = TradeContext.paycard                      #卡号
        
        #paytype支付条件（0凭密码，1凭证件，2凭单折）vouchno凭证号码  tbr_idno投保人身份证号码
        if TradeContext.paytype == '0':                                    #凭密码
            TradeContext.accPwd = TradeContext.password 
            TradeContext.vouhType = TradeContext.vouchtype                 #凭证种类
            if(TradeContext.vouchtype == "81"):
                TradeContext.vouhNo=TradeContext.paycard[8:18] 
            else:
                TradeContext.vouhNo = TradeContext.vouchno                 #凭证号码
        
        elif TradeContext.paytype == '1':                                  #凭证件
            TradeContext.idType = TradeContext.zjtype                      #证件种类
            TradeContext.idno = TradeContext.zjno                          #证件号码
            TradeContext.vouhType = TradeContext.vouchtype                 #凭证种类 
            TradeContext.vouhNo = TradeContext.vouchno                     #凭证号码
        
        elif TradeContext.paytype == "2":                                  #凭单折
            TradeContext.vouhType = TradeContext.vouchtype                 #凭证种类 
            TradeContext.vouhNo = TradeContext.vouchno                     #凭证号码
   
    return True

def SubModuleDoSnd( ):
    return True

def SubModuleDoTrd( ):
    AfaLoggerFunc.tradeInfo('进入续期缴费交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']与第三方通讯后处理' )
    
    names = Party3Context.getNames( )
    
    for name in names:
        value = getattr( Party3Context, name )
        if ( not name.startswith( '__' ) and type(value) is StringType) :
            setattr( TradeContext, name, value )
    
    if( TradeContext.errorCode == '0000' ):
        TradeContext.errorMsg = '交易成功'
        
        if not AfaYbtdb.ADBUpdateTransdtl( ):                              #缴费成功后更新主流水表的note字段值   
           return False
    else:
        AfaLoggerFunc.tradeInfo('与第三方交易失败')
        return False

   
    AfaLoggerFunc.tradeInfo('退出续期缴费交易与第三方通讯后处理' )
    return True
        


