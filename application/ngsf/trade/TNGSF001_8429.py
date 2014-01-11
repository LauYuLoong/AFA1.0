# -*- coding: gbk -*-
################################################################################
#   ����ҵ��ϵͳ����ѯ��ҵЭ��
#===============================================================================
#   �����ļ�:   T001000_8429.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ����
#   �޸�ʱ��:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc,NGSFAbdtFunc,AfaFlowControl
from types import *

#=====================��ѯ��ҵ��Ϣ==============================================
def TrxMain( ):
    AfaLoggerFunc.tradeInfo('**********��ѯ��ҵ��Ϣ(8429)��ʼ**********')
    
    flag = ( TradeContext.existVariable( "Protocolno" ) and  len(TradeContext.Protocolno) != 0 ) or ( TradeContext.existVariable( "BusiUserno" ) and  len(TradeContext.BusiUserno) != 0 ) or ( TradeContext.existVariable( "BankUserno" ) and  len(TradeContext.BankUserno) != 0 )
    
    #8429����λ��ѯ
    if( ( TradeContext.existVariable( "PayerAccno" ) and len(TradeContext.PayerAccno) == 0 ) and (not flag) ):
        AfaLoggerFunc.tradeInfo('8429����λ��ѯ>>>>>>>>>>>')
        
        if( not TradeContext.existVariable( "Appno" ) or (TradeContext.existVariable( "Appno" ) and len(TradeContext.Appno) == 0) ):
            return AfaFlowControl.ExitThisFlow( 'A010', 'ҵ����[Appno]ֵ������!' )
        if( not TradeContext.existVariable( "PayeeUnitno" ) or (TradeContext.existVariable( "PayeeUnitno" ) and len(TradeContext.PayeeUnitno) == 0) ):
            return AfaFlowControl.ExitThisFlow( 'A010', '��λ���[PayeeUnitno]ֵ������!' )
                
        sql = ""
        sql = sql + "select * from abdt_unitInfo"
        sql = sql + " where appno = '"  +TradeContext.Appno       +"'"
        sql = sql + " and busino  = '"  +TradeContext.PayeeUnitno +"'"
        
        AfaLoggerFunc.tradeInfo('8429����λ��ѯsql='+sql)
        record = AfaDBFunc.SelectSql(sql)
        
        if(record==None):
            TradeContext.errorCode,TradeContext.errorMsg = "A010" ,"���ݿ��쳣"
            return False
        
        if(len(record)==0):
            TradeContext.errorCode,TradeContext.errorMsg = "A010" ,"û�иõ�λ��Ϣ"    
            return False
        
        #�շѵ�λ�˻�,�շѵ�λ����
        AfaLoggerFunc.tradeInfo('8429����λ��ѯ���'+record[0][0].strip())
        TradeContext.tradeResponse.append(['PayeeAccno',record[0][6].strip()])
        TradeContext.tradeResponse.append(['PayeeName',record[0][12].strip()])
        
        AfaLoggerFunc.tradeInfo('**********��ѯ��ҵ��Ϣ(8429)����**********')
        
        #����
        TradeContext.tradeResponse.append(['errorCode','0000'])
        TradeContext.tradeResponse.append(['errorMsg','���׳ɹ�'])
        return True
        
    #8429���˻���ѯ
    if( (TradeContext.existVariable( "PayerAccno" ) and len(TradeContext.PayerAccno) > 0) and (not flag) ):
        AfaLoggerFunc.tradeInfo('8429���˻���ѯ>>>>>>>>>>>')
        
        #����8810��ѯ���˻�������
        NGSFAbdtFunc.QueryAccInfo()
        
        if TradeContext.errorCode !='0000':
            AfaLoggerFunc.tradeInfo('8810�����˻���ѯʧ��')
            return False
            
        AfaLoggerFunc.tradeInfo('8810�����˻���ѯ�ɹ�'+TradeContext.USERNAME)
        TradeContext.PayerName = TradeContext.USERNAME
        TradeContext.tradeResponse.append(['PayerName',TradeContext.PayerName])
        
        AfaLoggerFunc.tradeInfo('**********��ѯ��ҵ��Ϣ(8429)����**********')
       
        #����
        TradeContext.tradeResponse.append(['errorCode', '0000'])
        TradeContext.tradeResponse.append(['errorMsg',  '���׳ɹ�'])
        return True
    
    #8429����ҵ��ѯ
    if( flag ):        
        AfaLoggerFunc.tradeInfo('8429����ҵ��ѯ>>>>>>>>>>>')
        
        if( not TradeContext.existVariable( "Appno" ) or (TradeContext.existVariable( "Appno" ) and len(TradeContext.Appno) == 0) ):
            return AfaFlowControl.ExitThisFlow( 'A010', 'ҵ����[Appno]ֵ������!' )
        if( not TradeContext.existVariable( "PayeeUnitno" ) or (TradeContext.existVariable( "PayeeUnitno" ) and len(TradeContext.PayeeUnitno) == 0) ):
            return AfaFlowControl.ExitThisFlow( 'A010', '��λ���[PayeeUnitno]ֵ������!' )
        
        #TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #��������
        #TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #����ʱ��
        
        #�жϵ�λЭ���Ƿ���Ч
        if ( not NGSFAbdtFunc.ChkUnitInfo( ) ):
            return False
        
        try:
            AfaLoggerFunc.tradeInfo('��ҵЭ���ѯ')
            
            sql = "SELECT * FROM ABDT_CUSTINFO WHERE "
            sql = sql + "STATUS="                 + "'" + "1"                          + "'"            #״̬(0:�쳣,1:����)
            
            if ( len(TradeContext.Appno) > 0 ):
                sql = sql + " AND APPNO="         + "'" + TradeContext.Appno           + "'"            #ҵ����
            if ( len(TradeContext.PayeeUnitno) > 0 ):
                sql = sql + " AND BUSINO="        + "'" + TradeContext.PayeeUnitno     + "'"          #��λ���
            
            if( TradeContext.existVariable( "Protocolno" ) and len( TradeContext.Protocolno ) != 0 ):
                sql = sql + " and Protocolno = '"+ TradeContext.Protocolno +"'"
            if( TradeContext.existVariable( "BusiUserno" ) and len( TradeContext.BusiUserno ) != 0 ):
                sql = sql + " and BusiUserno = '"+ TradeContext.BusiUserno +"'"
            if( TradeContext.existVariable( "BankUserno" ) and len( TradeContext.BankUserno ) != 0 ):
                sql = sql + " and Accno = '"+ TradeContext.BankUserno +"'"
       
            AfaLoggerFunc.tradeInfo( '��ҵЭ���ѯ'+sql )
            records = AfaDBFunc.SelectSql( sql )
            
            if ( records == None ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return ExitSubTrade( '9000', '��ѯ��ҵЭ����Ϣ�쳣' )
        
            if ( len(records) == 0 ):
                return ExitSubTrade( '9000', 'û����ص���ҵЭ����Ϣ')
       
            AfaLoggerFunc.tradeInfo(">>>�ܹ���ѯ[" + str(len(records)) + "]����¼")
            AfaUtilTools.ListFilterNone( records )
                
            TradeContext.tradeResponse.append(['Appno',             str(records[0][0])])    #ҵ����
            TradeContext.tradeResponse.append(['PayeeUnitno',       str(records[0][1])])    #��λ���
            TradeContext.tradeResponse.append(['PayerUnitno',       str(records[0][2])])    #�û����
            
            #TradeContext.tradeResponse.append(['O1VOUHTYPE',        str(records[0][5])])    #ƾ֤����
            #TradeContext.tradeResponse.append(['O1VOUHNO',          str(records[0][6])])    #ƾ֤��
            
            TradeContext.tradeResponse.append(['PayerAccno',        str(records[0][7])])    #���ڴ���ʺ�
            
            #TradeContext.tradeResponse.append(['O1SUBACCNO',        str(records[0][8])])    #���ʺ�
            #TradeContext.tradeResponse.append(['O1CURRTYPE',        str(records[0][9])])    #����
            #TradeContext.tradeResponse.append(['O1LIMITAMT',        str(records[0][10])])   #�����޶�
            
            TradeContext.tradeResponse.append(['PartFlag',          str(records[0][11])])   #���ֿۿ��־
            TradeContext.tradeResponse.append(['Protocolno',        str(records[0][12])])   #Э����
            TradeContext.tradeResponse.append(['ContractDate',      str(records[0][13])])   #ǩԼ����(��ͬ����)
            TradeContext.tradeResponse.append(['StartDate',         str(records[0][14])])   #��Ч����
            TradeContext.tradeResponse.append(['EndDate',           str(records[0][15])])   #ʧЧ����
            
            #TradeContext.tradeResponse.append(['O1PASSCHKFLAG',     str(records[0][16])])   #������֤��־
            #TradeContext.tradeResponse.append(['O1PASSWD',          str(records[0][17])])   #����
            #TradeContext.tradeResponse.append(['O1IDCHKFLAG',       str(records[0][18])])   #֤����֤��־
            #TradeContext.tradeResponse.append(['O1IDTYPE',          str(records[0][19])])   #֤������
            #TradeContext.tradeResponse.append(['O1IDCODE',          str(records[0][20])])   #֤������
            #TradeContext.tradeResponse.append(['O1NAMECHKFLAG',     str(records[0][21])])   #������֤��־
            
            TradeContext.tradeResponse.append(['PayerName',         str(records[0][22])])   #�ͻ�����
            TradeContext.tradeResponse.append(['Tel',               str(records[0][23])])   #��ϵ�绰
            TradeContext.tradeResponse.append(['Address',           str(records[0][24])])   #��ϵ��ַ
            
            #TradeContext.tradeResponse.append(['O1ZIPCODE',         str(records[0][25])])   #�ʱ�
            #TradeContext.tradeResponse.append(['O1EMAIL',           str(records[0][26])])   #��������
            #TradeContext.tradeResponse.append(['O1STATUS',          str(records[0][27])])   #״̬
            #TradeContext.tradeResponse.append(['O1ZONENO',          str(records[0][28])])   #������
            
            TradeContext.tradeResponse.append(['InBrno',            str(records[0][29])])   #�����(��������)
            TradeContext.tradeResponse.append(['InTellerno',        str(records[0][30])])   #��Ա��
            TradeContext.tradeResponse.append(['InDate',            str(records[0][31])])   #¼������
            TradeContext.tradeResponse.append(['InTime',            str(records[0][32])])   #¼��ʱ��
            #TradeContext.tradeResponse.append(['PayeeName',         str(records[0][33])])   #��ע1
            TradeContext.tradeResponse.append(['UserName',          str(records[0][34])])   #��ϵ��
            TradeContext.tradeResponse.append(['PayeeAccno',        str(records[0][35])])   #�շѵ�λ�˻�
            
            #TradeContext.tradeResponse.append(['O1NOTE4',           str(records[0][36])])   #��ע4
            TradeContext.tradeResponse.append(['PayeeName',          str(records[0][37])])   #�շѵ�λ����
       
            AfaLoggerFunc.tradeInfo('**********��ѯ��ҵ��Ϣ(8429)����**********')
       
            #����
            TradeContext.tradeResponse.append(['errorCode', '0000'])
            TradeContext.tradeResponse.append(['errorMsg',  '���׳ɹ�'])
            return True
            
        except Exception, e:
            AfaLoggerFunc.tradeFatal( str(e) )
            return ExitSubTrade( '9999', '��ѯ��ҵЭ����Ϣ�쳣')

def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False