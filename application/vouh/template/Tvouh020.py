# -*- coding: gbk -*-

####################################################################
#    文    件:    Tvouh020.py
#    说    明:    凭证管理.查询明细交易根据流水号
#    环    境:    中间业务新平台（AFA）--- UNIX: AIX 5.3
#    作    者:    李亚杰
#    公    司:    北京赞同科技
#    创建地址:    安徽
#    创建时间:    2008年6月15日
#    维护纪录:
####################################################################

import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc,AfaFlowControl,AfaDBFunc
from types import *
#import AfaLoggerFunc

def tradeExit( code, msg ):
    TradeContext.errorCode, TradeContext.errorMsg=code, msg
    if code != '0000':
        return False
    return True

def main( ):
    
    AfaLoggerFunc.tradeInfo( '查询明细交易根据流水号['+TradeContext.TemplateCode+']进入' )
    
    #=============前台上送数据====================
    #TradeContext.oVouhSerial           原流水号 
    #TradeContext.sVouhType             凭证种类
    #TradeContext.sStartNo              起始号码
    #TradeContext.sEndNo                终止号码 
    #TradeContext.sVouhNum              凭证数量
    
    try:
        #=============初始化返回报文变量==================
        TradeContext.tradeResponse = []

        #=============获取当前系统时间====================
        TradeContext.sLstTrxDay = AfaUtilTools.GetSysDate( )
        TradeContext.sLstTrxTime = AfaUtilTools.GetSysTime( ) 
        
        #根据前台输入的凭证种类进行查询并返回前台
        sqlStr = "select distinct t.VOUHTYPE,t1.VOUHNAME,t.TELLERNO,t.STARTNO,t.ENDNO,t.VOUHNUM FROM VOUH_MODIFY t,VOUH_PARAMETER t1 \
                 where VOUHSERIAL='"+TradeContext.sVouhSerial+"' AND t.VOUHTYPE = t1.VOUHTYPE AND substr(t.BESBNO,1,6) = substr(t1.BESBNO,1,6) \
                 AND TRANSTYPE not like '%撤销' AND TRANSTATUS = '0'"

        AfaLoggerFunc.tradeDebug(sqlStr);
        #查询数据库并将返回的结果压至对应变量中
        records = AfaDBFunc.SelectSql( sqlStr )
        if( records == None ):
            tradeExit('A005067', '查询[凭证变更登记表]操作异常!')
            raise AfaFlowControl.flowException( )
        elif( len( records ) == 0 ):
            tradeExit('A005068', '凭证不存在!' )
            raise AfaFlowControl.flowException( )
        else :
            record=AfaUtilTools.ListFilterNone( records )
            total=len( records )
            
            sVouhType = ''
            sVouhName = ''
            sTellerNo = ''
            sStartNo = ''
            sEndNo = ''
            sVouhNum = ''
            
            for i in range( 0, total ):
                if( i <> 0):
                    strSplit = '|'
                else:
                    strSplit = ''
                sVouhType = sVouhType + strSplit + records[i][0]
                sVouhName = sVouhName + strSplit + records[i][1]
                sTellerNo = sTellerNo + strSplit + records[i][2]
                sStartNo = sStartNo + strSplit + records[i][3]
                sEndNo = sEndNo + strSplit + records[i][4]
                sVouhNum = sVouhNum + strSplit + records[i][5]
                
        TradeContext.tradeResponse.append( ['oVouhSerial',TradeContext.sVouhSerial] )
        TradeContext.tradeResponse.append( ['sVouhType',sVouhType] )
        TradeContext.tradeResponse.append( ['sVouhName',sVouhName] )
        TradeContext.tradeResponse.append( ['oTellerNo',sTellerNo] )
        TradeContext.tradeResponse.append( ['sStartNo',sStartNo] )
        TradeContext.tradeResponse.append( ['sEndNo',sEndNo] )
        TradeContext.tradeResponse.append( ['sVouhNum',sVouhNum] )
        TradeContext.tradeResponse.append( ['sLstTrxDay',TradeContext.sLstTrxDay] )
        TradeContext.tradeResponse.append( ['sLstTrxTime',TradeContext.sLstTrxTime] )
        TradeContext.tradeResponse.append( ['sNum',str(total)] )
        TradeContext.tradeResponse.append( ['errorCode','0000'] )
        TradeContext.tradeResponse.append( ['errorMsg','交易成功'] )

        AfaFunc.autoPackData()
        #=============程序退出====================
        AfaLoggerFunc.tradeInfo( '查询明细交易根据流水号['+TradeContext.TemplateCode+']退出' )
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))

  
