# -*- coding: gbk -*-
###############################################################################
# �ļ����ƣ�ahjf_admin.py
# ժ    Ҫ�����ս�����Ŀ����
# ��ǰ�汾��1.0
# ��    �ߣ�
# ������ڣ�2011��01��21��
###############################################################################
import TradeContext

TradeContext.sysType = 'ahjf'

import ConfigParser, sys, AfaDBFunc, os,HostContext,AfaUtilTools,AfaAdminFunc
from types import *



##########################################���ʴ���##########################################
def SendToCorp(sysId,unitNo,trxDate):

    try:
        #���н�����ˮ�����н�������,���н���ʱ�䣬�����������,�����������Ա������������ҵ�����ͣ�������������������,�����������ţ�
        #�������,���������֣��������˺ţ����������У���������ɽ��ܽ��
        sqlStr = "SELECT agentserialno,workDate,workTime,brno,tellerno,note1,agentflag,channelcode,note7,userno,note3,username,"
        sqlStr = sqlStr + "draccno,note6,note4,note5,amount from afa_maintransdtl where "
        sqlStr = sqlStr + " SYSID = '"        + sysId    + "'"
        sqlStr = sqlStr + " AND UNITNO = '"   + unitNo   + "'"
        sqlStr = sqlStr + " AND WORKDATE='"   + trxDate  + "'"
        sqlStr = sqlStr + " and revtranf = '0' and bankstatus = '0' and ChkFlag = '0'"

        AfaAdminFunc.WrtLog(sqlStr)

        records = AfaDBFunc.SelectSql( sqlStr )
        if (records==None):
            AfaAdminFunc.WrtLog('>>>������:���ɶ��ʴ���ʧ��,���ݿ��쳣')
            return False

        if (len(records)==0):
            AfaAdminFunc.WrtLog('>>>������:û���κ���ˮ��Ϣ,����Ҫ����ҵ���ж���,��Ƽ���Աȷ��')
            return False


        #���������ļ�
        localFileName = 'DOC_012' + '_' + trxDate + '_' + TradeContext.workTime  + '.txt'

        AfaAdminFunc.WrtLog(localFileName)

        dzfp= open(TradeContext.CORP_LDIR + '/' + localFileName,  "w")
        
        totalnum = 0
        totalamt = 0
        
        chuFaLeiBie = ''
        for i in range(0, len(records)):
            tmpStr = ""
            #���н�����ˮ
            tmpStr = tmpStr + records[i][0].strip() +  chr(05)
            #���н�������
            tmpStr = tmpStr + records[i][1].strip() +  chr(05)
            #���н���ʱ��
            tmpStr = tmpStr + records[i][2].strip() +  chr(05)
            #�����������
            tmpStr = tmpStr + records[i][3].strip() +  chr(05)
            #�����������Ա
            tmpStr = tmpStr + records[i][4].strip() +  chr(05)
            #��������
            tmpStr = tmpStr + records[i][5].strip() +  chr(05)
            #ҵ������
            #tmpStr = tmpStr + records[i][6].strip() +  chr(05)
            tmpStr = tmpStr + '00' +  chr(05)
            #��������
            #tmpStr = tmpStr + records[i][7].strip() +  chr(05)
            tmpStr = tmpStr + '00' +  chr(05) 
            #��������
            tmpStr = tmpStr + records[i][8].strip() +  chr(05)
            #������������
            tmpStr = tmpStr + records[i][9].strip() +  chr(05)
            #�������
            #tmpStr = tmpStr + records[i][10].strip() +  chr(05)
            tmpStr = tmpStr + '' +  chr(05)
            #����������
            tmpStr = tmpStr + records[i][11].strip() +  chr(05)
            #�������˺�
            tmpStr = tmpStr + records[i][12].strip() +  chr(05)
            #����������
            tmpStr = tmpStr + records[i][13].strip() +  chr(05)
            #������
            tmpStr = tmpStr + records[i][14].strip() +  chr(05)
            #���ɽ�
            tmpStr = tmpStr + records[i][15].strip() +  chr(05)
            #�ܽ��
            tmpStr = tmpStr + records[i][16].strip() +  chr(05)
            tmpStr = tmpStr +"\n"
            dzfp.write(tmpStr)

            totalnum = totalnum + 1
            totalamt = totalamt + (float)(records[i][16].strip())

        dzfp.close()

        sqlStr = "update afa_maintransdtl set corpchkflag = '0' where "
        sqlStr = sqlStr + " SYSID       ='"     +  sysId   +"'"
        sqlStr = sqlStr + " AND WORKDATE='"     + trxDate  + "'"
        sqlStr = sqlStr + " and revtranf = '0' and bankstatus = '0' and ChkFlag = '0'"
        
        AfaAdminFunc.WrtLog(sqlStr)
        
        if not AfaDBFunc.UpdateSqlCmt(sqlStr):
            AfaAdminFunc.WrtLog('>>>������:������ҵ���˱�ʶʧ��')
            return False

        AfaAdminFunc.WrtLog('>>>������:���ʴ���ɹ�[�ܱ���='+str(totalnum) + ',�ܽ��=' + str(totalamt) + ']')
        
       
        #�ļ��ֽڳ���
        TradeContext.DZFILESIZE = str(os.path.getsize(TradeContext.CORP_LDIR + '/' + localFileName))
        #�����ļ���
        rfileName = 'DOC_012' + '_' + trxDate + '_' + TradeContext.workTime + '_' + TradeContext.DZFILESIZE + '.txt'

        #�ܱ���
        TradeContext.DZNUM = str(totalnum)

        #�ܽ��
        TradeContext.DZAMT = str(totalamt)
        
        if not AfaAdminFunc.PutDzFile(sysId, localFileName, rfileName):
            return False

        return True

    except Exception, e:
        AfaAdminFunc.WrtLog(str(e))
        AfaAdminFunc.WrtLog('���ʴ����쳣')
        return False
        
###########################################������###########################################
if __name__=='__main__':

    AfaAdminFunc.WrtLog( '**********���ս������˲�����ʼ**********' )
    
    TradeContext.workTime=AfaUtilTools.GetSysTime( )
    
    if ( len(sys.argv) in (3,4)):
    
        sSysId1     = sys.argv[1]          #ҵ�����
        sUnitno1    = sys.argv[2]          #��˾����
        if ( len(sys.argv) == 3 ):
            #sTrxDate = '20110704'
            sTrxDate = AfaUtilTools.GetSysDate( ) 
        else:
            sTrxDate = sys.argv[3]          #��������
        
        if ( sSysId1 == 'AG2017' ):
            AfaAdminFunc.WrtLog('>>>���ս������ʿ�ʼ') 
        
        else:
            AfaAdminFunc.WrtLog('>>>�޴�ҵ�����ͣ��������') 
            sys.exit(-1)
            
        AfaAdminFunc.WrtLog('ϵͳ���� = ' + sSysId1)
        AfaAdminFunc.WrtLog('��λ���� = ' + sUnitno1)
        AfaAdminFunc.WrtLog('�������� = ' + sTrxDate)
            
        #��ȡ�����ļ�
        if ( not AfaAdminFunc.GetAdminConfig(sSysId1 + "_AHJF") ) :
            AfaAdminFunc.WrtLog('>>>��ȡ�����ļ�ʧ��') 
            sys.exit(-1)
        
        #����������
        AfaAdminFunc.WrtLog('>>>���������ʿ�ʼ')
        if not AfaAdminFunc.MatchData(sSysId1,sUnitno1,sTrxDate):
            AfaAdminFunc.WrtLog('>>>����������ʧ�ܣ�������ֹ') 
            sys.exit(-1)
        AfaAdminFunc.WrtLog('>>>���������ʽ���')
        
        #����ҵ����
        AfaAdminFunc.WrtLog('>>>����ҵ���ʶ��˿�ʼ')
        if not SendToCorp(sSysId1,sUnitno1,sTrxDate):
            AfaAdminFunc.WrtLog('>>>����ҵ����ʧ�ܣ�������ֹ')
            sys.exit(-1)
        AfaAdminFunc.WrtLog('>>>����ҵ���ʶ��˽���')
        
        
    else:
        print( '�÷�1: jtfk_Proc sysid1 unitno1 date')
        sys.exit(-1)

    AfaAdminFunc.WrtLog( '**********���ս������˲�������**********' )

    sys.exit(0)
