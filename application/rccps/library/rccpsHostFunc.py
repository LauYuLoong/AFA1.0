# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.������ͨѶ����
#=================================================================
#   �����ļ�:   rccpsHostFunc.py
#   �޸�ʱ��:   2006-09-12
#
##################################################################
import TradeContext,AfaFunc,UtilTools,HostComm,HostContext,HostDataHandler,AfaLoggerFunc,os,AfaFlowControl
from types import *

def InitHostReq(hostType ):
    #��ʼ����������ֵ����
    AfaLoggerFunc.tradeInfo('��ʼ��map�ļ���Ϣ[InitHostReq]')
    
    #�ر�� 20081105 �ƶ�InitHostReq�����г�ʼ��8810�����ӿ���س������˴�
    if (hostType == '8810'):

        AfaLoggerFunc.tradeInfo('>>>��ѯ�˻���Ϣ')

        HostContext.I1TRCD = TradeContext.HostCode              #������

        HostContext.I1SBNO = TradeContext.BESBNO                  #�����

        HostContext.I1USID = TradeContext.BETELR              #��Ա��

        if TradeContext.existVariable ( 'BEAUUS') and TradeContext.BEAUUS != '' and TradeContext.existVariable('BEAUPS') and TradeContext.BEAUPS != '':
            HostContext.I1AUUS = TradeContext.BEAUUS        #��Ȩ��Ա
            HostContext.I1AUPS = TradeContext.BEAUPS           #��Ȩ����
        else:
            HostContext.I1AUUS = ''
            HostContext.I1AUPS = ''

        if TradeContext.existVariable('TERMID') and TradeContext.TERMID != '':
            HostContext.I1WSNO = TradeContext.TERMID                #�ն˺�
        else:
            HostContext.I1WSNO = '1234567890'                #�ն˺�

        HostContext.I1ACNO = TradeContext.ACCNO                 #�ʺ�
        HostContext.I1CYNO = '01'                              #����

        if TradeContext.existVariable('PASSWD') and TradeContext.PASSWD != '':
            HostContext.I1CFFG = '0'
            HostContext.I1PSWD = TradeContext.PASSWD
        else:
            HostContext.I1CFFG = '1'                               #����У���־
            HostContext.I1PSWD = ''                                #����
        if TradeContext.existVariable('WARNTNO') and TradeContext.WARNTNO != '':     #ƾ֤����
            HostContext.I1CETY = TradeContext.WARNTNO[0:2]

            HostContext.I1CCSQ = TradeContext.WARNTNO[2:]
        else:
            HostContext.I1CETY = ''                                #ƾ֤����
            HostContext.I1CCSQ = ''                             #ƾ֤����

        AfaLoggerFunc.tradeInfo("I1CETY=[" + HostContext.I1CETY + "]")
        AfaLoggerFunc.tradeInfo("I1CCSQ=[" + HostContext.I1CCSQ + "]")

        HostContext.I1CTFG = '0'                               #�����־

    #�ر��  20081215  ����У��ŵ���Ϣ
    if (hostType == '0652'):

        AfaLoggerFunc.tradeInfo('>>>��֤�ŵ���Ϣ')

        HostContext.I1TRCD = TradeContext.HostCode             #������

        HostContext.I1SBNO = TradeContext.BESBNO                  #�����

        HostContext.I1USID = TradeContext.BETELR              #��Ա��

        if TradeContext.existVariable ( 'BEAUUS') and TradeContext.BEAUUS != '' and TradeContext.existVariable('BEAUPS') and TradeContext.BEAUPS != '':
            HostContext.I1AUUS = TradeContext.BEAUUS        #��Ȩ��Ա
            HostContext.I1AUPS = TradeContext.BEAUPS           #��Ȩ����
        else:
            HostContext.I1AUUS = ''
            HostContext.I1AUPS = ''

        if TradeContext.existVariable('TERMID') and TradeContext.TERMID != '':
            HostContext.I1WSNO = TradeContext.TERMID                #�ն˺�
        else:
            HostContext.I1WSNO = '1234567890'                #�ն˺�

        if TradeContext.existVariable('WARNTNO') and TradeContext.WARNTNO != '':     #ƾ֤����
            HostContext.I1CARD = TradeContext.WARNTNO
        else:
            HostContext.I1CARD = ''                                #ƾ֤����
        
        if TradeContext.existVariable('SCTRKINF') and TradeContext.SCTRKINF != '':   #���ŵ���Ϣ
            HostContext.I1AMTT = TradeContext.SCTRKINF
        else:
            HostContext.I1AMTT = TradeContext.SCTRKINF
        
        if TradeContext.existVariable('THTRKINF') and TradeContext.THTRKINF != '':   #���ŵ���Ϣ
            HostContext.I1AMST = TradeContext.THTRKINF
        else:
            HostContext.I1AMST = TradeContext.THTRKINF

    if (hostType =='8813'): # ������

        AfaLoggerFunc.tradeInfo('>>>������')

        HostContext.I1TRCD = '8813'

        HostContext.I1SBNO = TradeContext.BESBNO

        HostContext.I1USID = TradeContext.BETELR

        if TradeContext.existVariable ( 'BEAUUS') and TradeContext.BEAUUS != '' and TradeContext.existVariable('BEAUPS') and TradeContext.BEAUPS != '':
            HostContext.I1AUUS = TradeContext.BEAUUS  #��Ȩ��Ա
            HostContext.I1AUPS = TradeContext.BEAUPS  #��Ȩ����
        else:
            HostContext.I1AUUS = ''
            HostContext.I1AUPS = ''

        if TradeContext.existVariable('TERMID') and TradeContext.TERMID != '':
            HostContext.I1WSNO = TradeContext.TERMID    #�ն˺�
        else:
            HostContext.I1WSNO = '1234567890'
        
        #=====������ 20080804 �����ظ�����====
        if TradeContext.existVariable('ACUR') and TradeContext.ACUR != '':
            HostContext.I1ACUR  = TradeContext.ACUR
        else:
            HostContext.I1ACUR  =  '1'
            
        HostContext.I2NBBH = []                             #����ҵ���
        HostContext.I2NBBH.append('RCC')

        #�ر�� 20081230 ����CLDT,UNSQ���ԭǰ�����ں�ǰ����ˮ��
        HostContext.I2CLDT = []                             #����ί������
        if TradeContext.existVariable('CLDT') and TradeContext.CLDT != '':
            HostContext.I2CLDT.append(TradeContext.CLDT)
        else:
            HostContext.I2CLDT.append('')

        HostContext.I2UNSQ = []                             #����ί�к�
        if TradeContext.existVariable('UNSQ') and TradeContext.UNSQ != '':
            HostContext.I2UNSQ.append(TradeContext.UNSQ)
        else:
            HostContext.I2UNSQ.append('')

        HostContext.I2FEDT = []                             #ǰ������
        if TradeContext.existVariable('FEDT') and TradeContext.FEDT != '':
            HostContext.I2FEDT.append(TradeContext.FEDT)
        else:
            HostContext.I2FEDT.append(TradeContext.BJEDTE)

        HostContext.I2RBSQ = []                             #ǰ����ˮ��
        if TradeContext.existVariable('RBSQ') and TradeContext.RBSQ != '':
            HostContext.I2RBSQ.append(TradeContext.RBSQ)
        else:
            HostContext.I2RBSQ.append(TradeContext.BSPSQN)

        HostContext.I2DATE = []                             #��ϵͳ��������
        HostContext.I2DATE.append(TradeContext.NCCworkDate)

        HostContext.I2RVFG = []                             #�����ֱ�־
        if TradeContext.existVariable( 'RVFG' ) and TradeContext.RVFG != '':
            HostContext.I2RVFG.append(TradeContext.RVFG)
        else:
            HostContext.I2RVFG.append('')

        HostContext.I2SBNO = []                             #���׻���
        HostContext.I2SBNO.append(TradeContext.BESBNO)

        HostContext.I2TELR = []                             #���׹�Ա
        HostContext.I2TELR.append(TradeContext.BETELR)

        HostContext.I2TRSQ = []                             #���
        HostContext.I2TRSQ.append('1')

        HostContext.I2TINO = []                             #�������
        HostContext.I2TINO.append('1')


        HostContext.I2CYNO = []                             #����
        HostContext.I2CYNO.append('01')

        HostContext.I2WLBZ = []                             #�����ʱ�־
        HostContext.I2WLBZ.append(TradeContext.BRSFLG)

        HostContext.I2TRAM = []                             #������
        HostContext.I2TRAM.append(TradeContext.OCCAMT)

        HostContext.I2SMCD = []                             #ժҪ����
        if TradeContext.existVariable ('RCCSMCD') and TradeContext.RCCSMCD != '':
            HostContext.I2SMCD.append(TradeContext.RCCSMCD)
        else:
            HostContext.I2SMCD.append('')

        HostContext.I2NMFG = []                             #����У���־
        if TradeContext.existVariable ('NMCKFG') and TradeContext.NMCKFG != '':
            HostContext.I2NMFG.append(TradeContext.NMCKFG)
        else:
            HostContext.I2NMFG.append('0')

        #=====�����������  ������ 20080609====
        HostContext.I2DASQ = []
        if TradeContext.existVariable( 'DASQ' ) and TradeContext.DASQ != '':
            HostContext.I2DASQ.append(TradeContext.DASQ)
        else:
            HostContext.I2DASQ.append('')

        HostContext.I2APX1 = []                             #������Ϣ1(��λ����)
        HostContext.I2APX1.append('')

        HostContext.I2RBAC = []        #�����˺�
        if TradeContext.existVariable( 'RBAC' ) and TradeContext.RBAC != '':
            HostContext.I2RBAC.append(TradeContext.RBAC)
        else:
            HostContext.I2RBAC.append('')

        HostContext.I2OTNM = []        #��������
        if TradeContext.existVariable( 'OTNM' ) and TradeContext.OTNM != '':
            HostContext.I2OTNM.append(TradeContext.OTNM)
        else:
            HostContext.I2OTNM.append('')

        HostContext.I2SBAC = []        #�跽�˺�
        if TradeContext.existVariable('SBAC') and TradeContext.SBAC != '':
            HostContext.I2SBAC.append(TradeContext.SBAC)
        else:
            HostContext.I2SBAC.append('')

        HostContext.I2ACNM = []        #�跽����
        if TradeContext.existVariable('ACNM') and TradeContext.ACNM != '':
            HostContext.I2ACNM.append(TradeContext.ACNM)
        else:
            HostContext.I2ACNM.append('')

        HostContext.I2REAC = []        #�����˺�
        if TradeContext.existVariable('REAC') and TradeContext.REAC != '':
            HostContext.I2REAC.append(TradeContext.REAC)
        else:
            HostContext.I2REAC.append('')

        if TradeContext.existVariable('PASSWD') and TradeContext.PASSWD != '':
            HostContext.I2CFFG = []
            HostContext.I2CFFG.append('Y')              #����У�鷽ʽ
            AfaLoggerFunc.tradeDebug('>>>����У�鷽ʽ:'+str(HostContext.I2CFFG))

            HostContext.I2PSWD = []
            HostContext.I2PSWD.append(TradeContext.PASSWD)
            AfaLoggerFunc.tradeDebug('>>>����:'+str(TradeContext.PASSWD))
        else:
            HostContext.I2CFFG = []
            HostContext.I2CFFG.append('N')              #����У�鷽ʽ

            HostContext.I2PSWD = []
            HostContext.I2PSWD.append('')
            AfaLoggerFunc.tradeDebug('>>>����['+str(HostContext.I2PSWD)+']')

        if TradeContext.existVariable('CERTTYPE') and TradeContext.CERTTYPE != '' and TradeContext.existVariable('CERTNO') and TradeContext.CERTNO != '':
            HostContext.I2OPTY = []                     #֤��У���־
            HostContext.I2OPTY.append('1')

            HostContext.I2IDTY = []                     #֤������
            HostContext.I2IDTY.append(TradeContext.CERTTYPE)

            HostContext.I2IDNO = []                     #֤������
            HostContext.I2IDNO.append(TradeContext.CERTNO)
        else:
            HostContext.I2OPTY = []                             #֤��У���־
            HostContext.I2OPTY.append('0')

            HostContext.I2IDTY = []                     #֤������
            HostContext.I2IDTY.append('')

            HostContext.I2IDNO = []                     #֤������
            HostContext.I2IDNO.append('')

        if TradeContext.existVariable('WARNTNO') and TradeContext.WARNTNO != '':     #ƾ֤����
            HostContext.I2CETY = []
            HostContext.I2CETY.append(TradeContext.WARNTNO[0:2])

            HostContext.I2CCSQ = []
            HostContext.I2CCSQ.append(TradeContext.WARNTNO[2:])

            #=====������ 20080805 ����====
            HostContext.I2TRFG = []#ƾ֤�����־
            HostContext.I2TRFG.append('9')

            if (TradeContext.existVariable('BBSSRC') and TradeContext.BBSSRC=='2' ):     #�ʽ���ԴΪ 2-�Թ�����
                HostContext.I2CFFG = []
                HostContext.I2CFFG.append('N')          #����У�鷽ʽ��֧Ʊ��У������

                HostContext.I2TRFG = []#ƾ֤�����־
                HostContext.I2TRFG.append('0')
        else:
            HostContext.I2CETY = []                     #ƾ֤����
            HostContext.I2CETY.append('')

            HostContext.I2CCSQ = []                     #ƾ֤����
            HostContext.I2CCSQ.append('')

            HostContext.I2TRFG = []                     #ƾ֤�����־
            HostContext.I2TRFG.append('9')

        HostContext.I2CATR = []
        if TradeContext.existVariable('CATR') and TradeContext.CATR != '':        #��ת��־
            HostContext.I2CATR.append(TradeContext.CATR)
        else:
            HostContext.I2CATR.append('1')
        
        AfaLoggerFunc.tradeDebug('>>>��ת��־['+str(HostContext.I2CATR)+']')
            
        HostContext.I2PKFG = []
        if TradeContext.existVariable('PKFG') and TradeContext.PKFG != '':    #ͨ��ͨ�ұ�ʶ
            HostContext.I2PKFG.append(TradeContext.PKFG)
        else:
            HostContext.I2PKFG.append('')
        
        HostContext.I2CTFG = []
        if TradeContext.existVariable('CTFG') and TradeContext.CTFG != '':     #ͨ��ͨ�ұ����־
            HostContext.I2CTFG.append(TradeContext.CTFG)
        else:
            HostContext.I2CTFG.append('')

        #=====������ 20080804 ������Ʊǩ������ƾ֤�Ĵ���====
        if int(HostContext.I1ACUR) >=2:
            AfaLoggerFunc.tradeDebug('>>>��ʼ��ӵڶ�����¼')
            if TradeContext.existVariable('PKFG') and TradeContext.PKFG != '':    #ͨ��ͨ�ұ�ʶ
                HostContext.I2PKFG.append(TradeContext.PKFG)
            else:
                HostContext.I2PKFG.append('')
                
            #=====����ҵ��� RCC-ũ����====
            HostContext.I2NBBH.append('RCC')

            #�ر�� 20081230 ����CLDT,UNSQ���ԭǰ�����ں�ǰ����ˮ��
            #=====����ί������=====
            if TradeContext.existVariable('CLDT') and TradeContext.CLDT != '':
                HostContext.I2CLDT.append(TradeContext.CLDT)
            else:
                HostContext.I2CLDT.append('')
            #=====����ί�к�=====
            if TradeContext.existVariable('UNSQ') and TradeContext.UNSQ != '':
                HostContext.I2UNSQ.append(TradeContext.UNSQ)
            else:
                HostContext.I2UNSQ.append('')

            #=====ǰ������====
            if TradeContext.existVariable('FEDT') and TradeContext.FEDT != '':
                HostContext.I2FEDT.append(TradeContext.FEDT)
            else:
                HostContext.I2FEDT.append(TradeContext.BJEDTE)
            #=====ǰ����ˮ��====
            if TradeContext.existVariable('RBSQ') and TradeContext.RBSQ != '':
                HostContext.I2RBSQ.append(TradeContext.RBSQ)
            else:
                HostContext.I2RBSQ.append(TradeContext.BSPSQN)
            #HostContext.I2RBSQ.append(TradeContext.BSPSQN)
            HostContext.I2DATE.append(TradeContext.NCCworkDate)
            #=====�����ֱ�־====
            if TradeContext.existVariable('I2RVFG') and TradeContext.I2RVFG != '':
                HostContext.I2RVFG.append(TradeContext.I2RVFG)
            else:
                HostContext.I2RVFG.append('')
            #=====���׻���====
            HostContext.I2SBNO.append(TradeContext.BESBNO)
            #=====���׹�Ա====
            HostContext.I2TELR.append(TradeContext.BETELR)
            #=====���====
            HostContext.I2TRSQ.append('1')
            #=====�������====
            HostContext.I2TINO.append('2')
            #=====����====
            HostContext.I2CYNO.append('01')
            #=====�����˱�־====
            HostContext.I2WLBZ.append(TradeContext.BRSFLG)
            #=====�������====
            HostContext.I2DASQ.append('')
            #=====������Ϣ1====
            HostContext.I2APX1.append('')
            #=====����У���־====
            if TradeContext.existVariable('I2NMFG') and TradeContext.I2NMFG != '':
                HostContext.I2NMFG.append(TradeContext.I2NMFG)
            else:
                HostContext.I2NMFG.append('0')
            #=====�����˺�====
            if TradeContext.existVariable('I2RBAC') and TradeContext.I2RBAC != '':
                HostContext.I2RBAC.append(TradeContext.I2RBAC)
            else:
                HostContext.I2RBAC.append('')
            #=====��������====
            if TradeContext.existVariable('I2OTNM') and TradeContext.I2OTNM != '':
                HostContext.I2OTNM.append(TradeContext.I2OTNM)
            else:
                HostContext.I2OTNM.append('')
            #=====�跽�˺�====
            if TradeContext.existVariable('I2SBAC') and TradeContext.I2SBAC != '':
                HostContext.I2SBAC.append(TradeContext.I2SBAC)
            else:
                HostContext.I2SBAC.append('')
            #=====�跽����====
            if TradeContext.existVariable('I2ACNM') and TradeContext.I2ACNM != '':
                HostContext.I2ACNM.append(TradeContext.I2ACNM)
            else:
                HostContext.I2ACNM.append('')
            #=====�����˺�====
            if TradeContext.existVariable('I2REAC') and TradeContext.I2REAC != '':
                HostContext.I2REAC.append(TradeContext.I2REAC)
            else:
                HostContext.I2REAC.append('')
            if TradeContext.existVariable('I2PSWD') and TradeContext.I2PSWD != '':
                #=====����У�鷽ʽ====
                HostContext.I2CFFG.append('Y')              #����У�鷽ʽ
                #=====����====
                HostContext.I2PSWD.append(TradeContext.I2PSWD)
            else:
                #=====����У�鷽ʽ====
                HostContext.I2CFFG.append('N')              #����У�鷽ʽ
                #=====����====
                HostContext.I2PSWD.append('')
            
            #�ر��  20081117 �޸ĵڶ��ʷ�¼֤��У����ش���
            #=====֤��У���־====
            #HostContext.I2OPTY.append('')
            #=====֤������====
            #HostContext.I2IDTY.append('')
            #HostContext.I2IDTY.append('')
            #=====֤������====
            #HostContext.I2IDNO.append('')
            
            if TradeContext.existVariable('I2IDTY') and TradeContext.I2IDTY != '' and TradeContext.existVariable('I2IDNO') and TradeContext.I2IDNO != '':
                HostContext.I2OPTY.append('1')
            
                HostContext.I2IDTY.append(TradeContext.I2IDTY)
            
                HostContext.I2IDNO.append(TradeContext.I2IDNO)
            else:
                HostContext.I2OPTY.append('0')
            
                HostContext.I2IDTY.append('')
            
                HostContext.I2IDNO.append('')
            
            #=====��ת��־====
            if TradeContext.existVariable('I2CATR') and TradeContext.I2CATR != '':
                HostContext.I2CATR.append(TradeContext.I2CATR)
            else:
                HostContext.I2CATR.append('1')
                
            
            if TradeContext.existVariable('I2CTFG') and TradeContext.I2CTFG != '':     #ͨ��ͨ�ұ����־
                HostContext.I2CTFG.append(TradeContext.I2CTFG)
            else:
                HostContext.I2CTFG.append('')
                
            if TradeContext.existVariable('PKFG') and TradeContext.PKFG in ('T','E','W'): #ͨ��ͨ�ұ�ʶ:T-ͨ��ͨ��,W-�ֹ���ת,E-���˲���
                #ͨ��ͨ�ҵڶ��ʷ�¼���⴦��   �ر��
                if TradeContext.existVariable('I2WARNTNO') and TradeContext.I2WARNTNO != '':
                    #=====ƾ֤�����־====
                    HostContext.I2TRFG.append('9')
                    #=====ƾ֤����====
                    HostContext.I2CETY.append(TradeContext.I2WARNTNO[0:2])
                    #=====ƾ֤����====
                    HostContext.I2CCSQ.append(TradeContext.I2WARNTNO[2:])
                else:
                    HostContext.I2TRFG.append('9')
                    HostContext.I2CETY.append('')
                    HostContext.I2CCSQ.append('')
                    
                #=====������====
                HostContext.I2TRAM.append(TradeContext.I2TRAM)
                #=====ժҪ����====
                if TradeContext.existVariable('I2SMCD') and TradeContext.I2SMCD != '':
                    HostContext.I2SMCD.append(TradeContext.I2SMCD)
                else:
                    HostContext.I2SMCD.append('')

            elif TradeContext.existVariable('TRCTYP') and TradeContext.TRCTYP == '20': #��ұ�ʶ
                #�ر�� 20091123 ��ҵڶ��ʷ�¼���⴦��
                if TradeContext.existVariable('I2WARNTNO') and TradeContext.I2WARNTNO != '':
                    #=====ƾ֤�����־====
                    HostContext.I2TRFG.append('9')
                    #=====ƾ֤����====
                    HostContext.I2CETY.append(TradeContext.I2WARNTNO[0:2])
                    #=====ƾ֤����====
                    HostContext.I2CCSQ.append(TradeContext.I2WARNTNO[2:])
                else:
                    HostContext.I2TRFG.append('9')
                    HostContext.I2CETY.append('')
                    HostContext.I2CCSQ.append('')
                    
                #=====������====
                HostContext.I2TRAM.append(TradeContext.I2TRAM)
                #=====ժҪ����====
                if TradeContext.existVariable('I2SMCD') and TradeContext.I2SMCD != '':
                    HostContext.I2SMCD.append(TradeContext.I2SMCD)
                else:
                    HostContext.I2SMCD.append('')

            else:
                #��Ʊ�ڶ��ʷ�¼���⴦��
                #=====ƾ֤�����־====
                if TradeContext.existVariable('TRFG') and TradeContext.TRFG != '':
                    HostContext.I2TRFG.append(TradeContext.TRFG)
                else:
                    HostContext.I2TRFG.append('9')
                #=====ƾ֤����====
                #=====��Ʊ�⸶����ʱ����Ϊ��====
                if TradeContext.existVariable('I2CETY'):
                    HostContext.I2CETY.append(TradeContext.I2CETY)
                else:
                    HostContext.I2CETY.append('68')
                #=====ƾ֤����====
                #=====��Ʊ�⸶����ʱ����Ϊ��====
                #=====begin ������ 20110215 �޸�=====
                #if TradeContext.existVariable('BILNO'):                
                #    HostContext.I2CCSQ.append(TradeContext.BILNO)
                #else:
                #    HostContext.I2CCSQ.append('')
                if TradeContext.existVariable('BILNO'):                
                    if len(TradeContext.BILNO) == 16:
                        HostContext.I2CCSQ.append(TradeContext.BILNO[-8:])
                        HostContext.I2AMTT = []
                        HostContext.I2AMTT.append('')
                        HostContext.I2AMTT.append(TradeContext.BILNO)
                    else:
                        HostContext.I2CCSQ.append(TradeContext.BILNO)
                else:
                    HostContext.I2CCSQ.append('')
                #===========end============
                
                #=====������====
                if TradeContext.existVariable('I2TRAM') and TradeContext.I2TRAM != '':
                    HostContext.I2TRAM.append(TradeContext.I2TRAM)
                else:
                    HostContext.I2TRAM.append('1.00')
                
                #=====ժҪ����====
                if TradeContext.existVariable('I2SMCD') and TradeContext.I2SMCD != '':
                    HostContext.I2SMCD.append(TradeContext.I2SMCD)
                else:
                    HostContext.I2SMCD.append('610')
                
        #=====������ 20081105 ����ͨ��ͨ�Ҽ��˵Ĵ���====
        if int(HostContext.I1ACUR) >= 3:
            AfaLoggerFunc.tradeDebug('>>>��ʼ��ӵ�������¼')
            if TradeContext.existVariable('PKFG') and TradeContext.PKFG != '':    #ͨ��ͨ�ұ�ʶ
                HostContext.I2PKFG.append(TradeContext.PKFG)
            else:
                HostContext.I2PKFG.append('')
            if TradeContext.existVariable('I3WARNTNO') and TradeContext.I3WARNTNO != '':
                #=====ƾ֤�����־====
                HostContext.I2TRFG.append('9')
                #=====ƾ֤����====
                HostContext.I2CETY.append(TradeContext.I2WARNTNO)
                #=====ƾ֤����====
                HostContext.I2CCSQ.append(TradeContext.I2WARNTNO)
            else:
                HostContext.I2TRFG.append('9')
                HostContext.I2CETY.append('')
                HostContext.I2CCSQ.append('')

            #=====������====
            HostContext.I2TRAM.append(TradeContext.I3TRAM)
            #=====����ҵ��� RCC-ũ����====
            HostContext.I2NBBH.append('RCC')

            #�ر��  ����CLDT,UNSQ���ԭǰ������ǰ����ˮ��
            #=====����ί������=====
            if TradeContext.existVariable('CLDT') and TradeContext.CLDT != '':
                HostContext.I2CLDT.append(TradeContext.CLDT)
            else:
                HostContext.I2CLDT.append('')
            #=====����ί����ˮ��=====
            if TradeContext.existVariable('UNSQ') and TradeContext.UNSQ != '':
                HostContext.I2UNSQ.append(TradeContext.UNSQ)
            else:
                HostContext.I2UNSQ.append('')

            #=====ǰ������====
            if TradeContext.existVariable('FEDT') and TradeContext.FEDT != '':
                HostContext.I2FEDT.append(TradeContext.FEDT)
            else:
                HostContext.I2FEDT.append(TradeContext.BJEDTE)
            #=====ǰ����ˮ��====
            if TradeContext.existVariable('RBSQ') and TradeContext.RBSQ != '':
                HostContext.I2RBSQ.append(TradeContext.RBSQ)
            else:
                HostContext.I2RBSQ.append(TradeContext.BSPSQN)
            #HostContext.I2RBSQ.append(TradeContext.BSPSQN)
            HostContext.I2DATE.append(TradeContext.NCCworkDate)
            #=====�����ֱ�־====
            if TradeContext.existVariable('I3RVFG') and TradeContext.I3RVFG != '':
                HostContext.I2RVFG.append(TradeContext.I3RVFG)
            else:
                HostContext.I2RVFG.append('')
            #=====���׻���====
            HostContext.I2SBNO.append(TradeContext.BESBNO)
            #=====���׹�Ա====
            HostContext.I2TELR.append(TradeContext.BETELR)
            #=====���====
            HostContext.I2TRSQ.append('1')
            #=====�������====
            HostContext.I2TINO.append('3')
            #=====����====
            HostContext.I2CYNO.append('01')
            #=====�����˱�־====
            HostContext.I2WLBZ.append(TradeContext.BRSFLG)
            #=====ժҪ����====
            if TradeContext.existVariable('I3SMCD') and TradeContext.I3SMCD != '':
                HostContext.I2SMCD.append(TradeContext.I3SMCD)
            else:
                HostContext.I2SMCD.append('')
            #=====����У���־====
            HostContext.I2NMFG.append('0')
            #=====�������====
            HostContext.I2DASQ.append('')
            #=====������Ϣ1====
            HostContext.I2APX1.append('')
            #=====�����˺�====
            if TradeContext.existVariable('I3RBAC') and TradeContext.I3RBAC != '':
                HostContext.I2RBAC.append(TradeContext.I3RBAC)
            else:
                HostContext.I2RBAC.append('')
            #=====��������====
            if TradeContext.existVariable('I3OTNM') and TradeContext.I3OTNM != '':
                HostContext.I2OTNM.append(TradeContext.I3OTNM)
            else:
                HostContext.I2OTNM.append('')
            #=====�跽�˺�====
            if TradeContext.existVariable('I3SBAC') and TradeContext.I3SBAC != '':
                HostContext.I2SBAC.append(TradeContext.I3SBAC)
            else:
                HostContext.I2SBAC.append('')
            #=====�跽����====
            if TradeContext.existVariable('I3ACNM') and TradeContext.I3ACNM != '':
                HostContext.I2ACNM.append(TradeContext.I3ACNM)
            else:
                HostContext.I2ACNM.append('')
            #=====�����˺�====
            if TradeContext.existVariable('I3REAC') and TradeContext.I3REAC != '':
                HostContext.I2REAC.append(TradeContext.I3REAC)
            else:
                HostContext.I2REAC.append('')
            #=====����У�鷽ʽ====
            if TradeContext.existVariable('I3PSWD') and TradeContext.I3PSWD != '':
                HostContext.I2CFFG.append('Y')   #����У�鷽ʽ
                #=====����====
                HostContext.I2PSWD.append(TradeContext.I3PSWD)
            else:
                HostContext.I2CFFG.append('N')
                #=====����====
                HostContext.I2PSWD.append('')
            
            #�ر��  20081117  �޸ĵ����ʷ�¼֤��У����ش���
            #=====֤��У���־====
            #HostContext.I2OPTY.append('')
            #=====֤������====
            #HostContext.I2IDTY.append('')
            #HostContext.I2IDTY.append('')
            #=====֤������====
            #HostContext.I2IDNO.append('')

            if TradeContext.existVariable('I3IDTY') and TradeContext.I3IDTY != '' and TradeContext.existVariable('I3IDNO') and TradeContext.I3IDNO != '':
                HostContext.I2OPTY.append('1')

                HostContext.I2IDTY.append(TradeContext.I3IDTY)

                HostContext.I2IDNO.append(TradeContext.I3IDNO)
            else:
                HostContext.I2OPTY.append('0')

                HostContext.I2IDTY.append('')

                HostContext.I2IDNO.append('')

            #=====��ת��־====
            if TradeContext.existVariable('I3CATR') and TradeContext.I3CATR != '':
                HostContext.I2CATR.append(TradeContext.I3CATR)
            else:
                HostContext.I2CATR.append('1')
            
            if TradeContext.existVariable('I3CTFG') and TradeContext.I3CTFG != '':     #ͨ��ͨ�ұ����־
                HostContext.I2CTFG.append(TradeContext.I3CTFG)
            else:
                HostContext.I2CTFG.append('')

    elif (hostType =='8820'):   #������

        AfaLoggerFunc.tradeInfo('>>>������')

        HostContext.I1TRCD = '8820'

        HostContext.I1SBNO = TradeContext.BESBNO

        HostContext.I1USID = TradeContext.BETELR

        if TradeContext.existVariable ( 'BEAUUS') and TradeContext.BEAUUS != '' and TradeContext.existVariable('BEAUPS') and TradeContext.BEAUPS != '':
            HostContext.I1AUUS = TradeContext.BEAUUS
            HostContext.I1AUPS = TradeContext.BEAUPS
        else:
            HostContext.I1AUUS = ''
            HostContext.I1AUPS = ''

        if TradeContext.existVariable ( 'TERMID' ) and TradeContext.TERMID != '':
            HostContext.I1WSNO = TradeContext.TERMID
        else:
            HostContext.I1WSNO = ''

        HostContext.I1NBBH = 'RCC'
        HostContext.I1FEDT = TradeContext.BOJEDT
        HostContext.I1DATE = TradeContext.BOJEDT
        HostContext.I1RBSQ = TradeContext.BOSPSQ
        HostContext.I1TRDT = TradeContext.BOJEDT
        HostContext.I1UNSQ = TradeContext.BOSPSQ
        HostContext.I1OPTY = ''
        HostContext.I1OPFG = '0'       #(0.����,1.����)
        HostContext.I1RVSB = '0'       #(0���ز�-NO, 1	�ز�-YES)

    AfaLoggerFunc.tradeInfo('��ʼ��map�ļ���Ϣ[InitHostReq]���')

    return True

#====================��ʼ�������������ӿ�===========================
def InitGLHostReq( ):

    #��������
    HostContext.I1TRCD = TradeContext.HostCode              #������

    HostContext.I1SBNO = TradeContext.BESBNO                  #�����

    HostContext.I1USID = TradeContext.BETELR              #��Ա��

    if TradeContext.existVariable ( 'BEAUUS') and TradeContext.BEAUUS != '' and TradeContext.existVariable('BEAUPS') and TradeContext.BEAUPS != '':
        HostContext.I1AUUS = TradeContext.BEAUUS        #��Ȩ��Ա
        HostContext.I1AUPS = TradeContext.BEAUPS           #��Ȩ����
    else:
        HostContext.I1AUUS = ''
        HostContext.I1AUPS = ''

    if TradeContext.existVariable('TERMID') and TradeContext.TERMID != '':
        HostContext.I1WSNO = TradeContext.TERMID                #�ն˺�
    else:
        HostContext.I1WSNO = '1234567890'                #�ն˺�

    #˽�в���
    #�ر�� 20081105 �ƶ�8810����ӿڳ�ʼ��������InitHostReq������
    #if (TradeContext.HostCode == '8810'):
    #    #��ѯ�ʻ���Ϣ
    #    HostContext.I1ACNO = TradeContext.ACCNO                 #�ʺ�
    #    HostContext.I1CYNO = '01'    		                #����
    #    HostContext.I1CFFG = '1'         	                #����У���־
    #    HostContext.I1PSWD = ''          	                #����
    #    HostContext.I1CETY = ''          	                #ƾ֤����
    #    HostContext.I1CCSQ = ''                             #ƾ֤����
    #    HostContext.I1CTFG = '0'	                        #�����־
    #    return True

    if (TradeContext.HostCode == '8811'):
        #��ѯƾ֤��Ϣ
        AfaLoggerFunc.tradeDebug('>>>��ʼ��ѯƾ֤��Ϣ')
        HostContext.I1ACCN = TradeContext.ACCNO                 #�ʺ�
        HostContext.I1CETY = TradeContext.WARNTNO[0:2]         #ƾ֤����
        HostContext.I1CCSQ = TradeContext.WARNTNO[2:]       #ƾ֤����
        return True




    if (TradeContext.HostCode == '8812'):
        #���������ʻ��Ǽǽ���
        HostContext.I1TRFG = ''	    	                    #�����־(0-�Ǽ� 1-ȡ��)
        HostContext.I1ACCN = ''	    	                    #�ʺ�
        HostContext.I1PRCD = ''                             #�����־
        return True


    if (TradeContext.HostCode == '8814'):
        #��������
        HostContext.I1CLDT = ''	    	                    #����ί������
        HostContext.I1UNSQ = ''	    	                    #����ί�к�
        HostContext.I1NBBH = ''	    	                    #����ҵ���
        HostContext.I1OPFG = '2'	                        #�����־
        HostContext.I1TRFG = '1'	                        #�����־
        HostContext.I1RPTF = '0'	                        #�ظ���־
        HostContext.I1STDT = ''	                            #������ʼ����
        HostContext.I1ENDT = ''	                            #������ֹ����
        HostContext.I1COUT = ''	                            #ί���ܱ���
        HostContext.I1TOAM = ''	                            #ί���ܽ��
        HostContext.I1FINA = ''	                            #�����ļ�����
        return True


    if (TradeContext.HostCode == '8815'):
        #������ѯ
        HostContext.I1NBBH = 'RCC'                        #����ҵ���
        HostContext.I1CLDT = ''	                            #����ί������
        HostContext.I1UNSQ = ''	                            #����ί�к�
        HostContext.I1FINA = ''	                            #�´��ļ���
        HostContext.I1DWFG = '2'	                        #�´���־
        return True

    #=====������ 20081129 ����8816��ѯ��������====
    if (TradeContext.HostCode == '8816'):
        #���������ѯ
        if TradeContext.existVariable('OPFG') and TradeContext.OPFG != '':
            HostContext.I1OPFG = TradeContext.OPFG
        else:
            HostContext.I1OPFG = '1'                       #��ѯ����
        
        if TradeContext.existVariable('NBBH') and TradeContext.NBBH != '':
            HostContext.I1NBBH = TradeContext.NBBH
        else:
            HostContext.I1NBBH = 'RCC'                      #����ҵ���
        HostContext.I1FEDT = TradeContext.FEDT              #ԭǰ������
        HostContext.I1RBSQ = TradeContext.RBSQ              #ԭǰ����ˮ
        
        if TradeContext.existVariable('DATE') and TradeContext.DATE != '':
            HostContext.I1DATE = TradeContext.DATE
        else:
            HostContext.I1DATE = ''                         #ԭ��������
            
        if TradeContext.existVariable('I1TLSQ'):
            HostContext.I1TLSQ = TradeContext.I1TLSQ
        else:
            HostContext.I1TLSQ = ''                         #ԭ��������
        
        if TradeContext.existVariable('I1TRDT'):
            HostContext.I1TRDT = TradeContext.I1TRDT
        else:
            HostContext.I1TRDT = ''                         #ԭ��������
        
        if TradeContext.existVariable('I1RGSQ'):
            HostContext.I1RGSQ = TradeContext.I1RGSQ
        else:
            HostContext.I1RGSQ = ''                         #������ˮ
        
        if TradeContext.existVariable('DAFG'):
            HostContext.I1DAFG = TradeContext.DAFG
        else:
            HostContext.I1DAFG = '1'                        #Ĩ/���˱�־
        
        return True

    if (TradeContext.HostCode == '8818'):
        #������ϸ����
        HostContext.I1CLDT = ''	                            #����ί������
        HostContext.I1UNSQ = ''	                            #����ί�к�
        HostContext.I1NBBH = ''	                            #����ҵ���
        HostContext.I1DATE = ''	                            #��ϵͳ����
        HostContext.I1FINA = ''	                            #�´��ļ�����
        return True


    if (TradeContext.HostCode == '8819'):
        #����ļ��Ƿ�����
        HostContext.I1NBBH = ''	    	                    #����ҵ���
        HostContext.I1CLDT = ''	   	 	                    #ԭ��������
        HostContext.I1UNSQ = ''	    	                    #ԭ����ί�к�
        HostContext.I1FILE = ''	    	                    #ɾ���ļ���
        HostContext.I1OPFG = ''	    	                    #������־(0-��ѯ 1-ɾ���ϴ��ļ� 2-ɾ���´��ļ�)
        return True


    if (TradeContext.HostCode == '8847'):
        #����ļ��Ƿ�����
        HostContext.I1ACCN = ''	            #�Թ������ʺ�
        HostContext.I1STDT = ''	            #��ʼ����
        HostContext.I1EDDT = ''	            #��ֹ����
        HostContext.I1FINA = ''	            #�ļ�����
        return True

    #=====������ 20081205 �����������������ļ�====
    if (TradeContext.HostCode == '8825'):
        if TradeContext.existVariable('STRDAT'):
            HostContext.I1STDT = TradeContext.STRDAT
        else:
            HostContext.I1STDT = '' 

        if TradeContext.existVariable('ENDDAT'):
            HostContext.I1EDDT = TradeContext.ENDDAT
        else:
            HostContext.I1EDDT = '' 
        return True

    if (TradeContext.HostCode == '8826'):
        #��������
        if TradeContext.existVariable('NBBH'):
            HostContext.I1NBBH = TradeContext.NBBH  #�����ʶ
        else:
            HostContext.I1NBBH = ''	            #�����ʶ

        if TradeContext.existVariable('COUT'):
            HostContext.I1COUT = TradeContext.COUT  #�ܱ���
        else:
            HostContext.I1COUT = ''	            #�ܱ���

        if TradeContext.existVariable('TOAM'):
            HostContext.I1TOAM = TradeContext.TOAM  #�ܽ��
        else:
            HostContext.I1TOAM = ''	            #�ܽ��

        if TradeContext.existVariable('FINA'):
            HostContext.I1FINA = TradeContext.FINA  #�ϴ��ļ�����
        else:
            HostContext.I1FINA = ''	            #�ϴ��ļ�����

        return True
    
    #=====������ 20081128 ���������������嵥�ļ��ϴ�====
    if (TradeContext.HostCode == '8823'):
        #����������
        if TradeContext.existVariable('CONT'):
            HostContext.I1COUT = TradeContext.CONT  #�ܱ���
        else:
            HostContext.I1COUT = ''	                #�ܽ��

        if TradeContext.existVariable('OCCAMT'):
            HostContext.I1TOAM = TradeContext.OCCAMT  #�ܽ��
        else:
            HostContext.I1TOAM = ''	                  #�ܽ��

        if TradeContext.existVariable('fileName'):
            HostContext.I1FINA = TradeContext.fileName  #�ϴ��ļ�����
        else:
            HostContext.I1FINA = ''	                    #�ϴ��ļ�����

        return True
    
    #����̩ 20110520 �������ڴ��ʿ��ƺͽ�ؽ���====
    if (TradeContext.HostCode == '0061'):
        #���ʿ��ƽ�ر�ʶλ����
        if TradeContext.existVariable('kjflag'):
            HostContext.I1CLFG = TradeContext.kjflag  #���ƽ�ر�ʶλ
        else:
            HostContext.I1CLFG = ''	
        AfaLoggerFunc.tradeInfo(">>>>>>"+"test1")
        if TradeContext.existVariable('ACCNO'):               #�����ƻ��ص��˺�  
            AfaLoggerFunc.tradeInfo(">>>>>>"+"test2")
            AfaLoggerFunc.tradeInfo(">>>>>>"+"test((((("+TradeContext.ACCNO)
            AfaLoggerFunc.tradeInfo(len(TradeContext.ACCNO.strip()))
            AfaLoggerFunc.tradeInfo((TradeContext.ACCNO)[0:1])
            AfaLoggerFunc.tradeInfo(">>>>>>"+"test3")
            if (len(TradeContext.ACCNO.strip())==19 and ((TradeContext.ACCNO)[0:1]=='6')): #��
                
                HostContext.I1CCTY ='1'                          #�ͻ���� ��˽
                HostContext.I1CARD = (TradeContext.ACCNO)[6:18]       #����
            else:
                AfaLoggerFunc.tradeInfo(">>>>>>"+"test4")
                HostContext.I1CARD = ''                          #����
            
            if (len(TradeContext.ACCNO.strip())==19 and (TradeContext.ACCNO)[0:1]!='6'):  #���˺�
                HostContext.I1CCTY ='1'                                                 #�ͻ���� ��˽ ���˺�ȫ�Ƕ�˽
                HostContext.I1OLAC =TradeContext.ACCNO                               #���˺�
            else:
                HostContext.I1OLAC =''      
           
            if (len(TradeContext.ACCNO.strip())==23 and (TradeContext.ACCNO)[0:1]=='1'): #��˽�˺�
                HostContext.I1CCTY ='1'                                                #�ͻ����   1��˽ 2�Թ�
                HostContext.I1SVAC = TradeContext.ACCNO                             #��˽�˺�
            else:
                HostContext.I1SVAC = ''     
            
            if (len(TradeContext.ACCNO.strip())==23 and (TradeContext.ACCNO)[0:1]=='2'): #�Թ��˺�
                HostContext.I1CCTY ='2'                                                #�ͻ����   1��˽ 2�Թ�
                HostContext.I1ACCN = TradeContext.ACCNO                             #�ͻ��˺�
            else:
                HostContext.I1ACCN =''
        HostContext.I1CYNO = '01'                      #����
        HostContext.I1SBSQ = ''                        #˳���
         
        if TradeContext.existVariable('ERRCONBAL'):    #���ƽ��
            HostContext.I1NGAM = TradeContext.ERRCONBAL 
        else:
            HostContext.I1NGAM= '' 
        HostContext.I1YSQM = ''                        #Ԥ��Ȩ��
        
        return True    

#====================���������ݽ���=============================
def CommHost( result = '' ):

    AfaLoggerFunc.tradeInfo('>>>����ͨѶ����[CommHost]')

    #�����������ױ�־TradeContext.BRSFLG�жϾ���ѡ���ĸ�map�ļ��������ӿڷ�ʽ
    #===================��ʼ��=======================
    if not InitHostReq(result) :
        TradeContext.__status__='1'
        return False
    if (result == '8813'):
        AfaLoggerFunc.tradeInfo('>>>���ʼ���')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8813.map'

    elif (result == '8820' ):
        AfaLoggerFunc.tradeInfo('>>>����Ĩ��')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8820.map'
        TradeContext.HostCode = '8820'

    elif (result == '8810'):
        AfaLoggerFunc.tradeInfo('>>>��ѯ�ʻ���Ϣ')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8810.map'
        TradeContext.HostCode = '8810'

        #�ر�� 20081105 ��8810��������ӿڳ�ʼ�������InitGLHostReq�����ƶ���InitHostReq������
        #InitGLHostReq()

    elif (result == '8811'):
        AfaLoggerFunc.tradeInfo('>>>��ѯƾ֤��Ϣ')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8811.map'
        TradeContext.HostCode = '8811'
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
    
    #=====������ 20081129 ������ѯ����������Ϣ====
    elif (result == '8816'):
        AfaLoggerFunc.tradeInfo('>>>��ѯ����������Ϣ')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8816.map'
        TradeContext.HostCode = '8816'
        InitGLHostReq()

    #=====������ 20081129 ������ѯ����������Ϣ====
    elif (result == '8825'):
        AfaLoggerFunc.tradeInfo('>>>��ѯ����������Ϣ')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8825.map'
        TradeContext.HostCode = '8825'
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

    elif (result == '8826'):
        AfaLoggerFunc.tradeInfo('>>>��������')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8826.map'
        TradeContext.HostCode = '8826'
        InitGLHostReq()
        
    #�ر�� 20081215  ����0652У��ŵ���Ϣ�ӿ�
    elif (result == '0652' ):
        AfaLoggerFunc.tradeInfo('>>>У��ŵ���Ϣ')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH0652.map'
        TradeContext.HostCode = '0652'
        
    #=====������ 20081128 ����8823����ũ���������ѽӿ�====
    elif (result == '8823'):
        AfaLoggerFunc.tradeInfo('>>>�������嵥�ļ��ϴ�')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8823.map'
        TradeContext.HostCode = '8823'
        InitGLHostReq()
    
    #����̩20110520 ����0061 ���ʿ��ƽ�ؽ���
    elif (result == '0061'):
        AfaLoggerFunc.tradeInfo('>>>���ʿ��ƽ��')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH0061.map'
        TradeContext.HostCode = '0061'
        InitGLHostReq()
    else:
        TradeContext.errorCode = 'A9999'
        TradeContext.errorMsg  = '�����������'
        return False
    
    #�˴����״���Ҫ��10λ,�Ҳ��ո�
    HostComm.callHostTrade( mapfile, UtilTools.Rfill(TradeContext.HostCode,10,' ') ,'0002' )
    
    AfaLoggerFunc.tradeInfo( 'host_Error:'+str( HostContext.host_ErrorType )+':'+HostContext.host_ErrorMsg )
    if HostContext.host_Error:
        AfaLoggerFunc.tradeFatal( 'host_Error:'+str( HostContext.host_ErrorType )+':'+HostContext.host_ErrorMsg )
        AfaLoggerFunc.tradeInfo('5')

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
    AfaLoggerFunc.tradeInfo(HostContext.O1MGID)
    if (HostContext.host_Error == True):    #����ͨѶ����
        AfaLoggerFunc.tradeInfo('4')
        TradeContext.__status__='2'
        TradeContext.errorCode, TradeContext.errorMsg = 'A9998', '����ͨѶ����'
        TradeContext.MGID  = HostContext.host_ErrorType    #ͨѶ�������
        return False
    
    if( HostContext.O1MGID == 'AAAAAAA' ): #�ɹ�
        TradeContext.__status__='0'
        TradeContext.errorCode, TradeContext.errorMsg = '0000', '�����ɹ�'
        TradeContext.MGID  = HostContext.O1MGID  #�������ش���

        #=====���ݽ����벻ͬѡ��ͬ����Ϣ����====
        if TradeContext.HostCode == '8813':
            TradeContext.TRDT   = HostContext.O1TRDT  #��������
            TradeContext.TLSQ   = HostContext.O1TLSQ  #������ˮ��
            TradeContext.DASQ   = str(HostContext.O2DASQ[0])   #���������
            AfaLoggerFunc.tradeInfo('�������[' + TradeContext.DASQ +']')
        elif TradeContext.HostCode == '8820':
            TradeContext.TRDT   = HostContext.O1TRDT  #��������
            TradeContext.TLSQ   = HostContext.O1TLSQ  #������ˮ��
        elif TradeContext.HostCode == '8810':
            TradeContext.ACCNM  = UtilTools.trim(HostContext.O1CUNM)  #�˺�����
            TradeContext.ACCSO  = HostContext.O1OPNT  #��������
            TradeContext.ACCST  = HostContext.O1ACST  #�˻�״̬
            TradeContext.ACCCD  = HostContext.O1ITCD  #ҵ�����
            TradeContext.ACCEM  = HostContext.O1ITEM  #��Ŀ����
            TradeContext.ACITY  = HostContext.O1IDTY  #֤������
            TradeContext.ACINO  = HostContext.O1IDNO  #֤������
        elif TradeContext.HostCode == '8811':
            TradeContext.HPAYTYP = HostContext.O1WDTP
            TradeContext.ACCSTCD = HostContext.O1STCD #ƾ֤״̬
            AfaLoggerFunc.tradeDebug('>>>��ѯƾ֤��Ϣ���')
        #===========�ر�� 20080725 ����8820�ӿڷ�����Ϣ����===================
        elif TradeContext.HostCode == '8820':
            TradeContext.TRDT   = HostContext.O1TRDT  #��������
            TradeContext.TLSQ   = HostContext.O1TLSQ  #������ˮ��
        else:
            AfaLoggerFunc.tradeDebug('>>>�����������')

        AfaLoggerFunc.tradeDebug('>>>�����ɹ�����')
        return True

    else:                                  #ʧ��
        TradeContext.__status__='1'
        AfaLoggerFunc.tradeInfo('8')

        TradeContext.errorCode, TradeContext.errorMsg = HostContext.O1MGID, HostContext.O1INFO
        return False
##############################################################################################
#
#  �������ƣ� CrtAcc
#  ��ڲ����� accno  lenacc
#  ���ڲ����� accno  False
#  ��    �ߣ� ������
#  ��    �ڣ� 20080610
#  �����ܣ� �����˺�У��λ
#
##############################################################################################
def CrtAcc( no, lenacc ):
    AfaLoggerFunc.tradeInfo( '>>>��ʼ�����˺�У��λ' )
    #=====�жϴ���Ĳ��������Ƿ���ȷ====
    if len(no) != 24:
        return AfaFlowControl.ExitThisFlow('M999','�˺ų��Ȳ���ȷ')
    if int(lenacc) != 25:
        return AfaFlowControl.ExitThisFlow('M999','���볤�Ȳ���ȷ')

    #====��ʼУ���˺�====
    total = 10
    for i in range(0, lenacc-1):
        if( not no[i].isdigit() ):
            return AfaFlowControl.ExitThisFlow('M999', '�˺ű���Ϊ����')
        total = (total + int(no[i]) -0)%10
        if total == 0:
            total = 10
        else:
            total = total
        total =  (total + total)%11
    no = no + str((11 - total)%10)
    AfaLoggerFunc.tradeInfo( '�˺ţ�' + no )
    AfaLoggerFunc.tradeInfo( '>>>���������˺�У��λ' )
    return str(no)
