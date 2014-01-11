# -*- coding: gbk -*-
##########################################################
#       ���ƣ�����ͨ���պ���                             #
#       ���ڣ�2009-04-01                                 #
#       ʱ�䣺15:15                                      #
#       ��������ͬ�Ƽ�                                   #
##########################################################
import TradeContext, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaDBFunc,AfaUtilTools,AfaLoggerFunc
import HostContext,AfaHostFunc,HostComm,ConfigParser
import os
from types import *
from datetime import *


################################################################################
#           ����ͨ.��������
# ��    �ܣ���������ҵ���������
# ����˵����
# ��    ����
# 
################################################################################
def HostCkgDetail(logger):
    logger.info( "���˱�����ʼ��" )
    HostContext.I1TRCD = '8837'                        #����������
    HostContext.I1SBNO = "3400008889"                  #�ý��׵ķ������(ʡ��������)
    HostContext.I1USID = '999986'                      #���׹�Ա��
    HostContext.I1AUUS = ""                            #��Ȩ��Ա
    HostContext.I1AUPS = ""                            #��Ȩ��Ա����
    HostContext.I1WSNO = ""                            #�ն˺�
    HostContext.I1STDT = TradeContext.corpDate         #��ʼ����
    HostContext.I1EDDT = TradeContext.corpDate         #��������
    #HostContext.I1NBBH = TradeContext.sysId            #����ҵ���(̫��: AG2011)
    HostTradeCode = "8837".ljust(10,' ')
    #logger.info( "HostTradeCode = " + str(HostTradeCode) )
    HostComm.callHostTrade( os.environ['AFAP_HOME'] + '/conf/hostconf/AH8837.map', HostTradeCode, "9002" )
    if(HostContext.existVariable("O1MGID")):
        if(HostContext.O1MGID == "AAAAAAA"):
            logger.info( "����������������ɹ�")
            return 0
        else:
            logger.info("ͨѶ�ɹ���������������������ϢΪ:["+HostContext.O1INFO+"]")
            return -1
    else:
        logger.info( "������ͨѶ�쳣������")
        return -2
    return 0
################################################################################
#           ����ͨ.�ļ�ת��
# ��    �ܣ������������ļ�ת��
# ����˵����
# ��    ����
# 
################################################################################
def FileTransfer(logger):
    logger.info( "��ʼת���ļ�" )
    try:
        dstFileName    = os.environ['AFAP_HOME'] + '/data/cpic/host/' + TradeContext.corpDate + "_HOSTDZ"
        srcFileName    = os.environ['AFAP_HOME'] + '/data/cpic/host/' + TradeContext.fileName
        #���ø�ʽ:cvt2ascii -T �����ı��ļ� -P �����ļ� -F fld�ļ� [-D �����] [-S] [-R]
        CvtProg     = os.environ['AFAP_HOME'] + '/data/cvt/cvt2ascii'
        fldFileName    = os.environ['AFAP_HOME'] + '/data/cvt/tbsca.fld'
        cmdstr=CvtProg + " -T " + dstFileName + " -P " + srcFileName + " -F " + fldFileName
        logger.info( "cmdstr = " + str(cmdstr) )
        
        ret = os.system(cmdstr)
        if ( ret != 0 ):
            return -1
        else:
            return 0
    except Exception, e:
        logger.info(e)
        logger.info('��ʽ���ļ��쳣')
        return -1
    return 0
################################################################################
#           ����ͨ.��������
# ��    �ܣ���������(�޸��м���ˮ)
# ����˵����
# ��    ���������ļ���ʽ
#           �������0|����ҵ���1|��ϵͳ����2|ǰ������3|ǰ����ˮ��4|��������5|������ˮ��6|���˱�־7|��ת��־8
#           |�����ʱ�־9|���׽��10|����ʾ11|��¼״̬12|�����ֶΣ�13|�����ֶΣ�14|�����ֶΣ�15
#           
################################################################################
def loadMdtlFile(logger):
    logger.info( "��ʼ�������������ļ�" )
    total ,mistake= 0 ,0
    try:
        sFileName = os.environ['AFAP_HOME'] + '/data/cpic/host/' + TradeContext.corpDate + "_HOSTDZ"
        f = file(sFileName,"r")
    except:
        return -1
    while( True ):
        sLine = f.readline()
        print sLine
        logger.info(sLine)
        sLine=sLine.replace('\r','')
        sLine=sLine.replace('\n','')
#        logger.info(str(len(sLine)))
        total = total + 1
        if(len(sLine) == 0):
            break
        arrayList = sLine.split("|")
        if(len(arrayList) > 6):
            TradeContext.hostAgentSeriano        = arrayList[4].strip()
            #print TradeContext.hostAgentSeriano
            TradeContext.hostDate                = arrayList[5].strip()
            #print TradeContext.hostDate
            TradeContext.hostSeriano             = arrayList[6].strip()
            #print TradeContext.hostSeriano
            #TradeContext.hostErrCode             = arrayList[3].strip()
            #print TradeContext.hostErrCode
            #TradeContext.hostErrMsg              = arrayList[4].strip()
            #print TradeContext.hostErrMsg
            if(UpdateAfaDetail( logger ) == 0 ):
                #print "���ʳɹ�"
                continue
            else:
                #print "����ʧ��"
                continue
        else:
            mistake = mistake + 1
            continue
    logger.info( "�����������������ļ�" )
    if(mistake > 0):
        TradeContext.rFile = "���ļ�����["+str(total)+"]����¼,��["+str(mistake)+"]����ʽ����."
    else:
        TradeContext.rFile = ""
    TradeContext.returnMsg = TradeContext.rFile+ "�������������ļ�����"
    f.close()
    return 0
#---------------------------------------------------------------------------------------------------------
def UpdateAfaDetail(logger):
    #if(TradeContext.hostErrCode == "0000"): #�������ض�����Ϣ,"0"��ʾ�ɹ�,"1"��ʾʧ��
    #    chkflag = "0"
    #else:
    #    chkflag = "1"
    try:
        sql = "UPDATE AFA_MAINTRANSDTL SET bankcode = '0000',chkflag = '0'"
        sql = sql + " where agentserialno = '"+TradeContext.hostAgentSeriano+"'"
        logger.info( "�����м�ҵ����ˮ�� " + str(sql) )
        retCode = AfaDBFunc.UpdateSqlCmt(sql)
        #print 'retCode = '+str(retCode)
        if(retCode < 1):
            logger.info("fail")
            return -2
        else:
            return 0
    except Exception , e:
        logger.info(sql+"\n\n"+str(e))
        return -1
#----------------------------------------------------------------------------------------------------------
###########################################################
#       ����ͨ����
#       ���ܣ����ɵ�����������ִ�ļ�
#       ���ڣ�2008-11-04
#       ˵����
#       ���б���(10)+��������(8)+�����������(10)+����������(10)+������(7)+
#       ������ˮ��(30)+������(20)+���(12λ����С����)+����������2λ��
#       ���б���Ĭ��Ϊ"01",�����������"ANHNX00001",��������"01"
###########################################################
def CreCpicLjFile(logger):
    logger.info( "��ʼ��������ͨ�������׻�ִ�ļ�" )
    TradeContext.table = 'AFA_MAINTRANSDTL'
    splitStr = "|"
    emptyStr = " "
    psFilePath = os.environ['HOME']+"/afa/data/cpic/cpic/"+TradeContext.fileName
    try:
        f = file( psFilePath,"w")
    except:
        logger.info( "�����ļ�"+TradeContext.fileName+"ʧ��" )
        return -1
    
    sqlUpdate = "UPDATE "+TradeContext.table+" SET corpchkflag ='0' WHERE sysId ='"+TradeContext.sysId+"' and unitno = '" + TradeContext.unitno + "' "
    sqlUpdate = sqlUpdate + "AND workdate = '"+TradeContext.corpDate+"' AND chkflag = '0' and revtranf = '0' and bankstatus = '0'"
    #print sqlUpdate
    logger.info("����chkflag>>>>>>"+str(sqlUpdate))
    records = AfaDBFunc.UpdateSqlCmt( sqlUpdate )
    #print 'records = '+str(records)
    if(records < 0):
        return -2
    '''�û����,���,��ˮ��'''
    sql = "SELECT workdate,brno,agentserialno,note5,amount "
    sql = sql + "FROM "+TradeContext.table+" WHERE sysId ='"+TradeContext.sysId+"'"
    sql = sql + "AND workdate = '"+TradeContext.corpDate+"' AND chkflag = '0' and revtranf = '0' and bankstatus = '0'"
    #print sql
    logger.info("��ѯ����>>>>>>"+str(sql))
    records = AfaDBFunc.SelectSql( sql )
    print "-------------< [����ͨ����ͨ������ִ�ļ�:�� " + str(len(records)) + "���ɹ���¼] >------------"
    logger.info( "< [����ͨ����ͨ������ִ�ļ�:�� " + str(len(records)) + "���ɹ���¼] >")
    if ( len(records) > 0 ):
        for i in range(0,len(records)):
            tmpStr = ""
            #���б���
            tmpStr = tmpStr + "01" +splitStr
            #��������
            tmpStr = tmpStr + records[i][0].strip() +splitStr
            #�����������
            tmpStr = tmpStr + "ANHNX00001" +splitStr
            #����������
            tmpStr = tmpStr + records[i][1].strip()  +splitStr
            #������
            tmpStr = tmpStr + "6000113" +splitStr
            #������ˮ��
            tmpStr = tmpStr + records[i][2].strip()  +splitStr
            #������
            tmpStr = tmpStr + records[i][3].strip()  +splitStr
            #���
            tmpStr = tmpStr + records[i][4].strip()  +splitStr
            #��������
            tmpStr = tmpStr + "01|\n"
            f.write( tmpStr )
        f.close()
    else:
        logger.info( "������������ͨ������ִ�ļ�(�޼�¼)" )
        f.close()
    f.close()
    logger.info( "������������ͨ������ִ�ļ�" )
    return 0
################################################################################
#           ����ͨ.��������
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
#           ����ͨ.��������
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
#           ����ͨ.��������
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
    
    
################################################################################
#           ��������.���ɻ��ܱ���
# ��    �ܣ���������ͨ����
# ����˵����
# ��    ����
# 
################################################################################
def CreatTotalReport(logger):
    try:
        resulBrno = None
        i = 0
        splitStr = "|"
        tmpStr = ""

        #����ǲ�ѯ��һҳ�����ݣ�����ӡ�ļ�����
        if( TradeContext.I1STAR == "1" ):
            TradeContext.PBDAFILE = TradeContext.workDate+"_"+TradeContext.brno+"_"+TradeContext.tellerno+"_"+TradeContext.reportType+".txt"
            PfileName = os.environ['HOME']+"/afa/data/ybt/report/P_"+TradeContext.PBDAFILE
            TradeContext.P_PBDAFILE = "P_" + TradeContext.PBDAFILE
            logger.info ( " ��ӡ�ļ�·������  "+PfileName)
            try:
                Pf = file(PfileName,"w")
            except:
                logger.info("���ɴ�ӡ�ļ�["+PfileName+"]ʧ��")
                TradeContext.errorCode = "0001"
                TradeContext.errorMsg = "���ɴ�ӡ�ļ�["+PfileName+"]ʧ��"
                return -2
            
            logger.info ( " ��ʼ��������ͨ�ܱ����ļ�������Ϊ["+TradeContext.startdate+">>>>>"+TradeContext.enddate+"]" )
            
            sqlcount = "select brno,salerno,unitno,productid,count(*),sum(cast(amount as decimal(15,2))) from (select "
            if ( len(str(TradeContext.instno.strip()))>0):
                sqlcount = sqlcount + " brno,"
            else:
                sqlcount = sqlcount + " '' as brno,"
            if ( len(str(TradeContext.salerno.strip()))>0):
                sqlcount = sqlcount + "  trim(substr(note6,1,abs((locate('|',note6,1)-1)))) as salerno,"
            else:
                sqlcount = sqlcount + " '' as salerno,"
            if ( len(str(TradeContext.insuid.strip()))>0):
                sqlcount = sqlcount + " unitno,"
            else:
                sqlcount = sqlcount + " '' as unitno,"
            if ( len(str(TradeContext.productid.strip()))>0):
                sqlcount = sqlcount + " trim(substr(note8,1,abs((locate('|',note8,1)-1)))) as productid,"
            else:
                sqlcount = sqlcount + " '' as productid,"
            sqlcount=sqlcount+"amount from afa_maintransdtl"
            sqlcount = sqlcount + " where sysid = '"+TradeContext.sysId+"' and workdate >= '"+TradeContext.startdate+"' and workdate <= '"+TradeContext.enddate+"'"
            if ( TradeContext.sbgd=='02' and TradeContext.USGD=="20"):
                #ʡ�������ܿ��Բ�ѯ����ҵ��
                if( len(str(TradeContext.instno.strip()))>0):
                    sqlcount = sqlcount + " and brno='"+TradeContext.instno+"'"
            elif ( TradeContext.sbgd=='33' and TradeContext.USGD=="20"):
                #������񲿿��Բ�ѯ������
                if( len(str(TradeContext.instno.strip()))>0):
                    sqlcount = sqlcount + " and brno='"+TradeContext.instno+"'"
                else:
                    sqlcount = sqlcount + " and brno like '"+TradeContext.brno[0:6]+"%'"
            elif ( TradeContext.sbgd!='02' and TradeContext.sbgd!='33' and TradeContext.USGD=="20"):
                #���������ܿɲ�ѯ����������ҵ��
                sqlcount = sqlcount + " and brno='"+TradeContext.brno+"'"
            else:
                sqlcount = sqlcount + " and brno='"+TradeContext.brno+"'"
                sqlcount = sqlcount + " and tellerno ='"+TradeContext.tellerno+"'"
            if ( len(str(TradeContext.salerno.strip()))>0):
                sqlcount = sqlcount + " and trim(substr(note6,1,abs((locate('|',note6,1)-1))))='"+TradeContext.salerno+"'"
            if ( len(str(TradeContext.insuid.strip()))>0):
                sqlcount = sqlcount + " and unitno='"+TradeContext.insuid+"'"
            if ( len(str(TradeContext.productid.strip()))>0):
                sqlcount = sqlcount + " and trim(substr(note8,1,abs((locate('|',note8,1)-1))))='"+TradeContext.productid+"'"
            if ( TradeContext.startdate == TradeContext.workDate ):
                 sqlcount = sqlcount + "and chkflag = '9' and corpstatus='0'"
            else:
                 sqlcount = sqlcount + "and chkflag = '0' "
            sqlcount = sqlcount + " and bankstatus = '0' and revtranf = '0' "
            sqlcount = sqlcount + " ) t1 group by brno,salerno,unitno,productid"
                                 
            logger.info( "��ѯ���Ϊ:"+str(sqlcount))
            resulBrno = AfaDBFunc.SelectSql(sqlcount)
            logger.info( "��ѯ���:"+str(len(resulBrno)) )
            
            if resulBrno is None:
                logger.info("��ѯ����ͨ����:���ݿ�����쳣"+sqlcount)
                TradeContext.errorCode = "0001"
                TradeContext.errorMsg = "��ѯ�����:���ݿ�����쳣"+sqlcount
                return -2
            elif ( len(resulBrno) == 0 ):
                TradeContext.errorCode = "0001"
                TradeContext.errorMsg = "δ��ѯ����صĽ��׼�¼"
                return -3
            else:
                TradeContext.RecAllCount = str(len(resulBrno))
            
            tmpStr = "".ljust(40) + "�����ջ��ܱ�\n"
            tmpStr = tmpStr + "      ��ʼ����:  " + TradeContext.startdate + "                                 ��ֹ����:" + TradeContext.workDate + "\n"
            tmpStr = tmpStr + "".ljust(132,"=") + "\n"
            tmpStr = tmpStr + "      ������      Ӫ��ԱԱ����  ���չ�˾                ����                          ����   ���ս��        \n"
            Pf.write(tmpStr)
            
            for i in range( 0, len(resulBrno) ):
                tmpStr = "      "
                tmpStr = tmpStr + str(resulBrno[i][0]).ljust(12,' ')      																	#������
                tmpStr = tmpStr + str(resulBrno[i][1]).ljust(14,' ')      																	#Ӫ��ԱԱ����
                tmpStr = tmpStr + getUnitName(TradeContext.sysId,str(resulBrno[i][2])).ljust(24,' ')      	#���չ�˾����
                tmpStr = tmpStr + str(resulBrno[i][3]).ljust(30,' ')      																	#��������
                tmpStr = tmpStr + str(resulBrno[i][4]).ljust(7,' ')       																	#����
                tmpStr = tmpStr + str(resulBrno[i][5]).ljust(14,' ')     																		#���ս��
                tmpStr = tmpStr + "\n"
                logger.info("��ѯ����tmpStr["+str(i)+"]:"+str(tmpStr))
                Pf.write(tmpStr)
            
            #��ӡ�ļ����
            tmpStr = ""
            tmpStr = "\n" + "".ljust(6) + "�Ʊ�:" + TradeContext.tellerno + "\n"
            Pf.write(tmpStr)
            Pf.close()
             
        #���ز�ѯ��¼
        sqlcount = "select * from (select brno,salerno,unitno,productid,tnum,tamount,rownumber() OVER () AS rn from (select brno,salerno,unitno,productid,count(*) as tnum,sum(cast(amount as decimal(15,2))) as tamount"
        sqlcount = sqlcount + " from (select "
        if ( len(str(TradeContext.instno.strip()))>0):
            sqlcount = sqlcount + " brno,"
        else:
            sqlcount = sqlcount + " '' as brno,"
        if ( len(str(TradeContext.salerno.strip()))>0):
            sqlcount = sqlcount + "  trim(substr(note6,1,abs((locate('|',note6,1)-1)))) as salerno,"
        else:
            sqlcount = sqlcount + " '' as salerno,"
        if ( len(str(TradeContext.insuid.strip()))>0):
            sqlcount = sqlcount + " unitno,"
        else:
            sqlcount = sqlcount + " '' as unitno,"
        if ( len(str(TradeContext.productid.strip()))>0):
            sqlcount = sqlcount + " trim(substr(note8,1,abs((locate('|',note8,1)-1)))) as productid,"
        else:
            sqlcount = sqlcount + " '' as productid,"
        sqlcount=sqlcount+"amount from afa_maintransdtl"
        sqlcount = sqlcount + " where sysid = '"+TradeContext.sysId+"' and workdate >= '"+TradeContext.startdate+"' and workdate <= '"+TradeContext.enddate+"'"
        if ( TradeContext.sbgd=='02' and TradeContext.USGD=="20"):
            #ʡ�������ܿ��Բ�ѯ����ҵ��
            if( len(str(TradeContext.instno.strip()))>0):
                sqlcount = sqlcount + " and brno='"+TradeContext.instno+"'"
        elif ( TradeContext.sbgd=='33' and TradeContext.USGD=="20"):
            #������񲿿��Բ�ѯ������
            if( len(str(TradeContext.instno.strip()))>0):
                sqlcount = sqlcount + " and brno='"+TradeContext.instno+"'"
            else:
                sqlcount = sqlcount + " and brno like '"+TradeContext.brno[0:6]+"%'"
        elif ( TradeContext.sbgd!='02' and TradeContext.sbgd!='33' and TradeContext.USGD=="20"):
                #���������ܿɲ�ѯ����������ҵ��
            sqlcount = sqlcount + " and brno='"+TradeContext.brno+"'"
        else:
            sqlcount = sqlcount + " and brno='"+TradeContext.brno+"'"
            sqlcount = sqlcount + " and tellerno ='"+TradeContext.tellerno+"'"
        if ( len(str(TradeContext.salerno.strip()))>0):
            sqlcount = sqlcount + " and trim(substr(note6,1,abs((locate('|',note6,1)-1))))='"+TradeContext.salerno+"'"
        if ( len(str(TradeContext.insuid.strip()))>0):
            sqlcount = sqlcount + " and unitno='"+TradeContext.insuid+"'"
        if ( len(str(TradeContext.productid.strip()))>0):
            sqlcount = sqlcount + " and trim(substr(note8,1,abs((locate('|',note8,1)-1))))='"+TradeContext.productid+"'"
        if ( TradeContext.startdate == TradeContext.workDate ):
            sqlcount = sqlcount + "and chkflag = '9' and corpstatus='0'"
        else:
            sqlcount = sqlcount + "and chkflag = '0' "
        sqlcount = sqlcount + " and bankstatus = '0' and revtranf = '0' "
        sqlcount = sqlcount + " ) t1 group by brno,salerno,unitno,productid) a ) b where b.rn between "+TradeContext.I1STAR+" and "+str(int(TradeContext.I1STAR)+int(TradeContext.I1RCNM)-1)
        
        logger.info( "��ѯ���Ϊ:"+str(sqlcount))
        resulBrno = AfaDBFunc.SelectSql(sqlcount)
        logger.info( "��ѯ���:"+str(len(resulBrno)) )
        
        if resulBrno is None:
            logger.info("��ѯ����ͨ����:���ݿ�����쳣"+sqlcount)
            TradeContext.errorCode = "0001"
            TradeContext.errorMsg = "��ѯ�����:���ݿ�����쳣"+sqlcount
            return -2
        elif ( len(resulBrno) == 0 ):
            TradeContext.errorCode = "0000"
            TradeContext.errorMsg = "δ��ѯ����صĽ��׼�¼"
            return -3
        else:
            TradeContext.RecAllCount = str(len(resulBrno))
            
        INSTNO = []
        SALERNO = []
        INSUID = []
        PRODUCTID = []
        NUM = []
        AMOUNT = []        
        for i in range( 0, len(resulBrno) ):
            INSTNO.append(str(resulBrno[i][0]))
            SALERNO.append(str(resulBrno[i][1]))
            INSUID.append(getUnitName(TradeContext.sysId,str(resulBrno[i][2])))
            PRODUCTID.append(str(resulBrno[i][3]))
            NUM.append(str(resulBrno[i][4]))
            AMOUNT.append(str(resulBrno[i][5]))
            
        TradeContext.INSTNO = INSTNO
        TradeContext.SALERNO = SALERNO
        TradeContext.INSUID = INSUID
        TradeContext.PRODUCTID = PRODUCTID
        TradeContext.NUM = NUM
        TradeContext.AMOUNT = AMOUNT
        TradeContext.O1ACUR = TradeContext.RecAllCount
              
        return 0
    except Exception ,e:
        TradeContext.errorCode = "0001"
        TradeContext.errorMsg = "����ͨ��ϸ��ѯ���� ["+str(e)+"]"
        logger.info("����ͨ��ϸ��ѯ���� ["+str(e)+"]")
        return -3



################################################################################
#           ��������.������ϸ����
# ��    �ܣ���������ͨ��ϸ����
# ����˵����
# ��    ����
# 
################################################################################
def CreatDetailReport(logger):
    try:
        resulBrno = None
        i = 0
        splitStr = "|"
        tmpStr = ""
        
        #����ǲ�ѯ��һҳ�����ݣ�����ӡ�ļ�����
        if( TradeContext.I1STAR == "1" ):
            logger.info ( " ��ʼ��������ͨ��ϸ�����ļ�������Ϊ["+TradeContext.startdate+">>>>>"+TradeContext.enddate+"]" )
            #��ӡ�ļ�
            TradeContext.PBDAFILE = TradeContext.workDate+"_"+TradeContext.brno+"_"+TradeContext.tellerno+"_"+TradeContext.reportType+".txt"
            PfileName = os.environ['HOME']+"/afa/data/ybt/report/P_"+TradeContext.PBDAFILE
            TradeContext.P_PBDAFILE = "P_" + TradeContext.PBDAFILE
            logger.info ( " ��ӡ�ļ�·������  "+PfileName)
            try:
                Pf = file(PfileName,"w")
            except:
                logger.info("���ɴ�ӡ�ļ�["+PfileName+"]ʧ��")
                TradeContext.errorCode = "0001"
                TradeContext.errorMsg = "���ɴ�ӡ�ļ�["+PfileName+"]ʧ��"
                return -2
            
            sqlcount = "select brno,unitno,workdate,note8,bankserno,agentserialno,note9,userno,note4,cast(amount as decimal(15,2)) as amount from afa_maintransdtl"
            sqlcount = sqlcount + " where sysid = '"+TradeContext.sysId+"' and workdate >= '"+TradeContext.startdate+"' and workdate <= '"+TradeContext.enddate+"'"
            if ( TradeContext.sbgd=='02' and TradeContext.USGD=="20"):
                #ʡ�������ܿ��Բ�ѯ����ҵ��
                if( len(str(TradeContext.INSTNO.strip()))>0):
                    sqlcount = sqlcount + " and brno='"+TradeContext.INSTNO+"'"
            elif ( TradeContext.sbgd=='33' and TradeContext.USGD=="20"):
                #������񲿿��Բ�ѯ������
                if( len(str(TradeContext.INSTNO.strip()))>0):
                    sqlcount = sqlcount + " and brno='"+TradeContext.INSTNO+"'"
                else:
                    sqlcount = sqlcount + " and brno like '"+TradeContext.brno[0:6]+"%'"
            elif ( TradeContext.sbgd!='02' and TradeContext.sbgd!='33' and TradeContext.USGD=="20"):
                #���������ܿɲ�ѯ����������ҵ��
                sqlcount = sqlcount + " and brno='"+TradeContext.brno+"'"
            else:
                sqlcount = sqlcount + " and brno='"+TradeContext.brno+"'"
                sqlcount = sqlcount + " and tellerno ='"+TradeContext.tellerno+"'"
            if ( len(str(TradeContext.insuid.strip()))>0):                                                            
                sqlcount = sqlcount + " and unitno='"+TradeContext.insuid+"'"
            if ( len(str(TradeContext.productid.strip()))>0):                                                         
                sqlcount = sqlcount + " and note8 like '"+TradeContext.productid+"|%|%|%|'" 
            if ( len(str(TradeContext.TRANSRNO.strip()))>0):                                                          
                sqlcount = sqlcount + " and agentserialno='"+TradeContext.TRANSRNO+"'"
            if ( len(str(TradeContext.PAYACC.strip()))>0):                                                            
                sqlcount = sqlcount + " and draccno='"+TradeContext.PAYACC+"'" 
            if ( len(str(TradeContext.PAYCARD.strip()))>0):                                                           
                sqlcount = sqlcount + " and craccno='"+TradeContext.PAYCARD+"'"                                       
            if ( len(str(TradeContext.APPLNO.strip()))>0):                                                            
                sqlcount = sqlcount + " and note9 like '%|"+TradeContext.APPLNO+"|%|%'"                               
            if ( len(str(TradeContext.TBR_NAME.strip()))>0):                                                          
                sqlcount = sqlcount + " and note4 like '"+TradeContext.TBR_NAME+"|%|'"                                
            if ( str(TradeContext.PREMIUM.strip())!='0.00'):                                                          
                sqlcount = sqlcount + " and amount ='"+TradeContext.PREMIUM+"'"                                       
            if ( len(str(TradeContext.salerno.strip()))>0):                                                           
                sqlcount = sqlcount + " and trim(left(note6,abs((locate('|',note6,1)-1))))='"+TradeContext.salerno+"'"
            if ( TradeContext.startdate == TradeContext.workDate ):
                 sqlcount = sqlcount + " and chkflag = '9' and corpstatus='0'"
            else:
                 sqlcount = sqlcount + " and chkflag = '0' "
            sqlcount = sqlcount + " and bankstatus = '0' and revtranf = '0' "
            sqlcount = sqlcount + " order by agentserialno,workdate"
                   
            logger.info( "��ѯ���Ϊ:"+str(sqlcount) )
            resulBrno = AfaDBFunc.SelectSql(sqlcount)
            logger.info( "��ѯ���:"+str(len(resulBrno)) )
            
            if resulBrno is None:
                logger.info("��ѯ����ͨ����:���ݿ�����쳣"+sqlcount)
                TradeContext.errorCode = "0001"
                TradeContext.errorMsg = "��ѯ����ͨ����:���ݿ�����쳣"+sqlcount
                return -2
            elif ( len(resulBrno) == 0 ):
                TradeContext.errorCode = "0000"
                TradeContext.errorMsg = "δ��ѯ����صĽ��׼�¼"
                return -3
            else:
                TradeContext.O1ACUR = str(len(resulBrno))
            
            tmpStr = "".ljust(40) + "��������ϸ��\n"
            tmpStr = tmpStr + "      ��ʼ����:  " + TradeContext.startdate + "                                 ��ֹ����:" + TradeContext.workDate + "\n"
            tmpStr = tmpStr + "".ljust(110,"=") + "\n"
            tmpStr = tmpStr + "��������   ���չ�˾   �������� ����      ������ˮ ������                     ����ӡˢ�� �ͻ����� ���ѽ��     \n"
            Pf.write(tmpStr)
            
            for i in range( 0, len(resulBrno) ):
                tmpStr = ""
                tmpStr = tmpStr + str(resulBrno[i][0]).ljust(11,' ')     		        														#������
                tmpStr = tmpStr + getUnitName(TradeContext.sysId,str(resulBrno[i][1])).ljust(11,' ')      			#���չ�˾
                tmpStr = tmpStr + str(resulBrno[i][2]).ljust(9,' ')      																			#��������
                if (len(resulBrno[i][3].split('|'))>1):
                    tmpStr = tmpStr + str(resulBrno[i][3].split('|')[0]).ljust(10,' ')       										#��������
                else:
                    tmpStr = tmpStr + "".ljust(10,' ')
                #tmpStr = tmpStr + str(resulBrno[i][4]).ljust(11,' ')      																			#������ˮ
                tmpStr = tmpStr + str(resulBrno[i][5]).ljust(9,' ')       																			#������ˮ
                if (len(resulBrno[i][6].split('|'))>1):
                    tmpStr = tmpStr + str(resulBrno[i][6].split('|')[2]).ljust(27,' ')      										#������
                else:
                    tmpStr = tmpStr + "".ljust(26,' ')
                tmpStr = tmpStr + str(resulBrno[i][7]).ljust(11,' ')      																			#����ӡˢ��
                if (len(resulBrno[i][8].split('|'))>1):
                    tmpStr = tmpStr + str(resulBrno[i][8]).split('|')[0].ljust(9,' ')      										#�ͻ�����
                else:
                    tmpStr = tmpStr + "".ljust(9,' ')    
                tmpStr = tmpStr + str(resulBrno[i][9]).ljust(13,' ')      																			#���ѽ��
                tmpStr = tmpStr + "\n"
                logger.info("��ѯ��ϸtmpStr["+str(i)+"]:"+str(tmpStr))
                Pf.write(tmpStr)
            
            #��ѯ�ϼƽ��
            sql="select sum(amount) from ("+sqlcount+") as t1"
            logger.info( "��ѯ���Ϊ:"+str(sql) )
            resulBrno = AfaDBFunc.SelectSql(sql)
            logger.info( "��ѯ���:"+str(resulBrno) )
            
            if resulBrno is None:
                logger.info("��ѯ����ͨ����:���ݿ�����쳣"+sqlcount)
                TradeContext.errorCode = "0001"
                TradeContext.errorMsg = "��ѯ����ͨ����:���ݿ�����쳣"+sqlcount
                return -2
            elif ( len(resulBrno) == 0 ):
                TradeContext.errorCode = "0000"
                TradeContext.errorMsg = "δ��ѯ����صĽ��׼�¼"
                return -3
            else:
                totalamount = str(resulBrno[0][0])
            #��ӡ�ļ����
            tmpStr = "\n"+"".ljust(87,' ')+"�ϼƽ�"+totalamount
            tmpStr = tmpStr+"\n" + "".ljust(6) + "�Ʊ�:" + TradeContext.tellerno + "\n"
            Pf.write(tmpStr)
            Pf.close()
        
        #���ز�ѯ��¼
        sqlcount = "select * from (select brno,unitno,workdate,note8,bankserno,agentserialno,note9,userno,note4,cast(amount as decimal(15,2)) as amount,rownumber() OVER (ORDER BY agentserialno,workdate ASC) AS rn from afa_maintransdtl"
        sqlcount = sqlcount + " where sysid = '"+TradeContext.sysId+"' and workdate >= '"+TradeContext.startdate+"' and workdate <= '"+TradeContext.enddate+"'"
        if ( TradeContext.sbgd=='02' and TradeContext.USGD=="20"):
            #ʡ�������ܿ��Բ�ѯ����ҵ��
            if( len(str(TradeContext.INSTNO.strip()))>0):
                sqlcount = sqlcount + " and brno='"+TradeContext.INSTNO+"'"
        elif ( TradeContext.sbgd=='33' and TradeContext.USGD=="20"):
            #������񲿿��Բ�ѯ������
            if( len(str(TradeContext.INSTNO.strip()))>0):
                sqlcount = sqlcount + " and brno='"+TradeContext.INSTNO+"'"
            else:
                sqlcount = sqlcount + " and brno like '"+TradeContext.brno[0:6]+"%'"
        elif ( TradeContext.sbgd!='02' and TradeContext.sbgd!='33' and TradeContext.USGD=="20"):
            #���������ܿɲ�ѯ����������ҵ��
            sqlcount = sqlcount + " and brno='"+TradeContext.brno+"'"
        else:
            sqlcount = sqlcount + " and brno='"+TradeContext.brno+"'"
            sqlcount = sqlcount + " and tellerno ='"+TradeContext.tellerno+"'"
        if ( len(str(TradeContext.insuid.strip()))>0):
            sqlcount = sqlcount + " and unitno='"+TradeContext.insuid+"'"
        if ( len(str(TradeContext.productid.strip()))>0):
            sqlcount = sqlcount + " and note8 like '"+TradeContext.productid+"|%|%|%|'"
        if ( len(str(TradeContext.TRANSRNO.strip()))>0):
            sqlcount = sqlcount + " and agentserialno='"+TradeContext.TRANSRNO+"'"
        if ( len(str(TradeContext.PAYACC.strip()))>0):
            sqlcount = sqlcount + " and draccno='"+TradeContext.PAYACC+"'"
        if ( len(str(TradeContext.PAYCARD.strip()))>0):
            sqlcount = sqlcount + " and craccno='"+TradeContext.PAYCARD+"'"
        if ( len(str(TradeContext.APPLNO.strip()))>0):
            sqlcount = sqlcount + " and note9 like '%|"+TradeContext.APPLNO+"|%|%'"
        if ( len(str(TradeContext.TBR_NAME.strip()))>0):
            sqlcount = sqlcount + " and note4 like '"+TradeContext.TBR_NAME+"|%|'"
        if ( str(TradeContext.PREMIUM.strip())!='0.00'):
            sqlcount = sqlcount + " and amount ='"+TradeContext.PREMIUM+"'"
        if ( len(str(TradeContext.salerno.strip()))>0):
            sqlcount = sqlcount + " and trim(left(note6,abs((locate('|',note6,1)-1))))='"+TradeContext.salerno+"'"
        if ( TradeContext.startdate == TradeContext.workDate ):
            sqlcount = sqlcount + " and chkflag = '9' and corpstatus='0'"
        else:
            sqlcount = sqlcount + " and chkflag = '0' "
        sqlcount = sqlcount + " and bankstatus = '0' and revtranf = '0' "
        sqlcount = sqlcount + " ) a where a.rn between "+TradeContext.I1STAR+" and "+str(int(TradeContext.I1STAR)+int(TradeContext.I1RCNM)-1)
        
        logger.info( "��ѯ���Ϊ:"+str(sqlcount) )
        resulBrno = AfaDBFunc.SelectSql(sqlcount)
        logger.info( "��ѯ���:"+str(resulBrno) )
        
        if resulBrno is None:
            logger.info("��ѯ����ͨ����:���ݿ�����쳣"+sqlcount)
            TradeContext.errorCode = "0001"
            TradeContext.errorMsg = "��ѯ�����:���ݿ�����쳣"+sqlcount
            return -2
        elif ( len(resulBrno) == 0 ):
            TradeContext.errorCode = "0000"
            TradeContext.errorMsg = "δ��ѯ����صĽ��׼�¼"
            return -3
        else:
            TradeContext.O1ACUR = str(len(resulBrno)) 
        
        INSTNO = []
        INSUID = []
        TRANDATE = []
        PRODUCTID =[]
        ACCSRNO = []
        TRANSRNO =[]
        POLICY=[]
        BD_PRINT_NO =[] 
        TBR_NAME = []
        PREMIUM=[]
        for i in range( 0, len(resulBrno) ):
            INSTNO.append(str(resulBrno[i][0]))
            INSUID.append(getUnitName(TradeContext.sysId,str(resulBrno[i][1])))
            TRANDATE.append(str(resulBrno[i][2]))
            if (len(resulBrno[i][3].split('|'))>1):
                PRODUCTID.append(str(resulBrno[i][3].split('|')[0]))
            else:
                PRODUCTID.append("")
            ACCSRNO.append(str(resulBrno[i][4]))
            TRANSRNO.append(str(resulBrno[i][5]))
            if (len(resulBrno[i][6].split('|'))>1):
                POLICY.append(str(resulBrno[i][6].split('|')[2]))
            else:
                POLICY.append("")
            BD_PRINT_NO.append(str(resulBrno[i][7]))
            if (len(resulBrno[i][8].split('|'))>1):
                TBR_NAME.append(str(resulBrno[i][8]).split('|')[0])
            else:
                TBR_NAME.append("")
            PREMIUM.append(str(resulBrno[i][9]))
        
        TradeContext.INSTNO = INSTNO
        TradeContext.INSUID = INSUID
        TradeContext.TRANDATE = TRANDATE
        TradeContext.PRODUCTID = PRODUCTID
        TradeContext.ACCSRNO = ACCSRNO
        TradeContext.TRANSRNO = TRANSRNO
        TradeContext.POLICY = POLICY
        TradeContext.BD_PRINT_NO=BD_PRINT_NO
        TradeContext.TBR_NAME=TBR_NAME
        TradeContext.PREMIUM = PREMIUM
        
        return 0
    except Exception ,e:
        TradeContext.errorCode = "0001"
        TradeContext.errorMsg = "��������ͨ������� ["+str(e)+"]"
        logger.info("��������ͨ������� ["+str(e)+"]")
        return -3



################################################################################     
 #  ����ͨ�������� swap()                                                   
 # ��    �ܣ�ת����ͬ���չ�˾������                                                      
 # ����˵����                                                                         
 # ��    ����                                                                         
 #                                                                                    
 ################################################################################ 
def swap( ):                                                                         
                                                                                    
    filename = '/home/maps/afa/application/ybt/config/busino_' + TradeContext.unitno + '.conf'    #�����ļ���
    AfaLoggerFunc.tradeInfo('�ļ�����' + filename)
    
    sexType   = 'sexType'                                                                      #sexType:�����ļ����Ա�ѡ��
    idType    = 'idType'                                                                       #֤������ 
    tormType  = 'tormType'                                                                     #�����ڼ�����   
    payMethod = 'payMethod'                                                                    #�ɷѷ�ʽ
    Rela      = 'Rela'                                                                         #��ϵ
    workType  = 'workType'                                                                     #ְҵ���          
    
    #ת���Ա�����
    if (TradeContext.existVariable( "tbr_sex" ) and len(TradeContext.tbr_sex.strip()) > 0 ):                                                                     
        AfaLoggerFunc.tradeInfo("ӳ��ǰ���Ա�"+ TradeContext.tbr_sex  )
        TradeContext.pre_tbr_sex = TradeContext.tbr_sex
        if not datamap(sexType,TradeContext.tbr_sex,filename):                                           
            TradeContext.errorCode = 'E9999'                                               
            TradeContext.errorMsg  = '�ñ��չ�˾�����ڸ����Ա�ѡ�����¼����'                     
            return False                                                    
        else:                                                                         
            TradeContext.tbr_sex = datamap(sexType,TradeContext.tbr_sex,filename)
    else:
         TradeContext.tbr_sex=''
    AfaLoggerFunc.tradeInfo("ӳ�����Ա�"+ TradeContext.tbr_sex )
         
    #ת��֤������
    #Ͷ����֤������
    if (TradeContext.existVariable( "tbr_idtype" ) and len(TradeContext.tbr_idtype.strip()) > 0 ):                                                                     
        AfaLoggerFunc.tradeInfo("ӳ��ǰ��Ͷ����֤�����ͣ�"+ TradeContext.tbr_idtype )
        TradeContext.pre_tbr_idtype = TradeContext.tbr_idtype
        if not datamap(idType,TradeContext.tbr_idtype,filename):                                           
            TradeContext.errorCode = 'E9999'                                               
            TradeContext.errorMsg  = '�ñ��չ�˾�����ڸ���Ͷ����֤������ѡ�����¼����'                     
            raise AfaFlowControl.flowException()                                                              
        else:                                                                         
            TradeContext.tbr_idtype = datamap(idType,TradeContext.tbr_idtype,filename)
    else:
         TradeContext.tbr_idtype='' 
    AfaLoggerFunc.tradeInfo("ӳ����Ͷ����֤�����ͣ�"+ TradeContext.tbr_idtype )
    
    
    
    #������֤������ 
    if (TradeContext.existVariable( "bbr_idtype" ) and len(TradeContext.bbr_idtype.strip()) > 0 ):                                                                     
        AfaLoggerFunc.tradeInfo("ӳ��ǰ�ı�����֤�����ͣ�"+ TradeContext.bbr_idtype )
        TradeContext.pre_bbr_idtype = TradeContext.bbr_idtype  
        if not datamap(idType,TradeContext.bbr_idtype,filename):                                           
            TradeContext.errorCode = 'E9999'                                               
            TradeContext.errorMsg  = '�ñ��չ�˾�����ڸ��ֱ���������ѡ�����¼����'                     
            raise AfaFlowControl.flowException()                                                              
        else:                                                                         
            TradeContext.bbr_idtype = datamap(idType,TradeContext.bbr_idtype,filename)
    else:
         TradeContext.bbr_idtype=''
    AfaLoggerFunc.tradeInfo("ӳ���ı�����֤�����ͣ�"+ TradeContext.bbr_idtype ) 
    
    
    #������֤������
    if (TradeContext.existVariable( "syr_idtype" )): 
        TradeContext.pre_syr_idtype = TradeContext.syr_idtype
        for i in range(0,len(TradeContext.syr_idtype)):
            if len(TradeContext.syr_idtype[i].strip()) > 0:
                AfaLoggerFunc.tradeInfo("ӳ��ǰ��������֤�����ͣ�"+ TradeContext.syr_idtype[i] ) 
                if not datamap(idType,TradeContext.syr_idtype[i],filename):                                           
                    TradeContext.errorCode = 'E9999'                                               
                    TradeContext.errorMsg  = '�ñ��չ�˾�����ڸ���������֤������ѡ�����¼����'                     
                    raise AfaFlowControl.flowException()                                                            
                else:                                                                         
                    TradeContext.syr_idtype[i] = datamap(idType,TradeContext.syr_idtype[i],filename)
                AfaLoggerFunc.tradeInfo("ӳ����������֤�����ͣ�"+ TradeContext.syr_idtype[i] )
    else:
         TradeContext.syr_idtype='' 
        
  
   
    #�����ڼ����� 
    if (TradeContext.existVariable( "tormtype" ) and len(TradeContext.tormtype.strip()) > 0 ):
        TradeContext.pre_tormtype = TradeContext.tormtype
        AfaLoggerFunc.tradeInfo("ӳ��ǰ�ı����ڼ����ͣ�"+ TradeContext.tormtype ) 
        if not datamap(tormType,TradeContext.tormtype,filename):                                           
            TradeContext.errorCode = 'E9999'                                               
            TradeContext.errorMsg  = '�ñ��չ�˾�����ڸ��ֱ����ڼ�����ѡ�����¼����'                     
            raise AfaFlowControl.flowException()                                                              
        else:                                                                         
            TradeContext.tormtype = datamap(tormType,TradeContext.tormtype,filename)
    else:
         TradeContext.tormtype=''  
    AfaLoggerFunc.tradeInfo("ӳ���ı����ڼ����ͣ�"+ TradeContext.tormtype )    
    
    
    #�ɷѷ�ʽ
    if (TradeContext.existVariable( "paymethod" ) and len(TradeContext.paymethod.strip()) > 0 ):
        TradeContext.pre_paymethod = TradeContext.paymethod
        AfaLoggerFunc.tradeInfo("ӳ��ǰ�Ľɷѷ�ʽ��"+ TradeContext.pre_paymethod )
        if not datamap(payMethod,TradeContext.paymethod,filename):                                           
            TradeContext.errorCode = 'E9999'                                               
            TradeContext.errorMsg  = '�ñ��չ�˾�����ڸ��ֽɷѷ�ʽѡ�����¼����'                     
            raise AfaFlowControl.flowException()                                                             
        else:                                                                         
            TradeContext.paymethod = datamap(payMethod,TradeContext.paymethod,filename)
    else:
         TradeContext.paymethod=''
   
    AfaLoggerFunc.tradeInfo("ӳ���Ľɷѷ�ʽ��"+ TradeContext.paymethod )
   
   
    #��ϵ
    #��Ͷ���˹�ϵ 
    if (TradeContext.existVariable( "tbr_bbr_rela" ) and len(TradeContext.tbr_bbr_rela.strip()) > 0 ): 
        TradeContext.pre_tbr_bbr_rela = TradeContext.tbr_bbr_rela
        AfaLoggerFunc.tradeInfo("ӳ��ǰ����Ͷ���˹�ϵ>>>>>>>>>>>>>>��"+ TradeContext.pre_tbr_bbr_rela )
        AfaLoggerFunc.tradeInfo("ӳ��ǰ����Ͷ���˹�ϵ��"+ TradeContext.tbr_bbr_rela )
        if not datamap(Rela,TradeContext.tbr_bbr_rela,filename):                                           
            TradeContext.errorCode = 'E9999'                                               
            TradeContext.errorMsg  = '�ñ��չ�˾�����ڸ���Ͷ�����뱻���˹�ϵѡ�����¼����'                     
            raise AfaFlowControl.flowException()                                                             
        else:                                                                         
            TradeContext.tbr_bbr_rela = datamap(Rela,TradeContext.tbr_bbr_rela,filename)
    else:
         TradeContext.tbr_bbr_rela=''       
    AfaLoggerFunc.tradeInfo("ӳ������Ͷ���˹�ϵ��"+ TradeContext.tbr_bbr_rela )
    
    
    #�������˹�ϵ 
    if (TradeContext.existVariable( "syr_bbr_rela" ) ): 
        TradeContext.pre_syr_bbr_rela = TradeContext.syr_bbr_rela
        for i in range(0,len(TradeContext.syr_bbr_rela)):
            if len(TradeContext.syr_bbr_rela[i].strip()) > 0:
                AfaLoggerFunc.tradeInfo("ӳ��ǰ���������˹�ϵ��"+ TradeContext.syr_bbr_rela[i] + '��' + str(i) + '��')
                if not datamap(Rela,TradeContext.syr_bbr_rela[i],filename):                                           
                    TradeContext.errorCode = 'E9999'                                               
                    TradeContext.errorMsg  = '�ñ��չ�˾�����ڸ����������뱻���˹�ϵѡ�����¼����'                     
                    raise AfaFlowControl.flowException()                                                              
                else:                                                                         
                    TradeContext.syr_bbr_rela[i] = datamap(Rela,TradeContext.syr_bbr_rela[i],filename)
                AfaLoggerFunc.tradeInfo("ӳ�����������˹�ϵ��"+ TradeContext.syr_bbr_rela[i] )  
    else:
         TradeContext.syr_bbr_rela=''
    
      
    
    #ְҵ
    if (TradeContext.existVariable( "bbr_worktype" ) and len(TradeContext.bbr_worktype.strip()) > 0 ):
        TradeContext.pre_bbr_worktype = TradeContext.bbr_worktype
        AfaLoggerFunc.tradeInfo("ӳ��ǰ��ְҵ��"+ TradeContext.bbr_worktype )
        if not datamap(workType,TradeContext.bbr_worktype,filename):                                           
            TradeContext.errorCode = 'E9999'                                               
            TradeContext.errorMsg  = '�ñ��չ�˾�����ڸ���ְҵ���ѡ�����¼����'                     
            raise AfaFlowControl.flowException()                                                              
        else:                                                                         
            TradeContext.bbr_worktype = datamap(workType,TradeContext.bbr_worktype,filename)
    else:
         TradeContext.bbr_worktype=''      
    AfaLoggerFunc.tradeInfo("ӳ����ְҵ��"+ TradeContext.bbr_worktype )
 
 
         
################################################################################     
# ����ͨ�������� datemap()                                                   
# ��    �ܣ�ת����ͬ���չ�˾������                                                      
# ����˵����                                                                         
# ��    ����                                                                         
#                                                                                    
################################################################################        
         
def datamap(var,option,filename):

    try:

        config = ConfigParser.ConfigParser( )
       
        config.readfp ( open( filename ) )
        var = config.get( var,option)
        
        return var

    except Exception, e:
        AfaLoggerFunc.tradeInfo("ת���쳣���쳣��Ϣ��"+ str(e) )
        TradeContext.errorCode = "E0001"
        TradeContext.errorMsg  = "ѡ��ӳ���������¼����"
        return False         

################################################################################     
# ����ͨ��������                                                    
# ��    �ܣ����ݱ��չ�˾�����ѯ���չ�˾����                                                      
# ����˵����                                                                         
# ��    ����                                                                         
#                                                                                    
################################################################################        
         
def getUnitName(sysid,unitno):
    sql="select unitsname from afa_unitadm where sysid='"+sysid+"' and unitno='"+unitno+"'"
    result = AfaDBFunc.SelectSql(sql)
    if result is None:
        TradeContext.errorCode = "0001"
        TradeContext.errorMsg = "��ѯ���չ�˾��Ϣ:���ݿ�����쳣"+sql
        return -2
    elif ( len(result) == 0 ):
        return str(unitno)
    else:
        return result[0][0]

################################################################################
# ����ͨ�ļ�����                                  
# ��    �ܣ����ݲ�ͬ�ı��չ�˾������Ӧ���ֽ��ֵ�ļ�                           
# ����˵����                                                                  
# ��    ����                                                                   
#                                                                              
################################################################################    
def createFile( ):
    
    TradeContext.cashFileName = TradeContext.brno + "_" + TradeContext.tellerno + "_" + TradeContext.unitno + "_cash.txt"
    fileName = os.environ['HOME'] + "/afa/data/ybt/cash/" + TradeContext.cashFileName
    
    #�����й������ֽ��ֵ�ļ�
    if TradeContext.unitno == '0001':
        return createZgrsFile( fileName )
        
    #����̫ƽ���ֽ��ֵ�ļ�
    elif TradeContext.unitno == '0002':
        return createCpicFile( fileName )
        
    #���ɻ����ֽ��ֵ�ļ�
    elif TradeContext.unitno == '0003':
        return createHXFile( fileName )
        
    #�����Ҹ������ֽ��ֵ�ļ�
    elif TradeContext.unitno =='0004':
        return createHappyFile( fileName )
        
    #����̩�������ֽ��ֵ�ļ�               
    elif TradeContext.unitno =='0005':      
        return createTaikangFile( fileName )
        
    #�����˱������ֽ��ֵ�ļ�               
    elif TradeContext.unitno =='0006':      
        return createRbsxFile( fileName ) 
    
    #�������������ֽ��ֵ�ļ�
    elif TradeContext.unitno =='0007':
        return createLifeFile( fileName )
        
    #�����˱������ֽ��ֵ�ļ�
    elif TradeContext.unitno =='0008':
        return createRbjkFile( fileName )
        
    else:
        TradeContext.errorCode = 'F001'
        TradeContext.errorMsg  = 'û�иñ��չ�˾���룬�����ֽ��ֵ�ļ�ʧ��'
        return False

################################################################################
# ����ͨ�ļ�����                                  
# ��    �ܣ�����̫ƽ���ֽ��ֵ�ļ�                           
# ����˵����                                                                  
# ��    ����                                                                   
#                                                                              
################################################################################            
def createCpicFile( fileName ):
    
    AfaLoggerFunc.tradeInfo( '̫ƽ��---��ʼ�����ֽ��ֵ��' + fileName + '��' )
    
    try:
        cashFile = file( fileName,"w" )
        
        tmpStr = ""
        #����ʵ����Ҫ�ȿճ�47��
        for i in range( 47 ):
            tmpStr = tmpStr + "\n"
        tmpStr = tmpStr + " ".ljust( 105,"-" ) +  " \n"
        tmpStr = tmpStr + " �����ֽ��ֵ��Ԫ/�ݣ�".ljust( 105,  " " ) + " \n"
        tmpStr = tmpStr + " ".ljust( 105,"-" ) +  " \n"
        tmpStr = tmpStr + " " + TradeContext.year1.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year2.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year3.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year4.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year5.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year6.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year7.ljust(14," ") + " \n"
        tmpStr = tmpStr + " ".ljust( 105,"-" ) +  " \n"
        tmpStr = tmpStr + " " + TradeContext.cash1.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash2.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash3.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash4.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash5.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash6.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash7.ljust(14," ") + " \n"
        tmpStr = tmpStr + " ".ljust( 105,"-" ) +  " \n"
        tmpStr = tmpStr + " " + TradeContext.year8.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year9.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year10.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year11.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year12.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year13.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year14.ljust(14," ") + " \n"
        tmpStr = tmpStr + " ".ljust( 105,"-" ) +  " \n"
        tmpStr = tmpStr + " " + TradeContext.cash8.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash9.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash10.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash11.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash12.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash13.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash14.ljust(14," ") + " \n"
        tmpStr = tmpStr + " ".ljust( 105,"-" ) +  " \n"
        
        cashFile.write( tmpStr )
        
        cashFile.close( )
        
        AfaLoggerFunc.tradeInfo( '̫ƽ��--�����ֽ��ֵ��ɹ�' )
        
        return True
        
    except Exception ,e:
        cashFile.close( )
        AfaLoggerFunc.tradeInfo( str(e) )
        TradeContext.errorCode = "F001"
        TradeContext.errorMsg  = "̫ƽ��--�����ֽ��ֵ��ʧ��"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        return False

################################################################################
# ����ͨ�ļ�����                                  
# ��    �ܣ������й������ֽ��ֵ�ļ�                           
# ����˵����                                                                  
# ��    ����                                                                   
#                                                                              
################################################################################            
def createZgrsFile( fileName ):
    
    AfaLoggerFunc.tradeInfo( '�й�����---��ʼ�����ֽ��ֵ��' + fileName + '��' )
    
    try:
        cashFile = file( fileName,"w" )
        
        tmpStr = ""
        #����ʵ����Ҫ���ȿճ�8��
        for i in range(0,8):
            tmpStr = tmpStr + "\n"
        tmpStr = tmpStr + "".ljust(37,' ') + "��    ��    ��    ֵ    ��\n\n"
        tmpStr = tmpStr + "".ljust(32,' ') + "���Ա���������ÿ1000Ԫ���շ�Ϊ��׼��\n\n"
        tmpStr = tmpStr + "".ljust(8,' ') + "�������ƣ�"
        tmpStr = tmpStr + TradeContext.productname.ljust(40,' ')
        tmpStr = tmpStr + "������ͬ�ţ�"
        tmpStr = tmpStr + TradeContext.policy.ljust(40,' ') + "\n\n"
        tmpStr = tmpStr + "".ljust(8,' ') + "�������ĩ".ljust(16,' ')
        tmpStr = tmpStr + "�ֽ��ֵ".ljust(16,' ')
        tmpStr = tmpStr + "�������ĩ".ljust(16,' ')
        tmpStr = tmpStr + "�ֽ��ֵ".ljust(16,' ')
        tmpStr = tmpStr + "�������ĩ".ljust(16,' ')
        tmpStr = tmpStr + "�ֽ��ֵ".ljust(16,' ') + "\n\n"
        tmpStr = tmpStr + "".ljust(8,' ')
        for i in range(0,int(TradeContext.cashnum)):
            tmpStr = tmpStr + TradeContext.year[i].ljust(16,' ')
            tmpStr = tmpStr + TradeContext.cash[i].ljust(16,' ')
            if i != 0 and (i+1)%3 == 0:
                tmpStr = tmpStr + "\n"
                tmpStr = tmpStr + "".ljust(8,' ')
        
        cashFile.write( tmpStr )
        
        cashFile.close( )
        
        AfaLoggerFunc.tradeInfo( '�й�����--�����ֽ��ֵ��ɹ�' )
        
        return True
        
    except Exception ,e:
        cashFile.close( )
        AfaLoggerFunc.tradeInfo( str(e) )
        TradeContext.errorCode = "F001"
        TradeContext.errorMsg  = "�й�����--�����ֽ��ֵ��ʧ��"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        return False

################################################################################
# ����ͨ�ļ�����                                  
# ��    �ܣ����ɻ����ֽ��ֵ�ļ�                           
# ����˵����                                                                  
# ��    ����                                                                   
#                                                                              
################################################################################            
def createHXFile( fileName ):
    
    AfaLoggerFunc.tradeInfo( '����---��ʼ�����ֽ��ֵ��' + fileName + '��' )
    
    try:
        cashFile = file( fileName,"w" )
        
        tmpStr = ""
        #����ʵ����Ҫ�ȿճ�4��
        for i in range(4): 
            tmpStr = tmpStr + "\n"
        tmpStr = tmpStr + " ".ljust( 105,"-" ) +  " \n"
        tmpStr = tmpStr + " �����ֽ��ֵ".ljust( 105,  " " ) + " \n"
        tmpStr = tmpStr + " ".ljust( 105,"-" ) +  " \n"
        tmpStr = tmpStr + " " + TradeContext.year1.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year2.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year3.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year4.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year5.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year6.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year7.ljust(14," ") + " \n"
        tmpStr = tmpStr + " ".ljust( 105,"-" ) +  " \n"
        tmpStr = tmpStr + " " + TradeContext.cash1.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash2.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash3.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash4.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash5.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash6.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash7.ljust(14," ") + " \n"
        tmpStr = tmpStr + " ".ljust( 105,"-" ) +  " \n"
        tmpStr = tmpStr + " " + TradeContext.year8.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year9.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year10.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year11.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year12.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year13.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year14.ljust(14," ") + " \n"
        tmpStr = tmpStr + " ".ljust( 105,"-" ) +  " \n"
        tmpStr = tmpStr + " " + TradeContext.cash8.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash9.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash10.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash11.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash12.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash13.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash14.ljust(14," ") + " \n"
        tmpStr = tmpStr + " ".ljust( 105,"-" ) +  " \n"
        
        cashFile.write( tmpStr )
        
        cashFile.close( )
        
        AfaLoggerFunc.tradeInfo( '����--�����ֽ��ֵ��ɹ�' )
        
        return True
        
    except Exception ,e:
        cashFile.close( )
        AfaLoggerFunc.tradeInfo( str(e) )
        TradeContext.errorCode = "F00333"
        TradeContext.errorMsg  = "����--�����ֽ��ֵ��ʧ��"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        return False

################################################################################
# ����ͨ�ļ�����                                  
# ��    �ܣ������Ҹ������ֽ��ֵ�ļ�                           
# ����˵����                                                                  
# ��    ����                                                                   
#                                                                              
################################################################################            
def createHappyFile( fileName ):
    
    AfaLoggerFunc.tradeInfo( '�Ҹ�����---��ʼ�����ֽ��ֵ��' + fileName + '��' )
    
    try:
        cashFile = file( fileName,"w" )
        
        tmpStr = ""
        #����ʵ����Ҫ���ȿճ�8��
        for i in range(0,8):
            tmpStr = tmpStr + "\n"
        tmpStr = tmpStr + "".ljust(37,' ') + "��    ��    ��    ֵ    ��\n\n"
        tmpStr = tmpStr + "".ljust(32,' ') + "���Ա���������ÿ1000Ԫ���շ�Ϊ��׼��\n\n"
        tmpStr = tmpStr + "".ljust(8,' ') + "�������ƣ�"
        tmpStr = tmpStr + TradeContext.productname.ljust(40,' ')
        tmpStr = tmpStr + "������ͬ�ţ�"
        tmpStr = tmpStr + TradeContext.policy.ljust(40,' ') + "\n\n"
        tmpStr = tmpStr + "".ljust(8,' ') + "�������ĩ".ljust(16,' ')
        tmpStr = tmpStr + "�ֽ��ֵ".ljust(16,' ')
        tmpStr = tmpStr + "�������ĩ".ljust(16,' ')
        tmpStr = tmpStr + "�ֽ��ֵ".ljust(16,' ')
        tmpStr = tmpStr + "�������ĩ".ljust(16,' ')
        tmpStr = tmpStr + "�ֽ��ֵ".ljust(16,' ') + "\n\n"
        tmpStr = tmpStr + "".ljust(8,' ')
        for i in range(0,int(TradeContext.CashCount)):
            tmpStr = tmpStr + TradeContext.year[i].ljust(16,' ')
            tmpStr = tmpStr + TradeContext.cash[i].ljust(16,' ')
            if i != 0 and (i+1)%3 == 0:
                tmpStr = tmpStr + "\n"
                tmpStr = tmpStr + "".ljust(8,' ')
        
        cashFile.write( tmpStr )
        
        cashFile.close( )
        
        AfaLoggerFunc.tradeInfo( '�Ҹ�����--�����ֽ��ֵ��ɹ�' )
        
        return True
        
    except Exception ,e:
        cashFile.close( )
        AfaLoggerFunc.tradeInfo( str(e) )
        TradeContext.errorCode = "F001"
        TradeContext.errorMsg  = "�Ҹ�����--�����ֽ��ֵ��ʧ��"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        return False

################################################################################            
# ����ͨ�ļ�����                                                                            
# ��    �ܣ�����̩�������ֽ��ֵ�ļ�                                                        
# ����˵����                                                                                
# ��    ����                                                                                
#                                                                                           
################################################################################            
def createTaikangFile( fileName ):                                                            
                                                                                            
    AfaLoggerFunc.tradeInfo( '̩������---��ʼ�����ֽ��ֵ��' + fileName + '��' )          
                                                                                            
    try:                                                                                    
        cashFile = file( fileName,"w" )                                                     
                                                                                            
        tmpStr = ""                                                                         
        #����ʵ����Ҫ���ȿճ�8��                                                            
        for i in range(0,8):                                                                
            tmpStr = tmpStr + "\n"                                                          
        tmpStr = tmpStr + "".ljust(37,' ') + "��  ��  ��  ֵ  ��  ��  ��\n\n"               
        tmpStr = tmpStr + "".ljust(32,' ') + "(��1000Ԫ�꽻���շ�Ϊ��λ��ע��)\n\n"     
        tmpStr = tmpStr + "".ljust(8,' ') + "�������ƣ�"                                    
        tmpStr = tmpStr + TradeContext.productname.ljust(40,' ')                            
        tmpStr = tmpStr + "������ͬ�ţ�"                                                    
        tmpStr = tmpStr + TradeContext.policy.ljust(40,' ') + "\n\n"                        
        tmpStr = tmpStr + "".ljust(8,' ') + "�������".ljust(16,' ')                      
        tmpStr = tmpStr + "��ĩ�ֽ��ֵ".ljust(16,' ')                                          
        tmpStr = tmpStr + "�������".ljust(16,' ')                                        
        tmpStr = tmpStr + "��ĩ�ֽ��ֵ".ljust(16,' ')                                          
        tmpStr = tmpStr + "�������".ljust(16,' ')                                        
        tmpStr = tmpStr + "��ĩ�ֽ��ֵ ��λ��Ԫ".ljust(16,' ') + "\n\n"                                 
        tmpStr = tmpStr + "".ljust(8,' ')                                                   
        for i in range(0,int(TradeContext.CashCount)):                                      
            tmpStr = tmpStr + TradeContext.year[i].ljust(16,' ')                            
            tmpStr = tmpStr + TradeContext.cash[i].ljust(16,' ')                            
            if i != 0 and (i+1)%3 == 0:                                                     
                tmpStr = tmpStr + "\n"                                                      
                tmpStr = tmpStr + "".ljust(8,' ')                                           
                                                                                            
        cashFile.write( tmpStr )                                                            
                                                                                            
        cashFile.close( )                                                                   
                                                                                            
        AfaLoggerFunc.tradeInfo( '̩������--�����ֽ��ֵ��ɹ�' )                           
                                                                                            
        return True                                                                         
                                                                                            
    except Exception ,e:                                                                    
        cashFile.close( )                                                                   
        AfaLoggerFunc.tradeInfo( str(e) )                                                   
        TradeContext.errorCode = "F001"                                                     
        TradeContext.errorMsg  = "̩������--�����ֽ��ֵ��ʧ��"                             
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )                                    
        return False                     
        
################################################################################            
# ����ͨ�ļ�����                                                                            
# ��    �ܣ������˱������ֽ��ֵ�ļ�                                                        
# ����˵����                                                                                
# ��    ����                                                                                
#                                                                                           
################################################################################            
def createRbsxFile( fileName ):                                                            
                                                                                            
    AfaLoggerFunc.tradeInfo( '�˱�����---��ʼ�����ֽ��ֵ��' + fileName + '��' )          
                                                                                            
    try:                                                                                    
        cashFile = file( fileName,"w" )                                                     
                                                                                            
        tmpStr = ""                                                                         
        #����ʵ����Ҫ���ȿճ�8��                                                            
        for i in range(0,8):                                                                
            tmpStr = tmpStr + "\n"                                                          
        tmpStr = tmpStr + "".ljust(37,' ') + "��    ��    ��    ֵ    ��\n\n"               
        tmpStr = tmpStr + "".ljust(32,' ') + "���Ա���������ÿ1000Ԫ���շ�Ϊ��׼��\n\n"     
        tmpStr = tmpStr + "".ljust(8,' ') + "�������ƣ�"                                    
        tmpStr = tmpStr + TradeContext.productname.ljust(40,' ')                            
        tmpStr = tmpStr + "������ͬ�ţ�"                                                    
        tmpStr = tmpStr + TradeContext.policy.ljust(40,' ') + "\n\n"                        
        tmpStr = tmpStr + "".ljust(8,' ') + "�������ĩ".ljust(16,' ')                      
        tmpStr = tmpStr + "�ֽ��ֵ".ljust(16,' ')                                          
        tmpStr = tmpStr + "�������ĩ".ljust(16,' ')                                        
        tmpStr = tmpStr + "�ֽ��ֵ".ljust(16,' ')                                          
        tmpStr = tmpStr + "�������ĩ".ljust(16,' ')                                        
        tmpStr = tmpStr + "�ֽ��ֵ".ljust(16,' ') + "\n\n"                                 
        tmpStr = tmpStr + "".ljust(8,' ')                                                   
        for i in range(0,int(TradeContext.CashCount)):                                      
            tmpStr = tmpStr + TradeContext.year[i].ljust(16,' ')                            
            tmpStr = tmpStr + TradeContext.cash[i].ljust(16,' ')                            
            if i != 0 and (i+1)%3 == 0:                                                     
                tmpStr = tmpStr + "\n"                                                      
                tmpStr = tmpStr + "".ljust(8,' ')                                           
                                                                                            
        cashFile.write( tmpStr )                                                            
                                                                                            
        cashFile.close( )                                                                   
                                                                                            
        AfaLoggerFunc.tradeInfo( '�˱�����--�����ֽ��ֵ��ɹ�' )                           
                                                                                            
        return True                                                                         
                                                                                            
    except Exception ,e:                                                                    
        cashFile.close( )                                                                   
        AfaLoggerFunc.tradeInfo( str(e) )                                                   
        TradeContext.errorCode = "F001"                                                     
        TradeContext.errorMsg  = "�˱�����--�����ֽ��ֵ��ʧ��"                             
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )                                    
        return False                                                                        
                                                       
################################################################################
# ����ͨ�ļ�����                                  
# ��    �ܣ��������������ֽ��ֵ�ļ�                           
# ����˵����                                                                  
# ��    ����                                                                   
#                                                                              
################################################################################            
def createLifeFile( fileName ):
    
    AfaLoggerFunc.tradeInfo( '��������---��ʼ�����ֽ��ֵ��' + fileName + '��' )
    
    try:
        cashFile = file( fileName,"w" )
        
        tmpStr = ""
        #����ʵ����Ҫ���ȿճ�8��
        for i in range(0,8):
            tmpStr = tmpStr + "\n"
        tmpStr = tmpStr + "".ljust(37,' ') + "��    ��    ��    ֵ    ��\n\n"
        tmpStr = tmpStr + "".ljust(32,' ') + "���Ա���������ÿ1000Ԫ���շ�Ϊ��׼��\n\n"
        tmpStr = tmpStr + "".ljust(8,' ') + "�������ƣ�"
        tmpStr = tmpStr + TradeContext.productname.ljust(40,' ')
        tmpStr = tmpStr + "������ͬ�ţ�"
        tmpStr = tmpStr + TradeContext.policy.ljust(40,' ') + "\n\n"
        tmpStr = tmpStr + "".ljust(8,' ') + "���/����".ljust(16,' ')
        tmpStr = tmpStr + "�ֽ��ֵ".ljust(16,' ')
        tmpStr = tmpStr + "���/����".ljust(16,' ')
        tmpStr = tmpStr + "�ֽ��ֵ".ljust(16,' ')
        tmpStr = tmpStr + "���/����".ljust(16,' ')
        tmpStr = tmpStr + "�ֽ��ֵ".ljust(16,' ') + "\n\n"
        tmpStr = tmpStr + "".ljust(8,' ')
        for i in range(0,int(TradeContext.CashCount)):
            tmpStr = tmpStr + TradeContext.year[i].ljust(16,' ')
            tmpStr = tmpStr + TradeContext.cash[i].ljust(16,' ')
            if i != 0 and (i+1)%3 == 0:
                tmpStr = tmpStr + "\n"
                tmpStr = tmpStr + "".ljust(8,' ')
        
        cashFile.write( tmpStr )
        
        cashFile.close( )
        
        AfaLoggerFunc.tradeInfo( '��������--�����ֽ��ֵ��ɹ�' )
        
        return True
        
    except Exception ,e:
        cashFile.close( )
        AfaLoggerFunc.tradeInfo( str(e) )
        TradeContext.errorCode = "F001"
        TradeContext.errorMsg  = "��������--�����ֽ��ֵ��ʧ��"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        return False                                                                                    

################################################################################
# ����ͨ�ļ�����                                  
# ��    �ܣ������˱������ֽ��ֵ�ļ�                           
# ����˵����                                                                  
# ��    ����                                                                   
#                                                                              
################################################################################            
def createRbjkFile( fileName ):
    
    AfaLoggerFunc.tradeInfo( '�˱�����---��ʼ�����ֽ��ֵ��' + fileName + '��' )
    
    try:
        cashFile = file( fileName,"w" )
        
        tmpStr = ""
        #����ʵ����Ҫ���ȿճ�8��
        for i in range(0,8):
            tmpStr = tmpStr + "\n"
        tmpStr = tmpStr + "".ljust(37,' ') + "��    ��    ��    ֵ    ��\n\n"
        tmpStr = tmpStr + "".ljust(32,' ') + "���Ա���������ÿ1000Ԫ���շ�Ϊ��׼��\n\n"
        tmpStr = tmpStr + "".ljust(8,' ') + "�������ƣ�"
        tmpStr = tmpStr + TradeContext.productname.ljust(40,' ')
        tmpStr = tmpStr + "������ͬ�ţ�"
        tmpStr = tmpStr + TradeContext.policy.ljust(40,' ') + "\n\n"
        tmpStr = tmpStr + "".ljust(8,' ') + "���/����".ljust(16,' ')
        tmpStr = tmpStr + "�ֽ��ֵ".ljust(16,' ')
        tmpStr = tmpStr + "���/����".ljust(16,' ')
        tmpStr = tmpStr + "�ֽ��ֵ".ljust(16,' ')
        tmpStr = tmpStr + "���/����".ljust(16,' ')
        tmpStr = tmpStr + "�ֽ��ֵ".ljust(16,' ') + "\n\n"
        tmpStr = tmpStr + "".ljust(8,' ')
        for i in range(0,int(TradeContext.CashCount)):
            tmpStr = tmpStr + TradeContext.year[i].ljust(16,' ')
            tmpStr = tmpStr + TradeContext.cash[i].ljust(16,' ')
            if i != 0 and (i+1)%3 == 0:
                tmpStr = tmpStr + "\n"
                tmpStr = tmpStr + "".ljust(8,' ')
        
        cashFile.write( tmpStr )
        
        cashFile.close( )
        
        AfaLoggerFunc.tradeInfo( '�˱�����--�����ֽ��ֵ��ɹ�' )
        
        return True
        
    except Exception ,e:
        cashFile.close( )
        AfaLoggerFunc.tradeInfo( str(e) )
        TradeContext.errorCode = "F001"
        TradeContext.errorMsg  = "�˱�����--�����ֽ��ֵ��ʧ��"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        return False                                                                                    
