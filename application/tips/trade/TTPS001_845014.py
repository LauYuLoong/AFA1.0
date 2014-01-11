# -*- coding: gbk -*-
##################################################################
#   ��˰����.����Э��У��.����������
#=================================================================
#   �����ļ�:   TTPS001_845014.py
#   �޸�ʱ��:   2008-12-05
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools, AfaDBFunc
import TipsFunc,HostContext,os
from types import *

def SubModuleMainFst( ):

    AfaLoggerFunc.tradeInfo( '��������Э����֤/����(���з���)[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
        #============У�鹫���ڵ����Ч��==================
        # �����Լ��
        if( not TradeContext.existVariable( "VCSign" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '��ʶ[VCSign]ֵ������!' )
        if( not TradeContext.existVariable( "payAcct" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '�ʺ�[payAcct]ֵ������!' )
        if( not TradeContext.existVariable( "taxPayCode" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '�û���[taxPayCode]ֵ������!' )
        if( not TradeContext.existVariable( "taxPayName" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '�û���[taxPayName]ֵ������!' )
        if( not TradeContext.existVariable( "taxOrgCode" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '���ջ���[taxOrgCode]ֵ������!' )
        if( not TradeContext.existVariable( "protocolNo" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', 'Э���[protocolNo]ֵ������!' )
        if( not TradeContext.existVariable( "PayOpBkCode" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '��������к�[PayOpBkCode]ֵ������!' )
        if( not TradeContext.existVariable( "PayBkCode" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '�������к�[PayBkCode]ֵ������!' )
        
        #��֤�������    0	��֤ͨ����Э���ѿ���ʹ��
        #                1	��֤ʧ�ܣ�Э�鲻���ڻ���Ϣ����
        #                2	����ͨ����Э���Ѳ���ʹ��
        #                3	����ʧ�ܣ�Э�鲻���ڻ���Ϣ����
        if TradeContext.VCSign=='0':
            TradeContext.VCResult='1'
            TradeContext.AddWord='��֤ʧ�ܣ�Э�鲻���ڻ���Ϣ����'
        else:
            TradeContext.VCResult='3'
            TradeContext.AddWord='����ʧ�ܣ�Э�鲻���ڻ���Ϣ����'
                   
        #=============��ȡƽ̨��ˮ��==================== 
        if TipsFunc.GetSerialno( ) == -1 :
            return False
        
        if TradeContext.VCSign=='0':
            #=============�ж�״̬====================
            sql = "SELECT STATUS FROM TIPS_CUSTINFO WHERE "
            sql = sql +" TAXPAYCODE='"      +TradeContext.taxPayCode+"'"
            sql = sql +"AND PAYACCT='"      +TradeContext.payAcct+"'"
            sql = sql +"AND TAXORGCODE='"   +TradeContext.taxOrgCode+"'"
            sql = sql +"AND PROTOCOLNO='"   +TradeContext.protocolNo+"'"
            sql = sql +"AND PAYOPBKCODE='"   +TradeContext.PayOpBkCode+"'"
            sql = sql +"AND NOTE2='"   +TradeContext.PayBkCode+"'"
            AfaLoggerFunc.tradeInfo(sql)
            records = AfaDBFunc.SelectSql(sql)
            if( records == None or records < 0 ):
                AfaLoggerFunc.tradeFatal(sql)
                return TipsFunc.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
            elif( len( records ) == 0 ):
                AfaLoggerFunc.tradeInfo( "�ÿͻ���δǩԼ")
                TradeContext.errorCode='9999'
                TradeContext.errorMsg='��֤ʧ�ܣ�Э�鲻����'
                TradeContext.VCResult='1'
                TradeContext.AddWord='��֤ʧ�ܣ�Э�鲻����'
                return True
            else:
                AfaLoggerFunc.tradeFatal(sql)
                AfaLoggerFunc.tradeInfo(records[0][0])
                UtilTools.ListFilterNone( records )
                #0-ע�� 1-������˫��������֤�� 2-��ʱ״̬�����з���������֤��3-��ʱ״̬�����з������ѳ�����
                if (records[0][0] =="0" or records[0][0]=="3" ): #���иÿͻ���¼��״̬ΪδǩԼ���޷���֤
                    AfaLoggerFunc.tradeInfo( "���иÿͻ���¼��״̬ΪδǩԼ���޷���֤")
                    TradeContext.errorCode='9999'
                    TradeContext.errorMsg='��֤ʧ�ܣ�Э�鲻����'
                    TradeContext.VCResult='1'
                    TradeContext.AddWord='��֤ʧ�ܣ�Э�鲻����'
                    return True
            sql = "update TIPS_CUSTINFO set  STATUS     ='1'"
            sql = sql+" WHERE TAXPAYCODE='" +TradeContext.taxPayCode+"'"
            sql = sql +"AND PAYACCT='"      +TradeContext.payAcct   +"'"
            sql = sql +"AND TAXORGCODE='"   +TradeContext.taxOrgCode+"'"
            sql = sql +"AND PROTOCOLNO='"   +TradeContext.protocolNo+"'"
            AfaLoggerFunc.tradeInfo(sql)
            if( AfaDBFunc.UpdateSqlCmt(sql) == -1 ):
                AfaLoggerFunc.tradeFatal(sql)
                return TipsFunc.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
            TradeContext.errorCode='0000'
            TradeContext.errorMsg='��֤ͨ����Э���ѿ���ʹ��'
            TradeContext.VCResult='0'
            TradeContext.AddWord='��֤ͨ����Э���ѿ���ʹ��'
            

        elif TradeContext.VCSign=='1':
            #=============�ж�״̬====================
            sql = "SELECT STATUS FROM TIPS_CUSTINFO WHERE "
            sql = sql +" TAXPAYCODE='"      +TradeContext.taxPayCode+"'"
            sql = sql +"AND PAYACCT='"      +TradeContext.payAcct+"'"
            sql = sql +"AND TAXORGCODE='"   +TradeContext.taxOrgCode+"'"
            sql = sql +"AND PROTOCOLNO='"   +TradeContext.protocolNo+"'"
            sql = sql +"AND PAYOPBKCODE='"   +TradeContext.PayOpBkCode+"'"
            sql = sql +"AND NOTE2='"   +TradeContext.PayBkCode+"'"
            AfaLoggerFunc.tradeInfo(sql)
            records = AfaDBFunc.SelectSql(sql)
            if( records == None or records < 0 ):
                AfaLoggerFunc.tradeFatal(sql)
                return TipsFunc.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
            elif( len( records ) == 0 ):
                AfaLoggerFunc.tradeInfo( "�ÿͻ���δǩԼ")
                TradeContext.errorCode='9999'
                TradeContext.errorMsg='����ʧ�ܣ�Э�鲻���ڻ���Ϣ����'
                TradeContext.VCResult='3'
                TradeContext.AddWord='����ʧ�ܣ�Э�鲻���ڻ���Ϣ����'
                return True
            sql="update TIPS_CUSTINFO set "
            sql=sql+" STATUS     ='0'"
            sql = sql+" WHERE TAXPAYCODE='" +TradeContext.taxPayCode+"'"
            sql = sql +"AND PAYACCT='"      +TradeContext.payAcct   +"'"
            sql = sql +"AND TAXORGCODE='"   +TradeContext.taxOrgCode+"'"
            sql = sql +"AND PROTOCOLNO='"   +TradeContext.protocolNo+"'"
            AfaLoggerFunc.tradeInfo(sql)
            if( AfaDBFunc.UpdateSqlCmt(sql) == -1 ):
                AfaLoggerFunc.tradeFatal(sql)
                return TipsFunc.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
            TradeContext.errorCode='0000'
            TradeContext.errorMsg='����ͨ����Э���Ѳ���ʹ��'
            TradeContext.VCResult='2'
            TradeContext.AddWord='����ͨ����Э���Ѳ���ʹ��'
            
            
                       
               
            #TradeContext.revTranF       ='0' #������
            #TradeContext.tradeType      ='U' #ǩԼ�ཻ��
            #TradeContext.amount         ='0' #
            #TradeContext.__agentAccno__ =''  #�跽�ʺ��ÿ�
            #TradeContext.note1          =TradeContext.upBranchno       
            ##��¼ǩԼ��ˮ
            #if not TransDtlFunc.InsertDtl( ) :
            #    return False
            #TradeContext.__status__='0'
            #TradeContext.errorCode='0000'
            #TradeContext.errorMsg='���׳ɹ�'
            #if( not TransDtlFunc.UpdateDtl( 'TRADE' ) ):
            #    return False
            
        AfaLoggerFunc.tradeInfo(TradeContext.errorCode)
        AfaLoggerFunc.tradeInfo(TradeContext.errorMsg)
        AfaLoggerFunc.tradeInfo(TradeContext.VCResult)
        AfaLoggerFunc.tradeInfo(TradeContext.AddWord)
        #=============�����˳�====================
        AfaLoggerFunc.tradeInfo( '�˳�����Э����֤(����)[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        TradeContext.tradeResponse=[]
        return True
    except TipsFunc.flowException, e:
        TipsFunc.exitMainFlow( )
    except TipsFunc.accException:
        TipsFunc.exitMainFlow( )
    except Exception, e:
        TipsFunc.exitMainFlow(str(e))  
def SubModuleMainSnd():
    return True   
    
