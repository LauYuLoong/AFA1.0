# -*- coding: gbk -*-
##################################################################
#   财税库行横向联网.缴费交易模板（只上主机，主机未知会自动冲正）.
#=================================================================
#   程序文件:   TPS002.py
#   修改时间:   2008-5-2 10:24
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools, TipsFunc
#import Party3Context,AfaAfeFunc,AfaHostFunc
from types import *

def main( ):
    AfaLoggerFunc.tradeInfo('======进入缴费交易模板['+TradeContext.TemplateCode+']=======')
    flag = 0
    try:
        #=============初始化返回报文变量====================
        TradeContext.tradeResponse=[]

        #=============获取当前系统时间====================
        if not (TradeContext.existVariable( "workDate" ) and len(TradeContext.workDate)>0):
            TradeContext.workDate = UtilTools.GetSysDate( )
        TradeContext.workTime = UtilTools.GetSysTime( )
        TradeContext.appNo      ='TIPS'
        TradeContext.busiNo     ='00000000000001'
        
        #=============外调接口1====================
        subModuleExistFlag=0
        subModuleName = 'T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode
        try:
            subModuleHandle=__import__( subModuleName )
        except Exception, e:
            AfaLoggerFunc.tradeInfo( e)
        else:
            AfaLoggerFunc.tradeInfo( '执行['+subModuleName+']模块' )
            subModuleExistFlag=1
            if not subModuleHandle.SubModuleDoFst( ) :
                raise TipsFunc.flowException( )

        #=============获取平台流水号====================
        if TipsFunc.GetSerialno( ) == -1 :
            raise TipsFunc.flowException( )

        #============校验公共节点的有效性==================
        if( not TipsFunc.Pay_ChkVariableExist( ) ):
            raise TipsFunc.flowException( )

        #=============判断应用状态====================
        if not TipsFunc.ChkAppStatus( ) :
            raise TipsFunc.flowException( )


        #=============插入流水表====================
        if not TipsFunc.InsertDtl( ) :
            raise TipsFunc.flowException( )

        #=============与主机通讯====================
        TipsFunc.CommHost()

        #=============更新主机返回状态====================
        if( not TipsFunc.UpdateDtl( 'TRADE' ) ):
            if( TradeContext.__status__=='2' ):
                raise TipsFunc.accException( )
            raise TipsFunc.flowException( )

        #=============自动打包====================
        TipsFunc.autoPackData()

        #print TradeContext.tradeResponse

        AfaLoggerFunc.tradeInfo('=====退出缴费交易模板['+TradeContext.TemplateCode+']=====')

        #=============程序退出====================

    except TipsFunc.flowException, e:
        # print e
        TipsFunc.exitMainFlow( )

    except TipsFunc.accException,e:
        # print e

        if TradeContext.existVariable("errorMsg"):
            ErrorMessage = TradeContext.errorMsg
        else:
            ErrorMessage = ""

        AfaLoggerFunc.tradeInfo('处理结果:' + ErrorMessage)
        AfaLoggerFunc.tradeInfo('自动冲正')

        if TradeContext.__status__ == '2':
            AfaLoggerFunc.tradeInfo('主机异常情况-->冲正')
            TradeContext.__autoRevTranCtl__= '1'

        else:
            #主机失败
            TradeContext.__autoRevTranCtl__= '0'

        #=============自动冲正====================
        if TradeContext.__autoRevTranCtl__=='1' :

            #自动冲正数据初始化
            TradeContext.revTranF      = '2'
            TradeContext.preAgentSerno = TradeContext.agentSerialno
            TradeContext.revTrxDate    = TradeContext.workDate

            if TipsFunc.GetSerialno( ) == -1 :
                raise TipsFunc.exitMainFlow( )

             #=============插入流水表====================
            if not TipsFunc.InsertDtl( ) :
                raise TipsFunc.exitMainFlow( )

            #=============与主机通讯====================
            TipsFunc.CommHost()

            #=============更新主机返回状态====================
            if( not TipsFunc.UpdateDtl( 'TRADE' ) ):
                raise TipsFunc.exitMainFlow( )

            TradeContext.errorCode = 'A0048'

            if TradeContext.__status__ == '0':
                TradeContext.errorMsg = '交易失败:' + ErrorMessage + '(系统自动冲正成功)'
            else:
                TradeContext.errorMsg = '交易失败:' + ErrorMessage + '(系统自动冲正失败)'

            TipsFunc.exitMainFlow()

        else:
            TipsFunc.exitMainFlow( )

        TipsFunc.exitMainFlow( )

    except Exception, e:
        # print e
        TipsFunc.exitMainFlow( str(e))
