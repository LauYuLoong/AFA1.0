# -*- coding: gbk -*-
###############################################################################
# Copyright (c) 2006,北京赞同科技发展有限公司.第三事业部
# All rights reserved.
#
# 文件名称：TTPS001_8456.py
# 文件标识：
# 摘    要：财税库行.补打电子缴税付款凭证
# 当前版本：1.0
# 作    者：
# 完成日期：2008年12月05日
#
# 取代版本：
# 原 作 者：liyj
# 完成日期：
###############################################################################
import TradeContext, TipsFunc, AfaDBFunc,AfaLoggerFunc,os
#import TipsHostFunc,HostContext，LoggerHandler, UtilTools, ConfigParser

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo( '进入补打电子缴税付款凭证[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    
    #============变量值的有效性校验============
    AfaLoggerFunc.tradeInfo(">>>变量值的有效性校验")
    if( not TradeContext.existVariable( "taxPayCode" ) ):
        return TipsFunc.ExitThisFlow( 'A0001', '纳税人编码[taxPayCode]值不存在!' )
    if( not TradeContext.existVariable( "taxOrgCode" ) ):
        return TipsFunc.ExitThisFlow( 'A0001', '征收机关代码[taxOrgCode]值不存在!' )
    if( not TradeContext.existVariable( "payAcct" ) ):
        return TipsFunc.ExitThisFlow( 'A0001', '付款人账号[payAcct]值不存在!' )
    if( not TradeContext.existVariable( "protocolNo" ) ):
        return TipsFunc.ExitThisFlow( 'A0001', '三方协议号[protocolNo]值不存在!' )
    if( not TradeContext.existVariable( "serialNo" ) ):
        return TipsFunc.ExitThisFlow( 'A0001', '交易流水号[serialNo]值不存在!' )
    if( not TradeContext.existVariable( "workDate" ) ):
        return TipsFunc.ExitThisFlow( 'A0001', '交易日期[workDate]值不存在!' )
        
    

    #================获取帐务流水信息===============
    AfaLoggerFunc.tradeInfo(">>>获取帐务流水信息")
    sqlStr =''
    
    #begin 20101130 蔡永贵修改
    #sqlStr = "SELECT t.SERIALNO,t.WORKDATE,t.CORPSERNO,t.AMOUNT,t.TAXVOUNO,t1.payacct,t1.taxorgcode,t1.taxpaycode,t1.protocolno"
    sqlStr = "SELECT t.SERIALNO,t.WORKDATE,t.CORPSERNO,t.AMOUNT,t.TAXVOUNO,t1.payacct,t1.taxorgcode,t1.taxpaycode,t1.protocolno,t.note10"
    #end
    
    sqlStr = sqlStr + " FROM TIPS_MAINTRANSDTL t,tips_custinfo t1 WHERE "
    sqlStr = sqlStr + " t.SERIALNO ='"        + TradeContext.serialNo    +"'"
    sqlStr = sqlStr + " AND t.WORKDATE ='" + TradeContext.workDate +"'"
    ###################################################################################
    #guanbj 20091105 tips与maps对账完成后即可打印凭证
    #sqlStr = sqlStr + " AND t.CHKFLAG='0' and t.taxpaycode=t1.taxpaycode "
    sqlStr = sqlStr + " AND t.CORPCHKFLAG='0' and t.taxpaycode=t1.taxpaycode "
    ###################################################################################
    #begin 20101102 蔡永贵 增加查询条件，保证查询结果唯一
    sqlStr = sqlStr + " AND t.DRACCNO = t1.PAYACCT"
    sqlStr = sqlStr + " AND t1.status = '1' "
    #end
    AfaLoggerFunc.tradeInfo(sqlStr)     
    records = AfaDBFunc.SelectSql( sqlStr )
    if( records == None or records <0):
        return TipsFunc.ExitThisFlow( '0027', '表操作异常:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return TipsFunc.ExitThisFlow( '0028', '没有满足条件的数据' )
    else:
        AfaLoggerFunc.tradeInfo(records[0][0])
        
    TradeContext.tradeResponse.append(['traNo',records[0][2]])           #第三方流水
    TradeContext.tradeResponse.append(['amount',str(records[0][3])])     #金额
    TradeContext.tradeResponse.append(['taxVouhNo',records[0][4]])       #税票号码
    TradeContext.tradeResponse.append(['workDate',records[0][1]])        #交易日期
    
    #begin 20101130 蔡永贵增加
    TradeContext.tradeResponse.append(['BankName',records[0][9]])               #收款国库名称
    #end
    
    #===== add by liu.yl at 20110713 ====
    #===== 增加else判断，如果前台提交的数据不为空，判断是否与流水记录的信息匹配 ====
    #===== 信息不匹配，返回错误 ====
    if(len(TradeContext.payAcct)==0):
        TradeContext.payAcct=records[0][5]
    else:
        if(TradeContext.payAcct != records[0][5]):
            return TipsFunc.ExitThisFlow( '0028', '付款人账号与流水记录信息不匹配' )
        
        
    if(len(TradeContext.taxOrgCode)==0):
        TradeContext.taxOrgCode=records[0][6]
    else:
        if(TradeContext.taxOrgCode != records[0][6]):
            return TipsFunc.ExitThisFlow( '0028', '征收机关代码与流水记录信息不匹配' )
        
    if(len(TradeContext.taxPayCode)==0):
        TradeContext.taxPayCode=records[0][7]
    else:
        if(TradeContext.taxPayCode != records[0][7]):
            return TipsFunc.ExitThisFlow( '0028', '纳税人编码与流水记录信息不匹配' )
        
    if(len(TradeContext.protocolNo)==0):
        TradeContext.protocolNo=records[0][8]
    else:
        if(TradeContext.protocolNo != records[0][8]):
            return TipsFunc.ExitThisFlow( '0028', '三方协议号与流水记录信息不匹配' )
    #===== end of added ====
    
    
    #============获取三方协议信息=================
    AfaLoggerFunc.tradeInfo(">>>获取三方协议信息")
    sqlStr = ''
    sqlStr = sqlStr + "SELECT t1.taxPayCode,t1.HANDORGNAME,t1.payAcct,t1.taxPayName,t2.TAXORGNAME,t1.payOpBkCode,t3.TRENAME FROM TIPS_CUSTINFO t1,TIPS_TAXCODE t2,TIPS_LIQUIDATE_ADM t3"
    sqlStr = sqlStr + " where t1.PAYACCT = '" + TradeContext.payAcct + "'"
    sqlStr = sqlStr + " and t1.TAXORGCODE = '" + TradeContext.taxOrgCode + "'"
    sqlStr = sqlStr + " and t1.TAXPAYCODE = '" + TradeContext.taxPayCode + "'"
    sqlStr = sqlStr + " and t1.PROTOCOLNO = '" + TradeContext.protocolNo + "'"
    sqlStr = sqlStr + " and t1.taxOrgCode = t2.taxOrgCode and t1.NOTE2 = t3.PAYBKCODE"
    AfaLoggerFunc.tradeInfo(sqlStr)     
    records = AfaDBFunc.SelectSql( sqlStr )
    if( records == None ):
        return TipsFunc.ExitThisFlow( '0027', '表操作异常:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )== 0 ):
        return TipsFunc.ExitThisFlow( '0028', '没有满足条件的数据' )
    elif( len( records ) > 1 ):
        return TipsFunc.ExitThisFlow( '0028', '数据异常' )
    
    TradeContext.tradeResponse.append(['taxPayCode',records[0][1] + '  ' + records[0][0]])             #纳税人编码
    TradeContext.tradeResponse.append(['payAcct',records[0][2]])                #付款人帐号
    TradeContext.tradeResponse.append(['taxPayName',records[0][3]])             #付款人名称
    TradeContext.tradeResponse.append(['taxOrgName',records[0][4]])             #征收机关名称
    
    #begin 20101130 蔡永贵注释掉
    #TradeContext.tradeResponse.append(['BankName',records[0][6]])               #收款国库名称
    #end
    
    TradeContext.tradeResponse.append(['payOpBkName',TradeContext.brName])      #开户行名称
    if(TradeContext.brno != records[0][5]):
        return TipsFunc.ExitThisFlow( 'A0001', '非开户行' )
    
    
    
    
    #==========获取税种信息===========
    mx_file_name = os.environ['AFAP_HOME'] + '/tmp/' + 'AH_' + TradeContext.teller + '.txt'
    TradeContext.tradeResponse.append(['fileName',  'AH_' + TradeContext.teller + '.txt'])
    
    if (os.path.exists(mx_file_name) and os.path.isfile(mx_file_name)):
        #文件存在,先删除-再创建
        os.system("rm " + mx_file_name)
    
    sfp = open(mx_file_name, "w")
    AfaLoggerFunc.tradeInfo('明细文件=['+mx_file_name+']')
    
    sqlStrVou =''
    sqlStrVou = "SELECT TAXTYPENAME,TAXSTARTDATE,TAXENDDATE,TAXTYPEAMT,NOTE1"
    sqlStrVou = sqlStrVou + " FROM TIPS_VOU_TAXTYPE WHERE "
    sqlStrVou = sqlStrVou + " WORKDATE='"             + TradeContext.workDate    +"'"
    sqlStrVou = sqlStrVou + " AND SERIALNO='"         + TradeContext.serialNo   +"'"

    AfaLoggerFunc.tradeInfo(sqlStrVou)     
    recordsVou = AfaDBFunc.SelectSql( sqlStrVou )   
    if( recordsVou == None ):
        sfp.close()
        return TipsFunc.ExitThisFlow( '0027', '表操作异常:'+AfaDBFunc.sqlErrMsg )
    #begin 20101102 蔡永贵修改
    #elif( len(recordsVou) <0 ):
    #    sfp.close()
    #    return TipsFunc.ExitThisFlow( '0027', '表操作异常:'+AfaDBFunc.sqlErrMsg )
    elif( len(recordsVou) == 0 ):
        sfp.close()
        return TipsFunc.ExitThisFlow( '0027', '没有相关的税种信息' )
    #end
    else:
        for j in range(0,len(recordsVou)):
            A0 = str(recordsVou[j][0]).strip()
            A1 = str(recordsVou[j][1]).strip() + '-' + str(recordsVou[j][2]).strip()
            A2 = str(recordsVou[j][3]).strip()
        
            sfp.write(A0 +  '|'  +  A1 +  '|'  +  A2 +  '|' + '\n')
        
    sfp.close()
    
    TradeContext.tradeResponse.append(['printNo',str(int(recordsVou[0][4]) + 1)])                #打印次数
    
    #==============更改打印次数=====================
    AfaLoggerFunc.tradeInfo(">>>更改打印次数")
    sqlStr = ""
    sqlStr = "update TIPS_VOU_TAXTYPE set note1 = '" + str(int(recordsVou[0][4]) + 1) + "' where"
    sqlStr = sqlStr + " WORKDATE='"             + TradeContext.workDate    +"'"
    sqlStr = sqlStr + " AND SERIALNO='"         + TradeContext.serialNo   +"'"
    
    AfaLoggerFunc.tradeInfo(sqlStr)     
    res = AfaDBFunc.UpdateSqlCmt( sqlStr )   
    if( res == None ):
        return TipsFunc.ExitThisFlow( '0027', '表操作异常:'+AfaDBFunc.sqlErrMsg )
    elif( res <0 ):
        return TipsFunc.ExitThisFlow( '0027', '表操作异常:'+AfaDBFunc.sqlErrMsg )
    
    TradeContext.tradeResponse.append(['errorCode','0000'])
    TradeContext.tradeResponse.append(['errorMsg','交易成功'])
            
    AfaLoggerFunc.tradeInfo( '退出补打电子缴税付款凭证[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    return True

 
