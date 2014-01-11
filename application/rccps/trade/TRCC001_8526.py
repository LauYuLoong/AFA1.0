# -*- coding: gbk -*-
##################################################################
#   农信银系统：往账.本地类操作(1.本地操作).汇票信息明细查询
#=================================================================
#   程序文件:   TRCC001_8526.py
#   作    者:   潘广通
#   修改时间:   2008-07-09
##################################################################
import rccpsDBTrcc_bilinf,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools
from types import *
import os

def SubModuleDoFst():    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作交易[TRC001_8526]进入***' )
        
    #=====得到起始笔数====
    start_no=TradeContext.RECSTRNO
        
    #=====组织sql语句====
    wheresql=""
    wheresql = wheresql + "NOTE3='" + TradeContext.BESBNO + "' and "
    
    #=====判断起始时间是否为空====
    if (TradeContext.STRDAT != "00000000"):
        wheresql = wheresql + "BILDAT>='"+TradeContext.STRDAT+"' and "

    #=====判断终止时间是否为空====
    if (TradeContext.ENDDAT != "00000000"):
        wheresql=wheresql+" BILDAT<='"+TradeContext.ENDDAT+"' and "
    
    #=====判断汇票类别是否为空====
    if (TradeContext.BILTYP != ""):
        wheresql=wheresql+" BILTYP='"+TradeContext.BILTYP+"' and "
    
    #=====判断汇票状态是否为空====
    if (TradeContext.HPSTAT != ""):
        wheresql=wheresql+" HPSTAT='"+TradeContext.HPSTAT+"' and "

    #=====判断兑付方式是否为空==== 
    if (TradeContext.PAYWAY != ""):
        wheresql=wheresql+" PAYWAY='"+TradeContext.PAYWAY+"' and "

    #=====判断汇票本行他行标识是否为空====
    if(TradeContext.BILRS !="" ):
        wheresql=wheresql+" BILRS='"+TradeContext.BILRS+"' and "

    #=====判断汇票版本号是否为空====        
    if(TradeContext.BILVER!="" ):
        wheresql=wheresql+" BILVER='"+TradeContext.BILVER+"' and "

    #=====判断汇票号码是否为空====        
    if(TradeContext.BILNO!="" ):
        wheresql=wheresql+" BILNO='"+TradeContext.BILNO+"' and "

    #=====判断出票金额是否为0====        
    if((TradeContext.BILAMT).strip() != '0.00' ):
        wheresql = wheresql + " BILAMT=" + str(TradeContext.BILAMT) + ' and '
    
    #=====去除sql查询语句最后4位"end "====    
    wheresql = wheresql[:-4]
        
    #=====开始查询总笔数====
    allcount=rccpsDBTrcc_bilinf.count(wheresql)
    
    if(allcount<0):
        return AfaFlowControl.ExitThisFlow('A099','查找总记录数失败' )
        
    #=====开始查询明细====
    ordersql = " order by BILNO DESC"
    records=rccpsDBTrcc_bilinf.selectm(start_no,10,wheresql,ordersql)
    
    if(records==None):
        return AfaFlowControl.ExitThisFlow('A099','查询异常' )
        
    elif(len(records)==0):
        return AfaFlowControl.ExitThisFlow('S999','无对应记录' )
        
    else:
        #=====生成文件====
        filename = "rccps_" + TradeContext.BETELR + "_" + AfaUtilTools.GetHostDate() + "_" + TradeContext.TransCode       
        fpath=os.environ["AFAP_HOME"]+"/tmp/"
        f=open(fpath+filename,"w")
            
        if f == None:
            return AfaFlowControl.ExitThisFlow('S999','打开文件失败')
        
        for i in range(0,len(records)):            
            #=====生成文件内容====
            AfaLoggerFunc.tradeDebug ("生成文件内容 ")
            
            filecontext = ""
            filecontext = filecontext + records[i]['BILVER']      + "|"    #汇票版本号
            filecontext = filecontext + records[i]['BILNO']       + "|"    #汇票号码
            filecontext = filecontext + records[i]['BILRS']       + "|"    #汇票本行他行标识
            filecontext = filecontext + records[i]['BILTYP']      + "|"    #汇票类别
            filecontext = filecontext + records[i]['BILDAT']      + "|"    #汇票日期
            filecontext = filecontext + records[i]['PAYWAY']      + "|"    #兑付方式
            filecontext = filecontext + records[i]['REMBNKCO']    + "|"    #出票行行号
            filecontext = filecontext + records[i]['REMBNKNM']    + "|"    #出票行行名
            filecontext = filecontext + records[i]['PAYBNKCO']    + "|"    #代理付款行行号
            filecontext = filecontext + records[i]['PAYBNKNM']    + "|"    #代理付款行行名
            filecontext = filecontext + records[i]['PYRACC']      + "|"    #出票人账号
            filecontext = filecontext + records[i]['PYRNAM']      + "|"    #出票人户名
            filecontext = filecontext + records[i]['PYRADDR']     + "|"    #出票人地址
            filecontext = filecontext + records[i]['PYEACC']      + "|"    #收款人账号
            filecontext = filecontext + records[i]['PYENAM']      + "|"    #收款人户名
            filecontext = filecontext + records[i]['PYEADDR']     + "|"    #收款人地址
            filecontext = filecontext + records[i]['PYHACC']      + "|"    #持票人账号
            filecontext = filecontext + records[i]['PYHNAM']      + "|"    #持票人户名
            filecontext = filecontext + records[i]['PYHADDR']     + "|"    #持票人地址
            filecontext = filecontext + records[i]['PYITYP']      + "|"    #入账账户类型
            filecontext = filecontext + records[i]['PYIACC']      + "|"    #入账账户账号
            filecontext = filecontext + records[i]['PYINAM']      + "|"    #入账账户户名
            filecontext = filecontext + records[i]['CUR']         + "|"    #币种
            filecontext = filecontext + str(records[i]['BILAMT']) + "|"    #出票金额
            filecontext = filecontext + str(records[i]['OCCAMT']) + "|"    #实际结算金额
            filecontext = filecontext + str(records[i]['RMNAMT']) + "|"    #结余金额
            filecontext = filecontext + records[i]['SEAL']        + "|"    #密押
            filecontext = filecontext + records[i]['USE']         + "|"    #用途
            filecontext = filecontext + records[i]['REMARK']      + "|"    #备注
            filecontext = filecontext + records[i]['HPSTAT']      + "|"    #汇票状态

            f.write(filecontext+"\n")
            
        f.close()
        
    #=====输出接口====
    TradeContext.PBDAFILE=filename              #文件名
    TradeContext.RECCOUNT=str(len(records))     #查询笔数
    TradeContext.RECALLCOUNT=str(allcount)      #总笔数
    TradeContext.errorCode="0000"
    TradeContext.errorMsg="查询成功"
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作交易[TRC001_8526]退出***' )
        
    return True
