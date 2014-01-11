# -*- coding: gbk -*-
##################################################################
#   农信银.查询打印业务.汇兑业务流水状态查询
#=================================================================
#   程序文件:   TRCC001_8528.py
#   修改时间:   2008-06-08
#   作者：      潘广通
##################################################################
import os
import rccpsDBTrcc_sstlog,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools
from types import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统: 往账.本地类操作交易[RCC001_8528]进入***' )

    #=====判断输入接口值是否存在====
    #if( not TradeContext.existVariable( "BJEDTE" ) ):
    #    return AfaFlowControl.ExitThisFlow('A099', '交易日期[BJEDTE]不存在')
    #    
    #if( not TradeContext.existVariable( "BSPSQN" ) ):
    #    return AfaFlowControl.ExitThisFlow('A099', '报单序号[BSPSQN]不存在')
    
    start_no=TradeContext.RECSTRNO      #起始笔数
    sel_size=10                         #查询笔数
    
    #=====生成查询语句====
    wheresql=""
    
    #关彬捷  20090401  增加按(前置日期,前置流水号)或(主机日期,主机流水号)查询流水状态详细信息
    check_flag = 0
    if TradeContext.existVariable('BJEDTE') and TradeContext.BJEDTE != '00000000' and TradeContext.existVariable('BSPSQN') and TradeContext.BSPSQN != '':
        wheresql = wheresql + "BJEDTE='" + TradeContext.BJEDTE + "'"
        wheresql = wheresql + " AND BSPSQN='" + TradeContext.BSPSQN + "' and "
        check_flag = 1
    
    if TradeContext.existVariable('FEDT') and TradeContext.FEDT != '00000000' and TradeContext.existVariable('RBSQ') and TradeContext.RBSQ != '':
        wheresql = wheresql + "FEDT='" + TradeContext.FEDT + "'"
        wheresql = wheresql + " AND RBSQ='" + TradeContext.RBSQ + "' and "
        check_flag = 1
    
    if TradeContext.existVariable('TRDT') and TradeContext.TRDT != '00000000' and TradeContext.existVariable('TLSQ') and TradeContext.TLSQ != '':
        wheresql = wheresql + "TRDT='" + TradeContext.TRDT + "'"
        wheresql = wheresql + " AND TLSQ='" + TradeContext.TLSQ + "' and "
        check_flag = 1
        
    if check_flag == 0:
        return AfaFlowControl.ExitThisFlow('A099', '查询条件非法')
        
    wheresql = wheresql[:-5]    
    
    AfaLoggerFunc.tradeDebug( "生成查询语句结束 ")
    
    #=====查询总记录数====
    allcount=rccpsDBTrcc_sstlog.count(wheresql)
    
    if(allcount<0):
        return AfaFlowControl.ExitThisFlow('A099','查询总笔数失败' )
        
    #=====查询数据库====
    ordersql = " order by BCURSQ DESC "
    
    records=rccpsDBTrcc_sstlog.selectm(start_no,sel_size,wheresql,ordersql)
    
    if(records==None):
        return AfaFlowControl.ExitThisFlow('A099','查询失败' )        
    elif(len(records)<=0):
        return AfaFlowControl.ExitThisFlow('A099','没有查找到数据' )        
    else:
    	try:
            #=====生成文件====
            filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetHostDate()+"_"+TradeContext.TransCode
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
            
            if(f==None):
                return AfaFlowControl.ExitThisFlow('A099','打开文件失败' )
                   
            #=====写文件操作====
            filecontext=""
            for i in range(0,len(records)):
                filecontext= records[i]['BJEDTE']      + "|" \
                           + records[i]['BSPSQN']      + "|" \
                           + records[i]['BCSTAT']      + "|" \
                           + records[i]['BDWFLG']      + "|" \
                           + records[i]['BESBNO']      + "|" \
                           + records[i]['BEACSB']      + "|" \
                           + records[i]['BETELR']      + "|" \
                           + records[i]['BEAUUS']      + "|" \
                           + records[i]['FEDT']        + "|" \
                           + records[i]['RBSQ']        + "|" \
                           + records[i]['TRDT']        + "|" \
                           + records[i]['TLSQ']        + "|" \
                           + records[i]['SBAC']        + "|" \
                           + records[i]['ACNM']        + "|" \
                           + records[i]['RBAC']        + "|" \
                           + records[i]['OTNM']        + "|" \
                           + records[i]['DASQ']        + "|" \
                           + records[i]['MGID']        + "|" \
                           + records[i]['PRCCO']       + "|" \
                           + records[i]['STRINFO']     + "|" \
                           + str(records[i]['PRTCNT']) + "|" \
                           + records[i]['BJETIM']      + "|" \
                           + records[i]['NOTE3']       + "|" \
                           + str(records[i]['BCURSQ']) + "|"
                f.write(filecontext+"\n")      
            f.close()  
            
        except Exception, e:
            #=====关闭文件====
            f.close()
            return AfaFlowControl.ExitThisFlow('A099','写入返回文件失败' ) 
            
        #=====输出接口1====
        TradeContext.RECCOUNT=str(len(records))             #查询笔数
        TradeContext.RECALLCOUNT=str(allcount)              #总笔数
        TradeContext.errorCode="0000"
        TradeContext.errorMsg="查询成功"
        TradeContext.RECSTRNO=str(start_no)                 #起始笔数
        TradeContext.PBDAFILE=filename                      #文件名

    AfaLoggerFunc.tradeInfo( '***农信银系统: 往账.本地类操作交易[RCC001_8528]退出***' )
    return True
