# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   TTJYW003_8628.py
#   ����˵��:   ����������ɷѳ�������
#   �޸�ʱ��:   2011-01-21
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc,AfaAfeFunc,AfaFlowControl,Party3Context,AhjfFunc
import AfaHostFunc,AfaDBFunc
from types import *

def SubModuleDoFst( ):
    
    AfaLoggerFunc.tradeInfo( '����������Ԥ��ѯ����ѯ�Ƿ��д˽ɷѼ�¼' )
    try:
        sql = "select workdate,userno,tellerno,brno,amount from afa_maintransdtl"
        sql = sql + " where agentserialno = '"+TradeContext.preAgentSerno+"' and workdate = '"+TradeContext.workDate+"' and trxcode='8627'"
        sql = sql + " and revtranf = '0' and bankstatus = '0'and chkflag = '9'"
        
        AfaLoggerFunc.tradeInfo('�����ײ�ѯ��䣺'+ sql)
        
        records = AfaDBFunc.SelectSql( sql )
        AfaLoggerFunc.tradeInfo('�����ײ�ѯ�Ľ����'+ str(records))
        
        if records == None:
            TradeContext.errorCode,TradeContext.errorMsg = "0001","�����ײ�ѯ����ʧ��"
            raise AfaFlowControl.flowException( )
        elif(len(records) < 1):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","�޴˽���"
            return False
        else:
            if(records[0][1] != TradeContext.punishNo):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","��ԭ���׵Ĵ����������Ų�һ�£��������˽���"
                return False
            
            if(records[0][2] != TradeContext.tellerno):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","ԭ���׷Ǳ���Ա�������������˽���"
                return False
            if(records[0][3] != TradeContext.brno):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","ԭ���׷Ǳ������������������˽���"
                return False
            if(records[0][4].strip() != TradeContext.amount.strip()):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","��ԭ���׽������������˽���"
                return False
           
            TradeContext.orgDate       = records[0][0]                #ԭ��������
            TradeContext.punishNo      = records[0][1]                #������������ 
            TradeContext.userno        = records[0][1]                #��ʼ��userno��ֵ��ȡ���������ʱ��Ҫ
            TradeContext.amount        = records[0][4]                #��� 
            TradeContext.preAgentSerno = TradeContext.preAgentSerno   #ԭ������ˮ��
        TradeContext.note2             = TradeContext.busino          #ǩԼ��λ���
            
        return True     
    except  Exception, e:                     
        AfaLoggerFunc.tradeInfo( str(e) )     
        AfaFlowControl.flowException( )   
            
def SubModuleDoSnd( ):
    AfaLoggerFunc.tradeInfo('���볷������[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']�������ͨѶ����' )
    
    try:
        names = Party3Context.getNames( )
        
        for name in names:
            value = getattr( Party3Context, name )
            if ( not name.startswith( '__' ) and type(value) is StringType) :
                setattr( TradeContext, name, value )
            

        if( TradeContext.errorCode != '0000' ):
            
            AfaLoggerFunc.tradeInfo("���ش������ ["+TradeContext.errorCode+"]")
            AfaLoggerFunc.tradeInfo("���ش�����Ϣ ["+TradeContext.errorMsg+"]")
            
            #����������ʧ�ܺ��¼������ʹ�����Ϣ
            if not AhjfFunc.ADBUpdateTransdtlRev( ):
                raise AfaFlowControl.accException()
        
        return True
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))

def SubModuleDoTrd( ):
    return True
                            