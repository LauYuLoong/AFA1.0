# -*- coding: gbk -*-
###############################################################################
# Copyright (c) 2006,������ͬ�Ƽ���չ���޹�˾.������ҵ��
# All rights reserved.
#
# �ļ����ƣ�TTPS001_8464.py
# �ļ���ʶ��
# ժ    Ҫ����˰����.��ѯ��������
#
# ��ǰ�汾��1.0
# ��    �ߣ�liyj
# ������ڣ�2008��12��05��
#
# ȡ���汾��
# ԭ �� �ߣ�
# ������ڣ�
###############################################################################
import TradeContext, AfaFlowControl, AfaDBFunc,AfaLoggerFunc,os
#LoggerHandler, UtilTools, UtilTools
def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo( '�����ѯ������ϸ['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']'  )

    AfaLoggerFunc.tradeInfo('��������Ϊ��'+TradeContext.dataType)
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
            return AfaFlowControl.ExitThisFlow( '0027', '������쳣:'+AfaDBFunc.sqlErrMsg )
        elif( len( records )==0 ):
            return AfaFlowControl.ExitThisFlow( '0028', 'û����������������' )
        
        mx_file_name = os.environ['AFAP_HOME'] + '/tmp/' + 'AH_' + TradeContext.teller + '.txt'
        TradeContext.tradeResponse.append(['fileName',  'AH_' + TradeContext.teller + '.txt'])
    
        if (os.path.exists(mx_file_name) and os.path.isfile(mx_file_name)):
            #�ļ�����,��ɾ��-�ٴ���
            os.system("rm " + mx_file_name)
    
        sfp = open(mx_file_name, "w")
        AfaLoggerFunc.tradeInfo('��ϸ�ļ�=['+mx_file_name+']')
    
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
    if(TradeContext.dataType=="1"): #���д���
        sqlStr=" WHERE status='0' "
        sqlStr=sqlStr+" AND RECKBANKNO like '%"+ TradeContext.code +"%'"
        sqlStr=sqlStr+" AND GENBANKNAME like '%"+ TradeContext.name +"%'"

        sqlStr_detail="SELECT RECKBANKNO,GENBANKNAME,OFNODECODE,ADDRESS,PEOPLENAME,PEOPLEPHONE,STATUS,EFFECTDATE"
        sqlStr_detail=sqlStr_detail+" FROM TIPS_BANKCODE "
        sqlStr_detail=sqlStr_detail+sqlStr
        AfaLoggerFunc.tradeInfo(sqlStr_detail)     
        records = AfaDBFunc.SelectSql( sqlStr_detail )
        if( records == None ):
            return AfaFlowControl.ExitThisFlow( '0027', '������쳣:'+AfaDBFunc.sqlErrMsg )
        elif( len( records )==0 ):
            return AfaFlowControl.ExitThisFlow( '0028', 'û����������������' )
        
        mx_file_name = os.environ['AFAP_HOME'] + '/tmp/' + 'AH_' + TradeContext.teller + '.txt'
        TradeContext.tradeResponse.append(['fileName',  'AH_' + TradeContext.teller + '.txt'])
    
        if (os.path.exists(mx_file_name) and os.path.isfile(mx_file_name)):
            #�ļ�����,��ɾ��-�ٴ���
            os.system("rm " + mx_file_name)
    
        sfp = open(mx_file_name, "w")
        AfaLoggerFunc.tradeInfo('��ϸ�ļ�=['+mx_file_name+']')
    
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
    if(TradeContext.dataType=="2"): #�������
        sqlStr=" WHERE status='0' "
        sqlStr=sqlStr+" AND TRECODE like '%"+ TradeContext.code +"%'"
        sqlStr=sqlStr+" AND TRENAME like '%"+ TradeContext.name +"%'"

        sqlStr_detail="SELECT TRECODE,TRENAME,TRELEVEL,PAYBANKNO,RECKONTRECODE,UPTRECODE,OFPROVTREA,"
        sqlStr_detail=sqlStr_detail+"OFCITYTREA,OFCOUNTYTREA,ADDRESS,PEOPLENAME,PEOPLEPHONE,STATUS,EFFECTDATE FROM TIPS_TRECODE "
        sqlStr_detail=sqlStr_detail+sqlStr
        AfaLoggerFunc.tradeInfo(sqlStr_detail)     
        records = AfaDBFunc.SelectSql( sqlStr_detail )
        if( records == None ):
            return AfaFlowControl.ExitThisFlow( '0027', '������쳣:'+AfaDBFunc.sqlErrMsg )
        elif( len( records )==0 ):
            return AfaFlowControl.ExitThisFlow( '0028', 'û����������������' )
        
        mx_file_name = os.environ['AFAP_HOME'] + '/tmp/' + 'AH_' + TradeContext.teller + '.txt'
        TradeContext.tradeResponse.append(['fileName',  'AH_' + TradeContext.teller + '.txt'])
    
        if (os.path.exists(mx_file_name) and os.path.isfile(mx_file_name)):
            #�ļ�����,��ɾ��-�ٴ���
            os.system("rm " + mx_file_name)
    
        sfp = open(mx_file_name, "w")
        AfaLoggerFunc.tradeInfo('��ϸ�ļ�=['+mx_file_name+']')
    
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
    if(TradeContext.dataType=="3"): #Ԥ���Ŀ����
        sqlStr=" WHERE status='0' "
        sqlStr=sqlStr+" AND BUDGETSUBJECTCODE like '%"+ TradeContext.code +"%'"
        sqlStr=sqlStr+" AND BUDGETSUBJECTNAME like '%"+ TradeContext.name +"%'"

        sqlStr_detail="SELECT BUDGETSUBJECTCODE,BUDGETSUBJECTNAME,"
        sqlStr_detail=sqlStr_detail+"STATUS FROM TIPS_BUDGETSUBJECTCODE "
        sqlStr_detail=sqlStr_detail+sqlStr
        AfaLoggerFunc.tradeInfo(sqlStr_detail)     
        records = AfaDBFunc.SelectSql( sqlStr_detail )
        if( records == None ):
            return AfaFlowControl.ExitThisFlow( '0027', '������쳣:'+AfaDBFunc.sqlErrMsg )
        elif( len( records )==0 ):
            return AfaFlowControl.ExitThisFlow( '0028', 'û����������������' )
        
        mx_file_name = os.environ['AFAP_HOME'] + '/tmp/' + 'AH_' + TradeContext.teller + '.txt'
        TradeContext.tradeResponse.append(['fileName',  'AH_' + TradeContext.teller + '.txt'])
    
        if (os.path.exists(mx_file_name) and os.path.isfile(mx_file_name)):
            #�ļ�����,��ɾ��-�ٴ���
            os.system("rm " + mx_file_name)
    
        sfp = open(mx_file_name, "w")
        AfaLoggerFunc.tradeInfo('��ϸ�ļ�=['+mx_file_name+']')
    
        i = 0
        while ( i  < len(records) ):
            A0 = str(records[i][0]).strip()         #TRECODE
            A1 = str(records[i][1]).strip()         #TRENAME
    
            sfp.write(A0 +  '|'  +  A1 +  '|'  +  '\n')
    
            i=i+1
    
        sfp.close() 
    if(TradeContext.dataType=="4"): #˰�ִ���
        sqlStr=" WHERE status='0' "
        sqlStr=sqlStr+" AND TAXTYPECODE like '%"+ TradeContext.code +"%'"
        sqlStr=sqlStr+" AND TAXTYPENAME like '%"+ TradeContext.name +"%'"

        sqlStr_detail="SELECT TAXTYPECODE,TAXORGTYPE,TAXTYPENAME,"
        sqlStr_detail=sqlStr_detail+"STATUS FROM TIPS_TAXTYPECODE "
        sqlStr_detail=sqlStr_detail+sqlStr
        AfaLoggerFunc.tradeInfo(sqlStr_detail)     
        records = AfaDBFunc.SelectSql( sqlStr_detail )
        if( records == None ):
            return AfaFlowControl.ExitThisFlow( '0027', '������쳣:'+AfaDBFunc.sqlErrMsg )
        elif( len( records )==0 ):
            return AfaFlowControl.ExitThisFlow( '0028', 'û����������������' )
        
        mx_file_name = os.environ['AFAP_HOME'] + '/tmp/' + 'AH_' + TradeContext.teller + '.txt'
        TradeContext.tradeResponse.append(['fileName',  'AH_' + TradeContext.teller + '.txt'])
    
        if (os.path.exists(mx_file_name) and os.path.isfile(mx_file_name)):
            #�ļ�����,��ɾ��-�ٴ���
            os.system("rm " + mx_file_name)
    
        sfp = open(mx_file_name, "w")
        AfaLoggerFunc.tradeInfo('��ϸ�ļ�=['+mx_file_name+']')
    
        i = 0
        while ( i  < len(records) ):
            A0 = str(records[i][0]).strip()         #TRECODE
            A1 = str(records[i][1]).strip()         #TRENAME
            A2 = str(records[i][2]).strip()         #TRENAME
            
            sfp.write(A0 +  '|'  +  A1 +  '|'  + A2 +  '|'  +  '\n')
    
            i=i+1
    
        sfp.close() 
    if(TradeContext.dataType=="5"): #˰Ŀ����
        sqlStr=" WHERE status='0' "
        sqlStr=sqlStr+" AND TAXSUBJECTCODE like '%"+ TradeContext.code +"%'"
        sqlStr=sqlStr+" AND TAXSUBJECTNAME like '%"+ TradeContext.name +"%'"

        sqlStr_detail="SELECT TAXSUBJECTCODE,TAXORGTYPE,TAXSUBJECTNAME,"
        sqlStr_detail=sqlStr_detail+"STATUS FROM TIPS_TAXSUBJECTCODE "
        sqlStr_detail=sqlStr_detail+sqlStr
        AfaLoggerFunc.tradeInfo(sqlStr_detail)     
        records = AfaDBFunc.SelectSql( sqlStr_detail )
        if( records == None ):
            return AfaFlowControl.ExitThisFlow( '0027', '������쳣:'+AfaDBFunc.sqlErrMsg )
        elif( len( records )==0 ):
            return AfaFlowControl.ExitThisFlow( '0028', 'û����������������' )
        
        mx_file_name = os.environ['AFAP_HOME'] + '/tmp/' + 'AH_' + TradeContext.teller + '.txt'
        TradeContext.tradeResponse.append(['fileName',  'AH_' + TradeContext.teller + '.txt'])
    
        if (os.path.exists(mx_file_name) and os.path.isfile(mx_file_name)):
            #�ļ�����,��ɾ��-�ٴ���
            os.system("rm " + mx_file_name)
    
        sfp = open(mx_file_name, "w")
        AfaLoggerFunc.tradeInfo('��ϸ�ļ�=['+mx_file_name+']')
    
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
    TradeContext.tradeResponse.append(['errorMsg',   '���׳ɹ�'])
    return True                    
