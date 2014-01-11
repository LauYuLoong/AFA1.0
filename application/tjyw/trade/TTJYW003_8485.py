# -*- coding: gbk -*-
##################################################################
#   中间业务平台.
#=================================================================
#   程序文件:   TTJYW003_8498.py
#   程序说明:   缴费明细查询
#   修改时间:   2011-01-06
##################################################################
import TradeContext, AfaLoggerFunc,AfaFlowControl,AfaDBFunc,os
from types import *

def SubModuleDoFst( ):

    try:
        CrtJKMXFile( )
        TradeContext.count = "1"
        AfaLoggerFunc.tradeInfo(TradeContext.count)
        return True
    except  Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        AfaFlowControl.flowException( )

def CrtJKMXFile( ):
    
    try:
        sql = " select workdate,worktime,note3,amount,username,note1 from afa_maintransdtl"
        sql = sql + " where substr(workdate,1,6)='" + TradeContext.month  + "'"                         #缴款年月
        sql = sql + " and   sysid='"                + TradeContext.appno  + "'"                         #业务编号
        sql = sql + " and   unitno='"               + TradeContext.unitno + "'"                         #单位编号
        sql = sql + " and revtranf = '0' and bankstatus = '0' and ChkFlag = '0'"
        
        #20120709陈浩添加 note2 ---busino单位编码
        sql = sql + " and    note2   = '"           + TradeContext.busino +"'"                          #单位编码
        
        AfaLoggerFunc.tradeInfo( "缴款明细查询sql：" + sql )
        
        results = AfaDBFunc.SelectSql( sql )
        TradeContext.RecAllCount = str(len(results))
        
        if results == None:
            AfaLoggerFunc.tradeInfo( '查询缴款明细数据库异常' )
            return False
        elif len(results) == 0:
            AfaLoggerFunc.tradeInfo( '该月没有缴款明细记录' )
            TradeContext.errorCode = "E0001"
            TradeContext.errorMsg  = "该月没有缴款明细记录"
            return False
        else:
            AfaLoggerFunc.tradeInfo( '存在缴款明细' )
        
        #创建每月缴款明细电子文件
        mFileName = os.environ['HOME'] + "/afa/data/tjyw/report/P" + TradeContext.brno + "_" + TradeContext.tellerno + "_" + TradeContext.unitno + "_" + TradeContext.month + ".TXT"
        TradeContext.filename = "P" + TradeContext.brno + "_" + TradeContext.tellerno + "_" + TradeContext.unitno + "_" + TradeContext.month + ".TXT"
        AfaLoggerFunc.tradeInfo( '开始生成缴款明细电子文件：' + mFileName )
        AfaLoggerFunc.tradeInfo( TradeContext.filename )
        dfp = open( mFileName,"w" )
        
        tmpStr = "".ljust(116,"-") + "\n"
        #tmpStr = tmpStr + "".ljust(30)  + "代理中化化肥缴款明细" + "\n"
        tmpStr = tmpStr + "".ljust(30)  + "代理缴款明细" + "\n"
        tmpStr = tmpStr + "\n"
        tmpStr = tmpStr + "缴款月份：" + TradeContext.month + "\n"
        tmpStr = tmpStr + "\n"
        tmpStr = tmpStr + "".ljust(116,"-") + "\n"
        tmpStr = tmpStr + "缴款日期".ljust(14)
        tmpStr = tmpStr + "缴款时间".ljust(14)
        tmpStr = tmpStr + "交易机构名称".ljust(40)
        tmpStr = tmpStr + "金额".ljust(14)
        tmpStr = tmpStr + "缴款人姓名".ljust(20)
        tmpStr = tmpStr + "联系电话".ljust(14) + "\n"
        
        dfp.write( tmpStr )
        
        for i in range( 0,len(results) ):
            tmpStr =          results[i][0].lstrip().rstrip().ljust(14)          #缴款日期
            tmpStr = tmpStr + results[i][1].lstrip().rstrip().ljust(14)          #缴款时间
            tmpStr = tmpStr + results[i][2].lstrip().rstrip().ljust(40)          #交易机构名称
            tmpStr = tmpStr + results[i][3].lstrip().rstrip().ljust(14)          #金额
            tmpStr = tmpStr + results[i][4].lstrip().rstrip().ljust(20)          #缴款人姓名
            tmpStr = tmpStr + results[i][5].lstrip().rstrip().ljust(14)          #联系电话
            dfp.write( tmpStr + "\n" )
        dfp.close( )
        AfaLoggerFunc.tradeInfo( '生成缴款明细电子文件：' + mFileName + "成功")
        return True
        
    except  Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        AfaFlowControl.flowException( )
      
