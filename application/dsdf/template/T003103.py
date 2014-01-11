# -*- coding: gbk -*-
################################################################################
#   ���մ���.�쳣����ģ��
#===============================================================================
#   ģ���ļ�:   003103.py
#   �޸�ʱ��:   2006-04-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaDBFunc,AfaTransDtlFunc,AfaFlowControl,AfaHostFunc,AfaAfeFunc
from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('******���մ���.�쳣����ģ��[' + TradeContext.TemplateCode + ']����******')

    try:

        #=====================��ʼ�����ر��ı���================================
        TradeContext.tradeResponse=[]


        #=====================��ȡ��ǰϵͳʱ��==================================
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )

        #=====================�ж�Ӧ��ϵͳ״̬==================================
        if not AfaFunc.ChkSysStatus( ) :
            raise AfaFlowControl.flowException( )
                
        #=====================����ӿ�(ǰ����)==================================
        subModuleExistFlag=0
        subModuleName = 'T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode
        try:
            subModuleHandle=__import__( subModuleName )
            
        except Exception, e:
            AfaLoggerFunc.tradeInfo( e)
            
        else:
            AfaLoggerFunc.tradeInfo( 'ִ��['+subModuleName+']ģ��' )
            subModuleExistFlag=1
            if not subModuleHandle.SubModuleDoFst( ) :
                raise AfaFlowControl.flowException( )


        #=====================�����Լ��========================================
        if( not TradeContext.existVariable( "sysId" ) ):
            raise AfaFlowControl.flowException( 'A0001', 'ϵͳ��ʶ[sysId]ֵ������,���ܽ����쳣����' )

        if( not TradeContext.existVariable( "unitno" ) ):
            raise AfaFlowControl.flowException( 'A0001', '��λ����[unitno]ֵ������,���ܽ����쳣����' )

        if( not TradeContext.existVariable( "subUnitno" ) ):
            raise AfaFlowControl.flowException( 'A0001', '�ӵ�λ����[unitno]ֵ������,���ܽ����쳣����' )

        if( not TradeContext.existVariable( "agentFlag" ) ):
            raise AfaFlowControl.flowException( 'A0001', 'ҵ��ʽ[agentFlag]ֵ������,���ܽ����쳣����' )

        if( not TradeContext.existVariable( "zoneno" ) ):
            raise AfaFlowControl.flowException( 'A0001', '������[zoneno]ֵ������,���ܽ����쳣����' )

        if( not TradeContext.existVariable( "channelCode" ) ):
            raise AfaFlowControl.flowException( 'A0001', '��������[channelCode]ֵ������,���ܽ����쳣����' )

        if( not TradeContext.existVariable( "brno" ) ):
            raise AfaFlowControl.flowException( 'A0001', '�����[brno]ֵ������,���ܽ����쳣����' )

        if( not TradeContext.existVariable( "tellerno" ) ):
            raise AfaFlowControl.flowException( 'A0001', '��Ա��[tellerno]ֵ������,���ܽ����쳣����' )

        if( not TradeContext.existVariable( "amount" ) ):
            raise AfaFlowControl.flowException( 'A0001', '���[amount]ֵ������,���ܽ����쳣����' )

        if( not TradeContext.existVariable( "preAgentSerno" ) ):
            raise AfaFlowControl.flowException( 'A0001', 'ԭ������ˮ��[preAgentSerno]ֵ������,���ܽ����쳣����' )

        #��������(0-������ 1-������� 2-�ȵ�����,������ 3-������,�ٵ�����)
        if( not TradeContext.existVariable( "revType" ) ):
            raise AfaFlowControl.flowException( 'A0001', '��������[revType]ֵ������,���ܽ����쳣����' )

        AfaLoggerFunc.tradeInfo( '>>>revType       = ' + TradeContext.revType )
        AfaLoggerFunc.tradeInfo( '>>>preAgentSerno = ' + TradeContext.preAgentSerno )

        #��ͬ������
        TradeContext.revTranF='1'

        #=====================�ж�Ӧ��ϵͳ״̬==================================
        if not AfaFunc.ChkSysStatus( ) :
            raise AfaFlowControl.flowException( )
        
        #=====================�ж��̻�״̬======================================
        if not AfaFunc.ChkUnitStatus( ) :
            raise AfaFlowControl.flowException( )
        
        #=====================�ж�����״̬======================================
        if not AfaFunc.ChkChannelStatus( ) :
            raise AfaFlowControl.flowException( )

        #=====================��ȡδ֪���׵���Ϣ================================
        if( not GetAbnormalInfo( TradeContext.preAgentSerno ) ):
            raise AfaFlowControl.flowException( )

        #=====================��ȡƽ̨��ˮ��====================================
        if( not AfaFunc.GetSerialno( ) ):
            raise AfaFlowControl.flowException( )

        #=====================������ˮ��========================================
        if( not AfaTransDtlFunc.InsertDtl( ) ):
            raise AfaFlowControl.flowException( )

        #=====================��������(0-������)================================
        if( TradeContext.revType == '0' ) :

            #����������
            AfaHostFunc.CommHost()


            #���½�����ˮ
            if( not AfaTransDtlFunc.UpdateDtl( 'BANK' ) ):
                raise AfaFlowControl.flowException( )


            #����ӿ�(����)
            if subModuleExistFlag==1 :
                if not subModuleHandle.SubModuleDoSnd():
                    raise AfaFlowControl.flowException( )


        #=====================��������(1-�������)==============================
        if( TradeContext.revType == '1' ) :

            #�����������
            AfaAfeFunc.CommAfe()
            
            
            #���½�����ˮ
            if( not AfaTransDtlFunc.UpdateDtl( 'CORP' ) ):
                raise AfaFlowControl.flowException( )

            #����ӿ�(����)
            if subModuleExistFlag==1 :
                if not subModuleHandle.SubModuleDoTrd():
                    raise AfaFlowControl.flowException( )


        #=====================��������(2-�ȵ�����,������)=======================
        if( TradeContext.revType == '2' ) :

            #�����������
            AfaAfeFunc.CommAfe()
            
            
            #���½�����ˮ
            if( not AfaTransDtlFunc.UpdateDtl( 'CORP' ) ):
                raise AfaFlowControl.flowException( )

            #����������
            AfaHostFunc.CommHost()

            
            #���½�����ˮ
            if( not AfaTransDtlFunc.UpdateDtl( 'BANK' ) ):
                raise AfaFlowControl.flowException( )
        
        
            #����ӿ�(����)
            if subModuleExistFlag==1 :
                if not subModuleHandle.SubModuleDoFth():
                    raise AfaFlowControl.flowException( )
                    
        #=====================��������(3-������,�ٵ�����)=======================
        if( TradeContext.revType == '3' ) :

            #����������
            AfaHostFunc.CommHost()
            
            
            #���½�����ˮ
            if( not AfaTransDtlFunc.UpdateDtl( 'BANK' ) ):
                raise AfaFlowControl.flowException( )


            #�����������
            AfaAfeFunc.CommAfe()
            
            
            #���½�����ˮ
            if( not AfaTransDtlFunc.UpdateDtl( 'CORP' ) ):
                raise AfaFlowControl.flowException( )
                
            #����ӿ�(����)
            if subModuleExistFlag==1 :
                if not subModuleHandle.SubModuleDoFfh():
                    raise AfaFlowControl.flowException( )

        #=====================�Զ����==========================================
        AfaFunc.autoPackData()
        
        #=====================�˳�ģ��==========================================
        AfaLoggerFunc.tradeInfo('******���մ���.�쳣����ģ��[' + TradeContext.TemplateCode + ']�˳�******')

    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )

    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )


def GetAbnormalInfo( serialno ):

    #��ȡ�쳣������Ϣ
    names=['accType','__drAccno__','__crAccno__','userno','subUserno','userName','subAmount','vouhType','vouhno', \
    'vouhDate','bankSerno','currType','currFlag','note1','note2','note3','note4','note5', \
    'note6','note7','note8','note9','note10']


    #��ѯ���
    sql = "SELECT ACCTYPE,DRACCNO,CRACCNO,USERNO,SUBUSERNO,USERNAME,SUBAMOUNT,VOUHTYPE,VOUHNO,VOUHDATE,"
    sql = sql + "BANKSERNO,CURRTYPE,CURRFLAG,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5,NOTE6,NOTE7,"
    sql = sql + "NOTE8,NOTE9,NOTE10 FROM AFA_MAINTRANSDTL"
    
    sql = sql + " WHERE TELLERNO='"     + TradeContext.tellerno + "'"
    sql = sql + " AND ZONENO='"         + TradeContext.zoneno   + "'"
    sql = sql + " AND BRNO='"           + TradeContext.brno     + "'"
    sql = sql + " AND SYSID='"          + TradeContext.sysId    + "'"
    sql = sql + " AND AGENTSERIALNO='"  + serialno              + "'"
    sql = sql + " AND WORKDATE='"       + TradeContext.workDate + "'"
    sql = sql + " AND AMOUNT='"         + TradeContext.amount   + "'"
    sql = sql + " AND REVTRANF='0'"

    if (TradeContext.agentFlag=='01' or TradeContext.agentFlag=='03'):
        sql = sql + " AND (AGENTFLAG IN ('01','03') AND (BANKSTATUS='2' OR (BANKSTATUS='0' AND CORPSTATUS IN ('1','2','3'))))"
    else:
        sql = sql + " AND (AGENTFLAG IN ('02','04') AND (CORPSTATUS='2' OR (CORPSTATUS='0' AND BANKSTATUS IN ('1','2','3'))))"

    AfaLoggerFunc.tradeInfo( sql )

    result=None
    records=AfaDBFunc.SelectSql( sql )
    if( records == None ):
        TradeContext.errorCode, TradeContext.errorMsg='A0027', '��ˮ��������쳣'
        return False
        
    if( len( records ) == 0 ):
        TradeContext.errorCode, TradeContext.errorMsg='A0045', 'δ����ԭʼ����'        
        return False

    #���˽�����е�None
    result=AfaUtilTools.ListFilterNone( records[0] )

    #��TradeContext�еı�����ֵ
    k=0
    for name in names:
        setattr( TradeContext, name, result[k] )
        k=k+1

    return True
