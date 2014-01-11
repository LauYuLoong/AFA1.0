# -*- coding: gbk -*-
##################################################################
#   农信银.查询打印业务.撤销申请及紧急止付申请查询
#=================================================================
#   程序文件:   TRCC001_8527.py
#   修改时间:   2008-06-07
#   作    者：  潘广通
##################################################################
import rccpsDBTrcc_trccan,rccpsDBTrcc_existp,rccpsDBTrcc_trcbka,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,rccpsDBFunc
from types import *
import os

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作交易[TRC001_8527]进入***' )
    
    #=====判断输入接口值是否存在====
    if( not TradeContext.existVariable( "STRDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '起始日期[STRDAT]不存在')
    
    if( not TradeContext.existVariable( "ENDDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '结束日期[ENDDAT]不存在')
    
    if( not TradeContext.existVariable( "RECSTRNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '起始笔数[RECSTRNO]不存在')
        
    start_no=TradeContext.RECSTRNO
    sel_size=10                             #查询笔数
        
    #=====组织查询的sql语句====
    AfaLoggerFunc.tradeInfo(">>>开始组织查询语句")
    wheresql=""
    wheresql=wheresql+"BJEDTE>='"+TradeContext.STRDAT+"'"
    wheresql=wheresql+" AND BJEDTE<='"+TradeContext.ENDDAT+"'"
    wheresql=wheresql+" AND BESBNO ='"+TradeContext.BESBNO+"'"
    
    #=====判断交易代码是否为空====
    if(TradeContext.TRCCO!=""):
        wheresql=wheresql+" AND TRCCO='"+TradeContext.TRCCO+"'"
    
    #=====判断报单序号是否为空====
    if(TradeContext.BSPSQN!=""):
        wheresql=wheresql+" AND BSPSQN='"+TradeContext.BSPSQN+"'"
    
    AfaLoggerFunc.tradeDebug( "sql=" + wheresql )
    
    #=====紧急支付====
    if(TradeContext.TRCCO=="9900519"):
        #=====得到existp紧急止付登记簿总记录笔数====
        allcount=rccpsDBTrcc_existp.count(wheresql)
    #=====其它====    
    else:
        #=====得到trccan撤销申请登记簿总记录笔数====
        allcount=rccpsDBTrcc_trccan.count(wheresql)
    
    if(allcount<0):
        return AfaFlowControl.ExitThisFlow('A099','查询总记录数失败')
    
    #=====设置排列顺序====
    ordersql=" order by BJEDTE DESC,BSPSQN DESC"    

    #=====紧急支付====
    if(TradeContext.TRCCO=="9900519"):
        #=====查询紧急止付登记簿====
        records=rccpsDBTrcc_existp.selectm(start_no,sel_size,wheresql,ordersql)
    #=====其他====
    else:
        #=====查询撤销申请登记簿====
        records=rccpsDBTrcc_trccan.selectm(start_no,sel_size,wheresql,ordersql)
    
    if records==None:
        return AfaFlowControl.ExitThisFlow('A099','查询失败' )   
    if( len(records)<=0 ):
        return AfaFlowControl.ExitThisFlow('A099','未查找到数据' )    
    else:
        #=====生成文件====
        AfaLoggerFunc.tradeInfo(">>>开始生成文件")
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetHostDate()+"_"+TradeContext.TransCode
        fpath=os.environ["AFAP_HOME"]+"/tmp/"
        
        f=open(fpath+filename,"w")
        
        if(f==None):
            return AfaFlowControl.ExitThisFlow('A099','打开文件失败' )
            
        filecontext=""
        #=====写文件操作====
        if(TradeContext.TRCCO=="9900501"):  #撤销申请
            AfaLoggerFunc.tradeInfo(">>>开始撤销申请处理")
            for i in range(0,len(records)):
                #=====生成文件内容====
                filecontext=records[i]['BJEDTE']       + "|" \
                           +records[i]['BSPSQN']       + "|" \
                           +records[i]['BESBNO']       + "|" \
                           +records[i]['BETELR']       + "|" \
                           +records[i]['BEAUUS']       + "|" \
                           +records[i]['NCCWKDAT']     + "|" \
                           +records[i]['BOJEDT']       + "|" \
                           +records[i]['BOSPSQ']       + "|" \
                           +records[i]['TRCCO']        + "|" \
                           +records[i]['TRCDAT']       + "|" \
                           +records[i]['TRCNO']        + "|" \
                           +records[i]['SNDBNKCO']     + "|" \
                           +records[i]['SNDBNKNM']     + "|" \
                           +records[i]['RCVBNKCO']     + "|" \
                           +records[i]['RCVBNKNM']     + "|" \
                           +records[i]['ORTRCCO']      + "|" \
                           +records[i]['CUR']          + "|" \
                           +str(records[i]['OCCAMT'])  + "|" \
                           +records[i]['CONT']         + "|" \
                           +records[i]['CLRESPN']      + "|"
                AfaLoggerFunc.tradeDebug(">>>生成文件条目[" + str(i) + "]")           
                f.write(filecontext+"\n")                
        elif(TradeContext.TRCCO=='9900502'):   #撤销申请应答
            AfaLoggerFunc.tradeInfo(">>>进入撤销申请应答处理")
            for i in range(0,len(records)):
                #=====生成文件内容====
                filecontext=records[i]['BJEDTE']       + "|" \
                           +records[i]['BSPSQN']       + "|" \
                           +records[i]['BESBNO']       + "|" \
                           +records[i]['BETELR']       + "|" \
                           +records[i]['BEAUUS']       + "|" \
                           +records[i]['NCCWKDAT']     + "|" \
                           +records[i]['BOJEDT']       + "|" \
                           +records[i]['BOSPSQ']       + "|" \
                           +records[i]['TRCCO']        + "|" \
                           +records[i]['TRCDAT']       + "|" \
                           +records[i]['TRCNO']        + "|" \
                           +records[i]['SNDBNKCO']     + "|" \
                           +records[i]['SNDBNKNM']     + "|" \
                           +records[i]['RCVBNKCO']     + "|" \
                           +records[i]['RCVBNKNM']     + "|" \
                           +records[i]['ORTRCCO']       + "|" \
                           +records[i]['CUR']          + "|" \
                           +str(records[i]['OCCAMT'])  + "|" \
                           +records[i]['CONT']         + "|" \
                           +records[i]['CLRESPN']      + "|"
                AfaLoggerFunc.tradeDebug(">>>生成文件条目[" + str(i) + "]")           
                f.write(filecontext+"\n")        
        elif(TradeContext.TRCCO=='9900519'):  #紧急支付
            AfaLoggerFunc.tradeInfo(">>>进入紧急支付处理")
            errors=0
            for i in range(0,len(records)):
                #=====生成文件内容====
                filecontext=records[i]['BJEDTE']       + "|" \
                           +records[i]['BSPSQN']       + "|" \
                           +records[i]['BESBNO']       + "|" \
                           +records[i]['BETELR']       + "|" \
                           +records[i]['BEAUUS']       + "|" \
                           +records[i]['NCCWKDAT']     + "|" \
                           +records[i]['BOJEDT']       + "|" \
                           +records[i]['BOSPSQ']       + "|" \
                           +records[i]['TRCCO']        + "|" \
                           +records[i]['TRCDAT']       + "|" \
                           +records[i]['TRCNO']        + "|" \
                           +records[i]['SNDBNKCO']     + "|" \
                           +records[i]['SNDBNKNM']     + "|" \
                           +records[i]['RCVBNKCO']     + "|" \
                           +records[i]['RCVBNKNM']     + "|" \
                           +records[i]['ORTRCCO']      + "|" \
                           +records[i]['CUR']          + "|" \
                           +str(records[i]['OCCAMT'])  + "|" \
                           +records[i]['CONT']         + "|" \
                           +""                         + "|"
                AfaLoggerFunc.tradeDebug("生成文件条目[" + str(i) + "]")           
                f.write(filecontext+"\n")
                errors=errors+1
        else:
            return AfaFlowControl.ExitThisFlow('M999','业务类型非法')
                
        #====关闭文件====
        f.close()
        AfaLoggerFunc.tradeInfo( ">>>生成文件结束 ")
        
        #=====输出接口赋值====   
        TradeContext.PBDAFILE=filename              #文件名 
        TradeContext.RECSTRNO=start_no              #起始笔数
#        if(len(records)>10):
#            TradeContext.RECCOUNT=str(sel_size)     #查询笔数
#        else:
#            TradeContext.RECCOUNT=str(len(records)) #查询笔数
        TradeContext.RECCOUNT=str(len(records)) #查询笔数
        TradeContext.RECALLCOUNT=str(allcount)      #总笔数
        TradeContext.errorCode="0000"
        TradeContext.errorMsg="查询成功"
        
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作交易[TRC001_8527]退出***' )
    return True