# -*- coding: gbk -*-
###############################################################################
# Copyright (c) 2011,������ͬ�Ƽ���չ���޹�˾.������ҵ��
# All rights reserved.
# �ļ����ƣ�TPS001_8652.py
# �ļ���ʶ��
# ժ    Ҫ����˰����.����������к�
# ��ǰ�汾��1.0
# ��    �ߣ�
# ������ڣ�2012 �� 7 ��
# ȡ���汾��
# ԭ �� �ߣ�LLJ
###############################################################################
import TradeContext
TradeContext.sysType = 'tips'
import TipsFunc, AfaDBFunc,AfaLoggerFunc,AfaFlowControl
#,ConfigParser,os,LoggerHandler, UtilTools, 
#import TipsHostFunc,HostContext,TradeContext, 

def SubModuleMainFst( ):
    try:
        
        AfaLoggerFunc.tradeInfo( '�������������к�[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        
        #���ԭ�������к��Ƿ������ݿ��еǼǵĿ������к�һ��
        sqlStr = ""
        sqlStr = sqlStr + "SELECT PAYOPBKCODE FROM TIPS_CUSTINFO WHERE TAXORGCODE = '" + TradeContext.taxOrgCode + "'" 
        sqlStr = sqlStr + " AND PAYACCT ='" + TradeContext.payAcct + "'"
        #sqlStr = sqlStr + " AND PAYOPBKCODE ='" + TradeContext.payBkCode+ "'"
        sqlStr = sqlStr + " AND PROTOCOLNO ='" +TradeContext.protocolNo+"'"
        
        AfaLoggerFunc.tradeInfo(sqlStr)
        
        records = AfaDBFunc.SelectSql( sqlStr )
        
        if( records == None ):
            
            return TipsFunc.ExitThisFlow( 'A0027', '������쳣:'+AfaDBFunc.sqlErrMsg )
                
        elif( len( records )==0 ):
                
            return TipsFunc.ExitThisFlow( 'A0027', 'û���������������ݼ�¼��' )
            
        else: 
            AfaLoggerFunc.tradeDebug("ԭ�������к�Ϊ��" +records[0][0])
                
        if(records[0][0] !=TradeContext.payBkCode):
            TradeContext.errorCode,TradeContext.errorMsg = "A0001","ԭ�������кŲ���ȷ��"
            return False
                
        
        #====================���¿������к�====================
        AfaLoggerFunc.tradeInfo(">>>���Ŀ������к�")
        update_sql = ""
        update_sql = "UPDATE TIPS_CUSTINFO SET PAYOPBKCODE = '" + TradeContext.payBkCode1 + "'"
        update_sql = update_sql + "WHERE TAXORGCODE = '" + TradeContext.taxOrgCode + "'"
        update_sql = update_sql + " AND PAYACCT ='" + TradeContext.payAcct + "'"
        update_sql = update_sql + " AND PAYOPBKCODE ='" + TradeContext.payBkCode+ "'"
        update_sql = update_sql + " AND PROTOCOLNO ='" +TradeContext.protocolNo+"'" 
        
        AfaLoggerFunc.tradeInfo(update_sql)
        
        if  AfaDBFunc.UpdateSqlCmt(update_sql)<0:
                return AfaFlowControl.ExitThisFlow("A0027","���¿������к�ʧ�ܣ�")
        
        TradeContext.errorCode,TradeContext.errorMsg = "0000","���׳ɹ�"

        AfaLoggerFunc.tradeInfo( '�˳�����������к�[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    
        return True 
    
    except Exception, e:             

        AfaFlowControl.exitMainFlow(str(e))    
