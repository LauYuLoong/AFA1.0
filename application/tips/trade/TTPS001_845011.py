# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.ͣ������֪ͨ�����з���
#=================================================================
#   �����ļ�:   TTPS001_845011.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   �޸�ʱ��:   2008-9-9 
#   ��    �ߣ�  ������
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools,TipsFunc, AfaFlowControl,AfaDBFunc
from types import *

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('ͣ������֪ͨǰ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    #============У�鹫���ڵ����Ч��==================
    if( not TradeContext.existVariable( "RunSign" ) ):
        return TipsFunc.ExitThisFlow( 'A0001', '[RunSign]ֵ������!' )
            
    #============RunSign=0 ͣ��ʱ======================
    if( TradeContext.RunSign=='0'):
        if not stop():
            return False
        if not start():
            return False

    #============RunSign=1 ����ʱ======================
    if( TradeContext.RunSign=='1'):                
        if not start():
            return False
           
    TradeContext.errorCode='0000'
    TradeContext.errorMsg='���״���ɹ�'
    return True
    
    
#ͣ��
def stop():
    try:
        AfaLoggerFunc.tradeInfo('RunSign='+TradeContext.RunSign+' ͣ�˵���')
        
        if( TradeContext.existVariable( "StopRunTime" ) and len(TradeContext.StopRunTime)<=0 ):
            return TipsFunc.ExitThisFlow( 'A0001', '[StopRunTime]ֵ������!' )
            
        year=(TradeContext.StopRunTime)[0:4]
        month=(TradeContext.StopRunTime)[4:6]
        day=(TradeContext.StopRunTime)[6:8]
        hour=(TradeContext.StopRunTime)[8:10]
        minute=(TradeContext.StopRunTime)[10:12]
          
        sql="UPDATE AFA_CRONADM               "
        sql=sql+" SET YEAR = '"+year+"',      "
        sql=sql+"     MONTH = '"+month+"',    "
        sql=sql+"     DAY = '"+day+"',        "
        sql=sql+"     HOUR = '"+hour+"',      "
        sql=sql+"     MINUTE = '"+minute+"',  "
        sql=sql+"     STATUS = '1'            "
        sql=sql+" WHERE TASKID = '00051'      "
            
        AfaLoggerFunc.tradeDebug(sql)
        
        records = AfaDBFunc.UpdateSqlCmt(sql)
        if( records <=0  ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0027', 'δ���ֵ�����Ϣ:'+AfaDBFunc.sqlErrMsg )
        if( records == None ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
            
        return True
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return AfaFlowControl.ExitThisFlow('9999', '�������쳣'+str(e)) 
        
#����
def start():
    try:
        AfaLoggerFunc.tradeInfo('RunSign='+TradeContext.RunSign+' ���õ���')
        if( TradeContext.existVariable( "BackRunTime" ) and len(TradeContext.BackRunTime)<=0 ):
            return TipsFunc.ExitThisFlow( 'A0001', '[BackRunTime]ֵ������!' )
        
        year=(TradeContext.BackRunTime)[0:4]
        month=(TradeContext.BackRunTime)[4:6]
        day=(TradeContext.BackRunTime)[6:8]
        hour=(TradeContext.BackRunTime)[8:10]
        minute=(TradeContext.BackRunTime)[10:12]
            
        sql="UPDATE AFA_CRONADM              "
        sql=sql+" SET YEAR = '"+year+"',     "
        sql=sql+"     MONTH = '"+month+"',   "
        sql=sql+"     DAY = '"+day+"',       "
        sql=sql+"     HOUR = '"+hour+"',     "
        sql=sql+"     MINUTE = '"+minute+"', "
        sql=sql+"     STATUS = '1'           "
        sql=sql+" WHERE TASKID = '00050'     "
            
        AfaLoggerFunc.tradeInfo(sql)
        
        records = AfaDBFunc.UpdateSqlCmt(sql)
        if( records <=0  ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0027', 'δ���ֵ�����Ϣ:'+AfaDBFunc.sqlErrMsg )
        if( records == None ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
      
        return True
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return AfaFlowControl.ExitThisFlow('9999', '�������쳣'+str(e))         