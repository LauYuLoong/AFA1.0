# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.本地类操作(1.本地操作).通存通兑业务登记簿查询
#===============================================================================
#   模板文件:   TRCC001_8567.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘振东
#   修改时间:   2008-10-24
################################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_wtrbka 

def SubModuleDoFst():    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作交易(1.本地操作).通存通兑业务登记簿查询[TRCC001_8567]进入***' )
    
    #=====必要性检查====
    AfaLoggerFunc.tradeInfo(">>>开始必要性检查")
    
    if( not TradeContext.existVariable( "STRDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '起始日期[STRDAT]不存在')
        
    if( not TradeContext.existVariable( "ENDDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '终止日期[ENDDAT]不存在')
    
    if( not TradeContext.existVariable( "BRSFLG" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '往来标志[BRSFLG]不存在')

    if( not TradeContext.existVariable( "PYITYP" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '卡折标志[PYITYP]不存在')
    
    if( not TradeContext.existVariable( "RECSTRNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '起始笔数[RECSTRNO]不存在')
        
    #=====组织sql语句====
    AfaLoggerFunc.tradeInfo(">>>开始组织查询sql语句")
    
    wheresql = ""
    wheresql = wheresql + "BJEDTE>='" + TradeContext.STRDAT + "' AND BJEDTE<='" + TradeContext.ENDDAT + "' "
    
    ordersql = " order by BJEDTE DESC,BSPSQN DESC,NCCWKDAT DESC "
    
    start_no = TradeContext.RECSTRNO        #起始笔数
    sel_size = 10                           #查询笔数
    
    #====add by pgt 0106 增加新的机构号的判断====
    if(TradeContext.BESBNO1 != ""):
        wheresql = wheresql + " and BESBNO='" + TradeContext.BESBNO1 + "' " 
        
    else:
        if(TradeContext.BESBNO != PL_BESBNO_BCLRSB):
            wheresql = wheresql + " and BESBNO='" + TradeContext.BESBNO + "' " 
    
    #=====判断往来标志是否为空====
    if(TradeContext.BRSFLG != ""):
        wheresql = wheresql + " AND BRSFLG='" + TradeContext.BRSFLG + "' "
        
#    #=====判断交易种类是否为空====
#    if(TradeContext.OPRTPNO != ""):
#        wheresql = wheresql + " AND OPRTPNO='" + TradeContext.OPRTPNO + "' "
   
    #=====判断报单序号是否为空====
    if(TradeContext.BSPSQN != ""):
        wheresql = wheresql + " AND BSPSQN='" + TradeContext.BSPSQN + "' "
        
    #=====判断业务状态是否为空====
    if(TradeContext.BCSTAT != ""):
        wheresql = wheresql + " AND OPRATTNO='" + TradeContext.BCSTAT + "' "	
        
    #=====判断卡折标志是否为空====
    if(TradeContext.PYITYP != ""):
        #wheresql = wheresql + " AND BBSSRC='" + TradeContext.PYITYP + "' "
        wheresql = wheresql + " AND ((PYETYP = '" + TradeContext.PYITYP + "' AND TRCCO in ('3000002','3000003','3000004','3000005')) OR (PYRTYP = '" + TradeContext.PYITYP + "' AND TRCCO in ('3000102','3000103','3000104','3000105')))"
    
    #=====判断发起行行号是否为空====
    if(TradeContext.SNDBNKCO != ""):
        wheresql = wheresql + " AND SNDBNKCO='" + TradeContext.SNDBNKCO + "' "
    
    #=====判断接收行行号是否为空====
    if(TradeContext.RCVBNKCO != ""):
        wheresql = wheresql + " AND RCVBNKCO='" + TradeContext.RCVBNKCO + "' "
    
    AfaLoggerFunc.tradeDebug(">>>结束组织查询sql语句")    
    
    #=====查询总记录数====
    allcount=rccpsDBTrcc_wtrbka.count(wheresql)
    
    if(allcount<0):
        return AfaFlowControl.ExitThisFlow('A099','查询总笔数失败' )
        
    #=====查询数据库====
    
    AfaLoggerFunc.tradeInfo("wheresql=" + wheresql)
    records = rccpsDBTrcc_wtrbka.selectm(start_no,sel_size,wheresql,ordersql)
    
    if(records == None):
        return AfaFlowControl.ExitThisFlow('A099','查询失败' )    
    if len(records) <= 0:
        return AfaFlowControl.ExitThisFlow('A099','未查找到数据' )
    else:
        #=====生成文件====
        try:
            filename = "rccps_" + TradeContext.BETELR+"_" + AfaUtilTools.GetHostDate() + "_" + TradeContext.TransCode
            fpath = os.environ["AFAP_HOME"] + "/tmp/"
            f = open(fpath + filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S099','打开文件失败')
       
        #=====写文件操作====
        try:
            filecontext=""
            AfaLoggerFunc.tradeInfo ("生成文件内容 ")
            for i in range(0,len(records)):
                
                #=====得到业务状态BCSTAT==== 
                stat_dict = {}
                if not rccpsState.getTransStateCur(records[i]['BJEDTE'],records[i]['BSPSQN'],stat_dict):
                    return AfaFlowControl.ExitThisFlow( 'S999', '当前业务登记簿没有满足条件的记录' )
                    
                filecontext= records[i]['BJEDTE']          + "|" \
                           + records[i]['BSPSQN']          + "|" \
                           + records[i]['BRSFLG']          + "|" \
                           + stat_dict['BCSTAT']           + "|" \
                           + stat_dict['BDWFLG']           + "|" \
                           + records[i]['BESBNO']          + "|" \
                           + records[i]['BETELR']          + "|" \
                           + records[i]['BEAUUS']          + "|" \
                           + records[i]['DCFLG']           + "|" \
                           + records[i]['OPRNO']           + "|" \
                           + records[i]['NCCWKDAT']        + "|" \
                           + records[i]['TRCCO']           + "|" \
                           + records[i]['TRCDAT']          + "|" \
                           + records[i]['TRCNO']           + "|" \
                           + records[i]['COTRCNO']         + "|" \
                           + records[i]['SNDMBRCO']        + "|" \
                           + records[i]['RCVMBRCO']        + "|" \
                           + records[i]['SNDBNKCO']        + "|" \
                           + records[i]['SNDBNKNM']        + "|" \
                           + records[i]['RCVBNKCO']        + "|" \
                           + records[i]['RCVBNKNM']        + "|" \
                           + records[i]['CUR']             + "|" \
                           + str(records[i]['OCCAMT'])     + "|" \
                           + records[i]['CHRGTYP']         + "|" \
                           + str(records[i]['CUSCHRG'])    + "|" \
                           + records[i]['PYRACC']          + "|" \
                           + records[i]['PYRNAM']          + "|" \
                           + records[i]['PYEACC']          + "|" \
                           + records[i]['PYENAM']          + "|" \
                           + records[i]['STRINFO']         + "|" \
                           + records[i]['CERTTYPE']        + "|" \
                           + records[i]['CERTNO']          + "|" \
                           + records[i]['BNKBKNO']         + "|" \
                           + str(records[i]['BNKBKBAL'])   + "|" 
                           
                f.write(filecontext+"\n")      
        except Exception,e:                                        
            f.close()                                              
            return AfaFlowControl.ExitThisFlow('S099','写文件失败')
            
    #=====输出接口赋值====
    TradeContext.RECSTRNO=start_no              #起始笔数
    TradeContext.RECCOUNT=str(len(records))     #本次查询笔数
    TradeContext.RECALLCOUNT=str(allcount)      #总笔数
    TradeContext.errorCode="0000"
    TradeContext.errorMsg="查询成功"
#    TradeContext.PRTDAT= TradeContext.BJEDTE    #打印日期
    TradeContext.PBDAFILE=filename              #文件名
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作交易(1.本地操作).通存通兑业务登记簿查询[TRCC001_8567]退出***' )
    return True 	
