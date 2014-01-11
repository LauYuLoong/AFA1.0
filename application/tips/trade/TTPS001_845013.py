# -*- coding: gbk -*-
##################################################################
#   财税库行.自由格式报文接收交易(TIPS发起)
#=================================================================
#   程序文件:   TTPS001_845013.py
#   修改时间:   2007-10-18 16:29 
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools, TipsFunc,AfaDBFunc
from types import *

def SubModuleMainFst( ):

    AfaLoggerFunc.tradeInfo( '进入自由格式报文接收交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
        #=============初始化返回报文变量====================
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
            TipsFunc.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
            return False 

        #=============自动打包==================== 
        TradeContext.errorCode='0000'
        TradeContext.errorMsg='交易成功'
        TipsFunc.autoPackData()
        #=============程序退出====================
        AfaLoggerFunc.tradeInfo( '退出自由格式报文接收交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']\n' )
        return True
    except TipsFunc.flowException, e:
        return TipsFunc.exitMainFlow( )
    except TipsFunc.accException:
        return TipsFunc.exitMainFlow( )
    except Exception, e:
        return TipsFunc.exitMainFlow(str(e))  
def SubModuleMainSnd():
    return True   