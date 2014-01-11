# -*- coding: gbk -*-
##################################################################
#   代收代付平台.缴费交易模板（先上主机，再上第三方）.
#=================================================================
#   程序文件:   4202.py
#   修改时间:   2006-09-11
#   增加一个标志flag 用来判断是否第三方失败
#   如果第三方失败(合肥电信)视为成功处理
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, FSTransDtlFunc, AfaFlowControl, AfaFsFunc
import Party3Context, AfaAfeFunc, AfaHostFunc
from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('======进入缴费交易模板['+TradeContext.TemplateCode+']=======')
    
    flag = 0
    
    try:
        #=============初始化返回报文变量====================
        TradeContext.tradeResponse=[]


        #=============获取当前系统时间====================
        TradeContext.workDate = AfaUtilTools.GetSysDate( )
        TradeContext.workTime = AfaUtilTools.GetSysTime( )

        #begin 20100625 蔡永贵修改
        #TradeContext.sysId       = "AG2008"
        TradeContext.sysId       = TradeContext.appNo
        #end

        TradeContext.agentFlag   = "01"
        TradeContext.__respFlag__='0'

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


        #============校验公共节点的有效性==================
        if( not AfaFsFunc.Pay_ChkVariableExist( ) ):
            raise AfaFlowControl.flowException( )


        #=============查询摘要代码====================
        if not AfaFunc.GetSummaryInfo( ) :
            raise AfaFlowControl.flowException( )
            
        #=============判断系统状态====================
        if not AfaFsFunc.ChkAppStatus( ) :
            raise AfaFlowControl.flowException( )


        #=============转换====================
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

        #=============与主机通讯====================
        AfaHostFunc.CommHost()

        #=============更新主机返回状态====================
        if( not FSTransDtlFunc.UpdateDtl( 'BANK' ) ):
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
        if( not FSTransDtlFunc.UpdateDtl( 'CORP' ) ):
            raise AfaFlowControl.accException( )

        #=============外调接口3====================
        billData=[]
        if subModuleExistFlag==1 :
            billData=subModuleHandle.SubModuledoTrd( )
            if billData==None :
                raise AfaFlowControl.flowException( )

        #=============自动打包====================
        AfaFunc.autoPackData()

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

            if AfaFunc.GetSerialno( ) == -1 :
                raise AfaFlowControl.exitMainFlow( )

             #=============插入流水表====================
            if not FSTransDtlFunc.InsertDtl( ) :
                raise AfaFlowControl.exitMainFlow( )

            #=============与主机通讯====================
            AfaHostFunc.CommHost()

            #=============更新主机返回状态====================
            if( not FSTransDtlFunc.UpdateDtl( 'BANK' ) ):
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
        # print e
        AfaFlowControl.exitMainFlow( str(e))
