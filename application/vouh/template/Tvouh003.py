# -*- coding: gbk -*-
###################################################################
#    文    件:    Tvouh003.py
#    说    明:    凭证管理-->凭证调配
#    环    境:    中间业务新平台（AFA）--- UNIX: AIX 5.3
#    作    者:    李亚杰
#    公    司:    北京赞同科技
#    创建地址:    安徽
#    创建时间:    2008年6月4日
#    维护纪录:
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, AfaFlowControl, AfaDBFunc
from types import *
import VouhFunc,HostContext,VouhHostFunc

def main( ):
    AfaLoggerFunc.tradeInfo( '凭证调配['+TradeContext.TemplateCode+']进入' )
    
    
    #=============前台上送数据===================================
    #TradeContext.sBesbNo                                 机构号
    #TradeContext.sBesbSty                                机构类型
    #TradeContext.sCur                                    货币代码
    #TradeContext.sTellerNo                               柜员号
    #TradeContext.sVouhType                               凭证种类
    #TradeContext.sInBesbNo                               领用机构号
    #TradeContext.sInBesbSty                              领用机构类型
    #TradeContext.sInTellerNo                             领用柜员号
    #TradeContext.sStartNo                                起始号码
    #TradeContext.sEndNo                                  终止号码
    #TradeContext.sRivTeller                              对方柜员
    #TradeContext.sVouhStatus                             凭证状态
    #TradeContext.sVouhNum                                凭证数量
    #TradeContext.sLstTrxDay                              最后交易日期
    #TradeContext.sLstTrxTime                             最后交易时间
    #TradeContext.sDepository                             库箱标志

    try:
        #=============获取当前系统时间==========================
        TradeContext.sLstTrxDay = AfaUtilTools.GetSysDate( )
        TradeContext.sLstTrxTime = AfaUtilTools.GetSysTime( )
        
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
            AfaLoggerFunc.tradeInfo( '交易机构类型' )
            AfaLoggerFunc.tradeInfo( SBNO )
            
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
        
        #=============获取领用机构类型==========================
        HostContext.I1OTSB = TradeContext.sInBesbNo       #领用机构号
        HostContext.I1SBNO = TradeContext.sInBesbNo       #机构号
        HostContext.I1USID = TradeContext.sTellerNo       #柜员号
        HostContext.I1WSNO = TradeContext.sWSNO           #终端号
        if(not VouhHostFunc.CommHost('2001')):
            return VouhFunc.ExitThisFlow( TradeContext.errorCode, TradeContext.errorMsg )
        if(TradeContext.errorCode == '0000'):
            INSBNO = HostContext.O1SBCH
            AfaLoggerFunc.tradeInfo( '领用机构类型' )
            AfaLoggerFunc.tradeInfo( INSBNO )
            
        #begin凭证优化更改201109  
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
        
        #=============初始化返回报文变量========================
        TradeContext.tradeResponse = []
        TradeContext.sRivTeller = TradeContext.sInTellerTailNo
        
        #=============生成流水号========================
        TradeContext.sVouhSerial = VouhFunc.GetVouhSerial( )
        
        #=============定义变量=============================================================
        #31联社清算中心 32联社营业部 33联社财务部 40信用社/支行 50分社/分理处/储蓄所
        #1.分行管理库 2.支行管理库 3.网点管理库 4.柜员凭证箱
        if(SBNO=='33'):
            TradeContext.sExDepos     = '1' #原库箱标志
        elif(SBNO=='31' or SBNO=='40' or SBNO=='32' or SBNO=='41'):
            TradeContext.sExDepos     = '2' #原库箱标志
        elif(SBNO=='50'):
            TradeContext.sExDepos     = '3' #原库箱标志
        else:
            VouhFunc.tradeExit('A005061', '该机构柜员不能进行此操作!')
            raise AfaFlowControl.flowException( )
        
        if(INSBNO=='33'):
            TradeContext.sDepository     = '1' #库箱标志
        elif(INSBNO=='31' or INSBNO=='40' or INSBNO=='32' or INSBNO=='41'):
            TradeContext.sDepository     = '2' #库箱标志
        elif(INSBNO=='50'):
            TradeContext.sDepository     = '3' #库箱标志
        else:
            VouhFunc.tradeExit('A005061', '该机构柜员不能进行此操作!')
            raise AfaFlowControl.flowException( )
            
        if(INSBNO=='33'): 
            TradeContext.sVouhStatus  = '0' #状态       0.已入未发  2.已发未领
            TradeContext.sExStatus    = '2' #原状态
        elif(SBNO=='33'):
            TradeContext.sVouhStatus  = '2' #状态       0.已入未发  2.已发未领
            TradeContext.sExStatus    = '0' #原状态
        else:
            TradeContext.sVouhStatus  = '2' #状态       0.已入未发  2.已发未领
            TradeContext.sExStatus    = '2' #原状态
            
        
        TradeContext.sTransType    = '凭证调配'
        
        #================判断是否隔级机构调配===================================================
        if((SBNO =='33' and INSBNO=='50') or 
           (SBNO =='50' and INSBNO=='33') or
           (SBNO =='31' and INSBNO=='50') or
           (SBNO =='50' and INSBNO=='31') or
           (SBNO =='50' and INSBNO=='50') or
           (SBNO =='32' and INSBNO=='32') or
           (SBNO =='31' and INSBNO=='31') or
           (SBNO =='41' and INSBNO=='41') or
           (SBNO =='40' and INSBNO=='40')):
            VouhFunc.tradeExit('A005061', '该机构柜员不能进行此操作!')
            raise AfaFlowControl.flowException( )
            
        #================判断是否同级机构===================================================
        if((SBNO =='31' and INSBNO=='40') or 
           (SBNO =='40' and INSBNO=='31') or
           (SBNO =='31' and INSBNO=='32') or
           (SBNO =='32' and INSBNO=='31') or
           (SBNO =='40' and INSBNO=='32') or
           (SBNO =='32' and INSBNO=='40') or
           (SBNO =='41' and INSBNO=='32') or
           (SBNO =='41' and INSBNO=='31') or
           (SBNO =='32' and INSBNO=='41') or
           (SBNO =='31' and INSBNO=='41')):
            VouhFunc.tradeExit('A005061', '该机构柜员不能进行此操作!')
            raise AfaFlowControl.flowException( )
            
        #================判断领用机构的清算上级是否是调拨凭证的机构号=========================
        if((SBNO =='40' and INSBNO=='50') or
           (SBNO =='32' and INSBNO=='50') or
           (SBNO =='41' and INSBNO=='50')):
            if(TradeContext.sBesbNo <> VouhFunc.SelectSBTPAC(TradeContext.sInBesbNo)):
                VouhFunc.tradeExit('A005061', '该机构柜员不能进行此操作!')
                raise AfaFlowControl.flowException( )
        
        #================机构号的清算上级是否是领用机构号=====================================
        if((SBNO =='50' and INSBNO=='40') or
            (SBNO =='50' and INSBNO=='32') or
            (SBNO =='50' and INSBNO=='41')):
            if(TradeContext.sInBesbNo <> VouhFunc.SelectSBTPAC(TradeContext.sBesbNo)):
                VouhFunc.tradeExit('A005061', '该机构柜员不能进行此操作!')
                raise AfaFlowControl.flowException( )
                
        if((TradeContext.sBesbNo)[:6] <> (TradeContext.sInBesbNo)[:6]):
            VouhFunc.tradeExit('A005061', '该机构柜员不能进行此操作!')
            raise AfaFlowControl.flowException( )
            
        #交易公共部分    
        AfaLoggerFunc.tradeInfo( TradeContext.sExDepos )
        VouhFunc.VouhTrans()

        #更新凭证变更登记薄
        VouhFunc.VouhModify()
        
        #数据库提交
        AfaDBFunc.CommitSql( )
        
        #主机记账
        AfaLoggerFunc.tradeInfo( '------------主机记账' )
        TradeContext.sOperSty = '2'
        VouhHostFunc.VouhCommHost()
        TradeContext.sTranStatus = '0'
        AfaLoggerFunc.tradeInfo( '=======================12'+TradeContext.errorCode )
        
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
            
            tmpTeller = TradeContext.sInTellerTailNo
            TradeContext.sInTellerTailNo = TradeContext.sTellerTailNo
            TradeContext.sTellerTailNo = tmpTeller
            
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

        #=============程序退出=========================================
        AfaLoggerFunc.tradeInfo( '凭证调配['+TradeContext.TemplateCode+']退出' )
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
