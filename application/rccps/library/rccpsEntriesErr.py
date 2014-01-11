# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ.��Ʒ�¼��ֵģ��
#===============================================================================
#   �����ļ�:   rccpsEntriesErr.py
#   ��    ��:   �˹�ͨ
#   �޸�ʱ��:   2008-11-30
################################################################################

import AfaLoggerFunc,AfaDBFunc,TradeContext, LoggerHandler, sys, os, time, AfaUtilTools, ConfigParser,AfaFlowControl
from types import *
from rccpsConst import *
import rccpsHostFunc

##�����ֽ�ͨ�����˼��˻�Ʒ�¼��ֵ
def KZTCWZJZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>��ʼ�����ֽ�ͨ�����˼��˻�Ʒ�¼��ֵ")
        
    if not input_dict.has_key('CHRGTYP'):
        return AfaFLowControl.ExitThisFlow("S999","��������ȡ��ʽ����Ϊ��")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","���׽���Ϊ��")
        
    if not input_dict.has_key('CUSCHRG'):
        return AfaFlowControl.ExitThisFlow("S999","�����Ѳ���Ϊ��")
        
    
    TradeContext.HostCode = '8813' 
       
    TradeContext.PKFG = 'E'                                             #ͨ��ͨ�ұ�ʶ
#    TradeContext.CATR = '0'                                             #��ת��ʶ:0-�ֽ�
    TradeContext.RCCSMCD  = PL_RCCSMCD_DZBJ                          #����ժҪ��:�ֽ�ͨ������
    TradeContext.OCCAMT = str(input_dict['OCCAMT'])
    TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_QTYSK             #�跽�˺�
    TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25) 
    TradeContext.ACNM = '����Ӧ�տ�'
    TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSWZ           #�����˺�
    TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
    TradeContext.OTNM = "ũ��������������"
    TradeContext.CTFG = '7'                                             #���������ѱ�ʾ
    
    AfaLoggerFunc.tradeInfo("�跽�˺�1:[" + TradeContext.SBAC + "]")
    AfaLoggerFunc.tradeInfo("�����˺�1:[" + TradeContext.RBAC + "]")
    
    if input_dict['CHRGTYP'] == '0':
        #�ֽ���ȡ������
        TradeContext.ACUR = '2'                                         #�ظ����� 
        
        TradeContext.I2PKFG = 'E'                                       #ͨ��ͨ�ұ�ʶ
#        TradeContext.I2CATR = '0'                                       #��ת��ʶ:0-�ֽ�
        TradeContext.I2TRAM = str(input_dict['CUSCHRG'])                #�����ѽ��
        TradeContext.I2SMCD = PL_RCCSMCD_DZBJ                            #����ժҪ��:������
        TradeContext.I2SBAC = TradeContext.BESBNO + PL_ACC_QTYSK        #�跽�˺�
        TradeContext.I2SBAC = rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM = '����Ӧ�տ�'
        TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_TCTDSXF      #�����˺�:ͨ��ͨ��������
        TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM = "ũ����������"
        TradeContext.I2CTFG = '8'                                       #���������ѱ�ʾ 
    elif input_dict['CHRGTYP'] == '1':
        #�ֽ�ͨ���޷���ȡ�����˻�������
        return AfaFlowControl.ExitThisFlow("S999","�ֽ�ͨ���޷�ת����ȡ������")
    elif input_dict['CHRGTYP'] == '2':
        AfaLoggerFunc.tradeInfo(">>>����������")
    else:
        return AfaFlowControl.ExitThisFlow("S999","�Ƿ���������ȡ��ʽ")
        
    if TradeContext.existVariable("I2SBAC") and TradeContext.existVariable('I2RBAC'):
        AfaLoggerFunc.tradeInfo("�跽�˺�2:[" + TradeContext.I2SBAC + "]")
        AfaLoggerFunc.tradeInfo("�����˺�2:[" + TradeContext.I2RBAC + "]")
        
    AfaLoggerFunc.tradeInfo(">>>���������ֽ�ͨ�����˼��˻�Ʒ�¼��ֵ")
    return True
    
#�����ֽ�ͨ������Ĩ�˻�Ʒ�¼��ֵ
def KZTCWZMZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>��ʼ�����ֽ�ͨ������Ĩ�˻�Ʒ�¼��ֵ")
        
    if not input_dict.has_key('CHRGTYP'):
        return AfaFLowControl.ExitThisFlow("S999","��������ȡ��ʽ����Ϊ��")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","���׽���Ϊ��")
        
    if not input_dict.has_key('CUSCHRG'):
        return AfaFlowControl.ExitThisFlow("S999","�����Ѳ���Ϊ��")
        
    if not input_dict.has_key('RCCSMCD'):
        return AfaFlowControl.ExitThisFlow("S999","ժҪ���벻��Ϊ��")
        
    TradeContext.HostCode='8813'
    if input_dict['CHRGTYP'] == '0':                          #����  
        TradeContext.ACUR = '2'                                         #�ظ����� 
        #=====����====
        TradeContext.PKFG = 'T'                                         #ͨ��ͨ�ұ�ʶ
        TradeContext.RVFG = '2'                                         #�����ֱ�ʾ        
        TradeContext.OCCAMT = str(input_dict['OCCAMT'])           #���׽��
        TradeContext.RCCSMCD = PL_RCCSMCD_DZMZ                    #����ժҪ��
        TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_QTYFK
        TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM = '����Ӧ����'
        TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSWZ       #�����˺�
        TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM = "ũ��������������"
        TradeContext.CTFG = '7'                                         #���������ѱ�ʾ
        AfaLoggerFunc.tradeInfo("�跽�˺�1:[" + TradeContext.SBAC + "]")
        AfaLoggerFunc.tradeInfo("�����˺�1:[" + TradeContext.RBAC + "]")
        #=====������====
        TradeContext.I2PKFG = 'T'                                         #ͨ��ͨ�ұ�ʶ
        TradeContext.I2RVFG = '2'                                         #�����ֱ�ʾ
        TradeContext.I2TRAM = str(input_dict['CUSCHRG'])                  #������
        TradeContext.I2SMCD = PL_RCCSMCD_DZMZ    
        TradeContext.I2SBAC = TradeContext.BESBNO + PL_ACC_QTYFK
        TradeContext.I2SBAC = rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM = '����Ӧ����'
        TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_TCTDSXF
        TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM = "������"
        TradeContext.I2CTFG = '8'                                         #���������ѱ�ʾ
        AfaLoggerFunc.tradeInfo("�跽�˺�2:[" + TradeContext.I2SBAC + "]")
        AfaLoggerFunc.tradeInfo("�����˺�2:[" + TradeContext.I2RBAC + "]")
        
    elif input_dict['CHRGTYP'] == '2':                           #����
        #=====����====
        TradeContext.PKFG = 'T'                                         #ͨ��ͨ�ұ�ʶ
        TradeContext.RVFG = '2'                                         #�����ֱ�ʾ        
        TradeContext.OCCAMT = str(input_dict['OCCAMT'])           #���׽��
        TradeContext.RCCSMCD = PL_RCCSMCD_DZMZ                    #����ժҪ��
        TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_QTYFK
        TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM = '����Ӧ����'
        TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSWZ       #�����˺�
        TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM = "ũ��������������"
        TradeContext.CTFG = '7'                                         #���������ѱ�ʾ
        AfaLoggerFunc.tradeInfo("�跽�˺�1:[" + TradeContext.SBAC + "]")
        AfaLoggerFunc.tradeInfo("�����˺�1:[" + TradeContext.RBAC + "]")
        
    AfaLoggerFunc.tradeInfo(">>>���������ֽ�ͨ������Ĩ�˻�Ʒ�¼��ֵ")
    return True
        
#���۱�ת�����˼��˻�Ʒ�¼��ֵ
def KZBZYWZJZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>��ʼ���۱�ת�����˼��˻�Ʒ�¼��ֵ")
    
    if not input_dict.has_key('CHRGTYP'):
        return AfaFLowControl.ExitThisFlow("S999","��������ȡ��ʽ����Ϊ��")
        
    if not input_dict.has_key('PYRACC'):
        return AfaFlowControl.ExitThisFlow("S999","�������˺Ų���Ϊ��")
        
    if not input_dict.has_key('PYRNAM'):
        return AfaFlowControl.ExitThisFlow("S999","�����˻�������Ϊ��")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","���׽���Ϊ��")
        
    if not input_dict.has_key('CUSCHRG'):
        return AfaFlowControl.ExitThisFlow("S999","�����Ѳ���Ϊ��")
    
    TradeContext.HostCode = '8813' 
      
    TradeContext.PKFG = 'E'                                         #ͨ��ͨ�ұ�ʶ
    
    TradeContext.OCCAMT = str(input_dict['OCCAMT'])                 #��Ʊ���
    TradeContext.RCCSMCD  = PL_RCCSMCD_DZBJ                        #����ժҪ��:��ת������
    TradeContext.SBAC = input_dict['PYRACC']                        #�跽�˺�:�ͻ���
    TradeContext.ACNM = input_dict['PYRNAM']                        #�跽����
    TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSWZ       #�����˺�:������
    TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
    TradeContext.OTNM = "ũ��������������"
    if TradeContext.existVariable('PASSWD'):
        TradeContext.PASSWD = TradeContext.PASSWD                       #����������
    else:
        AfaLoggerFunc.tradeInfo("======��У���������======")
        
    if input_dict.has_key('WARNTNO'):
        TradeContext.WARNTNO = input_dict['WARNTNO']
    else:
        AfaLoggerFunc.tradeInfo("======��У��ƾ֤����======")
    
    if input_dict.has_key('CERTTYPE') and input_dict.has_key('CERTNO'):
        TradeContext.CERTTYPE = TradeContext.CERTTYPE                   #֤������
        TradeContext.CERTNO   = TradeContext.CERTNO                     #֤������
    else:
        AfaLoggerFunc.tradeInfo("======��У��֤������======")
        
    TradeContext.CTFG = '7'                                             #������ѧ�ѱ�ʾ
    
    AfaLoggerFunc.tradeInfo("�跽�˺�1:[" + TradeContext.SBAC + "]")
    AfaLoggerFunc.tradeInfo("�����˺�1:[" + TradeContext.RBAC + "]")
    
    if TradeContext.CHRGTYP == '0':
        #�ֽ���ȡ
        AfaLoggerFunc.tradeInfo(">>>�ֽ���ȡ������")
        TradeContext.ACUR = '2'                                         #�ظ�����
        
        TradeContext.I2PKFG = 'E'                                       #ͨ��ͨ�ұ�ʶ
#        TradeContext.I2CATR = '0'                                       #��ת��ʶ:0-�ֽ�
        TradeContext.I2TRAM = str(input_dict['CUSCHRG'])                #�����ѽ��
        TradeContext.I2SMCD = PL_RCCSMCD_DZBJ                            #����ժҪ��:������
        TradeContext.I2SBAC = TradeContext.BESBNO + PL_ACC_QTYSK        #�跽�˺�
        TradeContext.I2SBAC = rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM = "����Ӧ�տ�"                                        
        TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_TCTDSXF      #�����˺�:ͨ��ͨ��������
        TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM = "������"
        TradeContext.I2CTFG = '8'                                       #���������ѱ�ʾ
        
    elif TradeContext.CHRGTYP == '1':
        #�����˻���ȡ
        AfaLoggerFunc.tradeInfo(">>>�����˻���ȡ������")
        TradeContext.ACUR = '2'                                         #�ظ�����
        
        TradeContext.I2PKFG = 'E'                                       #ͨ��ͨ�ұ�ʶ
        TradeContext.I2TRAM = str(input_dict['CUSCHRG'])                #�����ѽ��
        TradeContext.I2SMCD = PL_RCCSMCD_DZBJ                            #����ժҪ��:������
        TradeContext.I2SBAC = input_dict['PYRACC']                      #�跽�˺�:�ͻ���
        TradeContext.I2ACNM = input_dict['PYRNAM']
        TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_TCTDSXF      #�����˺�:ͨ��ͨ��������
        TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM = "������"
        if input_dict.has_key('PASSWD'):
            TradeContext.I2PSWD = input_dict['PASSWD']                  #����������
        else:
            AfaLoggerFunc.tradeInfo("======��У���������======")
            
        if input_dict.has_key('WARNTNO'):
            TradeContext.I2WARNTNO = input_dict['WARNTNO']
        else:
            AfaLoggerFunc.tradeInfo("======��У��ƾ֤����======")
        
        if input_dict.has_key('CERTTYPE') and input_dict.has_key('CERTNO'):
            TradeContext.I2CERTTYPE = input_dict['CERTTYPE']            #֤������
            TradeContext.I2CERTNO   = input_dict['CERTNO']              #֤������
        else:
            AfaLoggerFunc.tradeInfo("======��У��֤������======")
        TradeContext.I2CTFG = '8'                                       #���������ѱ�ʾ     
    else:
        AfaLoggerFunc.tradeInfo(">>>����������")
    
    if TradeContext.existVariable("I2SBAC") and TradeContext.existVariable('I2RBAC'):
        AfaLoggerFunc.tradeInfo("�跽�˺�2:[" + TradeContext.I2SBAC + "]")
        AfaLoggerFunc.tradeInfo("�����˺�2:[" + TradeContext.I2RBAC + "]")
    
    AfaLoggerFunc.tradeInfo(">>>�������۱�ת�����˼��˻�Ʒ�¼��ֵ")
    return True
    
#���۱�ת������Ĩ�˻�Ʒ�¼��ֵ
def KZBZYWZMZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>��ʼ���۱�ת������Ĩ�˻�Ʒ�¼��ֵ")
    
    if not input_dict.has_key('CHRGTYP'):
        return AfaFLowControl.ExitThisFlow("S999","��������ȡ��ʽ����Ϊ��")
        
    if not input_dict.has_key('PYRACC'):
        return AfaFlowControl.ExitThisFlow("S999","�������˺Ų���Ϊ��")
        
    if not input_dict.has_key('PYRNAM'):
        return AfaFlowControl.ExitThisFlow("S999","�����˻�������Ϊ��")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","���׽���Ϊ��")
        
    if not input_dict.has_key('CUSCHRG'):
        return AfaFlowControl.ExitThisFlow("S999","�����Ѳ���Ϊ��")
    
    if not input_dict.has_key('RCCSMCD'):
        return AfaFlowControl.ExitThisFlow("S999","ժҪ���벻��Ϊ��")
    
    #�ֽ���ȡ
    AfaLoggerFunc.tradeInfo(">>>�ֽ���ȡ������")
    
    TradeContext.HostCode = '8813' 
    if input_dict['CHRGTYP'] == '1':    #ת��
        TradeContext.ACUR = '2'                                         #�ظ�����
        #=====����====
        TradeContext.PKFG = 'T'                                         #ͨ��ͨ�ұ�ʶ
        TradeContext.OCCAMT = "-" + str(input_dict['OCCAMT'])           #���׽��
        TradeContext.RCCSMCD = PL_RCCSMCD_DZMZ                    #����ժҪ��:��ת������
        TradeContext.SBAC = input_dict['PYRACC']                        #�跽�˺�:�ͻ���
        TradeContext.ACNM = input_dict['PYRNAM']                        #�跽����
        TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSWZ       #�����˺�
        TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM = "ũ��������������"
        if input_dict.has_key('PASSWD'):
            TradeContext.PASSWD = input_dict['PASSWD']                  #����������
        else:
            AfaLoggerFunc.tradeInfo("======��У���������======")
            
        if input_dict.has_key('WARNTNO'):
            TradeContext.WARNTNO = input_dict['WARNTNO']
        else:
            AfaLoggerFunc.tradeInfo("======��У��ƾ֤����======")
        
        if input_dict.has_key('CERTTYPE') and input_dict.has_key('CERTNO'):
            TradeContext.CERTTYPE = input_dict['CERTTYPE']              #֤������
            TradeContext.CERTNO   = input_dict['CERTNO']                #֤������
        else:
            AfaLoggerFunc.tradeInfo("======��У��֤������======")
        TradeContext.CTFG = '7'                                         #���������ѷ�ʽ
        AfaLoggerFunc.tradeInfo("�跽�˺�1:[" + TradeContext.SBAC + "]")
        AfaLoggerFunc.tradeInfo("�����˺�1:[" + TradeContext.RBAC + "]")
        #=====������====
        TradeContext.I2PKFG = 'T'                                       #ͨ��ͨ�ұ�ʶ
        TradeContext.I2TRAM = "-" + str(input_dict['CUSCHRG'])          #������
        TradeContext.I2SMCD = PL_RCCSMCD_DZMZ                     #����ժҪ��
        TradeContext.I2SBAC = input_dict['PYRACC']                        #�跽�˺�
        TradeContext.I2ACNM = input_dict['PYRNAM']                        #�跽����
        TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_TCTDSXF        #�����˺�
        TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM = "������"
        TradeContext.I2CTFG = '8'                                         #���������ѷ�ʽ
        AfaLoggerFunc.tradeInfo("�跽�˺�2:[" + TradeContext.I2SBAC + "]")
        AfaLoggerFunc.tradeInfo("�����˺�2:[" + TradeContext.I2RBAC + "]")
        
    elif input_dict['CHRGTYP'] == '0':    #����
        TradeContext.ACUR = '2'                                         #�ظ�����
        #=====����====
        TradeContext.PKFG = 'T'                                         #ͨ��ͨ�ұ�ʶ
        TradeContext.OCCAMT = "-" + str(input_dict['OCCAMT'])           #���׽��
        TradeContext.RCCSMCD = PL_RCCSMCD_DZMZ                    #����ժҪ��:��ת������
        TradeContext.SBAC = input_dict['PYRACC']                        #�跽�˺�:�ͻ���
        TradeContext.ACNM = input_dict['PYRNAM']                        #�跽����
        TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSWZ       #�����˺�:������
        TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM = "ũ��������������"
        TradeContext.CTFG = '7'                                         #���������ѷ�ʽ
        AfaLoggerFunc.tradeInfo("�跽�˺�1:[" + TradeContext.SBAC + "]")
        AfaLoggerFunc.tradeInfo("�����˺�1:[" + TradeContext.RBAC + "]")
        #=====������====
        TradeContext.I2PKFG = 'T'                                       #ͨ��ͨ�ұ�ʶ
        TradeContext.I2RVFG = '2'                                   #�����ֱ�ʾ
        TradeContext.I2TRAM = str(input_dict['CUSCHRG'])          #������
        TradeContext.I2SMCD = PL_RCCSMCD_DZMZ                     #����ժҪ��
        TradeContext.I2SBAC = TradeContext.BESBNO + PL_ACC_QTYFK       #�跽�˺�
        TradeContext.I2SBAC = rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM = "����Ӧ����"                       #�跽����
        TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_TCTDSXF
        TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM = "������"
        TradeContext.I2CTFG = '8'                                         #���������ѷ�ʽ
        AfaLoggerFunc.tradeInfo("�跽�˺�2:[" + TradeContext.I2SBAC + "]")
        AfaLoggerFunc.tradeInfo("�����˺�2:[" + TradeContext.I2RBAC + "]")
        
    else:                            #����                  
        #=====����====
        TradeContext.PKFG = 'T'                                         #ͨ��ͨ�ұ�ʶ
        TradeContext.OCCAMT = "-" + str(input_dict['OCCAMT'])           #���׽��
        TradeContext.RCCSMCD = PL_RCCSMCD_DZMZ                    #����ժҪ��:��ת������
        TradeContext.SBAC = input_dict['PYRACC']                        #�跽�˺�:�ͻ���
        TradeContext.ACNM = input_dict['PYRNAM']                        #�跽����
        TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSWZ       #�����˺�:������
        TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM = "ũ��������������"
        TradeContext.CTFG = '7'                                         #���������ѷ�ʽ
        AfaLoggerFunc.tradeInfo("�跽�˺�1:[" + TradeContext.SBAC + "]")
        AfaLoggerFunc.tradeInfo("�����˺�1:[" + TradeContext.RBAC + "]")
    
    
    AfaLoggerFunc.tradeInfo(">>>�������۱�ת������Ĩ�˻�Ʒ�¼��ֵ")
    return True
    
#�����ֽ�ͨ�����˼��˻�Ʒ�¼��ֵ
def KZTDWZJZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>��ʼ�����ֽ�ͨ�����˼��˻�Ʒ�¼��ֵ")
    
    if not input_dict.has_key('CHRGTYP'):
        return AfaFLowControl.ExitThisFlow("S999","��������ȡ��ʽ����Ϊ��")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","���׽���Ϊ��")
        
    if not input_dict.has_key('CUSCHRG'):
        return AfaFlowControl.ExitThisFlow("S999","�����Ѳ���Ϊ��")
    
    TradeContext.HostCode = '8813' 
    
    if input_dict['CHRGTYP'] == '1':
        #=====ת��====
        TradeContext.ACUR    =  '3'                                     #���˴���
        #=========���׽��+������===================
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZBJ                                 #ժҪ���� 
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  'ũ��������'                                  #�跽����
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  'ũ����������ʱ��'                            #��������
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #������
        TradeContext.PKFG    = 'E'                                            #ͨ��ͨ�ұ�ʾ
        TradeContext.CTFG    = '9'                                            #������ѧ�ѱ�ʾ
        TradeContext.CATR    = '1'
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�跽�˺�' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�����˺�' + TradeContext.RBAC )
        #=========���׽��============
        TradeContext.I2SMCD  =  PL_RCCSMCD_DZBJ                                 #ժҪ����
        TradeContext.I2SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�跽�˺�
        TradeContext.I2SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM  =  'ũ����������ʱ��'                                    #�跽����
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_QTYFK            #�����˺�
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  '����Ӧ����'                                            #��������
        TradeContext.I2TRAM  =  str(input_dict['OCCAMT'])                       #������
        TradeContext.I2CTFG  = '7'
        TradeContext.I2PKFG  = 'E'
        TradeContext.I2CATR    = '1'
        #TradeContext.I2WARNTNO = ''
        #TradeContext.I2CERTTYPE = ''
        #TradeContext.I2CERTNO = ''
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�跽�˺�' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�����˺�' + TradeContext.I2RBAC )
        #=========�������������뻧===========
        TradeContext.I3SMCD  =  PL_RCCSMCD_DZBJ                                 #ժҪ����
        TradeContext.I3SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�跽�˺�
        TradeContext.I3SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
        TradeContext.I3ACNM  =  'Ӧ����'                                    #�跽����
        TradeContext.I3RBAC  =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #�����˺�
        TradeContext.I3RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
        TradeContext.I3OTNM  =  '����������'                                  #��������
        TradeContext.I3TRAM  =  str(input_dict['CUSCHRG'])                    #������
        TradeContext.I3CTFG  = '8'
        TradeContext.I3PKFG  = 'E'
        TradeContext.I3CATR    = '1'
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�跽�˺�' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�����˺�' + TradeContext.I3RBAC )
    
    elif input_dict['CHRGTYP'] == '0':                                          #�ֽ�
        #=====����====
        TradeContext.ACUR    =  '2'                                           #���˴���
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZBJ                                 #ժҪ����
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  'ũ��������'                                  #�跽����
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_QTYFK            #�����˺�
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '����Ӧ����'                                  #��������
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #���
        TradeContext.CTFG    = '7'
        TradeContext.PKFG    = 'E'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO  = ''
        TradeContext.CATR    =  '1'                                             #��ת��־
        
        #=====�����Ѽ��˸�ֵ====
        TradeContext.I2SMCD  =  PL_RCCSMCD_DZBJ                                 #ժҪ����
        TradeContext.I2SBAC  =  TradeContext.BESBNO + PL_ACC_QTYSK            #�跽�˺�
        TradeContext.I2SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM  =  '����Ӧ�տ�'    
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #�����˺�
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  '�����ѿ�Ŀ'                                  #��������
        TradeContext.I2TRAM  =  str(input_dict['CUSCHRG'])                    #���
        TradeContext.I2CTFG  =  '8'
        TradeContext.I2PKFG  =  'E'
        TradeContext.I2CATR  =  '1'                                           #��ת��־
    elif input_dict['CHRGTYP'] == '2':
        #=====���շ�====
        TradeContext.ACUR    =  '1'                                           #���˴���
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZBJ                             #ժҪ����
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  'ũ��������'           
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_QTYFK            #�����˺�
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '����Ӧ����'                                            #��������
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #���
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    =  'E'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO  = ''
        TradeContext.CATR    =  '1'                                             #��ת��־
    else:
        return AfaFlowControl.ExitThisFlow("ԭ������������ȡ��ʽ�Ƿ�")
            
    AfaLoggerFunc.tradeInfo(">>>���������ֽ�ͨ�����˼��˻�Ʒ�¼��ֵ")
    return True
    
#�����ֽ�ͨ������Ĩ�˻�Ʒ�¼��ֵ
def KZTDWZMZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>��ʼ�����ֽ�ͨ������Ĩ�˻�Ʒ�¼��ֵ")
    
    if not input_dict.has_key('CHRGTYP'):
        return AfaFLowControl.ExitThisFlow("S999","��������ȡ��ʽ����Ϊ��")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","���׽���Ϊ��")
        
    if not input_dict.has_key('CUSCHRG'):
        return AfaFlowControl.ExitThisFlow("S999","�����Ѳ���Ϊ��")
        
    if not input_dict.has_key('RCCSMCD'):
        return AfaFlowControl.ExitThisFlow("S999","ժҪ���벻��Ϊ��")
    
    TradeContext.HostCode = '8813'
    
    if input_dict['CHRGTYP'] == '1':
        #=====ת��====
        TradeContext.ACUR    =  '3'                                           #���˴���
        #=========�������������뻧===========
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZMZ                        #ժҪ����
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  'ũ����������ʱ��'                                    #�跽����
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #�����˺�
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '����������'                                  #��������
        TradeContext.OCCAMT  =  "-" + str(input_dict['CUSCHRG'])              #������
        TradeContext.CTFG    = '8'
        TradeContext.PKFG    = 'T'
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�跽�˺�' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�����˺�' + TradeContext.RBAC )
        #=========���׽��============
        TradeContext.I2SMCD  =  PL_RCCSMCD_DZMZ                       #ժҪ����
        TradeContext.I2RVFG    = '0' 
        TradeContext.I2SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�跽�˺�
        TradeContext.I2SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM  =  'ũ����������ʱ'                               #�跽����
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_QTYSK          #�����˺�
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  '����Ӧ�տ�'                          #��������
        TradeContext.I2TRAM  =  str(input_dict['OCCAMT'])               #������
        TradeContext.I2CTFG  = '7'
        TradeContext.I2PKFG  = 'T'
        #TradeContext.I2WARNTNO = ''
        #TradeContext.I2CERTTYPE = ''
        #TradeContext.I2CERTNO = ''
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�跽�˺�' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�����˺�' + TradeContext.I2RBAC )
        #=========���׽��+������===================
        TradeContext.I3SMCD  =  PL_RCCSMCD_DZMZ                         #ժҪ����
        TradeContext.I3SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
        TradeContext.I3SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
        TradeContext.I3ACNM  =  'ũ��������'                                  #�跽����
        TradeContext.I3RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
        TradeContext.I3RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
        TradeContext.I3OTNM  =  'ũ����������ʱ��'                                    #��������
        TradeContext.I3TRAM  =  "-" + str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #������
        TradeContext.I3PKFG  = 'T'
        TradeContext.I3CTFG  = '9'
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�跽�˺�' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�����˺�' + TradeContext.I3RBAC )
    
    elif input_dict['CHRGTYP'] == '0':                                        #�ֽ�
        TradeContext.ACUR    =  '2'                                           #���˴���
        #=====����====
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZMZ                         #ժҪ����
        TradeContext.RVFG    = '0' 
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  'ũ��������'                                  #�跽����
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_QTYSK          #�����˺�
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '����Ӧ�տ�'                          #��������
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])               #���
        TradeContext.CTFG    = '7'
        TradeContext.PKFG    = 'T'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO  = ''
        #=====������====
        TradeContext.I2SMCD    =  PL_RCCSMCD_DZMZ                         #ժҪ����
        TradeContext.I2RVFG    = '2' 
        TradeContext.I2SBAC    =  TradeContext.BESBNO + PL_ACC_QTYFK         #�跽�˺�
        TradeContext.I2SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM    =  '����Ӧ����'   
        TradeContext.I2RBAC    =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #�����˺�
        TradeContext.I2RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM    =  '������'                          #��������
        TradeContext.I2TRAM    =  str(input_dict['CUSCHRG'])               #���
        TradeContext.I2CTFG    = '8'
        TradeContext.I2PKFG    = 'T'
        
    elif input_dict['CHRGTYP'] == '2':
        #=====���շ�====
        TradeContext.ACUR    =  '1'                                           #���˴���
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZMZ                         #ժҪ����
        TradeContext.RVFG    = '0' 
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  'ũ��������'  
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_QTYSK          #�����˺�
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '����Ӧ�տ�'                          #��������
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])               #���
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    =  'T'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO  = ''
    else:
        return AfaFlowControl.ExitThisFlow("ԭ������������ȡ��ʽ�Ƿ�")    
        
    AfaLoggerFunc.tradeInfo(">>>���������ֽ�ͨ������Ĩ�˻�Ʒ�¼��ֵ")
    return True
    
#������ת�����˼��˻�Ʒ�¼��ֵ
def KZYZBWZJZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>��ʼ������ת�����˼��˻�Ʒ�¼��ֵ")
    
    if not input_dict.has_key('CHRGTYP'):
        return AfaFLowControl.ExitThisFlow("S999","��������ȡ��ʽ����Ϊ��")
        
    if not input_dict.has_key('PYEACC'):
        return AfaFlowControl.ExitThisFlow("S999","�տ����˺Ų���Ϊ��")
        
    if not input_dict.has_key('PYENAM'):
        return AfaFlowControl.ExitThisFlow("S999","�տ��˻�������Ϊ��")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","���׽���Ϊ��")
        
    if not input_dict.has_key('CUSCHRG'):
        return AfaFlowControl.ExitThisFlow("S999","�����Ѳ���Ϊ��")
    
    TradeContext.HostCode = '8813' 
    
    if input_dict['CHRGTYP'] == '1':
        #=====ת��====
        TradeContext.ACUR    =  '3'                                     #���˴���
        #=========���׽��+������===================
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZBJ                              #ժҪ����  PL_RCCSMCD_YZBWZ ��ת��
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  'ũ��������'                                  #�跽����
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS           #�����˺�
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  'Ӧ����'                                    #��������
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #������
        TradeContext.PKFG    = 'E'
        TradeContext.CTFG    = '9'
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�跽�˺�' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�����˺�' + TradeContext.RBAC )
        #=========���׽��============
        TradeContext.I2SMCD  =  PL_RCCSMCD_DZBJ                              #ժҪ����
        TradeContext.I2SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�跽�˺�
        TradeContext.I2SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM  =  'Ӧ����'                                    #�跽����
        TradeContext.I2RBAC  =  input_dict['PYEACC']                          #�����˺�
        TradeContext.I2OTNM  =  input_dict['PYENAM']                          #��������
        TradeContext.I2TRAM  =  str(input_dict['OCCAMT'])                     #������
        TradeContext.I2CTFG  = '7'
        TradeContext.I2PKFG  = 'E'
        TradeContext.I2WARNTNO = ''
        TradeContext.I2CERTTYPE = ''
        TradeContext.I2CERTNO = ''
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�跽�˺�' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�����˺�' + TradeContext.I2RBAC )
        #=========�������������뻧===========
        TradeContext.I3SMCD  =  PL_RCCSMCD_DZBJ                                #ժҪ����
        TradeContext.I3SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�跽�˺�
        TradeContext.I3SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
        TradeContext.I3ACNM  =  'Ӧ����'                                    #�跽����
        TradeContext.I3RBAC  =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #�����˺�
        TradeContext.I3RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
        TradeContext.I3OTNM  =  '����������'                                  #��������
        TradeContext.I3TRAM  =  str(input_dict['CUSCHRG'])                    #������
        TradeContext.I3CTFG  = '8'
        TradeContext.I3PKFG  = 'E'
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�跽�˺�' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�����˺�' + TradeContext.I3RBAC )

    elif input_dict['CHRGTYP'] == '0':
        #=====����====
        TradeContext.ACUR    =  '2'                                           #���˴���
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZBJ                              #ժҪ����
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
        TradeContext.SBAC    = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  'ũ��������'                                  #�跽����
        TradeContext.RBAC    =  input_dict['PYEACC']                          #�����˺�
        TradeContext.OTNM    =  input_dict['PYENAM']                          #��������
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #���
        TradeContext.CTFG  = '7'
        TradeContext.PKFG  = 'E'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
        
        #=====�����Ѽ��˸�ֵ====
        TradeContext.I2SMCD  =  PL_RCCSMCD_DZBJ                                #ժҪ����
        TradeContext.I2SBAC  =  TradeContext.BESBNO + PL_ACC_QTYSK            #�跽�˺�
        TradeContext.I2SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM  =  '����Ӧ�տ�'
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #�����˺�
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  '�����ѿ�Ŀ'                                  #��������
        TradeContext.I2TRAM  =  str(input_dict['CUSCHRG'])                    #���
        TradeContext.I2CTFG  =  '8'
        TradeContext.I2PKFG  =  'E'
#        TradeContext.I2CATR  =  '0'                                           #��ת��־
    elif input_dict['CHRGTYP'] == '2':
        #=====���շ�====
        TradeContext.ACUR    =  '1'                                           #���˴���
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZBJ                              #ժҪ����
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.RBAC    =  input_dict['PYEACC']                          #�����˺�
        TradeContext.OTNM    =  input_dict['PYENAM']                          #��������
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #���
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    =  'E'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
    else:
        return AfaFlowControl.ExitThisFlow('S999','�������շѷ�ʽ�Ƿ�') 
    
    AfaLoggerFunc.tradeInfo(">>>����������ת�����˼��˻�Ʒ�¼��ֵ")
    return True
    
#������ת������Ĩ�˻�Ʒ�¼��ֵ
def KZYZBWZMZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>��ʼ������ת������Ĩ�˻�Ʒ�¼��ֵ")
    
    if not input_dict.has_key('CHRGTYP'):
        return AfaFLowControl.ExitThisFlow("S999","��������ȡ��ʽ����Ϊ��")
        
    if not input_dict.has_key('PYEACC'):
        return AfaFlowControl.ExitThisFlow("S999","�տ����˺Ų���Ϊ��")
        
    if not input_dict.has_key('PYENAM'):
        return AfaFlowControl.ExitThisFlow("S999","�տ��˻�������Ϊ��")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","���׽���Ϊ��")
        
    if not input_dict.has_key('CUSCHRG'):
        return AfaFlowControl.ExitThisFlow("S999","�����Ѳ���Ϊ��")
        
    if not input_dict.has_key('RCCSMCD'):
        return AfaFlowControl.ExitThisFlow("S999","ժҪ���벻��Ϊ��")
    
    TradeContext.HostCode = '8813' 
    
    if input_dict['CHRGTYP'] == '1':                  #ת��
        TradeContext.ACUR    =  '3'                                           #���˴���
        #=====����+������====
        TradeContext.I3SMCD    =  PL_RCCSMCD_DZMZ                        #ժҪ����
        TradeContext.I3SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
        TradeContext.I3SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
        TradeContext.I3ACNM    =  'ũ��������'                                  #�跽����
        TradeContext.I3RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
        TradeContext.I3RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
        TradeContext.I3OTNM    =  "ũ����������ʱ��"                           #��������
        TradeContext.I3TRAM    =  "-" + str(input_dict['OCCAMT'] + input_dict['CUSCHRG'])  #���
        TradeContext.I3CTFG    =  '9'
        TradeContext.I3PKFG    = 'T'
        TradeContext.I3WARNTNO = ''
        TradeContext.I3CERTTYPE = ''
        TradeContext.I3CERTNO = ''
        #=====����====
        TradeContext.RCCSMCD    =  PL_RCCSMCD_DZMZ                     #ժҪ����
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS         #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  'ũ����������ʱ��'                                  #�跽����
        TradeContext.RBAC    =  input_dict['PYEACC']                          #�����˺�
        TradeContext.OTNM    =  input_dict['PYENAM']                            #��������
        TradeContext.OCCAMT  =  "-" + str(input_dict['OCCAMT'])
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    = 'T'
        #=====������====
        TradeContext.I2SMCD    =  PL_RCCSMCD_DZMZ                         #ժҪ����
        TradeContext.I2SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS         #�跽�˺�
        TradeContext.I2SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM    =  'ũ����������ʱ��'                                  #�跽����
        TradeContext.I2RBAC    =  TradeContext.BESBNO + PL_ACC_TCTDSXF            #�����˺�
        TradeContext.I2RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM    =  "������"                            #��������
        TradeContext.I2TRAM    =  "-" + str(input_dict['CUSCHRG'])
        TradeContext.I2CTFG    =  '8'
        TradeContext.I2PKFG    =  'T'
        
    elif input_dict['CHRGTYP'] == '0':     #����
        TradeContext.ACUR    =  '2'                                           #���˴��� 
        #=====����====
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZMZ                         #ժҪ����
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  'ũ��������'                                  #�跽����
        TradeContext.RBAC    =  input_dict['PYEACC']                          #�����˺�
        TradeContext.OTNM    =  input_dict['PYENAM']                          #��������
        TradeContext.OCCAMT  =  "-" + str(input_dict['OCCAMT'])  #���
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    =  'T'
        #=====������====
        TradeContext.I2SMCD    =  PL_RCCSMCD_DZMZ                      #ժҪ����
        TradeContext.I2RVFG    = '2' 
        TradeContext.I2SBAC    =  TradeContext.BESBNO + PL_ACC_QTYFK         #�跽�˺�
        TradeContext.I2SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM    =  '����Ӧ����'                                  #�跽����
        TradeContext.I2RBAC    =  TradeContext.BESBNO + PL_ACC_TCTDSXF            #�����˺�
        TradeContext.I2RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM    =  "������"                                     #��������
        TradeContext.I2TRAM    =  str(input_dict['CUSCHRG'])
        TradeContext.I2CTFG    =  '8'
        TradeContext.I2PKFG    =  'T'
        
    else:                     #����
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZMZ                       #ժҪ����
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  'ũ��������'                                  #�跽����
        TradeContext.RBAC    =  input_dict['PYEACC']                          #�����˺�
        TradeContext.OTNM    =  input_dict['PYENAM']                          #��������
        TradeContext.OCCAMT  =  "-" + str(input_dict['OCCAMT'])  #���
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    =  'T'
        
    
    AfaLoggerFunc.tradeInfo(">>>����������ת������Ĩ�˻�Ʒ�¼��ֵ")
    return True
 
 
##########################add by pgt 12-9################################################
#�����ֽ�ͨ�����˼��˻�Ʒ�¼��ֵ
def KZTCLZJZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>��ʼ�����ֽ�ͨ�����˼��˻�Ʒ�¼��ֵ")

    if not input_dict.has_key('PYEACC'):
        return AfaFlowControl.ExitThisFlow("S999","�տ����˺Ų���Ϊ��")
        
    if not input_dict.has_key('PYENAM'):
        return AfaFlowControl.ExitThisFlow("S999","�տ��˻�������Ϊ��")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","���׽���Ϊ��")
    
    TradeContext.HostCode = '8813' 
       
    TradeContext.PKFG = 'E'                                             #ͨ��ͨ�ұ�ʶ
#    TradeContext.CATR = '0'                                             #��ת��ʶ:0-�ֽ�
    TradeContext.RCCSMCD  = PL_RCCSMCD_DZBJ                           #����ժҪ��:�ֽ�ͨ������    TradeContext.OCCAMT = str(input_dict['OCCAMT'])
    TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ           #�跽�˺�
    TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
    TradeContext.SBNM = "ũ��������������"                              #�跽����
    TradeContext.RBAC = input_dict['PYEACC']                            #�����˺�
    TradeContext.RBNM = input_dict['PYENAM']                            #��������
    TradeContext.CTFG = '7'                                             #���������ѱ�ʾ
    TradeContext.OCCAMT = str(input_dict['OCCAMT'])
    
    AfaLoggerFunc.tradeInfo("�跽�˺�1:[" + TradeContext.SBAC + "]")
    AfaLoggerFunc.tradeInfo("�����˺�1:[" + TradeContext.RBAC + "]")
    
    AfaLoggerFunc.tradeInfo(">>>���������ֽ�ͨ�����˼��˻�Ʒ�¼��ֵ")
    return True

    
#���۱�ת�����˼��˻�Ʒ�¼��ֵ
def KZBZYLZJZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>��ʼ���۱�ת���������˻�Ʒ�¼��ֵ")
            
    if not input_dict.has_key('PYEACC'):
        return AfaFlowControl.ExitThisFlow("S999","�������˺Ų���Ϊ��")
        
    if not input_dict.has_key('PYENAM'):
        return AfaFlowControl.ExitThisFlow("S999","�����˻�������Ϊ��")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","���׽���Ϊ��")
    
    TradeContext.HostCode = '8813' 
      
    TradeContext.PKFG = 'E'                                         #ͨ��ͨ�ұ�ʶ
    TradeContext.OCCAMT = str(input_dict['OCCAMT'])                 #��Ʊ���
    TradeContext.RCCSMCD  = PL_RCCSMCD_DZBJ                        #����ժҪ��:��ת������
    TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ       #�跽�˺�:ũ��������������
    TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
    TradeContext.ACNM = "ũ��������������"                          #�跽����
    TradeContext.RBAC = input_dict['PYEACC']                        #�����˺�
    TradeContext.OTNM = input_dict['PYENAM']
    if TradeContext.existVariable('PASSWD'):
        TradeContext.PASSWD = TradeContext.PASSWD                       #����������
    else:
        AfaLoggerFunc.tradeInfo("======��У���������======")
        
    if input_dict.has_key('WARNTNO'):
        TradeContext.WARNTNO = input_dict['WARNTNO']
    else:
        AfaLoggerFunc.tradeInfo("======��У��ƾ֤����======")
    
    if input_dict.has_key('CERTTYPE') and input_dict.has_key('CERTNO'):
        TradeContext.CERTTYPE = TradeContext.CERTTYPE                   #֤������
        TradeContext.CERTNO   = TradeContext.CERTNO                     #֤������
    else:
        AfaLoggerFunc.tradeInfo("======��У��֤������======")
        
    TradeContext.CTFG = '7'                                             #������ѧ�ѱ�ʾ
    
    AfaLoggerFunc.tradeInfo("�跽�˺�1:[" + TradeContext.SBAC + "]")
    AfaLoggerFunc.tradeInfo("�����˺�1:[" + TradeContext.RBAC + "]")
    
    AfaLoggerFunc.tradeInfo(">>>�������۱�ת�����˼��˻�Ʒ�¼��ֵ")
    return True
    

#�����ֽ�ͨ�����˼��˻�Ʒ�¼��ֵ    
def KZTDLZJZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>��ʼ�����ֽ�ͨ�����˼��˻�Ʒ�¼��ֵ")
    
    if not input_dict.has_key('CHRGTYP'):
        return AfaFLowControl.ExitThisFlow("S999","��������ȡ��ʽ����Ϊ��")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","���׽���Ϊ��")
        
    if not input_dict.has_key('CUSCHRG'):
        return AfaFlowControl.ExitThisFlow("S999","�����Ѳ���Ϊ��")
        
    if not input_dict.has_key('PYRACC'):
        return AfaFlowControl.ExitThisFlow("S999","�տ����˻�����Ϊ��")
        
    if not input_dict.has_key('PYRNAM'):
        return AfaFlowControl.ExitThisFlow("S999","�տ��˻�������Ϊ��")
    
    TradeContext.HostCode = '8813' 
    
    if input_dict['CHRGTYP'] == '1':
        #=====ת��====
        TradeContext.ACUR    =  '3'                                     #���˴���
        #=========���׽��+������===================
        TradeContext.I3SMCD =  PL_RCCSMCD_DZBJ                                 #ժҪ���� 
        TradeContext.I3SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�跽�˺�
        TradeContext.I3SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
        TradeContext.I3ACNM    =  'ũ����������ʱ��'                            #�跽����
        TradeContext.I3RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ         #�����˺�
        TradeContext.I3RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
        TradeContext.I3OTNM    =  'ũ��������'                                  #��������
        TradeContext.I3TRAM    =  str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #������
        TradeContext.I3PKFG    = 'E'                                            #ͨ��ͨ�ұ�ʾ
        TradeContext.I3CTFG    = '9'                                            #������ѧ�ѱ�ʾ
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�跽�˺�' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�����˺�' + TradeContext.I3RBAC )
        #=========���׽��============
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZBJ                             #ժҪ����
        TradeContext.SBAC  =  input_dict['PYRACC']                          #�跽�˺�
        TradeContext.ACNM  =  input_dict['PYRNAM']                          #�跽����
        TradeContext.RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
        TradeContext.RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM  =  'ũ����������ʱ��'                            #��������
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #������
        TradeContext.CTFG  = '7'
        TradeContext.PKFG  = 'E'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO = ''
#        TradeContext.CATR  =  '0'                                           #��ת��־
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�跽�˺�' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�����˺�' + TradeContext.RBAC )
        #=========�������������뻧===========
        TradeContext.I2SMCD  =  PL_RCCSMCD_DZBJ                                #ժҪ����
        TradeContext.I2SBAC  =  input_dict['PYRACC']                          #�跽�˺�
        TradeContext.I2ACNM  =  input_dict['PYRNAM']                          #�跽����
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  'ũ����������ʱ��'                            #��������
        TradeContext.I2TRAM  =  str(input_dict['CUSCHRG'])                    #������
        TradeContext.I2CTFG  = '8'
        TradeContext.I2PKFG  = 'E'
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�跽�˺�' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�����˺�' + TradeContext.I2RBAC )
    
    elif input_dict['CHRGTYP'] in ('2','0'):                                          #�ֽ�
        #=====����====
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZBJ                             #ժҪ����
        TradeContext.SBAC    =  input_dict['PYRACC']                          #�跽�˺�
        TradeContext.ACNM    =  input_dict['PYRNAM']                          #�跽����
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ         #�����˺�
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  'ũ��������������'                          #��������
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #���
        TradeContext.CTFG    = '7'
        TradeContext.PKFG    = 'E'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO  = ''
#        TradeContext.CATR    =  '0'                                             #��ת��־
        
    else:
        return AfaFlowControl.ExitThisFlow("ԭ������������ȡ��ʽ�Ƿ�")
            
    AfaLoggerFunc.tradeInfo(">>>���������ֽ�ͨ�������˻�Ʒ�¼��ֵ")
    return True
    
    
#������ת�����˼��˻�Ʒ�¼��ֵ
def KZYZBLZJZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>��ʼ������ת�����˼��˻�Ʒ�¼��ֵ")
    
    if not input_dict.has_key('CHRGTYP'):
        return AfaFLowControl.ExitThisFlow("S999","��������ȡ��ʽ����Ϊ��")
        
    if not input_dict.has_key('PYRACC'):
        return AfaFlowControl.ExitThisFlow("S999","�տ����˺Ų���Ϊ��")
        
    if not input_dict.has_key('PYRNAM'):
        return AfaFlowControl.ExitThisFlow("S999","�տ��˻�������Ϊ��")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","���׽���Ϊ��")
        
    if not input_dict.has_key('CUSCHRG'):
        return AfaFlowControl.ExitThisFlow("S999","�����Ѳ���Ϊ��")
    
    TradeContext.HostCode = '8813' 
    
    if input_dict['CHRGTYP'] == '1':
        #=====ת��====
        TradeContext.ACUR    =  '3'                                     #���˴���
        #=========���׽��+������===================
        TradeContext.I3RCCSMCD =  PL_RCCSMCD_DZBJ                                  #ժҪ����  PL_RCCSMCD_YZBWZ ��ת��
        TradeContext.I3SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS              #�跽�˺�
        TradeContext.I3SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)        
        TradeContext.I3ACNM    =  'ũ����������ʱ��'                                #�跽����
        TradeContext.I3RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ             #�����˺�
        TradeContext.I3RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)        
        TradeContext.I3OTNM    =  'ũ��������������'                                #��������
        TradeContext.I3TRAM  =  str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #������
        TradeContext.I3PKFG    = 'E'
        TradeContext.I3CTFG    = '9'
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�跽�˺�' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�����˺�' + TradeContext.I3RBAC )
        #=========���׽��============
        TradeContext.RCCSMCD  =  PL_RCCSMCD_DZBJ                              #ժҪ����
        TradeContext.SBAC  =  input_dict['PYRACC']                          #�跽�˺�
        TradeContext.ACNM  =  input_dict['PYRNAM']                          #�跽����
        TradeContext.RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
        TradeContext.RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM  =  'ũ����������ʱ��'                            #��������
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #������
        TradeContext.CTFG  = '7'
        TradeContext.PKFG  = 'E'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�跽�˺�' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�����˺�' + TradeContext.RBAC )
        #=========�������������뻧===========
        TradeContext.I2SMCD  =  PL_RCCSMCD_DZBJ                                #ժҪ����
        TradeContext.I2SBAC  =  input_dict['PYRACC']          #�跽�˺�
        TradeContext.I2ACNM  =  input_dict['PYRNAM']                                    #�跽����
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  'ũ����������ʱ��'                                  #��������
        TradeContext.I2TRAM  =  str(input_dict['CUSCHRG'])                    #������
        TradeContext.I2CTFG  = '8'
        TradeContext.I2PKFG  = 'E'
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�跽�˺�' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�����˺�' + TradeContext.I2RBAC )

    elif input_dict['CHRGTYP'] in ('2','0'):
        #=====����====
        TradeContext.ACUR    =  '1'                                           #���˴���
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZBJ                              #ժҪ����
        TradeContext.SBAC    =  input_dict['PYRACC']                          #�跽�˺�
        TradeContext.ACNM    =  input_dict['PYRNAM']                          #�跽����
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ          #�����˺�
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  'ũ��������������'                            #��������
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #���
        TradeContext.CTFG  = '7'
        TradeContext.PKFG  = 'E'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
        
    else:
        return AfaFlowControl.ExitThisFlow('S999','�������շѷ�ʽ�Ƿ�') 
    
    AfaLoggerFunc.tradeInfo(">>>����������ת�����˼��˻�Ʒ�¼��ֵ")
    return True   


#�����ֽ�ͨ������Ĩ�˻�Ʒ�¼��ֵ    
def KZTCLZMZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>��ʼ�����ֽ�ͨ������Ĩ�˻�Ʒ�¼��ֵ")

    if not input_dict.has_key('PYEACC'):
        return AfaFlowControl.ExitThisFlow("S999","�տ����˺Ų���Ϊ��")
        
    if not input_dict.has_key('PYENAM'):
        return AfaFlowControl.ExitThisFlow("S999","�տ��˻�������Ϊ��")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","���׽���Ϊ��")
    
    TradeContext.HostCode = '8813' 
       
    TradeContext.PKFG = 'T'                                             #ͨ��ͨ�ұ�ʶ
    TradeContext.RCCSMCD  = PL_RCCSMCD_DZMZ                          #����ժҪ��:�ֽ�ͨ������    
    TradeContext.OCCAMT = str(input_dict['OCCAMT'])
    TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ           #�跽�˺�
    TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
    TradeContext.SBNM = "ũ��������������"                              #�跽����
    TradeContext.RBAC = input_dict['PYEACC']                            #�����˺�
    TradeContext.RBNM = input_dict['PYENAM']                            #��������
    TradeContext.CTFG = '7'                                             #���������ѱ�ʾ
    TradeContext.OCCAMT = "-" + str(input_dict['OCCAMT'])
    
    AfaLoggerFunc.tradeInfo("�跽�˺�1:[" + TradeContext.SBAC + "]")
    AfaLoggerFunc.tradeInfo("�����˺�1:[" + TradeContext.RBAC + "]")
    
    AfaLoggerFunc.tradeInfo(">>>���������ֽ�ͨ������Ĩ�˻�Ʒ�¼��ֵ")
    return True    
    
#���۱�ת������Ĩ�˻�Ʒ�¼��ֵ
def KZBZYLZMZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>��ʼ���۱�ת������Ĩ�˻�Ʒ�¼��ֵ")
            
    if not input_dict.has_key('PYEACC'):
        return AfaFlowControl.ExitThisFlow("S999","�������˺Ų���Ϊ��")
        
    if not input_dict.has_key('PYENAM'):
        return AfaFlowControl.ExitThisFlow("S999","�����˻�������Ϊ��")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","���׽���Ϊ��")
    
    TradeContext.HostCode = '8813' 
      
    TradeContext.PKFG = 'T'                                         #ͨ��ͨ�ұ�ʶ
    
    TradeContext.OCCAMT = "-" + str(input_dict['OCCAMT'])                 #��Ʊ���
    TradeContext.RCCSMCD  = PL_RCCSMCD_DZMZ                        #����ժҪ��:��ת������
    TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ       #�跽�˺�:ũ��������������
    TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
    TradeContext.ACNM = "ũ��������������"                          #�跽����
    TradeContext.RBAC = input_dict['PYEACC']                        #�����˺�:�տ����˻�
    TradeContext.OTNM = input_dict['PYENAM']
    if TradeContext.existVariable('PASSWD'):
        TradeContext.PASSWD = TradeContext.PASSWD                       #����������
    else:
        AfaLoggerFunc.tradeInfo("======��У������Ĩ��======")
        
    if input_dict.has_key('WARNTNO'):
        TradeContext.WARNTNO = input_dict['WARNTNO']
    else:
        AfaLoggerFunc.tradeInfo("======��У��ƾ֤Ĩ��======")
    
    if input_dict.has_key('CERTTYPE') and input_dict.has_key('CERTNO'):
        TradeContext.CERTTYPE = TradeContext.CERTTYPE                   #֤������
        TradeContext.CERTNO   = TradeContext.CERTNO                     #֤������
    else:
        AfaLoggerFunc.tradeInfo("======��У��֤��Ĩ��======")
        
    TradeContext.CTFG = '7'                                             #���������ѱ�ʶ
    
    AfaLoggerFunc.tradeInfo("�跽�˺�1:[" + TradeContext.SBAC + "]")
    AfaLoggerFunc.tradeInfo("�����˺�1:[" + TradeContext.RBAC + "]")
    
    AfaLoggerFunc.tradeInfo(">>>�������۱�ת������Ĩ�˻�Ʒ�¼��ֵ")
    return True  

#�����ֽ�ͨ������Ĩ�˻�Ʒ�¼��ֵ        
def KZTDLZMZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>��ʼ�����ֽ�ͨ������Ĩ�˻�Ʒ�¼��ֵ")
    
    if not input_dict.has_key('CHRGTYP'):
        return AfaFLowControl.ExitThisFlow("S999","��������ȡ��ʽ����Ϊ��")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","���׽���Ϊ��")
        
    if not input_dict.has_key('CUSCHRG'):
        return AfaFlowControl.ExitThisFlow("S999","�����Ѳ���Ϊ��")
        
    if not input_dict.has_key('PYRACC'):
        return AfaFlowControl.ExitThisFlow("S999","�տ����˻�����Ϊ��")
        
    if not input_dict.has_key('PYRNAM'):
        return AfaFlowControl.ExitThisFlow("S999","�տ��˻�������Ϊ��")
    
    TradeContext.HostCode = '8813' 
    
    if input_dict['CHRGTYP'] == '1':
        #=====ת��====
        TradeContext.ACUR    =  '3'                                     #Ĩ�˴���
        #=========���׽��+������===================
        TradeContext.RCCSMCD    =  PL_RCCSMCD_DZMZ                                 #ժҪ���� 
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  'ũ����������ʱ��'                            #�跽����
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ         #�����˺�
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  'ũ��������'                                  #��������
        TradeContext.OCCAMT   = "-" + str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #������
        TradeContext.PKFG    = 'T'                                            #ͨ��ͨ�ұ�ʾ
        TradeContext.CTFG    = '9'                                            #������ѧ�ѱ�ʾ
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�跽�˺�' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�����˺�' + TradeContext.RBAC )
        #=========���׽��============
        TradeContext.I2SMCD  =  PL_RCCSMCD_DZMZ                             #ժҪ����
        TradeContext.I2SBAC  =  input_dict['PYRACC']                          #�跽�˺�
        TradeContext.I2ACNM  =  input_dict['PYRNAM']                          #�跽����
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
        TradeContext.I2RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  'ũ����������ʱ��'                            #��������
        TradeContext.I2TRAM  =  "-" + str(input_dict['OCCAMT'])                     #������
        TradeContext.I2CTFG  = '7'
        TradeContext.I2PKFG  = 'T'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO = ''
#        TradeContext.CATR  =  '0'                                           #��ת��־
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�跽�˺�' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�����˺�' + TradeContext.I2RBAC )
        #=========�������������뻧===========
        TradeContext.I3SMCD  =  PL_RCCSMCD_DZMZ                                #ժҪ����
        TradeContext.I3SBAC  =  input_dict['PYRACC']                          #�跽�˺�
        TradeContext.I3ACNM  =  input_dict['PYRNAM']                          #�跽����
        TradeContext.I3RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
        TradeContext.I3RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
        TradeContext.I3OTNM  =  'ũ����������ʱ��'                            #��������
        TradeContext.I3TRAM  =  "-" + str(input_dict['CUSCHRG'])                    #������
        TradeContext.I3CTFG  = '8'
        TradeContext.I3PKFG  = 'T'
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�跽�˺�' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�����˺�' + TradeContext.I3RBAC )
    
    elif input_dict['CHRGTYP'] == '0':                                          #�ֽ�
        #=====����====
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZMZ                             #ժҪ����
        TradeContext.SBAC    =  input_dict['PYRACC']         #�跽�˺�
        TradeContext.ACNM    =  input_dict['PYRNAM']                            #�跽����
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ                          #�����˺�
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  'ũ��������������'                          #��������
        TradeContext.OCCAMT  =  "-" + str(input_dict['OCCAMT'])                     #���
        TradeContext.CTFG    = '7'
        TradeContext.PKFG    = 'T'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO  = ''
#        TradeContext.CATR    =  '0'                                             #��ת��־
        
    elif input_dict['CHRGTYP'] == '2':
        #=====���շ�====
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZMZ                            #ժҪ����
        TradeContext.SBAC    =  input_dict['PYRACC']         #�跽�˺�
        TradeContext.ACNM    =  input_dict['PYRNAM']                            #�跽����
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ                          #�����˺�
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  'ũ��������������'                          #��������
        TradeContext.OCCAMT  =  "-" + str(input_dict['OCCAMT'])                     #���
        TradeContext.CTFG    = '7'
        TradeContext.PKFG    = 'T'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO  = ''
#        TradeContext.CATR    =  '0'                                             #��ת��־
    else:
        return AfaFlowControl.ExitThisFlow("ԭ������������ȡ��ʽ�Ƿ�")
            
    AfaLoggerFunc.tradeInfo(">>>���������ֽ�ͨ����Ĩ�˻�Ʒ�¼��ֵ")
    return True  
  
#������ת������Ĩ�˻�Ʒ�¼��ֵ
def KZYZBLZMZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>��ʼ������ת������Ĩ�˻�Ʒ�¼��ֵ")
    
    if not input_dict.has_key('CHRGTYP'):
        return AfaFLowControl.ExitThisFlow("S999","��������ȡ��ʽ����Ϊ��")
        
    if not input_dict.has_key('PYRACC'):
        return AfaFlowControl.ExitThisFlow("S999","�տ����˺Ų���Ϊ��")
        
    if not input_dict.has_key('PYRNAM'):
        return AfaFlowControl.ExitThisFlow("S999","�տ��˻�������Ϊ��")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","���׽���Ϊ��")
        
    if not input_dict.has_key('CUSCHRG'):
        return AfaFlowControl.ExitThisFlow("S999","�����Ѳ���Ϊ��")
    
    TradeContext.HostCode = '8813' 
    
    if input_dict['CHRGTYP'] == '1':
        #=====ת��====
        TradeContext.ACUR    =  '3'                                     #Ĩ�˴���
        #=========���׽��+������===================
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZMZ                                 #ժҪ����  PL_RCCSMCD_YZBWZ ��ת��
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS              #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)        
        TradeContext.ACNM    =  'ũ����������ʱ��'                                #�跽����
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ             #�����˺�
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)        
        TradeContext.OTNM    =  'ũ��������������'                                #��������
        TradeContext.OCCAMT    = "-" + str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #������
        TradeContext.PKFG    = 'T'
        TradeContext.CTFG    = '9'
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�跽�˺�' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�����˺�' + TradeContext.RBAC )
        #=========���׽��============
        TradeContext.I2SMCD  =  PL_RCCSMCD_DZMZ                             #ժҪ����
        TradeContext.I2SBAC  =  input_dict['PYRACC']                          #�跽�˺�
        TradeContext.I2ACNM  =  input_dict['PYRNAM']                          #�跽����
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  'ũ����������ʱ��'                            #��������
        TradeContext.I2TRAM  = "-" + str(input_dict['OCCAMT'])                     #������
        TradeContext.I2CTFG  = '7'
        TradeContext.I2PKFG  = 'T'
        TradeContext.I2WARNTNO = ''
        TradeContext.I2CERTTYPE = ''
        TradeContext.I2CERTNO = ''
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�跽�˺�' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�����˺�' + TradeContext.I2RBAC )
        #=========�������������뻧===========
        TradeContext.I3SMCD  =  PL_RCCSMCD_DZMZ                                #ժҪ����
        TradeContext.I3SBAC  =  input_dict['PYRACC']          #�跽�˺�
        TradeContext.I3ACNM  =  input_dict['PYRNAM']                                    #�跽����
        TradeContext.I3RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
        TradeContext.I3RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
        TradeContext.I3OTNM  =  'ũ����������ʱ��'                                  #��������
        TradeContext.I3TRAM  =  "-" + str(input_dict['CUSCHRG'])                    #������
        TradeContext.I3CTFG  = '8'
        TradeContext.I3PKFG  = 'T'
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�跽�˺�' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�����˺�' + TradeContext.I3RBAC )

    elif input_dict['CHRGTYP'] == '0':
        #=====����====
        TradeContext.ACUR    =  '1'                                           #Ĩ�˴���
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZMZ                              #ժҪ����
        TradeContext.SBAC    =  input_dict['PYRACC']                          #�跽�˺�
        TradeContext.ACNM    =  input_dict['PYRNAM']                          #�跽����
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ          #�����˺�
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  'ũ��������������'                            #��������
        TradeContext.OCCAMT  =  "-" + str(input_dict['OCCAMT'])                     #���
        TradeContext.CTFG  = '7'
        TradeContext.PKFG  = 'T'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
        
    elif input_dict['CHRGTYP'] == '2':
        #=====���շ�====
        TradeContext.ACUR    =  '1'                                           #Ĩ�˴���
        TradeContext.RCCSMCD =  PL_RCCSMCD_DZMZ                               #ժҪ����
        TradeContext.SBAC    =  input_dict['PYRACC']                          #�跽�˺�
        TradeContext.ACNM    =  input_dict['PYRNAM']                          #�跽����
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ          #�����˺�
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  'ũ��������������'                            #��������
        TradeContext.OCCAMT  =  "-" + str(input_dict['OCCAMT'])                     #���
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    =  'T'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
    else:
        return AfaFlowControl.ExitThisFlow('S999','�������շѷ�ʽ�Ƿ�') 
    
    AfaLoggerFunc.tradeInfo(">>>����������ת������Ĩ�˻�Ʒ�¼��ֵ")
    return True     