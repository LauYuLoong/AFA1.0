###############################################################################
# -*- coding: gbk -*-
# ժ    Ҫ����ũ��ǩԼ��Ϣ��ѯ
# ��ǰ�汾��1.0
# ��    �ߣ�LLJ
# ������ڣ�2012��7��
###############################################################################
import AfaDBFunc,AfaLoggerFunc,TradeContext,AfaFlowControl,AhXnbFunc
from types import *

def TrxMain( ):
    
    try:
    
        AfaLoggerFunc.tradeInfo('�ͻ�ǩԼ��Ϣ��ѯ[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']����' )
        
        #ҵ����
        if ( not (TradeContext.existVariable( "Appno" ) and len(TradeContext.Appno.strip()) > 0) ):
            TradeContext.errorCode,TradeContext.errorMsg = '0001', "������ҵ����"
            raise AfaFlowControl.flowException( )
            
        #��λ���
        if ( not (TradeContext.existVariable( "Busino" ) and len(TradeContext.Busino.strip()) > 0) ):
            TradeContext.errorCode,TradeContext.errorMsg = '0001', "�����ڵ�λ���"
            raise AfaFlowControl.flowException( )
            
        #�籣���
        if ( not (TradeContext.existVariable( "sbno" ) and len(TradeContext.sbno.strip()) > 0) ):
            TradeContext.errorCode,TradeContext.errorMsg = '0001', "�������籣���"
            raise AfaFlowControl.flowException( )
        
        #�жϵ�λЭ���Ƿ���Ч
        TradeContext.I1APPNO =TradeContext.Appno
        TradeContext.I1BUSINO=TradeContext.Busino
        if ( not AhXnbFunc.ChkUnitInfo( ) ):
            return False
        
        sql = ""
        sql = sql + "select USERNAME,IDCODE,ACCNO,VOUHTYPE,PROTOCOLNO,BRNO,CONTRACTDATE from abdt_custinfo where "
        sql = sql + " APPNO ='" + TradeContext.Appno + "'"
        sql = sql + " and BUSINO ='" + TradeContext.Busino+ "'"
        sql = sql + " and BUSIUSERNO ='" +TradeContext.sbno+"'" 
        
        AfaLoggerFunc.tradeInfo("�ͻ�ǩԼ��ѯsql="+sql)
        records = AfaDBFunc.SelectSql( sql )
        
        if(records == None):
            AfaLoggerFunc.tradeInfo("��ѯ���ݿ��쳣")
            TradeContext.errorCode,TradeContext.errorMsg = "0001","��ѯ���ݿ��쳣"
            
        elif(len(records)==0):
            AfaLoggerFunc.tradeInfo("û�в�ѯ�����ǩԼ��Ϣ")
            TradeContext.errorCode,TradeContext.errorMsg = "0001","û�в�ѯ�����ǩԼ��Ϣ"
            
        elif(len(records)>1):
            AfaLoggerFunc.tradeInfo("�ͻ�ǩԼ��Ϣ��Ψһ")
            TradeContext.errorCode,TradeContext.errorMsg = "0001","�ͻ�ǩԼ��Ϣ��Ψһ"
            
        else:
            TradeContext.name        = records[0][0].strip()     #�ͻ�����
            TradeContext.idcode      = records[0][1].strip()     #֤������
            TradeContext.accno       = records[0][2].strip()     #�˺�
            TradeContext.vouhtype    = records[0][3].strip()     #ƾ֤����
            TradeContext.protocolno  = records[0][4].strip()     #Э����
            TradeContext.brno        = records[0][5].strip()     #ǩԼ����
            TradeContext.contract_date = records[0][6].strip()   #ǩԼ����
            
            
            TradeContext.errorCode  = "0000"
            TradeContext.errorMsg   = "���׳ɹ�"
            return True
        AfaLoggerFunc.tradeInfo('�ͻ�ǩԼ��ѯ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']�˳�' )
        
    
    except Exception, e:                   
        AfaFlowControl.exitMainFlow(str(e))