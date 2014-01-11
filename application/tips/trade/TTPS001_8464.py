# -*- coding: gbk -*-
###############################################################################
# Copyright (c) 2006,北京赞同科技发展有限公司.第三事业部
# All rights reserved.
#
# 文件名称：TTPS001_8464.py
# 文件标识：
# 摘    要：财税库行.查询公共数据
#
# 当前版本：1.0
# 作    者：liyj
# 完成日期：2008年12月05日
#
# 取代版本：
# 原 作 者：
# 完成日期：
###############################################################################
import TradeContext, AfaFlowControl, AfaDBFunc,AfaLoggerFunc,os
#LoggerHandler, UtilTools, UtilTools
def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo( '进入查询交易明细['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']'  )

    AfaLoggerFunc.tradeInfo('数据类型为：'+TradeContext.dataType)
    if(TradeContext.dataType=="0"):
        sqlStr=" WHERE status='0' "
        sqlStr=sqlStr+" AND TaxOrgCode like '%"+ TradeContext.code +"%'"
        sqlStr=sqlStr+" AND TaxOrgName like '%"+ TradeContext.name +"%'"
        #if( TradeContext.existVariable( "dataCode" ) ):
        #    if len(TradeContext.dataCode)>0:
        #        sqlStr=sqlStr+" AND TaxOrgCode like '%"+ TradeContext.dataCode +"%'"
        #if( TradeContext.existVariable( "dataName" ) ):
        #    if len(TradeContext.dataName)>0:
        #        sqlStr=sqlStr+" AND TaxOrgName like '%"+ TradeContext.dataName +"%'"

        sqlStr_detail="SELECT TAXORGCODE,TAXORGNAME,TAXORGTYPE,UPTRECODE,OFPROVORG,"
        sqlStr_detail=sqlStr_detail+"OFCITYORG,OFCOUNTYORG,ADDRESS,PEOPLENAME,PEOPLEPHONE,POSTALCODE,STATUS,EFFECTDATE FROM TIPS_TAXCODE "
        sqlStr_detail=sqlStr_detail+sqlStr
        AfaLoggerFunc.tradeInfo(sqlStr_detail)     
        records = AfaDBFunc.SelectSql( sqlStr_detail )
        if( records == None ):
            return AfaFlowControl.ExitThisFlow( '0027', '表操作异常:'+AfaDBFunc.sqlErrMsg )
        elif( len( records )==0 ):
            return AfaFlowControl.ExitThisFlow( '0028', '没有满足条件的数据' )
        
        mx_file_name = os.environ['AFAP_HOME'] + '/tmp/' + 'AH_' + TradeContext.teller + '.txt'
        TradeContext.tradeResponse.append(['fileName',  'AH_' + TradeContext.teller + '.txt'])
    
        if (os.path.exists(mx_file_name) and os.path.isfile(mx_file_name)):
            #文件存在,先删除-再创建
            os.system("rm " + mx_file_name)
    
        sfp = open(mx_file_name, "w")
        AfaLoggerFunc.tradeInfo('明细文件=['+mx_file_name+']')
    
        i = 0
        while ( i  < len(records) ):
            lineStr = ''
            lineStr = lineStr + str(records[i][0]).strip() + '|'        
            lineStr = lineStr + str(records[i][1]).strip() + '|'       
            lineStr = lineStr + str(records[i][2]).strip() + '|'      
            lineStr = lineStr + str(records[i][3]).strip() + '|'       
            lineStr = lineStr + str(records[i][4]).strip() + '|'       
            lineStr = lineStr + str(records[i][5]).strip() + '|'       
            lineStr = lineStr + str(records[i][6]).strip() + '|'        
            lineStr = lineStr + str(records[i][7]).strip() + '|'       
            lineStr = lineStr + str(records[i][8]).strip() + '|'        
            lineStr = lineStr + str(records[i][9]).strip() + '|'       
            lineStr = lineStr + str(records[i][10]).strip() + '|'        
            lineStr = lineStr + str(records[i][11]).strip() + '|'       
            lineStr = lineStr + str(records[i][12]).strip() + '|'        
    
            sfp.write(lineStr  +  '\n')
    
            i=i+1
    
        sfp.close()
    if(TradeContext.dataType=="1"): #银行代码
        sqlStr=" WHERE status='0' "
        sqlStr=sqlStr+" AND RECKBANKNO like '%"+ TradeContext.code +"%'"
        sqlStr=sqlStr+" AND GENBANKNAME like '%"+ TradeContext.name +"%'"

        sqlStr_detail="SELECT RECKBANKNO,GENBANKNAME,OFNODECODE,ADDRESS,PEOPLENAME,PEOPLEPHONE,STATUS,EFFECTDATE"
        sqlStr_detail=sqlStr_detail+" FROM TIPS_BANKCODE "
        sqlStr_detail=sqlStr_detail+sqlStr
        AfaLoggerFunc.tradeInfo(sqlStr_detail)     
        records = AfaDBFunc.SelectSql( sqlStr_detail )
        if( records == None ):
            return AfaFlowControl.ExitThisFlow( '0027', '表操作异常:'+AfaDBFunc.sqlErrMsg )
        elif( len( records )==0 ):
            return AfaFlowControl.ExitThisFlow( '0028', '没有满足条件的数据' )
        
        mx_file_name = os.environ['AFAP_HOME'] + '/tmp/' + 'AH_' + TradeContext.teller + '.txt'
        TradeContext.tradeResponse.append(['fileName',  'AH_' + TradeContext.teller + '.txt'])
    
        if (os.path.exists(mx_file_name) and os.path.isfile(mx_file_name)):
            #文件存在,先删除-再创建
            os.system("rm " + mx_file_name)
    
        sfp = open(mx_file_name, "w")
        AfaLoggerFunc.tradeInfo('明细文件=['+mx_file_name+']')
    
        i = 0
        while ( i  < len(records) ):
            lineStr = ''
            lineStr = lineStr + str(records[i][0]).strip() + '|'        
            lineStr = lineStr + str(records[i][1]).strip() + '|'       
            lineStr = lineStr + str(records[i][2]).strip() + '|'      
            lineStr = lineStr + str(records[i][3]).strip() + '|'       
            lineStr = lineStr + str(records[i][4]).strip() + '|'       
            lineStr = lineStr + str(records[i][5]).strip() + '|'       
            lineStr = lineStr + str(records[i][6]).strip() + '|'        
            lineStr = lineStr + str(records[i][7]).strip() + '|'            
    
            sfp.write(lineStr  +  '\n')
    
            i=i+1
    
        sfp.close()
    if(TradeContext.dataType=="2"): #国库代码
        sqlStr=" WHERE status='0' "
        sqlStr=sqlStr+" AND TRECODE like '%"+ TradeContext.code +"%'"
        sqlStr=sqlStr+" AND TRENAME like '%"+ TradeContext.name +"%'"

        sqlStr_detail="SELECT TRECODE,TRENAME,TRELEVEL,PAYBANKNO,RECKONTRECODE,UPTRECODE,OFPROVTREA,"
        sqlStr_detail=sqlStr_detail+"OFCITYTREA,OFCOUNTYTREA,ADDRESS,PEOPLENAME,PEOPLEPHONE,STATUS,EFFECTDATE FROM TIPS_TRECODE "
        sqlStr_detail=sqlStr_detail+sqlStr
        AfaLoggerFunc.tradeInfo(sqlStr_detail)     
        records = AfaDBFunc.SelectSql( sqlStr_detail )
        if( records == None ):
            return AfaFlowControl.ExitThisFlow( '0027', '表操作异常:'+AfaDBFunc.sqlErrMsg )
        elif( len( records )==0 ):
            return AfaFlowControl.ExitThisFlow( '0028', '没有满足条件的数据' )
        
        mx_file_name = os.environ['AFAP_HOME'] + '/tmp/' + 'AH_' + TradeContext.teller + '.txt'
        TradeContext.tradeResponse.append(['fileName',  'AH_' + TradeContext.teller + '.txt'])
    
        if (os.path.exists(mx_file_name) and os.path.isfile(mx_file_name)):
            #文件存在,先删除-再创建
            os.system("rm " + mx_file_name)
    
        sfp = open(mx_file_name, "w")
        AfaLoggerFunc.tradeInfo('明细文件=['+mx_file_name+']')
    
        i = 0
        while ( i  < len(records) ):
            lineStr = ''
            lineStr = lineStr + str(records[i][0]).strip() + '|'        
            lineStr = lineStr + str(records[i][1]).strip() + '|'       
            lineStr = lineStr + str(records[i][2]).strip() + '|'      
            lineStr = lineStr + str(records[i][3]).strip() + '|'       
            lineStr = lineStr + str(records[i][4]).strip() + '|'       
            lineStr = lineStr + str(records[i][5]).strip() + '|'       
            lineStr = lineStr + str(records[i][6]).strip() + '|'        
            lineStr = lineStr + str(records[i][7]).strip() + '|'       
            lineStr = lineStr + str(records[i][8]).strip() + '|'        
            lineStr = lineStr + str(records[i][9]).strip() + '|'       
            lineStr = lineStr + str(records[i][10]).strip() + '|'        
            lineStr = lineStr + str(records[i][11]).strip() + '|'       
            lineStr = lineStr + str(records[i][12]).strip() + '|'        
            lineStr = lineStr + str(records[i][13]).strip() + '|' 
    
            sfp.write(lineStr  +  '\n')
    
            i=i+1
    
        sfp.close()                   
    if(TradeContext.dataType=="3"): #预算科目代码
        sqlStr=" WHERE status='0' "
        sqlStr=sqlStr+" AND BUDGETSUBJECTCODE like '%"+ TradeContext.code +"%'"
        sqlStr=sqlStr+" AND BUDGETSUBJECTNAME like '%"+ TradeContext.name +"%'"

        sqlStr_detail="SELECT BUDGETSUBJECTCODE,BUDGETSUBJECTNAME,"
        sqlStr_detail=sqlStr_detail+"STATUS FROM TIPS_BUDGETSUBJECTCODE "
        sqlStr_detail=sqlStr_detail+sqlStr
        AfaLoggerFunc.tradeInfo(sqlStr_detail)     
        records = AfaDBFunc.SelectSql( sqlStr_detail )
        if( records == None ):
            return AfaFlowControl.ExitThisFlow( '0027', '表操作异常:'+AfaDBFunc.sqlErrMsg )
        elif( len( records )==0 ):
            return AfaFlowControl.ExitThisFlow( '0028', '没有满足条件的数据' )
        
        mx_file_name = os.environ['AFAP_HOME'] + '/tmp/' + 'AH_' + TradeContext.teller + '.txt'
        TradeContext.tradeResponse.append(['fileName',  'AH_' + TradeContext.teller + '.txt'])
    
        if (os.path.exists(mx_file_name) and os.path.isfile(mx_file_name)):
            #文件存在,先删除-再创建
            os.system("rm " + mx_file_name)
    
        sfp = open(mx_file_name, "w")
        AfaLoggerFunc.tradeInfo('明细文件=['+mx_file_name+']')
    
        i = 0
        while ( i  < len(records) ):
            A0 = str(records[i][0]).strip()         #TRECODE
            A1 = str(records[i][1]).strip()         #TRENAME
    
            sfp.write(A0 +  '|'  +  A1 +  '|'  +  '\n')
    
            i=i+1
    
        sfp.close() 
    if(TradeContext.dataType=="4"): #税种代码
        sqlStr=" WHERE status='0' "
        sqlStr=sqlStr+" AND TAXTYPECODE like '%"+ TradeContext.code +"%'"
        sqlStr=sqlStr+" AND TAXTYPENAME like '%"+ TradeContext.name +"%'"

        sqlStr_detail="SELECT TAXTYPECODE,TAXORGTYPE,TAXTYPENAME,"
        sqlStr_detail=sqlStr_detail+"STATUS FROM TIPS_TAXTYPECODE "
        sqlStr_detail=sqlStr_detail+sqlStr
        AfaLoggerFunc.tradeInfo(sqlStr_detail)     
        records = AfaDBFunc.SelectSql( sqlStr_detail )
        if( records == None ):
            return AfaFlowControl.ExitThisFlow( '0027', '表操作异常:'+AfaDBFunc.sqlErrMsg )
        elif( len( records )==0 ):
            return AfaFlowControl.ExitThisFlow( '0028', '没有满足条件的数据' )
        
        mx_file_name = os.environ['AFAP_HOME'] + '/tmp/' + 'AH_' + TradeContext.teller + '.txt'
        TradeContext.tradeResponse.append(['fileName',  'AH_' + TradeContext.teller + '.txt'])
    
        if (os.path.exists(mx_file_name) and os.path.isfile(mx_file_name)):
            #文件存在,先删除-再创建
            os.system("rm " + mx_file_name)
    
        sfp = open(mx_file_name, "w")
        AfaLoggerFunc.tradeInfo('明细文件=['+mx_file_name+']')
    
        i = 0
        while ( i  < len(records) ):
            A0 = str(records[i][0]).strip()         #TRECODE
            A1 = str(records[i][1]).strip()         #TRENAME
            A2 = str(records[i][2]).strip()         #TRENAME
            
            sfp.write(A0 +  '|'  +  A1 +  '|'  + A2 +  '|'  +  '\n')
    
            i=i+1
    
        sfp.close() 
    if(TradeContext.dataType=="5"): #税目代码
        sqlStr=" WHERE status='0' "
        sqlStr=sqlStr+" AND TAXSUBJECTCODE like '%"+ TradeContext.code +"%'"
        sqlStr=sqlStr+" AND TAXSUBJECTNAME like '%"+ TradeContext.name +"%'"

        sqlStr_detail="SELECT TAXSUBJECTCODE,TAXORGTYPE,TAXSUBJECTNAME,"
        sqlStr_detail=sqlStr_detail+"STATUS FROM TIPS_TAXSUBJECTCODE "
        sqlStr_detail=sqlStr_detail+sqlStr
        AfaLoggerFunc.tradeInfo(sqlStr_detail)     
        records = AfaDBFunc.SelectSql( sqlStr_detail )
        if( records == None ):
            return AfaFlowControl.ExitThisFlow( '0027', '表操作异常:'+AfaDBFunc.sqlErrMsg )
        elif( len( records )==0 ):
            return AfaFlowControl.ExitThisFlow( '0028', '没有满足条件的数据' )
        
        mx_file_name = os.environ['AFAP_HOME'] + '/tmp/' + 'AH_' + TradeContext.teller + '.txt'
        TradeContext.tradeResponse.append(['fileName',  'AH_' + TradeContext.teller + '.txt'])
    
        if (os.path.exists(mx_file_name) and os.path.isfile(mx_file_name)):
            #文件存在,先删除-再创建
            os.system("rm " + mx_file_name)
    
        sfp = open(mx_file_name, "w")
        AfaLoggerFunc.tradeInfo('明细文件=['+mx_file_name+']')
    
        i = 0
        while ( i  < len(records) ):
            A0 = str(records[i][0]).strip()         #TRECODE
            A1 = str(records[i][1]).strip()         #TRENAME
            A2 = str(records[i][2]).strip()         #TRENAME
    
            sfp.write(A0 +  '|'  +  A1 +  '|'   +  A2 +  '|'  +  '\n')
    
            i=i+1
    
        sfp.close() 
    TradeContext.tradeResponse.append(['dataType',  TradeContext.dataType])
    TradeContext.tradeResponse.append(['errorCode',  '0000'])
    TradeContext.tradeResponse.append(['errorMsg',   '交易成功'])
    return True                    
