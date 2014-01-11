# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   5204_8438.py
#   ����˵��:   [�����ײ�ѯ]
#   �޸�ʱ��:   2009-04-07
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaDBFunc
import AfaHostFunc
from types import *

def SubModuleDoFst( ):
    AfaLoggerFunc.tradeInfo( '��ʼ�����ױ���' )
    AfaLoggerFunc.tradeInfo( '�����ױ���ֵ����Ч��У��' )
    if( not TradeContext.existVariable( "PreSerialno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', 'ԭ������ˮ��[PreSerialno]ֵ������!' )
    if( not TradeContext.existVariable( "channelCode" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '��������[channelCode]ֵ������!' )
    if( TradeContext.channelCode == '005' ):
        if( not TradeContext.existVariable( "tellerno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '��Ա��[tellerno]ֵ������!' )
        if( not TradeContext.existVariable( "brno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '�����[brno]ֵ������!' )
        if( not TradeContext.existVariable( "termid" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '��Ա��[termid]ֵ������!' )
    return True
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('���뷴��ѯ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
        sql = "select userno,username,amount,draccno,tellerno,craccno,subuserno,note8,note9,note10,note1,unitno,note7 "
        sql = sql + "from afa_maintransdtl where agentserialno = '"+TradeContext.PreSerialno+"'"
        sql = sql + "and workdate = '"+TradeContext.workDate+"'"
        sql = sql + " and revtranf = '0' and bankstatus = '0' and corpstatus = '0' and chkflag = '9'"
        AfaLoggerFunc.tradeInfo('�����ײ�ѯ���'+ sql)
        records = AfaDBFunc.SelectSql( sql )
        if(len(records) < 1):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","�޴˽���"
            return False
        else:
            #if(records[0][4] != TradeContext.tellerno):
            #    TradeContext.errorCode,TradeContext.errorMsg = "0001","ԭ���׷Ǳ���Ա�������������˽���"
            #    return False
            #�û����(���յ���)
            TradeContext.CpicNo = records[0][0]
            AfaLoggerFunc.tradeInfo("���յ���"+str(TradeContext.CpicNo))
            #�û�����
            #TradeContext.UserName = records[0][1]
            #���
            TradeContext.Amount = records[0][2]
            AfaLoggerFunc.tradeInfo("���"+str(TradeContext.Amount))
            #�ɷ�����(��������)/�ʺ�
            if(type(records[0][3]) is str):
                TradeContext.Accno = records[0][3]
                #TradeContext.backtype = "1"
            else:
                TradeContext.Accno = ""
                #TradeContext.backtype = "0"
            #�����ʺ�
            TradeContext.crAccno = records[0][5]
            #Ͷ�����֤
            #TradeContext.GovtID = records[0][6]
            #Ͷ������|��������
            arrayList = ""
            arrayList = (records[0][7]).split("|")
            TradeContext.IntialNum = arrayList[0].strip()
            TradeContext.ProCodeStr = arrayList[1].strip()
            #Ͷ��������|Ͷ�������֤����
            arrayList = ""
            arrayList = (records[0][8]).split("|")
            TradeContext.UserName = arrayList[0].strip()
            TradeContext.GovtID   = arrayList[1].strip()
            AfaLoggerFunc.tradeInfo("Ͷ��������"+str(TradeContext.UserName))
            #����������|���������֤
            arrayList = ""
            arrayList = (records[0][9]).split("|")
            TradeContext.FullName = arrayList[1].strip()
            TradeContext.GovtIDF  = arrayList[2].strip()
            AfaLoggerFunc.tradeInfo("����������"+str(TradeContext.FullName))
            #������
            TradeContext.CpciPNo  = records[0][10].strip()
            #��λ����
            TradeContext.unitno  = records[0][11].strip()
            #����
            TradeContext.ProCode = records[0][12].strip()
            #���׷�����
            TradeContext.errorCode = '0000'
        AfaLoggerFunc.tradeInfo('�˳�����ѯ����' )
        return True
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
