# -*- coding: gbk -*-
##################################################################
#   代收代付平台.缴费交易模板（只上主机，主机未知会自动冲正）. 为了非税退付正常交换借贷方帐号
#=================================================================
#   程序文件:   4102.py
#   修改时间:   2007-10-17
#   作    者：  ZZH
##################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,FSTransDtlFunc,AfaFlowControl,AfaFsFunc
import AfaAfeFunc, AfaHostFunc
from types import *

from types import *

def main( ):
    
    AfaLoggerFunc.tradeInfo('======进入缴费交易模板['+TradeContext.TemplateCode+']=======')

    #begin 20100625 蔡永贵修改
    #TradeContext.sysId       = "AG2008"
    TradeContext.sysId       = TradeContext.appNo
    #end

    TradeContext.agentFlag = "01"
    TradeContext.__respFlag__='0'

    flag = 0

    try:
        #=============初始化返回报文变量====================
        TradeContext.tradeResponse=[]

        #=============获取当前系统时间====================
        TradeContext.workDate = AfaUtilTools.GetSysDate( )
        TradeContext.workTime = AfaUtilTools.GetSysTime( )

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
        if AfaFunc.GetSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )

        AfaLoggerFunc.tradeInfo('======1=======')

        #============校验公共节点的有效性==================
        if( not AfaFsFunc.Pay_ChkVariableExist( ) ):
            raise AfaFlowControl.flowException( )

        AfaLoggerFunc.tradeInfo('======2=======')

        #=============判断应用状态====================
        if not AfaFsFunc.ChkAppStatus( ) :
            raise AfaFlowControl.flowException( )

        AfaLoggerFunc.tradeInfo('======3=======')

        if subModuleExistFlag==1 :
            subModuleHandle.SubModuleDoFstMore( ) 

        AfaLoggerFunc.tradeInfo('======4=======')

        #=============查询摘要代码====================
        if not AfaFunc.GetSummaryInfo( ) :
            raise AfaFlowControl.flowException( )

        TradeContext.channelCode = "005"
        TradeContext.userno    = TradeContext.userNo
        TradeContext.tellerno  = TradeContext.teller
        TradeContext.cashTelno = TradeContext.teller
        TradeContext.unitno    = "00000001"
        TradeContext.subUnitno = "00000000"
        if (TradeContext.catrFlag == '0'):    #现金
            TradeContext.accType = "000"
        else:
            TradeContext.accType = "001"

        #=============插入流水表====================
        if not FSTransDtlFunc.InsertDtl( ) :
            raise AfaFlowControl.flowException( )

        AfaLoggerFunc.tradeInfo('======5.5=======')


        #=============与主机通讯====================
        AfaHostFunc.CommHost()

        AfaLoggerFunc.tradeInfo('======6=======')

        #=============更新主机返回状态====================
        if( not FSTransDtlFunc.UpdateDtl( 'TRADE' ) ):
            if( TradeContext.__status__=='2' ):
                raise AfaFlowControl.accException( )
            raise AfaFlowControl.flowException( )

        AfaLoggerFunc.tradeInfo('======7=======')

        billData=[]
        if subModuleExistFlag==1 :
            billData=subModuleHandle.SubModuledoSnd( )
            if billData==None :
                raise AfaFlowControl.flowException( )

        AfaLoggerFunc.tradeInfo('======8=======')

        #=============自动打包====================
        AfaFunc.autoPackData()

        AfaLoggerFunc.tradeInfo('=====退出缴费交易模板['+TradeContext.TemplateCode+']=====')

        #=============程序退出====================

    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )

    except AfaFlowControl.accException,e:

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

            if AfaFunc.GetSerialno( ) == -1 :
                raise AfaFlowControl.exitMainFlow( )


            #=============插入流水表====================
            if not FSTransDtlFunc.InsertDtl( ) :
                raise AfaFlowControl.exitMainFlow( )

            #=============与主机通讯====================
            AfaHostFunc.CommHost( )


            #=============更新主机返回状态====================
            if( not FSTransDtlFunc.UpdateDtl( 'TRADE' ) ):
                raise AfaFlowControl.exitMainFlow( )


            TradeContext.errorCode = 'A0048'

            if TradeContext.__status__ == '0':
                TradeContext.errorMsg = '财政服务器异常:' + ErrorMessage + '(系统自动冲正成功)'
            else:
                TradeContext.errorMsg = '财政服务器异常:' + ErrorMessage + '(系统自动冲正失败)'

            AfaFlowControl.exitMainFlow()

        else:
            AfaFlowControl.exitMainFlow( )

        AfaFlowControl.exitMainFlow( )

    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
