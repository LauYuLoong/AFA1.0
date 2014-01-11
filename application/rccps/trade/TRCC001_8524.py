# -*- coding: gbk -*-
##################################################################
#   农信银.查询打印业务.汇兑业务往来明细查询
#=================================================================
#   程序文件:   TRCC001_8524.py
#   修改时间:   2008-06-06
##################################################################
import rccpsDBTrcc_trcbka,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,rccpsDBFunc,rccpsDBTrcc_spbsta,rccpsState
from types import *
from rccpsConst import *
import os

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统: 往账.本地类操作交易[RCC001_8524]进入***' )
    
    #=====判断输入接口值是否存在====
    if( not TradeContext.existVariable( "STRDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099','起始日期[STRDAT]不存在' )
    if( not TradeContext.existVariable( "ENDDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099','终止日期[ENDDAT]不存在' )
    if( not TradeContext.existVariable( "BRSFLG" ) ):
        return AfaFlowControl.ExitThisFlow('A099','往来标志[BRSFLG]不存在' )
        
    #=====组织查询sql语句====
    AfaLoggerFunc.tradeInfo( "组织查询语句")


    if(TradeContext.BESBNO == "3400008889" and TradeContext.RCVBNKCO != ""):    
        sql= "BJEDTE >='"+TradeContext.STRDAT+"' and BJEDTE <='"
        sql= sql + TradeContext.ENDDAT + "'"
    else:
        sql= "BESBNO='" + TradeContext.BESBNO + "' " 
        sql= sql + "and BJEDTE >='"+TradeContext.STRDAT+"' and BJEDTE <='"
        sql= sql + TradeContext.ENDDAT + "'"
    
    if(TradeContext.BRSFLG != ""):
        sql= sql + " and BRSFLG='"+TradeContext.BRSFLG+"'"
        
    AfaLoggerFunc.tradeDebug( "1.sql=" + sql )
    #=====判断其它查询条件是否存在====
    if(TradeContext.OPRNO != ""):               #业务属性
        sql = sql + " and OPRNO='" + TradeContext.OPRNO + "'"
    if(TradeContext.OPRATTNO != ""):            #业务属性
        sql = sql + " and OPRATTNO='" + TradeContext.OPRATTNO + "'"
    if(TradeContext.BSPSQN != ""):              #报单序号
        sql = sql + " and BSPSQN='" + TradeContext.BSPSQN + "'"
    if(float(TradeContext.OCCAMT) != 0.0):      #交易金额
        sql = sql + " and OCCAMT=" + TradeContext.OCCAMT
    if(TradeContext.RCVBNKCO != ""):            #接收行号
        sql = sql + " and RCVBNKCO='" + TradeContext.RCVBNKCO + "'"
    if(TradeContext.BCSTAT != ""):              #交易状态
        if(TradeContext.BDWFLG!= ""):           #流转标志
            sql = sql + " and exists (select * from RCC_SPBSTA where "
            sql = sql + " BJEDTE = RCC_TRCBKA.BJEDTE"
            sql = sql + " and BSPSQN = RCC_TRCBKA.BSPSQN"
            sql = sql + " and BCSTAT = '" + TradeContext.BCSTAT + "'"
            sql = sql + " and BDWFLG='" + TradeContext.BDWFLG + "')"
        else:
            sql = sql + " and exists (select * from RCC_SPBSTA tab2 where "
            sql = sql + " BJEDTE = RCC_TRCBKA.BJEDTE"
            sql = sql + " and BSPSQN = RCC_TRCBKA.BSPSQN"
            sql = sql + " and BCSTAT = '" + TradeContext.BCSTAT + "')"
            
    AfaLoggerFunc.tradeDebug( "sql=" + sql )
    
    #=====开始查询总笔数====
    TradeContext.RECALLCOUNT=str(rccpsDBTrcc_trcbka.count(sql))     #总记录笔数
    
    AfaLoggerFunc.tradeDebug( '>>>总笔数=' + TradeContext.RECALLCOUNT )
    
    #=====查询数据库====    
    ordersql=" order by BJEDTE DESC,BSPSQN DESC"   #组织按降序排列排序
    AfaLoggerFunc.tradeInfo("查询条件为："+sql)
    
    records=rccpsDBTrcc_trcbka.selectm(TradeContext.RECSTRNO,10,sql,ordersql)
    
    if(records==None):
        return AfaFlowControl.ExitThisFlow('A099','查询失败' )       
    elif(len(records)==0):
        return AfaFlowControl.ExitThisFlow('A099','没有查找到记录' )    
    else:        		
        try:
            #=====打开文件====	
            AfaLoggerFunc.tradeInfo(">>>生成文件")
            filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetHostDate()+"_"+TradeContext.TransCode
            fpath=os.environ["AFAP_HOME"]+"/tmp/"

            f=open(fpath+filename,"w")
	        
            #=====PL_HDOPRNO_TH 09 退汇====
            if(TradeContext.OPRNO==PL_HDOPRNO_TH):	
                AfaLoggerFunc.tradeInfo(">>>进入退汇处理")	
	            #=====得到文件内容，生成文件====
                for i in range(0,len(records)):
                    #=====得到业务状态BCSTAT====
                    state_dict={}
                    ret=rccpsState.getTransStateCur(records[i]['BJEDTE'],records[i]['BSPSQN'],state_dict)
                    if(ret==False):
                        return AfaFlowControl.ExitThisFlow( 'S999', '当前状态登记簿中无此交易状态' )
                    #=====写文件操作====
                    filecontext = records[i]['BJEDTE']        + "|" \
                                + records[i]['BSPSQN']        + "|" \
                                + records[i]['BRSFLG']        + "|" \
                                + records[i]['BESBNO']        + "|" \
                                + records[i]['BEACSB']        + "|" \
                                + records[i]['BETELR']        + "|" \
                                + records[i]['BEAUUS']        + "|" \
                                + records[i]['TRCCO']         + "|" \
                                + records[i]['OPRNO']         + "|" \
                                + records[i]['OPRATTNO']      + "|" \
                                + records[i]['TRCDAT']        + "|" \
                                + records[i]['TRCNO']         + "|" \
                                + records[i]['SNDBNKCO']      + "|" \
                                + records[i]['SNDBNKNM']      + "|" \
                                + records[i]['RCVBNKCO']      + "|" \
                                + records[i]['RCVBNKNM']      + "|" \
                                + records[i]['CUR']           + "|" \
                                + str(records[i]['OCCAMT'])   + "|" \
                                + records[i]['PYRACC']        + "|" \
                                + records[i]['PYRNAM']        + "|" \
                                + records[i]['PYRADDR']       + "|" \
                                + records[i]['PYEACC']        + "|" \
                                + records[i]['PYENAM']        + "|" \
                                + records[i]['PYEADDR']       + "|" \
                                + records[i]['USE']           + "|" \
                                + records[i]['REMARK']        + "|" \
                                + records[i]['BILTYP']        + "|" \
                                + records[i]['BILDAT']        + "|" \
                                + records[i]['BILNO']         + "|" \
                                + str(records[i]['COMAMT'])   + "|" \
                                + str(records[i]['OVPAYAMT']) + "|" \
                                + str(records[i]['CPSAMT'])   + "|" \
                                + str(records[i]['RFUAMT'])   + "|" \
                                + records[i]['CERTTYPE']      + "|" \
                                + records[i]['CERTNO']        + "|" \
                                + records[i]['ORTRCCO']       + "|" \
                                + records[i]['ORTRCDAT']      + "|" \
                                + records[i]['ORTRCNO']       + "|" \
                                + records[i]['ORSNDBNK']      + "|" \
                                + records[i]['ORRCVBNK']      + "|" \
                                + records[i]['PYRACC']        + "|" \
                                + records[i]['PYRNAM']        + "|" \
                                + records[i]['PYEACC']        + "|" \
                                + records[i]['PYENAM']        + "|" \
                                + records[i]['STRINFO']       + "|" \
                                + state_dict['BCSTAT']        + "|" \
                                + state_dict['BDWFLG']        + "|"	\
                                + records[i]['BOJEDT']        + "|" \
                                + records[i]['BOSPSQ']        + "|" \
                                + records[i]['CHRGTYP']       + "|" \
                                + str(records[i]['LOCCUSCHRG'])    + "|" 
                    f.write(filecontext+"\n")                    
            #=====非退汇====
            else:
                AfaLoggerFunc.tradeInfo(">>>进入非退汇处理")
                for i in range(len(records)):
                    #=====得到业务状态BCSTAT====
                    state_dict={}
                    ret=rccpsState.getTransStateCur(records[i]['BJEDTE'],records[i]['BSPSQN'],state_dict)
                    if(state_dict==False):
                        return AfaFlowControl.ExitThisFlow( 'S999', '当前状态登记簿中无此交易状态' )
                    #=====写文件操作====
                    filecontext = records[i]['BJEDTE']   +    "|" \
                                + records[i]['BSPSQN']   +    "|" \
                                + records[i]['BRSFLG']   +    "|" \
                                + records[i]['BESBNO']   +    "|" \
                                + records[i]['BEACSB']   +    "|" \
                                + records[i]['BETELR']   +    "|" \
                                + records[i]['BEAUUS']   +    "|" \
                                + records[i]['TRCCO']    +    "|" \
                                + records[i]['OPRNO']    +    "|" \
                                + records[i]['OPRATTNO'] +    "|" \
                                + records[i]['TRCDAT']   +    "|" \
                                + records[i]['TRCNO']    +    "|" \
                                + records[i]['SNDBNKCO'] +    "|" \
                                + records[i]['SNDBNKNM'] +    "|" \
                                + records[i]['RCVBNKCO'] +    "|" \
                                + records[i]['RCVBNKNM'] +    "|" \
                                + records[i]['CUR']      +    "|" \
                                + str(records[i]['OCCAMT'])+  "|" \
                                + records[i]['PYRACC']   +    "|" \
                                + records[i]['PYRNAM']   +    "|" \
                                + records[i]['PYRADDR']  +    "|" \
                                + records[i]['PYEACC']   +    "|" \
                                + records[i]['PYENAM']   +    "|" \
                                + records[i]['PYEADDR']  +    "|" \
                                + records[i]['USE']      +    "|" \
                                + records[i]['REMARK']   +    "|" \
                                + records[i]['BILTYP']   +    "|" \
                                + records[i]['BILDAT']   +    "|" \
                                + records[i]['BILNO']    +    "|" \
                                + str(records[i]['COMAMT'])+  "|" \
                                + str(records[i]['OVPAYAMT'])+"|" \
                                + str(records[i]['CPSAMT'])+  "|" \
                                + str(records[i]['RFUAMT'])+  "|" \
                                + records[i]['CERTTYPE']   +  "|" \
                                + records[i]['CERTNO']     +  "|" \
                                + records[i]['ORTRCCO']    +  "|" \
                                + records[i]['ORTRCDAT']   +  "|" \
                                + records[i]['ORTRCNO']    +  "|" \
                                + records[i]['ORSNDBNK']   +  "|" \
                                + records[i]['ORRCVBNK']   +  "|" \
                                + "" + "|" + "" + "|" + "" +  "|" + "" + "|" \
                                + records[i]['STRINFO']    +  "|" \
                                + state_dict['BCSTAT']     +  "|" \
                                + state_dict['BDWFLG']     +  "|" \
                                + records[i]['BOJEDT']     +  "|" \
                                + records[i]['BOSPSQ']     +  "|" \
                                + records[i]['CHRGTYP']    +  "|" \
                                + str(records[i]['LOCCUSCHRG']) +  "|" 
                    f.write(filecontext+"\n")
                    
                f.close()
                AfaLoggerFunc.tradeInfo(">>>生成文件结束")
	    
        except Exception, e:
            #=====关闭文件====
            f.close()
            return AfaFlowControl.ExitThisFlow('A099','写入返回文件失败' )    
	    
        #=====输出接口赋值====
        TradeContext.RECCOUNT=str(len(records))     #查询笔数
        TradeContext.errorCode="0000"               #返回码
        TradeContext.errorMsg="成功"                #返回信息
        TradeContext.PBDAFILE=filename              #文件名
        
    AfaLoggerFunc.tradeInfo( '***农信银系统: 往账.本地类操作交易[RCC001_8524]退出***' )
    return True
