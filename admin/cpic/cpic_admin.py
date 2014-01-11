#!/usr/bin/env python
# -*- coding: gbk -*-
###############################################################################
# �ļ����ƣ�cpic_admin.py
# �ļ���ʶ��
# ժ    Ҫ������������
#
# ��ǰ�汾��2.0
# ��    �ߣ�XZH
# ������ڣ�2008��7��12��
#
# ȡ���汾��
# ԭ �� �ߣ�
# ������ڣ�
###############################################################################
import TradeContext, ConfigParser, sys, AfaDBFunc, os, AfaAdminFunc
from types import *


fileNameHead = 'ANHNX00001'
##########################################���ʴ���##########################################
def SendToCorp(sysId,unitNo,trxDate):

    try:
        #��������,����������,,������ˮ��,������,���
        sqlStr = "SELECT workdate,brno,agentserialno,note5,amount from afa_maintransdtl where "
        sqlStr = sqlStr + " SYSID='"        + sysId    + "'"
        sqlStr = sqlStr + " AND UNITNO='"   + unitNo   + "'"
        sqlStr = sqlStr + " AND WORKDATE='" + trxDate  + "'"
        #sqlStr = sqlStr + " and revtranf = '0' and bankstatus = '0'"
        sqlStr = sqlStr + " and revtranf = '0' and bankstatus = '0' and chkflag='0'"

        AfaAdminFunc.WrtLog(sqlStr)

        records = AfaDBFunc.SelectSql( sqlStr )
        if (records==None):
            AfaAdminFunc.WrtLog('>>>������:���ɶ��ʴ���ʧ��,���ݿ��쳣')
            return False

        if (len(records)==0):
            AfaAdminFunc.WrtLog('>>>������:û���κ���ˮ��Ϣ,����Ҫ����ҵ���ж���,��Ƽ���Աȷ��')
            return False


        #���������ļ�
        dzFileName = TradeContext.CORP_LDIR + '/' + sysId + "_" + unitNo + '_' + trxDate + '.txt'

        AfaAdminFunc.WrtLog(dzFileName)

        dzfp= open(dzFileName,  "w")
        
        totalnum = 0
        totalamt = 0
        
        chuFaLeiBie = ''
        for i in range(0, len(records)):
            tmpStr = ""
            #���б���
            tmpStr = tmpStr + "01" + "|"
            #��������
            tmpStr = tmpStr + records[i][0].strip() + "|"
            #�����������
            tmpStr = tmpStr + "ANHNX00001" + "|"
            #����������
            tmpStr = tmpStr + records[i][1].strip()  + "|"
            #������
            tmpStr = tmpStr + "6000113" + "|"
            #������ˮ��
            tmpStr = tmpStr + records[i][2].strip()  + "|"
            #������
            tmpStr = tmpStr + records[i][3].strip()  + "|"
            #���
            tmpStr = tmpStr + records[i][4].strip()  + "|"
            #��������
            tmpStr = tmpStr + "01|\n"
            
            dzfp.write(tmpStr)

            totalnum = totalnum + 1
            totalamt = totalamt + (float)(records[i][4].strip())

        dzfp.close()

        sqlStr = "update afa_maintransdtl set corpchkflag = '0' where "
        sqlStr = sqlStr + " SYSID='"+ sysId    + "'"
        sqlStr = sqlStr + " AND UNITNO='"   + unitNo   + "'"
        sqlStr = sqlStr + " AND WORKDATE='" + trxDate  + "'"
        sqlStr = sqlStr + " and revtranf = '0' and bankstatus = '0'"
        
        AfaAdminFunc.WrtLog(sqlStr)
        
        if not AfaDBFunc.UpdateSqlCmt(sqlStr):
            AfaAdminFunc.WrtLog('>>>������:������ҵ���˱�ʶʧ��')
            return False

        AfaAdminFunc.WrtLog('>>>������:���ʴ���ɹ�[�ܱ���='+str(totalnum) + ',�ܽ��=' + str(totalamt) + ']')

        #�ļ�����
        TradeContext.DZFILESIZE = str(os.path.getsize(dzFileName))

        #�����ļ���
        TradeContext.DZFILENAME = dzFileName

        #�ܱ���
        TradeContext.DZNUM = str(totalnum)

        #�ܽ��
        TradeContext.DZAMT = str(totalamt)

        #�������������ϸ�ļ�
        lfileName = sysId + "_" + unitNo + '_' + trxDate + '.txt'
        rfileName = fileNameHead + trxDate + '.txt'

        if not AfaAdminFunc.PutDzFile(sysId, lfileName, rfileName):
            return False

        return True

    except Exception, e:
        AfaAdminFunc.WrtLog(str(e))
        AfaAdminFunc.WrtLog('���ʴ����쳣')
        return False
        
###########################################������###########################################
if __name__=='__main__':


    print('**********������������ʼ**********')

    if ( len(sys.argv) != 4 ):
        print( '�÷�: jtfk_Proc sysid unitno dateoffset')
        sys.exit(-1)

    sSysId      = sys.argv[1]
    sUnitno     = sys.argv[2]
    sOffSet     = sys.argv[3]
    sTrxDate   = AfaAdminFunc.getTimeFromNow(int(sOffSet))

    print '   ϵͳ���� = ' + sSysId
    print '   ��λ���� = ' + sUnitno
    print '   �������� = ' + sTrxDate

    #��ȡ�����ļ�
    if ( not AfaAdminFunc.GetAdminConfig(sSysId + "_" + sUnitno) ) :
        sys.exit(-1)


    AfaAdminFunc.WrtLog('>>>����������')
    if not AfaAdminFunc.MatchData(sSysId,sUnitno,sTrxDate):
        sys.exit(-1)


    AfaAdminFunc.WrtLog('>>>����ҵ����')
    if not SendToCorp(sSysId,sUnitno,sTrxDate):
        sys.exit(-1)


    print '**********��������������**********'

    sys.exit(0)
