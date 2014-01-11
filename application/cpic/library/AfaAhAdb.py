# -*- coding: gbk -*-
##################################################################
#   中间业务平台.安贷宝缴费数据库操作类
#=================================================================
#   程序文件:   AfaShebaoFunc.py
#   修改时间:   2009-04-16
#    作  者 :   Agree
##################################################################
import TradeContext,AfaLoggerFunc,AfaDBFunc,AfaUtilTools,AfaFlowControl,TransBillFunc,AfaFunc
from types import *

################################################################################
# 函 数 名: ADBUpdateTransdtl
# 功能说明: 缴费交易第三方返回成功后更新记录
# 修改记录: 
# 备    注: 
# 范    例: 
###############################################################################
def ADBUpdateTransdtl( ):
    AfaLoggerFunc.tradeInfo( '>>>>>>>开始更新原缴费交易<<<<<<<')
    sqlupdate = ""
    TradeContext.note2 = ""
    TradeContext.note3 = ""
    TradeContext.note4 = ""
    TradeContext.note6 = ""
    TradeContext.note7 = ""
    TradeContext.note8 = ""
    TradeContext.note9 = ""
    TradeContext.note10 = ""
    sqlupdate = sqlupdate + "update afa_maintransdtl set "

    #Third Serailno
    #corpSerno:第三方流水号
    if TradeContext.existVariable( "corpSerno" ):
        sqlupdate = sqlupdate + " corpSerno = '" + TradeContext.corpSerno.strip() + "' "
    else:
        sqlupdate = sqlupdate + " corpSerno = '' "

    #BaoDanNo:保单号
    if TradeContext.existVariable( "BaoDanNo" ):
        sqlupdate = sqlupdate + " ,note5 = '" + TradeContext.BaoDanNo.strip() + "' "

    #投保信息
    #note2:借款日期|借款结束日期
    if( TradeContext.existVariable( "LoanDate" ) ):
        TradeContext.note2 = TradeContext.note2 + TradeContext.LoanDate.strip()
    TradeContext.note2 = TradeContext.note2 + "|"

    if( TradeContext.existVariable( "LoanEndDate" ) ):
        TradeContext.note2 = TradeContext.note2 + TradeContext.LoanEndDate.strip()

    #note3:责任起始日期|责任结束日期
    if( TradeContext.existVariable( "EffDate" ) ):
        TradeContext.note3 = TradeContext.note3 + TradeContext.EffDate.strip()
    TradeContext.note3 = TradeContext.note3 + "|"

    if ( TradeContext.existVariable( "TermDate" ) ):
        TradeContext.note3 = TradeContext.note3 + TradeContext.TermDate.strip()

    #note4:贷款合同号码|贷款凭证编号
    if( TradeContext.existVariable( "CreBarNo" ) ):
        TradeContext.note4 = TradeContext.note4 + TradeContext.CreBarNo.strip()
    TradeContext.note4 = TradeContext.note4 + "|"

    if ( TradeContext.existVariable( "CreVouNo" ) ):
        TradeContext.note4 = TradeContext.note4 + TradeContext.CreVouNo.strip()

    #note6:太保业务人员代码
    if ( TradeContext.existVariable( "CpicTeller" ) ):
        TradeContext.note6 = TradeContext.CpicTeller.strip()

    #note7:险种类别
    if ( TradeContext.existVariable( "ProCode" ) ):
        TradeContext.note7 = TradeContext.note7 + TradeContext.ProCode.strip()

    #note8:投保份数|险种代码|险种名称
    if ( TradeContext.existVariable( "IntialNum" ) ):
        TradeContext.note8 = TradeContext.note8 + TradeContext.IntialNum.strip()
    TradeContext.note8 = TradeContext.note8 + "|"

    if ( TradeContext.existVariable( "ProCodeStr" ) ):
        TradeContext.note8 = TradeContext.note8 + TradeContext.ProCodeStr.strip()
    TradeContext.note8 = TradeContext.note8 + "|"

    if ( TradeContext.existVariable( "PlanName" ) ):
        TradeContext.note8 = TradeContext.note8 + TradeContext.PlanName.strip()

    #投保姓名|身份证|投保人地址|缴费电话|邮编
    if ( TradeContext.existVariable( "UserName" ) ):
        TradeContext.note9 = TradeContext.note9 + TradeContext.UserName.strip()
    TradeContext.note9 = TradeContext.note9 + "|"

    if ( TradeContext.existVariable( "TGovtID" ) ):
        TradeContext.note9 = TradeContext.note9 + TradeContext.TGovtID.strip()
    TradeContext.note9 = TradeContext.note9 + "|"

    if ( TradeContext.existVariable( "line1" ) ):
        TradeContext.note9 = TradeContext.note9 + TradeContext.line1.strip()
    TradeContext.note9 = TradeContext.note9 + "|"

    if ( TradeContext.existVariable( "DialNumber" ) ):
        TradeContext.note9 = TradeContext.note9 + TradeContext.DialNumber.strip()
    TradeContext.note9 = TradeContext.note9 + "|"

    #if ( TradeContext.existVariable( "Zip" ) ):
    #    TradeContext.note9 = TradeContext.note9 + TradeContext.Zip.strip()

    #与被保人关系名称|被保人名称|被保人身份证
    if ( TradeContext.existVariable( "RelationShip" ) ):
        TradeContext.note10 = TradeContext.note10 + TradeContext.RelationShip.strip() 
    TradeContext.note10 = TradeContext.note10 + "|"

    if ( TradeContext.existVariable( "UserNameB" ) ):
        TradeContext.note10 = TradeContext.note10 + TradeContext.UserNameB.strip()
    TradeContext.note10 = TradeContext.note10 + "|"

    if ( TradeContext.existVariable( "GovtIDB" ) ):
        TradeContext.note10 = TradeContext.note10 + TradeContext.GovtIDB.strip()
    
    #AfaLoggerFunc.tradeInfo( 'TradeContext.note8 = [' + str(TradeContext.note8) + ']')
    #AfaLoggerFunc.tradeInfo( 'TradeContext.note9 = [' + str(TradeContext.note9) + ']')
    #AfaLoggerFunc.tradeInfo( 'TradeContext.note10 = [' + str(TradeContext.note10) + ']')

    if ( len(str(TradeContext.note2.strip())) > 0):
        sqlupdate = sqlupdate + ",note2 = '"+TradeContext.note2+"' "
    if ( len(str(TradeContext.note3.strip())) > 0):
        sqlupdate = sqlupdate + ",note3 = '"+TradeContext.note3+"' "
    if ( len(str(TradeContext.note4.strip())) > 0):
        sqlupdate = sqlupdate + ",note4 = '"+TradeContext.note4+"' "
    if ( len(str(TradeContext.note6.strip())) > 0):
        sqlupdate = sqlupdate + ",note6 = '"+TradeContext.note6+"' "
    if ( len(str(TradeContext.note7.strip())) > 0):
        sqlupdate = sqlupdate + ",note7 = '"+TradeContext.note7+"' "
    if ( len(str(TradeContext.note8.strip())) > 0):
        sqlupdate = sqlupdate + ",note8 = '"+TradeContext.note8+"' "
    if ( len(str(TradeContext.note9.strip())) > 0):
        sqlupdate = sqlupdate + ",note9 = '"+TradeContext.note9+"' "
    if ( len(str(TradeContext.note10.strip())) > 0):
        sqlupdate = sqlupdate + ",note10 = '"+TradeContext.note10+"' "
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
################################################################################
# 函 数 名: AdbInsertQueDtl
# 功能说明: 安贷宝 新保试算交易登记流水
# 修改记录：
# 返回值：    True  插入流水表成功    False 插入流水表失败
# 函数说明：  将流水信息插入流水表
################################################################################
def AdbInsertQueDtl( ):
    AfaLoggerFunc.tradeInfo( '>>>>>>>开始插入安贷宝信息表: [ afa_adbinfo ]<<<<<<<')
    
    #流水表的列数-1
    count=39
    TransDtl=[[]]*( count+1 )
    TransDtl[0] = TradeContext.agentSerialno                    # AGENTSERIALNO 代理业务流水号
    TransDtl[1] = TradeContext.sysId                            # SYSID         系统标识
    TransDtl[2] = TradeContext.workDate                         # WORKDATE      交易日期
    TransDtl[3] = TradeContext.workTime                         # WORKTIME      交易时间
    TransDtl[4] = TradeContext.brno                             # BRNO          网点号
    TransDtl[5] = TradeContext.tellerno                         # TELLERNO      柜员号
    
    if( TradeContext.existVariable( "IdType" ) ) :
        TransDtl[6] = TradeContext.IdType                       # IdType        证件类型
    else:
        TransDtl[6] = ''
    
    TransDtl[7]= TradeContext.IdCode                            # IdCode        证件号码
    TransDtl[8]= TradeContext.UserNo                            # UserNo        保单号/用户编号
    TransDtl[9]= TradeContext.UserName                          # UserName      用户名称
    
    if( TradeContext.existVariable( "TelePhone" ) ) :
        TransDtl[10] = TradeContext.TelePhone                   # TelePhone     电话号码
    else:
        TransDtl[10] = ''
    
    if( TradeContext.existVariable( "Address" ) ) :
        TransDtl[11] = TradeContext.Address                     # Address        地址
    else:
        TransDtl[11] = ''
    
    if( TradeContext.existVariable( "ZipCode" ) ) :
        TransDtl[12] = TradeContext.ZipCode                     # ZipCode        邮编
    else:
        TransDtl[12] = ''
    
    if( TradeContext.existVariable( "Email" ) ) :
        TransDtl[13] = TradeContext.Email                        # Email        邮件地址
    else:
        TransDtl[13] = ''
    
    if( TradeContext.existVariable( "ProCode" ) ) :
        # ProCode =1 --------ProCodeStr = EL5602
        # ProCode =0 --------ProCodeStr = EL5601
        TransDtl[14] = TradeContext.ProCode                     # ProCode        险种代码
    else:
        TransDtl[14] = ''
    
    if( TradeContext.existVariable( "SubmisDate" ) ) :
        TransDtl[15] = TradeContext.SubmisDate                  # SubmisDate        投保日期
    else:
        TransDtl[15] = ''
    
    if( TradeContext.existVariable( "IntialNum" ) ) :
        TransDtl[16] = TradeContext.IntialNum                   # IntialNum        投保份数
    else:
        TransDtl[16] = ''
    
    TransDtl[17] = TradeContext.EffDate                         # EffDate      责任起始日期
    TransDtl[18] = TradeContext.TermDate                        # TermDate     责任结束日期
    TransDtl[19] = TradeContext.LoanDate                        # LoanDate     借款日期
    TransDtl[20] = TradeContext.LoanEndDate                     # LoanEndDate  借款到期日

    if( TradeContext.existVariable( "LoanContractNo" ) ) :
        TransDtl[21] = TradeContext.LoanContractNo                  # CreBarNo     贷款合同编号
    else:
        TransDtl[21] = ''

    if( TradeContext.existVariable( "LoanInvoiceNo" ) ) :
        TransDtl[22] = TradeContext.LoanInvoiceNo                   # CreVouNo     贷款凭证编号
    else:
        TransDtl[22] = ''
    
    if( TradeContext.existVariable( "PayoutDur" ) ) :
        TransDtl[23] = TradeContext.PayoutDur                   # PayoutDur        缴费年限
    else:
        TransDtl[23] = ''
    
    if( TradeContext.existVariable( "BenficName1" ) ) :
        TransDtl[24] = TradeContext.BenficName1                 # BenficName1      第一受益人名称
    else:
        TransDtl[24] = ''
    
    if( TradeContext.existVariable( "BenficType" ) ) :
        TransDtl[25] = TradeContext.BenficType                  # BenficType        第二受益人类型
    else:
        TransDtl[25] = ''
    
    if( TradeContext.existVariable( "BenficName2" ) ) :
        TransDtl[26] = TradeContext.BenficName2                 # BenficName2        指定受益人姓名
    else:
        TransDtl[26] = ''
    
    TransDtl[27] =  TradeContext.CpicTeller.strip()             # CPICTELLER        太保业务员号码(交易成功后返回 更新)
    
    if( TradeContext.errorCode.strip() == "0000"):
        TradeContext.DTLSTATUS = "0"
    else:
        TradeContext.DTLSTATUS = "1"
    TransDtl[28] = TradeContext.DTLSTATUS                       # DTLSTATUS        交易状态(交易成功后更新为"0")
    
    if( TradeContext.existVariable( "PaymentAmt" ) ) :
        TradeContext.AMOUNT = TradeContext.PaymentAmt
    else:
        TradeContext.AMOUNT = ''
    TransDtl[29] = TradeContext.AMOUNT                          # AMOUNT        保费金额(交易成功后返回 更新)
    
    if( TradeContext.existVariable( "GovtIDB" ) ) :
        TransDtl[30] = TradeContext.GovtIDB                     # IdCodeB        被保人证件号码(交易成功后返回 更新)
    else:
        TransDtl[30] = ''
    
    if( TradeContext.existVariable( "FullNameB" ) ) :
        TransDtl[31] = TradeContext.FullNameB                   # UserNameB        被保人姓名 (交易成功后返回 更新)
    else:
        TransDtl[31] = ''
    
    if( TradeContext.existVariable( "PolNumber" ) ):            # NOTE1         备注1(保险公司返回的保单号)
        TransDtl[32] = TradeContext.PolNumber
    else:
        TransDtl[32] = ''
    if( TradeContext.existVariable( "ProCode" ) ):              # NOTE2         备注2(保险种类)
        TransDtl[33] = TradeContext.ProCode
    else:
        TransDtl[33] = ''
    if( TradeContext.existVariable( "unitno" ) ):                # NOTE3         备注3(单位编码)
        TransDtl[34] = TradeContext.unitno
    else:
        TransDtl[34] = ''
    if( TradeContext.existVariable( "note4" ) ):                # NOTE4         备注4
        TransDtl[35] = TradeContext.note4
    else:
        TransDtl[35] = ''
    if( TradeContext.existVariable( "note5" ) ):                # NOTE5         备注5
        TransDtl[36] = TradeContext.note5
    else:
        TransDtl[36] = ''
    if( TradeContext.existVariable( "note6" ) ):                # NOT6         备注6
        TransDtl[37] = TradeContext.note6
    else:
        TransDtl[37] = ''
    if( TradeContext.existVariable( "note7" ) ):                # NOTE7         备注7
        TransDtl[38] = TradeContext.note7
    else:
        TransDtl[38] = ''
    if( TradeContext.existVariable( "errorMsg" ) ):                # NOTE8         备注8
        TransDtl[39] = TradeContext.errorMsg
    else:
        TransDtl[39] = ''
    sql = "INSERT INTO AFA_ADBINFO ("
    sql = sql + "AGENTSERIALNO,SYSID,WORKDATE,WORKTIME,BRNO,TELLERNO,IDTYPE,IDCODE,USERNO,USERNAME,TELEPHONE,"
    sql = sql + "ADDRESS,ZIPCODE,EMAIL,PROCODE,SUBMISDATE,INTIALNUM,EFFDATE,TERMDATE,LOANDATE,LOANENDDATE,CREBARNO,"
    sql = sql + "CREVOUNO,PAYOUTDUR,BENFICNAME1,BENFICTYPE,BENFICNAME2,CPICTELLER,DTLSTATUS,AMOUNT,IDCODEB,USERNAMEB,"
    sql = sql + "NOTE1,NOTE2,NOTE3,NOTE4,NOTE5,NOTE6,NOTE7,NOTE8) VALUES("
    
    i=0
    for i in range( 0, count ):
        if( type( TransDtl[i] ) is int ):
            sql=sql+str( TransDtl[i] )+","
        else:
            sql=sql+"'"+ TransDtl[i]+"',"
    
    sql=sql+"'"+TransDtl[count]+"')"
    
    AfaLoggerFunc.tradeInfo( '>>>>>>>新保试算交易登记流水<<<<<<< ' + str(sql))
    
    result=AfaDBFunc.InsertSqlCmt( sql )
        
    if( result < 1 ):
        TradeContext.errorCode, TradeContext.errorMsg='A0044', '插入流水主表失败'+AfaDBFunc.sqlErrMsg
        return False
    else:
        return True
################################################################################
# 函 数 名: ADBUpdateQueDtl
# 功能说明: 新保试算成功返回更新交易成功标识和试算金额
# 修改记录: 
# 备    注: 
# 范    例: 
###############################################################################
def ADBUpdateQueDtl( ):
    sqlupdate = ""
    AfaLoggerFunc.tradeInfo( '>>>>>>>新报试算更新原交易流水<<<<<<<')
    sqlupdate = sqlupdate + "update afa_adbinfo set "
    sqlupdate = sqlupdate + " note8 = '"+TradeContext.errorMsg.strip()+"' "
    if( TradeContext.errorCode.strip() == "0000"):
        sqlupdate = sqlupdate + ", dtlstatus = '0' "
        sqlupdate = sqlupdate + ", amount = '"+TradeContext.PaymentAmt.strip()+"' "
    #太保业务员号码
    if( TradeContext.existVariable( "CpicTeller" ) and len(TradeContext.CpicTeller.strip()) > 0):
        sqlupdate = sqlupdate + ", CpicTeller = '"+TradeContext.CpicTeller.strip()+"'"
    #被保人姓名
    if( TradeContext.existVariable( "FullNameB" ) and len(TradeContext.FullNameB.strip()) > 0):
        sqlupdate = sqlupdate + ", UserNameB = '"+TradeContext.FullNameB.strip()+"'"
    #被保人证件号码
    if( TradeContext.existVariable( "GovtIDB" ) and len(TradeContext.GovtIDB.strip()) > 0):
        sqlupdate = sqlupdate + ", IdCodeB = '"+TradeContext.GovtIDB.strip()+"'"
    sqlupdate = sqlupdate + " where sysid = '"+TradeContext.sysId+"' and agentserialno = '"+TradeContext.agentSerialno+"'"
    AfaLoggerFunc.tradeInfo( 'sqlupdate = ' + str(sqlupdate))
    record=AfaDBFunc.UpdateSqlCmt( sqlupdate )
    if( record > 0 ):
        AfaLoggerFunc.tradeInfo( '>>>>>>>更新新报试算原交易流水成功<<<<<<<')
        return True
    if( record == 0 ):
        AfaLoggerFunc.tradeInfo( '>>>>>>>更新新报试算原交易流水失败<<<<<<<')
        TradeContext.errorCode,TradeContext.errorMsg='A0100','未发现原始交易'
        return False
    else :
        AfaLoggerFunc.tradeInfo( '>>>>>>>更新新报试算原交易流水失败<<<<<<<')
        TradeContext.errorCode, TradeContext.errorMsg='A0100', '更新原交易状态失败' + AfaDBFunc.sqlErrMsg
        return False

################################################################################
# 函 数 名: ADBCheckCert
# 功能说明: 检查凭证种类与保险公司是否对应
# 修改记录: 20091120  蔡永贵  增加
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
# 函 数 名: ADBGetInfoByUnitno
# 功能说明: 获取保险公司相关信息
# 修改记录: 1. 关彬捷 2009-11-24 创建
# 备    注:
# 范    例:
###############################################################################
def ADBGetInfoByUnitno():
    AfaLoggerFunc.tradeInfo( '>>>>获取保险公司相关信息<<<<' )
    AfaLoggerFunc.tradeInfo("保险公司代码[" + TradeContext.unitno + "]")
    #初始化险种代码和险种名称
    TradeContext.ProCodeStr = ''
    TradeContext.PlanName   = ''
    sql = ""
    sql = "select NOTE2 from afa_unitadm where sysid = '" + TradeContext.sysId + "' and unitno = '" + TradeContext.unitno + "'"
    record = AfaDBFunc.SelectSql( sql )
    if ( record == None ):
        AfaLoggerFunc.tradeInfo( '>>>>获取保险公司相关信息异常<<<<' )
        TradeContext.errorCode,TradeContext.errorMsg='A0100','获取保险公司相关信息异常'
        return False

    if ( len(record) <= 0):
        AfaLoggerFunc.tradeInfo( '>>>>未查到相关保险公司信息<<<<' )
        TradeContext.errorCode,TradeContext.errorMsg='A0100','未查到相关保险公司信息'
        return False

    else:
        tmplist = record[0][0].split("|")
        if len(tmplist) < 2:
            AfaLoggerFunc.tradeInfo(">>>>保险公司配置信息非法<<<<")
            TradeContext.errorCode,TradeContext.errorMsg='A0100','保险公司配置信息非法'
            return False

        TradeContext.ProCodeStr = tmplist[0]
        TradeContext.PlanName = tmplist[1]

        AfaLoggerFunc.tradeInfo( '>>>>数据库配置险种代码[' + TradeContext.ProCodeStr + ']' )
        AfaLoggerFunc.tradeInfo( '>>>>数据库配置险种名称[' + TradeContext.PlanName + ']' )

        return True
