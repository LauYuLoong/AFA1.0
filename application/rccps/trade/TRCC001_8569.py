# -*- coding: gbk -*-
##################################################################
#   农信银.行内记账
#=================================================================
#   程序文件:   TRCC001_8569.py
#   修改时间:   2008-06-05
##################################################################

import rccpsDBFunc,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaDBFunc
from types import *
from rccpsConst import *
import rccpsState,rccpsFtpFunc,os,rccpsCronFunc,rccpsHostFunc

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统: 往账.本地类操作交易[RCC001_8569]进入***' )

    #=====判断输入接口值是否存在====
    if(not TradeContext.existVariable("STRDAT")):
        return AfaFlowControl.ExitThisFlow('A099', '起始日期[STRDAT]不存在')
    if(not TradeContext.existVariable("ENDDAT")):
        return AfaFlowControl.ExitThisFlow('A099', '结束日期[ENDDAT]不存在')
        
    if TradeContext.ENDDAT > AfaUtilTools.GetHostDate():
        return AfaFlowControl.ExitThisFlow('S999', '结束日期必须在当前日期之前')
        
    #=====获取主机日期==================
    TradeContext.BJEDTE=AfaUtilTools.GetHostDate( )

    #===========生成行内记账文件====================
    #===========文件格式===========================
    #交易日期|起始日期|终止日期|交易机构号|往来标志|收费总金额|汇兑类笔数|汇兑类总金额|汇票类笔数|汇票类总金额|
    #通存通兑类笔数|通存通兑类总金额|信息类笔数|信息类总金额|记录状态|备用字段 1|备用字段 2|备用字段 3|备用字段 4
    
    file_path = os.environ['AFAP_HOME'] + "/data/rccps/host/"
    file_name = 'rccsxfile' + TradeContext.BJEDTE
    TradeContext.OCCAMT = 0     #总金额
    TradeContext.CONT   = 0     #总笔数
    rb = open(file_path + file_name,'w')
    
    sqlStr = "select distinct NCCWKDAT,BESBNO from rcc_trcsta "
    sqlStr = sqlStr + "where NCCWKDAT >= '" + TradeContext.STRDAT + "' and NCCWKDAT <= '" + TradeContext.ENDDAT + "'"
    sqlStr = sqlStr + "and BRSFLG = '" + PL_BRSFLG_SND + "' order by NCCWKDAT,BESBNO"
    AfaLoggerFunc.tradeInfo(sqlStr)
    records = AfaDBFunc.SelectSql(sqlStr)
    if (records == None):
        return AfaFlowControl.ExitThisFlow('A099', '查询[RCC_NCCWKDAT]表异常')
    else:

        for i in range(len(records)):
            sqlStr_1 = "select t.TRCCO,t.ts,t.ts*double(t1.BPADAT) from("
            sqlStr_1 = sqlStr_1 + "select TRCCO,sum(TCNT) ts from rcc_trcsta"
            sqlStr_1 = sqlStr_1 + " where NCCWKDAT = '" + records[i][0] + "' and BESBNO = '" + records[i][1] + "'"
            sqlStr_1 = sqlStr_1 + " group by TRCCO" 
            sqlStr_1 = sqlStr_1 + ") t,RCC_PAMTBL t1 where t.TRCCO = t1.BPARAD and double(t1.BPADAT) > 0"

            AfaLoggerFunc.tradeDebug(sqlStr_1)
            res = AfaDBFunc.SelectSql(sqlStr_1)
            if (res == None):
                return AfaFlowControl.ExitThisFlow('A099', '查询[RCC_NCCWKDAT]表异常')
                
            amount20 = 0
            sum20 = 0
            amount21 = 0
            sum21 = 0
            amount30 = 0
            sum30 = 0
            amount99 = 0
            sum99 = 0 
            AfaLoggerFunc.tradeInfo(res)
            for j in range(len(res)):
                if(len(res[j][0]) < 7):
                    return AfaFlowControl.ExitThisFlow('A099', '[RCC_PAMTBL]表交易代码[' + res[j][0] + ']异常')
                elif((res[j][0])[:2] == '20'):
                    amount20 = amount20 + float(res[j][2])
                    sum20 = sum20 + int(res[j][1])
                elif((res[j][0])[:2] == '21'):
                    amount21 = amount21 + float(res[j][2])
                    sum21 = sum21 + int(res[j][1])
                elif((res[j][0])[:2] == '30'):
                    amount30 = amount30 + float(res[j][2])
                    sum30 = sum30 + int(res[j][1])
                elif((res[j][0])[:2] == '99'):
                    amount99 = amount99 + float(res[j][2])
                    sum99 = sum99 + int(res[j][1])
               
            Amount = amount20 + amount21 + amount30 + amount99
            #=====如果总金额不大于零，则进入下次循环=================
            if(Amount <= 0):
                continue
                
            TradeContext.OCCAMT = TradeContext.OCCAMT + Amount
            TradeContext.CONT   = TradeContext.CONT + 1
            lines = ""
            lines = lines + str(records[i][0]).strip().ljust(8, ' ') + "|"
            lines = lines + str(TradeContext.STRDAT).strip().ljust(8, ' ') + "|"
            lines = lines + str(TradeContext.ENDDAT).strip().ljust(8, ' ') + "|"
            lines = lines + str(records[i][1]).strip().ljust(10,' ') + "|"
            lines = lines + str(Amount).strip().ljust(15,' ') + "|"
            lines = lines + str(sum20).strip().ljust(8,' ') + "|"
            lines = lines + str(amount20).strip().ljust(15,' ') + "|"
            lines = lines + str(sum21).strip().ljust(8,' ') + "|"
            lines = lines + str(amount21).strip().ljust(15,' ') + "|"
            lines = lines + str(sum30).strip().ljust(8,' ') + "|"
            lines = lines + str(amount30).strip().ljust(15,' ') + "|"
            lines = lines + str(sum99).strip().ljust(8,' ') + "|"
            lines = lines + str(amount99).strip().ljust(15,' ') + "|"
            lines = lines + str('0').ljust(1,' ') + "|"
            lines = lines + str('').ljust(62,' ') + "|"
            lines = lines + str('').ljust(62,' ') + "|"
            lines = lines + str('').ljust(62,' ') + "|"
            lines = lines + str('').ljust(62,' ') + "|"
            
            rb.write(lines + "\n")
    
    
    rb.close()

    #===========文件转换============================
    AfaLoggerFunc.tradeInfo('>>>文件转换')
    sFileName = file_name
    dFileName = 'RCCSXFILE.SX'+ TradeContext.BJEDTE
    fldName = 'nxsxa.fld'
    if( not rccpsCronFunc.FormatFile('1', fldName, sFileName, dFileName)):
        return AfaFlowControl.ExitThisFlow('A099', '转换主机对账文件编码异常')
    
    
    #===========上传记账文件========================
    AfaLoggerFunc.tradeInfo('>>>上传记账文件')
    if( not rccpsFtpFunc.putHost(dFileName)):
        return AfaFlowControl.ExitThisFlow('A099', '上传记账文件异常')

    AfaLoggerFunc.tradeInfo('>>>触发主机接口')
    #===========发送主机交易===========================
    TradeContext.HostCode = '8823'                       #交易码
    TradeContext.OCCAMT = str(TradeContext.OCCAMT)
    AfaLoggerFunc.tradeInfo('>>>扣收金额'+ str(TradeContext.OCCAMT))
    TradeContext.fileName = 'SX' + TradeContext.BJEDTE   #文件名
    
    rccpsHostFunc.CommHost( TradeContext.HostCode )
    AfaLoggerFunc.tradeInfo("主机返回码[" + TradeContext.errorCode + "],主机返回信息[" + TradeContext.errorMsg +"]")
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
            
    TradeContext.errorCode = '0000'
    TradeContext.errorMsg  = '成功'
    
    AfaLoggerFunc.tradeInfo( '***农信银系统: 往账.本地类操作交易[RCC001_8569]退出***' )

    return True