# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.������ͨѶ����
#=================================================================
#   �����ļ�:   AfaHostFunc.py
#   �޸�ʱ��:   2006-09-12
#
##################################################################
import TradeContext,AfaFunc,UtilTools,HostComm,HostContext,HostDataHandler,AfaLoggerFunc,os
from types import *

def InitHostReq(hostType ):
    #��ʼ����������ֵ����
    AfaLoggerFunc.tradeInfo('��ʼ��map�ļ���Ϣ[InitHostReq]')

    if (hostType =='0'): # ������

        AfaLoggerFunc.tradeInfo('>>>������')

        HostContext.I1TRCD = '8813'
       
        HostContext.I1SBNO = TradeContext.brno
       
        HostContext.I1USID = TradeContext.tellerno
       
        if TradeContext.existVariable ( 'authTeller'):
            HostContext.I1AUUS = TradeContext.authTeller
            HostContext.I1AUPS = TradeContext.authPwd
        else:
            HostContext.I1AUUS = ''
            HostContext.I1AUPS = ''

        HostContext.I1WSNO = TradeContext.termId            #�ն˺�

        HostContext.I2NBBH = []                             #����ҵ���
        HostContext.I2NBBH.append(TradeContext.sysId)

        HostContext.I2FEDT = []                             #ǰ������
        HostContext.I2FEDT.append(TradeContext.workDate)

        HostContext.I2RBSQ = []                             #ǰ����ˮ��
        HostContext.I2RBSQ.append(TradeContext.agentSerialno)

        HostContext.I2DATE = []                             #��ϵͳ��������
        HostContext.I2DATE.append(TradeContext.workDate)

        HostContext.I2RVFG = []                             #�����ֱ�־
        HostContext.I2RVFG.append('0')

        HostContext.I2SBNO = []                             #���׻���
        HostContext.I2SBNO.append(TradeContext.brno)

        HostContext.I2TELR = []                             #���׹�Ա
        HostContext.I2TELR.append(TradeContext.tellerno)

        HostContext.I2TRSQ = []                             #���
        HostContext.I2TRSQ.append('000')
        
        HostContext.I2TINO = []                             #�������
        HostContext.I2TINO.append('00')

        HostContext.I2OPTY = []                             #֤��У���־
        HostContext.I2OPTY.append('0')

        HostContext.I2CYNO = []                             #����
        HostContext.I2CYNO.append('01')

        HostContext.I2WLBZ = []                             #�����ʱ�־
        HostContext.I2WLBZ.append('0')

        HostContext.I2TRAM = []                             #������
        HostContext.I2TRAM.append(TradeContext.amount.strip())

        HostContext.I2SMCD = []                             #ժҪ����
        if TradeContext.existVariable ( '__summaryCode__'):
            HostContext.I2SMCD.append(TradeContext.__summaryCode__)
        else:
            HostContext.I2SMCD.append('')

        HostContext.I2NMFG = []                             #����У���־
        HostContext.I2NMFG.append('0')

        HostContext.I2PKFG = []                             #����֧Ʊ��־(0-���� 1-֧Ʊ�� 2-��Ʊ�� 3-��Ʊ��)
        HostContext.I2PKFG.append('0')

        HostContext.I2TRFG = []                             #ƾ֤�����־(0-���� 1-���� 2-��� 3-�ָ�ƾ֤ 4-�Ǳ����� 9-������ ��Ʊǩ�����׼Ǳ���ƾ֤ʱ��=4)
        HostContext.I2TRFG.append('9')

        HostContext.I2CETY = []                             #ƾ֤����         
        if TradeContext.existVariable('vouhType'):      
            HostContext.I2CETY.append(TradeContext.vouhType)
        else:
            HostContext.I2CETY.append('')

        HostContext.I2CCSQ = []                             #ƾ֤��
        if TradeContext.existVariable('vouhNo'):      
            HostContext.I2CCSQ.append(TradeContext.vouhNo)
        else:
            HostContext.I2CCSQ.append('')

        HostContext.I2PS16 = []                             #֧������
        HostContext.I2PS16.append('')
            
        if (TradeContext.existVariable('idType') and len(TradeContext.idType)!=0):
            HostContext.I2OPTY = []                         #֤��У���־
            HostContext.I2OPTY.append('1')

            HostContext.I2IDTY = []                         #֤������
            HostContext.I2IDTY.append(TradeContext.idType)

            HostContext.I2IDNO = []                         #֤������
            HostContext.I2IDNO.append(TradeContext.idno)
        else:
            HostContext.I2OPTY = []                         #֤��У���־
            HostContext.I2OPTY.append('0')

            HostContext.I2IDTY = []                         #֤������
            HostContext.I2IDTY.append('')

            HostContext.I2IDNO = []                         #֤������
            HostContext.I2IDNO.append('')
        
        HostContext.I2APX1 = []                             #������Ϣ1(��λ����)
        if TradeContext.existVariable ( 'subUnitno'):
            HostContext.I2APX1.append(TradeContext.unitno + TradeContext.subUnitno)
        else:
            HostContext.I2APX1.append(TradeContext.unitno)


        #�ж��ֽ�ת�ʱ�־,�Ա���䲻ͬ������ͨѶ��
        if (TradeContext.accType == '000'):

            AfaLoggerFunc.tradeInfo('>>>�ֽ�')

            HostContext.I2CFFG = []                         #����У���־
            HostContext.I2CFFG.append('N')

            HostContext.I2PSWD = []                         #����
            HostContext.I2PSWD.append('')

            HostContext.I2CATR = []                         #��ת��־
            HostContext.I2CATR.append('0')

            #ҵ��ʽ(01-���� 02-���� 03-���� 04-����)
            if (TradeContext.agentFlag=='01' or TradeContext.agentFlag=='03' ):
                HostContext.I2RBAC = []                                             #�����˺�
                HostContext.I2RBAC.append(TradeContext.__agentAccno__)
            else:
                HostContext.I2SBAC = []
                HostContext.I2SBAC.append(TradeContext.__agentAccno__)              #�跽�˺�

        else:
            AfaLoggerFunc.tradeInfo('>>>ת��')


            #ҵ��ʽ(01-���� 02-���� 03-���� 04-����)
            if (TradeContext.agentFlag=='01' or TradeContext.agentFlag=='03' ):
                HostContext.I2RBAC = []                                             #�����˺�
                HostContext.I2RBAC.append(TradeContext.__agentAccno__)

                HostContext.I2SBAC = []                                             #�跽�˺�
                HostContext.I2SBAC.append(TradeContext.accno)                       
            else:
                HostContext.I2RBAC = []                                             #�����˺�
                HostContext.I2RBAC.append(TradeContext.accno)

                HostContext.I2SBAC = []                                             #�跽�˺�
                HostContext.I2SBAC.append(TradeContext.__agentAccno__)              


            if (TradeContext.existVariable('accPwd') and len(TradeContext.accPwd)!=0):
                HostContext.I2CFFG = []
                HostContext.I2CFFG.append('Y')              #����У�鷽ʽ

                HostContext.I2PSWD = []
                HostContext.I2PSWD.append(TradeContext.accPwd)
            else:
                HostContext.I2CFFG = []
                HostContext.I2CFFG.append('N')              #����У�鷽ʽ

            HostContext.I2CATR = []                         #��ת��־
            HostContext.I2CATR.append('1')

    else:   #������

        AfaLoggerFunc.tradeInfo('>>>������')

        HostContext.I1TRCD = '8820'

        AfaLoggerFunc.tradeInfo(TradeContext.brno)

        HostContext.I1SBNO = TradeContext.brno

        AfaLoggerFunc.tradeInfo(TradeContext.tellerno)

        HostContext.I1USID = TradeContext.tellerno

        if TradeContext.existVariable ( 'authTeller'):
            HostContext.I1AUUS = TradeContext.authTeller
            HostContext.I1AUPS = TradeContext.authPwd
        else:
            HostContext.I1AUUS = ''
            HostContext.I1AUPS = ''

        AfaLoggerFunc.tradeInfo(TradeContext.termId)
        AfaLoggerFunc.tradeInfo(TradeContext.sysId)
        AfaLoggerFunc.tradeInfo(TradeContext.workDate)
        AfaLoggerFunc.tradeInfo(TradeContext.agentSerialno)
        AfaLoggerFunc.tradeInfo(TradeContext.preAgentSerno)

        HostContext.I1WSNO = TradeContext.termId
        HostContext.I1NBBH = TradeContext.sysId
        HostContext.I1FEDT = TradeContext.workDate
        HostContext.I1DATE = TradeContext.workDate
        HostContext.I1RBSQ = TradeContext.agentSerialno
        HostContext.I1TRDT = TradeContext.workDate
        HostContext.I1UNSQ = TradeContext.preAgentSerno
        HostContext.I1OPTY = ''
        HostContext.I1OPFG = '0'                                        #(0.����,1.����)
        HostContext.I1RVSB = '0'                                        #(0���ز�-NO, 1	�ز�-YES)

    AfaLoggerFunc.tradeInfo('��ʼ��map�ļ���Ϣ[InitHostReq]���')

    return True

#====================��ʼ�������������ӿ�===========================
def InitGLHostReq( ):

    if (TradeContext.HostCode == '8808'):
        #��ѯ��������
        return True
        
    if (TradeContext.HostCode == '8810'):
        #��ѯ�ʻ���Ϣ
        return True


    if (TradeContext.HostCode == '8812'):
        #���������ʻ��Ǽǽ���
        return True                                         
                                                            
                                                            
    if (TradeContext.HostCode == '8814'):                   
        #��������                                           
        return True                                         
                                                            
                                                            
    if (TradeContext.HostCode == '8815'):                   
        #������ѯ                                           
        return True                                         
                                                            
                                                            
    if (TradeContext.HostCode == '8818'):                   
        #������ϸ����                                       
        return True                                         
                                                            
                                                            
    if (TradeContext.HostCode == '8819'):                   
        #����ļ��Ƿ�����                                   
        return True

        
    if (TradeContext.HostCode == '8847'):
        #����ļ��Ƿ�����
        return True
    
    

#====================���������ݽ���=============================
def CommHost( result = None ):

    AfaLoggerFunc.tradeInfo('>>>����ͨѶ����[CommHost]')
        
    TradeContext.errorCode = 'H999'
    TradeContext.errorMsg  = 'ϵͳ�쳣(������ͨѶ)'

    #�����������ױ�־TradeContext.revTranF�жϾ���ѡ���ĸ�map�ļ��������ӿڷ�ʽ
    if not result:
        result=TradeContext.revTranF
        #===================��ʼ��=======================
        if not InitHostReq(result) :
            TradeContext.__status__='1'
            return False

    if (result == '0'):
        AfaLoggerFunc.tradeInfo('>>>���ʼ���')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8813.map'
        TradeContext.HostCode = '8813'

    elif (result == '1' or result == '2' ):
        AfaLoggerFunc.tradeInfo('>>>����Ĩ��')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8820.map'
        TradeContext.HostCode = '8820'

    elif (result == '8808'):
        AfaLoggerFunc.tradeInfo('>>>��ѯ��������')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8808.map'
        TradeContext.HostCode = '8808'
        InitGLHostReq()
            
    elif (result == '8810'):
        AfaLoggerFunc.tradeInfo('>>>��ѯ�ʻ���Ϣ')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8810.map'
        TradeContext.HostCode = '8810'
        InitGLHostReq()
            
    elif (result == '8812'):
        AfaLoggerFunc.tradeInfo('>>>���������ʻ��Ǽǽ���')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8812.map'
        TradeContext.HostCode = '8812'
        InitGLHostReq()

    elif (result == '8814'):
        AfaLoggerFunc.tradeInfo('>>>��������')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8814.map'
        TradeContext.HostCode = '8814'
        InitGLHostReq()

    elif (result == '8815'):
        AfaLoggerFunc.tradeInfo('>>>������ѯ')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8815.map'
        TradeContext.HostCode = '8815'
        InitGLHostReq()

    elif (result == '8818'):
        AfaLoggerFunc.tradeInfo('>>>������ϸ����')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8818.map'
        TradeContext.HostCode = '8818'
        InitGLHostReq()

    elif (result == '8819'):
        AfaLoggerFunc.tradeInfo('>>>����ļ��Ƿ�����')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8819.map'
        TradeContext.HostCode = '8819'
        InitGLHostReq()

    elif (result == '8847'):
        AfaLoggerFunc.tradeInfo('>>>�Թ��ʺ���ˮ��ϸ��ѯ')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8847.map'
        TradeContext.HostCode = '8847'
        InitGLHostReq()

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
        TradeContext.bankSerno = HostContext.O1TLSQ                               #��Ա��ˮ��
        TradeContext.bankCode  = HostContext.O1MGID                               #�������ش���
        return True

    else:                                  #ʧ��
        TradeContext.__status__='1'
        TradeContext.errorCode, TradeContext.errorMsg = HostContext.O1MGID, HostContext.O1INFO
        return False
