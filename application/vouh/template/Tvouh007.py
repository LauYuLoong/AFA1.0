# -*- coding: gbk -*-
###################################################################
#    文    件:    Tvouh007.py
#    说    明:    凭证管理-->凭证上缴
#    环    境:    中间业务新平台（AFA）--- UNIX: AIX 5.3
#    作    者:    李亚杰
#    公    司:    北京赞同科技
#    创建地址:    安徽
#    创建时间:    2008年6月11日 
#    维护纪录:   
##################################################################
import TradeContext,  AfaUtilTools, AfaFunc, AfaFlowControl, AfaDBFunc
from types import *
import AfaLoggerFunc,VouhFunc,HostContext,VouhHostFunc

def main( ):
    AfaLoggerFunc.tradeInfo( '凭证上缴入库['+TradeContext.TemplateCode+']进入' )

    #=============前台上送数据===================================
    #TradeContext.sBesbNo                                 机构号
    #TradeContext.sBesbSty                                机构类型
    #TradeContext.sCur                                    货币代码
    #TradeContext.sTellerNo                               柜员号
    #TradeContext.sVouhType                               凭证种类
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
        #=====================获取机构类型===============================
        #TradeContext.sBesbSty = VouhFunc.SelectBesbSty(TradeContext.sBesbNo)
        
        #=============获取机构类型==========================
        HostContext.I1OTSB = TradeContext.sBesbNo         #机构号
        HostContext.I1SBNO = TradeContext.sBesbNo         #机构号
        HostContext.I1USID = TradeContext.sTellerNo       #柜员号
        HostContext.I1WSNO = TradeContext.sWSNO           #终端号
        if(not VouhHostFunc.CommHost('2001')):
            tradeExit(TradeContext.errorCode, TradeContext.errorMsg)
            raise AfaFlowControl.flowException( )
        if(TradeContext.errorCode == '0000'):
            SBNO = HostContext.O1SBCH
            AfaLoggerFunc.tradeInfo( SBNO )
        
        #================拆包========================
        TradeContext.sVouhType = VouhFunc.DelSpace(TradeContext.sVouhType.split("|"))
        TradeContext.sVouhName = VouhFunc.DelSpace(TradeContext.sVouhName.split("|"))
        TradeContext.sStartNo  = VouhFunc.DelSpace(TradeContext.sStartNo.split("|"))
        TradeContext.sEndNo    = VouhFunc.DelSpace(TradeContext.sEndNo.split("|"))
        TradeContext.sVouhNum  = VouhFunc.DelSpace(TradeContext.sVouhNum.split("|"))
        TradeContext.sNum      = len(TradeContext.sVouhType)
        
        #==================暂存==================================
        TradeContext.rVouhType = VouhFunc.AddSplit(TradeContext.sVouhType)
        TradeContext.rVouhName = VouhFunc.AddSplit(TradeContext.sVouhName)
        TradeContext.rStartNo  = VouhFunc.AddSplit(TradeContext.sStartNo)
        TradeContext.rEndNo    = VouhFunc.AddSplit(TradeContext.sEndNo)
        TradeContext.rVouhNum  = VouhFunc.AddSplit(TradeContext.sVouhNum)
        
        #=============生成流水号========================
        TradeContext.sVouhSerial = VouhFunc.GetVouhSerial( )

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
        
        #=============获取领用柜员尾箱号===============================
        HostContext.I1SBNO = TradeContext.sBesbNo           #机构号  机构号送交易机构号 
        #HostContext.I1USID = TradeContext.sInTellerNo      #柜员号
        HostContext.I1USID = '999996'                       #柜员号  柜员号送自动柜员
        HostContext.I1WSNO = TradeContext.sWSNO             #终端号
        HostContext.I1EDDT = TradeContext.sLstTrxDay        #终止日期
        HostContext.I1TELR = TradeContext.sInTellerNo       #柜员代号
        
        if(not VouhHostFunc.CommHost('0104')):
            VouhFunc.tradeExit( TradeContext.errorCode, TradeContext.errorMsg )
            raise AfaFlowControl.flowException( )
        if(TradeContext.errorCode == '0000'):
            TradeContext.sInTellerTailNobak = HostContext.O2CABO
            TradeContext.sInTellerTailNo    = TradeContext.sInTellerTailNobak[0]                 
            AfaLoggerFunc.tradeInfo( '领用柜员尾箱号：' + TradeContext.sInTellerTailNo ) 
        #end 
        
        #=============初始化返回报文变量========================
        TradeContext.tradeResponse = []
        TradeContext.sRivTeller = TradeContext.sInTellerTailNo

        #=============置凭证操作状态及库箱标志====================
        TradeContext.sExDepos  = '4' #原库箱标志   1.分行管理库 2.支行管理库 3.网点管理库 4.柜员凭证箱
        if(SBNO=='31' or SBNO=='40' or SBNO=='32'):
            TradeContext.sDepository = '2' #库箱标志
        elif(SBNO=='50'):
            TradeContext.sDepository = '3' #库箱标志
        else:
            VouhFunc.tradeExit('A005061', '该机构柜员不能进行此操作!')
            raise AfaFlowControl.flowException( )
        
        TradeContext.sVouhStatus  = '2' #状态       2.已发未领3.已领未用     
        TradeContext.sExStatus    = '3' #原状态     3.已领未用时，可以凭证上缴，上缴后为2.已发未领
        TradeContext.sTransType    = '凭证上缴'
        TradeContext.sInBesbNo    = TradeContext.sBesbNo
        
        tellerNo = TradeContext.sTellerTailNo
        TradeContext.sTellerTailNo = TradeContext.sInTellerTailNo
        TradeContext.sInTellerTailNo = tellerNo
        
        if(SBNO <> '31' and SBNO <> '32' and SBNO <> '40' and SBNO <> '50' ):
            tradeExit( 'A0001', '该机构柜员不能进行此操作!' )
            raise AfaFlowControl.flowException( )

        #交易公共部分    
        VouhFunc.VouhTrans()

        #更新凭证变更登记表
        VouhFunc.VouhModify()
       
        #数据库提交
        AfaDBFunc.CommitSql( )
        
        TradeContext.sInTellerTailNo = TradeContext.sTellerTailNo
        TradeContext.sTellerTailNo = tellerNo
        
        #主机记账
        AfaLoggerFunc.tradeInfo( '------------主机记账' )
        TradeContext.sOperSty = '3'
        VouhHostFunc.VouhCommHost()
        TradeContext.sTranStatus = '0'
        AfaLoggerFunc.tradeInfo( '=======================12'+TradeContext.errorCode )
        #TradeContext.errorCode = '0000'
        if(TradeContext.errorCode <> '0000'):
            tmpErrorCode= TradeContext.errorCode
            tmpErrorMsg = TradeContext.errorMsg
        
            #冲正
            
            #=============置凭证操作状态及库箱标志====================
            tmpDepos = TradeContext.sDepository
            TradeContext.sDepository = TradeContext.sExDepos
            TradeContext.sExDepos = tmpDepos

            tmpStatus = TradeContext.sVouhStatus
            TradeContext.sVouhStatus = TradeContext.sExStatus
            TradeContext.sExStatus = tmpStatus

            TradeContext.sRivTeller   = '   '     #对方柜员
            TradeContext.sTransType    = '冲正'
            
            tmpBesbNo = TradeContext.sInBesbNo
            TradeContext.sInBesbNo = TradeContext.sBesbNo
            TradeContext.sBesbNo = tmpBesbNo

            #交易公共部分    
            VouhFunc.VouhTrans()
            AfaDBFunc.CommitSql( )
            
            TradeContext.sTranStatus = '1'
            if(not TradeContext.existVariable( "HostSerno" )):
                TradeContext.HostSerno = ''    
            
            #更新流水表
            VouhFunc.ModifyVouhModify()
            
            AfaLoggerFunc.tradeInfo( '============================自动冲正！' )

            
            VouhFunc.tradeExit(tmpErrorCode, tmpErrorMsg)
            raise AfaFlowControl.flowException( )
        
        #更新流水表
        VouhFunc.ModifyVouhModify()     
        
        TradeContext.tradeResponse.append( ['sVouhSerial',TradeContext.sVouhSerial] )
        TradeContext.tradeResponse.append( ['sVouhType',TradeContext.rVouhType] )
        TradeContext.tradeResponse.append( ['sVouhName',TradeContext.rVouhName] )
        TradeContext.tradeResponse.append( ['sStartNo',TradeContext.rStartNo] )
        TradeContext.tradeResponse.append( ['sEndNo',TradeContext.rEndNo] )
        TradeContext.tradeResponse.append( ['sVouhNum',TradeContext.rVouhNum] )
        TradeContext.tradeResponse.append( ['sLstTrxDay',TradeContext.sLstTrxDay] )
        TradeContext.tradeResponse.append( ['sLstTrxTime',TradeContext.sLstTrxTime] )
        TradeContext.tradeResponse.append( ['sNum',str(TradeContext.sNum)] )
        TradeContext.tradeResponse.append( ['errorCode','0000'] )
        TradeContext.tradeResponse.append( ['errorMsg','交易成功'] )

        #自动打包
        AfaFunc.autoPackData()

        #=============程序退出====================
        AfaLoggerFunc.tradeInfo( '凭证上缴['+TradeContext.TemplateCode+']退出' )
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))

