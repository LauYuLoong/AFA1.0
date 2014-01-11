# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.������ͨѶ����
#=================================================================
#   �����ļ�:   VouhHostFunc.py
#   �޸�ʱ��:   2008-06-13
#               ���ǽ�
#
##################################################################
import TradeContext,UtilTools,HostComm,HostContext,AfaLoggerFunc,os
#,AfaFunc,AfaFlowControl,AfaHostFunc,HostDataHandler
from types import *

def VouhCommHost():
    if( TradeContext.existVariable( "sOperSty" ) ):
        HostContext.I1OPTY = TradeContext.sOperSty
    else:
        TradeContext.errorCode = 'A005060'
        TradeContext.errorMsg = '����ģʽ[sOperSty]ֵ������!'
        return False
        
    #################################################
    #����ģʽ��      0���跽 		�����;
	#				1������ 		����⡢���ϡ��ֹ�����;
	#				2��˫������ ���Ͻɡ����á�����;
	#################################################
	
    if( TradeContext.existVariable("sInTellerNo")):
        HostContext.I1SJUS = TradeContext.sInTellerNo
    elif( TradeContext.sOperSty =='2'):
        TradeContext.errorCode = 'A005060'
        TradeContext.errorMsg = '�Է���Ա[sInTellerNo]ֵ������!'
        return False
        
    if( TradeContext.existVariable("sInBesbNo")):
        HostContext.I1OPNT = TradeContext.sInBesbNo
    elif( TradeContext.sOperSty =='2'):
        TradeContext.errorCode = 'A005060'
        TradeContext.errorMsg = '�Է���������[sInBesbNo]ֵ������!'
        return False
        
    AfaLoggerFunc.tradeInfo( '=======================1' )
    if( TradeContext.existVariable("sPassWD")):
        HostContext.I1PSWD = TradeContext.sPassWD
    elif( TradeContext.sOperSty =='2'):
        TradeContext.errorCode = 'A005060'
        TradeContext.errorMsg = '����[sPassWD]ֵ������!'
        return False
    
    AfaLoggerFunc.tradeInfo( '=======================2' )
    if( TradeContext.existVariable( "sBesbNo" )):
        HostContext.I1SBNO = TradeContext.sBesbNo
    else:
        TradeContext.errorCode = 'A005060'
        TradeContext.errorMsg = '��������[sBesbNo]ֵ������!'
        return False
    
    
    AfaLoggerFunc.tradeInfo( '=======================3' )
    if( TradeContext.existVariable( "sTellerNo" )):
        HostContext.I1USID = TradeContext.sTellerNo      
    else:
        TradeContext.errorCode = 'A005060'
        TradeContext.errorMsg = '���׹�Ա[I1USID]ֵ������!'
        return False
     
    AfaLoggerFunc.tradeInfo( '=======================4' )   
    if( TradeContext.existVariable( "sWSNO" )):
        HostContext.I1WSNO = TradeContext.sWSNO
    else:
        TradeContext.errorCode = 'A005060'
        TradeContext.errorMsg = '�ն˺�[sWSNO]ֵ������!'
        return False    
                
    AfaLoggerFunc.tradeInfo( '=======================5' )
    if( TradeContext.existVariable( "sCur" )):
        HostContext.I1CYNO = TradeContext.sCur
        
    if( TradeContext.existVariable("sNum")):
        HostContext.I1ACUR = TradeContext.sNum
    
    AfaLoggerFunc.tradeInfo( '=======================6,'+str(TradeContext.sNum) )
    HostContext.I2CETY = []
    HostContext.I2NUBZ = []
    
    HostContext.I1DATE = TradeContext.sLstTrxDay           #��̨����
    HostContext.I1AGNO = TradeContext.sVouhSerial          #��̨��ˮ��
        
    for i in range(TradeContext.sNum):
        HostContext.I2CETY.append(TradeContext.sVouhType[i])
        HostContext.I2NUBZ.append(TradeContext.sVouhNum[i])
        
    AfaLoggerFunc.tradeInfo( '=======================7' )
        
    #���������ݽ���
    CommHost()
    
        

#====================���������ݽ���=============================
def CommHost( result = '8827' ):

    AfaLoggerFunc.tradeInfo('>>>����ͨѶ����[CommHost]')

    #�����������ױ�־TradeContext.revTranF�жϾ���ѡ���ĸ�map�ļ��������ӿڷ�ʽ

    if (result == '8827'):
        AfaLoggerFunc.tradeInfo('>>>ƾ֤����')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8827.map'
        TradeContext.HostCode = '8827'

    elif(result == '8828'):
        AfaLoggerFunc.tradeInfo('>>>ƾ֤����')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8828.map'
        TradeContext.HostCode = '8828'
    
    elif(result == '2001'):
        AfaLoggerFunc.tradeInfo('>>>��ȡ��������')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH2001.map'
        TradeContext.HostCode = '2001'
    
    elif(result == '8809'):
        AfaLoggerFunc.tradeInfo('>>>��ȡ��������')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8809.map'
        TradeContext.HostCode = '8809' 
    
    #beginƾ֤�Ż�����201109  
    elif(result == '0104'):
        AfaLoggerFunc.tradeInfo('>>>��ѯ��Աβ���')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH0104.map'
        TradeContext.HostCode = '0104'
    #end
    
    else:
        TradeContext.errorCode = 'A9999'
        TradeContext.errorMsg  = '�����������'
        return False

    AfaLoggerFunc.tradeInfo( '=======================8' )
    #�˴����״���Ҫ��10λ,�Ҳ��ո�
    HostComm.callHostTrade( mapfile, UtilTools.Rfill(TradeContext.HostCode,10,' ') ,'0002' )
    AfaLoggerFunc.tradeInfo( '=======================9' )
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
    AfaLoggerFunc.tradeInfo( '=======================10' )
    #================�����������ذ�====================
    return HostParseRet(result )


#================�����������ذ�====================
def HostParseRet( hostType ):
    HostContext.O1TLSQ=''
    AfaLoggerFunc.tradeInfo( '=======================11' )
    if (HostContext.host_Error == True):    #����ͨѶ����
        TradeContext.__status__='2'
        TradeContext.errorCode, TradeContext.errorMsg = 'A9998', '����ͨѶ����'
        TradeContext.bankCode  = HostContext.host_ErrorType                       #ͨѶ�������
        return False
    AfaLoggerFunc.tradeInfo( '=======================12'+HostContext.O1MGID )
    if( HostContext.O1MGID == 'AAAAAAA' ): #�ɹ�
        
        AfaLoggerFunc.tradeInfo('>>>ƾ֤����====' + HostContext.O1MGID)

        
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
        TradeContext.errorCode, TradeContext.errorMsg = HostContext.O1MGID, HostContext.O1INFO
        return False
