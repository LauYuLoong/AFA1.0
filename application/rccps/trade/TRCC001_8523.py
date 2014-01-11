# -*- coding: gbk -*-
##################################################################
#   农信银.查询打印业务.行名行号查询
#=================================================================
#   程序文件:   TRCC001_8523.py
#   修改时间:   2008-06-05
#   作者：      潘广通
##################################################################

import rccpsDBTrcc_paybnk,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools
from types import *
import os

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统: 往账.本地类操作交易[RCC001_8523]进入***' )
    
    #=====判断接口是否存在====
    if( (not TradeContext.existVariable("BANKBIN")) and (not TradeContext.existVariable("LNAME")) ):
        return AfaFlowControl.ExitThisFlow('A099','行名[LNAME]行号[BANKBIN]不能同时为空' )
        
    if int(TradeContext.RECSTRNO) == 0:
        return AfaFlowControl.ExitThisFlow('A009','起始笔数[RECSTRNO]不能为空')
    
    #=====起始笔数，查询笔数赋值====    
    start_no = TradeContext.RECSTRNO
    sel_size = 10 
    
    #=====组织sql语句====
    wheresql=""
    if(TradeContext.BANKBIN!=""):
        wheresql1=TradeContext.BANKBIN.split( )
        
        wheresql="BANKBIN like '%"
        j=0
        
        #=====如果只有一条记录时，不进入循环操作====
        for i in range(0,len(wheresql1)-1):
            wheresql=wheresql+wheresql1[i]+"%' and BANKBIN like '%"
            j=j+1
        
        wheresql=wheresql+wheresql1[j]+"%'"
        
    if(TradeContext.LNAME!=""):
        wheresql2=TradeContext.LNAME.split()
        
        #=====判断行号是否为空====
        if(TradeContext.BANKBIN!=""):
            wheresql=wheresql+" and BANKNAM like '%"        
        else:
            wheresql=wheresql+" BANKNAM like '%"
            
        j=0
        #=====如果只有一条记录时，不进入循环操作====
        for i in range(0,len(wheresql2)-1):
            wheresql=wheresql+wheresql2[i]+"%' and BANKNAM like '%"
            j=j+1
            
        wheresql=wheresql+wheresql2[j]+"%'"
        
    AfaLoggerFunc.tradeInfo("查询条件为："+wheresql)
    
    #=====查询总笔数====
    allcount=rccpsDBTrcc_paybnk.count(wheresql)
    if(allcount<0):
        return AfaFlowControl.ExitThisFlow('A099','查找总记录数失败' )
    
    AfaLoggerFunc.tradeInfo("总记录数为："+str(allcount))
    
    #=====开始查找数据库====
    ordersql = " order by BANKBIN "
    records=rccpsDBTrcc_paybnk.selectm(start_no,sel_size,wheresql,ordersql)
    
    if(records==None):
        return AfaFlowControl.ExitThisFlow('A099','查询数据库失败' )        
    elif(len(records)==0):
        return AfaFlowControl.ExitThisFlow('A099','没有查询到数据' )        
    else:
        #=====打开文件====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetHostDate()+"_"+TradeContext.TransCode
        fpath=os.environ["AFAP_HOME"]+"/tmp/"
        f=open(fpath+filename,"w")
        
        if(f==None):
            return AfaFlowControl.ExitThisFlow('A099','打开文件失败' )
            
        #=====写文件操作====
        AfaLoggerFunc.tradeInfo( '>>>开始组织文件' )       
        for i in xrange(0,len(records)):
            filecontext = records[i]['BANKBIN']    + "|" \
                        + records[i]['BANKNAM']    + "|" \
                        + records[i]['BANKSTATUS'] + "|" \
                        + records[i]['BANKATTR']   + "|" \
                        + records[i]['STLBANKBIN'] + "|" \
                        + records[i]['BANKADDR']   + "|" \
                        + records[i]['BANKPC']     + "|" \
                        + records[i]['BANKTEL']    + "|" \
                        + records[i]['EFCTDAT']    + "|" \
                        + records[i]['INVDAT']     + "|" \
                        + records[i]['ALTTYPE']    + "|" \
                        + records[i]['PRIVILEGE']  + "|"
            f.write(filecontext+"\n")
        f.close()
        
        #=====返回接口赋值====
        TradeContext.RECALLCOUNT=str(allcount)      #总笔数
        TradeContext.RECCOUNT=str(len(records))     #查询笔数
        TradeContext.PBDAFILE=filename              #文件名称
        TradeContext.errorMsg="查询成功"
        TradeContext.errorCode="0000"

        AfaLoggerFunc.tradeInfo( '***农信银系统: 往账.本地类操作交易[RCC001_8523]退出***' )

        return True
