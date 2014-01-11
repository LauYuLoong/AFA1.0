# -*- coding: gbk -*-
################################################################################
#   批量业务系统：查询单位信息
#===============================================================================
#   交易文件:   T001000_8402.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  XZH
#   修改时间:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,os,AfaFunc
from types import *


#=====================查询单位信息==============================================
def TrxMain():


    AfaLoggerFunc.tradeInfo('**********查询单位信息(8402)开始**********')


    TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #工作日期
    TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #工作时间


    #判断单位信息是否存在
    sqlStr = "SELECT * FROM ABDT_UNITINFO WHERE "
    sqlStr = sqlStr +       "APPNO=" + "'" + TradeContext.I1APPNO   + "'"        #业务编号
    sqlStr = sqlStr + " AND BUSINO=" + "'" + TradeContext.I1BUSINO  + "'"        #单位编号
#   sqlStr = sqlStr + " AND STATUS=" + "'" + "1"                    + "'"        #状态(0:注销,1:正常)

    AfaLoggerFunc.tradeInfo( sqlStr )

    records = AfaDBFunc.SelectSql( sqlStr )
    if ( records == None ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return ExitSubTrade( '9000', '查询单位信息异常' )

    if ( len(records) <= 0 ):
        return ExitSubTrade( '9000', '没有任何单位信息')


    AfaLoggerFunc.tradeInfo("总共查询[" + str(len(records)) + "]条记录")

    #过滤None
    AfaUtilTools.ListFilterNone( records )
    
    #记录条数
    TradeContext.tradeResponse.append(['RECNUM',  str(len(records))])

    i=0
    while ( i  < len(records) ):
        TradeContext.tradeResponse.append(['O1APPNO',           str(records[i][0])])         #业务编号
        TradeContext.tradeResponse.append(['O1BUSINO',          str(records[i][1])])         #单位编号
        TradeContext.tradeResponse.append(['O1AGENTTYPE',       str(records[i][2])])         #委托方式
        TradeContext.tradeResponse.append(['O1AGENTMODE',       str(records[i][3])])         #代理范围
        TradeContext.tradeResponse.append(['O1VOUHTYPE',        str(records[i][4])])         #凭证类型
        TradeContext.tradeResponse.append(['O1VOUHNO',          str(records[i][5])])         #凭证号码
        TradeContext.tradeResponse.append(['O1ACCNO',           str(records[i][6])])         #银行账户(对公帐户)
        TradeContext.tradeResponse.append(['O1SUBACCNO',        str(records[i][7])])         #子帐户代码
        TradeContext.tradeResponse.append(['O1SIGNUPMODE',      str(records[i][8])])         #签约方式
        TradeContext.tradeResponse.append(['O1GETUSERNOMODE',   str(records[i][9])])         #单位客户编号获取方式
        TradeContext.tradeResponse.append(['O1PROTNO',          str(records[i][10])])        #协议号
        TradeContext.tradeResponse.append(['O1APPNAME',         str(records[i][11])])        #业务名称
        TradeContext.tradeResponse.append(['O1BUSINAME',        str(records[i][12])])        #单位名称
        TradeContext.tradeResponse.append(['O1ADDRESS',         str(records[i][13])])        #联系地址
        TradeContext.tradeResponse.append(['O1TEL',             str(records[i][14])])        #联系电话
        TradeContext.tradeResponse.append(['O1USERNAME',        str(records[i][15])])        #联系人员
        TradeContext.tradeResponse.append(['O1WORKDATE',        str(records[i][16])])        #工作日期
        TradeContext.tradeResponse.append(['O1BATCHNO',         str(records[i][17])])        #批次号
        TradeContext.tradeResponse.append(['O1STARTDATE',       str(records[i][18])])        #生效日期
        TradeContext.tradeResponse.append(['O1ENDDATE',         str(records[i][19])])        #失效日期
        TradeContext.tradeResponse.append(['O1STARTTIME',       str(records[i][20])])        #服务开始时间
        TradeContext.tradeResponse.append(['O1ENDTIME',         str(records[i][21])])        #服务终止时间
        TradeContext.tradeResponse.append(['O1ZONENO',          str(records[i][22])])        #地区代码
        TradeContext.tradeResponse.append(['O1BRNO',            str(records[i][23])])        #机构代码
        TradeContext.tradeResponse.append(['O1TELLERNO',        str(records[i][24])])        #柜员代码
        TradeContext.tradeResponse.append(['O1REGDATE',         str(records[i][25])])        #注册日期
        TradeContext.tradeResponse.append(['O1REGTIME',         str(records[i][26])])        #注册时间
        TradeContext.tradeResponse.append(['O1STATUS',          str(records[i][27])])        #状态
        TradeContext.tradeResponse.append(['O1CHKDATE',         str(records[i][28])])        #对账日期                      
        TradeContext.tradeResponse.append(['O1CHKTIME',         str(records[i][29])])        #对账时间                      
        TradeContext.tradeResponse.append(['O1CHKFLAG',         str(records[i][30])])        #对帐标志(0-未对账, 1-已对账)  
        TradeContext.tradeResponse.append(['O1NOTE1',           str(records[i][31])])        #备注1
        TradeContext.tradeResponse.append(['O1NOTE2',           str(records[i][32])])        #备注2
        TradeContext.tradeResponse.append(['O1NOTE3',           str(records[i][33])])        #备注3
        TradeContext.tradeResponse.append(['O1NOTE4',           str(records[i][34])])        #备注4
        TradeContext.tradeResponse.append(['O1NOTE5',           str(records[i][35])])        #备注5
        i=i+1

    AfaLoggerFunc.tradeInfo('**********查询单位信息(8402)结束**********')


    #返回
    TradeContext.tradeResponse.append(['errorCode', '0000'])
    TradeContext.tradeResponse.append(['errorMsg',  '交易成功'])
    return True


def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
        