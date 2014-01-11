# -*- coding: gbk -*-
###############################################################################
# �ļ����ƣ�ybt_admin.py
# ժ    Ҫ��������������ͨ����
# ��ǰ�汾��1.0
# ��    �ߣ�CYG
# ������ڣ�2010��08��13��
###############################################################################
import TradeContext

TradeContext.sysType = 'cron'

import ConfigParser, sys, AfaDBFunc, os, YbtAdminFunc,HostContext,YbtFunc,AfaUtilTools
from types import *


fileNameHead = 'ANHNX00001'
##########################################���ʴ���##########################################
def SendToCorp(sysId,unitNo,sysId2,unitNo2,trxDate):

    try:
        #��������,����������,,������ˮ��,������,���
        sqlStr = "SELECT workdate,brno,agentserialno,note5,amount,sysid,note9,trxcode from afa_maintransdtl where "
        sqlStr = sqlStr + " ((SYSID = '"        + sysId    + "'"
        sqlStr = sqlStr + " AND UNITNO = '"   + unitNo   + "')"
        sqlStr = sqlStr + " OR (SYSID = '"        + sysId2    + "'"
        sqlStr = sqlStr + " AND UNITNO = '"   + unitNo2   + "'))"
        sqlStr = sqlStr + " AND WORKDATE='"     + trxDate  + "'"
        sqlStr = sqlStr + " and revtranf = '0' and bankstatus = '0' and ChkFlag = '0'"

        YbtAdminFunc.WrtLog(sqlStr)

        records = AfaDBFunc.SelectSql( sqlStr )
        if (records==None):
            YbtAdminFunc.WrtLog('>>>������:���ɶ��ʴ���ʧ��,���ݿ��쳣')
            return False

        if (len(records)==0):
            YbtAdminFunc.WrtLog('>>>������:û���κ���ˮ��Ϣ,����Ҫ����ҵ���ж���,��Ƽ���Աȷ��')
            return False


        #���������ļ�
        dzFileName = TradeContext.CORP_LDIR + '/' + sysId + "_" + unitNo + '_' + trxDate + '.txt'

        YbtAdminFunc.WrtLog(dzFileName)

        dzfp= open(dzFileName,  "w")
        
        totalnum = 0
        totalamt = 0
        
        chuFaLeiBie = ''
        for i in range(0, len(records)):
            tmpStr = ""
            #���б���
            tmpStr = tmpStr + "01"                  + "|"
            #��������
            tmpStr = tmpStr + records[i][0].strip() + "|"
            #�����������
            tmpStr = tmpStr + "ANHNX00001"          + "|"
            #����������
            tmpStr = tmpStr + records[i][1].strip() + "|"
            #������
            if records[i][5] == 'AG2011':
                tmpStr = tmpStr + "6000113"         + "|"
            elif records[i][5] == 'AG2013':
                #����ͨ��������ת���ɱ��չ�˾��Ӧ�Ľ�����
                filename = '/home/maps/afa/application/ybt/config/busino_' + unitNo2 + '.conf'    #�����ļ���
                transcode =  YbtFunc.datamap( "TransCode",records[i][7],filename )
                tmpStr = tmpStr + transcode         + "|"
            #������ˮ��
            tmpStr = tmpStr + records[i][2].strip() + "|"
            #������
            if records[i][5] == 'AG2011':
                tmpStr = tmpStr + records[i][3].strip()  + "|"
            elif records[i][5] == 'AG2013':
                items = records[i][6].split('|')
                if len(items) >= 4:
                    tmpStr = tmpStr + items[2]      + "|"
                else:
                    tmpStr = tmpStr + ""            + "|"
            #���
            tmpStr = tmpStr + records[i][4].strip() + "|"
            #��������
            tmpStr = tmpStr + "01|\n"
            
            dzfp.write(tmpStr)

            totalnum = totalnum + 1
            totalamt = totalamt + (float)(records[i][4].strip())

        dzfp.close()

        sqlStr = "update afa_maintransdtl set corpchkflag = '0' where "
        sqlStr = sqlStr + " SYSID in ('"        + sysId    + "','" +  sysId2 + "')"
        sqlStr = sqlStr + " AND UNITNO in ('"   + unitNo   + "','" + unitNo2 + "')"
        sqlStr = sqlStr + " AND WORKDATE='"     + trxDate  + "'"
        sqlStr = sqlStr + " and revtranf = '0' and bankstatus = '0' and ChkFlag = '0'"
        
        YbtAdminFunc.WrtLog(sqlStr)
        
        if not AfaDBFunc.UpdateSqlCmt(sqlStr):
            YbtAdminFunc.WrtLog('>>>������:������ҵ���˱�ʶʧ��')
            return False

        YbtAdminFunc.WrtLog('>>>������:���ʴ���ɹ�[�ܱ���='+str(totalnum) + ',�ܽ��=' + str(totalamt) + ']')

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

        if not YbtAdminFunc.PutDzFile(sysId, lfileName, rfileName):
            return False

        return True

    except Exception, e:
        YbtAdminFunc.WrtLog(str(e))
        YbtAdminFunc.WrtLog('���ʴ����쳣')
        return False
        
###########################################������###########################################
if __name__=='__main__':

    YbtAdminFunc.WrtLog( '**********������������ͨ���˲�����ʼ**********' )
    
    if ( len(sys.argv) in (3,4)):
    
        sSysId1     = sys.argv[1]          #ҵ�����
        sUnitno1    = sys.argv[2]          #���չ�˾����
        if ( len(sys.argv) == 3 ):
            sTrxDate = AfaUtilTools.GetSysDate( ) 
        else:
            sTrxDate = sys.argv[3]          #��������
        
        if ( sSysId1 == 'AG2011' ):
            YbtAdminFunc.WrtLog('>>>�ű�ͨ���ʿ�ʼ') 
        elif ( sSysId1 == 'AG2013' ):
            YbtAdminFunc.WrtLog('>>>����ͨ���ʿ�ʼ') 
        else:
            YbtAdminFunc.WrtLog('>>>�޴�ҵ�����ͣ��������') 
            sys.exit(-1)
            
        YbtAdminFunc.WrtLog('ϵͳ���� = ' + sSysId1)
        YbtAdminFunc.WrtLog('��λ���� = ' + sUnitno1)
        YbtAdminFunc.WrtLog('�������� = ' + sTrxDate)
            
        #��ȡ�����ļ�
        if ( not YbtAdminFunc.GetAdminConfig(sSysId1 + "_" + sUnitno1) ) :
            YbtAdminFunc.WrtLog('>>>��ȡ�����ļ�ʧ��') 
            sys.exit(-1)
        
        #����������
        YbtAdminFunc.WrtLog('>>>���������ʿ�ʼ')
        if not YbtAdminFunc.MatchData(sSysId1,sUnitno1,sTrxDate):
            YbtAdminFunc.WrtLog('>>>����������ʧ�ܣ�������ֹ') 
            sys.exit(-1)
        YbtAdminFunc.WrtLog('>>>���������ʽ���')
        
        #����ҵ����
        YbtAdminFunc.WrtLog('>>>����ҵ���ʶ��˿�ʼ')
        if not SendToCorp(sSysId1,sUnitno1,sSysId1,sUnitno1,sTrxDate):
            YbtAdminFunc.WrtLog('>>>����ҵ����ʧ�ܣ�������ֹ')
            sys.exit(-1)
        YbtAdminFunc.WrtLog('>>>����ҵ���ʶ��˽���')
        
    elif ( len(sys.argv) in (5,6)):
    
        YbtAdminFunc.WrtLog('>>>�ű�ͨ������ͨ���ʿ�ʼ') 
        sSysId1     = sys.argv[1]          #ҵ�����
        sUnitno1    = sys.argv[2]          #���չ�˾����
        sSysId2     = sys.argv[3]          #ҵ�����
        sUnitno2    = sys.argv[4]          #���չ�˾����
        if ( len(sys.argv) == 5 ):
            sTrxDate = AfaUtilTools.GetSysDate( )  
        else:
            sTrxDate = sys.argv[5]          #��������
        
        YbtAdminFunc.WrtLog('�ű�ͨϵͳ���� = ' + sSysId1)
        YbtAdminFunc.WrtLog('�ű�ͨ��λ���� = ' + sUnitno1)
        YbtAdminFunc.WrtLog('����ͨϵͳ���� = ' + sSysId2)
        YbtAdminFunc.WrtLog('����ͨ��λ���� = ' + sUnitno2)
        YbtAdminFunc.WrtLog('��  ��  ��  �� = ' + sTrxDate)
        
        #��ȡ�����ļ�
        if ( not YbtAdminFunc.GetAdminConfig(sSysId1 + "_" + sUnitno1) ) :
            YbtAdminFunc.WrtLog('>>>��ȡ�����ļ�ʧ��') 
            sys.exit(-1)
        
        #�ű�ͨ����������
        YbtAdminFunc.WrtLog('>>>�ű�ͨ���������ʿ�ʼ')
        if not YbtAdminFunc.MatchData(sSysId1,sUnitno1,sTrxDate):
            if (HostContext.O1MGID == 'TXT0001' or TradeContext.serialFlag == '0'):
                YbtAdminFunc.WrtLog('>>>����û�з����ű�ͨ������Ϣ') 
            else:
                YbtAdminFunc.WrtLog('>>>�ű�ͨ����������ʧ�ܣ�������ֹ') 
                sys.exit(-1)
        YbtAdminFunc.WrtLog('>>>�ű�ͨ���������ʽ���')
        
        #����ͨ����������
        YbtAdminFunc.WrtLog('>>>����ͨ���������ʿ�ʼ')
        if not YbtAdminFunc.MatchData(sSysId2,sUnitno2,sTrxDate):
            if (HostContext.O1MGID == 'TXT0001' or TradeContext.serialFlag == '0'):
                YbtAdminFunc.WrtLog('>>>����û�з�������ͨ������Ϣ') 
            else:
                YbtAdminFunc.WrtLog('>>>����ͨ����������ʧ�ܣ�������ֹ') 
                sys.exit(-1)
        YbtAdminFunc.WrtLog('>>>����ͨ���������ʽ���')
        
        #����ҵ����
        YbtAdminFunc.WrtLog('>>>����ҵ���ʶ��˿�ʼ')
        if not SendToCorp(sSysId1,sUnitno1,sSysId2,sUnitno2,sTrxDate):
            YbtAdminFunc.WrtLog('>>>����ҵ����ʧ�ܣ�������ֹ')
            sys.exit(-1)
        YbtAdminFunc.WrtLog('>>>����ҵ���ʶ��˽���')
        
    else:
        print( '�÷�1: jtfk_Proc sysid1 unitno1 date                 ��ֻ���ű�ͨ��������ͨ���ˣ�')
        print( '�÷�2: jtfk_Proc sysid1 unitno1 sysid2 unitno2 date  ��ͬʱ���ű�ͨ������ͨ���ˣ�')
        sys.exit(-1)

    YbtAdminFunc.WrtLog( '**********������������ͨ���˲�������**********' )

    sys.exit(0)
