# -*- coding: gbk -*-
import TradeContext, AfaFunc,AfaDBFunc,AfaUtilTools,HostContext,UtilTools
import os
from types import *
from datetime import *


################################################################################
#            ��������
# ��    �ܣ�����ĳһ���ڵ�ǰ���һ�������
# ����˵����datestr��Ϊԭʼ����
#           day��    Ϊƫ����
# ����˵����None��   �������
#           str��    ����
# ��    ����
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
#            ��������
# ��    �ܣ�У��ǰ̨����������
# ����˵����
#           arrayList��Ϊԭʼ����
#
# ����˵����None��   �������
#           str��    ����
# ��    ����
# 
################################################################################
def chkDate(arrayList,day = 0):
    try:
        date = ""
        if( len(arrayList) > 1 ):
            if(len(arrayList[1]) != 0 ):
                retCode = dateCvs(datestr = arrayList[1],day = day)
                if retCode == None:
                    TradeContext.returnMsg = "\t��������["+arrayList[1]+"]���Ϸ���"
                date = retCode
            else:
                date = dateCvs(day = day)
        else:
            date = dateCvs(day = day)
        if (date > dateCvs(day = 0)):
            TradeContext.returnMsg = "\t��������["+date+"] ���ڵ�ǰ����["+dateCvs(day = 0)+"],���ڴ���"
            return None
        return date
    except Exception,e:
        TradeContext.returnMsg = "\tУ������["+str(arrayList)+"]����"
        return None
################################################################################
#           ���մ���.��������
# ��    �ܣ�ȡ��ȡ�ļ�
# ����˵����
# ��    ����
# 
################################################################################
def getFile(logger):
    logger.info('��ʼ�����ļ�'+TradeContext.fileName)
    os.system( TradeContext.getFile )
    logger.info('���������ļ�'+TradeContext.fileName)
    return 0
################################################################################
#           ���մ���.��������
# ��    �ܣ������ļ�
# ����˵����
# ��    ����
# 
################################################################################
def putFile(logger):
    logger.info('��ʼ�����ļ�'+TradeContext.fileName)
    os.system( TradeContext.putFile )
    logger.info('���������ļ�'+TradeContext.fileName)
    return 0

################################################################################
#           ���մ���.��������
# ��    �ܣ������ļ��Ƿ����
# ����˵����
# ��    ����
# 
################################################################################
def isExistFile(logger):
    logger.info( "��ʼ�����ļ��Ƿ����" )
    psFilePath = TradeContext.filePath + TradeContext.fileName
    try:
        f = file( psFilePath,"r")
    except:
        logger.info( "�ļ�"+TradeContext.fileName+"������" )
        return -1
    f.close()
    logger.info( "���������ļ��Ƿ����" )
    return 0
