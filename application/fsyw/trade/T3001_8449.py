###############################################################################
# -*- coding: gbk -*-
# 文件标识：
# 摘    要：安徽非税
#
# 当前版本：1.0
# 作    者：WJJ
# 完成日期：2007年10月15日
###############################################################################

#表中的状态位 0 已勾兑待查  1未勾兑待查  *非待查数据
import TradeContext, AfaDBFunc, AfaLoggerFunc, os, sys
from types import *

def SubModuleMainFst( ):

    TradeContext.__agentEigen__  = '0'   #从表标志

    AfaLoggerFunc.tradeInfo( "********************中台清分开始***************" )

    fileName    =   os.environ['AFAP_HOME'] + "/data/ahfs/" + TradeContext.FileName
    cnt         =   0
    amount      =   0.0

    #-----------------------根据单位编码配置获取财政信息----------------------------
    sqlstr      =   "select aaa010,bankno from fs_businoinfo where busino='" + TradeContext.busiNo + "'"
    records = AfaDBFunc.SelectSql( sqlstr )
    if records == None or len(records)==0 :
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","查找单位信息表异常"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        AfaLoggerFunc.tradeInfo( sqlstr )
        sys.exit(1)

    elif len(records) > 1:
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","单位信息表异常:一个单位编号对应了多个财政信息"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        AfaLoggerFunc.tradeInfo( sqlstr )
        sys.exit(1)

    TradeContext.AAA010     =   records[0][0].strip()
    TradeContext.AFA101     =   records[0][1].strip()

    #TradeContext.AAA010     =   "0000000000"
    #TradeContext.AFA101     =   "011"
    try:
        cnt         =   0
        amount      =   0.0
        if ( os.path.exists(fileName) and os.path.isfile(fileName) ):
            fp      =   open(fileName,"r")
            sLine   =   fp.readline()
            while ( sLine ):
                LineItem    =   sLine.split("|")

                #查找到了流水号码，则更新状态位置

                dateTmp     =   TradeContext.serDate[0:4] + '-' + TradeContext.serDate[4:6] + '-' + TradeContext.serDate[6:8]
                if LineItem[0].strip() == '0':
                    TradeContext.errorCode  =   "0002"
                    TradeContext.errorMsg   =   "待查数据自动生成，不需写入待查"
                    #sqlstr  =   "update fs_fc74 set flag ='1',busino='" + TradeContext.busiNo + "',afc016='" + TradeContext.brno + "',teller='" + TradeContext.teller + "',date='" + TradeContext.workDate + "' where afc401='" + LineItem[1].strip() + "' and afc015='" + dateTmp + "' and BUSINO='" + TradeContext.busiNo + "'"
                else:
                    sqlstr  =   "select date from fs_fc74 where afc401='" + LineItem[1].strip() + "' and afc015='" + dateTmp + "' and BUSINO='" + TradeContext.busiNo + "'"

                    #===条件增加银行编码字段,张恒修改===
                    sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

                    AfaLoggerFunc.tradeInfo( sqlstr )
                    records =   AfaDBFunc.SelectSql( sqlstr )
                    if( records == None ):
                        TradeContext.errorCode  =   "0001"
                        TradeContext.errorMsg   =   "查找日期信息失败"
                        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                        AfaLoggerFunc.tradeInfo( sqlstr + AfaDBFunc.sqlErrMsg )
                        return False
                    date    =   records[0][0]
                    AfaLoggerFunc.tradeInfo( date )
                    if TradeContext.workDate != date:
                        TradeContext.errorCode  =   "0002"
                        TradeContext.errorMsg   =   "待查数据已上传，不得删除待查"
                        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                        return False
                    TradeContext.errorCode  =   "0002"
                    TradeContext.errorMsg   =   "待查数据自动生成，不得删除待查"
                    #sqlstr  =   "update fs_fc74 set flag ='*',busino='" + TradeContext.busiNo + "',afc016='" + TradeContext.brno + "',teller='" + TradeContext.teller + "',date='" + '00000000' + "' where afc401='" + LineItem[1].strip() + "' and afc015='" + dateTmp + "' and BUSINO='" + TradeContext.busiNo + "'"
                AfaLoggerFunc.tradeInfo( sqlstr )
                if( AfaDBFunc.UpdateSqlCmt( sqlstr ) < 1 ):
                    AfaLoggerFunc.tradeInfo( '---test----->[' +sqlstr + ']<------------')
                    TradeContext.errorCode, TradeContext.errorMsg='0002', '待查数据自动生成,更新流水号%s失败' %( LineItem[1].strip() )
                    #TradeContext.errorCode, TradeContext.errorMsg='0002', '待查数据自动生成，不可修改')
                    AfaLoggerFunc.tradeInfo( TradeContext.errorMsg + AfaDBFunc.sqlErrMsg )
                    AfaLoggerFunc.tradeInfo(  sqlstr )
                    return False

                cnt     =   cnt + 1
                amount  =   amount + float(LineItem[4].strip())

                sLine   =   fp.readline()

        else:
            AfaLoggerFunc.tradeInfo( "文件" + fileName + "不存在" )
            TradeContext.errorCode  =   "0002"
            TradeContext.errorMsg   =   "待查文件不存在"
            return False

        AfaLoggerFunc.tradeInfo( "********************中台清分结束***************" )
        TradeContext.errorCode  =   "0000"
        TradeContext.errorMsg   =   "插入或更新待查表成功"
        TradeContext.Total      =   str(amount)
        TradeContext.Count      =   str(cnt)
        AfaLoggerFunc.tradeInfo( TradeContext.Count )
        return True

    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        TradeContext.errorCode  =   "0003"
        TradeContext.errorMsg   =   "插入待查表异常"
        return False
