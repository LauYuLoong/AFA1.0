# -*- coding: gbk -*-
################################################################################
#   批量业务系统：下载参数表
#===============================================================================
#   交易文件:   T001000_8400.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  XZH
#   修改时间:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,os
from types import *


#=====================下载单位信息参数表========================================
def TrxMain():
    

    AfaLoggerFunc.tradeInfo('**********下载单位信息(8400)开始**********')


    TradeContext.fileSum1 = 0
    TradeContext.fileSum2 = 0


    #生成批量信息
    if not GetBatchBusiInfo():
        return False


    #生成实时信息
    if not GetRealBusiInfo():
        return False


    #统计下载文件数量
    sFileNum = 0
    sFileNum = TradeContext.fileSum1 + TradeContext.fileSum2
    if ( sFileNum <= 0 ):
        return ExitSubTrade( '9000', '没有任何单位信息' )

    #下载的单位数量
    TradeContext.tradeResponse.append(['fileSum', str(sFileNum)])


    AfaLoggerFunc.tradeInfo('**********下载单位信息(8400)结束**********')

    #返回
    TradeContext.tradeResponse.append(['errorCode', '0000'])
    TradeContext.tradeResponse.append(['errorMsg',  '交易成功'])
    return True


#获取批量单位信息
def GetBatchBusiInfo():

    try:
        AfaLoggerFunc.tradeInfo('下载批量单位信息')
    
        rm_cmd_str = "rm " + os.environ['AFAP_HOME'] + "/tmp/*" + TradeContext.I1SBNO + ".plist"
        os.system(rm_cmd_str)
    
        #统计该机构号下有多少个业务编码(批量)
        sql = "SELECT DISTINCT(APPNO),APPNAME FROM ABDT_UNITINFO WHERE STATUS = '1' AND AGENTTYPE IN ('3','4')" 
        sql = sql + " AND (AGENTMODE='0' OR (AGENTMODE='1' AND SUBSTR(BRNO,1,4)='" + TradeContext.I1SBNO[:4]
        sql = sql + "') OR (AGENTMODE='2' AND BRNO='" + TradeContext.I1SBNO + "'))"

        AfaLoggerFunc.tradeInfo(sql)

        records = AfaDBFunc.SelectSql( sql )
        if( records==None):
             return ExitSubTrade( '9000', '下载单位代码和名称异常1' )
                
        elif( len(records) == 0 ):
            AfaLoggerFunc.tradeInfo('没有发现任何单位信息')
            return True

        else:
            TradeContext.fileSum1 = len(records)     #将要下载多少个文件名字

            AfaLoggerFunc.tradeInfo('实时单位信息文件数量=' + str(TradeContext.fileSum1))

            #生成业务代码文件
            filename1 = os.environ['AFAP_HOME'] + "/tmp/BAPPNO_" + TradeContext.I1SBNO + ".plist"

            AfaLoggerFunc.tradeInfo('文件名=' + filename1)

            fp1 = open(filename1,'w')
            fp1.write("TITLE = 业务编码\n")

            for i in range(0,int(TradeContext.fileSum1)):

                fp1.write("ITEM  = " + AfaUtilTools.lrtrim(records[i][0]) + " | " + AfaUtilTools.lrtrim(records[i][1]) + " |\n")

                #生成一个固定的文件名字为appNo+机构代码.plist
                filename = os.environ['AFAP_HOME'] + "/tmp/B" + AfaUtilTools.lrtrim(records[i][0]) + TradeContext.I1SBNO + ".plist"
                fp = open(filename,'w')
                fp.write("TITLE = 单位编码\n")

                #根据appNo查询相应信息
                sql1 = "SELECT BUSINO,BUSINAME FROM ABDT_UNITINFO WHERE "
                sql1 = sql1 + "APPNO=" + "'" + records[i][0] + "'"                 #业务编号
                sql1 = sql1 + " AND STATUS='1'"                                    #状态(0:注销,1:正常)
                sql1 = sql1 + " AND AGENTTYPE IN ('1','2','3','4') AND (AGENTMODE='0' OR (AGENTMODE='1' AND SUBSTR(BRNO,1,4)='" + TradeContext.I1SBNO[:4] + "') OR (AGENTMODE='2' AND BRNO='" + TradeContext.I1SBNO + "'))"

                try:
                    AfaLoggerFunc.tradeInfo(sql1)
                    
                    records1 = AfaDBFunc.SelectSql( sql1 )
                        
                    if( records1==None):
                        fp.close()
                        fp1.close()
                        return ExitSubTrade( '9000', '下载单位代码和名称异常2' )

                    else:
                        TradeContext.busiSum = len(records1)

                        for j in range(0,int(TradeContext.busiSum)):
                            fp.write("ITEM = " + AfaUtilTools.lrtrim(records1[j][0]) + " | " + AfaUtilTools.lrtrim(records1[j][1]) + " |\n")

                        fp.close()

                except Exception,e:
                    AfaLoggerFunc.tradeInfo(e)
                    fp.close()
                    fp1.close()
                    return ExitSubTrade( '9000', '下载单位代码和名称异常3' )

        return True
        
    except Exception,e:
        AfaLoggerFunc.tradeInfo(e)
        fp1.close()
        return ExitSubTrade( '9999', '查找业务代码异常' )


	
#获取实时单位信息
def GetRealBusiInfo():

    try:
        AfaLoggerFunc.tradeInfo('下载实时单位信息')

        #统计该机构号下有多少个业务编码(实时)
        sql = "SELECT DISTINCT(APPNO),APPNAME FROM ABDT_UNITINFO WHERE AGENTTYPE IN ('1','2')" 
        sql = sql + " AND (AGENTMODE='0' OR (AGENTMODE='1' AND SUBSTR(BRNO,1,4)='" + TradeContext.I1SBNO[:4]
        sql = sql + "') OR (AGENTMODE='2' AND BRNO='" + TradeContext.I1SBNO + "'))"

        AfaLoggerFunc.tradeInfo(sql)

        records = AfaDBFunc.SelectSql( sql )
        if( records==None):
             return ExitSubTrade( '9000', '下载实时单位代码和名称异常1' )

        elif( len(records) == 0 ):
            AfaLoggerFunc.tradeInfo('没有发现任何实时单位信息')
            return True

        else:
            TradeContext.fileSum2 = len(records)     #将要下载多少个文件名字

            AfaLoggerFunc.tradeInfo('实时单位信息文件数量=' + str(TradeContext.fileSum2))

            #生成业务代码文件
            filename1 = os.environ['AFAP_HOME'] + "/tmp/RAPPNO_" + TradeContext.I1SBNO + ".plist"

            AfaLoggerFunc.tradeInfo('文件名=' + filename1)

            fp1 = open(filename1,'w')
            fp1.write("TITLE = 业务编码\n")

            for i in range(0,int(TradeContext.fileSum2)):

                fp1.write("ITEM  = " + AfaUtilTools.lrtrim(records[i][0]) + " | " + AfaUtilTools.lrtrim(records[i][1]) + " |\n")

                #生成一个固定的文件名字为appNo+机构代码.plist
                filename = os.environ['AFAP_HOME'] + "/tmp/R" + AfaUtilTools.lrtrim(records[i][0]) + TradeContext.I1SBNO + ".plist"
                fp = open(filename,'w')
                fp.write("TITLE = 单位编码\n")

                #根据appNo查询相应信息
                sql1 = "SELECT BUSINO,BUSINAME FROM ABDT_UNITINFO WHERE "
                sql1 = sql1 + "APPNO=" + "'" + records[i][0] + "'"                  #业务编号
                sql1 = sql1 + " AND STATUS='1'"                                    #状态(0:注销,1:正常)
                sql1 = sql1 + " AND AGENTTYPE IN ('1','2') AND (AGENTMODE='0' OR (AGENTMODE='1' AND SUBSTR(BRNO,1,4)='" + TradeContext.I1SBNO[:4] + "') OR (AGENTMODE='2' AND BRNO='" + TradeContext.I1SBNO + "'))"

                try:
                    AfaLoggerFunc.tradeInfo(sql1)

                    records1 = AfaDBFunc.SelectSql( sql1 )
                    
                    if( records1==None):
                        fp.close()
                        fp1.close()
                        return ExitSubTrade( '9000', '下载实时单位代码和名称异常2' )

                    else:
                        TradeContext.busiSum = len(records1)

                        for j in range(0,int(TradeContext.busiSum)):
                            fp.write("ITEM = " + AfaUtilTools.lrtrim(records1[j][0]) + " | " + AfaUtilTools.lrtrim(records1[j][1]) + " |\n")

                        fp.close()

                except Exception,e:
                    AfaLoggerFunc.tradeInfo(e)
                    fp.close()
                    fp1.close()
                    return ExitSubTrade( '9000', '下载实时单位代码和名称异常3' )

        return True

    except Exception,e:
        AfaLoggerFunc.tradeInfo(e)
        fp1.close()
        return ExitSubTrade( '9999', '查找实时业务代码异常' )



def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
