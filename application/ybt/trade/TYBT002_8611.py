# -*- coding: gbk -*-
##################################################################
#   中间业务平台.
#=================================================================
#   程序文件:   TYBT002_8611.py
#   程序说明:   新保缴费
#   修改时间:   2010—07-29
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,HostContext,AfaYbtdb,YbtFunc
import AfaHostFunc
from types import *

def SubModuleDoFst( ):

    
    #校验保险公司代码和凭证种类是否合法
    if not AfaYbtdb.ADBCheckCert( ):
        return False
   
    
    try:
        AfaLoggerFunc.tradeInfo( '初始化新保缴费交易变量' )
        
        #交易代码（8611）
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
        if not( TradeContext.existVariable( "applno" ) and len(TradeContext.applno.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "投保单号不存在"
            raise AfaFlowControl.flowException( )   
        
        #保单印刷号
        if not( TradeContext.existVariable( "userno" ) and len(TradeContext.userno.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "保单印刷号不存在"
            raise AfaFlowControl.flowException( )  
        
        #新保投保（核保）流水号
        if not( TradeContext.existVariable( "PreSerialno"  ) and len(TradeContext.PreSerialno.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "新保投保（核保）流水号不存在"
            raise AfaFlowControl.flowException( )  
        
        #主险种
        if not( TradeContext.existVariable( "productid" ) and len(TradeContext.productid.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "险种不存在"
            raise AfaFlowControl.flowException( )
        
        #缴费方式
        if not( TradeContext.existVariable( "paymethod" ) and len(TradeContext.paymethod.strip()) > 0 ):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "缴费方式不存在"
            raise AfaFlowControl.flowException( )   
        
        #缴费年限
        if not( TradeContext.existVariable( "paydatelimit" ) and len(TradeContext.paydatelimit.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "缴费年限不存在"
            raise AfaFlowControl.flowException( )  
        
        #投保人姓名
        if not( TradeContext.existVariable( "tbr_name" ) and len(TradeContext.tbr_name.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "投保人姓名不存在"
            raise AfaFlowControl.flowException( )
        
        #投保人证件号码
        if not( TradeContext.existVariable( "tbr_idno" ) and len(TradeContext.tbr_idno.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "投保人证件号码不存在"
            raise AfaFlowControl.flowException( )
        
        #被保险人姓名
        if not( TradeContext.existVariable( "bbr_name" ) and len(TradeContext.bbr_name.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "被保险人姓名不存在"
            raise AfaFlowControl.flowException( )  
        
        #被保险人证件号码
        if not( TradeContext.existVariable( "bbr_idno" ) and len(TradeContext.bbr_idno.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "被保险人号码证件不存在"
            raise AfaFlowControl.flowException( )  
        
        #与投保人关系
        if not( TradeContext.existVariable( "tbr_bbr_rela" ) and len(TradeContext.tbr_bbr_rela.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "与投保人关系不存在"
            raise AfaFlowControl.flowException( )  
       
        #行社营销人员工号
        if not( TradeContext.existVariable( "salerno" ) and len(TradeContext.salerno.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "行社营销人员工号不存在"
            raise AfaFlowControl.flowException( )  
        
        #paymethod1付费方式(0现金，1转账)  accType缴费介质代码（000:现金，001：对私账号，002：借记卡，
        #003：贷记卡，004：对公账号，005：公务卡）  payacc账号  paycard卡号
        TradeContext.accType = ''
        
        if TradeContext.paymethod1=="0":
            TradeContext.accType="000"
       
        else:
            if TradeContext.vouchtype == "49":                                 #vouchtype 49：存储存折
                TradeContext.accType="001"
                TradeContext.accno = TradeContext.payacc                       #账号
            
            elif TradeContext.vouchtype == "81":                               #vouchtype 81：金农借记卡
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
            AfaLoggerFunc.tradeInfo("TradeContext.vouhNo:"+TradeContext.vouhNo)
    except  Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        AfaFlowControl.flowException( )
    
    #输出缴费介质代码
    AfaLoggerFunc.tradeDebug("TradeContext.accType = [" + TradeContext.accType + "]")
    return True

def SubModuleDoSnd( ):
    return True

def SubModuleDoTrd( ):
    
    AfaLoggerFunc.tradeInfo('进入缴费交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']与第三方通讯后处理' )
    
    names = Party3Context.getNames( )
   
    for name in names:
        value = getattr( Party3Context, name )
        #AfaLoggerFunc.tradeInfo(str(name) + ":" + str(value))
        if ( not name.startswith( '__' ) and type(value) is StringType or type(value) is ListType) :
            setattr( TradeContext,name, value )
        #    AfaLoggerFunc.tradeInfo(name + ":" + value)
    
    if( TradeContext.errorCode == '0000' ):
        TradeContext.errorMsg = '交易成功'
        
        #第三方返回成功后生成现金价值文件
        if not YbtFunc.createFile( ):
            return False
          
        #第三方返回成功后更新主流水表的note字段
        if not AfaYbtdb.ADBUpdateTransdtl( ):
            return False
        
    else:
        AfaLoggerFunc.tradeInfo('与第三方交易失败')
        return False

    AfaLoggerFunc.tradeInfo('退出缴费交易与第三方通讯后处理' )
    
    return True


