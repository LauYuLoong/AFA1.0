# -*- coding: gbk -*-
################################################################################
#   批量业务系统：查询个人协议
#===============================================================================
#   交易文件:   T001000_8405.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  XZH
#   修改时间:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc,AbdtFunc
from types import *


#=====================查询个人信息==============================================
def TrxMain( ):


    AfaLoggerFunc.tradeInfo('**********查询个人信息(8405)开始**********')


    TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #工作日期
    TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #工作时间



    #判断单位协议是否有效
    if ( not AbdtFunc.ChkUnitInfo( ) ):
        return False


    try:
        sql = "SELECT * FROM ABDT_CUSTINFO WHERE "
        
        sql = sql + "STATUS="                 + "'" + "1"                          + "'"            #状态(0:异常,1:正常)

        #协议编号
        if ( len(TradeContext.I1PROTOCOLNO) > 0 ):
            sql = sql + " AND PROTOCOLNO="    + "'" + TradeContext.I1PROTOCOLNO    + "'"            #协议编号

        #业务编号
        if ( len(TradeContext.I1APPNO) > 0 ):
            sql = sql + " AND APPNO="         + "'" + TradeContext.I1APPNO         + "'"            #业务编号

        #单位编号
        if ( len(TradeContext.I1BUSINO) > 0 ):
            sql = sql + " AND BUSINO="        + "'" + TradeContext.I1BUSINO        + "'"            #单位编号

        #商户客户编号
        if ( len(TradeContext.I1BUSIUSERNO) > 0 ):
            sql = sql + " AND BUSIUSERNO="    + "'" + TradeContext.I1BUSIUSERNO    + "'"            #商户客户编号

#       #商户客户应用编号
#       if ( len(TradeContext.I1BUSIUSERAPPNO) > 0 ):
#           sql = sql + " AND BUSIUSERAPPNO=" + "'" + TradeContext.I1BUSIUSERAPPNO + "'"            #商户客户应用编号

        #银行客户编号
        if ( len(TradeContext.I1BANKUSERNO) > 0 ):
            sql = sql + " AND BANKUSERNO="    + "'" + TradeContext.I1BANKUSERNO    + "'"            #银行客户编号

#       #凭证类型
#       if ( len(TradeContext.I1VOUHTYPE) > 0 ):
#           sql = sql + " AND VOUHTYPE="      + "'" + TradeContext.I1VOUHTYPE      + "'"            #凭证类型
#
#       #凭证号
#       if ( len(TradeContext.I1VOUHNO) > 0 ):
#           sql = sql + " AND VOUHNO="        + "'" + TradeContext.I1VOUHNO        + "'"            #凭证类型

        #银行帐号
        if ( len(TradeContext.I1ACCNO) > 0 ):
            sql = sql + " AND ACCNO="         + "'" + TradeContext.I1ACCNO         + "'"            #银行帐号

#       #子帐号
#       if ( len(TradeContext.I1SUBACCNO) > 0 ):
#           sql = sql + " AND SUBACCNO="      + "'" + TradeContext.I1SUBACCNO      + "'"            #子帐号
#
#       #币种
#       if ( len(TradeContext.I1CURRTYPE) > 0 ):
#           sql = sql + " AND CURRTYPE="      + "'" + TradeContext.I1CURRTYPE      + "'"            #币种
#
#       #证件号码
#       if ( len(TradeContext.I1IDCODE) > 0 ):
#           sql = sql + " AND IDCODE="        + "'" + TradeContext.I1IDCODE        + "'"            #证件号码
#
#       #客户姓名
#       if ( len(TradeContext.I1USERNAME) > 0 ):
#           sql = sql + " AND USERNAME="      + "'" + TradeContext.I1USERNAME      + "'"            #客户姓名

        AfaLoggerFunc.tradeInfo( sql )

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '查询个人协议信息异常' )
    
        if ( len(records) == 0 ):
            return ExitSubTrade( '9000', '没有相关的个人协议信息')


        AfaLoggerFunc.tradeInfo(">>>总共查询[" + str(len(records)) + "]条记录")


        #打包记录数
        TradeContext.tradeResponse.append(['RECNUM',  str(len(records))])

        #过滤None
        AfaUtilTools.ListFilterNone( records )
            
        i = 0
        while ( i  < len(records) ):
            TradeContext.tradeResponse.append(['O1APPNO',           str(records[i][0])])    #业务编号
            TradeContext.tradeResponse.append(['O1BUSINO',          str(records[i][1])])    #单位编号
            TradeContext.tradeResponse.append(['O1BUSIUSERNO',      str(records[i][2])])    #商户客户编号
            TradeContext.tradeResponse.append(['O1BUSIUSERAPPNO',   str(records[i][3])])    #商户客户应用编号
            TradeContext.tradeResponse.append(['O1BANKUSERNO',      str(records[i][4])])    #银行客户编号
            TradeContext.tradeResponse.append(['O1VOUHTYPE',        str(records[i][5])])    #凭证类型
            TradeContext.tradeResponse.append(['O1VOUHNO',          str(records[i][6])])    #凭证号
            TradeContext.tradeResponse.append(['O1ACCNO',           str(records[i][7])])    #活期存款帐号
            TradeContext.tradeResponse.append(['O1SUBACCNO',        str(records[i][8])])    #子帐号
            TradeContext.tradeResponse.append(['O1CURRTYPE',        str(records[i][9])])    #币种
            TradeContext.tradeResponse.append(['O1LIMITAMT',        str(records[i][10])])   #交易限额
            TradeContext.tradeResponse.append(['O1PARTFLAG',        str(records[i][11])])   #部分扣款标志
            TradeContext.tradeResponse.append(['O1PROTOCOLNO',      str(records[i][12])])   #协议编号
            TradeContext.tradeResponse.append(['O1CONTRACTDATE',    str(records[i][13])])   #签约日期(合同日期)
            TradeContext.tradeResponse.append(['O1STARTDATE',       str(records[i][14])])   #生效日期
            TradeContext.tradeResponse.append(['O1ENDDATE',         str(records[i][15])])   #失效日期
            TradeContext.tradeResponse.append(['O1PASSCHKFLAG',     str(records[i][16])])   #密码验证标志
            TradeContext.tradeResponse.append(['O1PASSWD',          str(records[i][17])])   #密码
            TradeContext.tradeResponse.append(['O1IDCHKFLAG',       str(records[i][18])])   #证件验证标志
            TradeContext.tradeResponse.append(['O1IDTYPE',          str(records[i][19])])   #证件类型
            TradeContext.tradeResponse.append(['O1IDCODE',          str(records[i][20])])   #证件号码
            TradeContext.tradeResponse.append(['O1NAMECHKFLAG',     str(records[i][21])])   #姓名验证标志
            TradeContext.tradeResponse.append(['O1USERNAME',        str(records[i][22])])   #客户姓名
            TradeContext.tradeResponse.append(['O1TEL',             str(records[i][23])])   #联系电话
            TradeContext.tradeResponse.append(['O1ADDRESS',         str(records[i][24])])   #联系地址
            TradeContext.tradeResponse.append(['O1ZIPCODE',         str(records[i][25])])   #邮编
            TradeContext.tradeResponse.append(['O1EMAIL',           str(records[i][26])])   #电子邮箱
            TradeContext.tradeResponse.append(['O1STATUS',          str(records[i][27])])   #状态
            TradeContext.tradeResponse.append(['O1ZONENO',          str(records[i][28])])   #地区号
            TradeContext.tradeResponse.append(['O1BRNO',            str(records[i][29])])   #网点号(机构代码)
            TradeContext.tradeResponse.append(['O1TELLERNO',        str(records[i][30])])   #柜员号
            TradeContext.tradeResponse.append(['O1INDATE',          str(records[i][31])])   #录入日期
            TradeContext.tradeResponse.append(['O1INTIME',          str(records[i][32])])   #录入时间
            TradeContext.tradeResponse.append(['O1NOTE1',           str(records[i][33])])   #备注1
            TradeContext.tradeResponse.append(['O1NOTE2',           str(records[i][34])])   #备注2
            TradeContext.tradeResponse.append(['O1NOTE3',           str(records[i][35])])   #备注3
            TradeContext.tradeResponse.append(['O1NOTE4',           str(records[i][36])])   #备注4
            TradeContext.tradeResponse.append(['O1NOTE5',           str(records[i][37])])   #备注5
            i = i + 1


        AfaLoggerFunc.tradeInfo('**********查询个人信息(8405)结束**********')


        #返回
        TradeContext.tradeResponse.append(['errorCode', '0000'])
        TradeContext.tradeResponse.append(['errorMsg',  '交易成功'])
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '查询个人协议信息异常')




def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
        