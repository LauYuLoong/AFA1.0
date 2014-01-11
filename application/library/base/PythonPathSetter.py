# -*- coding: gbk -*-
################################################################
#     ���������ļ��ṩ����������python������·��PYTHONPATH
#==============================================================
#                ��    �ߣ�    �� �� ��
#                �޸�ʱ�䣺    20070821
################################################################
from PythonPathRegexDef import *
import LoggerHandler
import encodings.gb18030, encodings.gb2312, encodings.gbk
import os, sys

CONFIGFILENAME = os.environ['AFAP_HOME'] + '/conf/pythonpath.conf'

gPreloadedPathSet = set(sys.path)
gFileTotalSize, gFileModifyTime = 0, 0

#�ж��ļ��Ƿ��޸Ĺ�����ȷ���Ƿ���Ҫ���¶�ȡ���õĽ���·��
def isConfigFileModified(configFileName):
    global gFileTotalSize, gFileModifyTime
    result = os.stat(configFileName)
    if((gFileTotalSize != result[6]) or (gFileModifyTime != result[8])):
        gFileTotalSize, gFileModifyTime = result[6], result[8]
        return True
    return False

#��ȡ�����ļ������õ���Ч��������·��
def analyzeConfiguredPaths(configFileName):
    resultList, mapFile = [], open(configFileName, 'r')
    for line in mapFile.readlines():
        if pComment.match(line) != None : continue
        if pBlank.match(line) != None : continue
        resultList.append(line.replace("\r", "").replace("\n", ""))
    mapFile.close()
    return resultList

#�޸ļ�¼��ϵͳ�еĽű�����·��
def modifyPythonPath(configFileName = CONFIGFILENAME):
    logger = LoggerHandler.getLogger('service')
    if not isConfigFileModified(configFileName):
        #logger.debug('����·�������ļ���%s��û���޸ģ�����Ҫ��������·��'%(configFileName))
        return

    #logger.debug('����·�������ļ���%s�����޸ģ����ؽ��׽ű�����·��'%(configFileName))
    currentPathSet, futurePathSet = set(sys.path), set(analyzeConfiguredPaths(configFileName))
    pathSetToSubtract, pathSetToAdd = currentPathSet - futurePathSet - gPreloadedPathSet, futurePathSet - currentPathSet
    for pathElem in pathSetToSubtract:
        sys.path.remove(pathElem)
        #print '��ϵͳɾ���ű�����·����%s��'%(pathElem)
        #logger.debug('��ϵͳɾ���ű�����·����%s��'%(pathElem))
    for pathElem in pathSetToAdd:
        sys.path.append(pathElem)
        #print '��ϵͳ��ӽű�����·����%s��'%(pathElem)
        #logger.debug('��ϵͳ��ӽű�����·����%s��'%(pathElem))

#����־�������ǰϵͳ���׽ű�����·��
def logCurrentPythonPath():
    logger = LoggerHandler.getLogger('service')
    logger.debug('��ǰϵͳ�н��׽ű�����·�����£�\n----------------------------------------------------------------------')
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
