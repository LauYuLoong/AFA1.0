# -*- coding: gbk -*-
##################################################################
#   财税库行.三方协议校验.第三方发起
#=================================================================
#   程序文件:   TTPS001_845014.py
#   修改时间:   2008-12-05
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools, AfaDBFunc
import TipsFunc,HostContext,os
from types import *

def SubModuleMainFst( ):

    AfaLoggerFunc.tradeInfo( '进入三方协议验证/撤销(人行发起)[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
        #============校验公共节点的有效性==================
        # 完整性检查
        if( not TradeContext.existVariable( "VCSign" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '标识[VCSign]值不存在!' )
        if( not TradeContext.existVariable( "payAcct" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '帐号[payAcct]值不存在!' )
        if( not TradeContext.existVariable( "taxPayCode" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '用户号[taxPayCode]值不存在!' )
        if( not TradeContext.existVariable( "taxPayName" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '用户名[taxPayName]值不存在!' )
        if( not TradeContext.existVariable( "taxOrgCode" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '征收机关[taxOrgCode]值不存在!' )
        if( not TradeContext.existVariable( "protocolNo" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '协议号[protocolNo]值不存在!' )
        if( not TradeContext.existVariable( "PayOpBkCode" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '付款开户行行号[PayOpBkCode]值不存在!' )
        if( not TradeContext.existVariable( "PayBkCode" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '清算行行号[PayBkCode]值不存在!' )
        
        #验证撤销结果    0	验证通过，协议已可以使用
        #                1	验证失败，协议不存在或信息有误
        #                2	撤销通过，协议已不能使用
        #                3	撤销失败，协议不存在或信息有误
        if TradeContext.VCSign=='0':
            TradeContext.VCResult='1'
            TradeContext.AddWord='验证失败，协议不存在或信息有误'
        else:
            TradeContext.VCResult='3'
            TradeContext.AddWord='撤销失败，协议不存在或信息有误'
                   
        #=============获取平台流水号==================== 
        if TipsFunc.GetSerialno( ) == -1 :
            return False
        
        if TradeContext.VCSign=='0':
            #=============判断状态====================
            sql = "SELECT STATUS FROM TIPS_CUSTINFO WHERE "
            sql = sql +" TAXPAYCODE='"      +TradeContext.taxPayCode+"'"
            sql = sql +"AND PAYACCT='"      +TradeContext.payAcct+"'"
            sql = sql +"AND TAXORGCODE='"   +TradeContext.taxOrgCode+"'"
            sql = sql +"AND PROTOCOLNO='"   +TradeContext.protocolNo+"'"
            sql = sql +"AND PAYOPBKCODE='"   +TradeContext.PayOpBkCode+"'"
            sql = sql +"AND NOTE2='"   +TradeContext.PayBkCode+"'"
            AfaLoggerFunc.tradeInfo(sql)
            records = AfaDBFunc.SelectSql(sql)
            if( records == None or records < 0 ):
                AfaLoggerFunc.tradeFatal(sql)
                return TipsFunc.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
            elif( len( records ) == 0 ):
                AfaLoggerFunc.tradeInfo( "该客户尚未签约")
                TradeContext.errorCode='9999'
                TradeContext.errorMsg='验证失败，协议不存在'
                TradeContext.VCResult='1'
                TradeContext.AddWord='验证失败，协议不存在'
                return True
            else:
                AfaLoggerFunc.tradeFatal(sql)
                AfaLoggerFunc.tradeInfo(records[0][0])
                UtilTools.ListFilterNone( records )
                #0-注销 1-正常（双方都已验证） 2-临时状态（银行方柜面已验证）3-临时状态（银行方柜面已撤销）
                if (records[0][0] =="0" or records[0][0]=="3" ): #已有该客户记录，状态为未签约，无法验证
                    AfaLoggerFunc.tradeInfo( "已有该客户记录，状态为未签约，无法验证")
                    TradeContext.errorCode='9999'
                    TradeContext.errorMsg='验证失败，协议不存在'
                    TradeContext.VCResult='1'
                    TradeContext.AddWord='验证失败，协议不存在'
                    return True
            sql = "update TIPS_CUSTINFO set  STATUS     ='1'"
            sql = sql+" WHERE TAXPAYCODE='" +TradeContext.taxPayCode+"'"
            sql = sql +"AND PAYACCT='"      +TradeContext.payAcct   +"'"
            sql = sql +"AND TAXORGCODE='"   +TradeContext.taxOrgCode+"'"
            sql = sql +"AND PROTOCOLNO='"   +TradeContext.protocolNo+"'"
            AfaLoggerFunc.tradeInfo(sql)
            if( AfaDBFunc.UpdateSqlCmt(sql) == -1 ):
                AfaLoggerFunc.tradeFatal(sql)
                return TipsFunc.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
            TradeContext.errorCode='0000'
            TradeContext.errorMsg='验证通过，协议已可以使用'
            TradeContext.VCResult='0'
            TradeContext.AddWord='验证通过，协议已可以使用'
            

        elif TradeContext.VCSign=='1':
            #=============判断状态====================
            sql = "SELECT STATUS FROM TIPS_CUSTINFO WHERE "
            sql = sql +" TAXPAYCODE='"      +TradeContext.taxPayCode+"'"
            sql = sql +"AND PAYACCT='"      +TradeContext.payAcct+"'"
            sql = sql +"AND TAXORGCODE='"   +TradeContext.taxOrgCode+"'"
            sql = sql +"AND PROTOCOLNO='"   +TradeContext.protocolNo+"'"
            sql = sql +"AND PAYOPBKCODE='"   +TradeContext.PayOpBkCode+"'"
            sql = sql +"AND NOTE2='"   +TradeContext.PayBkCode+"'"
            AfaLoggerFunc.tradeInfo(sql)
            records = AfaDBFunc.SelectSql(sql)
            if( records == None or records < 0 ):
                AfaLoggerFunc.tradeFatal(sql)
                return TipsFunc.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
            elif( len( records ) == 0 ):
                AfaLoggerFunc.tradeInfo( "该客户尚未签约")
                TradeContext.errorCode='9999'
                TradeContext.errorMsg='撤销失败，协议不存在或信息有误'
                TradeContext.VCResult='3'
                TradeContext.AddWord='撤销失败，协议不存在或信息有误'
                return True
            sql="update TIPS_CUSTINFO set "
            sql=sql+" STATUS     ='0'"
            sql = sql+" WHERE TAXPAYCODE='" +TradeContext.taxPayCode+"'"
            sql = sql +"AND PAYACCT='"      +TradeContext.payAcct   +"'"
            sql = sql +"AND TAXORGCODE='"   +TradeContext.taxOrgCode+"'"
            sql = sql +"AND PROTOCOLNO='"   +TradeContext.protocolNo+"'"
            AfaLoggerFunc.tradeInfo(sql)
            if( AfaDBFunc.UpdateSqlCmt(sql) == -1 ):
                AfaLoggerFunc.tradeFatal(sql)
                return TipsFunc.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
            TradeContext.errorCode='0000'
            TradeContext.errorMsg='撤销通过，协议已不能使用'
            TradeContext.VCResult='2'
            TradeContext.AddWord='撤销通过，协议已不能使用'
            
            
                       
               
            #TradeContext.revTranF       ='0' #正交易
            #TradeContext.tradeType      ='U' #签约类交易
            #TradeContext.amount         ='0' #
            #TradeContext.__agentAccno__ =''  #借方帐号置空
            #TradeContext.note1          =TradeContext.upBranchno       
            ##记录签约流水
            #if not TransDtlFunc.InsertDtl( ) :
            #    return False
            #TradeContext.__status__='0'
            #TradeContext.errorCode='0000'
            #TradeContext.errorMsg='交易成功'
            #if( not TransDtlFunc.UpdateDtl( 'TRADE' ) ):
            #    return False
            
        AfaLoggerFunc.tradeInfo(TradeContext.errorCode)
        AfaLoggerFunc.tradeInfo(TradeContext.errorMsg)
        AfaLoggerFunc.tradeInfo(TradeContext.VCResult)
        AfaLoggerFunc.tradeInfo(TradeContext.AddWord)
        #=============程序退出====================
        AfaLoggerFunc.tradeInfo( '退出三方协议验证(撤销)[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        TradeContext.tradeResponse=[]
        return True
    except TipsFunc.flowException, e:
        TipsFunc.exitMainFlow( )
    except TipsFunc.accException:
        TipsFunc.exitMainFlow( )
    except Exception, e:
        TipsFunc.exitMainFlow(str(e))  
def SubModuleMainSnd():
    return True   
    
