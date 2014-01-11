# -*- coding: gbk -*-
##################################################################
#   ��˰����.���в���֪ͨ(TIPS����)
#=================================================================
#   �����ļ�:   3001_845012.py
#   �޸�ʱ��:   2007-10-18 16:29 
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools, TipsFunc,AfaDBFunc
from types import *

def SubModuleMainFst( ):

    AfaLoggerFunc.tradeInfo( '�������в���֪ͨ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
        #=============��ʼ�����ر��ı���====================
        TradeContext.tradeResponse=[]
        #=============��ȡ��ǰϵͳʱ��====================
        TradeContext.workDate=TipsFunc.GetTipsDate( )
        TradeContext.workTime=UtilTools.GetSysTime( )

        if( TradeContext.existVariable( "ListNum" ) ):
            ListNum=int(TradeContext.ListNum)
            AfaLoggerFunc.tradeInfo('listNum:'+TradeContext.ListNum)
            recNum_curr=0
            for j in range( 0, ListNum ): 
                if ListNum == 1 :
                    recNum=int(TradeContext.recNum)
                else:
                    recNum=int(TradeContext.recNum[j])
                
                AfaLoggerFunc.tradeInfo('recNum['+str(j)+']:'+str(recNum))
                for i in range( 0, recNum ): 
                    if len(TradeContext.DetailNo[recNum_curr+i])==0:
                        break
                    sql="select PARAMTYPENO,PARAMTYPEDESC,DETAILNO,DETAILDESC,PARAMVALUE from TIPS_RUNPARAM "
                    sql=sql+" where "
                    if ListNum == 1 :
                        sql=sql+"PARAMTYPENO='"+TradeContext.ParamTypeNo      +"'"
                    else:
                        sql=sql+"PARAMTYPENO='"+TradeContext.ParamTypeNo[j]      +"'"
                    sql=sql+"and DetailNo='"+TradeContext.DetailNo[recNum_curr+i]      +"'"
                    AfaLoggerFunc.tradeInfo(sql)
                    records = AfaDBFunc.SelectSql(sql)
                    if( records == None ):
                        AfaLoggerFunc.tradeFatal(sql)
                        return TipsFunc.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
                    #����
                    if( len( records )==0 ):
                        sql="insert into TIPS_RUNPARAM(WORKDATE,ParamTypeNo,ParamTypeDesc,DetailNo,DetailDesc,ParamValue)"
                        sql=sql+" values"
                        sql=sql+"('"+TradeContext.workDate      +"'"
                        if ListNum == 1 :
                            sql=sql+",'"+TradeContext.ParamTypeNo      +"'"
                        else:
                            sql=sql+",'"+TradeContext.ParamTypeNo[j]      +"'"
                        if ListNum == 1 :
                            sql=sql+",'"+TradeContext.ParamTypeDesc      +"'"
                        else:
                            sql=sql+",'"+TradeContext.ParamTypeDesc[j]      +"'"
                        sql=sql+",'"+TradeContext.DetailNo[recNum_curr+i]      +"'"
                        sql=sql+",'"+TradeContext.DetailDesc[recNum_curr+i]        +"'"
                        sql=sql+",'"+TradeContext.ParamValue[recNum_curr+i]       +"'"
                        sql=sql+")"
                        AfaLoggerFunc.tradeInfo(sql)
                        if( AfaDBFunc.InsertSqlCmt(sql) == -1 ):
                            AfaLoggerFunc.tradeFatal(sql)
                            TipsFunc.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
                            return False 
                    else:#����
                        sql="update TIPS_RUNPARAM set "
                        sql=sql+" WORKDATE ='"+TradeContext.workDate      +"'"
                        if ListNum == 1 :
                            sql=sql+",ParamTypeDesc ='"+TradeContext.ParamTypeDesc      +"'"
                        else:
                            sql=sql+",ParamTypeDesc ='"+TradeContext.ParamTypeDesc[j]      +"'"
                        sql=sql+",DetailDesc    ='"+TradeContext.DetailDesc[recNum_curr+i]     +"'"
                        sql=sql+",ParamValue    ='"+TradeContext.ParamValue[recNum_curr+i]     +"'"
                        if ListNum == 1 :
                            sql=sql+" WHERE ParamTypeNo ='"+TradeContext.ParamTypeNo      +"'"
                        else:
                            sql=sql+" WHERE ParamTypeNo ='"+TradeContext.ParamTypeNo[j]      +"'"
                        sql=sql+" and DetailNo      ='"+TradeContext.DetailNo[recNum_curr+i]      +"'"
                        AfaLoggerFunc.tradeInfo(sql)
                        if( AfaDBFunc.UpdateSqlCmt(sql) == -1 ):
                            AfaLoggerFunc.tradeFatal(sql)
                            TipsFunc.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
                            return False 
                recNum_curr = recNum_curr + recNum
                
        #=============�Զ����==================== 
        TradeContext.errorCode='0000'
        TradeContext.errorMsg='���׳ɹ�'
        TipsFunc.autoPackData()
        #=============�����˳�====================
        AfaLoggerFunc.tradeInfo( '�˳����в���֪ͨ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']\n' )
        return True
    except TipsFunc.flowException, e:
        return TipsFunc.exitMainFlow( )
    except TipsFunc.accException:
        return TipsFunc.exitMainFlow( )
    except Exception, e:
        return TipsFunc.exitMainFlow(str(e))  
def SubModuleMainSnd():
    return True   