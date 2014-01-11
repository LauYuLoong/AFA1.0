# -*- coding: gbk -*-
###################################################################
#    文    件:    Tvouh025.py
#    说    明:    凭证管理-->凭证柜员交接
#    环    境:    中间业务新平台（AFA）--- UNIX: AIX 5.3
#    作    者:    李亚杰
#    公    司:    北京赞同科技
#    创建地址:    安徽
#    创建时间:    2008年6月11日 
#    维护纪录:   
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, AfaFlowControl, AfaDBFunc
from types import *
import AfaLoggerFunc,VouhFunc,binascii,HostContext,VouhHostFunc


def main( ):
    AfaLoggerFunc.tradeInfo( '凭证柜员交接['+TradeContext.TemplateCode+']进入' )

    #=============前台上送数据===================================
    #TradeContext.sBesbNo                                 机构号
    #TradeContext.sBesbSty                                机构类型
    #TradeContext.sCur                                    货币代码
    #TradeContext.sTellerNo                               柜员号
    #TradeContext.sRivTeller                              对方柜员
    #TradeContext.sLstTrxDay                              最后交易日期
    #TradeContext.sLstTrxTime                             最后交易时间
    
    try: 
        #=============获取柜员级别==========================
        HostContext.I1TELR = TradeContext.sTellerNo       #柜员号
        HostContext.I1SBNO = TradeContext.sBesbNo         #机构号
        HostContext.I1USID = TradeContext.sTellerNo       #柜员号
        HostContext.I1WSNO = TradeContext.sWSNO           #终端号
        if(not VouhHostFunc.CommHost('8809')):
            tradeExit(TradeContext.errorCode, TradeContext.errorMsg)
            raise AfaFlowControl.flowException( )
        if(TradeContext.errorCode == '0000'):
            TELLER = HostContext.O1TLRK
            AfaLoggerFunc.tradeInfo( TELLER )
        
        #=============初始化返回报文变量========================
        TradeContext.tradeResponse = []
        TradeContext.sRivTeller = TradeContext.sInTellerNo
        
        #=============生成流水号========================
        TradeContext.sVouhSerial = VouhFunc.GetVouhSerial( )

        #=============获取当前系统时间==========================
        TradeContext.sLstTrxDay  = AfaUtilTools.GetSysDate( )
        TradeContext.sLstTrxTime = AfaUtilTools.GetSysTime( )

        TradeContext.sTransType    = '凭证柜员交接'
        
        #================判断对方柜员是否有凭证==================================
        if(len(TradeContext.sInTellerNo) == 0):
            VouhFunc.tradeExit('A005061', '对方柜员不能为空!')
            raise AfaFlowControl.flowException( )
        
        #if(TELLER == '01' or TELLER == '02' or TELLER == '03'):
        #    VouhFunc.tradeExit('A005061', '该柜员不能进行此操作!')
        #    raise AfaFlowControl.flowException( )
            
        sqlStr = "select * from VOUH_REGISTER where TELLERNO = '" + TradeContext.sInTellerNo + "' and VOUHSTATUS = '3'"
        
        records = AfaDBFunc.SelectSql( sqlStr )
        AfaLoggerFunc.tradeDebug(sqlStr)
        if records==-1 :
            VouhFunc.tradeExit( 'A005057', '查询[凭证登记表]信息异常!' )
            raise AfaFlowControl.flowException( )
        elif len(records) > 0 :
            VouhFunc.tradeExit( 'A005058', '['+TradeContext.sInTellerNo+']柜员不能交接!' )
            raise AfaFlowControl.flowException( )
        
        #================判断柜员是否有凭证==================================
        
        #if((TradeContext.sTellerNo)[4:] == '01' or (TradeContext.sTellerNo)[4:] == '02' or (TradeContext.sTellerNo)[4:] == '03'):
        #    VouhFunc.tradeExit('A005061', '该柜员不能进行此操作!')
        #    raise AfaFlowControl.flowException( )
            
        sqlStr = "select * from VOUH_REGISTER where TELLERNO = '" + TradeContext.sTellerNo + "' and VOUHSTATUS = '3'"
        
        records = AfaDBFunc.SelectSql( sqlStr )
        AfaLoggerFunc.tradeDebug(sqlStr)
        if records==-1 :
            VouhFunc.tradeExit( 'A005057', '查询[凭证登记表]信息异常!' )
            raise AfaFlowControl.flowException( )
        elif records==0 :
            VouhFunc.tradeExit( 'A005058', '无凭证!' )
            raise AfaFlowControl.flowException( )
        
        #======================柜员交接=====================================
        sqlStr = "update VOUH_REGISTER set TELLERNO = '" + TradeContext.sInTellerNo + "' where TELLERNO = '" + TradeContext.sTellerNo + "' and VOUHSTATUS = '3'"
        
        records = AfaDBFunc.UpdateSqlCmt( sqlStr )
        AfaLoggerFunc.tradeDebug(sqlStr)
        if records==-1 :
            VouhFunc.tradeExit( 'A005057', '更新[凭证登记表]信息异常!' )
            raise AfaFlowControl.flowException( )
        elif records==0 :
            VouhFunc.tradeExit( 'A005058', '修改[凭证登记表]基本信息失败!' )
            raise AfaFlowControl.flowException( )

        #更新凭证变更登记表
        VouhFunc.VouhModify()
        #数据库提交
        AfaDBFunc.CommitSql( )
        
        #==================查询交接凭证明细==================================
	#=====李亚杰  20080812  修改凭证查询条件,增加凭证状态为'3'的情况====
        #sqlStr = "select distinct t.VOUHTYPE,t1.VOUHNAME,t.STARTNO,t.ENDNO,t.VOUHNUM FROM VOUH_REGISTER t,VOUH_PARAMETER t1 \
        #         where t.VOUHTYPE = t1.VOUHTYPE AND substr(t.BESBNO,1,6) = substr(t1.BESBNO,1,6) \
        #         AND t.TELLERNO = '" + TradeContext.sInTellerNo + "'"

        sqlStr = "select distinct t.VOUHTYPE,t1.VOUHNAME,t.STARTNO,t.ENDNO,t.VOUHNUM FROM VOUH_REGISTER t,VOUH_PARAMETER t1 \
                 where t.VOUHTYPE = t1.VOUHTYPE AND substr(t.BESBNO,1,6) = substr(t1.BESBNO,1,6) \
                 AND t.VOUHSTATUS = '3' AND t.TELLERNO = '" + TradeContext.sInTellerNo + "'"

        AfaLoggerFunc.tradeDebug(sqlStr);
        #查询数据库并将返回的结果压至对应变量中
        records = AfaDBFunc.SelectSql( sqlStr )
        if( records == None ):
            VouhFunc.tradeExit('A005067', '查询[凭证表]操作异常!')
            raise AfaFlowControl.flowException( )
        elif( len( records ) == 0 ):
            VouhFunc.tradeExit('A005068', '凭证不存在!' )
            raise AfaFlowControl.flowException( )
        else :
            record=AfaUtilTools.ListFilterNone( records )
            total=len( records )
            
            sVouhType = ''
            sVouhName = ''
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
                sStartNo = sStartNo + strSplit + records[i][2]
                sEndNo = sEndNo + strSplit + records[i][3]
                sVouhNum = sVouhNum + strSplit + records[i][4]
                
        TradeContext.tradeResponse.append( ['sVouhType',sVouhType] )
        TradeContext.tradeResponse.append( ['sVouhName',sVouhName] )
        TradeContext.tradeResponse.append( ['sTellerNo',TradeContext.sTellerNo] )
        TradeContext.tradeResponse.append( ['sInTellerNo',TradeContext.sInTellerNo] )
        TradeContext.tradeResponse.append( ['sStartNo',sStartNo] )
        TradeContext.tradeResponse.append( ['sEndNo',sEndNo] )
        TradeContext.tradeResponse.append( ['sVouhNum',sVouhNum] )
        TradeContext.tradeResponse.append( ['sNum',str(total)] )
        TradeContext.tradeResponse.append( ['sVouhSerial',TradeContext.sVouhSerial] )
        TradeContext.tradeResponse.append( ['sLstTrxDay',TradeContext.sLstTrxDay] )
        TradeContext.tradeResponse.append( ['sLstTrxTime',TradeContext.sLstTrxTime] )
        TradeContext.tradeResponse.append( ['errorCode','0000'] )
        TradeContext.tradeResponse.append( ['errorMsg','交易成功'] )

        #自动打包
        AfaFunc.autoPackData()

        #=============程序退出====================
        AfaLoggerFunc.tradeInfo( '凭证柜员交接['+TradeContext.TemplateCode+']退出' )
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))

