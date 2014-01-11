# -*- coding: gbk -*-
################################################################################
#   代收代付.异常处理模板
#===============================================================================
#   模板文件:   003103.py
#   修改时间:   2006-04-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaDBFunc,AfaTransDtlFunc,AfaFlowControl,AfaHostFunc,AfaAfeFunc
from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('******代收代付.异常处理模板[' + TradeContext.TemplateCode + ']进入******')

    try:

        #=====================初始化返回报文变量================================
        TradeContext.tradeResponse=[]


        #=====================获取当前系统时间==================================
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )

        #=====================判断应用系统状态==================================
        if not AfaFunc.ChkSysStatus( ) :
            raise AfaFlowControl.flowException( )
                
        #=====================外调接口(前处理)==================================
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


        #=====================完整性检查========================================
        if( not TradeContext.existVariable( "sysId" ) ):
            raise AfaFlowControl.flowException( 'A0001', '系统标识[sysId]值不存在,不能进行异常处理' )

        if( not TradeContext.existVariable( "unitno" ) ):
            raise AfaFlowControl.flowException( 'A0001', '单位代码[unitno]值不存在,不能进行异常处理' )

        if( not TradeContext.existVariable( "subUnitno" ) ):
            raise AfaFlowControl.flowException( 'A0001', '子单位代码[unitno]值不存在,不能进行异常处理' )

        if( not TradeContext.existVariable( "agentFlag" ) ):
            raise AfaFlowControl.flowException( 'A0001', '业务方式[agentFlag]值不存在,不能进行异常处理' )

        if( not TradeContext.existVariable( "zoneno" ) ):
            raise AfaFlowControl.flowException( 'A0001', '地区号[zoneno]值不存在,不能进行异常处理' )

        if( not TradeContext.existVariable( "channelCode" ) ):
            raise AfaFlowControl.flowException( 'A0001', '渠道代码[channelCode]值不存在,不能进行异常处理' )

        if( not TradeContext.existVariable( "brno" ) ):
            raise AfaFlowControl.flowException( 'A0001', '网点号[brno]值不存在,不能进行异常处理' )

        if( not TradeContext.existVariable( "tellerno" ) ):
            raise AfaFlowControl.flowException( 'A0001', '柜员号[tellerno]值不存在,不能进行异常处理' )

        if( not TradeContext.existVariable( "amount" ) ):
            raise AfaFlowControl.flowException( 'A0001', '金额[amount]值不存在,不能进行异常处理' )

        if( not TradeContext.existVariable( "preAgentSerno" ) ):
            raise AfaFlowControl.flowException( 'A0001', '原交易流水号[preAgentSerno]值不存在,不能进行异常处理' )

        #冲正类型(0-冲主机 1-冲第三方 2-先第三方,再主机 3-先主机,再第三方)
        if( not TradeContext.existVariable( "revType" ) ):
            raise AfaFlowControl.flowException( 'A0001', '冲正类型[revType]值不存在,不能进行异常处理' )

        AfaLoggerFunc.tradeInfo( '>>>revType       = ' + TradeContext.revType )
        AfaLoggerFunc.tradeInfo( '>>>preAgentSerno = ' + TradeContext.preAgentSerno )

        #类同反交易
        TradeContext.revTranF='1'

        #=====================判断应用系统状态==================================
        if not AfaFunc.ChkSysStatus( ) :
            raise AfaFlowControl.flowException( )
        
        #=====================判断商户状态======================================
        if not AfaFunc.ChkUnitStatus( ) :
            raise AfaFlowControl.flowException( )
        
        #=====================判断渠道状态======================================
        if not AfaFunc.ChkChannelStatus( ) :
            raise AfaFlowControl.flowException( )

        #=====================获取未知交易的信息================================
        if( not GetAbnormalInfo( TradeContext.preAgentSerno ) ):
            raise AfaFlowControl.flowException( )

        #=====================获取平台流水号====================================
        if( not AfaFunc.GetSerialno( ) ):
            raise AfaFlowControl.flowException( )

        #=====================插入流水表========================================
        if( not AfaTransDtlFunc.InsertDtl( ) ):
            raise AfaFlowControl.flowException( )

        #=====================冲正类型(0-冲主机)================================
        if( TradeContext.revType == '0' ) :

            #与主机交换
            AfaHostFunc.CommHost()


            #更新交易流水
            if( not AfaTransDtlFunc.UpdateDtl( 'BANK' ) ):
                raise AfaFlowControl.flowException( )


            #外调接口(后处理)
            if subModuleExistFlag==1 :
                if not subModuleHandle.SubModuleDoSnd():
                    raise AfaFlowControl.flowException( )


        #=====================冲正类型(1-冲第三方)==============================
        if( TradeContext.revType == '1' ) :

            #与第三方交换
            AfaAfeFunc.CommAfe()
            
            
            #更新交易流水
            if( not AfaTransDtlFunc.UpdateDtl( 'CORP' ) ):
                raise AfaFlowControl.flowException( )

            #外调接口(后处理)
            if subModuleExistFlag==1 :
                if not subModuleHandle.SubModuleDoTrd():
                    raise AfaFlowControl.flowException( )


        #=====================冲正类型(2-先第三方,再主机)=======================
        if( TradeContext.revType == '2' ) :

            #与第三方交换
            AfaAfeFunc.CommAfe()
            
            
            #更新交易流水
            if( not AfaTransDtlFunc.UpdateDtl( 'CORP' ) ):
                raise AfaFlowControl.flowException( )

            #与主机交换
            AfaHostFunc.CommHost()

            
            #更新交易流水
            if( not AfaTransDtlFunc.UpdateDtl( 'BANK' ) ):
                raise AfaFlowControl.flowException( )
        
        
            #外调接口(后处理)
            if subModuleExistFlag==1 :
                if not subModuleHandle.SubModuleDoFth():
                    raise AfaFlowControl.flowException( )
                    
        #=====================冲正类型(3-先主机,再第三方)=======================
        if( TradeContext.revType == '3' ) :

            #与主机交换
            AfaHostFunc.CommHost()
            
            
            #更新交易流水
            if( not AfaTransDtlFunc.UpdateDtl( 'BANK' ) ):
                raise AfaFlowControl.flowException( )


            #与第三方交换
            AfaAfeFunc.CommAfe()
            
            
            #更新交易流水
            if( not AfaTransDtlFunc.UpdateDtl( 'CORP' ) ):
                raise AfaFlowControl.flowException( )
                
            #外调接口(后处理)
            if subModuleExistFlag==1 :
                if not subModuleHandle.SubModuleDoFfh():
                    raise AfaFlowControl.flowException( )

        #=====================自动打包==========================================
        AfaFunc.autoPackData()
        
        #=====================退出模板==========================================
        AfaLoggerFunc.tradeInfo('******代收代付.异常处理模板[' + TradeContext.TemplateCode + ']退出******')

    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )

    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )


def GetAbnormalInfo( serialno ):

    #获取异常交易信息
    names=['accType','__drAccno__','__crAccno__','userno','subUserno','userName','subAmount','vouhType','vouhno', \
    'vouhDate','bankSerno','currType','currFlag','note1','note2','note3','note4','note5', \
    'note6','note7','note8','note9','note10']


    #查询语句
    sql = "SELECT ACCTYPE,DRACCNO,CRACCNO,USERNO,SUBUSERNO,USERNAME,SUBAMOUNT,VOUHTYPE,VOUHNO,VOUHDATE,"
    sql = sql + "BANKSERNO,CURRTYPE,CURRFLAG,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5,NOTE6,NOTE7,"
    sql = sql + "NOTE8,NOTE9,NOTE10 FROM AFA_MAINTRANSDTL"
    
    sql = sql + " WHERE TELLERNO='"     + TradeContext.tellerno + "'"
    sql = sql + " AND ZONENO='"         + TradeContext.zoneno   + "'"
    sql = sql + " AND BRNO='"           + TradeContext.brno     + "'"
    sql = sql + " AND SYSID='"          + TradeContext.sysId    + "'"
    sql = sql + " AND AGENTSERIALNO='"  + serialno              + "'"
    sql = sql + " AND WORKDATE='"       + TradeContext.workDate + "'"
    sql = sql + " AND AMOUNT='"         + TradeContext.amount   + "'"
    sql = sql + " AND REVTRANF='0'"

    if (TradeContext.agentFlag=='01' or TradeContext.agentFlag=='03'):
        sql = sql + " AND (AGENTFLAG IN ('01','03') AND (BANKSTATUS='2' OR (BANKSTATUS='0' AND CORPSTATUS IN ('1','2','3'))))"
    else:
        sql = sql + " AND (AGENTFLAG IN ('02','04') AND (CORPSTATUS='2' OR (CORPSTATUS='0' AND BANKSTATUS IN ('1','2','3'))))"

    AfaLoggerFunc.tradeInfo( sql )

    result=None
    records=AfaDBFunc.SelectSql( sql )
    if( records == None ):
        TradeContext.errorCode, TradeContext.errorMsg='A0027', '流水主表操作异常'
        return False
        
    if( len( records ) == 0 ):
        TradeContext.errorCode, TradeContext.errorMsg='A0045', '未发现原始交易'        
        return False

    #过滤结果集中的None
    result=AfaUtilTools.ListFilterNone( records[0] )

    #给TradeContext中的变量赋值
    k=0
    for name in names:
        setattr( TradeContext, name, result[k] )
        k=k+1

    return True
