# -*- coding: gbk -*-
##################################################################
#   农信银.往账.本地类操作(1.本地操作).公共数据文件通知查询
#=================================================================
#   程序文件:   TRCC001_8550.py
#   修改时间:   2008-06-07
##################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,rccpsDBTrcc_pbdata,rccpsDBFunc,AfaUtilTools,os,rccpsFtpFunc
from types import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作)交易[TRC001_8550]进入***' )

    #=====判断输入接口值是否存在====
    if( not TradeContext.existVariable( "STRDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '起始日期[STRDAT]不存在')
    if( not TradeContext.existVariable( "ENDDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '结束日期[ENDDAT]不存在')
    if( not TradeContext.existVariable( "PBDATYP" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '数据类型[PBDATYP]不存在')
    if( not TradeContext.existVariable( "RECSTRNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '起始笔数[RECSTRNO]不存在')
        
    #=====组织sql语句====
    wheresql=""
    wheresql=wheresql+"NCCWKDAT>='"+TradeContext.STRDAT+"'"
    wheresql=wheresql+" AND NCCWKDAT<='"+TradeContext.ENDDAT+"'"
    wheresql=wheresql+" AND PbDaTyp='"+TradeContext.PBDATYP+"'"
    
    start_no=TradeContext.RECSTRNO      #起始笔数
    sel_size=10                         #查询笔数
    
    #=====查询总记录数====
    allcount=rccpsDBTrcc_pbdata.count(wheresql)
    if(allcount == -1):
        return AfaFlowControl.ExitThisFlow('S999', '查询总记录数异常')
    
    #=====查询数据====
    records=rccpsDBTrcc_pbdata.selectm(start_no,sel_size,wheresql,"")
    if(records == None):
        return AfaFlowControl.ExitThisFlow('S999', '查询公共数据登记簿异常')
    if(len(records) <= 0):
        return AfaFlowControl.ExitThisFlow('S999', '公共数据登记簿中无对应信息')
    else:
        AfaLoggerFunc.tradeInfo( "生成文件")
        #=====生成文件====
        filename="rccps_"+TradeContext.BESBNO+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            pub_path = os.environ["AFAP_HOME"]
            pub_path = pub_path + "/tmp/"
            f=open(pub_path+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('A099','打开文件失败')
            
        filecontext=""
        #=====写文件操作====
        for i in range(0,len(records)):
            #=====生成文件内容====
            pub_list=str(records[i]['PBDAFILE']).split('/')
            AfaLoggerFunc.tradeInfo( pub_list)
            mfilename=""
            mfilename=pub_list[len(pub_list)-1]

            filecontext = records[i]['EFCTDAT'] + "|" + records[i]['PBDATYP'] + "|" + os.environ["AFAP_HOME"] + "/data/rccps/filein/" + mfilename + "|"

            f.write(filecontext+"\n")
        f.close()
        #=====输出接口赋值====
        AfaLoggerFunc.tradeInfo( ">>>赋输出接口值")
        TradeContext.PBDAFILE=filename                  #文件名
        TradeContext.RECCOUNT=str(len(records))         #查询笔数
        TradeContext.RECALLCOUNT=str(len(records))      #总笔数
        TradeContext.errorCode="0000"
        TradeContext.errorMsg="查询成功"

    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作)交易[TRC001_8550]退出***' )
    return True
