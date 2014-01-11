# -*- coding: gbk -*-
##################################################################
#   中间业务平台.
#=================================================================
#   程序文件:   TYBT001_8610.py
#   程序说明:   新保投保
#
#   修改时间:   2010-07-28
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaYbtdb
import AfaHostFunc
from types import *

def SubModuleDoFst( ):

    #校验保险公司代码和凭证种类是否合法
    if not AfaYbtdb.ADBCheckCert( ):
        return False
        
    try:
        AfaLoggerFunc.tradeInfo( '初始化新保投保交易变量' )
        
        #交易代码（8610）
        TradeContext.tradeCode = TradeContext.TransCode
        
        #保险公司代码
        if not( TradeContext.existVariable( "unitno" ) and len(TradeContext.unitno.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "不存在保险公司代码"
            raise AfaFlowControl.flowException( )
            
        #险种
        if not( TradeContext.existVariable( "productid" ) and len(TradeContext.productid.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "险种不存在"
            raise AfaFlowControl.flowException( )
            
        #投保人姓名
        if not( TradeContext.existVariable( "tbr_name" ) and len(TradeContext.tbr_name.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "投保人姓名不存在"
            raise AfaFlowControl.flowException( )
            
        #投保人证件类型
        if not( TradeContext.existVariable( "tbr_idtype" ) and len(TradeContext.tbr_idtype.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "投保人证件类型不存在"
            raise AfaFlowControl.flowException( )
            
        #投保人证件号码
        if not( TradeContext.existVariable( "tbr_idno" ) and len(TradeContext.tbr_idno.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "投保人证件号码不存在"
            raise AfaFlowControl.flowException( )
            
        #投保人性别
        if not( TradeContext.existVariable( "tbr_sex" ) and len(TradeContext.tbr_sex.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "投保人性别不存在"
            raise AfaFlowControl.flowException( )
            
        #投保人出生日期
        if not( TradeContext.existVariable( "tbr_birth" ) and len(TradeContext.tbr_birth.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "投保人出生日期不存在"
            raise AfaFlowControl.flowException( )
            
        #投保人家庭地址    
        if not( TradeContext.existVariable( "tbr_addr" ) and len(TradeContext.tbr_addr.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "投保人家庭地址不存在"
            raise AfaFlowControl.flowException( )
            
        #投保人家庭号码 投保人移动号码
        if not( TradeContext.existVariable( "tbr_tel" )  or TradeContext.existVariable( "tbr_mobile" ) ):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "投保人电话不存在"
            raise AfaFlowControl.flowException( )
            
        #投保人邮政编码
        if not( TradeContext.existVariable( "tbr_postcode" ) and len(TradeContext.tbr_postcode.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "投保人邮政编码不存在"
            raise AfaFlowControl.flowException( )
              
        #投保单号
        if not( TradeContext.existVariable( "applno" ) and len(TradeContext.applno.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "投保单号不存在"
            raise AfaFlowControl.flowException( ) 
             
        #保单印刷号
        if not( TradeContext.existVariable( "userno" ) and len(TradeContext.userno.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "保单印刷号不存在"
            raise AfaFlowControl.flowException( )
              
        #投保日期
        if not( TradeContext.existVariable( "tb_date" ) and len(TradeContext.tb_date.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "投保日期不存在"
            raise AfaFlowControl.flowException( )  
       
        #应缴保费
        if not( TradeContext.existVariable( "amount" ) and len(TradeContext.amount.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "应缴保费不存在"
            raise AfaFlowControl.flowException( ) 
             
        #保险期间类型
        if not( TradeContext.existVariable( "tormtype" ) and len(TradeContext.tormtype.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "保险期间类型不存在"
            raise AfaFlowControl.flowException( )
              
        #保险期间
        if not( TradeContext.existVariable( "coverage_year" ) and len(TradeContext.coverage_year.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "保险期间不存在"
            raise AfaFlowControl.flowException( )  
       
        #缴费方式
        if ( TradeContext.existVariable( "paymethod" ) and len(TradeContext.paymethod.strip()) > 0 ):
            if(TradeContext.paymethod=='1'):
                #当缴费方式为1（期缴）时缴费年期类型为2（按年限交）（中国人寿特有字段）
                TradeContext.charge_period='2'                                         
            else:
                #当缴费方式为5（趸交）时缴费年期类型为1（趸交）
                TradeContext.charge_period='1'  
        
        #缴费年限
        if not( TradeContext.existVariable( "paydatelimit" ) and len(TradeContext.paydatelimit.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "缴费年限不存在"
            raise AfaFlowControl.flowException( )  
       
        #被保险人姓名
        if not( TradeContext.existVariable( "bbr_name" ) and len(TradeContext.bbr_name.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "被保险人姓名不存在"
            raise AfaFlowControl.flowException( )
              
        #被保险人证件类型
        if not( TradeContext.existVariable( "bbr_idtype" ) and len(TradeContext.bbr_idtype.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "被保险人证件类型不存在"
            raise AfaFlowControl.flowException( )  
            
        #被保险人证件号码
        if not( TradeContext.existVariable( "bbr_idno" ) and len(TradeContext.bbr_idno.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "被保险人号码证件不存在"
            raise AfaFlowControl.flowException( ) 
             
        #被保险人性别
        if not( TradeContext.existVariable( "bbr_sex" ) and len(TradeContext.bbr_sex.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "被保险人性别不存在"
            raise AfaFlowControl.flowException( )
              
        #被保险人出生日期
        if not( TradeContext.existVariable( "bbr_birth" ) and len(TradeContext.bbr_birth.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "被保险人出生日期不存在"
            raise AfaFlowControl.flowException( )
            
        #被保险人职业
        if not( TradeContext.existVariable( "bbr_worktype" ) and len(TradeContext.bbr_worktype.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "被保险人职业不存在"
            raise AfaFlowControl.flowException( ) 
             
        #与投保人关系
        if not( TradeContext.existVariable( "tbr_bbr_rela" ) and len(TradeContext.tbr_bbr_rela.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "与投保人关系不存在"
            raise AfaFlowControl.flowException( )  
        
        #柜员工号
        if not( TradeContext.existVariable( "tellers" ) and len(TradeContext.tellers.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "柜员工号不存在"
            raise AfaFlowControl.flowException( )
              
        #行社营销人员工号
        if not( TradeContext.existVariable( "salerno" ) and len(TradeContext.salerno.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "行社营销人员工号不存在"
            raise AfaFlowControl.flowException( ) 
             
        #凭证种类
        if not( TradeContext.existVariable( "I1CETY" ) and len(TradeContext.I1CETY.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "凭证种类不存在"
            raise AfaFlowControl.flowException( )  
        if(TradeContext.syr_type=='1'):      
            #初始化受益人信息 ,最多有五组   
            syr_name = []
            syr_idtype = []
            syr_idno = []
            syr_sex = []
            syr_order = []
            syr_bbr_rela = []
            syr_bent_profit_pcent = []
            syr_bent_profit_base = []
            
             
            #受益人1信息
            if TradeContext.existVariable( "syr_1" ) :  
                if not (len(TradeContext.syr_1.strip())>0 ):
                    syr_name.append("")
                    syr_idtype.append("")
                    syr_idno.append("")
                    syr_sex.append("")
                    syr_order.append("")
                    syr_bbr_rela.append("")
                    syr_bent_profit_pcent.append("")
                    syr_bent_profit_base.append("")
                else:
                    syr1=TradeContext.syr_1.split('|')
                    #受益人名字
                    syr_name.append(syr1[0])
                    #受益人证件类型
                    syr_idtype.append(syr1[1])
                    #受益人证件号码
                    syr_idno.append(syr1[2])
                    #受益人性别
                    syr_sex.append(syr1[3])
                    #受益顺序
                    syr_order.append(syr1[5])
                    #与受益人关系
                    syr_bbr_rela.append(syr1[6])
                    #受益份额（分子部分）
                    syr_bent_profit_pcent.append(syr1[7])
                    #受益份额（分母部分）
                    syr_bent_profit_base.append(syr1[8])
            
            
       
            #受益人2信息
            if  TradeContext.existVariable( "syr_2" ) :  
                if not (len(TradeContext.syr_2.strip())>0 ):
                    syr_name.append("")
                    syr_idtype.append("")
                    syr_idno.append("")
                    syr_sex.append("")
                    syr_order.append("")
                    syr_bbr_rela.append("")
                    syr_bent_profit_pcent.append("")
                    syr_bent_profit_base.append("")
                else:
                    syr2=TradeContext.syr_2.split('|')
                    #受益人名字
                    syr_name.append(syr2[0])
                    #受益人证件类型
                    syr_idtype.append(syr2[1])
                    #受益人证件号码
                    syr_idno.append(syr2[2])
                    #受益人性别
                    syr_sex.append(syr2[3])
                    #受益顺序
                    syr_order.append(syr2[5])
                    #与受益人关系
                    syr_bbr_rela.append(syr2[6])
                    #受益份额（分子部分）
                    syr_bent_profit_pcent.append(syr2[7])
                    #受益份额（分母部分）
                    syr_bent_profit_base.append(syr2[8])
                
                
            #受益人3信息
            if  TradeContext.existVariable( "syr_3" ):  
                if not (len(TradeContext.syr_3.strip())>0 ): 
                    syr_name.append("")   
                    syr_idtype.append("") 
                    syr_idno.append("")  
                    syr_sex.append("")      
                    syr_order.append("")    
                    syr_bbr_rela.append("") 
                    syr_bent_profit_pcent.append("")    
                    syr_bent_profit_base.append("")     
                else:
                    syr3=TradeContext.syr_3.split('|')
                    #受益人名字
                    syr_name.append(syr3[0])
                    #受益人证件类型
                    syr_idtype.append(syr3[1])
                    #受益人证件号码
                    syr_idno.append(syr3[2])
                    #受益人性别
                    syr_sex.append(syr3[3])
                    #受益顺序
                    syr_order.append(syr3[5])
                    #与受益人关系
                    syr_bbr_rela.append(syr3[6])
                    #受益份额（分子部分）
                    syr_bent_profit_pcent.append(syr3[7])
                    #受益份额（分母部分）
                    syr_bent_profit_base.append(syr3[8])
                
                
            #受益人4信息
            if  TradeContext.existVariable( "syr_4" ):  
                if not (len(TradeContext.syr_4.strip())>0 ):   
                    syr_name.append("")                        
                    syr_idtype.append("")                      
                    syr_idno.append("")                        
                    syr_sex.append("")                         
                    syr_order.append("")                       
                    syr_bbr_rela.append("")                    
                    syr_bent_profit_pcent.append("")           
                    syr_bent_profit_base.append("")            
                else:
                    syr4=TradeContext.syr_4.split('|')
                    #受益人名字
                    syr_name.append(syr4[0])
                    #受益人证件类型
                    syr_idtype.append(syr4[1])
                    #受益人证件号码
                    syr_idno.append(syr4[2])
                    #受益人性别
                    syr_sex.append(syr4[3])
                    #受益顺序
                    syr_order.append(syr4[5])
                    #与受益人关系
                    syr_bbr_rela.append(syr4[6])
                    #受益份额（分子部分）
                    syr_bent_profit_pcent.append(syr4[7])
                    #受益份额（分母部分）
                    syr_bent_profit_base.append(syr4[8]) 
                    
        
            #受益人5信息
            if  TradeContext.existVariable( "syr_5" ) :  
                
                if not (len(TradeContext.syr_5.strip())>0 ):   
                    syr_name.append("")                        
                    syr_idtype.append("")                      
                    syr_idno.append("")                        
                    syr_sex.append("")                         
                    syr_order.append("")                       
                    syr_bbr_rela.append("")                    
                    syr_bent_profit_pcent.append("")           
                    syr_bent_profit_base.append("")            
                else:
                    syr5=TradeContext.syr_5.split('|')
                    #受益人名字
                    syr_name.append(syr5[0])
                    #受益人证件类型
                    syr_idtype.append(syr5[1])
                    #受益人证件号码
                    syr_idno.append(syr5[2])
                    #受益人性别
                    syr_sex.append(syr5[3])
                    #受益顺序
                    syr_order.append(syr5[5])
                    #与受益人关系
                    syr_bbr_rela.append(syr5[6])
                    #受益份额（分子部分）
                    syr_bent_profit_pcent.append(syr5[7])
                    #受益份额（分母部分）
                    syr_bent_profit_base.append(syr5[8])    
       
            
            TradeContext.syr_name = syr_name
            TradeContext.syr_idtype = syr_idtype
            TradeContext.syr_idno = syr_idno
            TradeContext.syr_sex = syr_sex
            TradeContext.syr_order = syr_order
            TradeContext.syr_bbr_rela = syr_bbr_rela
            TradeContext.syr_bent_profit_pcent = syr_bent_profit_pcent
            TradeContext.syr_bent_profit_base = syr_bent_profit_base
            
        
        return True 
                
    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        AfaFlowControl.flowException( )       
   
   
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('进入查询交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']与第三方通讯后处理' )
    try:
        names = Party3Context.getNames( )
        for name in names:
            value = getattr( Party3Context, name )
            if ( not name.startswith( '__' ) and type(value) is StringType) :
                setattr( TradeContext, name, value )
                #AfaLoggerFunc.tradeInfo("name:" + str(name) + "     value:" + str(value))
            
        if( TradeContext.errorCode == '0000' ):
            if not AfaYbtdb.AdbSelectQueDtl( ):                             #根据投保单号和日期查询YBT_INFO表，有记录更新，无记录插入
                raise AfaFlowControl.flowException()
        
        AfaLoggerFunc.tradeInfo('退出查询交易与第三方通讯后处理' )
        return True
        
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
