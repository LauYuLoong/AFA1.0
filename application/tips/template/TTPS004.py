# -*- coding: gbk -*-
##################################################################
#   财税库行横向联网.缴费交易模板（先上主机，再上第三方）.
#=================================================================
#   程序文件:   TPS004.py
#   修改时间:   2008-5-2 10:24
#   增加一个标志flag 用来判断是否第三方失败
#   如果第三方失败视为成功处理
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools, AfaFlowControl, TipsFunc
import Party3Context,AfaAfeFunc,AfaHostFunc
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
                raise AfaFlowControl.flowException( )

        #=============获取平台流水号====================
        if TipsFunc.GetSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )

        #============校验公共节点的有效性==================
        if( not TipsFunc.Pay_ChkVariableExist( ) ):
            raise AfaFlowControl.flowException( )

        ##=============判断应用状态====================
        #if not TipsFunc.ChkAppStatus( ) :
        #    raise AfaFlowControl.flowException( )
        #
        #=============查询摘要代码====================
        #if not TipsFunc.GetSummaryCode( ) :
        #    raise AfaFlowControl.flowException( )
        #
        #=============插入流水表====================
        if not TipsFunc.InsertDtl( ) :
            raise AfaFlowControl.flowException( )

        #=============与主机通讯====================
        TipsFunc.CommHost()

        #=============更新主机返回状态====================
        if( not TipsFunc.UpdateDtl( 'BANK' ) ):
            if( TradeContext.__status__=='2' ):
                flag = 1
                raise AfaFlowControl.accException( )

            raise AfaFlowControl.flowException( )

        #=============外调接口2====================
        if subModuleExistFlag==1 :
            if not subModuleHandle.SubModuledoSnd( ) :
                raise AfaFlowControl.flowException( )

        AfaLoggerFunc.tradeInfo('与通讯前置通讯')
        #=============与通讯前置通讯====================
        AfaAfeFunc.CommAfe()

        #=============更新第三方返回状态====================
        if( not TransDtlFunc.UpdateDtl( 'CORP' ) ):
            raise AfaFlowControl.accException( )

        #=============外调接口3====================
        billData=[]
        if subModuleExistFlag==1 :
            billData=subModuleHandle.SubModuledoTrd( )
            if billData==None :
                raise AfaFlowControl.flowException( )

        #=============发票信息处理====================
        if not ( TransBillFunc.InsertBill( billData ) ) :
            raise AfaFlowControl.flowException( )

        #=============自动打包====================
        TipsFunc.autoPackData()

        #print TradeContext.tradeResponse

        AfaLoggerFunc.tradeInfo('=====退出缴费交易模板['+TradeContext.TemplateCode+']=====')

        #=============程序退出====================

    except AfaFlowControl.flowException, e:
        # print e
        AfaFlowControl.exitMainFlow( )

    except AfaFlowControl.accException,e:
        # print e

        if TradeContext.existVariable("errorMsg"):
            ErrorMessage = TradeContext.errorMsg
        else:
            ErrorMessage = ""

        AfaLoggerFunc.tradeInfo('处理结果:' + ErrorMessage)
        AfaLoggerFunc.tradeInfo('自动冲正')

        if flag==1 and TradeContext.__status__ == '2':
            AfaLoggerFunc.tradeInfo('主机异常情况-->冲正')
            TradeContext.__autoRevTranCtl__= '1'

        elif flag==0 and ( TradeContext.__status__ == '1' or TradeContext.__status__ == '2' ):
            AfaLoggerFunc.tradeInfo('第三方(失败或异常)情况-->冲正')
            TradeContext.__autoRevTranCtl__= '1'

        else:
            #主机失败、第三方异常
            TradeContext.__autoRevTranCtl__= '0'

        #=============自动冲正====================
        if TradeContext.__autoRevTranCtl__=='1' :

            #自动冲正数据初始化
            TradeContext.revTranF      = '2'
            TradeContext.preAgentSerno = TradeContext.agentSerialno
            TradeContext.revTrxDate    = TradeContext.workDate

            if TipsFunc.GetSerialno( ) == -1 :
                raise AfaFlowControl.exitMainFlow( )

             #=============插入流水表====================
            if not TransDtlFunc.InsertDtl( ) :
                raise AfaFlowControl.exitMainFlow( )

            #=============与主机通讯====================
            TipsFunc.CommHost()

            #=============更新主机返回状态====================
            if( not TipsFunc.UpdateDtl( 'BANK' ) ):
                raise AfaFlowControl.exitMainFlow( )

            TradeContext.errorCode = 'A0048'

            if TradeContext.__status__ == '0':
                TradeContext.errorMsg = '交易失败:' + ErrorMessage + '(系统自动冲正成功)'
            else:
                TradeContext.errorMsg = '交易失败:' + ErrorMessage + '(系统自动冲正失败)'

            AfaFlowControl.exitMainFlow()

        else:
            AfaFlowControl.exitMainFlow( )

        AfaFlowControl.exitMainFlow( )

    except Exception, e:
        # print e
        AfaFlowControl.exitMainFlow( str(e))
