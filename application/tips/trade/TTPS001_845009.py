# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.����֪ͨ�����з���
#=================================================================
#   �����ļ�:   TTPS001_845009.py
#   �޸�ʱ��:   2007-5-28 10:28
##################################################################
import TradeContext, AfaLoggerFunc, TipsFunc,AfaFlowControl
import AfaDBFunc
#UtilTools,
from types import *

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('����֪ͨ����ǰ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
        
        AfaLoggerFunc.tradeInfo('�ڵ����֪ͨ' )
        sql="UPDATE TIPS_NODECODE SET RUNSTATUS='"+TradeContext.NodeState+\
            "',NOTE2='"+ TradeContext.TroubleReason+\
            "' where NODECODE='"+ TradeContext.TroubleNode+"'"
        AfaLoggerFunc.tradeInfo(sql )
        records=AfaDBFunc.UpdateSqlCmt( sql )
        if( records <0 ):
            AfaLoggerFunc.tradeFatal( sql )
            return AfaFlowControl.ExitThisFlow( 'A0025', '���ݿ���󣬽ڵ���Ϣ������쳣:'+AfaDBFunc.sqlErrMsg )
        if( records ==0 ):
            AfaLoggerFunc.tradeFatal( sql )
            return AfaFlowControl.ExitThisFlow( 'A0027', '���ݿ�����޴˽ڵ���Ϣ:'+AfaDBFunc.sqlErrMsg )

        TradeContext.errorCode = '0000'
        TradeContext.errorMsg = '���׳ɹ�' 
        #=============�Զ����====================
        AfaLoggerFunc.tradeInfo('����֪ͨǰ�������[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        return True
    except Exception, e:
        return TipsFunc.exitMainFlow(str(e))
