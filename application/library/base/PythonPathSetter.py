# -*- coding: gbk -*-
################################################################
#     根据配置文件提供的内容设置python的搜索路径PYTHONPATH
#==============================================================
#                作    者：    陈 显 明
#                修改时间：    20070821
################################################################
from PythonPathRegexDef import *
import LoggerHandler
import encodings.gb18030, encodings.gb2312, encodings.gbk
import os, sys

CONFIGFILENAME = os.environ['AFAP_HOME'] + '/conf/pythonpath.conf'

gPreloadedPathSet = set(sys.path)
gFileTotalSize, gFileModifyTime = 0, 0

#判断文件是否被修改过，以确定是否需要重新读取配置的交易路径
def isConfigFileModified(configFileName):
    global gFileTotalSize, gFileModifyTime
    result = os.stat(configFileName)
    if((gFileTotalSize != result[6]) or (gFileModifyTime != result[8])):
        gFileTotalSize, gFileModifyTime = result[6], result[8]
        return True
    return False

#读取配置文件中配置的有效交易搜索路径
def analyzeConfiguredPaths(configFileName):
    resultList, mapFile = [], open(configFileName, 'r')
    for line in mapFile.readlines():
        if pComment.match(line) != None : continue
        if pBlank.match(line) != None : continue
        resultList.append(line.replace("\r", "").replace("\n", ""))
    mapFile.close()
    return resultList

#修改记录在系统中的脚本搜索路径
def modifyPythonPath(configFileName = CONFIGFILENAME):
    logger = LoggerHandler.getLogger('service')
    if not isConfigFileModified(configFileName):
        #logger.debug('搜索路径配置文件【%s】没有修改，不需要重载搜索路径'%(configFileName))
        return

    #logger.debug('搜索路径配置文件【%s】被修改，重载交易脚本搜索路径'%(configFileName))
    currentPathSet, futurePathSet = set(sys.path), set(analyzeConfiguredPaths(configFileName))
    pathSetToSubtract, pathSetToAdd = currentPathSet - futurePathSet - gPreloadedPathSet, futurePathSet - currentPathSet
    for pathElem in pathSetToSubtract:
        sys.path.remove(pathElem)
        #print '从系统删除脚本搜索路径【%s】'%(pathElem)
        #logger.debug('从系统删除脚本搜索路径【%s】'%(pathElem))
    for pathElem in pathSetToAdd:
        sys.path.append(pathElem)
        #print '往系统添加脚本搜索路径【%s】'%(pathElem)
        #logger.debug('往系统添加脚本搜索路径【%s】'%(pathElem))

#往日志中输出当前系统交易脚本搜索路径
def logCurrentPythonPath():
    logger = LoggerHandler.getLogger('service')
    logger.debug('当前系统中交易脚本搜索路径如下：\n----------------------------------------------------------------------')
    for pathElem in sys.path:
        logger.debug(pathElem)

modifyPythonPath()

if(__name__ == "__main__"):
    print "\n", gPreloadedPathSet
    for elem in gPreloadedPathSet:
        print elem

    modifyPythonPath()
    print "\n", sys.path
    for elem in sys.path:
        print elem

    import time
    time.sleep(10)

    modifyPythonPath()
    print "\n", sys.path
    for elem in sys.path:
        print elem
