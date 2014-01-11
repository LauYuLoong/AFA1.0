# -*- coding: gbk -*-
################################################################################
#   批量业务系统：查询企业协议
#===============================================================================
#   交易文件:   T001000_8429.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  胡友
#   修改时间:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc,NGSFAbdtFunc,AfaFlowControl
from types import *

#=====================查询企业信息==============================================
def TrxMain( ):
    AfaLoggerFunc.tradeInfo('**********查询企业信息(8429)开始**********')
    
    flag = ( TradeContext.existVariable( "Protocolno" ) and  len(TradeContext.Protocolno) != 0 ) or ( TradeContext.existVariable( "BusiUserno" ) and  len(TradeContext.BusiUserno) != 0 ) or ( TradeContext.existVariable( "BankUserno" ) and  len(TradeContext.BankUserno) != 0 )
    
    #8429做单位查询
    if( ( TradeContext.existVariable( "PayerAccno" ) and len(TradeContext.PayerAccno) == 0 ) and (not flag) ):
        AfaLoggerFunc.tradeInfo('8429做单位查询>>>>>>>>>>>')
        
        if( not TradeContext.existVariable( "Appno" ) or (TradeContext.existVariable( "Appno" ) and len(TradeContext.Appno) == 0) ):
            return AfaFlowControl.ExitThisFlow( 'A010', '业务编号[Appno]值不存在!' )
        if( not TradeContext.existVariable( "PayeeUnitno" ) or (TradeContext.existVariable( "PayeeUnitno" ) and len(TradeContext.PayeeUnitno) == 0) ):
            return AfaFlowControl.ExitThisFlow( 'A010', '单位编号[PayeeUnitno]值不存在!' )
                
        sql = ""
        sql = sql + "select * from abdt_unitInfo"
        sql = sql + " where appno = '"  +TradeContext.Appno       +"'"
        sql = sql + " and busino  = '"  +TradeContext.PayeeUnitno +"'"
        
        AfaLoggerFunc.tradeInfo('8429做单位查询sql='+sql)
        record = AfaDBFunc.SelectSql(sql)
        
        if(record==None):
            TradeContext.errorCode,TradeContext.errorMsg = "A010" ,"数据库异常"
            return False
        
        if(len(record)==0):
            TradeContext.errorCode,TradeContext.errorMsg = "A010" ,"没有该单位信息"    
            return False
        
        #收费单位账户,收费单位名称
        AfaLoggerFunc.tradeInfo('8429做单位查询结果'+record[0][0].strip())
        TradeContext.tradeResponse.append(['PayeeAccno',record[0][6].strip()])
        TradeContext.tradeResponse.append(['PayeeName',record[0][12].strip()])
        
        AfaLoggerFunc.tradeInfo('**********查询企业信息(8429)结束**********')
        
        #返回
        TradeContext.tradeResponse.append(['errorCode','0000'])
        TradeContext.tradeResponse.append(['errorMsg','交易成功'])
        return True
        
    #8429做账户查询
    if( (TradeContext.existVariable( "PayerAccno" ) and len(TradeContext.PayerAccno) > 0) and (not flag) ):
        AfaLoggerFunc.tradeInfo('8429做账户查询>>>>>>>>>>>')
        
        #调用8810查询该账户的名称
        NGSFAbdtFunc.QueryAccInfo()
        
        if TradeContext.errorCode !='0000':
            AfaLoggerFunc.tradeInfo('8810主机账户查询失败')
            return False
            
        AfaLoggerFunc.tradeInfo('8810主机账户查询成功'+TradeContext.USERNAME)
        TradeContext.PayerName = TradeContext.USERNAME
        TradeContext.tradeResponse.append(['PayerName',TradeContext.PayerName])
        
        AfaLoggerFunc.tradeInfo('**********查询企业信息(8429)结束**********')
       
        #返回
        TradeContext.tradeResponse.append(['errorCode', '0000'])
        TradeContext.tradeResponse.append(['errorMsg',  '交易成功'])
        return True
    
    #8429做企业查询
    if( flag ):        
        AfaLoggerFunc.tradeInfo('8429做企业查询>>>>>>>>>>>')
        
        if( not TradeContext.existVariable( "Appno" ) or (TradeContext.existVariable( "Appno" ) and len(TradeContext.Appno) == 0) ):
            return AfaFlowControl.ExitThisFlow( 'A010', '业务编号[Appno]值不存在!' )
        if( not TradeContext.existVariable( "PayeeUnitno" ) or (TradeContext.existVariable( "PayeeUnitno" ) and len(TradeContext.PayeeUnitno) == 0) ):
            return AfaFlowControl.ExitThisFlow( 'A010', '单位编号[PayeeUnitno]值不存在!' )
        
        #TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #工作日期
        #TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #工作时间
        
        #判断单位协议是否有效
        if ( not NGSFAbdtFunc.ChkUnitInfo( ) ):
            return False
        
        try:
            AfaLoggerFunc.tradeInfo('企业协议查询')
            
            sql = "SELECT * FROM ABDT_CUSTINFO WHERE "
            sql = sql + "STATUS="                 + "'" + "1"                          + "'"            #状态(0:异常,1:正常)
            
            if ( len(TradeContext.Appno) > 0 ):
                sql = sql + " AND APPNO="         + "'" + TradeContext.Appno           + "'"            #业务编号
            if ( len(TradeContext.PayeeUnitno) > 0 ):
                sql = sql + " AND BUSINO="        + "'" + TradeContext.PayeeUnitno     + "'"          #单位编号
            
            if( TradeContext.existVariable( "Protocolno" ) and len( TradeContext.Protocolno ) != 0 ):
                sql = sql + " and Protocolno = '"+ TradeContext.Protocolno +"'"
            if( TradeContext.existVariable( "BusiUserno" ) and len( TradeContext.BusiUserno ) != 0 ):
                sql = sql + " and BusiUserno = '"+ TradeContext.BusiUserno +"'"
            if( TradeContext.existVariable( "BankUserno" ) and len( TradeContext.BankUserno ) != 0 ):
                sql = sql + " and Accno = '"+ TradeContext.BankUserno +"'"
       
            AfaLoggerFunc.tradeInfo( '企业协议查询'+sql )
            records = AfaDBFunc.SelectSql( sql )
            
            if ( records == None ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return ExitSubTrade( '9000', '查询企业协议信息异常' )
        
            if ( len(records) == 0 ):
                return ExitSubTrade( '9000', '没有相关的企业协议信息')
       
            AfaLoggerFunc.tradeInfo(">>>总共查询[" + str(len(records)) + "]条记录")
            AfaUtilTools.ListFilterNone( records )
                
            TradeContext.tradeResponse.append(['Appno',             str(records[0][0])])    #业务编号
            TradeContext.tradeResponse.append(['PayeeUnitno',       str(records[0][1])])    #单位编号
            TradeContext.tradeResponse.append(['PayerUnitno',       str(records[0][2])])    #用户编号
            
            #TradeContext.tradeResponse.append(['O1VOUHTYPE',        str(records[0][5])])    #凭证类型
            #TradeContext.tradeResponse.append(['O1VOUHNO',          str(records[0][6])])    #凭证号
            
            TradeContext.tradeResponse.append(['PayerAccno',        str(records[0][7])])    #活期存款帐号
            
            #TradeContext.tradeResponse.append(['O1SUBACCNO',        str(records[0][8])])    #子帐号
            #TradeContext.tradeResponse.append(['O1CURRTYPE',        str(records[0][9])])    #币种
            #TradeContext.tradeResponse.append(['O1LIMITAMT',        str(records[0][10])])   #交易限额
            
            TradeContext.tradeResponse.append(['PartFlag',          str(records[0][11])])   #部分扣款标志
            TradeContext.tradeResponse.append(['Protocolno',        str(records[0][12])])   #协议编号
            TradeContext.tradeResponse.append(['ContractDate',      str(records[0][13])])   #签约日期(合同日期)
            TradeContext.tradeResponse.append(['StartDate',         str(records[0][14])])   #生效日期
            TradeContext.tradeResponse.append(['EndDate',           str(records[0][15])])   #失效日期
            
            #TradeContext.tradeResponse.append(['O1PASSCHKFLAG',     str(records[0][16])])   #密码验证标志
            #TradeContext.tradeResponse.append(['O1PASSWD',          str(records[0][17])])   #密码
            #TradeContext.tradeResponse.append(['O1IDCHKFLAG',       str(records[0][18])])   #证件验证标志
            #TradeContext.tradeResponse.append(['O1IDTYPE',          str(records[0][19])])   #证件类型
            #TradeContext.tradeResponse.append(['O1IDCODE',          str(records[0][20])])   #证件号码
            #TradeContext.tradeResponse.append(['O1NAMECHKFLAG',     str(records[0][21])])   #姓名验证标志
            
            TradeContext.tradeResponse.append(['PayerName',         str(records[0][22])])   #客户姓名
            TradeContext.tradeResponse.append(['Tel',               str(records[0][23])])   #联系电话
            TradeContext.tradeResponse.append(['Address',           str(records[0][24])])   #联系地址
            
            #TradeContext.tradeResponse.append(['O1ZIPCODE',         str(records[0][25])])   #邮编
            #TradeContext.tradeResponse.append(['O1EMAIL',           str(records[0][26])])   #电子邮箱
            #TradeContext.tradeResponse.append(['O1STATUS',          str(records[0][27])])   #状态
            #TradeContext.tradeResponse.append(['O1ZONENO',          str(records[0][28])])   #地区号
            
            TradeContext.tradeResponse.append(['InBrno',            str(records[0][29])])   #网点号(机构代码)
            TradeContext.tradeResponse.append(['InTellerno',        str(records[0][30])])   #柜员号
            TradeContext.tradeResponse.append(['InDate',            str(records[0][31])])   #录入日期
            TradeContext.tradeResponse.append(['InTime',            str(records[0][32])])   #录入时间
            #TradeContext.tradeResponse.append(['PayeeName',         str(records[0][33])])   #备注1
            TradeContext.tradeResponse.append(['UserName',          str(records[0][34])])   #联系人
            TradeContext.tradeResponse.append(['PayeeAccno',        str(records[0][35])])   #收费单位账户
            
            #TradeContext.tradeResponse.append(['O1NOTE4',           str(records[0][36])])   #备注4
            TradeContext.tradeResponse.append(['PayeeName',          str(records[0][37])])   #收费单位名称
       
            AfaLoggerFunc.tradeInfo('**********查询企业信息(8429)结束**********')
       
            #返回
            TradeContext.tradeResponse.append(['errorCode', '0000'])
            TradeContext.tradeResponse.append(['errorMsg',  '交易成功'])
            return True
            
        except Exception, e:
            AfaLoggerFunc.tradeFatal( str(e) )
            return ExitSubTrade( '9999', '查询企业协议信息异常')

def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False