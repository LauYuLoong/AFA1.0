# -*- coding: gbk -*-
##################################################################
#   农信银.往账.本地类操作(1.本地操作).清算账户余额通知查询交易
#=================================================================
#   程序文件:   TRCC001_8540.py
#   修改时间:   2008-06-10
##################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,rccpsDBTrcc_rekbal,rccpsDBFunc,os
from types import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作)交易[TRC001_8540]进入***' )

    #=====判断输入接口值是否存在====
    if( not TradeContext.existVariable( "NCCWKDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '中心日期[NCCWKDAT]不存在')
    if( not TradeContext.existVariable( "RECSTRNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '起始笔数[RECSTRNO]不存在')
        
    #=====组织sql语句====
    wheresql=""
    wheresql=wheresql+"NCCWKDAT='"+TradeContext.NCCWKDAT+"'"
    
    start_no=TradeContext.RECSTRNO      #起始笔数
    sel_size=10                         #查询笔数
    
    #=====查询总记录数====
    allcount=rccpsDBTrcc_rekbal.count(wheresql)     #得到总记录笔数
    if(allcount == -1):
        return AfaFlowControl.ExitThisFlow('S999', '查询总记录数异常')
    
    #=====查询明细记录====
    ordersql=" order by BJEDTE DESC,BSPSQN DESC"
    records=rccpsDBTrcc_rekbal.selectm(start_no,sel_size,wheresql,ordersql)
    
    if(records == None):
        return AfaFlowControl.ExitThisFlow('S999', '查询清算余额通知登记簿异常')
    if(len(records) <= 0):
    	  return AfaFlowControl.ExitThisFlow('S999', '清算余额通知登记簿中无对应信息')
    else:
        #=====生成文件====
        AfaLoggerFunc.tradeInfo( "生成文件")
        filename="rccps_"+TradeContext.BESBNO+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            pub_path = os.environ["AFAP_HOME"]
            pub_path = pub_path + "/tmp/"
            f=open(pub_path + filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','打开文件失败')
        #=====写文件操作====
        for i in range(0,len(records)):
            #=====生成文件内容====
            filecontext=records[i]['BJEDTE']+"|"+records[i]['BSPSQN']+"|"\
                        +records[i]['TRCCO']+"|"+records[i]['NCCWKDAT']+"|"\
                        +records[i]['TRCDAT']+"|"+records[i]['TRCNO']+"|"\
                        +records[i]['CUR']+"|"+records[i]['LBDCFLG']+"|"\
                        +str(records[i]['LSTDTBAL'])+"|"+records[i]['NTTDCFLG']+"|"\
                        +str(records[i]['NTTBAL'])+"|"+records[i]['BALDCFLG']+"|"\
                        +str(records[i]['TODAYBAL'])+"|"+str(records[i]['AVLBAL'])+"|"\
                        +str(records[i]['NTODAYBAL'])+"|"+records[i]['CHKRST']+"|"
            f.write(filecontext+"\n")
        f.close()

        #=====输出接口赋值====
        TradeContext.PBDAFILE=filename              #文件名
        TradeContext.RECCOUNT=str(len(records))     #查询笔数
        TradeContext.RECALLCOUNT=str(allcount)      #总笔数
        TradeContext.errorCode="0000"
        TradeContext.errorMsg="查询成功"
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作)交易[TRC001_8540]退出***' )
    return True
