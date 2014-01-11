# -*- coding: gbk -*-
##################################################################
#   财税库行.三方协议查询.柜面发起
#=================================================================
#   程序文件:   003001_91141.py
#   修改时间:   2006-04-05
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools, TipsFunc,AfaDBFunc
from types import *

def SubModuleMainFst( ):

    AfaLoggerFunc.tradeInfo( '进入客户签约查询[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
        #=============获取当前系统时间====================
        TradeContext.workDate=UtilTools.GetSysDate( )
        TradeContext.workTime=UtilTools.GetSysTime( )

          #============校验公共节点的有效性==================
        # 完整性检查
        if( not TradeContext.existVariable( "channelCode" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '渠道代码[channelCode]值不存在!' )
        if( not TradeContext.existVariable( "zoneno" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '分行号[zoneno]值不存在!' )
        if( not TradeContext.existVariable( "brno" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '行所号[brno]值不存在!' )
        if( not TradeContext.existVariable( "opType" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '操作类型[opType]值不存在!' )
        if( not TradeContext.existVariable( "taxOrgCode" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '征收机关代码[taxOrgCode]值不存在!' )
        if( not TradeContext.existVariable( "taxPayCode" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '纳税人编码[taxPayCode]值不存在!' )
        if( not TradeContext.existVariable( "accno" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '付款账户[accno]值不存在!' )
        if( not TradeContext.existVariable( "protocolNo" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '协议书号[protocolNo]值不存在!' )

        if TradeContext.opType=='0':
            AfaLoggerFunc.tradeInfo('>>>查询')
            #=============判断状态====================
            sql="SELECT STATUS,TAXPAYCODE,PROTOCOLNO,PAYACCT,IDTYPE,IDCODE,TAXPAYNAME,"
            sql=sql+"TAXORGCODE,HANDORGNAME,STARTDATE,ENDDATE,ZONENO,BRNO,TELLERNO,WORKDATE,"
            sql=sql+"NOTE1,NOTE2,NOTE3,NOTE4,NOTE5"
            sql=sql+" FROM TIPS_CUSTINFO WHERE 1=1 "
            sql=sql+" and TAXORGCODE     ='"+TradeContext.taxOrgCode  +"'"
            
            if( len(TradeContext.taxPayCode) != 0 ):
            	AfaLoggerFunc.tradeInfo('>>>' + TradeContext.taxPayCode)
            	sql=sql+" AND TAXPAYCODE ='"+TradeContext.taxPayCode +"'"
            if( len(TradeContext.accno) != 0 ):
            	sql=sql+" and PAYACCT     ='"+TradeContext.accno  +"'"
            if( len(TradeContext.protocolNo) != 0 ):
            	sql=sql+" and PROTOCOLNO     ='"+TradeContext.protocolNo  +"'"
            
            AfaLoggerFunc.tradeInfo(sql)
            records = AfaDBFunc.SelectSql(sql)
            if( records == None ):
                AfaLoggerFunc.tradeFatal(sql)
                return TipsFunc.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
            elif( len( records )==0 ):
                return TipsFunc.ExitThisFlow( 'A0027', '该客户尚未签约' )
            elif( len( records )>1 ):
                return TipsFunc.ExitThisFlow( 'A0027', '存在多条签约记录' )
            else:
                AfaLoggerFunc.tradeFatal(sql)
                AfaLoggerFunc.tradeInfo(records[0][0])
                UtilTools.ListFilterNone( records )
                if (records[0][0]=='1'):
                    TradeContext.status='协议已验证，可正常使用'
                elif (records[0][0]=='2'):
                    TradeContext.status='银行端已签约，等待征收机关验证协议'
                elif (records[0][0]=='3'):
                    TradeContext.status='银行端已解约，等待征收机关撤销协议'
                else:
                    TradeContext.status='协议已撤消'
                TradeContext.taxPayCode =records[0][1]
                TradeContext.protocolNo =records[0][2]
                TradeContext.accno      =records[0][3]
                TradeContext.idType     =records[0][4]
                TradeContext.idCode     =records[0][5]
                TradeContext.taxPayName =records[0][6]
                TradeContext.taxOrgCode =records[0][7]
                TradeContext.handOrgName =records[0][8]
                TradeContext.workDate = records[0][14]
                TradeContext.note2      =records[0][16]
                
                TipsFunc.GetTaxOrg(TradeContext.taxOrgCode)
        elif TradeContext.opType=='1':
            AfaLoggerFunc.tradeInfo('>>>删除')
            #=============判断状态====================
            sql="SELECT STATUS,TAXPAYCODE,PROTOCOLNO,PAYACCT,IDTYPE,IDCODE,TAXPAYNAME,"
            sql=sql+"TAXORGCODE,HANDORGNAME,STARTDATE,ENDDATE,ZONENO,BRNO,TELLERNO,WORKDATE,"
            sql=sql+"NOTE1,NOTE2,NOTE3,NOTE4,NOTE5"
            sql=sql+" FROM TIPS_CUSTINFO WHERE TAXORGCODE  ='"+TradeContext.taxOrgCode +"'"
            
            if( len(TradeContext.taxPayCode) != 0 ):
            	AfaLoggerFunc.tradeInfo('>>>' + TradeContext.taxPayCode)
            	sql=sql+" AND TAXPAYCODE ='"+TradeContext.taxPayCode +"'"
            if( len(TradeContext.accno) != 0 ):
            	sql=sql+" and PAYACCT     ='"+TradeContext.accno  +"'"
            if( len(TradeContext.protocolNo) != 0 ):
            	sql=sql+" and PROTOCOLNO     ='"+TradeContext.protocolNo  +"'"

            AfaLoggerFunc.tradeInfo(sql)
            records = AfaDBFunc.SelectSql(sql)
            if( records == None or  records <0):
                AfaLoggerFunc.tradeFatal(sql)
                return TipsFunc.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
            elif( len( records )==0 ):
                #return TipsFunc.ExitThisFlow( 'A0027', '该客户三方协议尚未签约，无法撤消' )
                return TipsFunc.ExitThisFlow( 'A0027', '该客户三方协议尚未签约，无法删除' )
            elif( len( records )>1 ):
                return TipsFunc.ExitThisFlow( 'A0027', '存在多条验证记录' )
            else:
                AfaLoggerFunc.tradeFatal(sql)
                AfaLoggerFunc.tradeInfo(records[0][0])
                UtilTools.ListFilterNone( records )
                #if (records[0][0]=='0' or records[0][0]=='3'):
                #    return TipsFunc.ExitThisFlow( 'A0027', '三方协议状态为已撤消，不能重复撤消' )
                if (records[0][0]=='1'):
                    #return TipsFunc.ExitThisFlow( 'A0027', '三方协议状态为已验证，不能撤消' )
                    return TipsFunc.ExitThisFlow( 'A0027', '三方协议状态为已验证，不能删除，请做解约交易' )
            TradeContext.taxPayCode =records[0][1]
            TradeContext.protocolNo =records[0][2]
            TradeContext.accno      =records[0][3]
            TradeContext.idType     =records[0][4]
            TradeContext.idCode     =records[0][5]
            TradeContext.taxPayName =records[0][6]
            TradeContext.taxOrgCode =records[0][7]
            TradeContext.handOrgName =records[0][8]
            TradeContext.workDate = records[0][14]
            TradeContext.note2      =records[0][16]
            TipsFunc.GetTaxOrg(TradeContext.taxOrgCode)
            TradeContext.status = '删除成功'

            #sql="update TIPS_CUSTINFO set "
            #sql=sql+" STATUS     ='"+'3'                     +"'"
            #sql=sql+",ENDDATE      ='"+TradeContext.workDate   +"'"
            #sql=sql+",ZONENO     ='"+TradeContext.zoneno     +"'"
            #sql=sql+",BRNO       ='"+TradeContext.brno       +"'"
            #sql=sql+",TELLERNO   ='"+TradeContext.teller   +"'"
            #sql=sql+" WHERE TAXPAYCODE ='"  +TradeContext.taxPayCode   +"'"
            #sql=sql+" AND PAYACCT ='"       +TradeContext.accno        +"'"
            #sql=sql+" AND PROTOCOLNO  ='"   +TradeContext.protocolNo   +"'"
            #sql=sql+" AND TAXORGCODE  ='"   +TradeContext.taxOrgCode   +"'"
            #AfaLoggerFunc.tradeInfo(sql)
            #if( AfaDBFunc.UpdateSqlCmt(sql) == -1 ):
            #    AfaLoggerFunc.tradeFatal(sql)
            #    return TipsFunc.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
            sql="delete "
            sql="DELETE FROM TIPS_CUSTINFO WHERE TAXORGCODE  ='"+TradeContext.taxOrgCode +"'"
            
            if( len(TradeContext.taxPayCode) != 0 ):
            	AfaLoggerFunc.tradeInfo('>>>' + TradeContext.taxPayCode)
            	sql=sql+" AND TAXPAYCODE ='"+TradeContext.taxPayCode +"'"
            if( len(TradeContext.accno) != 0 ):
            	sql=sql+" and PAYACCT     ='"+TradeContext.accno  +"'"
            if( len(TradeContext.protocolNo) != 0 ):
            	sql=sql+" and PROTOCOLNO     ='"+TradeContext.protocolNo  +"'"

            AfaLoggerFunc.tradeInfo(sql)
            rec=AfaDBFunc.DeleteSqlCmt(sql)
            if rec<0:
                return TipsFunc.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
            
        else:
            return TipsFunc.ExitThisFlow('0001', '未定义该操作类型')
            
        #=============自动打包==================== 
        TradeContext.errorCode='0000'
        TradeContext.errorMsg='交易成功'
        #=============程序退出====================
        AfaLoggerFunc.tradeInfo( '退出客户信息维护模板['+TradeContext.TemplateCode+']\n' )
        return True
    except TipsFunc.flowException, e:
        TipsFunc.exitMainFlow( )
    except TipsFunc.accException:
        TipsFunc.exitMainFlow( )
    except Exception, e:
        TipsFunc.exitMainFlow(str(e))  
def SubModuleMainSnd():
    return True   