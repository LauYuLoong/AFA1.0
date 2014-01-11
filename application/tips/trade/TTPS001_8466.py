# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.��˰���к�������.��������
#       procType  01 ��ѯ�˻���Ϣ
#       procType  02 ��ѯ���ջ�����Ϣ
#=================================================================
#   �����ļ�:   TTPS001_8466.py
#   �޸�ʱ��:   2007-10-23
##################################################################
#UtilTools,AfaDBFunc��TradeFunc,
import TradeContext, AfaLoggerFunc,  AfaFlowControl, os,HostContext
import HostComm,TipsFunc

def SubModuleMainFst( ):
    
    if TradeContext.procType=='01':
        AfaLoggerFunc.tradeInfo('>>>��ѯ�˻���Ϣ')
        if not QueryAccInfo():
            return False
    elif TradeContext.procType=='02': 
        AfaLoggerFunc.tradeInfo('>>>��ѯ���ջ�����Ϣ')
        if not TipsFunc.ChkTaxOrg(TradeContext.taxOrgCode):
            return False
    elif TradeContext.procType=='03': #�ɷѲ�ѯ������Ϣ��������Ϣ
        if not TipsFunc.ChkTaxOrg(TradeContext.taxOrgCode):
            return False
        #if not TipsFunc.ChkLiquidInfo():
        #    return False
    elif TradeContext.procType=='04': 
        AfaLoggerFunc.tradeInfo('>>>��ѯ���������Ϣ')
        if not TipsFunc.ChkTre(TradeContext.treCode,TradeContext.payeeBankNo):
            return False
    else:
        return AfaFlowControl.ExitThisFlow('0001', 'δ����ò�ѯ����')    
    TradeContext.errorCode='0000'
    TradeContext.errorMsg='��ѯ��Ϣ�ɹ�'
    return True
 
def SubModuleMainSnd ():
    return True


def QueryAccInfo():
    try:
        #ͨѶ�����
        HostContext.I1TRCD = '8810'                        #����������
        HostContext.I1SBNO = TradeContext.brno             #�ý��׵ķ������
        HostContext.I1USID = TradeContext.teller           #���׹�Ա��
        HostContext.I1AUUS = TradeContext.authTeller       #��Ȩ��Ա
        HostContext.I1AUPS = TradeContext.authPwd          #��Ȩ��Ա����
        HostContext.I1WSNO = TradeContext.termId           #�ն˺�
        HostContext.I1ACNO = TradeContext.accno            #�ʺ�
        HostContext.I1CYNO = '01'                          #����
        HostContext.I1CFFG = '1'                           #����У���־(0-��Ҫ,1-����Ҫ)
        HostContext.I1PSWD = ''                            #����
        #HostContext.I1CETY = TradeContext.I1VOUTHTYPE      #ƾ֤����
        #HostContext.I1CCSQ = TradeContext.I1VOUTHNO        #ƾ֤����
        #HostContext.I1CTFG = TradeContext.I1CHFLAG         #�����־
        HostContext.I1CETY = ''                           #ƾ֤����
        HostContext.I1CCSQ = ''                           #ƾ֤����
        HostContext.I1CTFG = ''                           #�����־

        HostTradeCode = "8810".ljust(10,' ')
        HostComm.callHostTrade( os.environ['AFAP_HOME'] + '/conf/hostconf/AH8810.map', HostTradeCode, "0002" )
        if( HostContext.host_Error ):
            AfaLoggerFunc.tradeInfo('>>>��������ʧ��=[' + str(HostContext.host_ErrorType) + ']:' +  HostContext.host_ErrorMsg)
            return AfaFlowControl.ExitThisFlow('9001', HostContext.host_ErrorMsg)
        else:
            if ( HostContext.O1MGID == 'AAAAAAA' ):
                TradeContext.userName         = HostContext.O1CUNM
                TradeContext.accStatus        = HostContext.O1ACST
                TradeContext.idType         = HostContext.O1IDTY
                TradeContext.idCode         = HostContext.O1IDNO
                TradeContext.openBrno        = HostContext.O1OPNT
                
                if ( TradeContext.accStatus != '0'):
                    return AfaFlowControl.ExitThisFlow('9000','�ͻ������˻�״̬�쳣,���ܽ���ע��')
            else:
                return AfaFlowControl.ExitThisFlow(HostContext.O1MGID, HostContext.O1INFO)

    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return AfaFlowControl.ExitThisFlow('9999', '�������쳣'+str(e))
    return True