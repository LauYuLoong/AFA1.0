# -*- coding: gbk -*-
import TradeContext, AfaFunc,AfaDBFunc,AfaUtilTools,HostContext,UtilTools
import os
from types import *
from datetime import *


################################################################################
#            公共函数
# 功    能：计算某一日期的前或后一天的日期
# 参数说明：datestr：为原始日期
#           day：    为偏移量
# 返回说明：None：   计算出错
#           str：    日期
# 事    例：
# 
################################################################################
def dateCvs(datestr = '',day = -1):
    try:
        if( not(type(day) is int) ):
            return None
        elif( not( (type(datestr) is str) and (len(datestr)==0 or len(datestr) == 8)) ):
            return None
        if(len(datestr) == 8):
            try:
                tmpDate = date(int(datestr[0:4]),int(datestr[4:6]),int(datestr[6:8]))
            except Exception, e:
                print str(e)
                return None
            else:
                retDate = tmpDate + timedelta(day)
                retDateStr = retDate.strftime("%Y%m%d")
                return retDateStr
        else:
            tmpDate = date.today()
            retDate = tmpDate + timedelta(day)
            retDateStr = retDate.strftime("%Y%m%d")
            return retDateStr    
    except Exception, e:
        print str(e)
        return None
################################################################################
#            公共函数
# 功    能：校验前台上上送日期
# 参数说明：
#           arrayList：为原始日期
#
# 返回说明：None：   计算出错
#           str：    日期
# 事    例：
# 
################################################################################
def chkDate(arrayList,day = 0):
    try:
        date = ""
        if( len(arrayList) > 1 ):
            if(len(arrayList[1]) != 0 ):
                retCode = dateCvs(datestr = arrayList[1],day = day)
                if retCode == None:
                    TradeContext.returnMsg = "\t输入日期["+arrayList[1]+"]不合法！"
                date = retCode
            else:
                date = dateCvs(day = day)
        else:
            date = dateCvs(day = day)
        if (date > dateCvs(day = 0)):
            TradeContext.returnMsg = "\t输入日期["+date+"] 大于当前日期["+dateCvs(day = 0)+"],日期错误！"
            return None
        return date
    except Exception,e:
        TradeContext.returnMsg = "\t校验日期["+str(arrayList)+"]出错"
        return None
################################################################################
#           日终处理.公共函数
# 功    能：取获取文件
# 参数说明：
# 事    例：
# 
################################################################################
def getFile(logger):
    logger.info('开始接收文件'+TradeContext.fileName)
    os.system( TradeContext.getFile )
    logger.info('结束接收文件'+TradeContext.fileName)
    return 0
################################################################################
#           日终处理.公共函数
# 功    能：发送文件
# 参数说明：
# 事    例：
# 
################################################################################
def putFile(logger):
    logger.info('开始发送文件'+TradeContext.fileName)
    os.system( TradeContext.putFile )
    logger.info('结束发送文件'+TradeContext.fileName)
    return 0

################################################################################
#           日终处理.公共函数
# 功    能：测试文件是否存在
# 参数说明：
# 事    例：
# 
################################################################################
def isExistFile(logger):
    logger.info( "开始测试文件是否存在" )
    psFilePath = TradeContext.filePath + TradeContext.fileName
    try:
        f = file( psFilePath,"r")
    except:
        logger.info( "文件"+TradeContext.fileName+"不存在" )
        return -1
    f.close()
    logger.info( "结束测试文件是否存在" )
    return 0
