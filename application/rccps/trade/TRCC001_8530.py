# -*- coding: gbk -*-
##################################################################
#   农信银.查询打印业务.支付业务状态登记簿查询
#=================================================================
#   程序文件:   TRCC001_8530.py
#   修改时间:   2008-06-09
#   作    者：  刘雨龙
##################################################################
import rccpsDBTrcc_ztcbka,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,os
from types import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统: 往账.本地类操作交易[RCC001_8530]进入***' )

    #=====判断输入接口值是否存在====
    if( not TradeContext.existVariable( "STRDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '起始日期[STRDAT]不存在')
    
    if( not TradeContext.existVariable( "ENDDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '终止日期[ENDDAT]不存在')
    
    if( not TradeContext.existVariable( "BRSFLG" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '往来标志[BRSFLG]不存在')
    
    if( not TradeContext.existVariable( "RECSTRNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '起始笔数[RECSTRNO]不存在')
        
    start_no = TradeContext.RECSTRNO        #起始笔数
    sel_size = 10                           #查询笔数
        
    #=====生成查询语句====
    wheresql = ""
    wheresql = wheresql + "BESBNO='" + TradeContext.BESBNO + "' " 
    wheresql = wheresql + " AND BJEDTE>='" + TradeContext.STRDAT + "'"
    wheresql = wheresql + " AND BJEDTE<='" + TradeContext.ENDDAT + "'"

    #=====判断往来标志是否为空====
    if(TradeContext.BRSFLG != ""):
        wheresql = wheresql +" AND BRSFLG='" + TradeContext.BRSFLG + "'"

    #=====判断报单序号是否为空====
    if(TradeContext.BSPSQN != ""):
        wheresql = wheresql + " AND BSPSQN='" + TradeContext.BSPSQN + "'"
    
    #=====判断原交易日期是否为空====    
    if(TradeContext.BOJEDT != "00000000"):
        wheresql = wheresql + " AND BOJEDT='" + TradeContext.BOJEDT + "'"
    
    #=====判断原表单序号是否为空====    
    if(TradeContext.BOSPSQ != ""):
        wheresql = wheresql + " AND BOSPSQ='" + TradeContext.BOSPSQ + "'"
    
    #=====判断复查标志是否为空====    
    if(TradeContext.ISDEAL != ""):
        wheresql = wheresql + " AND ISDEAL='" + TradeContext.ISDEAL + "'"
        
    AfaLoggerFunc.tradeInfo( "查询条件: "+wheresql)
    
    #=====查询总记录数====
    allcount = rccpsDBTrcc_ztcbka.count(wheresql)
    if(allcount < 0):
        return AfaFlowControl.ExitThisFlow('A099', '查询总记录数失败')
        
    AfaLoggerFunc.tradeDebug("查询总记录数完成")
    
    #=====查询数据库====
    ordersql = " order by BJEDTE DESC,BSPSQN DESC"
    
    records = rccpsDBTrcc_ztcbka.selectm(start_no,sel_size,wheresql,ordersql)
    
    if(records == None):
        return AfaFlowControl.ExitThisFlow('A099','查询失败' )    
    if len(records) <= 0:
        return AfaFlowControl.ExitThisFlow('A099','未查找到数据' )
    else:
        #=====生成文件====
        filename = "rccps_" + TradeContext.BETELR+"_" + AfaUtilTools.GetHostDate() + "_" + TradeContext.TransCode
        fpath = os.environ["AFAP_HOME"] + "/tmp/"
        
        f = open(fpath + filename,"w")
        
        if f == None:
            return AfaLoggerFunc.tradeInfo("S999","打开文件异常")
        filecontext = ""
        
        #=====写文件操作====
        for i in range(0,len(records)):
            filecontext = records[i]['BJEDTE']      + "|" \
                        + records[i]['BSPSQN']      + "|" \
                        + records[i]['BRSFLG']      + "|" \
                        + records[i]['TRCDAT']      + "|" \
                        + records[i]['TRCNO']       + "|" \
                        + records[i]['SNDBNKCO']    + "|" \
                        + records[i]['SNDBNKNM']    + "|" \
                        + records[i]['RCVBNKCO']    + "|" \
                        + records[i]['RCVBNKNM']    + "|" \
                        + records[i]['BOJEDT']      + "|" \
                        + records[i]['BOSPSQ']      + "|" \
                        + records[i]['ORTRCCO']     + "|" \
                        + records[i]['CUR']         + "|" \
                        + str(records[i]['OCCAMT']) + "|" \
                        + records[i]['CONT']        + "|" \
                        + records[i]['NCCTRCST']    + "|" \
                        + records[i]['MBRTRCST']    + "|" \
                        + records[i]['PRCCO']       + "|" \
                        + records[i]['STRINFO']     + "|"
                        
            f.write(filecontext+"\n")
        
        f.close()        
        AfaLoggerFunc.tradeInfo("生成文件结束")
        
    #=====输出接口赋值====
    TradeContext.RECSTRNO=start_no              #起始笔数
    TradeContext.RECCOUNT=str(len(records))     #查询笔数
    TradeContext.RECALLCOUNT=str(allcount)      #总笔数
    TradeContext.errorCode="0000"
    TradeContext.errorMsg="查询成功"
    TradeContext.PBDAFILE=filename              #文件名
    
    AfaLoggerFunc.tradeInfo( '***农信银系统: 往账.本地类操作交易[RCC001_8530]退出***' )
    return True