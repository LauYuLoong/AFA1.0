# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.������ͨѶ����
#=================================================================
#   �����ļ�:   TipsHostFunc.py
#   �޸�ʱ��:   2008-06-13
#               ���ǽ�
#
##################################################################
import TradeContext,UtilTools,HostComm,HostContext,AfaLoggerFunc,os
from types import *

#=================��ʼ������ͨѶ�ӿ�=======================
def InitHostReq( ):
    #��ʼ����������ֵ����
    AfaLoggerFunc.tradeInfo('��ʼ��map�ļ���Ϣ[InitHostReq]')
    HostContext.I1SBNO = TradeContext.sBrNo              #���׻�����
    HostContext.I1USID = TradeContext.sTeller            #���׹�Ա��
    HostContext.I1WSNO = TradeContext.sTermId            #�ն˺�
    if(TradeContext.existVariable('sOpeFlag' ) ): 
        HostContext.I1OPFG = TradeContext.sOpeFlag           #������־
    #if(TradeContext.existVariable('entrustDate' ) ): 
    #    HostContext.I1TRDT = TradeContext.entrustDate        #����ί������
    if(TradeContext.existVariable('entrustDate' ) ): 
        HostContext.I1CLDT = TradeContext.entrustDate        #����ί������
    if(TradeContext.existVariable('packNo' ) ):  
        HostContext.I1UNSQ = TradeContext.packNo             #����ί�к�
    if(TradeContext.existVariable('sFileName')):
        HostContext.I1FINA = TradeContext.sFileName          #�ļ���
    if(TradeContext.existVariable('sTotal' ) ):          #�ܱ���
        HostContext.I1COUT = TradeContext.sTotal      
    if(TradeContext.existVariable('sAmount' )):       
        HostContext.I1TOAM = TradeContext.sAmount            #�ܽ��
    
    AfaLoggerFunc.tradeInfo('��ʼ��map�ļ���Ϣ[InitHostReq]���')

    return True

#====================���������ݽ���=============================
def CommHost( result = '8830' ):

    AfaLoggerFunc.tradeInfo('>>>����ͨѶ����[CommHost]')
    
    if(not InitHostReq()):
        return False

    #�����������ױ�־TradeContext.revTranF�жϾ���ѡ���ĸ�map�ļ��������ӿڷ�ʽ

    if (result == '8830'):
        AfaLoggerFunc.tradeInfo('>>>�����ϴ�')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8830.map'
        TradeContext.HostCode = '8830'

    elif(result == '8831'):
        AfaLoggerFunc.tradeInfo('>>>������������')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8831.map'
        TradeContext.HostCode = '8831'
    elif(result == '8833'):
        AfaLoggerFunc.tradeInfo('>>>���������ļ���������')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8833.map'
        TradeContext.HostCode = '8833'
    elif(result == '8834'):
        AfaLoggerFunc.tradeInfo('>>>��ѯ�������˽��')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8834.map'
        TradeContext.HostCode = '8834'
    elif(result == '8810'):
        AfaLoggerFunc.tradeInfo('>>>��ѯ�����˻���Ϣ')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8810.map'
        TradeContext.HostCode = '8810'    
    elif(result == '8835'):
        AfaLoggerFunc.tradeInfo('>>>ƾ֤����')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8835.map'
        TradeContext.HostCode = '8835'    
    else:
        TradeContext.errorCode = 'A9999'
        TradeContext.errorMsg  = '�����������'
        return False

    #�˴����״���Ҫ��10λ,�Ҳ��ո�
    HostComm.callHostTrade( mapfile, UtilTools.Rfill(TradeContext.HostCode,10,' ') ,'0002' )
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
    #================�����������ذ�====================
    return HostParseRet(result )


#================�����������ذ�====================
def HostParseRet( hostType ):
    if (HostContext.host_Error == True):    #����ͨѶ����
        TradeContext.__status__='2'
        TradeContext.errorCode, TradeContext.errorMsg = 'A9998', '����ͨѶ����'
        TradeContext.bankCode  = HostContext.host_ErrorType                       #ͨѶ�������
        return False

    if( HostContext.O1MGID == 'AAAAAAA' ): #�ɹ�

        TradeContext.__status__='0'
        TradeContext.errorCode, TradeContext.errorMsg = '0000', '�����ɹ�'
        TradeContext.HostSerno = HostContext.O1TLSQ                               #��Ա��ˮ��
        TradeContext.HostDate = HostContext.O1TRDT                                #����ʱ��
        TradeContext.bankCode  = HostContext.O1MGID                               #�������ش���
        return True

    else:                                  #ʧ��
        TradeContext.__status__='1'
        
        #����ũ��-�����Զ����ش�����Ϣ������Ҫת��
        #result = AfapFunc.RespCodeMsg(HostContext.O1MGID,'0000','100000')
        #if not result :
        #    TradeContext.errorCode, TradeContext.errorMsg = 'A9999', 'ϵͳ����[����δ֪����]['+HostContext.ERR+']'
        #else:
        TradeContext.errorCode, TradeContext.errorMsg = HostContext.O1MGID, HostContext.O1INFO
        return False
