# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   TYBT003_8615.py
#   ����˵��:   ���ճ������±��ɷѳ�����
#   �޸�ʱ��:   2010-7-30
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaYbtdb
import AfaHostFunc,AfaDBFunc
from types import *

def SubModuleDoFst( ):
    
    #���״���
    TradeContext.tradeCode = TradeContext.TransCode
    
    AfaLoggerFunc.tradeInfo( '����������Ԥ��ѯ����ѯ�Ƿ��д��±��ɷ�' )
   
    sql = "select workdate,worktime,userno,tellerno,brno,note9,unitno,amount,trxcode from afa_maintransdtl"
    sql = sql + " where agentserialno = '"+TradeContext.PreSerialno+"' and workdate = '"+TradeContext.workDate+"' and trxcode='8611'"
    sql = sql + " and revtranf = '0' and bankstatus = '0' and corpstatus = '0' and chkflag = '9'"
    
    AfaLoggerFunc.tradeInfo('�����ײ�ѯ��䣺'+ sql)
   
    records = AfaDBFunc.SelectSql( sql )
    
    AfaLoggerFunc.tradeInfo('�����ײ�ѯ�Ľ����'+ str(records))
    
    if records == None:
        TradeContext.errorCode,TradeContext.errorMsg = "0001","�����ײ�ѯ����ͨ����ʧ��"
        raise AfaFlowControl.flowException( )
    
    elif(len(records) < 1):
        TradeContext.errorCode,TradeContext.errorMsg = "0001","�޴˽���"
        return False
    
    else:
        if(records[0][3] != TradeContext.tellerno):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","ԭ���׷Ǳ���Ա�������������˽���"
            return False
        
        if(records[0][4] != TradeContext.brno):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","ԭ���׷Ǳ������������������˽���"
            return False
        
        if(records[0][6] != TradeContext.unitno):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","��ԭ���ױ��չ�˾�������������˽���"
            return False
        
        if(records[0][7].strip() != TradeContext.amount.strip()):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","��ԭ���׽������������˽���"
            return False
        
        if(records[0][5].split('|')[2] != TradeContext.policy):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","��ԭ���ױ��յ��Ų������������˽���"
            return False
    
        #ԭ��������
        TradeContext.PreWorkDate = records[0][0]
        
        #ԭ����ʱ��
        TradeContext.PreWorktime = records[0][1]
        
        #ԭ������
        TradeContext.PreTrxCode = records[0][8]
        
        #���
        TradeContext.amount = records[0][7]
        
        #����ӡˢ��
        TradeContext.userno = records[0][2]
        
        #ԭ������ˮ��
        TradeContext.preAgentSerno = TradeContext.PreSerialno
        
        #Ͷ������
        TradeContext.applno =records[0][5].split('|')[1]
        
        return True

def SubModuleDoSnd( ):
    AfaLoggerFunc.tradeInfo('���뵱�ճ���[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']�������ͨѶ����' )
    
    try:
        names = Party3Context.getNames( )
        
        for name in names:
            value = getattr( Party3Context, name )
            if ( not name.startswith( '__' ) and type(value) is StringType) :
                setattr( TradeContext, name, value )
            

        if( TradeContext.errorCode != '0000' ):
            
            AfaLoggerFunc.tradeInfo("����ͨ���ش������ ["+TradeContext.errorCode+"]")
            AfaLoggerFunc.tradeInfo("����ͨ���ش�����Ϣ ["+TradeContext.errorMsg+"]")
            
            #����������ʧ�ܺ��¼������ʹ�����Ϣ
            if not AfaYbtdb.ADBUpdateTransdtlRev( ):
                raise AfaFlowControl.accException()
        
        return True
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))

def SubModuleDoTrd( ):
    return True
