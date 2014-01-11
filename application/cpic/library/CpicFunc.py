# -*- coding: gbk -*-
##########################################################
#       ���ƣ����������պ���                             #
#       ���ڣ�2009-04-01                                 #
#       ʱ�䣺15:15                                      #
#       ��������ͬ�Ƽ�                                   #
##########################################################
import TradeContext, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaDBFunc,AfaUtilTools,AfaLoggerFunc
import HostContext,AfaHostFunc,HostComm,AfaAhAdb
import os
from types import *
from datetime import *


################################################################################
#           ������.��������
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
#           ������.�ļ�ת��
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
#           ������.��������
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
#       ����������
#       ���ܣ����ɵ�����������ִ�ļ�
#       ���ڣ�2008-11-04
#       ˵����
#       ���б���(10)+��������(8)+�����������(10)+����������(10)+������(7)+
#       ������ˮ��(30)+������(20)+���(12λ����С����)+����������2λ��
#       ���б���Ĭ��Ϊ"01",�����������"ANHNX00001",��������"01"
###########################################################
def CreCpicLjFile(logger):
    logger.info( "��ʼ���ɰ������������׻�ִ�ļ�" )
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
    print "-------------< [����ͨ������������ִ�ļ�:�� " + str(len(records)) + "���ɹ���¼] >------------"
    logger.info( "< [����ͨ������������ִ�ļ�:�� " + str(len(records)) + "���ɹ���¼] >")
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
        logger.info( "�������ɰ�����������ִ�ļ�(�޼�¼)" )
        f.close()
    f.close()
    logger.info( "�������ɰ�����������ִ�ļ�" )
    return 0
################################################################################
#           ������.��������
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
#           ������.��������
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
#           ������.��������
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
# ��    �ܣ����ɰ���������
# ����˵����
# ��    ����
# 
################################################################################
def CreatReport(logger):
    try:
        resulBrno = None
        i = 0
        splitStr = "|"
        #�ж��Ƿ��ǶԹ��ʻ���������
        sqlbrno = "select note1 from afa_unitadm where sysid = '" + TradeContext.sysId + "' and unitno = '" + TradeContext.unitno + "'"
        logger.info("��ѯ�Թ��ʻ��������㣺"+sqlbrno)
        resultb = AfaDBFunc.SelectSql(sqlbrno)
        if resultb is None:
            logger.info("���ݿ�����쳣"+sqlbrno)
            return -1
        elif(len(resultb)) == 0:
            logger.info("Ӧ�ò�������˶�")
            TradeContext.errorCode = "0002"
            TradeContext.errorMsg = "Ӧ�ò�����"
            return 0
        else:
            logger.info("���ݿ��������"+resultb[0][0])
            TradeContext.brnoAll = resultb[0][0]
        TradeContext.corpDate = TradeContext.workDate
        logger.info ( " ��ӡ����  "+TradeContext.corpDate)
        TradeContext.PBDAFILE = TradeContext.corpDate+"_"+TradeContext.brno+"_"+TradeContext.tellerno+"_"+TradeContext.reportType+".txt"
        fileName = os.environ['HOME']+"/afa/data/cpic/report/"+TradeContext.PBDAFILE
        logger.info ( " �ļ�·������  "+fileName)
        try:
            f = file(fileName,"w")
        except:
            logger.info("�����ļ�["+fileName+"]ʧ��")
            TradeContext.errorCode = "0001"
            TradeContext.errorMsg = "�����ļ�["+fileName+"]ʧ��"
            return -2
            
        #��ӡ�ļ�
        PfileName = os.environ['HOME']+"/afa/data/cpic/report/P_"+TradeContext.PBDAFILE
        TradeContext.P_PBDAFILE = "P_" + TradeContext.PBDAFILE
        logger.info ( " ��ӡ�ļ�·������  "+PfileName)
        try:
            Pf = file(PfileName,"w")
        except:
            logger.info("���ɴ�ӡ�ļ�["+PfileName+"]ʧ��")
            TradeContext.errorCode = "0001"
            TradeContext.errorMsg = "���ɴ�ӡ�ļ�["+PfileName+"]ʧ��"
            return -2
        # ���Ϊ��ϸ�����ؼ�¼����
        #if ( TradeContext.reportType == "2" ):
        #    sqltrade = "select agentserialno from afa_maintransdtl where sysid = '"+TradeContext.sysId+"' and unitno = '" + TradeContext.unitno + "'"
        #    if ( TradeContext.existVariable( "ProSel" ) and TradeContext.ProSel.strip() == "0" ):
        #        sqltrade = sqltrade + " and note7 = '"+TradeContext.ProCode+"'"
        #    #sqltrade = sqltrade + " and brno = '"+TradeContext.EBrno+"'"
        #    sqltrade = sqltrade + " and workdate >= '"+TradeContext.startdate+"' and workdate <= '"+TradeContext.enddate+"'"
        #    sqlbrno = sqlbrno + " and chkflag = '0' and corpchkflag = '0'"
        #    sqltrade = sqltrade + " and bankstatus = '0' and corpstatus = '0' and revtranf = '0' order by agentserialno"
        #    logger.info( "��ѯ��¼����"+str(sqltrade) )
        #    resultrade = AfaDBFunc.SelectSql(sqltrade)
        #    if resultrade is None:
        #        logger.info("��ѯ��ϸ:���ݿ�����쳣"+sqltrade)
        #        TradeContext.errorCode = "0001"
        #        TradeContext.errorMsg = "��ѯ��ϸ:���ݿ�����쳣"+sqltrade
        #        return -2
        #    else:
        #        TradeContext.RecCount = str(len(resultrade))
        logger.info ( " ��ʼ���ɰ������ܱ����ļ�������Ϊ["+TradeContext.startdate+">>>>>"+TradeContext.enddate+"]" )
        logger.info ( " TradeContext.brnoAll  ["+TradeContext.brnoAll+"]" )
        logger.info ( " TradeContext.brno     ["+TradeContext.brno+"]" )
        logger.info ( " TradeContext.Brno     ["+TradeContext.Brno+"]" )
        #logger.info ( " TradeContext.brnoFlag ["+TradeContext.brnoFlag+"]" )
        logger.info ( " TradeContext.ProSel   ["+TradeContext.ProSel+"]" )
        logger.info ( " TradeContext.ProCode  ["+TradeContext.ProCode+"]" )
        
        #�����������ͻ�����,��ѯ��ӡ���л�������;���ͻ�����,������ѯ��ӡ�˻�������;
        #��������ֻ�ܲ�ѯ��ӡ����������
        
        #�����������ͻ�����,��ѯ��ӡ���л�������
        if ( TradeContext.brno == TradeContext.brnoAll and TradeContext.Brno.strip() == ""):
            sqlbrno = "select distinct brno from afa_maintransdtl where sysid = '"+TradeContext.sysId+"' and unitno = '" + TradeContext.unitno + "'"
            if ( TradeContext.existVariable( "ProSel" ) and TradeContext.ProSel.strip() == "0" ):
                sqlbrno = sqlbrno + " and note7 = '"+TradeContext.ProCode+"'"
            
            #begin 20100618 ������  Ϊ���ܹ���ѯ����δ������ϸ�޸Ĳ�ѯ����
            if ( TradeContext.startdate == TradeContext.enddate and TradeContext.startdate == TradeContext.workDate ):
                sqlbrno = sqlbrno + " and chkflag = '9' and corpchkflag = '9'"
            else:
                sqlbrno = sqlbrno + " and chkflag = '0' and corpchkflag = '0'"
            #end
            
            sqlbrno = sqlbrno + " and workdate >= '"+TradeContext.startdate+"' and workdate <= '"+TradeContext.enddate+"'"
            #sqlbrno = sqlbrno + " and chkflag = '0' and corpchkflag = '0'"
            sqlbrno = sqlbrno + " and bankstatus = '0' and revtranf = '0' order by brno"
        #elif ( TradeContext.existVariable( "brnoFlag" ) and TradeContext.brnoFlag.strip() == "0" ):
        #    sqlbrno = "select distinct brno from afa_maintransdtl where sysid = '"+TradeContext.sysId+"' and unitno = '" + TradeContext.unitno + "'"
        #    if ( TradeContext.existVariable( "ProSel" ) and TradeContext.ProSel.strip() == "0" ):
        #        sqlbrno = sqlbrno + " and note7 = '"+TradeContext.ProCode+"'"
        #    sqlbrno = sqlbrno + " and workdate >= '"+TradeContext.startdate+"' and workdate <= '"+TradeContext.enddate+"'"
        #    sqlbrno = sqlbrno + " and brno like '%"+TradeContext.brno[0:6]+"%'"
        #    sqlbrno = sqlbrno + " and chkflag = '0' and corpchkflag = '0'"
        #    sqlbrno = sqlbrno + " and bankstatus = '0' and corpstatus = '0' and revtranf = '0' order by brno"
        #�����в�ѯ��ӡָ����������
        elif ( TradeContext.brno == TradeContext.brnoAll and TradeContext.Brno.strip() != ""):
            sqlbrno = "select distinct brno from afa_maintransdtl where sysid = '"+TradeContext.sysId+"' and unitno = '" + TradeContext.unitno + "'"
            if ( TradeContext.existVariable( "ProSel" ) and TradeContext.ProSel.strip() == "0" ):
                sqlbrno = sqlbrno + " and note7 = '"+TradeContext.ProCode+"'"
            sqlbrno = sqlbrno + " and brno = '"+TradeContext.Brno+"'"
            
            #begin 20100618 ������  Ϊ���ܹ���ѯ����δ������ϸ�޸Ĳ�ѯ����
            if ( TradeContext.startdate == TradeContext.enddate and TradeContext.startdate == TradeContext.workDate ):
                sqlbrno = sqlbrno + " and chkflag = '9' and corpchkflag = '9'"
            else:
                sqlbrno = sqlbrno + " and chkflag = '0' and corpchkflag = '0'"
            #end
            
            sqlbrno = sqlbrno + " and workdate >= '"+TradeContext.startdate+"' and workdate <= '"+TradeContext.enddate+"'"
            #sqlbrno = sqlbrno + " and chkflag = '0' and corpchkflag = '0'"
            sqlbrno = sqlbrno + " and bankstatus = '0' and revtranf = '0'"
        #��������ֻ�ܲ�ѯ��ӡ����������
        else:
            sqlbrno = "select distinct brno from afa_maintransdtl where sysid = '"+TradeContext.sysId+"' and unitno = '" + TradeContext.unitno + "'"
            if ( TradeContext.existVariable( "ProSel" ) and TradeContext.ProSel.strip() == "0" ):
                sqlbrno = sqlbrno + " and note7 = '"+TradeContext.ProCode+"'"
            sqlbrno = sqlbrno + " and brno = '"+TradeContext.brno+"'"
            
            #begin 20100618 ������  Ϊ���ܹ���ѯ����δ������ϸ�޸Ĳ�ѯ����
            if ( TradeContext.startdate == TradeContext.enddate and TradeContext.startdate == TradeContext.workDate ):
                sqlbrno = sqlbrno + " and chkflag = '9' and corpchkflag = '9'"
            else:
                sqlbrno = sqlbrno + " and chkflag = '0' and corpchkflag = '0'"
            #end
            
            sqlbrno = sqlbrno + " and workdate >= '"+TradeContext.startdate+"' and workdate <= '"+TradeContext.enddate+"'"
            #sqlbrno = sqlbrno + " and chkflag = '0' and corpchkflag = '0'"
            sqlbrno = sqlbrno + " and bankstatus = '0'  and revtranf = '0'"
        logger.info( "��ѯ�����"+str(sqlbrno) )
        resulBrno = AfaDBFunc.SelectSql(sqlbrno)
        logger.info( "��ѯ���"+str(len(resulBrno)) )
        if resulBrno is None:
            logger.info("��ѯ�����:���ݿ�����쳣"+sqlbrno)
            TradeContext.errorCode = "0001"
            TradeContext.errorMsg = "��ѯ�����:���ݿ�����쳣"+sqlbrno
            return -2
        elif ( len(resulBrno) == 0 ):
            TradeContext.errorCode = "0000"
            TradeContext.errorMsg = "δ��ѯ����صĽ��׼�¼"
            return -3
        else:
            TradeContext.RecAllCount = 0
            reccount = 1
            #��ӡ�ļ���ͷ
            if TradeContext.reportType == "1":
                tmpStr = "".ljust(40) + "�����ջ��ܱ�\n"
            else:
                tmpStr = "".ljust(40) + "��������ϸ��\n"
            tmpStr = tmpStr + "      ��������:  " + TradeContext.brno + "\n"
            tmpStr = tmpStr + "      ��ֹ����:  " + TradeContext.startdate + "-" + TradeContext.enddate + "      ��ӡ����:" + TradeContext.workDate + "\n"
#            tmpStr = tmpStr + "".ljust(132,"=") + "\n"
            if TradeContext.reportType == "1":
                tmpStr = tmpStr + "".ljust(100,"=") + "\n"
                tmpStr = tmpStr + "      ������      ��������           ����˵��                ����         ���ս��\n"
                
            else:
                tmpStr = tmpStr + "".ljust(151,"=") + "\n"
                tmpStr = tmpStr + "      ��������    ��������        ��������    ����˵��               ������ˮ           Ͷ������        �ͻ�����            ���ѽ��           ������ˮ\n"
                tmpStr = tmpStr + "".ljust(151,"=") + "\n"
            Pf.write(tmpStr)
            
            for i in range (0,len(resulBrno)):
                TradeContext.EBrno = str(resulBrno[i][0])
                #�жϱ����������ɲ�ͬ�ı���
                logger.info("reportType=[" + TradeContext.reportType + "]")
                if ( TradeContext.reportType == "1" ):
                    logger.info ( " [" + TradeContext.EBrno + "]���ɻ��ܱ� " )
                    resulCount = None
                    sqlcount = "select count(*),sum(cast(amount as decimal(15,2)) ) from afa_maintransdtl where sysid = '"+TradeContext.sysId+"' and unitno = '" + TradeContext.unitno + "'"
                    if ( TradeContext.existVariable( "ProSel" ) and TradeContext.ProSel.strip() == "0" ):
                        sqlcount = sqlcount + " and note7 = '"+TradeContext.ProCode+"'"
                    sqlcount = sqlcount + " and brno = '"+str(TradeContext.EBrno)+"'"
                    
                    #begin 20100618 ������  Ϊ���ܹ���ѯ����δ������ϸ�޸Ĳ�ѯ����
                    if ( TradeContext.startdate == TradeContext.enddate and TradeContext.startdate == TradeContext.workDate ):
                        sqlcount = sqlcount + " and chkflag = '9' and corpchkflag = '9'"
                    else:
                        sqlcount = sqlcount + " and chkflag = '0' and corpchkflag = '0'"
                    #end
                    
                    sqlcount = sqlcount + " and workdate >= '"+TradeContext.startdate+"' and workdate <= '"+TradeContext.enddate+"'"
                    #sqlcount = sqlcount + " and chkflag = '0' and corpchkflag = '0'"
                    sqlcount = sqlcount + " and bankstatus = '0'  and revtranf = '0'"
                    logger.info( "���ɻ��ܱ�ÿ���������"+str(sqlcount) )
                    resulCount = AfaDBFunc.SelectSql(sqlcount)
                    if resulCount is None:
                        logger.info("��ѯ����:���ݿ�����쳣"+sqlcount)
                        TradeContext.errorCode = "0001"
                        TradeContext.errorMsg = "��ѯ����:���ݿ�����쳣"+sqlcount
                        return -2
                    else:
                        TradeContext.RecAllCount += 1
                        TradeContext.Dcount  = resulCount[0][0]
                        TradeContext.Damount = resulCount[0][1]
                        tmpStr = ""
                        tmpStr = tmpStr + str(TradeContext.EBrno) + splitStr      #�����
                        tmpStr = tmpStr + str(TradeContext.ProCode) + splitStr    #��������
                        tmpStr = tmpStr + str(TradeContext.Dcount) +splitStr      #�ܼ�¼����
                        tmpStr = tmpStr + str(TradeContext.Damount) +splitStr     #�ܽ��
                        tmpStr = tmpStr + "\n"
                        logger.info("��ѯ����:tmpStr      "+str(tmpStr))
                        if (reccount >= int(TradeContext.RecStrNo)) and (reccount <= int(TradeContext.RecStrNo) + 10):
                            f.write(tmpStr)
                        
                        #��ӡ�ļ�
                        tmpStr = "".ljust(6)
                        tmpStr = tmpStr + str(TradeContext.EBrno).ljust(12)       #�����
                        tmpStr = tmpStr + str(TradeContext.ProCode).ljust(19)     #��������
                        #�ر�� 20091124 ���ݵ�λ�����ȡ���չ�˾��Ϣ
                        AfaAhAdb.ADBGetInfoByUnitno()
                        tmpStr = tmpStr + str(TradeContext.PlanName).ljust(24)    #��������
                        ##��ӡ�ļ��мӸ�����˵��
                        #if str(TradeContext.ProCode) == str(1):
                        #    tmpStr = tmpStr + "������                ".ljust(24) #����˵��
                        #if str(TradeContext.ProCode) == str(2):
                        #    tmpStr = tmpStr + "���Ľ���������˺�����".ljust(24) #����˵��
                        tmpStr = tmpStr + str(TradeContext.Dcount).ljust(13)      #�ܼ�¼����
                        tmpStr = tmpStr + str(TradeContext.Damount).ljust(28)     #�ܽ��
                        tmpStr = tmpStr + "\n" + "".ljust(100,"-") + "\n"
                        Pf.write(tmpStr)
                        
                        reccount += 1
                else:
                    logger.info ( " [" + TradeContext.EBrno + "]������ϸ�� " )
                    #����ǰ̨�ܼ�¼����
                    resulDetail = None
                    j = 0
                    sqldetail = "select brno,workdate,note7,bankserno,userno,username,amount,revtranf,agentserialno from afa_maintransdtl where sysid = '"+TradeContext.sysId+"' and unitno = '" + TradeContext.unitno + "'"
                    if ( TradeContext.existVariable( "ProSel" ) and TradeContext.ProSel.strip() == "0" ):
                        sqldetail = sqldetail + " and note7 = '"+TradeContext.ProCode+"'"
                    sqldetail = sqldetail + " and brno = '"+TradeContext.EBrno+"'"
                    
                    #begin 20100618 ������  Ϊ���ܹ���ѯ����δ������ϸ�޸Ĳ�ѯ����
                    if ( TradeContext.startdate == TradeContext.enddate and TradeContext.startdate == TradeContext.workDate ):
                        sqldetail = sqldetail + " and chkflag = '9' and corpchkflag = '9'"
                    else:
                        sqldetail = sqldetail + " and chkflag = '0' and corpchkflag = '0'"
                    #end
                    
                    sqldetail = sqldetail + " and workdate >= '"+TradeContext.startdate+"' and workdate <= '"+TradeContext.enddate+"'"
                    #sqldetail = sqldetail + " and chkflag = '0' and corpchkflag = '0'"
                    sqldetail = sqldetail + " and bankstatus = '0'  and revtranf = '0' order by agentserialno"
                    logger.info( str(sqldetail) )
                    resulDetail = AfaDBFunc.SelectSql(sqldetail)
                    if resulDetail is None:
                        logger.info("��ѯ��ϸ:���ݿ�����쳣"+sqldetail)
                        TradeContext.errorCode = "0001"
                        TradeContext.errorMsg = "��ѯ��ϸ:���ݿ�����쳣"+sqldetail
                        return -2
                    else:
                        TradeContext.RecAllCount = TradeContext.RecAllCount + len(resulDetail)
                        #���û�н��׼�¼�򷵻�
                        if ( len(resulDetail) > 0 ):
                            for j in range (0,len(resulDetail)):
                                # ��������   ��������   ��������   ������ˮ    ��������        �ͻ�����      ���ѽ��   ������ˮ ������־
                                tmpStr = ""
                                tmpStr = tmpStr + str(resulDetail[j][0]).strip() + splitStr      #��������
                                tmpStr = tmpStr + str(resulDetail[j][1]).strip() + splitStr      #��������
                                tmpStr = tmpStr + str(resulDetail[j][2]).strip() + splitStr      #��������
                                tmpStr = tmpStr + str(resulDetail[j][3]).strip() + splitStr      #������ˮ
                                tmpStr = tmpStr + str(resulDetail[j][4]).strip() + splitStr      #��������
                                tmpStr = tmpStr + str(resulDetail[j][5]).strip() + splitStr      #�ͻ�����
                                tmpStr = tmpStr + str(resulDetail[j][6]).strip() + splitStr      #���ѽ��
                                #begin 20100730 ������ ������ϸ��ѯ��ӡ��̨������ˮ�ֶ�
                                tmpStr = tmpStr + str(resulDetail[j][8]).strip() + splitStr      #������ˮ
                                #end
                                tmpStr = tmpStr + "\n"
                                AfaLoggerFunc.tradeInfo("reccount0 = [" + str(reccount) + "]")
                                if (reccount >= int(TradeContext.RecStrNo)) and (reccount < int(TradeContext.RecStrNo) + 10):
                                    AfaLoggerFunc.tradeInfo("reccount = [" + str(reccount) + "]")
                                    f.write(tmpStr)
                                    
                                tmpStr = "".ljust(6)
                                tmpStr = tmpStr + str(resulDetail[j][0]).ljust(12)      #��������
                                tmpStr = tmpStr + str(resulDetail[j][1]).ljust(16)      #�������� 
                                tmpStr = tmpStr + str(resulDetail[j][2]).ljust(12)      #��������
                                #begin 20100203 ���������� ���ݵ�λ�����ȡ���չ�˾��Ϣ
                                AfaAhAdb.ADBGetInfoByUnitno()
                                tmpStr = tmpStr + str(TradeContext.PlanName).ljust(24)    #��������
                                #end   
                                #��ӡ�ļ��мӸ�����˵��
                                #if str(resulDetail[j][2]) == str(1):
                                    #tmpStr = tmpStr + "������                ".ljust(24) #����˵��
                                #if str(resulDetail[j][2]) == str(2):
                                    #tmpStr = tmpStr + "���Ľ���������˺�����".ljust(24) #����˵��
                                tmpStr = tmpStr + str(resulDetail[j][3]).ljust(19)      #������ˮ
                                tmpStr = tmpStr + str(resulDetail[j][4]).ljust(16)      #��������
                                tmpStr = tmpStr + str(resulDetail[j][5]).ljust(12)      #�ͻ�����
                                tmpStr = tmpStr + str(resulDetail[j][6]).ljust(10)      #���ѽ��

                                #begin 20100730 ������ ������ϸ��ѯ��ӡ��̨������ˮ�ֶ�
                                tmpStr = tmpStr + str(resulDetail[j][8]).rjust(19)      #������ˮ
                                #end

                                tmpStr = tmpStr + "\n" + "".ljust(151,"-") + "\n"
                                Pf.write(tmpStr)
                                
                                reccount += 1
                        else:
                            logger.info( "��������������ϸ�ļ�(�޼�¼)" )
                            f.close()
                            
            #��ӡ�ļ����
            if TradeContext.reportType == "1":
                tmpStr = "\n" + "".ljust(6) + "�Ʊ�:" + TradeContext.tellerno + "\n"
            else:
                tmpStr = "\n" + "".ljust(6) + "�Ʊ�:" + TradeContext.tellerno.ljust(10) + "���:".ljust(15) + "����:".ljust(15) + "����:".ljust(15) + "�������:\n"
            Pf.write(tmpStr)
            
            f.close()
            if (int(TradeContext.RecAllCount) - int(TradeContext.RecStrNo) >= 10):
                TradeContext.RecCount = 10
            else:
                TradeContext.RecCount = int(TradeContext.RecAllCount) - int(TradeContext.RecStrNo) + 1
                
            if TradeContext.RecCount <= 0:
                TradeContext.errorCode = "0001"
                TradeContext.errorMsg = "��ʼ�����Ƿ�"
                return -2
                
            TradeContext.RecCount = str(TradeContext.RecCount)
            TradeContext.RecAllCount = str(TradeContext.RecAllCount)
            AfaLoggerFunc.tradeInfo("RecCount=[" + TradeContext.RecCount + "]")
            AfaLoggerFunc.tradeInfo("RecAllCount=[" + TradeContext.RecAllCount + "]")
            return 0
    except Exception ,e:
        TradeContext.errorCode = "0001"
        TradeContext.errorMsg = "���ɰ������������ ["+str(e)+"]"
        logger.info("���ɰ������������ ["+str(e)+"]")
        return -3
