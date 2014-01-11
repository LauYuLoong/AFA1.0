#!/usr/bin/env python
# -*- coding: gbk -*-
###############################################################################
# 文件名称：cpic_admin.py
# 文件标识：
# 摘    要：安贷宝对帐
#
# 当前版本：2.0
# 作    者：XZH
# 完成日期：2008年7月12日
#
# 取代版本：
# 原 作 者：
# 完成日期：
###############################################################################
import TradeContext, ConfigParser, sys, AfaDBFunc, os, AfaAdminFunc
from types import *


fileNameHead = 'ANHNX00001'
##########################################对帐处理##########################################
def SendToCorp(sysId,unitNo,trxDate):

    try:
        #交易日期,储蓄所代码,,银行流水号,保单号,金额
        sqlStr = "SELECT workdate,brno,agentserialno,note5,amount from afa_maintransdtl where "
        sqlStr = sqlStr + " SYSID='"        + sysId    + "'"
        sqlStr = sqlStr + " AND UNITNO='"   + unitNo   + "'"
        sqlStr = sqlStr + " AND WORKDATE='" + trxDate  + "'"
        #sqlStr = sqlStr + " and revtranf = '0' and bankstatus = '0'"
        sqlStr = sqlStr + " and revtranf = '0' and bankstatus = '0' and chkflag='0'"

        AfaAdminFunc.WrtLog(sqlStr)

        records = AfaDBFunc.SelectSql( sqlStr )
        if (records==None):
            AfaAdminFunc.WrtLog('>>>处理结果:生成对帐处理失败,数据库异常')
            return False

        if (len(records)==0):
            AfaAdminFunc.WrtLog('>>>处理结果:没有任何流水信息,不需要与企业进行对帐,请科技人员确定')
            return False


        #创建交换文件
        dzFileName = TradeContext.CORP_LDIR + '/' + sysId + "_" + unitNo + '_' + trxDate + '.txt'

        AfaAdminFunc.WrtLog(dzFileName)

        dzfp= open(dzFileName,  "w")
        
        totalnum = 0
        totalamt = 0
        
        chuFaLeiBie = ''
        for i in range(0, len(records)):
            tmpStr = ""
            #银行编码
            tmpStr = tmpStr + "01" + "|"
            #交易日期
            tmpStr = tmpStr + records[i][0].strip() + "|"
            #银行区域代码
            tmpStr = tmpStr + "ANHNX00001" + "|"
            #储蓄所代码
            tmpStr = tmpStr + records[i][1].strip()  + "|"
            #交易码
            tmpStr = tmpStr + "6000113" + "|"
            #银行流水号
            tmpStr = tmpStr + records[i][2].strip()  + "|"
            #保单号
            tmpStr = tmpStr + records[i][3].strip()  + "|"
            #金额
            tmpStr = tmpStr + records[i][4].strip()  + "|"
            #销售渠道
            tmpStr = tmpStr + "01|\n"
            
            dzfp.write(tmpStr)

            totalnum = totalnum + 1
            totalamt = totalamt + (float)(records[i][4].strip())

        dzfp.close()

        sqlStr = "update afa_maintransdtl set corpchkflag = '0' where "
        sqlStr = sqlStr + " SYSID='"+ sysId    + "'"
        sqlStr = sqlStr + " AND UNITNO='"   + unitNo   + "'"
        sqlStr = sqlStr + " AND WORKDATE='" + trxDate  + "'"
        sqlStr = sqlStr + " and revtranf = '0' and bankstatus = '0'"
        
        AfaAdminFunc.WrtLog(sqlStr)
        
        if not AfaDBFunc.UpdateSqlCmt(sqlStr):
            AfaAdminFunc.WrtLog('>>>处理结果:更新企业对账标识失败')
            return False

        AfaAdminFunc.WrtLog('>>>处理结果:对帐处理成功[总笔数='+str(totalnum) + ',总金额=' + str(totalamt) + ']')

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

        if not AfaAdminFunc.PutDzFile(sysId, lfileName, rfileName):
            return False

        return True

    except Exception, e:
        AfaAdminFunc.WrtLog(str(e))
        AfaAdminFunc.WrtLog('对帐处理异常')
        return False
        
###########################################主函数###########################################
if __name__=='__main__':


    print('**********安贷宝操作开始**********')

    if ( len(sys.argv) != 4 ):
        print( '用法: jtfk_Proc sysid unitno dateoffset')
        sys.exit(-1)

    sSysId      = sys.argv[1]
    sUnitno     = sys.argv[2]
    sOffSet     = sys.argv[3]
    sTrxDate   = AfaAdminFunc.getTimeFromNow(int(sOffSet))

    print '   系统编码 = ' + sSysId
    print '   单位编码 = ' + sUnitno
    print '   交易日期 = ' + sTrxDate

    #读取配置文件
    if ( not AfaAdminFunc.GetAdminConfig(sSysId + "_" + sUnitno) ) :
        sys.exit(-1)


    AfaAdminFunc.WrtLog('>>>与主机对帐')
    if not AfaAdminFunc.MatchData(sSysId,sUnitno,sTrxDate):
        sys.exit(-1)


    AfaAdminFunc.WrtLog('>>>与企业对帐')
    if not SendToCorp(sSysId,sUnitno,sTrxDate):
        sys.exit(-1)


    print '**********安贷宝操作结束**********'

    sys.exit(0)
