# -*- coding: gbk -*-
##################################################################
#   农信银.往账.本地类操作(1.本地操作).对账差错登记簿查询
#=================================================================
#   程序文件:   TRCC001_8542.py
#   修改时间:   2008-06-07
#   修改者  ：  刘雨龙
#   修改时间：  2008-07-02
##################################################################
#   修改者  ：  刘振东
#   修改时间：  2008-10-27
#   修改内容:   添加 30 通存通兑 的相关查询
##################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,rccpsDBTrcc_hddzcz,rccpsDBTrcc_trcbka,rccpsDBTrcc_bilbka
import rccpsDBTrcc_hpdzcz,rccpsDBTrcc_tddzcz,rccpsDBFunc,os
from types import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作)对账差错登记簿查询[TRC001_8542]进入***' )
    
    #=====判断输入接口值是否存在====
    if( not TradeContext.existVariable( "STRDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '起始日期[STRDAT]不存在')
    if( not TradeContext.existVariable( "ENDDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '终止日期[ENDDAT]不存在')
    if( not TradeContext.existVariable( "OPRTYPNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '交易类型[OPRTYPNO]不存在')
    if( not TradeContext.existVariable( "RECSTRNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '起始笔数[RECSTRNO]不存在')
    
    #=====组织sql语句====
    wheresql=""
    wheresql=wheresql+"BJEDTE>='"+TradeContext.STRDAT+"'"
    wheresql=wheresql+" AND BJEDTE<='"+TradeContext.ENDDAT+"'"
    
    ordersql = " order by NCCWKDAT DESC"
    
    start_no=TradeContext.RECSTRNO          #起始笔数
    sel_size=10                             #查询笔数
    
    #=====20 汇兑====
    if TradeContext.OPRTYPNO == '20':
        #=====查询总笔数====
        allcount=rccpsDBTrcc_hddzcz.count(wheresql)
        if(allcount == -1):
            return AfaFlowControl.ExitThisFlow('S999', '查询总记录数异常')
        
        #=====查询明细====
        records=rccpsDBTrcc_hddzcz.selectm(start_no,sel_size,wheresql,ordersql)
        if(records == None):
            return AfaFlowControl.ExitThisFlow('S999', '查询汇兑错账登记簿异常')
        if(len(records) <= 0):
            return AfaFlowControl.ExitThisFlow('S999', '汇兑错账登记簿中无对应信息') 
    
    #=====21 汇票====        
    if TradeContext.OPRTYPNO == '21':
        #=====查询总笔数====
        allcount=rccpsDBTrcc_hpdzcz.count(wheresql)
        if(allcount == -1):
            return AfaFlowControl.ExitThisFlow('S999', '查询总记录数异常')
        
        #=====查询明细====
        records=rccpsDBTrcc_hpdzcz.selectm(start_no,sel_size,wheresql,ordersql)
        if(records == None):
            return AfaFlowControl.ExitThisFlow('S999', '查询汇票错账登记簿异常')
        if(len(records) <= 0):
            return AfaFlowControl.ExitThisFlow('S999', '汇票错账登记簿中无对应信息')
    
    #=====30 通存通兑(刘振东 20081024 添加)====        
    if TradeContext.OPRTYPNO == '30':
        #=====查询总笔数====
        allcount=rccpsDBTrcc_tddzcz.count(wheresql)
        if(allcount == -1):
            return AfaFlowControl.ExitThisFlow('S999', '查询总记录数异常')
        
        #=====查询明细====
        records=rccpsDBTrcc_tddzcz.selectm(start_no,sel_size,wheresql,ordersql)
        if(records == None):
            return AfaFlowControl.ExitThisFlow('S999', '查询汇票错账登记簿异常')
        if(len(records) <= 0):
            return AfaFlowControl.ExitThisFlow('S999', '汇票错账登记簿中无对应信息')
    
    #=====生成文件====
    AfaLoggerFunc.tradeInfo( "生成文件")
    filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
    try:
        pub_path = os.environ["AFAP_HOME"]
        pub_path = pub_path + "/tmp/"
        f=open(pub_path+filename,"w")
    except IOError:
        return AfaLoggerFunc.ExitThisFlow('S099','打开文件失败')
        
    #=====写文件操作====
    try:
        filecontext=""
        for i in range(0,len(records)):
            #=====生成文件内容====
            filecontext=records[i]['NCCWKDAT'] + "|" \
                       +records[i]['BJEDTE']   + "|" \
                       +records[i]['BSPSQN']   + "|" \
                       +records[i]['SNDBNKCO'] + "|" \
                       +records[i]['TRCDAT']   + "|" \
                       +records[i]['TRCNO']    + "|" \
                       +records[i]['EACTYP']   + "|" \
                       +records[i]['EACINF']   + "|" \
                       +records[i]['ISDEAL']   + "|" \
            
            #曾照泰20120614添加明细文件中增加接收行号
            filecontext1=""
            #=====20 汇兑====
            if(TradeContext.OPRTYPNO == '20'): 
                trcbka_sql = {}
                trcbka_sql = {'BJEDTE':records[i]['BJEDTE'],'BSPSQN':records[i]['BSPSQN']}
                result=rccpsDBTrcc_trcbka.selectu(trcbka_sql)
                if(result == None):
                    return AfaFlowControl.ExitThisFlow('S999', '查询汇兑业务登记簿异常')
                
                if(len(result) <= 0):
                    filecontext1=" " + "|" 
                else:
                    filecontext1= result['RCVBNKCO']+ "|" 
            #=====21 汇票====        
            elif TradeContext.OPRTYPNO == '21': 
                bilbka_sql = {}
                bilbka_sql = {'BJEDTE':records[i]['BJEDTE'],'BSPSQN':records[i]['BSPSQN']}
                result=rccpsDBTrcc_bilbka.selectu(bilbka_sql)
                AfaLoggerFunc.tradeInfo(result)
                if(result == None):
                    return AfaFlowControl.ExitThisFlow('S999', '查询汇票业务登记簿异常')
                
                if(len(result) <= 0):
                    filecontext1=" " + "|" 
                else:
                    filecontext1= result['RCVBNKCO']+ "|"              
            
            else:
                filecontext1= records[i]['RCVBNKCO'] + "|" 
            filecontext=filecontext+filecontext1 
            #end  
            f.write(filecontext+"\n")
    except Exception,e:     
        f.close()
        return AfaFlowControl.ExitThisFlow('S099','写文件失败')
    
    #=====输出接口赋值====
    TradeContext.PBDAFILE=filename              #文件名
    TradeContext.RECCOUNT=str(len(records))     #查询笔数
    TradeContext.RECALLCOUNT=str(allcount)      #总笔数
    TradeContext.errorCode="0000"
    TradeContext.errorMsg="查询成功"
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作)对账差错登记簿查询[TRC001_8542]退出***' )
    return True
