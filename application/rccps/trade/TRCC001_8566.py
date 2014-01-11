# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.本地类操作(1.本地操作).冲正\冲销登记簿查询
#===============================================================================
#   模板文件:   TRCC001_8566.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘振东
#   修改时间:   2008-10-20
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_atcbka,rccpsDBTrcc_mpcbka

#=====个性化处理（本地操作）====
def SubModuleDoFst():    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作).冲正\冲销登记簿查询[TRC001_8566]进入***' )
        
    #=====必要性检查====
    AfaLoggerFunc.tradeInfo(">>>开始必要性检查")
    
    if( not TradeContext.existVariable( "STRDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '起始日期[STRDAT]不存在')
    
    if( not TradeContext.existVariable( "ENDDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '终止日期[ENDDAT]不存在')
    
    if( not TradeContext.existVariable( "TRCCO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '交易代码[TRCCO]不存在')
    
    if( not TradeContext.existVariable( "BRSFLG" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '往来标志[BRSFLG]不存在')
        
    if( not TradeContext.existVariable( "BESBNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '机构号[BESBNO]不存在')
    
    if( not TradeContext.existVariable( "RECSTRNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '起始笔数[RECSTRNO]不存在')
        
    AfaLoggerFunc.tradeInfo(">>>必要性检查结束")
    
    #=====组织sql语句====
    AfaLoggerFunc.tradeInfo(">>>开始组织查询sql语句")
    
    wheresql=""
    wheresql=wheresql+"BESBNO='"+TradeContext.BESBNO+"'"
    wheresql=wheresql+" AND BJEDTE>='"+TradeContext.STRDAT+"'"
    wheresql=wheresql+" AND BJEDTE<='"+TradeContext.ENDDAT+"'"
    
    ordersql = " order by BJEDTE DESC,BSPSQN DESC "
    
    start_no=TradeContext.RECSTRNO          #起始笔数
    sel_size=10                             #查询笔数
    
    #=====判断交易代码是否为空====
    if(TradeContext.TRCCO != ""):
        wheresql = wheresql + " AND TRCCO='" + TradeContext.TRCCO + "'"    
    
    #=====判断原交易代码是否为空====
    if(TradeContext.ORTRCCO != ""):
        wheresql = wheresql + " AND ORTRCCO='" + TradeContext.ORTRCCO + "'" 
        
    #=====判断报单序号是否为空====
    if(TradeContext.BSPSQN != ""):
        wheresql = wheresql + " AND BSPSQN='" + TradeContext.BSPSQN + "'"
    
    #=====判断原报单序号是否为空====
    if(TradeContext.BOSPSQ != ""):
        wheresql = wheresql + " AND BOSPSQ='" + TradeContext.BOSPSQ + "'"
            
    #=====判断往来标志是否为空====
    if(TradeContext.BRSFLG != ""):
        wheresql = wheresql +" AND BRSFLG='" + TradeContext.BRSFLG + "'"
        
    AfaLoggerFunc.tradeDebug(">>>结束组织查询sql语句")
    AfaLoggerFunc.tradeDebug(">>>sql="+str(wheresql) )
    
    #=====3000506 自动冲正登记簿查询====
    if TradeContext.TRCCO == '3000506':
        #=====查询总笔数====
        allcount=rccpsDBTrcc_atcbka.count(wheresql)
        if(allcount == -1):
            return AfaFlowControl.ExitThisFlow('S999','查询总记录数异常')
            
        #=====查询明细====
        AfaLoggerFunc.tradeInfo("wheresql=" + wheresql)
        records=rccpsDBTrcc_atcbka.selectm(start_no,sel_size,wheresql,ordersql)
        if(records == None):
            return AfaFlowControl.ExitThisFlow('S999', '查询冲正登记簿异常')
        if(len(records) <= 0):
            return AfaFlowControl.ExitThisFlow('S999', '冲正登记簿中无此对应信息')
    
    #=====3000504 手工冲销登记簿查询====
    elif TradeContext.TRCCO == '3000504':
        #=====查询总笔数====
        allcount=rccpsDBTrcc_mpcbka.count(wheresql)
        if(allcount == -1):
            return AfaFlowControl.ExitThisFlow('S999','查询总记录数异常')
            
        #=====查询明细====
        AfaLoggerFunc.tradeInfo("wheresql=" + wheresql)
        records=rccpsDBTrcc_mpcbka.selectm(start_no,sel_size,wheresql,ordersql)
        if(records == None):
            return AfaFlowControl.ExitThisFlow('S999', '查询冲销登记簿异常')
        if(len(records) <= 0):
            return AfaFlowControl.ExitThisFlow('S999', '冲销登记簿中无此对应信息')
    else:
        return AfaFlowControl.ExitThisFlow('S999','交易码非法' )      
    
    #=====生成文件====
    try:
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetHostDate()+"_"+TradeContext.TransCode
        fpath=os.environ["AFAP_HOME"]+"/tmp/"
        f=open(fpath+filename,"w")
    except IOError:
        return AfaFlowControl.ExitThisFlow('S099','打开文件失败')
              
    #=====写文件操作====
    AfaLoggerFunc.tradeInfo("记录数：" + str(len(records)))
    try:
        filecontext=""
        for i in range(0,len(records)):
            #AfaLoggerFunc.tradeDebug("写入第"+str(i)+"笔记录开始")
            filecontext= records[i]['BJEDTE']        + "|" \
                       + records[i]['BSPSQN']        + "|" \
                       + records[i]['BRSFLG']        + "|" \
                       + records[i]['BESBNO']        + "|" \
                       + records[i]['BETELR']        + "|" \
                       + records[i]['BEAUUS']        + "|" \
                       + records[i]['NCCWKDAT']      + "|" \
                       + records[i]['TRCCO']         + "|" \
                       + records[i]['TRCDAT']        + "|" \
                       + records[i]['TRCNO']         + "|" \
                       + records[i]['ORTRCDAT']      + "|" \
                       + records[i]['ORTRCNO']       + "|" \
                       + records[i]['SNDMBRCO']      + "|" \
                       + records[i]['RCVMBRCO']      + "|" \
                       + records[i]['SNDBNKCO']      + "|" \
                       + records[i]['SNDBNKNM']      + "|" \
                       + records[i]['RCVBNKCO']      + "|" \
                       + records[i]['RCVBNKNM']      + "|" \
                       + records[i]['BOJEDT']        + "|" \
                       + records[i]['BOSPSQ']        + "|" \
                       + records[i]['RESNCO']        + "|" \
                       + records[i]['PRCCO']         + "|" \
                       + records[i]['STRINFO']       + "|" 
                           
            f.write(filecontext+"\n")
            #AfaLoggerFunc.tradeDebug("写入第"+str(i)+"笔记录结束")
    except Exception,e:     
        f.close()
        return AfaFlowControl.ExitThisFlow('S099','写文件失败')
    
    #=====输出接口赋值====
    TradeContext.PBDAFILE=filename              #文件名
    TradeContext.RECCOUNT=str(len(records))     #本次查询笔数
    TradeContext.RECALLCOUNT=str(allcount)      #总笔数
    TradeContext.errorCode="0000"
    TradeContext.errorMsg="查询成功"
    
    AfaLoggerFunc.tradeDebug("filename=" + filename)
    
    TradeContext.PBDAFILE=filename              #文件名
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作)冲正\冲销登记簿查询[TRC001_8566]退出***' )
    
    return True
    
    
