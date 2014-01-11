# -*- coding: gbk -*-
##################################################################
#   财税库行.三方协议校验.柜面发起
#=================================================================
#   程序文件:   TTPS001_8451.py
#   修改时间:   2006-04-05
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools, TradeFunc,AfaDBFunc
import TipsFunc,AfaAfeFunc,TipsHostFunc,HostContext
from types import *

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo( '进入三方协议验证/撤消[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )

    try:
        #=============获取当前系统时间====================
        #TradeContext.workDate=UtilTools.GetSysDate( )
        TradeContext.workTime=UtilTools.GetSysTime( )
        
        ##====获取工作日期=======
        #if not TipsFunc.GetUnitWorkdate( ):
        #    return False
        
        #============校验公共节点的有效性==================
        # 完整性检查
        if( not TradeContext.existVariable( "VCSign" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '标识[VCSign]值不存在!' )
        if( not TradeContext.existVariable( "zoneno" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '分行号[zoneno]值不存在!' )
        if( not TradeContext.existVariable( "channelCode" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '渠道代码[channelCode]值不存在!' )
        if( not TradeContext.existVariable( "brno" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '行所号[brno]值不存在!' )
        if( not TradeContext.existVariable( "teller" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '柜员号[teller]值不存在!' )
        if( not TradeContext.existVariable( "accno" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '帐号[accno]值不存在!' )
        if( not TradeContext.existVariable( "taxPayCode" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '纳税人编码[taxPayCode]值不存在!' )
        if( not TradeContext.existVariable( "taxPayName" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '纳税人名称[taxPayName]值不存在!' )
        if( not TradeContext.existVariable( "passWDFlag" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '密码验证标志[passWDFlag]值不存在!' )
        if( not TradeContext.existVariable( "payBkCode" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '清算行行号[payBkCode]值不存在!' )
            
        TradeContext.note1 = TradeContext.payBkCode
        
        if(TradeContext.passWDFlag == '0'):
            #验证密码
            TradeContext.sBrNo = TradeContext.brno          #交易机构
            TradeContext.sTeller = TradeContext.teller      #交易柜员
            TradeContext.sTermId = TradeContext.termId      #终端号 
            HostContext.I1ACNO = TradeContext.accno         #付款帐户
            HostContext.I1CYNO = '01'
            accnoLen = len(TradeContext.accno)
            if(accnoLen == 23):
                HostContext.I1CFFG = 'A'
            elif(accnoLen == 19):
                HostContext.I1CFFG = '0'
                HostContext.I1CETY = (TradeContext.accno)[6:8]
                HostContext.I1CCSQ = (TradeContext.accno)[8:19]
            else:
                return TipsFunc.ExitThisFlow( 'A0001', '帐号错误！' )
            HostContext.I1PSWD = TradeContext.passWD    
            
            if(not TipsHostFunc.CommHost('8810')):    
                return TipsFunc.ExitThisFlow( TradeContext.errorCode, TradeContext.errorMsg )
            if(TradeContext.errorCode == '0000'):
                if(HostContext.O1CFFG == '1'):
                    return TipsFunc.ExitThisFlow( 'A0001', '密码错误!' )
        
        #=============判断应用状态====================
        if not TipsFunc.ChkAppStatus( ) :
            raise TipsFunc.flowException( )
        #=============判断机构是否开通此应用===============
        #if not TipsFunc.ChkBranchStatus( ) :
        #    raise TipsFunc.flowException( )
        #=============获取平台流水号==================== 
        if TipsFunc.GetSerialno( ) == -1 :
            raise TipsFunc.flowException( )
        
        #签约
        if TradeContext.VCSign=='0':
            #=============判断状态====================
            sql="SELECT STATUS FROM TIPS_CUSTINFO WHERE "
            sql=sql+" TAXORGCODE ='"+TradeContext.taxOrgCode     +"'"
            sql=sql+" AND TAXPAYCODE='"+TradeContext.taxPayCode+"'"
            sql=sql+" AND PROTOCOLNO='"+TradeContext.protocolNo+"'"
            sql=sql+" AND PAYACCT='"+TradeContext.accno+"'"
            records = AfaDBFunc.SelectSql(sql)
            AfaLoggerFunc.tradeFatal(sql)
            if( records == None or  records <0):
                #AfaLoggerFunc.tradeFatal(sql)
                return TipsFunc.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
            elif( len( records )==0 ):
                AfaLoggerFunc.tradeInfo( "该客户尚未签约，可正常处理" )
            else:
                AfaLoggerFunc.tradeFatal(sql)
                AfaLoggerFunc.tradeInfo(records[0][0])
                UtilTools.ListFilterNone( records )
                AfaLoggerFunc.tradeInfo( "==================1" )
                #0-注销 1-正常（双方都已验证） 2-临时状态（银行方柜面已验证）3-临时状态（银行方柜面已撤销）
                if (records[0][0]=="1" or records[0][0]=="2" ): #已有该客户记录，状态为"已启用"，不允许签约
                    return TipsFunc.ExitThisFlow( 'A0002', '客户编号或帐号已经签约，不能重复签约')
            AfaLoggerFunc.tradeInfo( "==================2" )
            TradeContext.status = '2'
            #TradeContext.revTranF       ='0' #正交易
            #TradeContext.tradeType      ='S' #签约类交易
            #TradeContext.amount         ='0' #
            #TradeContext.__agentAccno__ =''  #借方帐号置空
            ##记录签约流水
            #if not TipsFunc.InsertDtl( ) :
            #    return False
            #=============与第三方通讯====================
            #AfaAfeFunc.CommAfe()
            TradeContext.__status__='0'
            TradeContext.errorCode='0000'
            TradeContext.errorMsg='交易成功'
            
            ##=============更新流水表====================
            #if( not TipsFunc.UpdateDtl( 'TRADE' ) ):
            #    return False
            AfaLoggerFunc.tradeInfo( "==================3" )
            if TradeContext.errorCode!='0000':
                return TipsFunc.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
            if ( len( records )!=0 ):
                sql="update TIPS_CUSTINFO set "
                sql=sql+" PAYACCT         ='"+TradeContext.accno      +"'"
                sql=sql+",STATUS     ='"+'2'                     +"'"
                sql=sql+",TAXPAYNAME      ='"+TradeContext.taxPayName  +"'"
                sql=sql+",HANDORGNAME      ='"+TradeContext.handOrgName  +"'"
                sql=sql+",STARTDATE     ='"+TradeContext.workDate   +"'"
                sql=sql+",ZONENO     ='"+TradeContext.zoneno     +"'"
                sql=sql+",BRNO       ='"+TradeContext.brno       +"'"
                sql=sql+",TELLERNO   ='"+TradeContext.teller   +"'"
                if( TradeContext.existVariable( "NOTE1" ) ):
                    sql=sql+",NOTE1         ='"+TradeContext.note1   +"'"
                if( TradeContext.existVariable( "NOTE2" ) ):
                    sql=sql+",NOTE2         ='"+TradeContext.note2   +"'"
                if( TradeContext.existVariable( "NOTE3" ) ):
                    sql=sql+",NOTE3         ='"+TradeContext.note3   +"'"
                if( TradeContext.existVariable( "NOTE4" ) ):
                    sql=sql+",NOTE4         ='"+TradeContext.note4   +"'"
                if( TradeContext.existVariable( "NOTE5" ) ):
                    sql=sql+",NOTE5         ='"+TradeContext.note5   +"'"
                sql=sql+" WHERE TAXORGCODE ='"+TradeContext.taxOrgCode     +"'"
                sql=sql+" AND TAXPAYCODE ='"+TradeContext.taxPayCode     +"'"
                AfaLoggerFunc.tradeInfo(sql)
                if( AfaDBFunc.UpdateSql(sql) == -1 ):
                    AfaLoggerFunc.tradeFatal(sql)
                    return TipsFunc.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
            else:
                sql="insert into TIPS_CUSTINFO(TAXPAYCODE,TAXORGCODE,PROTOCOLNO,PAYACCT,IDTYPE,IDCODE,TAXPAYNAME,STATUS,"
                sql=sql+"HANDORGNAME,STARTDATE,ENDDATE,ZONENO,BRNO,TELLERNO,WORKDATE,PAYOPBKCODE,"
                sql=sql+"NOTE1,NOTE2,NOTE3,NOTE4,NOTE5)"
                sql=sql+" values"
                sql=sql+"('"+TradeContext.taxPayCode    +"'"
                sql=sql+",'"+TradeContext.taxOrgCode    +"'"
                sql=sql+",'"+TradeContext.protocolNo+"'"
                sql=sql+",'"+TradeContext.accno     +"'"
                sql=sql+",'',''"
                sql=sql+",'"+TradeContext.taxPayName +"'"
                sql=sql+",'2'" #临时状态，待第三方验证后改为1
                if( TradeContext.existVariable( "handOrgName" ) ):
                    sql=sql+",'"+TradeContext.handOrgName    +"'"
                else:
                    sql=sql+",''"
                #if( TradeContext.existVariable( "custAdd" ) ):
                #    sql=sql+",'"+TradeContext.custAdd    +"'"
                #else:
                #    sql=sql+",''"
                #if( TradeContext.existVariable( "zipCode" ) ):
                #    sql=sql+",'"+TradeContext.zipCode    +"'"
                #else:
                #    sql=sql+",''"
                #if( TradeContext.existVariable( "email" ) ):
                #    sql=sql+",'"+TradeContext.email    +"'"
                #else:
                #    sql=sql+",''"
                sql=sql+",'"+TradeContext.workDate    +"'"
                sql=sql+",''"
                sql=sql+",'"+TradeContext.zoneno      +"'"
                sql=sql+",'"+TradeContext.brno    +"'"
                sql=sql+",'"+TradeContext.teller    +"'"
                sql=sql+",'"+TradeContext.workDate    +"'"
                sql=sql+",'"+TradeContext.payOpBkCode    +"'"
                if( TradeContext.existVariable( "note1" ) ):
                    sql=sql+",'"+TradeContext.note1    +"'"
                else:
                    sql=sql+",''"
                if( TradeContext.existVariable( "note2" ) ):
                    sql=sql+",'"+TradeContext.note2    +"'"
                else:
                    sql=sql+",''"          
                if( TradeContext.existVariable( "note3" ) ):
                    sql=sql+",'"+TradeContext.note3    +"'"
                else:
                    sql=sql+",''"
                if( TradeContext.existVariable( "note4" ) ):
                    sql=sql+",'"+TradeContext.note4    +"'"
                else:
                    sql=sql+",''"
                if( TradeContext.existVariable( "note5" ) ):
                    sql=sql+",'"+TradeContext.note5    +"'"
                else:
                    sql=sql+",''"
                sql=sql+")"
                AfaLoggerFunc.tradeInfo(sql)
                records=AfaDBFunc.InsertSqlCmt(sql)
                if( records == 0 ):
                    return TipsFunc.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                
                if( records == -1 ):
                    return TipsFunc.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                AfaLoggerFunc.tradeInfo('***************')
        elif TradeContext.VCSign=='1':
            #=============判断状态====================
            sql="SELECT STATUS"
            sql=sql+" FROM TIPS_CUSTINFO WHERE TAXPAYCODE ='"+TradeContext.taxPayCode +"'"
            sql=sql+" and PAYACCT     ='"+TradeContext.accno  +"'"
            sql=sql+" and PROTOCOLNO  ='"+TradeContext.protocolNo  +"'"
            sql=sql+" and TAXORGCODE  ='"+TradeContext.taxOrgCode  +"'"
            AfaLoggerFunc.tradeInfo(sql)
            records = AfaDBFunc.SelectSql(sql)
            if( records == None or  records <0):
                AfaLoggerFunc.tradeFatal(sql)
                return TipsFunc.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
            elif( len( records )==0 ):
                return TipsFunc.ExitThisFlow( 'A0027', '该客户三方协议尚未验证，无法撤消' )
            elif( len( records )>1 ):
                return TipsFunc.ExitThisFlow( 'A0027', '存在多条验证记录' )
            else:
                AfaLoggerFunc.tradeFatal(sql)
                AfaLoggerFunc.tradeInfo(records[0][0])
                UtilTools.ListFilterNone( records )
                if (records[0][0]=='0' or records[0][0]=='3'):
                    return TipsFunc.ExitThisFlow( 'A0027', '三方协议状态为已撤消，不能重复撤消' )
            TradeContext.status = '3'
            #TradeContext.revTranF       ='0' #正交易
            #TradeContext.tradeType      ='U' #解约类交易
            #TradeContext.amount         ='0' #
            #TradeContext.__agentAccno__ =''  #借方帐号置空
            ##记录签约流水
            #if not TipsFunc.InsertDtl( ) :
            #    return False
            #=============与第三方通讯通讯====================
            #AfaAfeFunc.CommAfe()
            #TradeContext.__status__='0'
            #TradeContext.errorCode='0000'
            #TradeContext.errorMsg='交易成功'
            ##=============更新流水表====================
            #if( not TipsFunc.UpdateDtl( 'TRADE' ) ):
            #    return False
            #if TradeContext.errorCode!='0000':
            #    return TipsFunc.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
            #if TradeContext.errorCode=='0000':
            sql="update TIPS_CUSTINFO set "
            sql=sql+" STATUS     ='"+'3'                     +"'"
            sql=sql+",ENDDATE      ='"+TradeContext.workDate   +"'"
            sql=sql+",ZONENO     ='"+TradeContext.zoneno     +"'"
            sql=sql+",BRNO       ='"+TradeContext.brno       +"'"
            sql=sql+",TELLERNO   ='"+TradeContext.teller   +"'"
            sql=sql+" WHERE TAXPAYCODE ='"  +TradeContext.taxPayCode   +"'"
            sql=sql+" AND PAYACCT ='"       +TradeContext.accno        +"'"
            sql=sql+" AND PROTOCOLNO  ='"   +TradeContext.protocolNo   +"'"
            sql=sql+" AND TAXORGCODE  ='"   +TradeContext.taxOrgCode   +"'"
            AfaLoggerFunc.tradeInfo(sql)
            if( AfaDBFunc.UpdateSql(sql) == -1 ):
                AfaLoggerFunc.tradeFatal(sql)
                return TipsFunc.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
        #=============自动打包==================== 
        TradeContext.errorCode='0000'
        TradeContext.errorMsg='交易成功'
        #=============程序退出====================
        AfaLoggerFunc.tradeInfo( '退出三方协议验证/撤消['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        return True
    except TipsFunc.flowException, e:
        return False
    except Exception, e:
        return TipsFunc.ExitThisFlow('A9999','系统异常'+str(e) )
def SubModuleMainSnd():
    return True   
