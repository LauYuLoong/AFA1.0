#  -*- coding: gbk -*-
##################################################################
#   中间业务平台.银保通数据库操作类
#=================================================================
#   程序文件:   AfaybtDb.py
#   修改时间:   2010-07-28
#   作    者:   Agree
##################################################################
import TradeContext,AfaLoggerFunc,AfaDBFunc,AfaUtilTools,AfaFlowControl,TransBillFunc,AfaFunc
from types import *


################################################################################
# 函 数 名: AdbInsertQueDtl
# 功能说明: 银保通 交易信息登记流水
# 修改记录：
# 返回值：    True  插入流水表成功    False 插入流水表失败
# 函数说明：  将流水信息插入流水表
################################################################################
def AdbInsertQueDtl( ):
    AfaLoggerFunc.tradeInfo( '>>>>>>>开始插入银保通信息表: [ybt_info ]<<<<<<<')
    
    #流水表的列数-1
    count=42
    TransDtl=[[]]*( count+1 )
   
    #中间业务信息
    TransDtl[0] = TradeContext.agentSerialno                              # AGENTSERIALNO 代理业务流水号
    TransDtl[1] = TradeContext.sysId                                      # SYSID         系统标识
    TransDtl[2] = TradeContext.workDate                                   # WORKDATE      交易日期
    TransDtl[3] = TradeContext.workTime                                   # WORKTIME      交易时间
    TransDtl[4] = TradeContext.brno                                       # BRNO          交易机构
    TransDtl[5] = TradeContext.tellerno                                   # TELLERNO      柜员号
    
    #投保信息
    TransDtl[6] = TradeContext.unitno                                     # unitno        保险公司编码
    TransDtl[7] = TradeContext.tb_date                                    # tb_date       投保日期
    TransDtl[8] = TradeContext.applno                                     # applno        投保单号
    TransDtl[9] =TradeContext.I1CETY                                      #pz_type        凭证类型
    TransDtl[10] = TradeContext.userno                                    # bd_print_no   保单印刷号（凭证号） 
    TransDtl[11] =TradeContext.amount                                     #amount       应缴保费
    
    #初始化TransDtl[12]和TransDtl[14]
    TransDtl[12] = ''
    TransDtl[14] = ''
    
    #AfaLoggerFunc.tradeInfo('------------test1-----------------')
    
    #险种信息（主险|附加险）                             
    if( TradeContext.existVariable( "productid" ) ):                      #productid      主险险种
        TransDtl[12] = TransDtl[12] + TradeContext.productid.strip()
    TransDtl[12] = TransDtl[12] + "|"
    
    if ( TradeContext.existVariable( "productid1" ) ):                    #productid1    附加险种
        TransDtl[12] = TransDtl[12] + TradeContext.productid1.strip()
   
    #保险期间类型  
    if( TradeContext.existVariable( "pre_tormtype" ) ):                   #tormtype     保险期间类型   
        TransDtl[13] = TradeContext.pre_tormtype  
    
    #保险期间
    if( TradeContext.existVariable( "coverage_year" ) ):                  #保险期间 （年份或起始日期）            
        TransDtl[14] = TransDtl[14] + TradeContext.coverage_year.strip()
    TransDtl[14] = TransDtl[14] + "|"
    
    if ( TradeContext.existVariable( "TermDate" ) ):                      #终止日期 
        TransDtl[14] = TransDtl[14] + TradeContext.TermDate.strip()    
                              
    if( TradeContext.existVariable( "paydatelimit" ) ):                   #缴费年限
        TransDtl[15] = TradeContext.paydatelimit
          
    if( TradeContext.existVariable( "pre_paymethod" ) ):                  #缴费方式
        TransDtl[16] = TradeContext.pre_paymethod
    
    #投保人信息
    if( TradeContext.existVariable( "tbr_name" ) ):                       #投保人姓名
        TransDtl[17] = TradeContext.tbr_name
    
    if( TradeContext.existVariable( "pre_tbr_sex" ) ):                    #投保人性别
        TransDtl[18] = TradeContext.pre_tbr_sex
    
    if( TradeContext.existVariable( "tbr_birth" ) ):                      #投保人生日
        TransDtl[19] = TradeContext.tbr_birth
    
    if( TradeContext.existVariable( "pre_tbr_idtype" ) ):                     #投保人证件类型
        TransDtl[20] = TradeContext.pre_tbr_idtype
    
    if( TradeContext.existVariable( "tbr_idno" ) ):                       #投保人证件号码
        TransDtl[21] = TradeContext.tbr_idno
    
    if( TradeContext.existVariable( "tbr_addr" ) ):                       #投保人地址
        TransDtl[22] = TradeContext.tbr_addr
   
    if( TradeContext.existVariable( "tbr_postcode" ) ):                   #投保人邮编
        TransDtl[23] = TradeContext.tbr_postcode
    
    if( TradeContext.existVariable( "tbr_tel" ) ):                        #投保人电话
        TransDtl[24] = TradeContext.tbr_tel
    else:
        TransDtl[24] = ''
        
    if( TradeContext.existVariable( "tbr_mobile" ) ):                     #投保人移动电话
        TransDtl[25] = TradeContext.tbr_mobile
    else:
        TransDtl[25] = ''
        
    if( TradeContext.existVariable( "tbr_email" ) ):                      #投保人邮箱
        TransDtl[26] = TradeContext.tbr_email
    else:
        TransDtl[26] = ''
        
    if( TradeContext.existVariable( "pre_tbr_bbr_rela" ) ):                   #投保人与被保人关系
        TransDtl[27] = TradeContext.pre_tbr_bbr_rela  
    
    #被保人信息
    if( TradeContext.existVariable( "bbr_name" ) ):                       #被保人名字
        TransDtl[28] = TradeContext.bbr_name
    
    if( TradeContext.existVariable( "bbr_sex" ) ):                        #被保人性别
        TransDtl[29] = TradeContext.bbr_sex
   
    if( TradeContext.existVariable( "bbr_birth" ) ):                      #被保人生日
        TransDtl[30] = TradeContext.bbr_birth
    
    if( TradeContext.existVariable( "pre_bbr_idtype" ) ):                     #被保人证件类型
        TransDtl[31] = TradeContext.pre_bbr_idtype
    
    if( TradeContext.existVariable( "bbr_idno" ) ):                       #被保人证件号
        TransDtl[32] = TradeContext.bbr_idno
        
    if( TradeContext.existVariable( "bbr_addr" ) ):                       #被保人地址
        TransDtl[33] = TradeContext.bbr_addr
    else:
        TransDtl[33]= ''
        
    if( TradeContext.existVariable( "bbr_postcode" ) ):                   #被保人邮编
        TransDtl[34] = TradeContext.bbr_postcode
    else:
        TransDtl[34] =''
        
    if( TradeContext.existVariable( "bbr_tel" ) ):                        #被保人电话
        TransDtl[35] = TradeContext.bbr_tel
    else:
        TransDtl[35]=''
        
    if( TradeContext.existVariable( "bbr_mobile" ) ):                     #被保人移动电话
        TransDtl[36] = TradeContext.bbr_mobile
    else:
        TransDtl[36]=''
        
    if( TradeContext.existVariable( "bbr_email" ) ):                      #被保人邮箱
        TransDtl[37] = TradeContext.bbr_email
    else:
        TransDtl[37]=''

    #初始化信息
    TransDtl[38] = ''
    TransDtl[39] = ''
    TransDtl[40] = ''
    TransDtl[41] = ''
    TransDtl[42] = ''
    
    #受益人信息
    #受益人1信息（姓名|证件类型|证件号码|性别|生日|与被保人关系|收益顺序|收益份额(分子)|收益份额（分母））
    if( TradeContext.existVariable( "syr_1" ) and len(TradeContext.syr_1)!=0 ): 
        TransDtl[38] = TransDtl[38] + TradeContext.syr_1
    else:
        TransDtl[38]='' 
    
    if ( TradeContext.existVariable( "syr_2" ) and len(TradeContext.syr_2)!=0):                        
        TransDtl[39] = TransDtl[39] + TradeContext.syr_2
    else:
        TransDtl[39]=''
            
    if( TradeContext.existVariable( "syr_3" )and len(TradeContext.syr_3)!=0 ):                   
        TransDtl[40] = TransDtl[40] + TradeContext.syr_3
    else:
         TransDtl[40]=''
    
    if ( TradeContext.existVariable( "syr_4" ) and len(TradeContext.syr_4)!=0 ):                   
        TransDtl[41] = TransDtl[41] + TradeContext.syr_4
    else:
        TransDtl[41]=''  
    
    if ( TradeContext.existVariable( "syr_5" )and len(TradeContext.syr_5)!=0  ):                 
        TransDtl[42] = TransDtl[42] + TradeContext.syr_5
    else:
        TransDtl[42]=''    
  
    sql = "INSERT INTO YBT_INFO ("
    sql = sql + "AGENTSERIALNO,SYSID,WORKDATE,WORKTIME,BRNO,TELLERNO,CPICNO,SUBMISDATE,SUBMINO,PROCODE,PRINTNO,AMOUNT,XZINFO,"
    sql = sql + "TORMTYPE,EFFTORM,PAYOUTDUR,PAYOUTTYPE,TBR_NAME,TBR_SEX,TBR_BIRTH,TBR_IDTYPE,TBR_IDNO,TBR_ADDR,TBR_POSTCODE,"
    sql = sql + "TBR_TEL,TBR_MOBILE,TBR_EMAIL,TBR_BBR_RELA,BBR_NAME,BBR_SEX,BBR_BIRTH,BBR_IDTYPE,BBR_IDNO,BBR_ADDR,BBR_POSTCODE,"
    sql = sql + "BBR_TEL,BBR_MOBILE,BBR_EMAIL,SYR_INFO1,SYR_INFO2,SYR_INFO3,SYR_INFO4,SYR_INFO5) VALUES("

    i=0
    for i in range( 0, count ):
        if( type( TransDtl[i] ) is int ):
            sql=sql+str( TransDtl[i] )+","
        else:
            sql=sql+"'"+ TransDtl[i]+"',"
    
    sql=sql+"'"+TransDtl[count]+"')"
    
    AfaLoggerFunc.tradeInfo( '>>>>>>>新保投保交易登记流水<<<<<<< ' + str(sql))
    
    #插入并提交数据
    result=AfaDBFunc.InsertSqlCmt( sql )
        
    if( result < 1 ):
        TradeContext.errorCode, TradeContext.errorMsg='A0044', '插入流水表失败'+AfaDBFunc.sqlErrMsg
        return False
    
    else:
        return True




################################################################################
# 函 数 名： AdbSelectQueDtl
# 功能说明: 缴费交易第三方返回成功后查询是否存在原投保单号的记录
# 修改记录: 
# 备    注: 
# 范    例: 
###############################################################################     
def AdbSelectQueDtl( ):
   
    AfaLoggerFunc.tradeInfo( '>>>>>>>开始查询原交易<<<<<<<') 
      
    sql = "select * from YBT_INFO "
    sql = sql + " where WORKDATE = '" + TradeContext.workDate.strip() + "'"         #交易日期
    sql = sql + " and   SUBMINO  = '" + TradeContext.applno.strip()   + "'"         #投保单号
    sql = sql + " and   cpicno   = '" + TradeContext.unitno           + "'"         #保险公司单位编码
    sql = sql + " and   tellerno = '" + TradeContext.tellerno         + "'"         #交易柜员号
    
    AfaLoggerFunc.tradeInfo( '>>>>>>>开始查询原交易：'+ str(sql)) 
    
    records = AfaDBFunc.SelectSql( sql ) 
   
    AfaLoggerFunc.tradeInfo('查询到记录条数为：'+str(len(records)))
    
    #没有记录则插入数据
    if(len(records)==0):
        if not AdbInsertQueDtl( ):
            raise AfaFlowControl.flowException() 
        else:
            return True       
   
    #有记录则更新原纪录       
    else:
        if not AdbUpdateQueDtl( ):
            raise AfaFlowControl.flowException()
        else:
            return True    





################################################################################
# 函 数 名： AdbUpdateQueDtl
# 功能说明: 更新原投保记录(YBT_INFO表)确保一个投保单号对应一条记录
# 修改记录: 

# 备    注: 
# 范    例: 
###############################################################################          
def AdbUpdateQueDtl( ):
    
    AfaLoggerFunc.tradeInfo( '>>>>>>>开始更新原投保记录确保一个投保单号对应一条记录<<<<<<<')
    
    sqlupdate = ""
    sqlupdate = sqlupdate + " update YBT_INFO SET "
    
    #系统信息
    sqlupdate = sqlupdate + "AGENTSERIALNO = '" + TradeContext.agentSerialno.strip() + "',"                        # AGENTSERIALNO 代理业务流水号
    sqlupdate = sqlupdate + "SYSID         = '" + TradeContext.sysId.strip()         + "',"                        # SYSID         系统标识
    sqlupdate = sqlupdate + "WORKDATE      = '" + TradeContext.workDate.strip()      + "',"                        # WORKDATE      交易日期
    sqlupdate = sqlupdate + "WORKTIME      = '" + TradeContext.workTime.strip()      + "',"                        # WORKTIME      交易时间
    sqlupdate = sqlupdate + "BRNO          = '" + TradeContext.brno.strip()          + "',"                        # BRNO          交易机构
    sqlupdate = sqlupdate + "TELLERNO      = '" + TradeContext.tellerno.strip()      + "',"                        # TELLERNO      柜员号
    
    #投保信息
    sqlupdate = sqlupdate + "CPICNO        = '" + TradeContext.unitno.strip()         +"',"                        # unitno        保险公司编码
    sqlupdate = sqlupdate + "SUBMISDATE    = '" + TradeContext.tb_date.strip()        +"',"                        # tb_date       投保日期
    sqlupdate = sqlupdate + "SUBMINO       = '" + TradeContext.applno.strip()         +"',"                        # applno        投保单号
    sqlupdate = sqlupdate + "PROCODE       = '" + TradeContext.I1CETY.strip()         +"',"                        #pz_type        凭证类型
    sqlupdate = sqlupdate + "PRINTNO       = '" + TradeContext.userno.strip()         +"',"                        # bd_print_no   保单印刷号（凭证号）
    sqlupdate = sqlupdate + "AMOUNT        = '" + TradeContext.amount.strip()         +"',"                        #amount         应缴保费
    
    #险种信息（主险|附加险）file1做为中间变量保存险种信息
    TradeContext.file1 = ""
    
    if TradeContext.existVariable( "productid" ):                                                                  #productid      主险险种
        TradeContext.file1 = TradeContext.file1 + TradeContext.productid.strip() 
    TradeContext.file1     = TradeContext.file1 + "|"    
       
    if TradeContext.existVariable( "productid1" ):                                                                 #productid1     附加险种
        TradeContext.file1 = TradeContext.file1 +TradeContext.productid1.strip()
    
    if ( len(str(TradeContext.file1.strip())) > 0): 
        sqlupdate = sqlupdate + "XZINFO = '"+TradeContext.file1+"', " 
   
    #保险期间类型     
    if( TradeContext.existVariable( "pre_tormtype" ) ):
        sqlupdate = sqlupdate + "TORMTYPE = '" + TradeContext.pre_tormtype.strip() + "',"              
    
    #保险期间 file2做为中间变量保存信息   
    TradeContext.file2=""
    
    if TradeContext.existVariable( "coverage_year" ):                                             #保险期间 （年份或起始日期）                      
        TradeContext.file2 = TradeContext.file2 + TradeContext.coverage_year.strip() 
    TradeContext.file2 = TradeContext.file2 + "|"    
       
    if TradeContext.existVariable( "TermDate" ):                                                  #终止日期                    
        TradeContext.file2 = TradeContext.file2 +TradeContext.TermDate.strip()  
    
    if ( len(str(TradeContext.file2.strip())) > 0): 
        sqlupdate = sqlupdate + "EFFTORM = '"+TradeContext.file2+"', " 
    
    
        
    if( TradeContext.existVariable( "paydatelimit" ) ):                                            #缴费年限
        sqlupdate = sqlupdate + "PAYOUTDUR = '" + TradeContext.paydatelimit.strip() + "',"   
              
    if( TradeContext.existVariable( "pre_paymethod" ) ):                                           #缴费方式 
        sqlupdate = sqlupdate + "PAYOUTTYPE = '" + TradeContext.pre_paymethod.strip() + "',"   
      
    #投保人信息        
    if( TradeContext.existVariable( "tbr_name" ) ):                                                #投保人姓名
        sqlupdate = sqlupdate + "TBR_NAME = '" + TradeContext.tbr_name.strip() + "',"    
    
    if( TradeContext.existVariable( "pre_tbr_sex" ) ):                                                 #投保人性别
        sqlupdate = sqlupdate + "TBR_SEX = '" + TradeContext.pre_tbr_sex.strip() + "',"    
    
    if( TradeContext.existVariable( "tbr_birth" ) ):                                               #投保人生日
        sqlupdate = sqlupdate + "TBR_BIRTH= '" + TradeContext.tbr_birth.strip() + "',"    
   
    if( TradeContext.existVariable( "pre_tbr_idtype" ) ):                                              #投保人证件类型
        sqlupdate = sqlupdate + " TBR_IDTYPE='" + TradeContext.pre_tbr_idtype.strip() + "',"
    
    if( TradeContext.existVariable( "tbr_idno" ) ):                                                #投保人证件号码
        sqlupdate = sqlupdate + " TBR_IDNO='" + TradeContext.tbr_idno.strip() + "',"
   
    if( TradeContext.existVariable( "tbr_addr" ) ):                                                #投保人地址
        sqlupdate = sqlupdate + " TBR_ADDR='" + TradeContext.tbr_addr.strip() + "',"
    
    if( TradeContext.existVariable( "tbr_postcode" ) ):                                            #投保人邮编
        sqlupdate = sqlupdate + " TBR_POSTCODE='" + TradeContext.tbr_postcode.strip() + "',"
        
    if( TradeContext.existVariable( "tbr_tel" ) ):                                                 #投保人电话
        sqlupdate = sqlupdate + " TBR_TEL= '" + TradeContext.tbr_tel.strip() + "',"
    else:
        sqlupdate = sqlupdate + " TBR_TEL= '',"  
          
    if( TradeContext.existVariable( "tbr_mobile" ) ):                                             #投保人移动电话
        sqlupdate = sqlupdate + " TBR_MOBILE= '" + TradeContext.tbr_mobile.strip() + "',"
    else:
        sqlupdate = sqlupdate + " TBR_MOBILE= '',"    
        
    if( TradeContext.existVariable( "tbr_email" ) ):                                              #投保人邮箱
         sqlupdate = sqlupdate + " TBR_EMAIL= '" + TradeContext.tbr_email.strip() + "',"
    else:
         sqlupdate = sqlupdate + "TBR_EMAIL = ''," 
         
    if( TradeContext.existVariable( "pre_tbr_bbr_rela" ) ):                                       #投保人与被保人关系
        sqlupdate = sqlupdate + " TBR_BBR_RELA= '" + TradeContext.pre_tbr_bbr_rela.strip() + "',"     
     
    #被保人信息
    if( TradeContext.existVariable( "bbr_name" ) ):                                               #被保人名字
        sqlupdate = sqlupdate + " BBR_NAME= '" + TradeContext.bbr_name.strip() + "',"
    
    if( TradeContext.existVariable( "bbr_sex" ) ):                                                #被保人性别
        sqlupdate = sqlupdate + " BBR_SEX= '" + TradeContext.bbr_sex.strip() + "',"
    
    if( TradeContext.existVariable( "bbr_birth" ) ):                                              #被保人生日
        sqlupdate = sqlupdate + " BBR_BIRTH= '" + TradeContext.bbr_birth.strip() + "',"
    
    if( TradeContext.existVariable( "pre_bbr_idtype" ) ):                                         #被保人证件类型
        sqlupdate = sqlupdate + " BBR_IDTYPE= '" + TradeContext.pre_bbr_idtype.strip() + "',"
    
    if( TradeContext.existVariable( "bbr_idno" ) ):                                               #被保人证件号
        sqlupdate = sqlupdate + " BBR_IDNO= '" + TradeContext.bbr_idno.strip() + "',"
        
    if( TradeContext.existVariable( "bbr_addr" ) ):                                               #被保人地址
        sqlupdate = sqlupdate + " BBR_ADDR= '" + TradeContext.bbr_addr.strip() + "',"
    else:
        sqlupdate = sqlupdate + " BBR_ADDR= '',"
        
    if( TradeContext.existVariable( "bbr_postcode" ) ):                                           #被保人邮编
        sqlupdate = sqlupdate + " BBR_POSTCODE= '" + TradeContext.bbr_postcode.strip() + "',"
    else:
        sqlupdate = sqlupdate + " BBR_POSTCODE= '',"
        
    if( TradeContext.existVariable( "bbr_tel" ) ):                                                #被保人电话
        sqlupdate = sqlupdate + " BBR_TEL= '" + TradeContext.bbr_tel.strip() + "',"
    else:
        sqlupdate = sqlupdate + " BBR_TEL= '',"
        
    if( TradeContext.existVariable( "bbr_mobile" ) ):                                             #被保人移动电话
        sqlupdate = sqlupdate + " BBR_MOBILE= '" + TradeContext.bbr_mobile.strip() + "',"
    else:
        sqlupdate = sqlupdate + " BBR_MOBILE= '',"
        
    if( TradeContext.existVariable( "bbr_email" ) ):                                              #被保人邮箱
        sqlupdate = sqlupdate + " BBR_EMAIL= '" + TradeContext.bbr_email.strip() + "',"
    else:
        sqlupdate = sqlupdate + " BBR_EMAIL= '',"
        
    #受益人信息
    #受益人1信息（姓名|证件类型|证件号码|性别|生日|与被保人关系|收益顺序|收益份额(分子)|收益份额（分母））   
    if( TradeContext.existVariable( "syr_1" ) and len(TradeContext.syr_1)!=0 ):                   #受益人1信息    
        sqlupdate = sqlupdate + " SYR_INFO1= '" + TradeContext.syr_1.strip() + "',"   
    else:
        sqlupdate = sqlupdate + " SYR_INFO1= ''," 
         
    if( TradeContext.existVariable( "syr_2" ) and len(TradeContext.syr_2)!=0 ):                   #受益人2信息    
        sqlupdate = sqlupdate + " SYR_INFO2= '" + TradeContext.syr_2.strip() + "',"                 
    else:
        sqlupdate = sqlupdate + " SYR_INFO2= '',"
        
    if( TradeContext.existVariable( "syr_3" ) and len(TradeContext.syr_3)!=0 ):                   #受益人3信息    
        sqlupdate = sqlupdate + " SYR_INFO3= '" + TradeContext.syr_3.strip() + "',"  
    else:
        sqlupdate = sqlupdate + " SYR_INFO3= '',"
        
    if( TradeContext.existVariable( "syr_4" ) and len(TradeContext.syr_4)!=0 ):                   #受益人4信息    
        sqlupdate = sqlupdate + " SYR_INFO4= '" + TradeContext.syr_4.strip() + "',"    
    else:
        sqlupdate = sqlupdate + " SYR_INFO4= '',"
        
    if( TradeContext.existVariable( "syr_5" ) and len(TradeContext.syr_5)!=0 ):                   #受益人5信息    
        sqlupdate = sqlupdate + " SYR_INFO5= '" + TradeContext.syr_5.strip() + "'"  
    else:
        sqlupdate = sqlupdate + " SYR_INFO5= ''"
        
    sqlupdate = sqlupdate + " where WORKDATE = '"+TradeContext.workDate+"' and SUBMINO = '"+TradeContext.applno+"'"
    
    AfaLoggerFunc.tradeInfo( 'sqlupdate = ' + str(sqlupdate))                                     #输出SQL语句
    
    #更新并提交数据
    record=AfaDBFunc.UpdateSqlCmt( sqlupdate )
    
    if( record > 0 ):
        AfaLoggerFunc.tradeInfo( '>>>>>>>更新原投保记录成功<<<<<<<')
        return True
        
    if( record == 0 ):
        AfaLoggerFunc.tradeInfo( '>>>>>>>无投保记录<<<<<<<')
        TradeContext.errorCode,TradeContext.errorMsg='A0100','无投保记录'
        return False
        
    else :
        AfaLoggerFunc.tradeInfo( '>>>>>>>更新原投保记录失败<<<<<<<')
        TradeContext.errorCode, TradeContext.errorMsg='A0100', '更新原投保记录失败' + AfaDBFunc.sqlErrMsg
        return False
      
################################################################################
# 函 数 名: ADBUpdateTransdtl
# 功能说明:缴费交易第三方返回成功后更新记录
# 修改记录: 
# 备    注: 
# 范    例: 
###############################################################################
def ADBUpdateTransdtl( ):
    AfaLoggerFunc.tradeInfo( '>>>>>>>开始更新原缴费交易<<<<<<<')
    
    #初始化信息
    sqlupdate = ""
    TradeContext.note1  = ""
    TradeContext.note2  = ""
    TradeContext.note3  = ""
    TradeContext.note4  = ""
    TradeContext.note5  = ""
    TradeContext.note6  = ""
    TradeContext.note7  = ""
    TradeContext.note8  = ""
    TradeContext.note9  = ""
    TradeContext.note10 = ""
    
    sqlupdate = sqlupdate + "update afa_maintransdtl set "

    #corpSerno:更新第三方流水号
    if TradeContext.existVariable( "corpSerno" ):
        sqlupdate = sqlupdate + " corpSerno = '" + TradeContext.corpSerno.strip() + "' "
    else:
        sqlupdate = sqlupdate + " corpSerno = '' "

    #note1:账号代码|首期保费|保险金额|保费
    #if( TradeContext.existVariable( "acc_code" ) ):
        #TradeContext.note1 = TradeContext.note1 + TradeContext.acc_code.strip()
    #TradeContext.note1 = TradeContext.note1 + "|"

    if( TradeContext.existVariable( "premium" ) ):
        TradeContext.note1 = TradeContext.note1 + TradeContext.premium.strip()
    TradeContext.note1 = TradeContext.note1 + "|"
    
    if( TradeContext.existVariable( "prem" ) ):
        TradeContext.note1 = TradeContext.note1 + TradeContext.prem.strip()
    TradeContext.note1 = TradeContext.note1 + "|"
    
    if( TradeContext.existVariable( "premium1" ) ):
        TradeContext.note1 = TradeContext.note1 + TradeContext.premium1.strip()
    
    #note2:交费期满日期|交费年期类型|交费期间（缴费年限）
    #if ( TradeContext.existVariable( "payenddate" ) ):
        #TradeContext.note2 = TradeContext.note2 + TradeContext.payenddate.strip()
    #TradeContext.note2 = TradeContext.note2 + "|"

    #if ( TradeContext.existVariable( "charge_period" ) ):
    #    TradeContext.note2 = TradeContext.note2 + TradeContext.charge_period.strip()
    #TradeContext.note2 = TradeContext.note2 + "|"

    if ( TradeContext.existVariable( "paydatelimit" ) ):
        TradeContext.note2 = TradeContext.note2 + TradeContext.paydatelimit.strip()
    
   
    #note3:投保日期|交费日期|保单生效日期
    if( TradeContext.existVariable( "tb_date" ) ):
        TradeContext.note3 = TradeContext.note3 + TradeContext.tb_date.strip()
    TradeContext.note3 = TradeContext.note3 + "|"

    if( TradeContext.existVariable( "paydate" ) ):
        TradeContext.note3 = TradeContext.note3 + TradeContext.paydate.strip()
    #TradeContext.note3 = TradeContext.note3 + "|"

    #if ( TradeContext.existVariable( "validate" ) ):
        #TradeContext.note3 = TradeContext.note3 + TradeContext.validate.strip()
   
    #note4:投保人姓名|投保人证件号码|与投保人关系
    if( TradeContext.existVariable( "tbr_name" ) ):
        TradeContext.note4 = TradeContext.note4 + TradeContext.tbr_name.strip()
    TradeContext.note4 = TradeContext.note4 + "|"

    if ( TradeContext.existVariable( "tbr_idno" ) ):
       TradeContext.note4 = TradeContext.note4 + TradeContext.tbr_idno.strip()
    TradeContext.note4 = TradeContext.note4 + "|"
    if ( TradeContext.existVariable( "tbr_bbr_rela" ) ):
       TradeContext.note4 = TradeContext.note4 + TradeContext.tbr_bbr_rela.strip()
    
    
    #note5:被保人姓名|被保人证件号码|与被保险人关系
    if( TradeContext.existVariable( "bbr_name" ) ):
        TradeContext.note5 = TradeContext.note5 + TradeContext.bbr_name.strip()
    TradeContext.note5 = TradeContext.note5 + "|"

    if ( TradeContext.existVariable( "bbr_idno" ) ):
        TradeContext.note5 = TradeContext.note5 + TradeContext.bbr_idno.strip()
    TradeContext.note5 = TradeContext.note5 + "|"
    
    if ( TradeContext.existVariable( "syr_bbr_rela" ) ):
        TradeContext.note5 = TradeContext.note5 + TradeContext.syr_bbr_rela.strip()
    
    
    #note6:行所营销员员工号|付费方式
    if( TradeContext.existVariable( "salerno" ) ):
        TradeContext.note6 = TradeContext.note6 + TradeContext.salerno.strip()
    TradeContext.note6 = TradeContext.note6 + "|"
   
    if( TradeContext.existVariable( "paymethod1" ) ):
        TradeContext.note6 = TradeContext.note6 + TradeContext.paymethod1.strip()   
    
    
    #note7:交费方式|缴费期次|交费期间
    if( TradeContext.existVariable( "paymethod" ) ):
        TradeContext.note7 = TradeContext.note7 + TradeContext.paymethod.strip()
    TradeContext.note7 = TradeContext.note7 + "|"

    if ( TradeContext.existVariable( "rev_frequ" ) ):
        TradeContext.note7 = TradeContext.note7 + TradeContext.rev_frequ.strip()
    TradeContext.note7 = TradeContext.note7 + "|"
    
    if ( TradeContext.existVariable( "payyear" ) ):
        TradeContext.note7 = TradeContext.note7 + TradeContext.payyear.strip()
    
    #note8:主险险种代码|险种名称|附加险种|保险期间类型|保险期间
    if ( TradeContext.existVariable( "productid" ) ):
        TradeContext.note8 = TradeContext.note8 + TradeContext.productid.strip()
    TradeContext.note8 = TradeContext.note8 + "|"

    if ( TradeContext.existVariable( "productname" ) ):
        TradeContext.note8 = TradeContext.note8 + TradeContext.productname.strip()
    TradeContext.note8 = TradeContext.note8 + "|"
    
    if ( TradeContext.existVariable( "productid1" ) ):
        TradeContext.note8 = TradeContext.note8 + TradeContext.productid1.strip()
    TradeContext.note8 = TradeContext.note8 + "|"
   
    if ( TradeContext.existVariable( "coverage_period" ) ):
        TradeContext.note8 = TradeContext.note8 + TradeContext.coverage_period.strip()
    TradeContext.note8 = TradeContext.note8 + "|"
    
    if ( TradeContext.existVariable( "coverage_year" ) ):
        TradeContext.note8 = TradeContext.note8 + TradeContext.coverage_year.strip 
    
    #note9:投保份数|投保单号|保险单号|主附险标志
    if( TradeContext.existVariable( "amt_unit" ) ):
        TradeContext.note9 = TradeContext.note9 + TradeContext.amt_unit.strip()
    TradeContext.note9 = TradeContext.note9 + "|"

    if ( TradeContext.existVariable( "applno" ) ):
        TradeContext.note9 = TradeContext.note9 + TradeContext.applno.strip()
    TradeContext.note9 = TradeContext.note9 + "|"
    
    if( TradeContext.existVariable( "policy" ) ):
        TradeContext.note9 = TradeContext.note9 + TradeContext.policy.strip()
    TradeContext.note9 = TradeContext.note9 + "|"

    if ( TradeContext.existVariable( "mainsubflg" ) ):
        TradeContext.note9 = TradeContext.note9 + TradeContext.mainsubflg.strip()
    
    #note10:受益人信息
    #if( TradeContext.existVariable( "syr_1" ) ):
    #   TradeContext.note10 = TradeContext.note10 + TradeContext.syr_1.strip()
    #TradeContext.note10 = TradeContext.note10 + "|"

    #if ( TradeContext.existVariable( "syr_2" ) ):
    #    TradeContext.note10 = TradeContext.note10 + TradeContext.syr_2.strip()
    #TradeContext.note10 = TradeContext.note10 + "|"
    
    #if( TradeContext.existVariable( "syr_3" ) ):
    #    TradeContext.note10 = TradeContext.note10 + TradeContext.syr_3.strip()
    #TradeContext.note10 = TradeContext.note10 + "|"

    #if ( TradeContext.existVariable( "syr_4" ) ):
    #   TradeContext.note10 = TradeContext.note10 + TradeContext.syr_4.strip()
    #TradeContext.note10 = TradeContext.note10 + "|"
    
    #if( TradeContext.existVariable( "syr_5" ) ):
    #    TradeContext.note10 = TradeContext.note10 + TradeContext.syr_5.strip()
    
    if ( len(str(TradeContext.note1.strip())) > 0):
        sqlupdate = sqlupdate + ",note1 = '"+TradeContext.note1+"' "
    if ( len(str(TradeContext.note2.strip())) > 0):
        sqlupdate = sqlupdate + ",note2 = '"+TradeContext.note2+"' "
    if ( len(str(TradeContext.note3.strip())) > 0):
        sqlupdate = sqlupdate + ",note3 = '"+TradeContext.note3+"' "
    if ( len(str(TradeContext.note4.strip())) > 0):
        sqlupdate = sqlupdate + ",note4 = '"+TradeContext.note4+"' "
    if ( len(str(TradeContext.note5.strip())) > 0):
        sqlupdate = sqlupdate + ",note5 = '"+TradeContext.note5+"' "
    if ( len(str(TradeContext.note6.strip())) > 0):
        sqlupdate = sqlupdate + ",note6 = '"+TradeContext.note6+"' "
    if ( len(str(TradeContext.note7.strip())) > 0):
        sqlupdate = sqlupdate + ",note7 = '"+TradeContext.note7+"' "
    if ( len(str(TradeContext.note8.strip())) > 0):
        sqlupdate = sqlupdate + ",note8 = '"+TradeContext.note8+"' "
    if ( len(str(TradeContext.note9.strip())) > 0):
        sqlupdate = sqlupdate + ",note9 = '"+TradeContext.note9+"' "
    #if ( len(str(TradeContext.note10.strip())) > 0):
    #    sqlupdate = sqlupdate + ",note10 = '"+TradeContext.note10+"' "
    
    sqlupdate = sqlupdate + " where sysid = '"+TradeContext.sysId+"' and agentserialno = '"+TradeContext.agentSerialno+"'"
    
    AfaLoggerFunc.tradeInfo( 'sqlupdate = ' + str(sqlupdate))
    
    record=AfaDBFunc.UpdateSqlCmt( sqlupdate )
    
    if( record > 0 ):
        AfaLoggerFunc.tradeInfo( '>>>>>>>更新原缴费交易成功<<<<<<<')
        return True
    
    if( record == 0 ):
        AfaLoggerFunc.tradeInfo( '>>>>>>>更新原缴费交易失败<<<<<<<')
        TradeContext.errorCode,TradeContext.errorMsg='A0100','未发现原始交易'
        return False
    else :
        AfaLoggerFunc.tradeInfo( '>>>>>>>更新原缴费交易失败<<<<<<<')
        TradeContext.errorCode, TradeContext.errorMsg='A0100', '更新原交易状态失败' + AfaDBFunc.sqlErrMsg
        return False

        
        
################################################################################
# 函 数 名: ADBCheckCert
# 功能说明: 检查凭证种类与保险公司是否对应
# 
# 备    注:
# 范    例:
###############################################################################
def ADBCheckCert( ):
    AfaLoggerFunc.tradeInfo('>>>>获取保险公司[' + TradeContext.unitno + ']凭证号，做校验<<<<')
    sql = ""
    sql = sql + " select certtype from afa_adbpam where "
    sql = sql + " unitno='" + TradeContext.unitno + "'"                       #单位名称（根据保险公司编号来
                                                                              #查询凭证种类）
    sql = sql + " and certtype='" + TradeContext.I1CETY + "'"
    
    AfaLoggerFunc.tradeInfo( sql )
    
    record = AfaDBFunc.SelectSql( sql )
    
    if ( record==None ):
        AfaLoggerFunc.tradeInfo( '>>>>查询凭证种类异常<<<<' )
        TradeContext.errorCode,TradeContext.errorMsg = 'A0100', '查询凭证种类异常'
        return False
        
    if ( len(record) <= 0):
        AfaLoggerFunc.tradeInfo( '>>>>保险公司代码或凭证种类非法<<<<' )
        TradeContext.errorCode,TradeContext.errorMsg = 'A0100', '保险公司代码或凭证种类非法'
        return False
    
    return True


################################################################################
# 函 数 名: ADBUpdateTransdtlRev
# 功能说明: 冲正缴费交易第三方返回成功后更新返回结果信息
# 修改记录: 
# 备    注: 只有在冲正失败的情况下才记录失败信息
# 范    例: 
###############################################################################
def ADBUpdateTransdtlRev( ):
    sqlupdate = ""
   
    AfaLoggerFunc.tradeInfo( '>>>>>>>开始更新原冲正交易结果信息<<<<<<<')
   
    sqlupdate = sqlupdate + "update afa_maintransdtl set "
    sqlupdate = sqlupdate + " corpcode = '"+TradeContext.errorCode.strip()+"' "
    sqlupdate = sqlupdate + ", errorMsg = '"+TradeContext.errorMsg.strip()+"' "
    sqlupdate = sqlupdate + " where sysid = '"+TradeContext.sysId+"' and agentserialno = '"+TradeContext.agentSerialno+"'"
   
    AfaLoggerFunc.tradeInfo( 'sqlupdate = ' + str(sqlupdate))
   
    record=AfaDBFunc.UpdateSqlCmt( sqlupdate )
   
    if( record > 0 ):
        AfaLoggerFunc.tradeInfo( '>>>>>>>更新原冲正交易结果信息成功<<<<<<<')
        return True
    if( record == 0 ):
        AfaLoggerFunc.tradeInfo( '>>>>>>>更新原冲正交易结果信息失败<<<<<<<')
        TradeContext.errorCode,TradeContext.errorMsg='A0100','未发现原始交易'
        return False
    else :
        AfaLoggerFunc.tradeInfo( '>>>>>>>更新原冲正交易结果信息失败<<<<<<<')
        TradeContext.errorCode, TradeContext.errorMsg='A0100', '更新原交易状态失败' + AfaDBFunc.sqlErrMsg
        return False
