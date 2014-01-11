# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.������ͨѶ����
#=================================================================
#   �����ļ�:   VouhHostFunc.py
#   �޸�ʱ��:   2008-12-18
#               
#
##################################################################
import TradeContext,AfaFunc,UtilTools,HostComm,HostContext,HostDataHandler,AfaLoggerFunc,os,AfaFlowControl
from types import *

#====================���������ݽ���=============================
def CommHost( result = '8844' ):

    AfaLoggerFunc.tradeInfo('>>>����ͨѶ����[CommHost]')

    #�����������ױ�־TradeContext.revTranF�жϾ���ѡ���ĸ�map�ļ��������ӿڷ�ʽ

    if (result == '8844'):
        AfaLoggerFunc.tradeInfo('>>>���ļ���')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8844.map'
        TradeContext.HostCode = '8844'

    else:
        TradeContext.errorCode = 'A9999'
        TradeContext.errorMsg  = '�����������'
        return False

    AfaLoggerFunc.tradeInfo( '=======================7' )
    #�˴����״���Ҫ��10λ,�Ҳ��ո�
    HostComm.callHostTrade( mapfile, UtilTools.Rfill(TradeContext.HostCode,10,' ') ,'0002' )
    AfaLoggerFunc.tradeInfo( '=======================8' )
    if HostContext.host_Error:
        AfaLoggerFunc.tradeFatal( 'host_Error:'+str( HostContext.host_ErrorType )+':'+HostContext.host_ErrorMsg )

        if HostContext.host_ErrorType != 5 :
            TradeContext.__status__='1'
            TradeContext.errorCode='A0101'
            TradeContext.errorMsg=HostContext.host_ErrorMsg
        else :
            TradeContext.__status__='2'
            TradeContext.errorCode='A0102'
            TradeContext.errorMsg=HostContext.host_ErrorMsg
        return False
    AfaLoggerFunc.tradeInfo( '=======================9' )
    #================�����������ذ�====================
    return HostParseRet(result )


#================�����������ذ�====================
def HostParseRet( hostType ):
    HostContext.O1TLSQ=''
    AfaLoggerFunc.tradeInfo( '=======================10' )
    if (HostContext.host_Error == True):    #����ͨѶ����
        TradeContext.__status__='2'
        TradeContext.errorCode, TradeContext.errorMsg = 'A9998', '����ͨѶ����'
        TradeContext.bankCode  = HostContext.host_ErrorType                       #ͨѶ�������
        return False
    AfaLoggerFunc.tradeInfo( '=======================11'+HostContext.O1MGID )
    if( HostContext.O1MGID == 'AAAAAAA' ): #�ɹ�
        
        TradeContext.__status__='0'
        TradeContext.errorCode, TradeContext.errorMsg = '0000', '�����ɹ�'
        TradeContext.PDTLSQ = HostContext.O1TLSQ                               #��Ա��ˮ��
        TradeContext.PDTRDT = HostContext.O1TRDT                                #����ʱ��
        TradeContext.PAMGID = HostContext.O1MGID                               #�������ش���
        return True

    else:                                  #ʧ��
        TradeContext.__status__='1'
        
        #����ũ��-�����Զ����ش�����Ϣ������Ҫת��
        #result = AfapFunc.RespCodeMsg(HostContext.O1MGID,'0000','100000')
        #if not result :
        TradeContext.errorCode, TradeContext.errorMsg = HostContext.O1MGID, HostContext.O1INFO
        return False
