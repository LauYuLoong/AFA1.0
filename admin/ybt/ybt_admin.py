# -*- coding: gbk -*-
###############################################################################
# 文件名称：ybt_admin.py
# 摘    要：安贷保、银保通对帐
# 当前版本：1.0
# 作    者：CYG
# 完成日期：2010年08月13日
###############################################################################
import TradeContext

TradeContext.sysType = 'cron'

import ConfigParser, sys, AfaDBFunc, os, YbtAdminFunc,HostContext,YbtFunc,AfaUtilTools
from types import *


fileNameHead = 'ANHNX00001'
##########################################对帐处理##########################################
def SendToCorp(sysId,unitNo,sysId2,unitNo2,trxDate):

    try:
        #交易日期,储蓄所代码,,银行流水号,保单号,金额
        sqlStr = "SELECT workdate,brno,agentserialno,note5,amount,sysid,note9,trxcode from afa_maintransdtl where "
        sqlStr = sqlStr + " ((SYSID = '"        + sysId    + "'"
        sqlStr = sqlStr + " AND UNITNO = '"   + unitNo   + "')"
        sqlStr = sqlStr + " OR (SYSID = '"        + sysId2    + "'"
        sqlStr = sqlStr + " AND UNITNO = '"   + unitNo2   + "'))"
        sqlStr = sqlStr + " AND WORKDATE='"     + trxDate  + "'"
        sqlStr = sqlStr + " and revtranf = '0' and bankstatus = '0' and ChkFlag = '0'"

        YbtAdminFunc.WrtLog(sqlStr)

        records = AfaDBFunc.SelectSql( sqlStr )
        if (records==None):
            YbtAdminFunc.WrtLog('>>>处理结果:生成对帐处理失败,数据库异常')
            return False

        if (len(records)==0):
            YbtAdminFunc.WrtLog('>>>处理结果:没有任何流水信息,不需要与企业进行对帐,请科技人员确定')
            return False


        #创建交换文件
        dzFileName = TradeContext.CORP_LDIR + '/' + sysId + "_" + unitNo + '_' + trxDate + '.txt'

        YbtAdminFunc.WrtLog(dzFileName)

        dzfp= open(dzFileName,  "w")
        
        totalnum = 0
        totalamt = 0
        
        chuFaLeiBie = ''
        for i in range(0, len(records)):
            tmpStr = ""
            #银行编码
            tmpStr = tmpStr + "01"                  + "|"
            #交易日期
            tmpStr = tmpStr + records[i][0].strip() + "|"
            #银行区域代码
            tmpStr = tmpStr + "ANHNX00001"          + "|"
            #储蓄所代码
            tmpStr = tmpStr + records[i][1].strip() + "|"
            #交易码
            if records[i][5] == 'AG2011':
                tmpStr = tmpStr + "6000113"         + "|"
            elif records[i][5] == 'AG2013':
                #银保通将交易码转换成保险公司对应的交易码
                filename = '/home/maps/afa/application/ybt/config/busino_' + unitNo2 + '.conf'    #配置文件名
                transcode =  YbtFunc.datamap( "TransCode",records[i][7],filename )
                tmpStr = tmpStr + transcode         + "|"
            #银行流水号
            tmpStr = tmpStr + records[i][2].strip() + "|"
            #保单号
            if records[i][5] == 'AG2011':
                tmpStr = tmpStr + records[i][3].strip()  + "|"
            elif records[i][5] == 'AG2013':
                items = records[i][6].split('|')
                if len(items) >= 4:
                    tmpStr = tmpStr + items[2]      + "|"
                else:
                    tmpStr = tmpStr + ""            + "|"
            #金额
            tmpStr = tmpStr + records[i][4].strip() + "|"
            #销售渠道
            tmpStr = tmpStr + "01|\n"
            
            dzfp.write(tmpStr)

            totalnum = totalnum + 1
            totalamt = totalamt + (float)(records[i][4].strip())

        dzfp.close()

        sqlStr = "update afa_maintransdtl set corpchkflag = '0' where "
        sqlStr = sqlStr + " SYSID in ('"        + sysId    + "','" +  sysId2 + "')"
        sqlStr = sqlStr + " AND UNITNO in ('"   + unitNo   + "','" + unitNo2 + "')"
        sqlStr = sqlStr + " AND WORKDATE='"     + trxDate  + "'"
        sqlStr = sqlStr + " and revtranf = '0' and bankstatus = '0' and ChkFlag = '0'"
        
        YbtAdminFunc.WrtLog(sqlStr)
        
        if not AfaDBFunc.UpdateSqlCmt(sqlStr):
            YbtAdminFunc.WrtLog('>>>处理结果:更新企业对账标识失败')
            return False

        YbtAdminFunc.WrtLog('>>>处理结果:对帐处理成功[总笔数='+str(totalnum) + ',总金额=' + str(totalamt) + ']')

        #文件长度
        TradeContext.DZFILESIZE = str(os.path.getsize(dzFileName))

        #对帐文件名
        TradeContext.DZFILENAME = dzFileName

        #总笔数
        TradeContext.DZNUM = str(totalnum)

        #总金额
        TradeContext.DZAMT = str(totalamt)

        #向第三方发送明细文件
        lfileName = sysId + "_" + unitNo + '_' + trxDate + '.txt'
        rfileName = fileNameHead + trxDate + '.txt'

        if not YbtAdminFunc.PutDzFile(sysId, lfileName, rfileName):
            return False

        return True

    except Exception, e:
        YbtAdminFunc.WrtLog(str(e))
        YbtAdminFunc.WrtLog('对帐处理异常')
        return False
        
###########################################主函数###########################################
if __name__=='__main__':

    YbtAdminFunc.WrtLog( '**********安贷保、银保通对账操作开始**********' )
    
    if ( len(sys.argv) in (3,4)):
    
        sSysId1     = sys.argv[1]          #业务代码
        sUnitno1    = sys.argv[2]          #保险公司代码
        if ( len(sys.argv) == 3 ):
            sTrxDate = AfaUtilTools.GetSysDate( ) 
        else:
            sTrxDate = sys.argv[3]          #对账日期
        
        if ( sSysId1 == 'AG2011' ):
            YbtAdminFunc.WrtLog('>>>信保通对帐开始') 
        elif ( sSysId1 == 'AG2013' ):
            YbtAdminFunc.WrtLog('>>>银保通对帐开始') 
        else:
            YbtAdminFunc.WrtLog('>>>无此业务类型，请检查参数') 
            sys.exit(-1)
            
        YbtAdminFunc.WrtLog('系统编码 = ' + sSysId1)
        YbtAdminFunc.WrtLog('单位编码 = ' + sUnitno1)
        YbtAdminFunc.WrtLog('对账日期 = ' + sTrxDate)
            
        #读取配置文件
        if ( not YbtAdminFunc.GetAdminConfig(sSysId1 + "_" + sUnitno1) ) :
            YbtAdminFunc.WrtLog('>>>读取配置文件失败') 
            sys.exit(-1)
        
        #与主机对账
        YbtAdminFunc.WrtLog('>>>与主机对帐开始')
        if not YbtAdminFunc.MatchData(sSysId1,sUnitno1,sTrxDate):
            YbtAdminFunc.WrtLog('>>>与主机对账失败，程序中止') 
            sys.exit(-1)
        YbtAdminFunc.WrtLog('>>>与主机对帐结束')
        
        #与企业对账
        YbtAdminFunc.WrtLog('>>>与企业对帐对账开始')
        if not SendToCorp(sSysId1,sUnitno1,sSysId1,sUnitno1,sTrxDate):
            YbtAdminFunc.WrtLog('>>>与企业对账失败，程序中止')
            sys.exit(-1)
        YbtAdminFunc.WrtLog('>>>与企业对帐对账结束')
        
    elif ( len(sys.argv) in (5,6)):
    
        YbtAdminFunc.WrtLog('>>>信保通、银保通对帐开始') 
        sSysId1     = sys.argv[1]          #业务代码
        sUnitno1    = sys.argv[2]          #保险公司代码
        sSysId2     = sys.argv[3]          #业务代码
        sUnitno2    = sys.argv[4]          #保险公司代码
        if ( len(sys.argv) == 5 ):
            sTrxDate = AfaUtilTools.GetSysDate( )  
        else:
            sTrxDate = sys.argv[5]          #对账日期
        
        YbtAdminFunc.WrtLog('信保通系统编码 = ' + sSysId1)
        YbtAdminFunc.WrtLog('信保通单位编码 = ' + sUnitno1)
        YbtAdminFunc.WrtLog('银保通系统编码 = ' + sSysId2)
        YbtAdminFunc.WrtLog('银保通单位编码 = ' + sUnitno2)
        YbtAdminFunc.WrtLog('对  账  日  期 = ' + sTrxDate)
        
        #读取配置文件
        if ( not YbtAdminFunc.GetAdminConfig(sSysId1 + "_" + sUnitno1) ) :
            YbtAdminFunc.WrtLog('>>>读取配置文件失败') 
            sys.exit(-1)
        
        #信保通与主机对账
        YbtAdminFunc.WrtLog('>>>信保通与主机对帐开始')
        if not YbtAdminFunc.MatchData(sSysId1,sUnitno1,sTrxDate):
            if (HostContext.O1MGID == 'TXT0001' or TradeContext.serialFlag == '0'):
                YbtAdminFunc.WrtLog('>>>主机没有发现信保通账务信息') 
            else:
                YbtAdminFunc.WrtLog('>>>信保通与主机对账失败，程序中止') 
                sys.exit(-1)
        YbtAdminFunc.WrtLog('>>>信保通与主机对帐结束')
        
        #银保通与主机对账
        YbtAdminFunc.WrtLog('>>>银保通与主机对帐开始')
        if not YbtAdminFunc.MatchData(sSysId2,sUnitno2,sTrxDate):
            if (HostContext.O1MGID == 'TXT0001' or TradeContext.serialFlag == '0'):
                YbtAdminFunc.WrtLog('>>>主机没有发现银保通账务信息') 
            else:
                YbtAdminFunc.WrtLog('>>>银保通与主机对账失败，程序中止') 
                sys.exit(-1)
        YbtAdminFunc.WrtLog('>>>银保通与主机对帐结束')
        
        #与企业对账
        YbtAdminFunc.WrtLog('>>>与企业对帐对账开始')
        if not SendToCorp(sSysId1,sUnitno1,sSysId2,sUnitno2,sTrxDate):
            YbtAdminFunc.WrtLog('>>>与企业对账失败，程序中止')
            sys.exit(-1)
        YbtAdminFunc.WrtLog('>>>与企业对帐对账结束')
        
    else:
        print( '用法1: jtfk_Proc sysid1 unitno1 date                 （只对信保通或者银保通的账）')
        print( '用法2: jtfk_Proc sysid1 unitno1 sysid2 unitno2 date  （同时对信保通和银保通的账）')
        sys.exit(-1)

    YbtAdminFunc.WrtLog( '**********安贷保、银保通对账操作结束**********' )

    sys.exit(0)
