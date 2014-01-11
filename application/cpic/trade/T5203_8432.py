# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   004203_8203.py
#   ����˵��:   [8432--6000901]����Ͷ������
#   �޸�ʱ��:   2006-04-06
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaAhAdb
import AfaHostFunc,AfaDBFunc
from types import *

def SubModuleDoFst( ):
    #���״���
    TradeContext.tradeCode = TradeContext.TransCode
    #TradeContext.Amount = ""
    AfaLoggerFunc.tradeInfo( '����������Ԥ��ѯ' )
    sql = "select corpserno,workdate,worktime,userno,amount,tellerno,brno,note5 "
    sql = sql + "from afa_maintransdtl where agentserialno = '"+TradeContext.PreSerialno+"'"
    sql = sql + "and workdate = '"+TradeContext.workDate+"'"
    sql = sql + " and revtranf = '0' and bankstatus = '0' and corpstatus = '0' and chkflag = '9'"
    AfaLoggerFunc.tradeInfo('�����ײ�ѯ���'+ sql)
    records = AfaDBFunc.SelectSql( sql )
    if(len(records) < 1):
        TradeContext.errorCode,TradeContext.errorMsg = "0001","�޴˽���"
        return False
    else:
        if(records[0][5] != TradeContext.tellerno):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","ԭ���׷Ǳ���Ա�������������˽���"
            return False
        if(records[0][6] != TradeContext.brno):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","ԭ���׷Ǳ������������������˽���"
            return False
        #ԭ���׵�̫����ˮ��
        TradeContext.PreCpicno = records[0][0]
        #ԭ��������
        TradeContext.PreWorkDate = records[0][1]
        #ԭ����ʱ��
        TradeContext.PreWorktime = records[0][2]
        #������
        TradeContext.userno = records[0][3]
        TradeContext.CpicNo = records[0][3]
        #���
        TradeContext.amount = records[0][4]
        #������(������)�뱣�յ��Ų�ͬ
        TradeContext.PolNumber = records[0][7]
        #��ˮ��
        TradeContext.preAgentSerno = TradeContext.PreSerialno
    return True
def SubModuleDoSnd( ):
    AfaLoggerFunc.tradeInfo('����ɷѷ�����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']�������ͨѶ����' )
    try:
        
        Party3Context.preAgentSerno = TradeContext.preAgentSerno
        Party3Context.Amount        = TradeContext.amount        
        Party3Context.workDate      = TradeContext.workDate      

        names = Party3Context.getNames( )
        for name in names:
            value = getattr( Party3Context, name )
            setattr( TradeContext, name, value )
            #AfaLoggerFunc.tradeInfo("�ֶ�����  ["+str(name)+"] =  "+str(value))

        if( TradeContext.errorCode != '0000' ):
            AfaLoggerFunc.tradeInfo("̫�����ش������ ["+TradeContext.errorCode+"]")
            AfaLoggerFunc.tradeInfo("̫�����ش�����Ϣ ["+TradeContext.errorMsg+"]")
            #����������ʧ�ܺ��¼������ʹ�����Ϣ
            if not AfaAhAdb.ADBUpdateTransdtlRev( ):
                raise AfaFlowControl.accException()
        return True
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))

def SubModuleDoTrd( ):
    return True
