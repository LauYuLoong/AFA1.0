# -*- coding: gbk -*-
################################################################################
#   批量业务.通用模板
#===============================================================================
#   模板文件:   AHXNB001.py
#   修改时间:   2010-12-15
################################################################################
import TradeContext

TradeContext.sysType = "ahxnb"

import AfaLoggerFunc,AfaUtilTools,AfaFlowControl,AfaFunc,os

from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('********安徽省新农保.批量模板['+TradeContext.TemplateCode+']进入********')

    try:
    
        #=====================初始化返回报文变量================================
        TradeContext.tradeResponse=[]

       
        #=====================获取系统日期时间==================================
        TradeContext.WorkDate=AfaUtilTools.GetSysDate( )
        TradeContext.WorkTime=AfaUtilTools.GetSysTime( )
        
        #=====================判断应用系统状态==================================
        if not AfaFunc.ChkSysStatus( ) :
            raise AfaFlowControl.flowException( )


        #=====================动态加载交易脚本==================================
        trxModuleName = 'T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode
        try:
            trxModuleHandle=__import__( trxModuleName )

        except Exception, e:
            AfaLoggerFunc.tradeInfo(e)
            raise AfaFlowControl.flowException( 'A0001', '加载交易脚本失败或交易脚本不存在' )


        #=====================安徽新农保业务个性化操作==========================
        if not trxModuleHandle.TrxMain( ) :
            raise AfaFlowControl.flowException( TradeContext.errorCode,TradeContext.errorMsg)


        #=====================自动打包==========================================
        AfaFunc.autoPackData()


        #=====================退出模板==========================================
        AfaLoggerFunc.tradeInfo('********安徽省新农保.批量模板['+TradeContext.TemplateCode+']退出********')


    except AfaFlowControl.flowException, e:
        #流程异常
        AfaFlowControl.exitMainFlow( str(e) )

    except AfaFlowControl.accException:
        #账务异常
        AfaFunc.autoPackData()

    except Exception, e:
        #默认异常
        AfaFlowControl.exitMainFlow( str( e ) )
        
if __name__ == '__main__':
    TradeContext.TemplateCode = "AHXNB001"
    TradeContext.TransCode = "8492"
    TradeContext.I1SBNO    ="3401010077"
    TradeContext.sysId     ="AG2015"
    TradeContext.I1USID    ="007905"
    TradeContext.I1AUUS    =""
    TradeContext.I1AUPS    =""
    TradeContext.I1WSNO    =""
    TradeContext.I1APPNO   ="AG1014"
    TradeContext.I1BUSINO  ="34010100770001"
    #TradeContext.I1FTPTYPE ="2"
    #TradeContext.I1FILENAME="yhdkfs_nchz_340122_2.txt"
    TradeContext.I1FTPTYPE ="1"
    TradeContext.I1FILENAME = "daifa.txt"
    TradeContext.I1TOTALNUM="10"
    TradeContext.I1TOTALAMT="120.00"
    TradeContext.I1STARTDATE="20101217"
    TradeContext.I1ENDDATE  ="20101217"
    
    fileCount = os.popen("sed -n '$=' /home/maps/afa/data/ahxnb/yhkhfs_nchz_340122_1.txt").read().strip()
    print fileCount
    
    
    
    main( )

