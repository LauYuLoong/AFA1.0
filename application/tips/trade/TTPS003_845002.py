# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.��˰����_����
#=================================================================
#   �����ļ�:   TPS003_845002.py
#   �޸�ʱ��:   2008-5-3 16:26
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools, TipsFunc    
import AfaDBFunc
from types import *

def SubModuleDealFst( ):
    AfaLoggerFunc.tradeInfo('����ɷѷ�����[TPS003_845002]����Ԥ��ѯ' )
    #====�ж�Ӧ��״̬=======
    if not TipsFunc.ChkAppStatus():
        return False
    sqlstr="SELECT TAXPAYCODE,AMOUNT,SERIALNO,ZONENO,BRNO,TELLERNO,BANKSTATUS,CORPSTATUS FROM TIPS_MAINTRANSDTL WHERE "
    sqlstr=sqlstr + " WORKDATE='"+TradeContext.workDate+ "' AND  REVTRANF='0'"
    sqlstr=sqlstr + "AND CORPSERNO='"+TradeContext.preCorpSerno+"'"
    AfaLoggerFunc.tradeInfo( sqlstr )
    tmp = AfaDBFunc.SelectSql( sqlstr )
    if tmp == None :
        return TipsFunc.ExitThisFlow( 'A0025', AfaDBFunc.sqlErrMsg )
    elif len( tmp ) == 0 :
        AfaLoggerFunc.tradeFatal( sqlstr )
        return TipsFunc.ExitThisFlow( 'A0045', 'δ����ԭ����' )
    else: 
        if tmp[0][6]=='1':
            return TipsFunc.ExitThisFlow( 'A0045', 'ԭ����δ�ɹ�' )
        if tmp[0][6]=='3':
            return TipsFunc.ExitThisFlow( 'A0045', 'ԭ�����ѳ���' )
        else:
            tmp=UtilTools.ListFilterNone( tmp )
            TradeContext.taxPayCode     =tmp[0][0]   #�û���
            TradeContext.amount         =tmp[0][1]   #���
            TradeContext.preAgentSerno  =tmp[0][2]   #ԭ������ˮ��
            TradeContext.zoneno         =tmp[0][3]    
            TradeContext.brno           =tmp[0][4]    
            TradeContext.teller         =tmp[0][5]    
            #TradeContext.appNo          =tmp[0][9]    
    AfaLoggerFunc.tradeInfo('�˳��ɷѷ�����[T004203_031021]����Ԥ��ѯ' )
    return True
def SubModuleDealSnd( ):
    return True  
def SubModuleDealThd( ):
    return True   
    
