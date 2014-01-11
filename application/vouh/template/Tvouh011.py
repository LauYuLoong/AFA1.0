# -*- coding: gbk -*-
####################################################################
#    文    件:    Tvouh011.py
#    说    明:    凭证管理.查询凭证库存交易
#    环    境:    中间业务新平台（AFA）--- UNIX: AIX 5.3
#    作    者:    李亚杰
#    公    司:    北京赞同科技
#    创建地址:    安徽
#    创建时间:    2008年6月16日
#    维护纪录:
#####################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc,AfaFlowControl,AfaDBFunc
from types import *
import HostContext,VouhHostFunc,VouhFunc

def tradeExit( code, msg ):
    TradeContext.errorCode, TradeContext.errorMsg=code, msg
    if code != '0000':
        return False
    return True
    
def main( ):
    
    AfaLoggerFunc.tradeInfo( '查询凭证库存交易['+TradeContext.TemplateCode+']进入' )
    
    #=============前台上送数据====================
    #TradeContext.sBesbNo           机构号
    #TradeContext.sTellerNo         柜员号
    #TradeContext.sVouhType         凭证种类
    #TradeCoutext.sVouhStatus       凭证状态
    #TradeCoutext.sStartDate        起始日期
    #TradeCoutext.sEndDate          终止日期
    #TradeContext.sStart          起始记录数
    #TradeContext.arraySize         查询条数
    
    try:
        #=============初始化返回报文变量==================
        TradeContext.tradeResponse = []

        #=============获取当前系统时间====================
        TradeContext.sLstTrxDay = AfaUtilTools.GetSysDate( )
        TradeContext.sLstTrxTime = AfaUtilTools.GetSysTime( ) 
        
        #begin凭证优化更改201109  
        #=============获取柜员尾箱号===============================
        HostContext.I1SBNO = TradeContext.sBesbNo         #机构号
        HostContext.I1USID = TradeContext.sTellerNo       #柜员号
        HostContext.I1WSNO = TradeContext.sWSNO           #终端号
        HostContext.I1EDDT = TradeContext.sLstTrxDay      #终止日期
        HostContext.I1TELR = TradeContext.sTellerNo       #柜员代号
        
        if(not VouhHostFunc.CommHost('0104')):
            VouhFunc.tradeExit( TradeContext.errorCode, TradeContext.errorMsg )
            raise AfaFlowControl.flowException( )
        if(TradeContext.errorCode == '0000'):
            TradeContext.sTellerTailNobak = HostContext.O2CABO
            TradeContext.sTellerTailNo    = TradeContext.sTellerTailNobak[0]                 
            AfaLoggerFunc.tradeInfo( '交易柜员尾箱号：' + TradeContext.sTellerTailNo ) 
        #end   
        
        wheresql="substr(t1.BESBNO,1,6) = substr(t.BESBNO,1,6) AND t1.VOUHTYPE = t.VOUHTYPE AND t.VOUHSTATUS in ('0','2')"
        
        #==============设机构号=====================
        if (TradeContext.existVariable("sSelBesbNo") and len(TradeContext.sSelBesbNo) <> 0 ):
            wheresql = wheresql + " and t.BESBNO = '" + TradeContext.sSelBesbNo + "'"
            
        #==============设凭证种类=====================
        if (TradeContext.existVariable("sVouhType") and len(TradeContext.sVouhType) <> 0 ):
            wheresql = wheresql + " and t.VOUHTYPE = '" + TradeContext.sVouhType + "'"
        
        sqlStr = "SELECT TELLERNO,VOUHTYPE,STARTNO,ENDNO,VOUHNUM,VOUHNAME \
            FROM ( \
                    SELECT row_number() over() as rowid,t.TELLERNO,t.VOUHTYPE,t.STARTNO,t.ENDNO,t.VOUHNUM,t1.VOUHNAME \
                    FROM VOUH_REGISTER t,VOUH_PARAMETER t1 \
                    WHERE " + wheresql + " \
            ) as tab1 \
            where tab1.rowid >= " + str(TradeContext.sStart)
        
        AfaLoggerFunc.tradeDebug(sqlStr);
        #查询数据库并将返回的结果压至对应变量中
        records = AfaDBFunc.SelectSql( sqlStr, int(TradeContext.arraySize))
        if( records == None ):
            tradeExit('A005067', '查询[凭证登记表]操作异常!')
            raise AfaFlowControl.flowException( )
        elif( len( records ) == 0 ):
            tradeExit('A005068', '凭证不存在!' )
            raise AfaFlowControl.flowException( )
        else :
            record=AfaUtilTools.ListFilterNone( records )
            total=len( records )

            sTellerTailNo = ''
            sVouhType = ''
            sStartNo = ''
            sEndNo = ''
            sVouhNum = ''
            sVouhName = ''
            
            for i in range( 0, total ):
                if( i <> 0):
                    strSplit = '|'
                else:
                    strSplit = ''
                sTellerTailNo = sTellerTailNo + strSplit + records[i][0]
                sVouhType = sVouhType + strSplit + records[i][1]
                sStartNo = sStartNo + strSplit + records[i][2]
                sEndNo = sEndNo + strSplit + records[i][3]
                sVouhNum = sVouhNum + strSplit + records[i][4]
                sVouhName = sVouhName + strSplit + records[i][5]
                
        TradeContext.tradeResponse.append( ['sVouhType',sVouhType] )
        TradeContext.tradeResponse.append( ['sVouhName',sVouhName] )
        TradeContext.tradeResponse.append( ['sStartNo',sStartNo] )
        TradeContext.tradeResponse.append( ['sEndNo',sEndNo] )
        TradeContext.tradeResponse.append( ['sVouhNum',sVouhNum] )
        TradeContext.tradeResponse.append( ['sTellerTailNo',TradeContext.sTellerTailNo] ) 
        TradeContext.tradeResponse.append( ['sTellerNo',TradeContext.sTellerNo] )           #凭证优化更改201109  柜员代号新增   
        TradeContext.tradeResponse.append( ['sLstTrxDay',TradeContext.sLstTrxDay] )
        TradeContext.tradeResponse.append( ['sLstTrxTime',TradeContext.sLstTrxTime] )
        TradeContext.tradeResponse.append( ['sNum',str(total)] )
        TradeContext.tradeResponse.append( ['errorCode','0000'] )
        TradeContext.tradeResponse.append( ['errorMsg','交易成功'] )

        AfaFunc.autoPackData()
        #=============程序退出====================
        AfaLoggerFunc.tradeInfo( '查询凭证库存交易['+TradeContext.TemplateCode+']退出' )
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))

  
