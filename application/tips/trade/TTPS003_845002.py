# -*- coding: gbk -*-
##################################################################
#   中间业务平台.财税库行_冲正
#=================================================================
#   程序文件:   TPS003_845002.py
#   修改时间:   2008-5-3 16:26
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools, TipsFunc    
import AfaDBFunc
from types import *

def SubModuleDealFst( ):
    AfaLoggerFunc.tradeInfo('进入缴费反交易[TPS003_845002]数据预查询' )
    #====判断应用状态=======
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
        return TipsFunc.ExitThisFlow( 'A0045', '未发现原交易' )
    else: 
        if tmp[0][6]=='1':
            return TipsFunc.ExitThisFlow( 'A0045', '原交易未成功' )
        if tmp[0][6]=='3':
            return TipsFunc.ExitThisFlow( 'A0045', '原交易已冲正' )
        else:
            tmp=UtilTools.ListFilterNone( tmp )
            TradeContext.taxPayCode     =tmp[0][0]   #用户号
            TradeContext.amount         =tmp[0][1]   #金额
            TradeContext.preAgentSerno  =tmp[0][2]   #原交易流水号
            TradeContext.zoneno         =tmp[0][3]    
            TradeContext.brno           =tmp[0][4]    
            TradeContext.teller         =tmp[0][5]    
            #TradeContext.appNo          =tmp[0][9]    
    AfaLoggerFunc.tradeInfo('退出缴费反交易[T004203_031021]数据预查询' )
    return True
def SubModuleDealSnd( ):
    return True  
def SubModuleDealThd( ):
    return True   
    
