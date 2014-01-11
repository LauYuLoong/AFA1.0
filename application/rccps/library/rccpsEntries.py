# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ.��Ʒ�¼��ֵģ��
#===============================================================================
#   �����ļ�:   rccpsEntries.py
#   ��    ��:   �ر��
#   �޸�ʱ��:   2008-11-30
################################################################################

import AfaLoggerFunc,AfaDBFunc,TradeContext, LoggerHandler, sys, os, time, AfaUtilTools, ConfigParser,AfaFlowControl
import rccpsDBFunc,rccpsGetFunc
from types import *
from rccpsConst import *
import rccpsHostFunc

##������ʼ���
def HDWZJZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>��ʼ������˼��˻�Ʒ�¼��ֵ")
    
    if not input_dict.has_key('CHRGTYP'):
        return AfaFLowControl.ExitThisFlow("S999","��������ȡ��ʽ����Ϊ��")
        
    if not input_dict.has_key('PYRACC'):
        return AfaFlowControl.ExitThisFlow("S999","�������˺Ų���Ϊ��")
        
    if not input_dict.has_key('ACNM'):
        return AfaFlowControl.ExitThisFlow("S999","�����˻�������Ϊ��")
    
    if not input_dict.has_key('OTNM'):
        return AfaFlowControl.ExitThisFlow("S999","�տ��˻�������Ϊ��")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","���׽���Ϊ��")
        
    if not input_dict.has_key('LOCCUSCHRG'):
        return AfaFlowControl.ExitThisFlow("S999","�����Ѳ���Ϊ��")

    if not input_dict.has_key('BBSSRC'):
        return AfaFlowControl.ExitThisFlow("S999","�ʽ���Դ����Ϊ��")
        
    if not input_dict.has_key('BESBNO'):
        return AfaFlowControl.ExitThisFlow("S999","�����Ų���Ϊ��")
    #=====���ü��˺����ӿ�====

    TradeContext.HostCode = '8813'
    TradeContext.BRSFLG   = PL_BRSFLG_SND                                    #������ʶ:����
    TradeContext.RCCSMCD  = PL_RCCSMCD_HDWZ                                  #����ժҪ���룺�������
    
    TradeContext.BESBNO   = input_dict['BESBNO']
    TradeContext.BBSSRC   = input_dict['BBSSRC']

    #=====�跽�˺�,�ʽ���ԴΪ3-�ڲ���====
    if TradeContext.BBSSRC != '3' and TradeContext.BBSSRC != '5':
        TradeContext.SBAC = input_dict['PYRACC']
    else:
        TradeContext.SBAC = ''
        
    #=====�ж��ʽ���Դ����ƾ֤����====
    if TradeContext.BBSSRC == '0':
        TradeContext.WARNTNO = TradeContext.SBAC[6:18]
        AfaLoggerFunc.tradeInfo( 'ƾ֤���룺' + TradeContext.WARNTNO )
    #=====�ֽ�ʱ����ת��־====
    if TradeContext.BBSSRC == '5':
        TradeContext.CATR = '0'
        
    TradeContext.CTFG     = '7'                                              #���������ѱ�ʾ
    TradeContext.TRCTYP   = '20'                                             
    TradeContext.OCCAMT   = str(input_dict['OCCAMT'])                        #���

    TradeContext.OTNM     = input_dict['OTNM']                               #�տ��˻���
    TradeContext.ACNM     = input_dict['ACNM']                               #�����˻���
    
    #=====��ʼƴ�����˺�====
    AfaLoggerFunc.tradeInfo( ">>>׼���������������" )
    TradeContext.RBAC =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ

    #=====��ʼ������ƴ�����˺ŵ�25λУ��λ====
    TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC, 25)
    
    AfaLoggerFunc.tradeInfo("�跽�˺�1:[" + TradeContext.SBAC + "]")
    AfaLoggerFunc.tradeInfo("�����˺�1:[" + TradeContext.RBAC + "]")
    
    
    ##======�ź� ������������ȡ 20091109  ======================
    if   input_dict['CHRGTYP'] == '0' :                                      # �ֽ���ȡ������'0' 
        TradeContext.ACUR    = '2'                                           #�ظ����� 
        TradeContext.I2SMCD  = PL_RCCSMCD_SXF                                #����ժҪ���룺�������
        TradeContext.I2TRAM = str(input_dict['LOCCUSCHRG'])                  #�����ѽ��
        TradeContext.I2CATR = '0'                                            #��ת��ʶ:0-�ֽ�
        TradeContext.I2SBAC = ''                                             #�跽�˺�  
        TradeContext.I2ACNM = ''
        TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_HDSXF             #�����˺�,���������뻧
        TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM = "ũ����������"
        TradeContext.I2CTFG = '8'                                             #�����ѱ�ʾ

        AfaLoggerFunc.tradeInfo(">>>�ֽ���ȡ������")  
        
    elif input_dict['CHRGTYP'] == '1' :                                       # ת��������'1'
        TradeContext.ACUR    = '2'                                            #�ظ�����
        TradeContext.I2SMCD  = PL_RCCSMCD_SXF                                 #����ժҪ���룺�������
        TradeContext.I2TRAM  = str(input_dict['LOCCUSCHRG'])                  #�����ѽ��

        TradeContext.I2SBAC = input_dict['PYRACC']                            #�������˺�  
        
        TradeContext.I2ACNM = input_dict['ACNM'] 
        TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_HDSXF              #�����˺�,���������뻧
        TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM = "ũ����������"
        TradeContext.I2CTFG = '8'                                             #�����ѱ�ʾ
        
        AfaLoggerFunc.tradeInfo(">>>ת��������")

    elif input_dict['CHRGTYP'] == '2' :                                       # ����������'2'
        
        AfaLoggerFunc.tradeInfo(">>>����ȡ������")
        
    else:
        return AfaFlowControl.ExitThisFlow("S999","�Ƿ���������ȡ��ʽ")
        
    if TradeContext.existVariable("I2SBAC") and TradeContext.existVariable('I2RBAC'):
        AfaLoggerFunc.tradeInfo("�跽�˺�2:[" + TradeContext.I2SBAC + "]")
        AfaLoggerFunc.tradeInfo("�����˺�2:[" + TradeContext.I2RBAC + "]")
    
    AfaLoggerFunc.tradeInfo(">>>����������˼��˻�Ʒ�¼��ֵ")
    return True

##�������Ĩ��
def HDWZMZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>��ʼ�������Ĩ�˻�Ʒ�¼��ֵ")
    
    if not input_dict.has_key('BJEDTE'):                                   #ԭ����������
        return AfaFlowControl.ExitThisFlow("S999","���ڲ���Ϊ��")
        
    if not input_dict.has_key('BSPSQN'):                                   #ԭ������ǰ����ˮ��
        return AfaFlowControl.ExitThisFlow("S999","������Ų���Ϊ��")
    
    if not input_dict.has_key('PYRACC'):
        return AfaFlowControl.ExitThisFlow("S999","�������˺Ų���Ϊ��")

    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","����Ϊ��")

    if not input_dict.has_key('BBSSRC'):
        return AfaFlowControl.ExitThisFlow("S999","�ʽ���Դ����Ϊ��")

    if not input_dict.has_key('BESBNO'):
        return AfaFlowControl.ExitThisFlow("S999","�����Ų���Ϊ��")
        
    #=====����ʽ���ԴΪ�����ˣ�ʹ��8813���ֳ���====  
    if input_dict['BBSSRC']   ==  '3':                                           #������
        #ΪĨ�˸�ֵ��Ʒ�¼
        input_dict['SBAC']       = TradeContext.BESBNO  +  PL_ACC_NXYDQSWZ       #�跽�˺�
        input_dict['RBAC']       = TradeContext.BESBNO  +  PL_ACC_NXYDXZ         #�����˺�
        input_dict['CATR']       = '1' 
        TradeContext.OCCAMT      = str(input_dict['OCCAMT'])
        TradeContext.RVFG        = '0'                                           #�����ֱ�ʶ,0���
        #=====��ʼ������ƴ�����˺ŵ�25λУ��λ====
        input_dict['SBAC'] = rccpsHostFunc.CrtAcc(input_dict['SBAC'], 25)
        input_dict['RBAC'] = rccpsHostFunc.CrtAcc(input_dict['RBAC'], 25)
        
    elif input_dict['BBSSRC'] == '5':                                            # �ֽ� 
        #ΪĨ�˸�ֵ��Ʒ�¼ 
        input_dict['SBAC']       = TradeContext.BESBNO  +  PL_ACC_NXYDQSWZ       #�跽�˺�
        input_dict['RBAC']       = TradeContext.BESBNO  +  PL_ACC_DYKJQ          #�����˺�,2621,�����
        input_dict['CATR']       = '0' 
        TradeContext.RVFG        = '0'                                           #�����ֱ�ʶ,0���
        TradeContext.OCCAMT      = str(input_dict['OCCAMT'])
        #=====��ʼ������ƴ�����˺ŵ�25λУ��λ====
        input_dict['SBAC'] = rccpsHostFunc.CrtAcc(input_dict['SBAC'], 25)
        input_dict['RBAC'] = rccpsHostFunc.CrtAcc(input_dict['RBAC'], 25)
    else:
        #ΪĨ�˸�ֵ��Ʒ�¼
        input_dict['SBAC']       = input_dict['PYRACC'] 
        input_dict['RBAC']       = TradeContext.BESBNO  +  PL_ACC_NXYDQSWZ
        input_dict['CATR']       = '1' 
        TradeContext.OCCAMT      = "-" + str(input_dict['OCCAMT'])
        TradeContext.RVFG        = ''                                            #�����ֱ�ʶ,0���
        #=====��ʼ������ƴ�����˺ŵ�25λУ��λ====
        #TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
        input_dict['RBAC'] = rccpsHostFunc.CrtAcc(input_dict['RBAC'], 25)

    #�������˽ӿ�
    TradeContext.HostCode ='8813'
    
    TradeContext.CLDT     = input_dict['BJEDTE']                           #���ԭǰ������
    TradeContext.UNSQ     = input_dict['BSPSQN']                           #���ԭǰ����ˮ��
    
    if rccpsGetFunc.GetRBSQ(PL_BRSFLG_SND) == -1 :                         #ǰ����ˮ��new
        return AfaFlowControl.ExitThisFlow('A099','������ǰ����ˮ��ʧ��')
    TradeContext.FEDT=AfaUtilTools.GetHostDate( )                          #ǰ������new
    
    TradeContext.ACUR     = '1'                                            #�ظ�����
    TradeContext.CATR     = input_dict['CATR']                             #��ת��ʶ 
    TradeContext.RCCSMCD  = PL_RCCSMCD_WCH                                 #����ժҪ����
    TradeContext.DASQ     = ''
    
    TradeContext.SBAC     = input_dict['SBAC']                             #�跽�˺�
    TradeContext.RBAC     = input_dict['RBAC']                             #�����˺�
    
    
    AfaLoggerFunc.tradeInfo( '�跽�˺�:' + TradeContext.SBAC )
    AfaLoggerFunc.tradeInfo( '�����˺�:' + TradeContext.RBAC )
    
    AfaLoggerFunc.tradeInfo(">>>�����������Ĩ�˻�Ʒ�¼��ֵ")
    
    return True     

##������ʼ���
def HDLZJZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>��ʼ������˼��˻�Ʒ�¼��ֵ")
        
    if not input_dict.has_key('PYEACC'):
        return AfaFlowControl.ExitThisFlow("S999","�տ����˺Ų���Ϊ��")
            
    if not input_dict.has_key('OTNM'):
        return AfaFlowControl.ExitThisFlow("S999","�տ��˻�������Ϊ��")
    
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","���׽���Ϊ��")
        
    if not input_dict.has_key('accflag'):
        return AfaFlowControl.ExitThisFlow("S999","�ǹ��˱�־����Ϊ��")
        
    if not input_dict.has_key('BESBNO'):
        return AfaFlowControl.ExitThisFlow("S999","�����Ų���Ϊ��")

    if (TradeContext.existVariable( "SBACACNM" ) and len(TradeContext.SBACACNM) != 0):       #�����˻���
          TradeContext.ACNM      =      TradeContext.SBACACNM
    else:
          TradeContext.ACNM      =      ''
    #=====���ü��˺����ӿ�====

    TradeContext.HostCode = '8813'
    TradeContext.BRSFLG   = PL_BRSFLG_RCV                                    #������ʶ:����
    TradeContext.RCCSMCD  = PL_RCCSMCD_HDLZ                                  #����ժҪ���룺�������
    TradeContext.ACUR = '1'
    
    TradeContext.OCCAMT   = input_dict['OCCAMT']
    TradeContext.BESBNO   = input_dict['BESBNO']
    TradeContext.accflag  = input_dict['accflag']

    if TradeContext.accflag == '0':
        AfaLoggerFunc.tradeInfo('>>>�Զ�����')
        TradeContext.STRINFO = '�Զ�����'
        TradeContext.BCSTAT  = PL_BCSTAT_AUTO                            #�Զ�����
        TradeContext.BDWFLG  = PL_BDWFLG_WAIT                            #������
        
        TradeContext.SBAC    = TradeContext.BESBNO + PL_ACC_NXYDQSLZ     #�跽�˻�
        TradeContext.SBAC    = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
        
        TradeContext.RBAC    = input_dict['PYEACC']                      #�����˺�
        TradeContext.OTNM    = input_dict['OTNM']                        #��������
        
        AfaLoggerFunc.tradeInfo( '�跽�˺�:' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '�����˺�:' + TradeContext.RBAC )
    else:
        AfaLoggerFunc.tradeInfo('>>>�Զ�����')
        TradeContext.STRINFO = '�Զ�����'
        TradeContext.BCSTAT  = PL_BCSTAT_HANG                            #�Զ�����
        TradeContext.BDWFLG  = PL_BDWFLG_WAIT                            #������
            
        TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ        #�跽�˻�
        TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
        
        TradeContext.REAC = TradeContext.BESBNO + PL_ACC_NXYDXZ          #�����˺�
        TradeContext.REAC = rccpsHostFunc.CrtAcc(TradeContext.REAC, 25)

        AfaLoggerFunc.tradeInfo( '�跽�˺�:' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '�����˺�:' + TradeContext.REAC )

    AfaLoggerFunc.tradeInfo(">>>����������˼��˻�Ʒ�¼��ֵ")
    return True

##������ʹ���
def HDLZGZ(input_dict):
    AfaLoggerFunc.tradeInfo(">>>��ʼ������˹��˻�Ʒ�¼��ֵ")
            
    if not input_dict.has_key('OCCAMT'):
        return AfaFlowControl.ExitThisFlow("S999","���׽���Ϊ��")
        
    if not input_dict.has_key('accflag'):
        return AfaFlowControl.ExitThisFlow("S999","�ǹ��˱�־����Ϊ��")
        
    if not input_dict.has_key('BESBNO'):
        return AfaFlowControl.ExitThisFlow("S999","�����Ų���Ϊ��")

    #=====���ü��˺����ӿ�====

    TradeContext.HostCode = '8813'
    TradeContext.BRSFLG   = PL_BRSFLG_RCV                                    #������ʶ:����
    TradeContext.RCCSMCD  = PL_RCCSMCD_HDLZ                                  #����ժҪ���룺�������
    TradeContext.ACUR = '1'
    
    TradeContext.OCCAMT   = input_dict['OCCAMT']
    TradeContext.BESBNO   = input_dict['BESBNO']
    TradeContext.accflag  = input_dict['accflag']
    
    if TradeContext.accflag == '0':
        AfaLoggerFunc.tradeInfo('>>>�Զ�����')
        TradeContext.STRINFO = '�Զ�����'
        TradeContext.NOTE3 = '��������ʧ��,����!'
        TradeContext.BCSTAT  = PL_BCSTAT_HANG                            #�Զ�����
        TradeContext.BDWFLG  = PL_BDWFLG_WAIT                            #������
            
        TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ        #�跽�˻�
        TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
        
        TradeContext.REAC = TradeContext.BESBNO + PL_ACC_NXYDXZ          #�����˺�
        TradeContext.REAC = rccpsHostFunc.CrtAcc(TradeContext.REAC, 25)

        AfaLoggerFunc.tradeInfo( '�跽�˺�:' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '�����˺�:' + TradeContext.REAC )

    AfaLoggerFunc.tradeInfo(">>>����������˹��˻�Ʒ�¼��ֵ")
    return True


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
       
    TradeContext.PKFG = 'T'                                             #ͨ��ͨ�ұ�ʶ
    TradeContext.CATR = '0'                                             #��ת��ʶ:0-�ֽ�
    TradeContext.RCCSMCD  = PL_RCCSMCD_XJTCWZ                           #����ժҪ��:�ֽ�ͨ������
    TradeContext.OCCAMT = str(input_dict['OCCAMT'])
    TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_QTYSK
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
        
        TradeContext.I2PKFG = 'T'                                       #ͨ��ͨ�ұ�ʶ
        TradeContext.I2CATR = '0'                                       #��ת��ʶ:0-�ֽ�
        TradeContext.I2TRAM = str(input_dict['CUSCHRG'])                #�����ѽ��
        TradeContext.I2SMCD = PL_RCCSMCD_SXF                            #����ժҪ��:������
        TradeContext.I2SBAC = TradeContext.BESBNO + PL_ACC_QTYSK
        TradeContext.I2SBAC = rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM = '����Ӧ�׿�'
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
        
    TradeContext.PKFG = 'T'                                         #ͨ��ͨ�ұ�ʶ
    TradeContext.RVFG = '2'                                         #�����ֱ�־ 2
    TradeContext.CATR = '0'                                         #��ת��ʶ:0-�ֽ�
    TradeContext.OCCAMT = str(input_dict['OCCAMT'])                 #���׽��
    TradeContext.RCCSMCD = input_dict['RCCSMCD']                    #����ժҪ��:�ֽ�ͨ������
    TradeContext.SBAC = ''
    TradeContext.ACNM = ''
    TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSWZ       #�����˺�
    TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
    TradeContext.OTNM = "ũ��������������"
    TradeContext.CTFG = '7'                                         #���������ѱ�ʾ
    
    AfaLoggerFunc.tradeInfo("�跽�˺�1:[" + TradeContext.SBAC + "]")
    AfaLoggerFunc.tradeInfo("�����˺�1:[" + TradeContext.RBAC + "]")
    
    if input_dict['CHRGTYP'] == '0':
        #�ֽ���ȡ������
        TradeContext.ACUR   = '2'                                       #�ظ�����
        
        TradeContext.I2PKFG = 'T'                                       #ͨ��ͨ�ұ�ʶ
        TradeContext.I2RVFG = '2'                                       #�����ֱ�־ 2
        TradeContext.I2CATR = '0'                                       #��ת��ʶ:0-�ֽ�
        TradeContext.I2TRAM = str(input_dict['CUSCHRG'])                #�����ѽ��
        TradeContext.I2SMCD = input_dict['RCCSMCD']                     #����ժҪ��:������
        TradeContext.I2SBAC = ''
        TradeContext.I2ACNM = ''
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
      
    TradeContext.PKFG = 'T'                                         #ͨ��ͨ�ұ�ʶ
    
    TradeContext.OCCAMT = str(input_dict['OCCAMT'])                 #��Ʊ���
    TradeContext.RCCSMCD  = PL_RCCSMCD_BZYWZ                        #����ժҪ��:��ת������
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
        
        TradeContext.I2PKFG = 'T'                                       #ͨ��ͨ�ұ�ʶ
        TradeContext.I2CATR = '0'                                       #��ת��ʶ:0-�ֽ�
        TradeContext.I2TRAM = str(input_dict['CUSCHRG'])                #�����ѽ��
        TradeContext.I2SMCD = PL_RCCSMCD_SXF                            #����ժҪ��:������
        TradeContext.I2SBAC = ""                                        #�跽�˺�:��Աβ��
        TradeContext.I2ACNM = ""                                        
        TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_TCTDSXF      #�����˺�:ͨ��ͨ��������
        TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM = "������"
        TradeContext.I2CTFG = '8'                                       #���������ѱ�ʾ
        
    elif TradeContext.CHRGTYP == '1':
        #�����˻���ȡ
        AfaLoggerFunc.tradeInfo(">>>�����˻���ȡ������")
        TradeContext.ACUR = '2'                                         #�ظ�����
        
        TradeContext.I2PKFG = 'T'                                       #ͨ��ͨ�ұ�ʶ
        TradeContext.I2TRAM = str(input_dict['CUSCHRG'])                #�����ѽ��
        TradeContext.I2SMCD = PL_RCCSMCD_SXF                            #����ժҪ��:������
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
    
    if input_dict['CHRGTYP'] == '0':
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
        
        TradeContext.ACUR = '2'                                         #�ظ�����
        
        TradeContext.PKFG = 'T'                                         #ͨ��ͨ�ұ�ʶ
        TradeContext.OCCAMT = "-" + str(input_dict['OCCAMT'])           #���׽��
        TradeContext.RCCSMCD = input_dict['RCCSMCD']                    #����ժҪ��:��ת������
        TradeContext.SBAC = input_dict['PYRACC']                        #�跽�˺�:�ͻ���
        TradeContext.ACNM = input_dict['PYRNAM']                        #�跽����
        TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSWZ       #�����˺�:������
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
        
        TradeContext.I2PKFG = 'T'                                       #ͨ��ͨ�ұ�ʶ
        TradeContext.I2RVFG = '2'                                       #�����ֱ�־ 2
        TradeContext.I2CATR = '0'                                       #��ת��ʶ:0-�ֽ�
        TradeContext.I2TRAM = str(input_dict['CUSCHRG'])                #�����ѽ��
        TradeContext.I2SMCD = input_dict['RCCSMCD']                     #����ժҪ��:������
        TradeContext.I2SBAC = ""                                        #�跽�˺�:��Աβ��
        TradeContext.I2ACNM = ""                                        
        TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_TCTDSXF      #�����˺�:ͨ��ͨ��������
        TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM = "������"
        TradeContext.I2CTFG = '8'                                       #������ѧ�ѱ�ʾ
        
        AfaLoggerFunc.tradeInfo("�跽�˺�2:[" + TradeContext.I2SBAC + "]")
        AfaLoggerFunc.tradeInfo("�����˺�2:[" + TradeContext.I2RBAC + "]")
    else:
        TradeContext.HostCode='8820'
        if not input_dict.has_key('FEDT'):
            return AfaFlowControl.ExitThisFlow("S999","ԭǰ�����ڲ���Ϊ��")
        if not input_dict.has_key('RBSQ'):
            return AfaFlowControl.ExitThisFlow("S999","ԭǰ����ˮ�Ų���Ϊ��")
            
        TradeContext.BOJEDT = input_dict['FEDT']
        TradeContext.BOSPSQ = input_dict['RBSQ']
        
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
        TradeContext.RCCSMCD =  PL_RCCSMCD_CX                                 #ժҪ���� 
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  'ũ��������'                                  #�跽����
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  'Ӧ����'                                    #��������
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #������
        TradeContext.PKFG    = 'T'                                            #ͨ��ͨ�ұ�ʾ
        TradeContext.CTFG    = '9'                                            #������ѧ�ѱ�ʾ
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�跽�˺�' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�����˺�' + TradeContext.RBAC )
        #=========���׽��============
        TradeContext.I2SMCD  =  PL_RCCSMCD_CX                                 #ժҪ����
        TradeContext.I2SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�跽�˺�
        TradeContext.I2SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM  =  'Ӧ����'                                    #�跽����
        TradeContext.I2RBAC  =  ''                                            #�����˺�
        TradeContext.I2OTNM  =  ''                                            #��������
        TradeContext.I2TRAM  =  str(input_dict['OCCAMT'])                       #������
        TradeContext.I2CTFG  = '7'
        TradeContext.I2PKFG  = 'T'
        #TradeContext.I2WARNTNO = ''
        #TradeContext.I2CERTTYPE = ''
        #TradeContext.I2CERTNO = ''
        TradeContext.I2CATR  =  '0'                                           #��ת��־
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�跽�˺�' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�����˺�' + TradeContext.I2RBAC )
        #=========�������������뻧===========
        TradeContext.I3SMCD  =  PL_RCCSMCD_CX                                 #ժҪ����
        TradeContext.I3SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�跽�˺�
        TradeContext.I3SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
        TradeContext.I3ACNM  =  'Ӧ����'                                    #�跽����
        TradeContext.I3RBAC  =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #�����˺�
        TradeContext.I3RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
        TradeContext.I3OTNM  =  '����������'                                  #��������
        TradeContext.I3TRAM  =  str(input_dict['CUSCHRG'])                    #������
        TradeContext.I3CTFG  = '8'
        TradeContext.I3PKFG  = 'T'
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�跽�˺�' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�����˺�' + TradeContext.I3RBAC )
    
    elif input_dict['CHRGTYP'] == '0':                                          #�ֽ�
        #=====����====
        TradeContext.ACUR    =  '2'                                           #���˴���
        TradeContext.RCCSMCD =  PL_RCCSMCD_CX                                 #ժҪ����
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  'ũ��������'                                  #�跽����
        TradeContext.RBAC    =  ''                                            #�����˺�
        TradeContext.OTNM    =  ''                                            #��������
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #���
        TradeContext.CTFG    = '7'
        TradeContext.PKFG    = 'T'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO  = ''
        TradeContext.CATR    =  '0'                                             #��ת��־
        
        #=====�����Ѽ��˸�ֵ====
        TradeContext.I2SMCD  =  PL_RCCSMCD_CX                                 #ժҪ����
        TradeContext.I2SBAC  =  ''                                            #�跽�˺�
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #�����˺�
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  '�����ѿ�Ŀ'                                  #��������
        TradeContext.I2TRAM  =  str(input_dict['CUSCHRG'])                    #���
        TradeContext.I2CTFG  =  '8'
        TradeContext.I2PKFG  =  'T'
        TradeContext.I2CATR  =  '0'                                           #��ת��־
    elif input_dict['CHRGTYP'] == '2':
        #=====���շ�====
        TradeContext.ACUR    =  '1'                                           #���˴���
        TradeContext.RCCSMCD =  PL_RCCSMCD_XJTDWZ                             #ժҪ����
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.RBAC    =  ''                                            #�����˺�
        TradeContext.OTNM    =  ''                                            #��������
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #���
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    =  'T'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO  = ''
        TradeContext.CATR    =  '0'                                             #��ת��־
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
        TradeContext.RCCSMCD =  input_dict['RCCSMCD']                         #ժҪ����
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  'Ӧ����'                                    #�跽����
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #�����˺�
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  '����������'                                  #��������
        TradeContext.OCCAMT  =  "-" + str(input_dict['CUSCHRG'])              #������
        TradeContext.CTFG    = '8'
        TradeContext.PKFG    = 'T'
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�跽�˺�' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�����˺�' + TradeContext.RBAC )
        #=========���׽��============
        TradeContext.I2RVFG  = '0'                                            #�����ֱ�־
        TradeContext.I2SMCD  =  input_dict['RCCSMCD']                         #ժҪ����
        TradeContext.I2SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�跽�˺�
        TradeContext.I2SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM  =  'Ӧ����'                                    #�跽����
        TradeContext.I2RBAC  =  ''                                            #�����˺�
        TradeContext.I2OTNM  =  ''                                            #��������
        TradeContext.I2TRAM  =  str(input_dict['OCCAMT'])                     #������
        TradeContext.I2CTFG  = '7'
        TradeContext.I2PKFG  = 'T'
        #TradeContext.I2WARNTNO = ''
        #TradeContext.I2CERTTYPE = ''
        #TradeContext.I2CERTNO = ''
        TradeContext.I2CATR  =  '0'                                           #��ת��־
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�跽�˺�' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�����˺�' + TradeContext.I2RBAC )
        #=========���׽��+������===================
        TradeContext.I3SMCD  =  input_dict['RCCSMCD']                         #ժҪ����
        TradeContext.I3SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
        TradeContext.I3SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
        TradeContext.I3ACNM  =  'ũ��������'                                  #�跽����
        TradeContext.I3RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
        TradeContext.I3RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
        TradeContext.I3OTNM  =  'Ӧ����'                                    #��������
        TradeContext.I3TRAM  =  "-" + str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #������
        TradeContext.I3PKFG  = 'T'
        TradeContext.I3CTFG  = '9'
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�跽�˺�' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�����˺�' + TradeContext.I3RBAC )
    
    elif input_dict['CHRGTYP'] == '0':                                        #�ֽ�
        #=====����====
        TradeContext.RVFG    =  '0'                                           #�����ֱ�־
        TradeContext.ACUR    =  '2'                                           #���˴���
        TradeContext.RCCSMCD =  input_dict['RCCSMCD']                         #ժҪ����
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  'ũ��������'                                  #�跽����
        TradeContext.RBAC    =  ''                                            #�����˺�
        TradeContext.OTNM    =  ''                                            #��������
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #���
        TradeContext.CTFG    = '7'
        TradeContext.PKFG    = 'T'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO  = ''
        TradeContext.CATR    =  '0'                                           #��ת��־
        
        #=====�����Ѽ��˸�ֵ====
        TradeContext.I2RVFG  =  '2'                                           #�����ֱ�־
        TradeContext.I2SMCD  =  input_dict['RCCSMCD']                         #ժҪ����
        TradeContext.I2SBAC  =  ''                                            #�跽�˺�
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #�����˺�
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  '�����ѿ�Ŀ'                                  #��������
        TradeContext.I2TRAM  =  str(input_dict['CUSCHRG'])                    #���
        TradeContext.I2CTFG  =  '8'
        TradeContext.I2PKFG  =  'T'
        TradeContext.I2CATR  =  '0'                                           #��ת��־
    elif input_dict['CHRGTYP'] == '2':
        #=====���շ�====
        TradeContext.RVFG    =  '0'                                           #�����ֱ�־
        TradeContext.ACUR    =  '1'                                           #���˴���
        TradeContext.RCCSMCD =  input_dict['RCCSMCD']                         #ժҪ����
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.RBAC    =  ''                                            #�����˺�
        TradeContext.OTNM    =  ''                                            #��������
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #���
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    =  'T'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO  = ''
        TradeContext.CATR    =  '0'                                             #��ת��־
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
        TradeContext.RCCSMCD =  PL_RCCSMCD_YZBWZ                              #ժҪ����  PL_RCCSMCD_YZBWZ ��ת��
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  'ũ��������'                                  #�跽����
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS           #�����˺�
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  'Ӧ����'                                    #��������
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #������
        TradeContext.PKFG    = 'T'
        TradeContext.CTFG    = '9'
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�跽�˺�' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�����˺�' + TradeContext.RBAC )
        #=========���׽��============
        TradeContext.I2SMCD  =  PL_RCCSMCD_YZBWZ                              #ժҪ����
        TradeContext.I2SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�跽�˺�
        TradeContext.I2SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM  =  'Ӧ����'                                    #�跽����
        TradeContext.I2RBAC  =  input_dict['PYEACC']                          #�����˺�
        TradeContext.I2OTNM  =  input_dict['PYENAM']                          #��������
        TradeContext.I2TRAM  =  str(input_dict['OCCAMT'])                     #������
        TradeContext.I2CTFG  = '7'
        TradeContext.I2PKFG  = 'T'
        TradeContext.I2WARNTNO = ''
        TradeContext.I2CERTTYPE = ''
        TradeContext.I2CERTNO = ''
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�跽�˺�' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�����˺�' + TradeContext.I2RBAC )
        #=========�������������뻧===========
        TradeContext.I3SMCD  =  PL_RCCSMCD_SXF                                #ժҪ����
        TradeContext.I3SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�跽�˺�
        TradeContext.I3SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
        TradeContext.I3ACNM  =  'Ӧ����'                                    #�跽����
        TradeContext.I3RBAC  =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #�����˺�
        TradeContext.I3RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
        TradeContext.I3OTNM  =  '����������'                                  #��������
        TradeContext.I3TRAM  =  str(input_dict['CUSCHRG'])                    #������
        TradeContext.I3CTFG  = '8'
        TradeContext.I3PKFG  = 'T'
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�跽�˺�' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�����˺�' + TradeContext.I3RBAC )

    elif input_dict['CHRGTYP'] == '0':
        #=====����====
        TradeContext.ACUR    =  '2'                                           #���˴���
        TradeContext.RCCSMCD =  PL_RCCSMCD_YZBWZ                              #ժҪ����
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
        TradeContext.SBAC    = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  'ũ��������'                                  #�跽����
        TradeContext.RBAC    =  input_dict['PYEACC']                          #�����˺�
        TradeContext.OTNM    =  input_dict['PYENAM']                          #��������
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #���
        TradeContext.CTFG  = '7'
        TradeContext.PKFG  = 'T'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
        
        #=====�����Ѽ��˸�ֵ====
        TradeContext.I2SMCD  =  PL_RCCSMCD_SXF                                #ժҪ����
        TradeContext.I2SBAC  =  ''                                            #�跽�˺�
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #�����˺�
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  '�����ѿ�Ŀ'                                  #��������
        TradeContext.I2TRAM  =  str(input_dict['CUSCHRG'])                    #���
        TradeContext.I2CTFG  =  '8'
        TradeContext.I2PKFG  =  'T'
        TradeContext.I2CATR  =  '0'                                           #��ת��־
    elif input_dict['CHRGTYP'] == '2':
        #=====���շ�====
        TradeContext.ACUR    =  '1'                                           #���˴���
        TradeContext.RCCSMCD =  PL_RCCSMCD_YZBWZ                              #ժҪ����
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.RBAC    =  input_dict['PYEACC']                          #�����˺�
        TradeContext.OTNM    =  input_dict['PYENAM']                          #��������
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #���
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    =  'T'
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
    
    if input_dict['CHRGTYP'] == '0':
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
        
        #=====����====
        TradeContext.ACUR    =  '2'                                           #���˴���
        TradeContext.RCCSMCD =  input_dict['RCCSMCD']                         #ժҪ����
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
        TradeContext.SBAC    = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  'ũ��������'                                  #�跽����
        TradeContext.RBAC    =  input_dict['PYEACC']                          #�����˺�
        TradeContext.OTNM    =  input_dict['PYENAM']                          #��������
        TradeContext.OCCAMT  =  "-" + str(input_dict['OCCAMT'])               #���
        TradeContext.CTFG    = '7'
        TradeContext.PKFG    = 'T'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
        
        #=====�����Ѽ��˸�ֵ====
        TradeContext.I2RVFG  = '2'                                            #�����ֱ�־ 2
        TradeContext.I2SMCD  =  input_dict['RCCSMCD']                         #ժҪ����
        TradeContext.I2SBAC  =  ''                                            #�跽�˺�
        TradeContext.I2SBNM  =  ''
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #�����˺�
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  '�����ѿ�Ŀ'                                  #��������
        TradeContext.I2TRAM  =  str(input_dict['CUSCHRG'])                    #���
        TradeContext.I2CTFG  =  '8'
        TradeContext.I2PKFG  =  'T'
        TradeContext.I2CATR  =  '0'                                           #��ת��־
    else:
        TradeContext.HostCode='8820'
        if not input_dict.has_key('FEDT'):
            return AfaFlowControl.ExitThisFlow("S999","ԭǰ�����ڲ���Ϊ��")
        if not input_dict.has_key('RBSQ'):
            return AfaFlowControl.ExitThisFlow("S999","ԭǰ����ˮ�Ų���Ϊ��")
            
        TradeContext.BOJEDT = input_dict['FEDT']
        TradeContext.BOSPSQ = input_dict['RBSQ']
    
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
       
    TradeContext.PKFG = 'T'                                             #ͨ��ͨ�ұ�ʶ
#    TradeContext.CATR = '0'                                             #��ת��ʶ:0-�ֽ�
    TradeContext.RCCSMCD  = PL_RCCSMCD_XJTCLZ                           #����ժҪ��:�ֽ�ͨ������    TradeContext.OCCAMT = str(input_dict['OCCAMT'])
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
      
    TradeContext.PKFG = 'T'                                         #ͨ��ͨ�ұ�ʶ
    
    TradeContext.OCCAMT = str(input_dict['OCCAMT'])                 #��Ʊ���
    TradeContext.RCCSMCD  = PL_RCCSMCD_BZYLZ                        #����ժҪ��:��ת������
    TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ       #�跽�˺�:ũ��������������
    TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
    TradeContext.ACNM = "ũ��������������"                          #�跽����
    TradeContext.RBAC = input_dict['PYEACC']                        #�����˺�:�տ����˻�
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
        TradeContext.I3SMCD =  PL_RCCSMCD_XJTDLZ                                 #ժҪ���� 
        TradeContext.I3SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�跽�˺�
        TradeContext.I3SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
        TradeContext.I3ACNM    =  'ũ����������ʱ��'                            #�跽����
        TradeContext.I3RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ         #�����˺�
        TradeContext.I3RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
        TradeContext.I3OTNM    =  'ũ��������'                                  #��������
        TradeContext.I3TRAM  =  str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #������
        TradeContext.I3PKFG    = 'T'                                            #ͨ��ͨ�ұ�ʾ
        TradeContext.I3CTFG    = '9'                                            #������ѧ�ѱ�ʾ
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�跽�˺�' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�����˺�' + TradeContext.I3RBAC )
        #=========���׽��============
        TradeContext.RCCSMCD =  PL_RCCSMCD_XJTDLZ                             #ժҪ����
        TradeContext.SBAC  =  input_dict['PYRACC']                          #�跽�˺�
        TradeContext.ACNM  =  input_dict['PYRNAM']                          #�跽����
        TradeContext.RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM  =  'ũ����������ʱ��'                            #��������
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #������
        TradeContext.CTFG  = '7'
        TradeContext.PKFG  = 'T'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO = ''
#        TradeContext.CATR  =  '0'                                           #��ת��־
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�跽�˺�' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�����˺�' + TradeContext.RBAC )
        #=========�������������뻧===========
        TradeContext.I2SMCD  =  PL_RCCSMCD_SXF                                #ժҪ����
        TradeContext.I2SBAC  =  input_dict['PYRACC']                          #�跽�˺�
        TradeContext.I2ACNM  =  input_dict['PYRNAM']                          #�跽����
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  'ũ����������ʱ��'                            #��������
        TradeContext.I2TRAM  =  str(input_dict['CUSCHRG'])                    #������
        TradeContext.I2CTFG  = '8'
        TradeContext.I2PKFG  = 'T'
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�跽�˺�' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�����˺�' + TradeContext.I2RBAC )
    
    elif input_dict['CHRGTYP'] == '0':                                          #�ֽ�
        #=====����====
        TradeContext.RCCSMCD =  PL_RCCSMCD_XJTDLZ                             #ժҪ����
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ         #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  'ũ��������������'                            #�跽����
        TradeContext.RBAC    =  input_dict['PYRACC']                          #�����˺�
        TradeContext.OTNM    =  input_dict['PYRNAM']                          #��������
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #���
        TradeContext.CTFG    = '7'
        TradeContext.PKFG    = 'T'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO  = ''
#        TradeContext.CATR    =  '0'                                             #��ת��־
        
    elif input_dict['CHRGTYP'] == '2':
        #=====���շ�====
        TradeContext.ACUR    =  '1'                                           #���˴���
        TradeContext.RCCSMCD =  PL_RCCSMCD_XJTDLZ                             #ժҪ����
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ         #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  'ũ��������������'                            #�跽����
        TradeContext.RBAC    =  input_dict['PYRACC']                          #�����˺�
        TradeContext.OTNM    =  input_dict['PYRNAM']                          #��������
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #���
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    =  'T'
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
        TradeContext.I3RCCSMCD =  PL_RCCSMCD_YZBWZ                                  #ժҪ����  PL_RCCSMCD_YZBWZ ��ת��
        TradeContext.I3SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS              #�跽�˺�
        TradeContext.I3SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)        
        TradeContext.I3ACNM    =  'ũ����������ʱ��'                                #�跽����
        TradeContext.I3RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ             #�����˺�
        TradeContext.I3RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)        
        TradeContext.I3OTNM    =  'ũ��������������'                                #��������
        TradeContext.I3TRAM  =  str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #������
        TradeContext.I3PKFG    = 'T'
        TradeContext.I3CTFG    = '9'
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�跽�˺�' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�����˺�' + TradeContext.I3RBAC )
        #=========���׽��============
        TradeContext.RCCSMCD  =  PL_RCCSMCD_YZBWZ                              #ժҪ����
        TradeContext.SBAC  =  input_dict['PYRACC']                          #�跽�˺�
        TradeContext.ACNM  =  input_dict['PYRNAM']                          #�跽����
        TradeContext.RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
        TradeContext.RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM  =  'ũ����������ʱ��'                            #��������
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #������
        TradeContext.CTFG  = '7'
        TradeContext.PKFG  = 'T'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�跽�˺�' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�����˺�' + TradeContext.RBAC )
        #=========�������������뻧===========
        TradeContext.I2SMCD  =  PL_RCCSMCD_SXF                                #ժҪ����
        TradeContext.I2SBAC  =  input_dict['PYRACC']          #�跽�˺�
        TradeContext.I2ACNM  =  input_dict['PYRNAM']                                    #�跽����
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  'ũ����������ʱ��'                                  #��������
        TradeContext.I2TRAM  =  str(input_dict['CUSCHRG'])                    #������
        TradeContext.I2CTFG  = '8'
        TradeContext.I2PKFG  = 'T'
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�跽�˺�' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�����˺�' + TradeContext.I2RBAC )

    elif input_dict['CHRGTYP'] == '0':
        #=====����====
        TradeContext.ACUR    =  '1'                                           #���˴���
        TradeContext.RCCSMCD =  PL_RCCSMCD_YZBWZ                              #ժҪ����
        TradeContext.SBAC    =  input_dict['PYRACC']                          #�跽�˺�
        TradeContext.ACNM    =  input_dict['PYRNAM']                          #�跽����
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ          #�����˺�
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  'ũ����������ʱ��'                            #��������
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #���
        TradeContext.CTFG  = '7'
        TradeContext.PKFG  = 'T'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
        
    elif input_dict['CHRGTYP'] == '2':
        #=====���շ�====
        TradeContext.ACUR    =  '1'                                           #���˴���
        TradeContext.RCCSMCD =  PL_RCCSMCD_YZBWZ                              #ժҪ����
        TradeContext.SBAC    =  input_dict['PYRACC']                          #�跽�˺�
        TradeContext.ACNM    =  input_dict['PYRNAM']                          #�跽����
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ          #�����˺�
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  'ũ����������ʱ��'                            #��������
        TradeContext.OCCAMT  =  str(input_dict['OCCAMT'])                     #���
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    =  'T'
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
#    TradeContext.CATR = '0'                                             #��ת��ʶ:0-�ֽ�
    TradeContext.RCCSMCD  = input_dict['RCCSMCD']                           #����ժҪ��:�ֽ�ͨ������    TradeContext.OCCAMT = str(input_dict['OCCAMT'])
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
    TradeContext.RCCSMCD  = input_dict['RCCSMCD']                        #����ժҪ��:��ת������
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
        
    TradeContext.CTFG = '7'                                             #������ѧ�ѱ�ʾ
    
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
        TradeContext.I3SMCD =  input_dict['RCCSMCD']                                 #ժҪ���� 
        TradeContext.I3SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�跽�˺�
        TradeContext.I3SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
        TradeContext.I3ACNM    =  'ũ����������ʱ��'                            #�跽����
        TradeContext.I3RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ         #�����˺�
        TradeContext.I3RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
        TradeContext.I3OTNM    =  'ũ��������'                                  #��������
        TradeContext.I3TRAM    = "-" + str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #������
        TradeContext.I3PKFG    = 'T'                                            #ͨ��ͨ�ұ�ʾ
        TradeContext.I3CTFG    = '9'                                            #������ѧ�ѱ�ʾ
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�跽�˺�' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�����˺�' + TradeContext.I3RBAC )
        #=========���׽��============
        TradeContext.RCCSMCD =  input_dict['RCCSMCD']                             #ժҪ����
        TradeContext.SBAC  =  input_dict['PYRACC']                          #�跽�˺�
        TradeContext.ACNM  =  input_dict['PYRNAM']                          #�跽����
        TradeContext.RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM  =  'ũ����������ʱ��'                            #��������
        TradeContext.OCCAMT  =  "-" + str(input_dict['OCCAMT'])                     #������
        TradeContext.CTFG  = '7'
        TradeContext.PKFG  = 'T'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO = ''
#        TradeContext.CATR  =  '0'                                           #��ת��־
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�跽�˺�' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�����˺�' + TradeContext.RBAC )
        #=========�������������뻧===========
        TradeContext.I2SMCD  =  input_dict['RCCSMCD']                                #ժҪ����
        TradeContext.I2SBAC  =  input_dict['PYRACC']                          #�跽�˺�
        TradeContext.I2ACNM  =  input_dict['PYRNAM']                          #�跽����
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  'ũ����������ʱ��'                            #��������
        TradeContext.I2TRAM  =  "-" + str(input_dict['CUSCHRG'])                    #������
        TradeContext.I2CTFG  = '8'
        TradeContext.I2PKFG  = 'T'
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�跽�˺�' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�����˺�' + TradeContext.I2RBAC )
    
    elif input_dict['CHRGTYP'] == '0':                                          #�ֽ�
        #=====����====
        TradeContext.RCCSMCD =  input_dict['RCCSMCD']                             #ժҪ����
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ         #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  'ũ��������������'                            #�跽����
        TradeContext.RBAC    =  input_dict['PYRACC']                          #�����˺�
        TradeContext.OTNM    =  input_dict['PYRNAM']                          #��������
        TradeContext.OCCAMT  =  "-" + str(input_dict['OCCAMT'])                     #���
        TradeContext.CTFG    = '7'
        TradeContext.PKFG    = 'T'
        #TradeContext.WARNTNO = ''
        #TradeContext.CERTTYPE = ''
        #TradeContext.CERTNO  = ''
#        TradeContext.CATR    =  '0'                                             #��ת��־
        
    elif input_dict['CHRGTYP'] == '2':
        #=====���շ�====
        TradeContext.ACUR    =  '1'                                           #Ĩ�˴���
        TradeContext.RCCSMCD =  input_dict['RCCSMCD']                             #ժҪ����
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ         #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  'ũ��������������'                            #�跽����
        TradeContext.RBAC    =  input_dict['PYRACC']                          #�����˺�
        TradeContext.OTNM    =  input_dict['PYRNAM']                          #��������
        TradeContext.OCCAMT  =  "-" + str(input_dict['OCCAMT'])                     #���
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    =  'T'
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
        TradeContext.I3RCCSMCD =  input_dict['RCCSMCD']                                  #ժҪ����  PL_RCCSMCD_YZBWZ ��ת��
        TradeContext.I3SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS              #�跽�˺�
        TradeContext.I3SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)        
        TradeContext.I3ACNM    =  'ũ����������ʱ��'                                #�跽����
        TradeContext.I3RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ             #�����˺�
        TradeContext.I3RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)        
        TradeContext.I3OTNM    =  'ũ��������������'                                #��������
        TradeContext.I3TRAM    = "-" + str(input_dict['OCCAMT'] + input_dict['CUSCHRG']) #������
        TradeContext.I3PKFG    = 'T'
        TradeContext.I3CTFG    = '9'
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�跽�˺�' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�����˺�' + TradeContext.I3RBAC )
        #=========���׽��============
        TradeContext.RCCSMCD  =  input_dict['RCCSMCD']                              #ժҪ����
        TradeContext.SBAC  =  input_dict['PYRACC']                          #�跽�˺�
        TradeContext.ACNM  =  input_dict['PYRNAM']                          #�跽����
        TradeContext.RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
        TradeContext.RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM  =  'ũ����������ʱ��'                            #��������
        TradeContext.OCCAMT  = "-" + str(input_dict['OCCAMT'])                     #������
        TradeContext.CTFG  = '7'
        TradeContext.PKFG  = 'T'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�跽�˺�' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�����˺�' + TradeContext.RBAC )
        #=========�������������뻧===========
        TradeContext.I2SMCD  =  input_dict['RCCSMCD']                                #ժҪ����
        TradeContext.I2SBAC  =  input_dict['PYRACC']          #�跽�˺�
        TradeContext.I2ACNM  =  input_dict['PYRNAM']                                    #�跽����
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  'ũ����������ʱ��'                                  #��������
        TradeContext.I2TRAM  =  "-" + str(input_dict['CUSCHRG'])                    #������
        TradeContext.I2CTFG  = '8'
        TradeContext.I2PKFG  = 'T'
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�跽�˺�' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�����˺�' + TradeContext.I2RBAC )

    elif input_dict['CHRGTYP'] == '0':
        #=====����====
        TradeContext.ACUR    =  '1'                                           #Ĩ�˴���
        TradeContext.RCCSMCD =  input_dict['RCCSMCD']                              #ժҪ����
        TradeContext.SBAC    =  input_dict['PYRACC']                          #�跽�˺�
        TradeContext.ACNM    =  input_dict['PYRNAM']                          #�跽����
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ          #�����˺�
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  'ũ����������ʱ��'                            #��������
        TradeContext.OCCAMT  =  "-" + str(input_dict['OCCAMT'])                     #���
        TradeContext.CTFG  = '7'
        TradeContext.PKFG  = 'T'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
        
    elif input_dict['CHRGTYP'] == '2':
        #=====���շ�====
        TradeContext.ACUR    =  '1'                                           #Ĩ�˴���
        TradeContext.RCCSMCD =  input_dict['RCCSMCD']                              #ժҪ����
        TradeContext.SBAC    =  input_dict['PYRACC']                          #�跽�˺�
        TradeContext.ACNM    =  input_dict['PYRNAM']                          #�跽����
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ          #�����˺�
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  'ũ����������ʱ��'                            #��������
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