# -*- coding: gbk -*-
##################################################################
#   农信银系统：往账.本地类操作(1.本地操作).头寸预警登记簿查询 
#=================================================================
#   程序文件:   TRCC001_8539.py
#   修改时间:   2008-06-07
#   作    者：  潘广通
##################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,rccpsDBTrcc_cshalm,rccpsDBFunc,rccpsState,os
from types import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作)交易[TRC001_8539]进入***' )

    #=====判断输入接口值是否存在====
    if( not TradeContext.existVariable( "STRDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '起始日期[STRDAT]不存在')
    if( not TradeContext.existVariable( "ENDDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '结束日期[ENDDAT]不存在')
    if( not TradeContext.existVariable( "RECSTRNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '起始笔数[RECSTRNO]不存在')
        
    #=====组织sql语句====
    wheresql = ""
    wheresql = wheresql+"BJEDTE>='"+TradeContext.STRDAT+"'"
    wheresql = wheresql+" AND BJEDTE<='"+TradeContext.ENDDAT+"'"
    
    start_no=TradeContext.RECSTRNO      #起始笔数
    sel_size=10                         #查询笔数
    
    #=====查询总记录笔数====
    allcount=rccpsDBTrcc_cshalm.count(wheresql)
    
    if(allcount == -1):
        return AfaFlowControl.ExitThisFlow('S999', '查询总记录数异常')
    
    #=====查询数据库====
    ordersql = " order by BJEDTE DESC"   
    records=rccpsDBTrcc_cshalm.selectm(start_no,sel_size,wheresql,ordersql)
    
    if(records == None):
        return AfaFlowControl.ExitThisFlow('S999', '查询头寸预警登记簿异常')
    if(len(records) <= 0):
    	  return AfaFlowControl.ExitThisFlow('S999', '头寸预警登记簿中无对应信息')
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

        filecontext=""
        #=====写文件操作====
        for i in range(0,len(records)):
            #=====生成文件内容====
            filecontext=records[i]['BJEDTE']+"|"+records[i]['BSPSQN']+"|"\
                       +records[i]['NCCWKDAT']+"|"+records[i]['TRCDAT']+"|"\
                       +records[i]['TRCNO']+"|"+records[i]['CUR']+"|"\
                       +str(records[i]['POSITION'])+"|"+str(records[i]['POSALAMT'])+"|"
            AfaLoggerFunc.tradeInfo( filecontext)            
            f.write(filecontext+"\n")
        f.close()
        
        #=====输出接口赋值====
        TradeContext.PBDAFILE=filename              #文件名
        TradeContext.RECCOUNT=str(len(records))     #查询笔数
        TradeContext.RECALLCOUNT=str(allcount)  #总笔数
        TradeContext.errorCode="0000"
        TradeContext.errorMsg="查询成功"
           
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作)交易[TRC001_8539]退出***' )
    return True
