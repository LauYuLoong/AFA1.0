# -*- coding: gbk -*-
##################################################################
#   财税库行.公共数据更新通知(TIPS发起)
#=================================================================
#   程序文件:   TTPS001_845007.py
#   修改时间:   2007-6-11 
#   生效日期为当日的数据，及时修改运行参数表
#   生效日期不为当日的数据，由日切程序检查参数操作表中是否有需要操作的数据，进行处理？
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools, AfaFlowControl,AfaDBFunc
from types import *

def SubModuleMainFst( ):

    AfaLoggerFunc.tradeInfo( '进入公共数据更新交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
        #=============初始化返回报文变量====================
        TradeContext.tradeResponse=[]
        #=============获取当前系统时间====================
        TradeContext.workDate=UtilTools.GetSysDate( )
        TradeContext.workTime=UtilTools.GetSysTime( )

        #============校验公共节点的有效性==================
        # 完整性检查
        #if( not TradeContext.existVariable( "sysId" ) ):
        #    TradeFunc.exitOnError( 'A0001', '系统标识[sysId]值不存在!' )
        #if( not TradeContext.existVariable( "agentFlag" ) ):
        #    TradeFunc.exitOnError( 'A0001', '业务方式[agentFlag]值不存在!' )
        #if( not TradeContext.existVariable( "zoneno" ) ):
        #    TradeFunc.exitOnError( 'A0001', '分行号[zoneno]值不存在!' )
        #if( not TradeContext.existVariable( "channelCode" ) ):
        #    TradeFunc.exitOnError( 'A0001', '渠道代码[channelCode]值不存在!' )
        #
        ##===============判断应用系统状态======================
        #if not AfaFlowControl.ChkSysStatus( ) :
        #    raise AfaFlowControl.flowException( )
        ##===============判断商户状态======================
        #if not AfaFlowControl.ChkUnitStatus( ) :
        #    raise AfaFlowControl.flowException( )
        ##=============判断应用状态====================
        #if not AfaFlowControl.ChkAppStatus( ) :
        #    raise AfaFlowControl.flowException( )
        #
        ##=============判断渠道状态====================
        #if not AfaFlowControl.ChkChannelStatus( ) :
        #    raise AfaFlowControl.flowException( )
        ##=============获取平台流水号==================== 
        #if AfaFlowControl.GetSerialno( ) == -1 :
        #    raise AfaFlowControl.flowException( )
        #TradeContext.serialno=TradeContext.agentSerialno
        if int(TradeContext.UpdateNum101) > 0:
            TradeContext.recNum=int(TradeContext.UpdateNum101)
        elif int(TradeContext.UpdateNum102) > 0:
            TradeContext.recNum=int(TradeContext.UpdateNum102)
        elif int(TradeContext.UpdateNum103) > 0:
            TradeContext.recNum=int(TradeContext.UpdateNum103)
        elif int(TradeContext.UpdateNum104) > 0:
            TradeContext.recNum=int(TradeContext.UpdateNum104)
        elif int(TradeContext.UpdateNum105) > 0:
            TradeContext.recNum=int(TradeContext.UpdateNum105)
        elif int(TradeContext.UpdateNum106) > 0:
            TradeContext.recNum=int(TradeContext.UpdateNum106)
        elif int(TradeContext.UpdateNum107) > 0:
            TradeContext.recNum=int(TradeContext.UpdateNum107)
        elif int(TradeContext.UpdateNum108) > 0:
            TradeContext.recNum=int(TradeContext.UpdateNum108)
        elif int(TradeContext.UpdateNum109) > 0:
            TradeContext.recNum=int(TradeContext.UpdateNum109)
            
        AfaLoggerFunc.tradeInfo(str(TradeContext.recNum))
        
        #TradeContext.tradeResponse.append(['dealFlag','0'])
        if not TIPS_TAXCODEDTL():
            TradeContext.tradeResponse.append(['dealFlag','0'])
            return False
        if not TIPS_BANKCODEDTL():
            TradeContext.tradeResponse.append(['dealFlag','0'])
            return False
        if not TIPS_NODECODEDTL():
            TradeContext.tradeResponse.append(['dealFlag','0'])
            return False
        if not TIPS_TRECODEDTL():
            TradeContext.tradeResponse.append(['dealFlag','0'])
            return False
        #if not TIPS_CORRECTREASONCODEDTL():
        #    return False
        #if not TIPS_RETURNREASONCODEDTL():
        #    return False
        if not TIPS_TAXTYPECODEDTL():
            TradeContext.tradeResponse.append(['dealFlag','0'])
            return False
        if not TIPS_BUDGETSUBJECTCODEDTL():
            TradeContext.tradeResponse.append(['dealFlag','0'])
            return False
        #=============自动打包==================== 
        TradeContext.tradeResponse.append(['dealFlag','1'])
        TradeContext.tradeResponse.append(['errorCode','0000'])
        TradeContext.tradeResponse.append(['errorMsg','交易成功'])
        #=============程序退出====================
        AfaLoggerFunc.tradeInfo( '退出公共数据更新交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']\n' )
        return True
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))  
def SubModuleMainSnd():
    return True   

def TIPS_TAXCODEDTL():
    #征收机关代码
    #if( TradeContext.existVariable( "DataType101" ) ):
    if int(TradeContext.UpdateNum101) > 0:
        for i in range( 0, TradeContext.recNum ):
            sql="insert into TIPS_TAXCODEDTL(TAXORGCODE,TAXORGNAME,TAXORGTYPE,ORGLEVEL,UPTRECODE,OFNODECODE,OFPROVORG,OFCITYORG"
            sql=sql+",OFCOUNTYORG,ADDRESS,POSTALCODE,PEOPLENAME,PEOPLEPHONE,PEOPLEMOBILE,EMAIL"
            sql=sql+",OPERSIGN,EFFECTDATE,UPDATEAREA,UPDATEBATCH)"
            sql=sql+" values"
            if TradeContext.recNum==1:
                sql=sql+"('"+TradeContext.TaxOrgCode1      +"'"
                sql=sql+",'"+TradeContext.TaxOrgName1      +"'"
                sql=sql+",'"+TradeContext.TaxOrgType1      +"'"
                sql=sql+",'"+TradeContext.OrgLevel1        +"'"
                sql=sql+",'"+TradeContext.UpTreCode1       +"'"
                sql=sql+",'"+TradeContext.OfNodeCode1      +"'"
                sql=sql+",'"+TradeContext.OfProvOrg1       +"'"
                sql=sql+",'"+TradeContext.OfCityOrg1       +"'"
                sql=sql+",'"+TradeContext.OfCountyOrg1     +"'"
                sql=sql+",'"+TradeContext.Address1         +"'"
                sql=sql+",'"+TradeContext.PostalCode1      +"'"
                sql=sql+",'"+TradeContext.PeopleName1      +"'"
                sql=sql+",'"+TradeContext.PeoplePhone1     +"'"
                sql=sql+",'"+TradeContext.PeopleMobile1    +"'"
                sql=sql+",'"+TradeContext.Email1           +"'"
                sql=sql+",'"+TradeContext.OperSign1        +"'"
                sql=sql+",'"+TradeContext.EffectDate1      +"'"
                sql=sql+",'"+TradeContext.UpdateArea1[:10]      +"'"
                sql=sql+",'"+TradeContext.UpdateBatch        +"'"
                #sql=sql+",'"+TradeContext.NOTE1[i]           +"'"
                #sql=sql+",'"+TradeContext.NOTE2[i]           +"'"
                EffectDate1=TradeContext.EffectDate1
                OperSign1=TradeContext.OperSign1
            else:
                sql=sql+"('"+TradeContext.TaxOrgCode1[i]      +"'"
                sql=sql+",'"+TradeContext.TaxOrgName1[i]      +"'"
                sql=sql+",'"+TradeContext.TaxOrgType1[i]      +"'"
                sql=sql+",'"+TradeContext.OrgLevel1[i]        +"'"
                sql=sql+",'"+TradeContext.UpTreCode1[i]       +"'"
                sql=sql+",'"+TradeContext.OfNodeCode1[i]      +"'"
                sql=sql+",'"+TradeContext.OfProvOrg1[i]       +"'"
                sql=sql+",'"+TradeContext.OfCityOrg1[i]       +"'"
                sql=sql+",'"+TradeContext.OfCountyOrg1[i]     +"'"
                sql=sql+",'"+TradeContext.Address1[i]         +"'"
                sql=sql+",'"+TradeContext.PostalCode1[i]      +"'"
                sql=sql+",'"+TradeContext.PeopleName1[i]      +"'"
                sql=sql+",'"+TradeContext.PeoplePhone1[i]     +"'"
                sql=sql+",'"+TradeContext.PeopleMobile1[i]    +"'"
                sql=sql+",'"+TradeContext.Email1[i]           +"'"
                sql=sql+",'"+TradeContext.OperSign1[i]        +"'"
                sql=sql+",'"+TradeContext.EffectDate1[i]      +"'"
                sql=sql+",'"+TradeContext.UpdateArea1[i][:10]      +"'"
                sql=sql+",'"+TradeContext.UpdateBatch        +"'"
                #sql=sql+",'"+TradeContext.NOTE1[i]           +"'"
                #sql=sql+",'"+TradeContext.NOTE2[i]           +"'"
                EffectDate1=TradeContext.EffectDate1[i]
                OperSign1=TradeContext.OperSign1[i]
            sql=sql+")"
            AfaLoggerFunc.tradeInfo(sql)
            if( AfaDBFunc.InsertSqlCmt(sql) == -1 ):
                AfaLoggerFunc.tradeFatal(sql)
                AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                f = open("TIPS_TAXCODEDTL","a")
                f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                f.close()
                #return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
            #如果生效日期为当日，即时生效
            if EffectDate1<=TradeContext.workDate:
                sql="select TAXORGCODE from  TIPS_TAXCODE "
                if TradeContext.recNum==1:
                    sql=sql+" WHERE TAXORGCODE   ='"+TradeContext.TaxOrgCode1      +"'"
                else:
                    sql=sql+" WHERE TAXORGCODE   ='"+TradeContext.TaxOrgCode1[i]      +"'"
                AfaLoggerFunc.tradeInfo(sql)
                records = AfaDBFunc.SelectSql(sql)
                if( records == None ):
                    AfaLoggerFunc.tradeFatal(sql)
                    return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                if len( records )==0: #新增
                    sql="insert into TIPS_TAXCODE(TAXORGCODE,TAXORGNAME,TAXORGTYPE,ORGLEVEL,UPTRECODE,OFNODECODE,OFPROVORG,OFCITYORG"
                    sql=sql+",OFCOUNTYORG,ADDRESS,POSTALCODE,PEOPLENAME,PEOPLEPHONE,PEOPLEMOBILE,EMAIL"
                    sql=sql+",STATUS,EFFECTDATE,UPDATEAREA,UPDATEBATCH)"
                    sql=sql+" values"
                    if TradeContext.recNum==1:
                        sql=sql+"('"+TradeContext.TaxOrgCode1      +"'"
                        sql=sql+",'"+TradeContext.TaxOrgName1      +"'"
                        sql=sql+",'"+TradeContext.TaxOrgType1      +"'"
                        sql=sql+",'"+TradeContext.OrgLevel1        +"'"
                        sql=sql+",'"+TradeContext.UpTreCode1       +"'"
                        sql=sql+",'"+TradeContext.OfNodeCode1      +"'"
                        sql=sql+",'"+TradeContext.OfProvOrg1       +"'"
                        sql=sql+",'"+TradeContext.OfCityOrg1       +"'"
                        sql=sql+",'"+TradeContext.OfCountyOrg1     +"'"
                        sql=sql+",'"+TradeContext.Address1         +"'"
                        sql=sql+",'"+TradeContext.PostalCode1      +"'"
                        sql=sql+",'"+TradeContext.PeopleName1      +"'"
                        sql=sql+",'"+TradeContext.PeoplePhone1     +"'"
                        sql=sql+",'"+TradeContext.PeopleMobile1    +"'"
                        sql=sql+",'"+TradeContext.Email1           +"'"
                        sql=sql+",'"+'0'                          +"'"
                        sql=sql+",'"+TradeContext.EffectDate1      +"'"
                        sql=sql+",'"+TradeContext.UpdateArea1[:10]      +"'"
                        sql=sql+",'"+TradeContext.UpdateBatch     +"'"
                        #sql=sql+",'"+TradeContext.NOTE1           +"'"
                        #sql=sql+",'"+TradeContext.NOTE2           +"'"
                        sql=sql+")"
                    else:
                        sql=sql+"('"+TradeContext.TaxOrgCode1[i]      +"'"
                        sql=sql+",'"+TradeContext.TaxOrgName1[i]      +"'"
                        sql=sql+",'"+TradeContext.TaxOrgType1[i]      +"'"
                        sql=sql+",'"+TradeContext.OrgLevel1[i]        +"'"
                        sql=sql+",'"+TradeContext.UpTreCode1[i]       +"'"
                        sql=sql+",'"+TradeContext.OfNodeCode1[i]      +"'"
                        sql=sql+",'"+TradeContext.OfProvOrg1[i]       +"'"
                        sql=sql+",'"+TradeContext.OfCityOrg1[i]       +"'"
                        sql=sql+",'"+TradeContext.OfCountyOrg1[i]     +"'"
                        sql=sql+",'"+TradeContext.Address1[i]         +"'"
                        sql=sql+",'"+TradeContext.PostalCode1[i]      +"'"
                        sql=sql+",'"+TradeContext.PeopleName1[i]      +"'"
                        sql=sql+",'"+TradeContext.PeoplePhone1[i]     +"'"
                        sql=sql+",'"+TradeContext.PeopleMobile1[i]    +"'"
                        sql=sql+",'"+TradeContext.Email1[i]           +"'"
                        sql=sql+",'"+'0'                             +"'"
                        sql=sql+",'"+TradeContext.EffectDate1[i]      +"'"
                        sql=sql+",'"+TradeContext.UpdateArea1[i][:10]      +"'"
                        sql=sql+",'"+TradeContext.UpdateBatch     +"'"
                        #sql=sql+",'"+TradeContext.NOTE1[i]           +"'"
                        #sql=sql+",'"+TradeContext.NOTE2[i]           +"'"
                        sql=sql+")"
                    AfaLoggerFunc.tradeInfo(sql)
                    if( AfaDBFunc.InsertSqlCmt(sql) == -1 ):
                        AfaLoggerFunc.tradeFatal(sql)
                        AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                        f = open("TIPS_TAXCODE","a")
                        f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                        f.close()
                        #return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                elif OperSign1=='2' or (OperSign1=='1' and len( records )!=0):#更新
                    sql="update TIPS_TAXCODE set "
                    if TradeContext.recNum==1:
                        sql=sql+" TAXORGCODE  ='"+TradeContext.TaxOrgCode1      +"'"
                        sql=sql+",TAXORGNAME  ='"+TradeContext.TaxOrgName1      +"'"
                        sql=sql+",TAXORGTYPE  ='"+TradeContext.TaxOrgType1      +"'"
                        sql=sql+",ORGLEVEL    ='"+TradeContext.OrgLevel1        +"'"
                        sql=sql+",UPTRECODE   ='"+TradeContext.UpTreCode1       +"'"
                        sql=sql+",OFNODECODE  ='"+TradeContext.OfNodeCode1      +"'"
                        sql=sql+",OFPROVORG   ='"+TradeContext.OfProvOrg1       +"'"
                        sql=sql+",OFCITYORG   ='"+TradeContext.OfCityOrg1       +"'"
                        sql=sql+",OFCOUNTYORG ='"+TradeContext.OfCountyOrg1     +"'"
                        sql=sql+",ADDRESS     ='"+TradeContext.Address1         +"'"
                        sql=sql+",POSTALCODE  ='"+TradeContext.PostalCode1      +"'"
                        sql=sql+",PEOPLENAME  ='"+TradeContext.PeopleName1      +"'"
                        sql=sql+",PEOPLEPHONE ='"+TradeContext.PeoplePhone1     +"'"
                        sql=sql+",PEOPLEMOBILE='"+TradeContext.PeopleMobile1    +"'"
                        sql=sql+",EMAIL       ='"+TradeContext.Email1           +"'"
                        sql=sql+",EFFECTDATE  ='"+TradeContext.EffectDate1      +"'"
                        sql=sql+",UPDATEAREA  ='"+TradeContext.UpdateArea1[:10]      +"'"
                        sql=sql+",UPDATEBATCH ='"+TradeContext.UpdateBatch     +"'"
                        #sql=sql+",NOTE1       ='"+TradeContext.NOTE1           +"'"
                        #sql=sql+",NOTE2       ='"+TradeContext.NOTE2           +"'"
                        sql=sql+" WHERE TAXORGCODE   ='"+TradeContext.TaxOrgCode1      +"'"
                    else:
                        sql=sql+" TAXORGCODE  ='"+TradeContext.TaxOrgCode1[i]      +"'"
                        sql=sql+",TAXORGNAME  ='"+TradeContext.TaxOrgName1[i]      +"'"
                        sql=sql+",TAXORGTYPE  ='"+TradeContext.TaxOrgType1[i]      +"'"
                        sql=sql+",ORGLEVEL    ='"+TradeContext.OrgLevel1[i]        +"'"
                        sql=sql+",UPTRECODE   ='"+TradeContext.UpTreCode1[i]       +"'"
                        sql=sql+",OFNODECODE  ='"+TradeContext.OfNodeCode1[i]      +"'"
                        sql=sql+",OFPROVORG   ='"+TradeContext.OfProvOrg1[i]       +"'"
                        sql=sql+",OFCITYORG   ='"+TradeContext.OfCityOrg1[i]       +"'"
                        sql=sql+",OFCOUNTYORG ='"+TradeContext.OfCountyOrg1[i]     +"'"
                        sql=sql+",ADDRESS     ='"+TradeContext.Address1[i]         +"'"
                        sql=sql+",POSTALCODE  ='"+TradeContext.PostalCode1[i]      +"'"
                        sql=sql+",PEOPLENAME  ='"+TradeContext.PeopleName1[i]      +"'"
                        sql=sql+",PEOPLEPHONE ='"+TradeContext.PeoplePhone1[i]     +"'"
                        sql=sql+",PEOPLEMOBILE='"+TradeContext.PeopleMobile1[i]    +"'"
                        sql=sql+",EMAIL       ='"+TradeContext.Email1[i]           +"'"
                        sql=sql+",EFFECTDATE  ='"+TradeContext.EffectDate1[i]      +"'"
                        sql=sql+",UPDATEAREA  ='"+TradeContext.UpdateArea1[i][:10]      +"'"
                        sql=sql+",UPDATEBATCH ='"+TradeContext.UpdateBatch     +"'"
                        #sql=sql+",NOTE1       ='"+TradeContext.NOTE1[i]           +"'"
                        #sql=sql+",NOTE2       ='"+TradeContext.NOTE2[i]           +"'"
                        sql=sql+" WHERE TAXORGCODE   ='"+TradeContext.TaxOrgCode1[i]      +"'"
                    AfaLoggerFunc.tradeInfo(sql)
                    if( AfaDBFunc.UpdateSqlCmt(sql) == -1 ):
                        AfaLoggerFunc.tradeFatal(sql)
                        AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                        f = open("TIPS_TAXCODE","a")
                        f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                        f.close()

#                        return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                elif OperSign1=='3' and len( records )!=0:#注销
                    sql="update TIPS_TAXCODE set "
                    sql=sql+" STATUS      ='"+'1'          +"'"
                    if TradeContext.recNum==1:
                        sql=sql+" WHERE TAXORGCODE   ='"+TradeContext.TaxOrgCode1      +"'"
                    else:
                        sql=sql+" WHERE TAXORGCODE   ='"+TradeContext.TaxOrgCode1[i]      +"'"
                    AfaLoggerFunc.tradeInfo(sql)
                    if( AfaDBFunc.UpdateSqlCmt(sql) == -1 ):
                        AfaLoggerFunc.tradeFatal(sql)
                        AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                        f = open("TIPS_TAXCODE","a")
                        f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                        f.close()

#                        return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
    return True
def TIPS_BANKCODEDTL():
    #银行代码
    #if( TradeContext.existVariable( "DataType102" ) ):
    if int(TradeContext.UpdateNum102) > 0:
        for i in range( 0, TradeContext.recNum ):
            sql="insert into TIPS_BANKCODEDTL(RECKBANKNO,GENBANKNAME,RECKONTYPE,OFNODECODE,"
            sql=sql+"ADDRESS,POSTALCODE,PEOPLENAME,PEOPLEPHONE,PEOPLEMOBILE,EMAIL,OPERSIGN,"
            sql=sql+"EFFECTDATE,UPDATEAREA,UPDATEBATCH)"
            sql=sql+" values"
            if TradeContext.recNum==1:
                sql=sql+"('"+TradeContext.ReckBankNo2      +"'"
                sql=sql+",'"+TradeContext.GenBankName2     +"'"
                sql=sql+",'"+TradeContext.ReckonType2      +"'"
                sql=sql+",'"+TradeContext.OfNodeCode2      +"'"
                sql=sql+",'"+TradeContext.Address2         +"'"
                sql=sql+",'"+TradeContext.PostalCode2      +"'"
                sql=sql+",'"+TradeContext.PeopleName2      +"'"
                sql=sql+",'"+TradeContext.PeoplePhone2     +"'"
                sql=sql+",'"+TradeContext.PeopleMobile2    +"'"
                sql=sql+",'"+TradeContext.Email2           +"'"
                sql=sql+",'"+TradeContext.OperSign2        +"'"
                sql=sql+",'"+TradeContext.EffectDate2      +"'"
                sql=sql+",'"+TradeContext.UpdateArea2[:10]      +"'"
                sql=sql+",'"+TradeContext.UpdateBatch     +"'"
                #sql=sql+",'"+TradeContext.NOTE1[i]           +"'"
                #sql=sql+",'"+TradeContext.NOTE2[i]           +"'"
                EffectDate2=TradeContext.EffectDate2
                OperSign2=TradeContext.OperSign2
            else:
                sql=sql+"('"+TradeContext.ReckBankNo2[i]      +"'"
                sql=sql+",'"+TradeContext.GenBankName2[i]     +"'"
                sql=sql+",'"+TradeContext.ReckonType2[i]      +"'"
                sql=sql+",'"+TradeContext.OfNodeCode2[i]      +"'"
                sql=sql+",'"+TradeContext.Address2[i]         +"'"
                sql=sql+",'"+TradeContext.PostalCode2[i]      +"'"
                sql=sql+",'"+TradeContext.PeopleName2[i]      +"'"
                sql=sql+",'"+TradeContext.PeoplePhone2[i]     +"'"
                sql=sql+",'"+TradeContext.PeopleMobile2[i]    +"'"
                sql=sql+",'"+TradeContext.Email2[i]           +"'"
                sql=sql+",'"+TradeContext.OperSign2[i]        +"'"
                sql=sql+",'"+TradeContext.EffectDate2[i]      +"'"
                sql=sql+",'"+TradeContext.UpdateArea2[i][:10]      +"'"
                sql=sql+",'"+TradeContext.UpdateBatch     +"'"
                EffectDate2=TradeContext.EffectDate2[i]
                OperSign2=TradeContext.OperSign2[i]
                #sql=sql+",'"+TradeContext.NOTE1[i]           +"'"
                #sql=sql+",'"+TradeContext.NOTE2[i]           +"'"
            sql=sql+")"
            AfaLoggerFunc.tradeInfo(sql)
            if( AfaDBFunc.InsertSqlCmt(sql) == -1 ):
                AfaLoggerFunc.tradeFatal(sql)
                AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                f = open("TIPS_BANKCODEDTL","a")
                f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                f.close()
                #return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
            #如果生效日期为当日，即时生效
            if EffectDate2<=TradeContext.workDate:
                sql="select RECKBANKNO from  TIPS_BANKCODE "
                if TradeContext.recNum==1:
                    sql=sql+" WHERE RECKBANKNO   ='"+TradeContext.ReckBankNo2      +"'"
                else:
                    sql=sql+" WHERE RECKBANKNO   ='"+TradeContext.ReckBankNo2[i]      +"'"
                AfaLoggerFunc.tradeInfo(sql)
                records = AfaDBFunc.SelectSql(sql)
                if( records == None ):
                    AfaLoggerFunc.tradeFatal(sql)
                    return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                AfaLoggerFunc.tradeInfo(str(len( records )) +'|'+OperSign2)
                
                if len( records )==0: #新增
                    sql="insert into TIPS_BANKCODE(RECKBANKNO,GENBANKNAME,RECKONTYPE,OFNODECODE,ADDRESS,"
                    sql=sql+"POSTALCODE,PEOPLENAME,PEOPLEPHONE,PEOPLEMOBILE,EMAIL,STATUS,EFFECTDATE,"
                    sql=sql+"UPDATEAREA,UPDATEBATCH)"
                    sql=sql+" values"
                    if TradeContext.recNum==1:
                        sql=sql+"('"+TradeContext.ReckBankNo2      +"'"
                        sql=sql+",'"+TradeContext.GenBankName2     +"'"
                        sql=sql+",'"+TradeContext.ReckonType2      +"'"
                        sql=sql+",'"+TradeContext.OfNodeCode2      +"'"
                        sql=sql+",'"+TradeContext.Address2         +"'"
                        sql=sql+",'"+TradeContext.PostalCode2      +"'"
                        sql=sql+",'"+TradeContext.PeopleName2      +"'"
                        sql=sql+",'"+TradeContext.PeoplePhone2     +"'"
                        sql=sql+",'"+TradeContext.PeopleMobile2    +"'"
                        sql=sql+",'"+TradeContext.Email2           +"'"
                        sql=sql+",'"+'0'                          +"'"
                        sql=sql+",'"+TradeContext.EffectDate2      +"'"
                        sql=sql+",'"+TradeContext.UpdateArea2[:10]      +"'"
                        sql=sql+",'"+TradeContext.UpdateBatch     +"'"
                        #sql=sql+",'"+TradeContext.NOTE1           +"'"
                        #sql=sql+",'"+TradeContext.NOTE2           +"'"
                        sql=sql+")"
                    else:
                        sql=sql+"('"+TradeContext.ReckBankNo2[i]      +"'"
                        sql=sql+",'"+TradeContext.GenBankName2[i]     +"'"
                        sql=sql+",'"+TradeContext.ReckonType2[i]      +"'"
                        sql=sql+",'"+TradeContext.OfNodeCode2[i]      +"'"
                        sql=sql+",'"+TradeContext.Address2[i]         +"'"
                        sql=sql+",'"+TradeContext.PostalCode2[i]      +"'"
                        sql=sql+",'"+TradeContext.PeopleName2[i]      +"'"
                        sql=sql+",'"+TradeContext.PeoplePhone2[i]     +"'"
                        sql=sql+",'"+TradeContext.PeopleMobile2[i]    +"'"
                        sql=sql+",'"+TradeContext.Email2[i]           +"'"
                        sql=sql+",'"+'0'                             +"'"
                        sql=sql+",'"+TradeContext.EffectDate2[i]      +"'"
                        sql=sql+",'"+TradeContext.UpdateArea2[i][:10]      +"'"
                        sql=sql+",'"+TradeContext.UpdateBatch     +"'"
                        #sql=sql+",'"+TradeContext.NOTE1[i]           +"'"
                        #sql=sql+",'"+TradeContext.NOTE2[i]           +"'"
                        sql=sql+")"
                    AfaLoggerFunc.tradeInfo(sql)
                    if( AfaDBFunc.InsertSqlCmt(sql) == -1 ):
                        AfaLoggerFunc.tradeFatal(sql)
                        AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                        f = open("TIPS_BANKCODE","a")
                        f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                        f.close()
                        #return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                elif OperSign2=='2' or (OperSign2=='1' and len( records )!=0):#更新
                    sql="update TIPS_BANKCODE set "
                    if TradeContext.recNum==1:
                        sql=sql+" RECKBANKNO  ='"+TradeContext.ReckBankNo2      +"'"
                        sql=sql+",GENBANKNAME ='"+TradeContext.GenBankName2     +"'"
                        sql=sql+",RECKONTYPE  ='"+TradeContext.ReckonType2      +"'"
                        sql=sql+",OFNODECODE  ='"+TradeContext.OfNodeCode2      +"'"
                        sql=sql+",ADDRESS     ='"+TradeContext.Address2         +"'"
                        sql=sql+",POSTALCODE  ='"+TradeContext.PostalCode2      +"'"
                        sql=sql+",PEOPLENAME  ='"+TradeContext.PeopleName2      +"'"
                        sql=sql+",PEOPLEPHONE ='"+TradeContext.PeoplePhone2     +"'"
                        sql=sql+",PEOPLEMOBILE='"+TradeContext.PeopleMobile2    +"'"
                        sql=sql+",EMAIL       ='"+TradeContext.Email2           +"'"
                        sql=sql+",EFFECTDATE  ='"+TradeContext.EffectDate2      +"'"
                        sql=sql+",UPDATEAREA  ='"+TradeContext.UpdateArea2[:10]      +"'"
                        sql=sql+",UPDATEBATCH ='"+TradeContext.UpdateBatch     +"'"
                        #sql=sql+",NOTE1       ='"+TradeContext.NOTE1           +"'"
                        #sql=sql+",NOTE2       ='"+TradeContext.NOTE2           +"'"
                        sql=sql+" WHERE RECKBANKNO   ='"+TradeContext.ReckBankNo2      +"'"
                    else:         
                        sql=sql+" RECKBANKNO  ='"+TradeContext.ReckBankNo2[i]      +"'"
                        sql=sql+",GENBANKNAME ='"+TradeContext.GenBankName2[i]     +"'"
                        sql=sql+",RECKONTYPE  ='"+TradeContext.ReckonType2[i]      +"'"
                        sql=sql+",OFNODECODE  ='"+TradeContext.OfNodeCode2[i]      +"'"
                        sql=sql+",ADDRESS     ='"+TradeContext.Address2[i]         +"'"
                        sql=sql+",POSTALCODE  ='"+TradeContext.PostalCode2[i]      +"'"
                        sql=sql+",PEOPLENAME  ='"+TradeContext.PeopleName2[i]      +"'"
                        sql=sql+",PEOPLEPHONE ='"+TradeContext.PeoplePhone2[i]     +"'"
                        sql=sql+",PEOPLEMOBILE='"+TradeContext.PeopleMobile2[i]    +"'"
                        sql=sql+",EMAIL       ='"+TradeContext.Email2[i]           +"'"
                        sql=sql+",EFFECTDATE  ='"+TradeContext.EffectDate2[i]      +"'"
                        sql=sql+",UPDATEAREA  ='"+TradeContext.UpdateArea2[i][:10]      +"'"
                        sql=sql+",UPDATEBATCH ='"+TradeContext.UpdateBatch     +"'"
                        #sql=sql+",NOTE1       ='"+TradeContext.NOTE1[i]           +"'"
                        #sql=sql+",NOTE2       ='"+TradeContext.NOTE2[i]           +"'"
                        sql=sql+" WHERE RECKBANKNO   ='"+TradeContext.ReckBankNo2[i]      +"'"
                    AfaLoggerFunc.tradeInfo(sql)
                    if( AfaDBFunc.UpdateSqlCmt(sql) == -1 ):
                        AfaLoggerFunc.tradeFatal(sql)
                        AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                        f = open("TIPS_BANKCODE","a")
                        f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                        f.close()

#                        return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                elif OperSign2=='3' and len( records )!=0:#注销
                    sql="update TIPS_BANKCODE set "
                    sql=sql+" STATUS      ='"+'1'          +"'"
                    if TradeContext.recNum==1:
                        sql=sql+" WHERE RECKBANKNO   ='"+TradeContext.ReckBankNo2      +"'"
                    else:
                        sql=sql+" WHERE RECKBANKNO   ='"+TradeContext.ReckBankNo2[i]      +"'"
                    AfaLoggerFunc.tradeInfo(sql)
                    if( AfaDBFunc.UpdateSqlCmt(sql) == -1 ):
                        AfaLoggerFunc.tradeFatal(sql)
                        AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                        f = open("TIPS_BANKCODE","a")
                        f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                        f.close()

#                        return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
    return True

def TIPS_NODECODEDTL():
#节点代码
    #if( TradeContext.existVariable( "DataType103" ) ):
    if int(TradeContext.UpdateNum103) > 0:
        for i in range( 0, TradeContext.recNum ):
            sql="insert into TIPS_NODECODEDTL(NODECODE,NODENAME,OFNODETYPE,NODEDN,OPERSIGN,EFFECTDATE,UPDATEAREA,UPDATEBATCH)"
            sql=sql+" values"
            if TradeContext.recNum==1:
                sql=sql+"('"+TradeContext.NodeCode3      +"'"
                sql=sql+",'"+TradeContext.NodeName3      +"'"
                sql=sql+",'"+TradeContext.OfNodeType3    +"'"
                sql=sql+",'"+TradeContext.NodeDN3        +"'"
                sql=sql+",'"+TradeContext.OperSign3      +"'"
                sql=sql+",'"+TradeContext.EffectDate3    +"'"
                sql=sql+",'"+TradeContext.UpdateArea3[:10]    +"'"
                sql=sql+",'"+TradeContext.UpdateBatch     +"'"
                #sql=sql+",'"+TradeContext.NOTE1[i]           +"'"
                #sql=sql+",'"+TradeContext.NOTE2[i]           +"'"
                EffectDate3 =TradeContext.EffectDate3
                OperSign3   =TradeContext.OperSign3
                
            else:
                sql=sql+"('"+TradeContext.NodeCode3[i]      +"'"
                sql=sql+",'"+TradeContext.NodeName3[i]      +"'"
                sql=sql+",'"+TradeContext.OfNodeType3[i]    +"'"
                sql=sql+",'"+TradeContext.NodeDN3[i]        +"'"
                sql=sql+",'"+TradeContext.OperSign3[i]      +"'"
                sql=sql+",'"+TradeContext.EffectDate3[i]    +"'"
                sql=sql+",'"+TradeContext.UpdateArea3[i][:10]    +"'"
                sql=sql+",'"+TradeContext.UpdateBatch     +"'"
                #sql=sql+",'"+TradeContext.NOTE1[i]           +"'"
                #sql=sql+",'"+TradeContext.NOTE2[i]           +"'"
                EffectDate3 =TradeContext.EffectDate3[i]
                OperSign3   =TradeContext.OperSign3[i]
                
            sql=sql+")"
            AfaLoggerFunc.tradeInfo(sql)
            if( AfaDBFunc.InsertSqlCmt(sql) == -1 ):
                AfaLoggerFunc.tradeFatal(sql)
                AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                f = open("TIPS_NODECODEDTL","a")
                f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                f.close()
                #return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
            #如果生效日期为当日，即时生效
            if EffectDate3<=TradeContext.workDate:
                sql="select NODECODE from  TIPS_NODECODE "
                if TradeContext.recNum==1:
                    sql=sql+" WHERE NODECODE   ='"+TradeContext.NodeCode3      +"'"
                else:
                    sql=sql+" WHERE NODECODE   ='"+TradeContext.NodeCode3[i]      +"'"
                AfaLoggerFunc.tradeInfo(sql)
                records = AfaDBFunc.SelectSql(sql)
                if( records == None ):
                    AfaLoggerFunc.tradeFatal(sql)
                    return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                
                if OperSign3=='1' and len( records )==0: #新增
                    sql="insert into TIPS_NODECODE(NODECODE,NODENAME,OFNODETYPE,NODEDN,STATUS,RUNSTATUS,EFFECTDATE,UPDATEAREA,UPDATEBATCH)"
                    sql=sql+" values"
                    if TradeContext.recNum==1:
                        sql=sql+"('"+TradeContext.NodeCode3     +"'"
                        sql=sql+",'"+TradeContext.NodeName3     +"'"
                        sql=sql+",'"+TradeContext.OfNodeType3   +"'"
                        sql=sql+",'"+TradeContext.NodeDN3       +"'"
                        sql=sql+",'"+'0'                          +"'"
                        sql=sql+",'"+'0'                          +"'"
                        sql=sql+",'"+TradeContext.EffectDate3   +"'"
                        sql=sql+",'"+TradeContext.UpdateArea3[:10]   +"'"
                        sql=sql+",'"+TradeContext.UpdateBatch     +"'"
                        #sql=sql+",'"+TradeContext.NOTE1           +"'"
                        #sql=sql+",'"+TradeContext.NOTE2           +"'"
                        sql=sql+")"
                    else:
                        sql=sql+"('"+TradeContext.NodeCode3[i]      +"'"
                        sql=sql+",'"+TradeContext.NodeName3[i]      +"'"
                        sql=sql+",'"+TradeContext.OfNodeType3[i]    +"'"
                        sql=sql+",'"+TradeContext.NodeDN3[i]        +"'"
                        sql=sql+",'"+'0'                             +"'"
                        sql=sql+",'"+'0'                             +"'"
                        sql=sql+",'"+TradeContext.EffectDate3[i]    +"'"
                        sql=sql+",'"+TradeContext.UpdateArea3[i][:10]    +"'"
                        sql=sql+",'"+TradeContext.UpdateBatch     +"'"
                        #sql=sql+",'"+TradeContext.NOTE1[i]           +"'"
                        #sql=sql+",'"+TradeContext.NOTE2[i]           +"'"
                        sql=sql+")"
                    AfaLoggerFunc.tradeInfo(sql)
                    if( AfaDBFunc.InsertSqlCmt(sql) == -1 ):
                        AfaLoggerFunc.tradeFatal(sql)
                        AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                        f = open("TIPS_NODECODE","a")
                        f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                        f.close()
                        #return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                elif OperSign3=='2' or (OperSign3=='1' and len( records )!=0):#更新
                    sql="update TIPS_NODECODE set "
                    if TradeContext.recNum==1:
                        sql=sql+" NODECODE   ='"+TradeContext.NodeCode3       +"'"
                        sql=sql+",NODENAME   ='"+TradeContext.NodeName3       +"'"
                        sql=sql+",OFNODETYPE ='"+TradeContext.OfNodeType3     +"'"
                        sql=sql+",NODEDN     ='"+TradeContext.NodeDN3         +"'"
                        sql=sql+",RUNSTATUS  ='"+TradeContext.OperSign3       +"'"
                        sql=sql+",EFFECTDATE ='"+TradeContext.EffectDate3     +"'"
                        sql=sql+",UPDATEAREA ='"+TradeContext.UpdateArea3[:10]     +"'"
                        sql=sql+",UPDATEBATCH='"+TradeContext.UpdateBatch    +"'"
                        #sql=sql+",NOTE1       ='"+TradeContext.NOTE1           +"'"
                        #sql=sql+",NOTE2       ='"+TradeContext.NOTE2           +"'"
                        sql=sql+" WHERE NODECODE   ='"+TradeContext.NodeCode3      +"'"
                    else:         
                        sql=sql+" NODECODE    ='"+TradeContext.NodeCode3[i]      +"'"
                        sql=sql+",NODENAME    ='"+TradeContext.NodeName3[i]      +"'"
                        sql=sql+",OFNODETYPE  ='"+TradeContext.OfNodeType3[i]    +"'"
                        sql=sql+",NODEDN      ='"+TradeContext.NodeDN3[i]        +"'"
                        sql=sql+",RUNSTATUS   ='"+TradeContext.OperSign3[i]      +"'"
                        sql=sql+",EFFECTDATE  ='"+TradeContext.EffectDate3[i]    +"'"
                        sql=sql+",UPDATEAREA  ='"+TradeContext.UpdateArea3[i][:10]    +"'"
                        sql=sql+",UPDATEBATCH ='"+TradeContext.UpdateBatch     +"'"
                        #sql=sql+",NOTE1       ='"+TradeContext.NOTE1[i]           +"'"
                        #sql=sql+",NOTE2       ='"+TradeContext.NOTE2[i]           +"'"
                        sql=sql+" WHERE NODECODE   ='"+TradeContext.NodeCode3[i]      +"'"
                    AfaLoggerFunc.tradeInfo(sql)
                    if( AfaDBFunc.UpdateSqlCmt(sql) == -1 ):
                        AfaLoggerFunc.tradeFatal(sql)
                        AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                        f = open("TIPS_NODECODE","a")
                        f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                        f.close()

#                        return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                elif OperSign3=='3' and len( records )!=0:#注销
                    sql="update TIPS_NODECODE set "
                    sql=sql+" STATUS      ='"+'1'          +"'"
                    if TradeContext.recNum==1:
                        sql=sql+" WHERE NODECODE   ='"+TradeContext.NodeCode3      +"'"
                    else:
                        sql=sql+" WHERE NODECODE   ='"+TradeContext.NodeCode3[i]      +"'"
                    AfaLoggerFunc.tradeInfo(sql)
                    if( AfaDBFunc.UpdateSqlCmt(sql) == -1 ):
                        AfaLoggerFunc.tradeFatal(sql)
                        AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                        f = open("TIPS_NODECODE","a")
                        f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                        f.close()

#                        return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
    
    return True
def TIPS_TRECODEDTL():
    #国库代码
    #if( TradeContext.existVariable( "DataType104" ) ):
    if int(TradeContext.UpdateNum104) > 0:
        for i in range( 0, TradeContext.recNum ):
            sql="insert into TIPS_TRECODEDTL(TRECODE,TRENAME,TRELEVEL,PAYBANKNO,RECKONTRECODE,UPTRECODE,OFPROVTREA,"
            sql=sql+"OFCITYTREA,OFCOUNTYTREA,OFNODECODE,ADDRESS,POSTALCODE,PEOPLENAME,PEOPLEPHONE,PEOPLEMOBILE,"
            sql=sql+"EMAIL,OPERSIGN,EFFECTDATE,UPDATEAREA,UPDATEBATCH)"
            sql=sql+" values"
            if TradeContext.recNum==1:
                sql=sql+"('"+TradeContext.TreCode4          +"'"
                sql=sql+",'"+TradeContext.TreName4          +"'"
                sql=sql+",'"+TradeContext.TreLevel4         +"'"
                sql=sql+",'"+TradeContext.PayBankNo4        +"'"
                sql=sql+",'"+TradeContext.ReckonTreCode4    +"'"
                sql=sql+",'"+TradeContext.UpTreCode4        +"'"
                sql=sql+",'"+TradeContext.OfProvTrea4       +"'"
                sql=sql+",'"+TradeContext.OfCityTrea4       +"'"
                sql=sql+",'"+TradeContext.ofCountyTrea4     +"'"
                sql=sql+",'"+TradeContext.OfNodeCode4       +"'"
                sql=sql+",'"+TradeContext.Address4          +"'"
                sql=sql+",'"+TradeContext.PostalCode4       +"'"
                sql=sql+",'"+TradeContext.PeopleName4       +"'"
                sql=sql+",'"+TradeContext.PeoplePhone4      +"'"
                sql=sql+",'"+TradeContext.PeopleMobile4     +"'"
                sql=sql+",'"+TradeContext.Email4            +"'"
                sql=sql+",'"+TradeContext.OperSign4         +"'"
                sql=sql+",'"+TradeContext.EffectDate4       +"'"
                sql=sql+",'"+TradeContext.UpdateArea4[:10]       +"'"
                sql=sql+",'"+TradeContext.UpdateBatch       +"'"
                #sql=sql+",'"+TradeContext.NOTE1[i]           +"'"
                #sql=sql+",'"+TradeContext.NOTE2[i]           +"'"
                EffectDate4  = TradeContext.EffectDate4
                OperSign4    = TradeContext.OperSign4
            else:
                sql=sql+"('"+TradeContext.TreCode4[i]         +"'"
                sql=sql+",'"+TradeContext.TreName4[i]         +"'"
                sql=sql+",'"+TradeContext.TreLevel4[i]        +"'"
                sql=sql+",'"+TradeContext.PayBankNo4[i]       +"'"
                sql=sql+",'"+TradeContext.ReckonTreCode4[i]   +"'"
                sql=sql+",'"+TradeContext.UpTreCode4[i]       +"'"
                sql=sql+",'"+TradeContext.OfProvTrea4[i]      +"'"
                sql=sql+",'"+TradeContext.OfCityTrea4[i]      +"'"
                sql=sql+",'"+TradeContext.ofCountyTrea4[i]    +"'"
                sql=sql+",'"+TradeContext.OfNodeCode4[i]      +"'"
                sql=sql+",'"+TradeContext.Address4[i]         +"'"
                sql=sql+",'"+TradeContext.PostalCode4[i]      +"'"
                sql=sql+",'"+TradeContext.PeopleName4[i]      +"'"
                sql=sql+",'"+TradeContext.PeoplePhone4[i]     +"'"
                sql=sql+",'"+TradeContext.PeopleMobile4[i]    +"'"
                sql=sql+",'"+TradeContext.Email4[i]           +"'"
                sql=sql+",'"+TradeContext.OperSign4[i]        +"'"
                sql=sql+",'"+TradeContext.EffectDate4[i]      +"'"
                sql=sql+",'"+TradeContext.UpdateArea4[i][:10]      +"'"
                sql=sql+",'"+TradeContext.UpdateBatch        +"'"
                #sql=sql+",'"+TradeContext.NOTE1[i]           +"'"
                #sql=sql+",'"+TradeContext.NOTE2[i]           +"'"
                EffectDate4  = TradeContext.EffectDate4[i]
                OperSign4    = TradeContext.OperSign4[i]
            sql=sql+")"
            AfaLoggerFunc.tradeInfo(sql)
            if( AfaDBFunc.InsertSqlCmt(sql) == -1 ):
                AfaLoggerFunc.tradeFatal(sql)
                AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                f = open("TIPS_TRECODEDTL","a")
                f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                f.close()
                #return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
            #如果生效日期为当日，即时生效
            if EffectDate4<=TradeContext.workDate:
                sql="select TRECODE from  TIPS_TRECODE "
                if TradeContext.recNum==1:
                    sql=sql+" WHERE TRECODE   ='"+TradeContext.TreCode4      +"'"
                else:
                    sql=sql+" WHERE TRECODE   ='"+TradeContext.TreCode4[i]      +"'"
                AfaLoggerFunc.tradeInfo(sql)
                records = AfaDBFunc.SelectSql(sql)
                if( records == None ):
                    AfaLoggerFunc.tradeFatal(sql)
                    return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                
                if OperSign4=='1' and len( records )==0: #新增
                    sql="insert into TIPS_TRECODE(TRECODE,TRENAME,TRELEVEL,PAYBANKNO,RECKONTRECODE,UPTRECODE,"
                    sql=sql+"OFPROVTREA,OFCITYTREA,OFCOUNTYTREA,OFNODECODE,ADDRESS,POSTALCODE,PEOPLENAME,"
                    sql=sql+"PEOPLEPHONE,PEOPLEMOBILE,EMAIL,STATUS,EFFECTDATE,UPDATEAREA,UPDATEBATCH)"
                    sql=sql+" values"
                    if TradeContext.recNum==1:
                        sql=sql+"('"+TradeContext.TreCode4          +"'"
                        sql=sql+",'"+TradeContext.TreName4          +"'"
                        sql=sql+",'"+TradeContext.TreLevel4         +"'"
                        sql=sql+",'"+TradeContext.PayBankNo4        +"'"
                        sql=sql+",'"+TradeContext.ReckonTreCode4    +"'"
                        sql=sql+",'"+TradeContext.UpTreCode4        +"'"
                        sql=sql+",'"+TradeContext.OfProvTrea4       +"'"
                        sql=sql+",'"+TradeContext.OfCityTrea4       +"'"
                        sql=sql+",'"+TradeContext.ofCountyTrea4     +"'"
                        sql=sql+",'"+TradeContext.OfNodeCode4       +"'"
                        sql=sql+",'"+TradeContext.Address4          +"'"
                        sql=sql+",'"+TradeContext.PostalCode4       +"'"
                        sql=sql+",'"+TradeContext.PeopleName4       +"'"
                        sql=sql+",'"+TradeContext.PeoplePhone4      +"'"
                        sql=sql+",'"+TradeContext.PeopleMobile4     +"'"
                        sql=sql+",'"+TradeContext.Email4            +"'"
                        sql=sql+",'"+'0'                            +"'"
                        sql=sql+",'"+TradeContext.EffectDate4       +"'"
                        sql=sql+",'"+TradeContext.UpdateArea4[:10]       +"'"
                        sql=sql+",'"+TradeContext.UpdateBatch     +"'"
                        #sql=sql+",'"+TradeContext.NOTE1           +"'"
                        #sql=sql+",'"+TradeContext.NOTE2           +"'"
                        sql=sql+")"
                    else:
                        sql=sql+"('"+TradeContext.TreCode4[i]           +"'"
                        sql=sql+",'"+TradeContext.TreName4[i]           +"'"
                        sql=sql+",'"+TradeContext.TreLevel4[i]          +"'"
                        sql=sql+",'"+TradeContext.PayBankNo4[i]         +"'"
                        sql=sql+",'"+TradeContext.ReckonTreCode4[i]     +"'"
                        sql=sql+",'"+TradeContext.UpTreCode4[i]         +"'"
                        sql=sql+",'"+TradeContext.OfProvTrea4[i]        +"'"
                        sql=sql+",'"+TradeContext.OfCityTrea4[i]        +"'"
                        sql=sql+",'"+TradeContext.ofCountyTrea4[i]      +"'"
                        sql=sql+",'"+TradeContext.OfNodeCode4[i]        +"'"
                        sql=sql+",'"+TradeContext.Address4[i]           +"'"
                        sql=sql+",'"+TradeContext.PostalCode4[i]        +"'"
                        sql=sql+",'"+TradeContext.PeopleName4[i]        +"'"
                        sql=sql+",'"+TradeContext.PeoplePhone4[i]       +"'"
                        sql=sql+",'"+TradeContext.PeopleMobile4[i]      +"'"
                        sql=sql+",'"+TradeContext.Email4[i]             +"'"
                        sql=sql+",'"+'0'                                +"'"
                        sql=sql+",'"+TradeContext.EffectDate4[i]        +"'"
                        sql=sql+",'"+TradeContext.UpdateArea4[i][:10]      +"'"
                        sql=sql+",'"+TradeContext.UpdateBatch        +"'"
                        #sql=sql+",'"+TradeContext.NOTE1[i]           +"'"
                        #sql=sql+",'"+TradeContext.NOTE2[i]           +"'"
                        sql=sql+")"
                    AfaLoggerFunc.tradeInfo(sql)
                    if( AfaDBFunc.InsertSqlCmt(sql) == -1 ):
                        AfaLoggerFunc.tradeFatal(sql)
                        AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                        f = open("TIPS_TRECODE","a")
                        f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                        f.close()
                        #return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                elif OperSign4=='2' or (OperSign4=='1' and len( records )!=0):#更新
                    sql="update TIPS_TRECODE set "
                    if TradeContext.recNum==1:
                        sql=sql+" TRECODE      ='"+TradeContext.TreCode4          +"'"
                        sql=sql+",TRENAME      ='"+TradeContext.TreName4          +"'"
                        sql=sql+",TRELEVEL     ='"+TradeContext.TreLevel4         +"'"
                        sql=sql+",PAYBANKNO    ='"+TradeContext.PayBankNo4        +"'"
                        sql=sql+",RECKONTRECODE='"+TradeContext.ReckonTreCode4    +"'"
                        sql=sql+",UPTRECODE    ='"+TradeContext.UpTreCode4        +"'"
                        sql=sql+",OFPROVTREA   ='"+TradeContext.OfProvTrea4       +"'"
                        sql=sql+",OFCITYTREA   ='"+TradeContext.OfCityTrea4       +"'"
                        sql=sql+",OFCOUNTYTREA ='"+TradeContext.ofCountyTrea4     +"'"
                        sql=sql+",OFNODECODE   ='"+TradeContext.OfNodeCode4       +"'"
                        sql=sql+",ADDRESS      ='"+TradeContext.Address4          +"'"
                        sql=sql+",POSTALCODE   ='"+TradeContext.PostalCode4       +"'"
                        sql=sql+",PEOPLENAME   ='"+TradeContext.PeopleName4       +"'"
                        sql=sql+",PEOPLEPHONE  ='"+TradeContext.PeoplePhone4      +"'"
                        sql=sql+",PEOPLEMOBILE ='"+TradeContext.PeopleMobile4     +"'"
                        sql=sql+",EMAIL        ='"+TradeContext.Email4            +"'"
                        sql=sql+",EFFECTDATE   ='"+TradeContext.EffectDate4       +"'"
                        sql=sql+",UPDATEAREA   ='"+TradeContext.UpdateArea4[:10]       +"'"
                        sql=sql+",UPDATEBATCH  ='"+TradeContext.UpdateBatch      +"'"
                        #sql=sql+",NOTE1       ='"+TradeContext.NOTE1           +"'"
                        #sql=sql+",NOTE2       ='"+TradeContext.NOTE2           +"'"
                        sql=sql+" WHERE TRECODE   ='"+TradeContext.TreCode4      +"'"
                    else:
                        sql=sql+" TRECODE      ='"+TradeContext.TreCode4[i]          +"'"
                        sql=sql+",TRENAME      ='"+TradeContext.TreName4[i]          +"'"
                        sql=sql+",TRELEVEL     ='"+TradeContext.TreLevel4[i]         +"'"
                        sql=sql+",PAYBANKNO    ='"+TradeContext.PayBankNo4[i]        +"'"
                        sql=sql+",RECKONTRECODE='"+TradeContext.ReckonTreCode4[i]    +"'"
                        sql=sql+",UPTRECODE    ='"+TradeContext.UpTreCode4[i]        +"'"
                        sql=sql+",OFPROVTREA   ='"+TradeContext.OfProvTrea4[i]       +"'"
                        sql=sql+",OFCITYTREA   ='"+TradeContext.OfCityTrea4[i]       +"'"
                        sql=sql+",OFCOUNTYTREA ='"+TradeContext.ofCountyTrea4[i]     +"'"
                        sql=sql+",OFNODECODE   ='"+TradeContext.OfNodeCode4[i]       +"'"
                        sql=sql+",ADDRESS      ='"+TradeContext.Address4[i]          +"'"
                        sql=sql+",POSTALCODE   ='"+TradeContext.PostalCode4[i]       +"'"
                        sql=sql+",PEOPLENAME   ='"+TradeContext.PeopleName4[i]       +"'"
                        sql=sql+",PEOPLEPHONE  ='"+TradeContext.PeoplePhone4[i]      +"'"
                        sql=sql+",PEOPLEMOBILE ='"+TradeContext.PeopleMobile4[i]     +"'"
                        sql=sql+",EMAIL        ='"+TradeContext.Email4[i]            +"'"
                        sql=sql+",EFFECTDATE   ='"+TradeContext.EffectDate4[i]       +"'"
                        sql=sql+",UPDATEAREA   ='"+TradeContext.UpdateArea4[i][:10]       +"'"
                        sql=sql+",UPDATEBATCH  ='"+TradeContext.UpdateBatch          +"'"
                        #sql=sql+",NOTE1       ='"+TradeContext.NOTE1[i]           +"'"
                        #sql=sql+",NOTE2       ='"+TradeContext.NOTE2[i]           +"'"
                        sql=sql+" WHERE TRECODE   ='"+TradeContext.TreCode4[i]      +"'"
                    AfaLoggerFunc.tradeInfo(sql)
                    if( AfaDBFunc.UpdateSqlCmt(sql) == -1 ):
                        AfaLoggerFunc.tradeFatal(sql)
                        AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                        f = open("TIPS_TRECODE","a")
                        f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                        f.close()

#                        return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                elif OperSign4=='3' and len( records )!=0:#注销
                    sql="update TIPS_TRECODE set "
                    sql=sql+" STATUS      ='"+'1'          +"'"
                    if TradeContext.recNum==1:
                        sql=sql+" WHERE TRECODE   ='"+TradeContext.TreCode4      +"'"
                    else:
                        sql=sql+" WHERE TRECODE   ='"+TradeContext.TreCode4[i]      +"'"
                    AfaLoggerFunc.tradeInfo(sql)
                    if( AfaDBFunc.UpdateSqlCmt(sql) == -1 ):
                        AfaLoggerFunc.tradeFatal(sql)
                        AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                        f = open("TIPS_TRECODE","a")
                        f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                        f.close()

#                        return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
    return True
def TIPS_BUDGETSUBJECTCODEDTL():
    #预算科目代码
    #if( TradeContext.existVariable( "DataType105" ) ):
    if int(TradeContext.UpdateNum105) > 0:
        for i in range( 0, TradeContext.recNum ):
            sql="insert into TIPS_BUDGETSUBJECTCODEDTL(BUDGETSUBJECTCODE,BUDGETSUBJECTNAME,SUBJECTTYPE,IESIGN,BUDGETATTRIB,"
            sql=sql+"OPERSIGN,EFFECTDATE,UPDATEAREA,UPDATEBATCH)"
            sql=sql+" values"
            if TradeContext.recNum==1:
                sql=sql+"('"+TradeContext.BudgetSubjectCode5+"'"
                sql=sql+",'"+TradeContext.BudgetSubjectName5+"'"
                sql=sql+",'"+TradeContext.SubjectType5      +"'"
                sql=sql+",'"+TradeContext.IESign5           +"'"
                sql=sql+",'"+TradeContext.BudgetAttrib5     +"'"
                sql=sql+",'"+TradeContext.OperSign5         +"'"
                sql=sql+",'"+TradeContext.EffectDate5       +"'"
                sql=sql+",'"+TradeContext.UpdateArea5[:10]       +"'"
                sql=sql+",'"+TradeContext.UpdateBatch      +"'"
                EffectDate5  = TradeContext.EffectDate5
                OperSign5    = TradeContext.OperSign5
            else:
                sql=sql+"('"+TradeContext.BudgetSubjectCode5[i]+"'"
                sql=sql+",'"+TradeContext.BudgetSubjectName5[i]+"'"
                sql=sql+",'"+TradeContext.SubjectType5[i]      +"'"
                sql=sql+",'"+TradeContext.IESign5[i]           +"'"
                sql=sql+",'"+TradeContext.BudgetAttrib5[i]     +"'"
                sql=sql+",'"+TradeContext.OperSign5[i]         +"'"
                sql=sql+",'"+TradeContext.EffectDate5[i]       +"'"
                sql=sql+",'"+TradeContext.UpdateArea5[i][:10]       +"'"
                sql=sql+",'"+TradeContext.UpdateBatch      +"'"
                EffectDate5  = TradeContext.EffectDate5[i]
                OperSign5    = TradeContext.OperSign5[i]
            sql=sql+")"
            AfaLoggerFunc.tradeInfo(sql)
            if( AfaDBFunc.InsertSqlCmt(sql) == -1 ):
                AfaLoggerFunc.tradeFatal(sql)
                AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                f = open("TIPS_BUDGETSUBJECTCODEDTL","a")
                f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                f.close()
                #return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
            #如果生效日期为当日，即时生效
            if EffectDate5<=TradeContext.workDate:
                sql="select BUDGETSUBJECTCODE from  TIPS_BUDGETSUBJECTCODE "
                if TradeContext.recNum==1:
                    sql=sql+" WHERE BUDGETSUBJECTCODE   ='"+TradeContext.BudgetSubjectCode5      +"'"
                else:
                    sql=sql+" WHERE BUDGETSUBJECTCODE   ='"+TradeContext.BudgetSubjectCode5[i]      +"'"
                AfaLoggerFunc.tradeInfo(sql)
                records = AfaDBFunc.SelectSql(sql)
                if( records == None ):
                    AfaLoggerFunc.tradeFatal(sql)
                    return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                
                if OperSign5=='1' and len( records )==0: #新增
                    sql="insert into TIPS_BUDGETSUBJECTCODE(BUDGETSUBJECTCODE,BUDGETSUBJECTNAME,SUBJECTTYPE,IESIGN,"
                    sql=sql+"BUDGETATTRIB,STATUS,EFFECTDATE,UPDATEAREA,UPDATEBATCH)"
                    sql=sql+" values"
                    if TradeContext.recNum==1:
                        sql=sql+"('"+TradeContext.BudgetSubjectCode5    +"'"
                        sql=sql+",'"+TradeContext.BudgetSubjectName5    +"'"
                        sql=sql+",'"+TradeContext.SubjectType5          +"'"
                        sql=sql+",'"+TradeContext.IESign5               +"'"
                        sql=sql+",'"+TradeContext.BudgetAttrib5         +"'"
                        sql=sql+",'"+'0'                            +"'"
                        sql=sql+",'"+TradeContext.EffectDate5       +"'"
                        sql=sql+",'"+TradeContext.UpdateArea5[:10]       +"'"
                        sql=sql+",'"+TradeContext.UpdateBatch     +"'"
                        #sql=sql+",'"+TradeContext.NOTE1           +"'"
                        #sql=sql+",'"+TradeContext.NOTE2           +"'"
                        sql=sql+")"
                    else:
                        sql=sql+"('"+TradeContext.BudgetSubjectCode5[i]     +"'"
                        sql=sql+",'"+TradeContext.BudgetSubjectName5[i]     +"'"
                        sql=sql+",'"+TradeContext.SubjectType5[i]           +"'"
                        sql=sql+",'"+TradeContext.IESign5[i]                +"'"
                        sql=sql+",'"+TradeContext.BudgetAttrib5[i]          +"'"
                        sql=sql+",'"+'0'                                +"'"
                        sql=sql+",'"+TradeContext.EffectDate5[i]        +"'"
                        sql=sql+",'"+TradeContext.UpdateArea5[i][:10]      +"'"
                        sql=sql+",'"+TradeContext.UpdateBatch        +"'"
                        #sql=sql+",'"+TradeContext.NOTE1[i]           +"'"
                        #sql=sql+",'"+TradeContext.NOTE2[i]           +"'"
                        sql=sql+")"
                    AfaLoggerFunc.tradeInfo(sql)
                    if( AfaDBFunc.InsertSqlCmt(sql) == -1 ):
                        AfaLoggerFunc.tradeFatal(sql)
                        AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                        f = open("TIPS_BUDGETSUBJECTCODE","a")
                        f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                        f.close()
                        #return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                elif OperSign5=='2' or (OperSign5=='1' and len( records )!=0):#更新
                    sql="update TIPS_BUDGETSUBJECTCODE set "
                    if TradeContext.recNum==1:
                        sql=sql+" BUDGETSUBJECTCODE ='"+TradeContext.BudgetSubjectCode5    +"'"
                        sql=sql+",BUDGETSUBJECTNAME ='"+TradeContext.BudgetSubjectName5    +"'"
                        sql=sql+",SUBJECTTYPE       ='"+TradeContext.SubjectType5          +"'"
                        sql=sql+",IESIGN            ='"+TradeContext.IESign5               +"'"
                        sql=sql+",BUDGETATTRIB      ='"+TradeContext.BudgetAttrib5         +"'"
                        sql=sql+",EFFECTDATE        ='"+TradeContext.EffectDate5       +"'"
                        sql=sql+",UPDATEAREA        ='"+TradeContext.UpdateArea5[:10]       +"'"
                        sql=sql+",UPDATEBATCH       ='"+TradeContext.UpdateBatch      +"'"
                        sql=sql+" WHERE BUDGETSUBJECTCODE   ='"+TradeContext.BudgetSubjectCode5      +"'"
                        sql=sql+" AND SUBJECTTYPE   ='"+TradeContext.SubjectType5      +"'"
                        sql=sql+" AND IESIGN   ='"+TradeContext.IESign5      +"'"
                        sql=sql+" AND UPDATEAREA   ='"+TradeContext.UpdateArea5[:10]      +"'"
                    else:
                        sql=sql+" BUDGETSUBJECTCODE ='"+TradeContext.BudgetSubjectCode5[i]    +"'"
                        sql=sql+",BUDGETSUBJECTNAME ='"+TradeContext.BudgetSubjectName5[i]    +"'"
                        sql=sql+",SUBJECTTYPE       ='"+TradeContext.SubjectType5[i]          +"'"
                        sql=sql+",IESIGN            ='"+TradeContext.IESign5[i]               +"'"
                        sql=sql+",BUDGETATTRIB      ='"+TradeContext.BudgetAttrib5[i]         +"'"
                        sql=sql+",EFFECTDATE        ='"+TradeContext.EffectDate5[i]       +"'"
                        sql=sql+",UPDATEAREA        ='"+TradeContext.UpdateArea5[i][:10]       +"'"
                        sql=sql+",UPDATEBATCH       ='"+TradeContext.UpdateBatch          +"'"
                        sql=sql+" WHERE BUDGETSUBJECTCODE   ='"+TradeContext.BudgetSubjectCode5[i]      +"'"
                        sql=sql+" AND SUBJECTTYPE   ='"+TradeContext.SubjectType5[i]      +"'"
                        sql=sql+" AND IESIGN   ='"+TradeContext.IESign5[i]      +"'"
                        sql=sql+" AND UPDATEAREA   ='"+TradeContext.UpdateArea5[i][:10]      +"'"
                    AfaLoggerFunc.tradeInfo(sql)
                    if( AfaDBFunc.UpdateSqlCmt(sql) == -1 ):
                        AfaLoggerFunc.tradeFatal(sql)
                        AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                        f = open("TIPS_BUDGETSUBJECTCODE","a")
                        f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                        f.close()

#                        return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                elif OperSign5=='3' and len( records )!=0:#注销
                    sql="update TIPS_BUDGETSUBJECTCODE set "
                    sql=sql+" STATUS      ='"+'1'          +"'"
                    if TradeContext.recNum==1:
                        sql=sql+" WHERE BUDGETSUBJECTCODE   ='"+TradeContext.BudgetSubjectCode5      +"'"
                        sql=sql+" AND SUBJECTTYPE   ='"+TradeContext.SubjectType5      +"'"
                        sql=sql+" AND IESIGN   ='"+TradeContext.IESign5      +"'"
                        sql=sql+" AND UPDATEAREA   ='"+TradeContext.UpdateArea5[:10]      +"'"
                    else:
                        sql=sql+" WHERE BUDGETSUBJECTCODE   ='"+TradeContext.BudgetSubjectCode5[i]   +"'"
                        sql=sql+" AND SUBJECTTYPE   ='"+TradeContext.SubjectType5[i]      +"'"
                        sql=sql+" AND IESIGN   ='"+TradeContext.IESign5[i]      +"'"
                        sql=sql+" AND UPDATEAREA   ='"+TradeContext.UpdateArea5[i][:10]      +"'"
                    AfaLoggerFunc.tradeInfo(sql)
                    if( AfaDBFunc.UpdateSqlCmt(sql) == -1 ):
                        AfaLoggerFunc.tradeFatal(sql)
                        AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                        f = open("TIPS_BUDGETSUBJECTCODE","a")
                        f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                        f.close()

#                        return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
    return True
def TIPS_RETURNREASONCODEDTL():
    #退库原因代码
    #if( TradeContext.existVariable( "DataType106" ) ):
    if int(TradeContext.UpdateNum106) > 0:
        for i in range( 0, TradeContext.recNum ):
            sql="insert into TIPS_RETURNREASONCODEDTL(REASONCODE,DESCRIPTION,OPERSIGN,EFFECTDATE,UPDATEAREA,UPDATEBATCH)"
            sql=sql+" values"
            if TradeContext.recNum==1:
                sql=sql+"('"+TradeContext.ReasonCode6   +"'"
                sql=sql+",'"+TradeContext.Description6  +"'"
                sql=sql+",'"+TradeContext.OperSign6     +"'"
                sql=sql+",'"+TradeContext.EffectDate6   +"'"
                sql=sql+",'"+TradeContext.UpdateArea6[:10]   +"'"
                sql=sql+",'"+TradeContext.UpdateBatch   +"'"
                EffectDate6  = TradeContext.EffectDate6
                OperSign6    = TradeContext.OperSign6
            else:
                sql=sql+"('"+TradeContext.ReasonCode6[i] +"'"
                sql=sql+",'"+TradeContext.Description6[i]+"'"
                sql=sql+",'"+TradeContext.OperSign6[i]   +"'"
                sql=sql+",'"+TradeContext.EffectDate6[i] +"'"
                sql=sql+",'"+TradeContext.UpdateArea6[i][:10] +"'"
                sql=sql+",'"+TradeContext.UpdateBatch   +"'"
                EffectDate6  = TradeContext.EffectDate6[i]
                OperSign6    = TradeContext.OperSign6[i]
            sql=sql+")"
            AfaLoggerFunc.tradeInfo(sql)
            if( AfaDBFunc.InsertSqlCmt(sql) == -1 ):
                AfaLoggerFunc.tradeFatal(sql)
                return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
            #如果生效日期为当日，即时生效
            if EffectDate6<=TradeContext.workDate:
                sql="select REASONCODE from  TIPS_RETURNREASONCODE "
                if TradeContext.recNum==1:
                    sql=sql+" WHERE REASONCODE   ='"+TradeContext.ReasonCode6      +"'"
                else:
                    sql=sql+" WHERE REASONCODE   ='"+TradeContext.ReasonCode6[i]      +"'"
                AfaLoggerFunc.tradeInfo(sql)
                records = AfaDBFunc.SelectSql(sql)
                if( records == None ):
                    AfaLoggerFunc.tradeFatal(sql)
                    AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                    f = open("TIPS_RETURNREASONCODE","a")
                    f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                    f.close()

#                    return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                
                if OperSign6=='1' and len( records )==0: #新增
                    sql="insert into TIPS_RETURNREASONCODE(REASONCODE,DESCRIPTION,OPERSIGN,EFFECTDATE,UPDATEAREA,UPDATEBATCH)"
                    sql=sql+" values"
                    if TradeContext.recNum==1:
                        sql=sql+"('"+TradeContext.ReasonCode6   +"'"
                        sql=sql+",'"+TradeContext.Description6  +"'"
                        sql=sql+",'"+TradeContext.OperSign6     +"'"
                        sql=sql+",'"+'0'                            +"'"
                        sql=sql+",'"+TradeContext.EffectDate5       +"'"
                        sql=sql+",'"+TradeContext.UpdateArea5[:10]       +"'"
                        sql=sql+",'"+TradeContext.UpdateBatch     +"'"
                        #sql=sql+",'"+TradeContext.NOTE1           +"'"
                        #sql=sql+",'"+TradeContext.NOTE2           +"'"
                        sql=sql+")"
                    else:
                        sql=sql+"('"+TradeContext.ReasonCode6[i]     +"'"
                        sql=sql+",'"+TradeContext.Description6[i]     +"'"
                        sql=sql+",'"+TradeContext.OperSign6[i]           +"'"
                        sql=sql+",'"+'0'                                +"'"
                        sql=sql+",'"+TradeContext.EffectDate6[i]        +"'"
                        sql=sql+",'"+TradeContext.UpdateArea6[i][:10]      +"'"
                        sql=sql+",'"+TradeContext.UpdateBatch        +"'"
                        #sql=sql+",'"+TradeContext.NOTE1[i]           +"'"
                        #sql=sql+",'"+TradeContext.NOTE2[i]           +"'"
                        sql=sql+")"
                    AfaLoggerFunc.tradeInfo(sql)
                    if( AfaDBFunc.InsertSqlCmt(sql) == -1 ):
                        AfaLoggerFunc.tradeFatal(sql)
                        AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                        f = open("TIPS_RETURNREASONCODE","a")
                        f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                        f.close()

#                        return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                elif OperSign6=='2' or (OperSign6=='1' and len( records )!=0):#更新
                    sql="update TIPS_BUDGETSUBJECTCODE set "
                    if TradeContext.recNum==1:
                        sql=sql+" REASONCODE        ='"+TradeContext.ReasonCode6   +"'"
                        sql=sql+",DESCRIPTION       ='"+TradeContext.Description6  +"'"
                        sql=sql+",OPERSIGN          ='"+TradeContext.OperSign6     +"'"
                        sql=sql+",EFFECTDATE        ='"+TradeContext.EffectDate6       +"'"
                        sql=sql+",UPDATEAREA        ='"+TradeContext.UpdateArea6[:10]       +"'"
                        sql=sql+",UPDATEBATCH       ='"+TradeContext.UpdateBatch      +"'"
                        sql=sql+" WHERE REASONCODE   ='"+TradeContext.ReasonCode6      +"'"
                    else:
                        sql=sql+" REASONCODE        ='"+TradeContext.ReasonCode6[i]    +"'"
                        sql=sql+",DESCRIPTION       ='"+TradeContext.Description6[i]    +"'"
                        sql=sql+",OPERSIGN          ='"+TradeContext.OperSign6[i]          +"'"
                        sql=sql+",EFFECTDATE        ='"+TradeContext.EffectDate6[i]       +"'"
                        sql=sql+",UPDATEAREA        ='"+TradeContext.UpdateArea6[i][:10]       +"'"
                        sql=sql+",UPDATEBATCH       ='"+TradeContext.UpdateBatch          +"'"
                        sql=sql+" WHERE REASONCODE   ='"+TradeContext.ReasonCode6[i]      +"'"
                    AfaLoggerFunc.tradeInfo(sql)
                    if( AfaDBFunc.UpdateSqlCmt(sql) == -1 ):
                        AfaLoggerFunc.tradeFatal(sql)
                        AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                        f = open("TIPS_RETURNREASONCODE","a")
                        f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                        f.close()

#                        return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                elif OperSign6=='3' and len( records )!=0:#注销
                    sql="update TIPS_RETURNREASONCODE set "
                    sql=sql+" STATUS      ='"+'1'          +"'"
                    if TradeContext.recNum==1:
                        sql=sql+" WHERE REASONCODE   ='"+TradeContext.ReasonCode6           +"'"
                    else:
                        sql=sql+" WHERE REASONCODE   ='"+TradeContext.ReasonCode6[i]        +"'"
                    AfaLoggerFunc.tradeInfo(sql)
                    if( AfaDBFunc.UpdateSqlCmt(sql) == -1 ):
                        AfaLoggerFunc.tradeFatal(sql)
                        AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                        f = open("TIPS_RETURNREASONCODE","a")
                        f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                        f.close()

#                        return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
    return True
def TIPS_CORRECTREASONCODEDTL():
    #更正原因代码
    #if( TradeContext.existVariable( "DataType107" ) ):
    if int(TradeContext.UpdateNum107) > 0:
        for i in range( 0, TradeContext.recNum ):
            sql="insert into TIPS_CORRECTREASONCODEDTL(REASONCODE,DESCRIPTION,OPERSIGN,EFFECTDATE,UPDATEAREA,UPDATEBATCH)"
            sql=sql+" values"
            if TradeContext.recNum==1:
                sql=sql+"('"+TradeContext.ReasonCode7   +"'"
                sql=sql+",'"+TradeContext.Description7  +"'"
                sql=sql+",'"+TradeContext.OperSign7     +"'"
                sql=sql+",'"+TradeContext.EffectDate7   +"'"
                sql=sql+",'"+TradeContext.UpdateArea7[:10]   +"'"
                sql=sql+",'"+TradeContext.UpdateBatch   +"'"
                EffectDate7  = TradeContext.EffectDate7
                OperSign7    = TradeContext.OperSign7
            else:
                sql=sql+"('"+TradeContext.ReasonCode7[i] +"'"
                sql=sql+",'"+TradeContext.Description7[i]+"'"
                sql=sql+",'"+TradeContext.OperSign7[i]   +"'"
                sql=sql+",'"+TradeContext.EffectDate7[i] +"'"
                sql=sql+",'"+TradeContext.UpdateArea7[i][:10] +"'"
                sql=sql+",'"+TradeContext.UpdateBatch   +"'"
                EffectDate7  = TradeContext.EffectDate7[i]
                OperSign7    = TradeContext.OperSign7[i]
            sql=sql+")"
            AfaLoggerFunc.tradeInfo(sql)
            if( AfaDBFunc.InsertSqlCmt(sql) == -1 ):
                AfaLoggerFunc.tradeFatal(sql)
                return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
            #如果生效日期为当日，即时生效
            if EffectDate7<=TradeContext.workDate:
                sql="select REASONCODE from  TIPS_CORRECTREASONCODE "
                if TradeContext.recNum==1:
                    sql=sql+" WHERE REASONCODE   ='"+TradeContext.ReasonCode7      +"'"
                else:
                    sql=sql+" WHERE REASONCODE   ='"+TradeContext.ReasonCode7[i]      +"'"
                AfaLoggerFunc.tradeInfo(sql)
                records = AfaDBFunc.SelectSql(sql)
                if( records == None ):
                    AfaLoggerFunc.tradeFatal(sql)
                    AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                    f = open("TIPS_CORRECTREASONCODE","a")
                    f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                    f.close()

#                    return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                
                if OperSign7=='1' and len( records )==0: #新增
                    sql="insert into TIPS_CORRECTREASONCODE(REASONCODE,DESCRIPTION,OPERSIGN,EFFECTDATE,UPDATEAREA,UPDATEBATCH)"
                    sql=sql+" values"
                    if TradeContext.recNum==1:
                        sql=sql+"('"+TradeContext.ReasonCode7      +"'"
                        sql=sql+",'"+TradeContext.Description7     +"'"
                        sql=sql+",'"+TradeContext.OperSign7        +"'"
                        sql=sql+",'"+'0'                            +"'"
                        sql=sql+",'"+TradeContext.EffectDate7       +"'"
                        sql=sql+",'"+TradeContext.UpdateArea7[:10]       +"'"
                        sql=sql+",'"+TradeContext.UpdateBatch     +"'"
                        #sql=sql+",'"+TradeContext.NOTE1           +"'"
                        #sql=sql+",'"+TradeContext.NOTE2           +"'"
                        sql=sql+")"
                    else:
                        sql=sql+"('"+TradeContext.ReasonCode7[i]      +"'"
                        sql=sql+",'"+TradeContext.Description7[i]     +"'"
                        sql=sql+",'"+TradeContext.OperSign7[i]        +"'"
                        sql=sql+",'"+'0'                                +"'"
                        sql=sql+",'"+TradeContext.EffectDate7[i]        +"'"
                        sql=sql+",'"+TradeContext.UpdateArea7[i][:10]      +"'"
                        sql=sql+",'"+TradeContext.UpdateBatch        +"'"
                        #sql=sql+",'"+TradeContext.NOTE1[i]           +"'"
                        #sql=sql+",'"+TradeContext.NOTE2[i]           +"'"
                        sql=sql+")"
                    AfaLoggerFunc.tradeInfo(sql)
                    if( AfaDBFunc.InsertSqlCmt(sql) == -1 ):
                        AfaLoggerFunc.tradeFatal(sql)
                        AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                        f = open("TIPS_CORRECTREASONCODE","a")
                        f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                        f.close()

#                        return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                elif OperSign7=='2' or (OperSign7=='1' and len( records )!=0):#更新
                    sql="update TIPS_CORRECTREASONCODE set "
                    if TradeContext.recNum==1:
                        sql=sql+" REASONCODE        ='"+TradeContext.ReasonCode7    +"'"
                        sql=sql+",DESCRIPTION       ='"+TradeContext.Description7    +"'"
                        sql=sql+",OPERSIGN          ='"+TradeContext.OperSign7          +"'"
                        sql=sql+",EFFECTDATE        ='"+TradeContext.EffectDate7       +"'"
                        sql=sql+",UPDATEAREA        ='"+TradeContext.UpdateArea7[:10]       +"'"
                        sql=sql+",UPDATEBATCH       ='"+TradeContext.UpdateBatch      +"'"
                        sql=sql+" WHERE REASONCODE   ='"+TradeContext.ReasonCode7      +"'"
                    else:
                        sql=sql+" REASONCODE        ='"+TradeContext.ReasonCode7[i]    +"'"
                        sql=sql+",DESCRIPTION       ='"+TradeContext.Description7[i]    +"'"
                        sql=sql+",OPERSIGN          ='"+TradeContext.OperSign7[i]          +"'"
                        sql=sql+",EFFECTDATE        ='"+TradeContext.EffectDate7[i]       +"'"
                        sql=sql+",UPDATEAREA        ='"+TradeContext.UpdateArea7[i][:10]       +"'"
                        sql=sql+",UPDATEBATCH       ='"+TradeContext.UpdateBatch          +"'"
                        sql=sql+" WHERE REASONCODE   ='"+TradeContext.ReasonCode7[i]      +"'"
                    AfaLoggerFunc.tradeInfo(sql)
                    if( AfaDBFunc.UpdateSqlCmt(sql) == -1 ):
                        AfaLoggerFunc.tradeFatal(sql)
                        AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                        f = open("TIPS_CORRECTREASONCODE","a")
                        f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                        f.close()

#                        return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                elif OperSign7=='3' and len( records )!=0:#注销
                    sql="update TIPS_CORRECTREASONCODE set "
                    sql=sql+" STATUS      ='"+'1'          +"'"
                    if TradeContext.recNum==1:
                        sql=sql+" WHERE REASONCODE   ='"+TradeContext.ReasonCode7      +"'"
                    else:
                        sql=sql+" WHERE REASONCODE   ='"+TradeContext.ReasonCode7[i]      +"'"
                    AfaLoggerFunc.tradeInfo(sql)
                    if( AfaDBFunc.UpdateSqlCmt(sql) == -1 ):
                        AfaLoggerFunc.tradeFatal(sql)
                        AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                        f = open("TIPS_CORRECTREASONCODE","a")
                        f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                        f.close()

#                        return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
    return True
def TIPS_TAXTYPECODEDTL():
    #税种代码
    #if( TradeContext.existVariable( "DataType108" ) ):
    if int(TradeContext.UpdateNum108) > 0:
        for i in range( 0, TradeContext.recNum ):
            sql="insert into TIPS_TAXTYPECODEDTL(TAXTYPECODE,TAXORGTYPE,TAXTYPENAME,DESCRIPTION,OPERSIGN,EFFECTDATE,UPDATEAREA,UPDATEBATCH)"
            sql=sql+" values"
            if TradeContext.recNum==1:
                sql=sql+"('"+TradeContext.TaxTypeCode8      +"'"
                sql=sql+",'"+TradeContext.TaxOrgType8       +"'"
                sql=sql+",'"+TradeContext.TaxTypeName8      +"'"
                sql=sql+",'"+TradeContext.Description8      +"'"
                sql=sql+",'"+TradeContext.OperSign8         +"'"
                sql=sql+",'"+TradeContext.EffectDate8       +"'"
                sql=sql+",'"+TradeContext.UpdateArea8[:10]       +"'"
                sql=sql+",'"+TradeContext.UpdateBatch       +"'"
                EffectDate8  = TradeContext.EffectDate8
                OperSign8    = TradeContext.OperSign8
            else:
                sql=sql+"('"+TradeContext.TaxTypeCode8[i] +"'"
                sql=sql+",'"+TradeContext.TaxOrgType8[i]+"'"
                sql=sql+",'"+TradeContext.TaxTypeName8[i]   +"'"
                sql=sql+",'"+TradeContext.Description8[i] +"'"
                sql=sql+",'"+TradeContext.OperSign8[i]+"'"
                sql=sql+",'"+TradeContext.EffectDate8[i] +"'"
                sql=sql+",'"+TradeContext.UpdateArea8[i][:10] +"'"
                sql=sql+",'"+TradeContext.UpdateBatch   +"'"
                EffectDate8  = TradeContext.EffectDate8[i]
                OperSign8    = TradeContext.OperSign8[i]
            sql=sql+")"
            AfaLoggerFunc.tradeInfo(sql)
            if( AfaDBFunc.InsertSqlCmt(sql) == -1 ):
                AfaLoggerFunc.tradeFatal(sql)
                AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                f = open("TIPS_TAXTYPECODEDTL","a")
                f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                f.close()
                #return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
            #如果生效日期为当日，即时生效
            if EffectDate8<=TradeContext.workDate:
                sql="select TAXTYPECODE from  TIPS_TAXTYPECODE "
                if TradeContext.recNum==1:
                    sql=sql+" WHERE TAXTYPECODE   ='"+TradeContext.TaxTypeCode8      +"'"
                    sql=sql+" AND TAXORGTYPE   ='"+TradeContext.TaxOrgType8      +"'"
                else:
                    sql=sql+" WHERE TAXTYPECODE   ='"+TradeContext.TaxTypeCode8[i]      +"'"
                    sql=sql+" AND TAXORGTYPE   ='"+TradeContext.TaxOrgType8[i]      +"'"
                AfaLoggerFunc.tradeInfo(sql)
                records = AfaDBFunc.SelectSql(sql)
                if( records == None ):
                    AfaLoggerFunc.tradeFatal(sql)
                    AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                    f = open("TIPS_TAXTYPECODEDTL","a")
                    f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                    f.close()

#                    return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                
                if OperSign8=='1' and len( records )==0: #新增
                    sql="insert into TIPS_TAXTYPECODE(TAXTYPECODE,TAXORGTYPE,TAXTYPENAME,DESCRIPTION,OPERSIGN,EFFECTDATE,UPDATEAREA,UPDATEBATCH)"
                    sql=sql+" values"
                    if TradeContext.recNum==1:
                        sql=sql+"('"+TradeContext.TaxTypeCode8      +"'"
                        sql=sql+",'"+TradeContext.TaxOrgType8     +"'"
                        sql=sql+",'"+TradeContext.TaxTypeName8        +"'"
                        sql=sql+",'"+TradeContext.Description8        +"'"
                        sql=sql+",'"+TradeContext.OperSign8        +"'"
                        #sql=sql+",'"+'0'                            +"'"
                        sql=sql+",'"+TradeContext.EffectDate8       +"'"
                        sql=sql+",'"+TradeContext.UpdateArea8[:10]       +"'"
                        sql=sql+",'"+TradeContext.UpdateBatch     +"'"
                        #sql=sql+",'"+TradeContext.NOTE1           +"'"
                        #sql=sql+",'"+TradeContext.NOTE2           +"'"
                        sql=sql+")"
                    else:
                        sql=sql+"('"+TradeContext.TaxTypeCode8[i]      +"'"
                        sql=sql+",'"+TradeContext.TaxOrgType8[i]     +"'"
                        sql=sql+",'"+TradeContext.TaxTypeName8[i]        +"'"
                        sql=sql+",'"+TradeContext.Description8[i]        +"'"
                        sql=sql+",'"+TradeContext.OperSign8[i]        +"'"
                        #sql=sql+",'"+'0'                                +"'"
                        sql=sql+",'"+TradeContext.EffectDate8[i]        +"'"
                        sql=sql+",'"+TradeContext.UpdateArea8[i][:10]      +"'"
                        sql=sql+",'"+TradeContext.UpdateBatch        +"'"
                        #sql=sql+",'"+TradeContext.NOTE1[i]           +"'"
                        #sql=sql+",'"+TradeContext.NOTE2[i]           +"'"
                        sql=sql+")"
                    AfaLoggerFunc.tradeInfo(sql)
                    if( AfaDBFunc.InsertSqlCmt(sql) == -1 ):
                        AfaLoggerFunc.tradeFatal(sql)
                        AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                        f = open("TIPS_TAXTYPECODE","a")
                        f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                        f.close()
                        #return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                elif OperSign8=='2' or (OperSign8=='1' and len( records )!=0):#更新
                    sql="update TIPS_TAXTYPECODE set "
                    if TradeContext.recNum==1:
                        sql=sql+" TAXTYPECODE       ='"+TaxTypeCode8  +"'"
                        sql=sql+",TAXORGTYPE        ='"+TaxOrgType8    +"'"
                        sql=sql+",TAXTYPENAME       ='"+TaxTypeName8      +"'"
                        sql=sql+",DESCRIPTION       ='"+Description8  +"'"
                        sql=sql+",OPERSIGN          ='"+OperSign8      +"'"
                        sql=sql+",EFFECTDATE        ='"+TradeContext.EffectDate8       +"'"
                        sql=sql+",UPDATEAREA        ='"+TradeContext.UpdateArea8[:10]       +"'"
                        sql=sql+",UPDATEBATCH       ='"+TradeContext.UpdateBatch      +"'"
                        sql=sql+" WHERE TAXTYPECODE   ='"+TradeContext.TaxTypeCode8      +"'"
                        sql=sql+" AND TAXORGTYPE   ='"+TradeContext.TaxOrgType8      +"'"
                    else:
                        sql=sql+" TAXTYPECODE       ='"+TradeContext.TaxTypeCode8[i]   +"'"
                        sql=sql+",TAXORGTYPE        ='"+TradeContext.TaxOrgType8[i]     +"'"
                        sql=sql+",TAXTYPENAME       ='"+TradeContext.TaxTypeName8[i]   +"'"
                        sql=sql+",DESCRIPTION       ='"+TradeContext.Description8[i]    +"'"
                        sql=sql+",OPERSIGN          ='"+TradeContext.OperSign8[i]          +"'"
                        sql=sql+",EFFECTDATE        ='"+TradeContext.EffectDate8[i]       +"'"
                        sql=sql+",UPDATEAREA        ='"+TradeContext.UpdateArea8[i][:10]       +"'"
                        sql=sql+",UPDATEBATCH       ='"+TradeContext.UpdateBatch          +"'"
                        sql=sql+" WHERE TAXTYPECODE   ='"+TradeContext.TaxTypeCode8[i]      +"'"
                        sql=sql+" AND TAXORGTYPE   ='"+TradeContext.TaxOrgType8[i]      +"'"
                    AfaLoggerFunc.tradeInfo(sql)
                    if( AfaDBFunc.UpdateSqlCmt(sql) == -1 ):
                        AfaLoggerFunc.tradeFatal(sql)
                        AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                        f = open("TIPS_TAXTYPECODE","a")
                        f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                        f.close()

#                        return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
                elif OperSign8=='3' and len( records )!=0:#注销
                    sql="update TIPS_TAXTYPECODE set "
                    sql=sql+" STATUS      ='"+'1'          +"'"
                    if TradeContext.recNum==1:
                        sql=sql+" WHERE TAXTYPECODE     ='"+TradeContext.TaxTypeCode8      +"'"
                        sql=sql+" AND TAXORGTYPE        ='"+TradeContext.TaxOrgType8      +"'"
                    else:
                        sql=sql+" WHERE TAXTYPECODE     ='"+TradeContext.TaxTypeCode8[i]      +"'"
                        sql=sql+" AND TAXORGTYPE        ='"+TradeContext.TaxOrgType8[i]      +"'"
                    AfaLoggerFunc.tradeInfo(sql)
                    if( AfaDBFunc.UpdateSqlCmt(sql) == -1 ):
                        AfaLoggerFunc.tradeFatal(sql)
                        AfaLoggerFunc.tradeFatal(AfaDBFunc.sqlErrMsg)
                        f = open("TIPS_TAXTYPECODE","a")
                        f.write(sql + "\n" + AfaDBFunc.sqlErrMsg + "\n\n")
                        f.close()

#                        return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
    return True
  
