# -*- coding: gbk -*-
###############################################################################
# �ļ����ƣ�AbdtSq.py
# �ļ���ʶ��
# ժ    Ҫ�������ļ�����
#
# ��ǰ�汾��2.0
# ��    �ߣ�XZH
# ������ڣ�2008��06��10��
#
# ȡ���汾��
# ԭ �� �ߣ�
# ������ڣ�
###############################################################################
import time,AfaDBFunc,TradeContext,os,AfaUtilTools,AbdtManager
from types import *



#=========================������==============================================
def MainSQ_Proc( ):
    
    #��ȡ��ǰϵͳʱ��
    TradeContext.WorkDate=AfaUtilTools.GetSysDate( )
    TradeContext.WorkTime=AfaUtilTools.GetSysTime( )

    AbdtManager.WrtLog('>>>����=' + TradeContext.WorkDate + ' ʱ��=' + TradeContext.WorkTime)

    #��ѯ������������Ϣ
    try:
        sql = ""

        #10-���� 11-���������� 20-���������� 21-���ύ 22-���ύ 30-����� 31-������� 32-����� 40-���� 88-�������
        sql = "SELECT * FROM ABDT_BATCHINFO WHERE STATUS IN ('10')"
        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AbdtManager.WrtLog( AfaDBFunc.sqlErrMsg )
            return AbdtManager.ExitThisFlow( '9000', '��ѯ��Ҫ�����������Ϣ�쳣')


        if ( len(records) == 0 ):
            return AbdtManager.ExitThisFlow( '9000', 'û����Ҫ�����������Ϣ')


        AbdtManager.WrtLog('>>>�ܹ���[' + str(len(records)) + ']�����������μ�¼')

        i = 0
        while ( i  < len(records) ):
            TradeContext.BATCHNO     = str(records[i][0]).strip()          #ί�к�(���κ�)
            TradeContext.APPNO       = str(records[i][1]).strip()          #ҵ����
            TradeContext.BUSINO      = str(records[i][2]).strip()          #��λ���
            TradeContext.ZONENO      = str(records[i][3]).strip()          #������
            TradeContext.BRNO        = str(records[i][4]).strip()          #�����
            TradeContext.USERNO      = str(records[i][5]).strip()          #����Ա
            TradeContext.ADMINNO     = str(records[i][6]).strip()          #����Ա
            TradeContext.TERMTYPE    = str(records[i][7]).strip()          #�ն�����
            TradeContext.FILENAME    = str(records[i][8]).strip()          #�ϴ��ļ���
            TradeContext.INDATE      = str(records[i][9]).strip()          #��������
            TradeContext.INTIME      = str(records[i][10]).strip()         #����ʱ��
            TradeContext.BATCHDATE   = str(records[i][11]).strip()         #�ύ����
            TradeContext.BATCHTIME   = str(records[i][12]).strip()         #�ύʱ��
            TradeContext.TOTALNUM    = str(records[i][13]).strip()         #�ܱ���
            TradeContext.TOTALAMT    = str(records[i][14]).strip()         #�ܽ��
            TradeContext.SUCCNUM     = str(records[i][15]).strip()         #�ɹ�����
            TradeContext.SUCCAMT     = str(records[i][16]).strip()         #�ɹ����
            TradeContext.FAILNUM     = str(records[i][17]).strip()         #ʧ�ܱ���
            TradeContext.FAILAMT     = str(records[i][18]).strip()         #ʧ�ܽ��
            TradeContext.STATUS      = str(records[i][19]).strip()         #״̬
            TradeContext.STARTDATE   = str(records[i][20]).strip()         #��Ч����
            TradeContext.ENDDATE     = str(records[i][21]).strip()         #ʧЧ����
            TradeContext.PROCMSG     = str(records[i][22]).strip()         #������Ϣ
            TradeContext.NOTE1       = str(records[i][23]).strip()         #��ע1
            TradeContext.NOTE2       = str(records[i][24]).strip()         #��ע3
            TradeContext.NOTE3       = str(records[i][25]).strip()         #��ע3
            TradeContext.NOTE4       = str(records[i][26]).strip()         #��ע4
            TradeContext.NOTE5       = str(records[i][27]).strip()         #��ע5
            i=i+1


            AbdtManager.WrtLog('#################################')


            AbdtManager.WrtLog('����:APPNO=[' + TradeContext.APPNO + '],BATCHNO=[' + TradeContext.BATCHNO + ']')


            #��ѯ��λ��Ϣ
            if not AbdtManager.QueryBusiInfo() :
                AbdtManager.WrtLog( '�Զ�����,û�з��ֵ�λ��Ϣ' )
                AbdtManager.UpdateBatchInfo(TradeContext.BATCHNO, '40', '�Զ�����,û�з��ֵ�λ��Ϣ')
                continue

    
            if ( TradeContext.TERMTYPE == '0' ):
                #(�����ϴ��ļ�)
                AbdtManager.SQ_VMENU_Proc(TradeContext.BATCHNO)

            else:
                #ת��(��Χ�ϴ��ļ�)
                AbdtManager.SQ_OTHER_Proc(TradeContext.BATCHNO)

            AbdtManager.WrtLog('#################################')


    except Exception, e:
        AbdtManager.WrtLog( str(e) )
        return AbdtManager.ExitThisFlow( '9000', '��ѯ������Ϣ(����)�쳣')


###########################################������###########################################
if __name__=='__main__':

    AbdtManager.WrtLog('********************�������봦��ʼ********************')

    #��ȡ�����ļ�
    BatchConfig = AbdtManager.GetBatchConfig()

    #���봦��
    MainSQ_Proc( )
        

    AbdtManager.WrtLog('********************�������봦�����********************')
