# -*- coding: gbk -*-
###############################################################################
# Copyright (c) 2006,������ͬ�Ƽ���չ���޹�˾.������ҵ��
# All rights reserved.
#
# �ļ����ƣ�TTPS001_8456.py
# �ļ���ʶ��
# ժ    Ҫ����˰����.������ӽ�˰����ƾ֤
# ��ǰ�汾��1.0
# ��    �ߣ�
# ������ڣ�2008��12��05��
#
# ȡ���汾��
# ԭ �� �ߣ�liyj
# ������ڣ�
###############################################################################
import TradeContext, TipsFunc, AfaDBFunc,AfaLoggerFunc,os
#import TipsHostFunc,HostContext��LoggerHandler, UtilTools, ConfigParser

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo( '���벹����ӽ�˰����ƾ֤[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    
    #============����ֵ����Ч��У��============
    AfaLoggerFunc.tradeInfo(">>>����ֵ����Ч��У��")
    if( not TradeContext.existVariable( "taxPayCode" ) ):
        return TipsFunc.ExitThisFlow( 'A0001', '��˰�˱���[taxPayCode]ֵ������!' )
    if( not TradeContext.existVariable( "taxOrgCode" ) ):
        return TipsFunc.ExitThisFlow( 'A0001', '���ջ��ش���[taxOrgCode]ֵ������!' )
    if( not TradeContext.existVariable( "payAcct" ) ):
        return TipsFunc.ExitThisFlow( 'A0001', '�������˺�[payAcct]ֵ������!' )
    if( not TradeContext.existVariable( "protocolNo" ) ):
        return TipsFunc.ExitThisFlow( 'A0001', '����Э���[protocolNo]ֵ������!' )
    if( not TradeContext.existVariable( "serialNo" ) ):
        return TipsFunc.ExitThisFlow( 'A0001', '������ˮ��[serialNo]ֵ������!' )
    if( not TradeContext.existVariable( "workDate" ) ):
        return TipsFunc.ExitThisFlow( 'A0001', '��������[workDate]ֵ������!' )
        
    

    #================��ȡ������ˮ��Ϣ===============
    AfaLoggerFunc.tradeInfo(">>>��ȡ������ˮ��Ϣ")
    sqlStr =''
    
    #begin 20101130 �������޸�
    #sqlStr = "SELECT t.SERIALNO,t.WORKDATE,t.CORPSERNO,t.AMOUNT,t.TAXVOUNO,t1.payacct,t1.taxorgcode,t1.taxpaycode,t1.protocolno"
    sqlStr = "SELECT t.SERIALNO,t.WORKDATE,t.CORPSERNO,t.AMOUNT,t.TAXVOUNO,t1.payacct,t1.taxorgcode,t1.taxpaycode,t1.protocolno,t.note10"
    #end
    
    sqlStr = sqlStr + " FROM TIPS_MAINTRANSDTL t,tips_custinfo t1 WHERE "
    sqlStr = sqlStr + " t.SERIALNO ='"        + TradeContext.serialNo    +"'"
    sqlStr = sqlStr + " AND t.WORKDATE ='" + TradeContext.workDate +"'"
    ###################################################################################
    #guanbj 20091105 tips��maps������ɺ󼴿ɴ�ӡƾ֤
    #sqlStr = sqlStr + " AND t.CHKFLAG='0' and t.taxpaycode=t1.taxpaycode "
    sqlStr = sqlStr + " AND t.CORPCHKFLAG='0' and t.taxpaycode=t1.taxpaycode "
    ###################################################################################
    #begin 20101102 ������ ���Ӳ�ѯ��������֤��ѯ���Ψһ
    sqlStr = sqlStr + " AND t.DRACCNO = t1.PAYACCT"
    sqlStr = sqlStr + " AND t1.status = '1' "
    #end
    AfaLoggerFunc.tradeInfo(sqlStr)     
    records = AfaDBFunc.SelectSql( sqlStr )
    if( records == None or records <0):
        return TipsFunc.ExitThisFlow( '0027', '������쳣:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return TipsFunc.ExitThisFlow( '0028', 'û����������������' )
    else:
        AfaLoggerFunc.tradeInfo(records[0][0])
        
    TradeContext.tradeResponse.append(['traNo',records[0][2]])           #��������ˮ
    TradeContext.tradeResponse.append(['amount',str(records[0][3])])     #���
    TradeContext.tradeResponse.append(['taxVouhNo',records[0][4]])       #˰Ʊ����
    TradeContext.tradeResponse.append(['workDate',records[0][1]])        #��������
    
    #begin 20101130 ����������
    TradeContext.tradeResponse.append(['BankName',records[0][9]])               #�տ��������
    #end
    
    #===== add by liu.yl at 20110713 ====
    #===== ����else�жϣ����ǰ̨�ύ�����ݲ�Ϊ�գ��ж��Ƿ�����ˮ��¼����Ϣƥ�� ====
    #===== ��Ϣ��ƥ�䣬���ش��� ====
    if(len(TradeContext.payAcct)==0):
        TradeContext.payAcct=records[0][5]
    else:
        if(TradeContext.payAcct != records[0][5]):
            return TipsFunc.ExitThisFlow( '0028', '�������˺�����ˮ��¼��Ϣ��ƥ��' )
        
        
    if(len(TradeContext.taxOrgCode)==0):
        TradeContext.taxOrgCode=records[0][6]
    else:
        if(TradeContext.taxOrgCode != records[0][6]):
            return TipsFunc.ExitThisFlow( '0028', '���ջ��ش�������ˮ��¼��Ϣ��ƥ��' )
        
    if(len(TradeContext.taxPayCode)==0):
        TradeContext.taxPayCode=records[0][7]
    else:
        if(TradeContext.taxPayCode != records[0][7]):
            return TipsFunc.ExitThisFlow( '0028', '��˰�˱�������ˮ��¼��Ϣ��ƥ��' )
        
    if(len(TradeContext.protocolNo)==0):
        TradeContext.protocolNo=records[0][8]
    else:
        if(TradeContext.protocolNo != records[0][8]):
            return TipsFunc.ExitThisFlow( '0028', '����Э�������ˮ��¼��Ϣ��ƥ��' )
    #===== end of added ====
    
    
    #============��ȡ����Э����Ϣ=================
    AfaLoggerFunc.tradeInfo(">>>��ȡ����Э����Ϣ")
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
        return TipsFunc.ExitThisFlow( '0027', '������쳣:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )== 0 ):
        return TipsFunc.ExitThisFlow( '0028', 'û����������������' )
    elif( len( records ) > 1 ):
        return TipsFunc.ExitThisFlow( '0028', '�����쳣' )
    
    TradeContext.tradeResponse.append(['taxPayCode',records[0][1] + '  ' + records[0][0]])             #��˰�˱���
    TradeContext.tradeResponse.append(['payAcct',records[0][2]])                #�������ʺ�
    TradeContext.tradeResponse.append(['taxPayName',records[0][3]])             #����������
    TradeContext.tradeResponse.append(['taxOrgName',records[0][4]])             #���ջ�������
    
    #begin 20101130 ������ע�͵�
    #TradeContext.tradeResponse.append(['BankName',records[0][6]])               #�տ��������
    #end
    
    TradeContext.tradeResponse.append(['payOpBkName',TradeContext.brName])      #����������
    if(TradeContext.brno != records[0][5]):
        return TipsFunc.ExitThisFlow( 'A0001', '�ǿ�����' )
    
    
    
    
    #==========��ȡ˰����Ϣ===========
    mx_file_name = os.environ['AFAP_HOME'] + '/tmp/' + 'AH_' + TradeContext.teller + '.txt'
    TradeContext.tradeResponse.append(['fileName',  'AH_' + TradeContext.teller + '.txt'])
    
    if (os.path.exists(mx_file_name) and os.path.isfile(mx_file_name)):
        #�ļ�����,��ɾ��-�ٴ���
        os.system("rm " + mx_file_name)
    
    sfp = open(mx_file_name, "w")
    AfaLoggerFunc.tradeInfo('��ϸ�ļ�=['+mx_file_name+']')
    
    sqlStrVou =''
    sqlStrVou = "SELECT TAXTYPENAME,TAXSTARTDATE,TAXENDDATE,TAXTYPEAMT,NOTE1"
    sqlStrVou = sqlStrVou + " FROM TIPS_VOU_TAXTYPE WHERE "
    sqlStrVou = sqlStrVou + " WORKDATE='"             + TradeContext.workDate    +"'"
    sqlStrVou = sqlStrVou + " AND SERIALNO='"         + TradeContext.serialNo   +"'"

    AfaLoggerFunc.tradeInfo(sqlStrVou)     
    recordsVou = AfaDBFunc.SelectSql( sqlStrVou )   
    if( recordsVou == None ):
        sfp.close()
        return TipsFunc.ExitThisFlow( '0027', '������쳣:'+AfaDBFunc.sqlErrMsg )
    #begin 20101102 �������޸�
    #elif( len(recordsVou) <0 ):
    #    sfp.close()
    #    return TipsFunc.ExitThisFlow( '0027', '������쳣:'+AfaDBFunc.sqlErrMsg )
    elif( len(recordsVou) == 0 ):
        sfp.close()
        return TipsFunc.ExitThisFlow( '0027', 'û����ص�˰����Ϣ' )
    #end
    else:
        for j in range(0,len(recordsVou)):
            A0 = str(recordsVou[j][0]).strip()
            A1 = str(recordsVou[j][1]).strip() + '-' + str(recordsVou[j][2]).strip()
            A2 = str(recordsVou[j][3]).strip()
        
            sfp.write(A0 +  '|'  +  A1 +  '|'  +  A2 +  '|' + '\n')
        
    sfp.close()
    
    TradeContext.tradeResponse.append(['printNo',str(int(recordsVou[0][4]) + 1)])                #��ӡ����
    
    #==============���Ĵ�ӡ����=====================
    AfaLoggerFunc.tradeInfo(">>>���Ĵ�ӡ����")
    sqlStr = ""
    sqlStr = "update TIPS_VOU_TAXTYPE set note1 = '" + str(int(recordsVou[0][4]) + 1) + "' where"
    sqlStr = sqlStr + " WORKDATE='"             + TradeContext.workDate    +"'"
    sqlStr = sqlStr + " AND SERIALNO='"         + TradeContext.serialNo   +"'"
    
    AfaLoggerFunc.tradeInfo(sqlStr)     
    res = AfaDBFunc.UpdateSqlCmt( sqlStr )   
    if( res == None ):
        return TipsFunc.ExitThisFlow( '0027', '������쳣:'+AfaDBFunc.sqlErrMsg )
    elif( res <0 ):
        return TipsFunc.ExitThisFlow( '0027', '������쳣:'+AfaDBFunc.sqlErrMsg )
    
    TradeContext.tradeResponse.append(['errorCode','0000'])
    TradeContext.tradeResponse.append(['errorMsg','���׳ɹ�'])
            
    AfaLoggerFunc.tradeInfo( '�˳�������ӽ�˰����ƾ֤[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    return True

 
