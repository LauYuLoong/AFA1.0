# -*- coding: gbk -*-
##################################################################
#   ��˰����.���ɸ�ʽ���Ľ��ս���(TIPS����)
#=================================================================
#   �����ļ�:   TTPS001_845013.py
#   �޸�ʱ��:   2007-10-18 16:29 
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools, TipsFunc,AfaDBFunc
from types import *

def SubModuleMainFst( ):

    AfaLoggerFunc.tradeInfo( '�������ɸ�ʽ���Ľ��ս���[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
        #=============��ʼ�����ر��ı���====================
        TradeContext.tradeResponse=[]
        
        sql="insert into TIPS_NOTE(WORKDATE,WORKTIME,SRCNODECODE,DESNODECODE,SENDORGCODE,RCVORGCODE,CONTENT)"
        sql=sql+" values"
        sql=sql+"('"+TradeContext.workDate      +"'"
        sql=sql+",'"+TradeContext.workTime      +"'"
        sql=sql+",'"+TradeContext.SrcNodeCode   +"'"
        sql=sql+",'"+TradeContext.DesNodeCode   +"'"
        sql=sql+",'"+TradeContext.SendOrgCode   +"'"
        sql=sql+",'"+TradeContext.RcvOrgCode    +"'"
        sql=sql+",'"+TradeContext.Content       +"'"
        sql=sql+")"
        AfaLoggerFunc.tradeInfo(sql)
        if( AfaDBFunc.InsertSqlCmt(sql) == -1 ):
            AfaLoggerFunc.tradeFatal(sql)
            TipsFunc.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
            return False 

        #=============�Զ����==================== 
        TradeContext.errorCode='0000'
        TradeContext.errorMsg='���׳ɹ�'
        TipsFunc.autoPackData()
        #=============�����˳�====================
        AfaLoggerFunc.tradeInfo( '�˳����ɸ�ʽ���Ľ��ս���[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']\n' )
        return True
    except TipsFunc.flowException, e:
        return TipsFunc.exitMainFlow( )
    except TipsFunc.accException:
        return TipsFunc.exitMainFlow( )
    except Exception, e:
        return TipsFunc.exitMainFlow(str(e))  
def SubModuleMainSnd():
    return True   