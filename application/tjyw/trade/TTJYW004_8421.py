# -*- coding: gbk -*-
##################################################################
# ժ    Ҫ��TTJYW004_8421.py  ͨ��ҵ��������ѯ
# ��ǰ�汾��1.0
# ��    �ߣ�������
# ������ڣ�2011��03��08��
##################################################################
import TradeContext,AfaLoggerFunc,AfaFunc,AfaFlowControl,AfaDBFunc,HostContext,AfaHostFunc
from types import *

def SubModuleDoFst( ):
    try:
        AfaLoggerFunc.tradeInfo('--------------ͨ��ҵ��������ѯ��ʼ--------------------')
        
        #��Ա��ˮ���м�ҵ����ˮ����ϵ�绰�����׻������������ڡ�����ʱ�䡢�ɿ����������ɿ��� ���ɿ����˺š��տ����˺š�����
        sql = "select bankserno,agentserialno,note1,brno,workdate,worktime,username,cast(amount as decimal(15,2)),draccno,craccno,currtype from afa_maintransdtl"
        sql = sql + " where agentserialno = '" + TradeContext.agentserialno + "'"
        sql = sql + " and        workdate = '" + TradeContext.workdate      + "'"
        
        #20120820�º�ע�ͣ�sysId �ֶβ���Ҫ����ˮ�ź����ڿ�Ψһȷ��һ�ʽ���
        #sql = sql + " and           sysid = '" + TradeContext.sysId         + "'"
        
        sql = sql + " and revtranf = '0' and bankstatus='0'"
        
        AfaLoggerFunc.tradeInfo('������ѯ���'+ sql)
        
        records = AfaDBFunc.SelectSql( sql )
        
        if records == None:
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"��ѯ���ݿ�ʧ��"
            return False
        elif len(records) == 0:
            TradeContext.errorCode,TradeContext.errorMsg = "0001","û�иñʽɷѼ�¼"
            AfaLoggerFunc.tradeInfo('û�иñʽɷѼ�¼')
            return False
        else:
            TradeContext.O1TLSQ	   = str(records[0][0]).strip()                 #��Ա��ˮ
            TradeContext.SERIALNO  = str(records[0][1]).strip()                 #�м�ҵ����ˮ
            TradeContext.PHONE	   = str(records[0][2]).strip()                 #��ϵ�绰
            TradeContext.BANKNAME  = str(records[0][3]).strip()                 #���׻���
            TradeContext.TransDate = str(records[0][4]).strip()                 #��������
            TradeContext.TransTime = str(records[0][5]).strip()                 #����ʱ��
            TradeContext.PYRNAM	   = str(records[0][6]).strip()                 #�ɿ�������
            TradeContext.OCCAMT	   = str(records[0][7]).strip()                 #�ɿ���
            TradeContext.PYRACCNO  = str(records[0][8]).strip()                 #�ɿ����˺�
            TradeContext.REVACCNO  = str(records[0][9]).strip()                 #�տ����˺�
            TradeContext.CUR       = str(records[0][10]).strip().rjust(2,'0')   #����

        #����8810��ѯ�տ����˻���Ϣ
        HostContext.I1TRCD="8810"
        HostContext.I1SBNO=""
        HostContext.I1USID="999996"
        HostContext.I1AUUS=""
        HostContext.I1AUPS=""
        HostContext.I1WSNO=""
        HostContext.I1ACNO=TradeContext.REVACCNO
        HostContext.I1CYNO="01"
        HostContext.I1CFFG=""
        HostContext.I1PSWD=""
        HostContext.I1CETY=""
        HostContext.I1CCSQ=""
        HostContext.I1CTFG="0"
        AfaHostFunc.CommHost("8810")
        
        if(TradeContext.errorCode!="0000"):
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"�����Ĳ�ѯ�Թ��˻���Ϣʧ��" 
            return False
        else:
            AfaLoggerFunc.tradeInfo( '>>>>��ѯ�˻���Ϣ�ɹ�' )
            TradeContext.REVNAME = HostContext.O1ACNM            #�տ��˻���
            TradeContext.REVBANK = HostContext.O1OPNT            #�տ��˿�����
        if len(TradeContext.PYRACCNO) != 0:
            #����8810��ѯ�ɿ����˻���Ϣ
            HostContext.I1TRCD="8810"
            HostContext.I1SBNO=""
            HostContext.I1USID="999996"
            HostContext.I1AUUS=""
            HostContext.I1AUPS=""
            HostContext.I1WSNO=""
            HostContext.I1ACNO=TradeContext.PYRACCNO
            HostContext.I1CYNO="01"
            HostContext.I1CFFG=""
            HostContext.I1PSWD=""
            HostContext.I1CETY=""
            HostContext.I1CCSQ=""
            HostContext.I1CTFG="0"
            AfaHostFunc.CommHost("8810")
            
            if(TradeContext.errorCode!="0000"):
                TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"�����Ĳ�ѯ�ɿ����˻���Ϣʧ��" 
                return False
            else:
                AfaLoggerFunc.tradeInfo( '>>>>��ѯ�˻���Ϣ�ɹ�' )
                TradeContext.SNDBNKNM = HostContext.O1OPNT            #�տ��˿�����
            
        #��ȡժҪ����
        if not AfaFunc.GetSummaryInfo( ):
            return False
        else:
            TradeContext.SUMMARY = TradeContext.__summaryName__               #ժҪ
            
        AfaLoggerFunc.tradeInfo('---------------ͨ��ҵ��������ѯ����--------------------')
        
        return True 
    except  Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        TradeContext.errorMsg = str(e)
        AfaFlowControl.flowException( )
    
    
     