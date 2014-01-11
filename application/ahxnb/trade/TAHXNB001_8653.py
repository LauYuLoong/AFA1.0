###############################################################################
# -*- coding: gbk -*-
# ժ    Ҫ����ũ��ǩԼ�˺Ÿ���
# ��ǰ�汾��1.0
# ��    �ߣ�LLJ
# ������ڣ�2012��7��
###############################################################################
import AfaDBFunc,AfaLoggerFunc,TradeContext,AfaFlowControl
from types import *

def TrxMain( ):
    
    try:
    
        AfaLoggerFunc.tradeInfo('�ͻ�ǩԼ�˺Ÿ���[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']����' )
        
        sql = ""
        sql = sql + "select USERNAME,ACCNO,VOUHTYPE,BRNO,TELLERNO from abdt_custinfo where "
        sql = sql + "  APPNO ='" + TradeContext.Appno + "'"
        sql = sql + " and BUSINO ='" + TradeContext.Busino+ "'"
        sql = sql + " and BUSIUSERNO ='" +TradeContext.sbno+"'" 
        
        AfaLoggerFunc.tradeInfo("��ѯԭǩԼ��Ϣsql="+sql)
        records = AfaDBFunc.SelectSql( sql )
        
        if(records == None):
            AfaLoggerFunc.tradeInfo("��ѯ���ݿ��쳣")
            TradeContext.errorCode,TradeContext.errorMsg = "0001","��ѯ���ݿ��쳣"
            
        elif(len(records)==0):
            AfaLoggerFunc.tradeInfo("û�в�ѯ��ǩԼ��Ϣ")
            TradeContext.errorCode,TradeContext.errorMsg = "0001","û�в�ѯ��ǩԼ��Ϣ"
            
        elif(len(records)>1):
            AfaLoggerFunc.tradeInfo("�ͻ�ǩԼ��Ϣ��Ψһ")
            TradeContext.errorCode,TradeContext.errorMsg = "0001","�ͻ�ǩԼ��Ϣ��Ψһ"
            
        else:
            #note5�ֶα��� ԭ�˺�|ԭ�˺�����|
            TradeContext.accno       = records[0][1].strip()
            TradeContext.vouhtype    = records[0][2].strip()
            
            TradeContext.note5 = ''
            TradeContext.note5 = TradeContext.accno + '|'+ TradeContext.vouhtype
            AfaLoggerFunc.tradeInfo(TradeContext.note5) 
            
            #note3�ֶα��� �����˺�����|�����˺Ż���|�����˺Ź�Ա|
            TradeContext.note3 = ''
            TradeContext.note3 = TradeContext.note3 + TradeContext.WorkDate + '|' + TradeContext.brno +'|'+ TradeContext.tellerno
            AfaLoggerFunc.tradeInfo(TradeContext.note3) 
            
        #���Ŀͻ�ǩԼ�˺�
        AfaLoggerFunc.tradeInfo(">>>���Ŀͻ�ǩԼ�˺�")
        update_sql = ""
        update_sql = "UPDATE ABDT_CUSTINFO SET "
        update_sql = update_sql + "ACCNO = '" + TradeContext.accno1 + "',"
        update_sql = update_sql + "VOUHTYPE = '" + TradeContext.vouhtype1 + "',"
        update_sql = update_sql + "NOTE3 = '" + TradeContext.note3 + "',"
        update_sql = update_sql + "NOTE5 = '" + TradeContext.note5 + "'"
        update_sql = update_sql + "WHERE APPNO = '" + TradeContext.Appno + "'" 
        update_sql = update_sql + " and BUSINO ='" + TradeContext.Busino + "'"
        update_sql = update_sql + " and BUSIUSERNO ='" + TradeContext.sbno+ "'"
        
        AfaLoggerFunc.tradeInfo(update_sql)
        
        if  AfaDBFunc.UpdateSqlCmt(update_sql)<0:
                return AfaFlowControl.ExitThisFlow("0001","�����˺�ʧ�ܣ�")
        
        TradeContext.errorCode,TradeContext.errorMsg = "0000","���׳ɹ�"    	
        
        AfaLoggerFunc.tradeInfo( '�ͻ�ǩԼ�˺Ÿ���[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']�˳�' )
    
        return True 
    
    except Exception, e:                   
        AfaFlowControl.exitMainFlow(str(e))