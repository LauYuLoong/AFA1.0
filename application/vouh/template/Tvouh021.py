# -*- coding: gbk -*-
###################################################################
#    文    件:    Tvouh021.py
#    说    明:    凭证管理-->查询凭证状态
#    环    境:    中间业务新平台（AFA）--- UNIX: AIX 5.3
#    作    者:    李亚杰
#    公    司:    北京赞同科技
#    创建地址:    安徽
#    创建时间:    2008年6月11日 
#    维护纪录:
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, AfaFlowControl, AfaDBFunc
from types import *
import VouhFunc,HostContext,VouhHostFunc

#=============返回错误码,错误信息===================================
def tradeExit( code, msg ):
    TradeContext.errorCode, TradeContext.errorMsg=code, msg
    if code != '0000':
        return False
    return True

def main( ):
    AfaLoggerFunc.tradeInfo( '凭证使用查询['+TradeContext.TemplateCode+']进入' )

    #=============前台上送数据===================================
    #TradeContext.sVouhNo                                 凭证号码
    #TradeContext.sVouhType                               凭证种类
    #TradeContext.sBESBNO                                 机构号
    #TradeContext.sTellerNo                               柜员号
    #TradeContext.sStartNo                                起始号码
    #TradeContext.sEndNo                                  终止号码
    #TradeContext.sRivTeller                              对方柜员
    #TradeContext.sVouhStatus                             凭证状态
    #TradeContext.sVouhNum                                凭证数量
    #TradeContext.sLstTrxDay                              最后交易日期
    #TradeContext.sLstTrxTime                             最后交易时间
    #TradeContext.sDepository                             库箱标志
    #TradeContext.sVouhName                               凭证名称
    
    try:
        #=============初始化返回报文变量========================
        TradeContext.tradeResponse = []
        
        #=============获取当前系统时间==========================
        TradeContext.sLstTrxDay  = AfaUtilTools.GetSysDate( )
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
        
        #==============判断凭证状态===========================================
        sqlStr = "SELECT VOUHTYPE,VOUHNAME,BESBNO FROM VOUH_PARAMETER WHERE (SUBSTR(BESBNO,1,6) = '"+ (TradeContext.sBesbNo)[:6] +"' \
                    or BESBNO ='3400008887')"
        if (len(TradeContext.sVouhType)!=0 and len(TradeContext.sVouhType)!=0):
            sqlStr = sqlStr + " AND VOUHTYPE = '" + TradeContext.sVouhType + "' AND STATUS = '1'"
        
        AfaLoggerFunc.tradeInfo( 'sqlStr = ' + sqlStr )
        records = AfaDBFunc.SelectSql( sqlStr )
        if( records == None ):
            TradeContext.tradeResponse.append( ['retCount','0'] )
            tradeExit( 'A005052', '查询[凭证参数维护表]操作异常!'  )
            raise AfaFlowControl.flowException( )
        elif( len( records )==0 ):
            TradeContext.tradeResponse.append( ['retCount','0'] )
            tradeExit( 'A005059', '查询[凭证参数维护表]基本信息不存在!' )
            raise AfaFlowControl.flowException( )
        
        #===================判断是否为连续号段=======================================
        
        sqlStr = "select STARTNO,ENDNO,LSTTRXDAY,LSTTRXTIME,RIVTELLER,TELLERNO \
            from VOUH_REGISTER \
            where VOUHTYPE = '" + TradeContext.sVouhType+ "' \
            and BESBNO = '" + TradeContext.sBesbNo + "'\
            and TELLERNO = '" + TradeContext.sTellerTailNo + "'\
            and VOUHSTATUS = '3' \
            and ( ENDNO >= '" + TradeContext.sEndNo + "' and STARTNO <= '" + TradeContext.sStartNo + "' )"
        records = AfaDBFunc.SelectSql( sqlStr )
        AfaLoggerFunc.tradeDebug(sqlStr)
        if( records == None ):          #查询凭证登记表异常
            tradeExit('A005061', '查询[凭证登记表]操作异常!')
            raise AfaFlowControl.flowException( )
        elif( len( records ) == 0 ):    #如果凭证登记表中无对应记录
            tradeExit('A005067', '凭证操作失败,凭证库中不存在本次操作的凭证!')
            raise AfaFlowControl.flowException( )

        TradeContext.sVouhNo=TradeContext.sStartNo


        sqlStr = "select STARTNO,ENDNO from VOUH_REGISTER \
            where TELLERNO = '" + TradeContext.sTellerTailNo + "' \
            and BESBNO = '" + TradeContext.sBesbNo + "'\
            and VOUHTYPE = '" + TradeContext.sVouhType + "'\
            and VOUHSTATUS = '3' \
            and STARTNO = '" + TradeContext.sVouhNo + "'"

        records = AfaDBFunc.SelectSql( sqlStr )
        AfaLoggerFunc.tradeDebug(sqlStr)
        if( records == None ):          #查询凭证登记表异常
            tradeExit('A005061', '查询[凭证登记表]操作异常!')
            raise AfaFlowControl.flowException( )
        elif( len( records ) == 0 ):    #如果凭证登记表中无对应记录
            tradeExit('A005067', '凭证操作失败,凭证库中不存在本次操作的凭证!')
            sStatus = '1'
            #raise AfaFlowControl.flowException( )
        else :
            vouhNos = []
            for i in range(len(records)):
                vouhNos.append(int(records[i][0]))
            if(int(TradeContext.sVouhNo)== min(vouhNos)):
                tradeExit('0000', '凭证号码确认无误！')
                sStatus = '0'
            else:
                tradeExit('A005061', '凭证号码错误!!')
                sStatus = '1'
                #raise AfaFlowControl.flowException( )

        TradeContext.tradeResponse.append( ['sVouhType',TradeContext.sVouhType] )
        TradeContext.tradeResponse.append( ['sVouhName',''] )
        TradeContext.tradeResponse.append( ['sStartNo',TradeContext.sVouhNo] )
        TradeContext.tradeResponse.append( ['sEndNo',TradeContext.sVouhNo] )
        TradeContext.tradeResponse.append( ['sVouhNum','1'] )
        TradeContext.tradeResponse.append( ['sStatus',sStatus] )
        TradeContext.tradeResponse.append( ['sLstTrxDay',TradeContext.sLstTrxDay] )
        TradeContext.tradeResponse.append( ['sLstTrxTime',TradeContext.sLstTrxTime] )
        TradeContext.tradeResponse.append( ['sNum','1'] )
        TradeContext.tradeResponse.append( ['errorCode','0000'] )
        TradeContext.tradeResponse.append( ['errorMsg','交易成功'] )
        #自动打包
        AfaFunc.autoPackData()

        #=============程序退出=========================================
        AfaLoggerFunc.tradeInfo( '凭证使用查询['+TradeContext.TemplateCode+']退出' )
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
