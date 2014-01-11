# -*- coding: gbk -*-
##################################################################
#   ũ����.ͨ��ͨ�����˽��ս���.�� ����ѯ
#=================================================================
#   �����ļ�:   TRCC005_1134.py
#   �޸�ʱ��:   2008-10-21
#   ���ߣ�      �˹�ͨ
##################################################################

import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaAfeFunc,HostContext
import AfaFunc,rccpsDBFunc
import AfaDBFunc,rccpsState,rccpsGetFunc,rccpsHostFunc
import rccpsDBTrcc_balbka
from types import *
from rccpsConst import *
import jiami

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("'***ũ����ϵͳ��ͨ��ͨ�����˽��ս���.��  ����ѯ[1134] ����")
    
    AfaLoggerFunc.tradeInfo("����ǰ����(�Ǽ���ˮ,����ǰ����)")
    
    AfaLoggerFunc.tradeInfo("TradeContext.BNKBKNO<<<<<<<<<<<"+TradeContext.BNKBKNO)
    
    #=====�ж��Ƿ�����ظ�����====
    AfaLoggerFunc.tradeInfo("�ж��Ƿ�����ظ�����")
    balbka_dict = {'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO,'SNDBNKCO':TradeContext.SNDBNKCO}
    record_balbka = rccpsDBTrcc_balbka.selectu(balbka_dict)
    if( record_balbka == None ):
        return AfaFlowControl.ExitThisFlow('A009','�ж��ظ�����ʱ��ѯ���Ǽǲ�ʧ��')
        
    if( len(record_balbka) > 0 ):  
        AfaLoggerFunc.tradeInfo("�����ظ�����")
        
        #====��֯Ӧ����====
        Rcvmbrco = TradeContext.SNDMBRCO
        Sndmbrco = TradeContext.RCVMBRCO
        Ormfn    = TradeContext.MSGFLGNO
                
        #=====����ͷ====
        TradeContext.MSGTYPCO = 'SET010' #���������
        TradeContext.RCVSTLBIN = Rcvmbrco #���ܷ���Ա�к�
        TradeContext.SNDSTLBIN = Sndmbrco #���ͷ���Ա�к�
        TradeContext.SNDBRHCO = TradeContext.BESBNO         #�����������
        TradeContext.SNDCLKNO = TradeContext.BETELR         #�����й�Ա��
        TradeContext.SNDTRDAT = TradeContext.BJEDTE         #�����н�������
        TradeContext.SNDTRTIM = TradeContext.BJETIM         #�����н���ʱ��
        TradeContext.MSGFLGNO = Rcvmbrco+TradeContext.BJEDTE + TradeContext.SerialNo  #���ı�ʾ��
        TradeContext.ORMFN    = Ormfn          #�ο����ı�ʾ��
        TradeContext.NCCWKDAT = TradeContext.NCCworkDate   #���Ĺ�������
        TradeContext.OPRTYPNO = '30'     #ҵ������
        TradeContext.ROPRTPNO = '30'     #�ο�ҵ������
        TradeContext.TRANTYP  = '0'      #��������
        #=====ҵ��Ҫ�ؼ�====
        TradeContext.CURPIN   = "" #��ؿͻ�����   
        TradeContext.PRCCO    = "RCCS1105"  #������
        TradeContext.STRINFO  = "�ظ�����"  #����     
        TradeContext.AVLBAL   = record_balbka['AVLBAL'] #�������
        TradeContext.ACCBAL   = record_balbka['ACCBAL'] #�������
        TradeContext.BNKBKNO  = record_balbka['BNKBKNO'] #���ۺ���
        
        #=====ֱ����AFE����ͨѶ��ִ====
        AfaLoggerFunc.tradeInfo("ֱ����AFE����ͨѶ��ִ")
        AfaAfeFunc.CommAfe()
        
        AfaLoggerFunc.tradeInfo("�ظ����ģ�����������")
        
        return AfaFlowControl.ExitThisFlow('A009','�ظ���������������')
        
##########���ظ�����############################################    
    AfaLoggerFunc.tradeInfo("���ظ�����")
    
    #=====��֯�Ǽ�����ѯ��ѯ�Ǽǲ��Ĳ����ֵ�====
    AfaLoggerFunc.tradeInfo("��֯�Ǽ�����ѯ��ѯ�Ǽǲ��Ĳ����ֵ�")
    insert_dict = {}
    insert_dict['BJEDTE']      = TradeContext.BJEDTE
    insert_dict['BSPSQN']      = TradeContext.BSPSQN
    insert_dict['BRSFLG']      = PL_BRSFLG_RCV
    insert_dict['BESBNO']      = TradeContext.BESBNO 
    insert_dict['BEACSB']      = ""                    #���������
    insert_dict['BETELR']      = TradeContext.BETELR 
    insert_dict['BEAUUS']      = ""                    #��Ȩ��Ա��
    insert_dict['BEAUPS']      = ""                    #��Ȩ��Ա����
    insert_dict['TERMID']      = ""                    #�ն˺�
    insert_dict['OPRNO']       = TradeContext.OPRTYPNO #ҵ������
    insert_dict['OPRATTNO']    = ""                    #ҵ������
    insert_dict['NCCWKDAT']    = TradeContext.NCCWKDAT #���Ĺ�������
    insert_dict['TRCCO']       = TradeContext.TRCCO    #���״���
    insert_dict['TRCDAT']      = TradeContext.TRCDAT   #ί������
    insert_dict['TRCNO']       = TradeContext.TRCNO    #������ˮ��
    insert_dict['MSGFLGNO']    = TradeContext.MSGFLGNO #���ı�ʾ��
    insert_dict['SNDMBRCO']    = TradeContext.SNDMBRCO #���ͷ���Ա�к�
    insert_dict['RCVMBRCO']    = TradeContext.RCVMBRCO #���ܷ���Ա�к�
    insert_dict['SNDBNKCO']    = TradeContext.SNDBNKCO #���ͷ��к�
    insert_dict['SNDBNKNM']    = TradeContext.SNDBNKNM #���ͷ�����
    insert_dict['RCVBNKCO']    = TradeContext.RCVBNKCO #���ܷ��к�
    insert_dict['RCVBNKNM']    = TradeContext.RCVBNKNM #���ܷ�����
    insert_dict['CUR']         = '01'                  #����
    insert_dict['CHRGTYP']     = ""                    #��������ȡ��ʽ
    insert_dict['LOCCUSCHRG']  = ""                    #���ؿͻ�������
    insert_dict['CUSCHRG']     = TradeContext.CUSCHRG  #��ؿͻ�������
    insert_dict['PYRACC']      = TradeContext.PYRACC   #�������˺�
    insert_dict['PYEACC']      = TradeContext.PYEACC   #�տ����˺�
    insert_dict['STRINFO']     = TradeContext.STRINFO  #����
    insert_dict['CERTTYPE']    = ""                    #֤������
    insert_dict['CERTNO']      = ""                    #֤������
    insert_dict['BNKBKNO']     = TradeContext.BNKBKNO  #���ۺ���
    insert_dict['AVLBAL']      = ""                    #�������
    insert_dict['ACCBAL']      = ""                    #�������
    insert_dict['PRCCO']       = ""                    #������
    #insert_dict['PRCINFO']     = ""                    #������Ϣ
    
    #=====�Ǽǲ�ѯ�Ǽǲ�====
    AfaLoggerFunc.tradeInfo("�Ǽǲ�ѯ�Ǽǲ�")
    res = rccpsDBTrcc_balbka.insertCmt(insert_dict)
    if( res == -1 ):
        return AfaFlowControl.ExitThisFlow('A009','�Ǽ�����ѯ�Ǽǲ�ʧ��')
        
    #���ܿͻ�����
    MIMA = '      '
    PIN  = TradeContext.CURPIN
    ACC  = TradeContext.PYEACC
    AfaLoggerFunc.tradeDebug('����[' + PIN + ']')
    AfaLoggerFunc.tradeDebug('�˺�[' + ACC + ']')
    ret = jiami.secDecryptPin(PIN,ACC,MIMA)
    if ret != 0:
        AfaLoggerFunc.tradeDebug("ret=[" + str(ret) + "]")
        AfaLoggerFunc.tradeDebug('���ü��ܷ�����ʧ��')
    else:
        TradeContext.CURPIN = MIMA
        AfaLoggerFunc.tradeDebug('����new[' + TradeContext.CURPIN + ']')
        
    #=====�����������ף���֯����������������Ҫ�Ĳ���====
    AfaLoggerFunc.tradeInfo("Ϊ�������׸�����")
    TradeContext.HostCode = '8810'
    TradeContext.ACCNO = TradeContext.PYEACC
    TradeContext.PASSWD = TradeContext.CURPIN
    TradeContext.CFFG = '1'
    TradeContext.WARNTNO = '49' + TradeContext.BNKBKNO
          
    AfaLoggerFunc.tradeInfo("����ǰ����(�Ǽ���ˮ,����ǰ����) ����")
    
    return True
    
                                 
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo("�����д���(�޸���ˮ,��������,����ǰ����)")
    
    AfaLoggerFunc.tradeInfo("TradeContext.errorCode<<<<<" + TradeContext.errorCode)
    
    #=====�ж������������жϽ����Ƿ�����====
    if( TradeContext.errorCode != '0000' ):
        AfaLoggerFunc.tradeInfo("������������ʧ��")
        #=====��������ȸ�ֵ====
        TradeContext.PRCCO = "NN1CA999"
        TradeContext.STRINFO  = "����ʧ�� "+TradeContext.errorMsg[7:]+" "  #���� 
        TradeContext.AVLBAL   = "0.00" #�������
        TradeContext.ACCBAL   = "0.00" #�������
        
        #=====��������ѯ�Ǽǲ�====
        AfaLoggerFunc.tradeInfo("��֯�����ֵ�")
        where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}
        update_dict = {'STRINFO':TradeContext.STRINFO,'PRCCO':TradeContext.PRCCO}
            
        AfaLoggerFunc.tradeInfo("��ʼ��������ѯ�Ǽǲ�")
        res = rccpsDBTrcc_balbka.updateCmt(update_dict,where_dict)
        
        if( res == -1 ):
            return AfaFlowControl.ExitThisFlow('A009','��������ѯ�Ǽǲ�ʧ��')
            
    else:
        AfaLoggerFunc.tradeInfo("�����������׳ɹ�")
        TradeContext.PRCCO = "RCCI0000"  #������
        TradeContext.STRINFO = "��ѯ�ɹ�"  #����
        TradeContext.ACCBAL = HostContext.O1ACBL #�ʻ����
        TradeContext.AVLBAL = HostContext.O1CUBL #�������
        
        ##=====�ж��Ƿ���ͬ���˻���====
        #if( TradeContext.BESBNO != PL_BESBNO_BCLRSB ):
        #    if( TradeContext.BESBNO[:6] != TradeContext.ACCSO[:6] ):
        #        AfaLoggerFunc.tradeInfo(">>>����編�����˽���")
        #        TradeContext.PRCCO = 'NN1IO999'
        #        TradeContext.STRINFO = "���������˻������в�����ͬһ����"
        #        TradeContext.ACCBAL = '0.00' #�ʻ����
        #        TradeContext.AVLBAL = '0.00' #�������
                
        #=====�жϿ�����������ͨ��ͨ��Ȩ��====
        if not rccpsDBFunc.chkTDBESAuth(TradeContext.ACCSO):
            AfaLoggerFunc.tradeInfo(">>>���˻�����������ͨ��ͨ��ҵ��Ȩ��")
            TradeContext.PRCCO = 'NN1IO999'
            TradeContext.STRINFO = "���˻�����������ͨ��ͨ��ҵ��Ȩ��"
            TradeContext.ACCBAL = '0.00'  #�ʻ����
            TradeContext.AVLBAL = '0.00'  #�������
        
        #=====�ж��˺��뻧���Ƿ����====
        if(TradeContext.PYENAM != HostContext.O1CUNM):
            TradeContext.PRCCO   = 'NN1IA102'
            TradeContext.STRINFO = "�������˺Ų���"
            TradeContext.ACCBAL = '0.00' #�ʻ����
            TradeContext.AVLBAL = '0.00' #�������
        
        #=====�ж��˻���״̬====
        AfaLoggerFunc.tradeInfo("�ж��˻���״̬")
        if( TradeContext.ACCST != "0" ):
            TradeContext.PRCCO = 'NN1IA999'
            TradeContext.STRINFO = "�˻�״̬������"
            TradeContext.ACCBAL = '0.00' #�ʻ����
            TradeContext.AVLBAL = '0.00' #�������
            
        #=====�ж��Ƿ�Ϊ���˽����˻�====
        if not (TradeContext.ACCCD == '0428' and TradeContext.ACCEM == '21111'):
            AfaLoggerFunc.tradeInfo(">>>���˻��Ǹ��˽��㻧")
            TradeContext.PRCCO    = 'NN1IA999'
            TradeContext.STRINFO  = '���˻��Ǹ��˽��㻧'
            TradeContext.ACCBAL = '0.00' #�ʻ����
            TradeContext.AVLBAL = '0.00' #�������
        
        #=====��������ѯ�Ǽǲ�====
        AfaLoggerFunc.tradeInfo("��֯�����ֵ�")
        where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}
        update_dict = {'AVLBAL':TradeContext.AVLBAL,'ACCBAL':TradeContext.ACCBAL,\
                       'STRINFO':TradeContext.STRINFO,'PRCCO':TradeContext.PRCCO}
         
        AfaLoggerFunc.tradeInfo("��ʼ��������ѯ�Ǽǲ�")
        res = rccpsDBTrcc_balbka.updateCmt(update_dict,where_dict)
        
        if( res == -1 ):
            return AfaFlowControl.ExitThisFlow('A009','��������ѯ�Ǽǲ�ʧ��')
     
    #=====��֯Ӧ����====
    AfaLoggerFunc.tradeInfo("��֯Ӧ����") 
    Rcvmbrco = TradeContext.SNDMBRCO
    Sndmbrco = TradeContext.RCVMBRCO
    Ormfn    = TradeContext.MSGFLGNO
            
    #=====����ͷ====
    TradeContext.MSGTYPCO = 'SET010' #���������
    TradeContext.RCVSTLBIN = Rcvmbrco #���ܷ���Ա�к�
    TradeContext.SNDSTLBIN = Sndmbrco #���ͷ���Ա�к�
    TradeContext.SNDBRHCO = TradeContext.BESBNO         #�����������
    TradeContext.SNDCLKNO = TradeContext.BETELR         #�����й�Ա��
    TradeContext.SNDTRDAT = TradeContext.BJEDTE         #�����н�������
    TradeContext.SNDTRTIM = TradeContext.BJETIM         #�����н���ʱ��
    TradeContext.MSGFLGNO = Rcvmbrco+TradeContext.BJEDTE + TradeContext.SerialNo  #���ı�ʾ��
    TradeContext.ORMFN    = Ormfn          #�ο����ı�ʾ��
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate   #���Ĺ�������
    TradeContext.OPRTYPNO = '30'     #ҵ������
    TradeContext.ROPRTPNO = '30'     #�ο�ҵ������
    TradeContext.TRANTYP  = '0'      #��������
    #=====ҵ��Ҫ�ؼ�====
    TradeContext.CURPIN   = "" #��ؿͻ�����   
#    TradeContext.PRCCO    =   #������
#    TradeContext.STRINFO  =   #����     
#    TradeContext.TRCCO =  "3000502"
#    TradeContext.SNDBNKCO =  #�������к�
#    TradeContext.SNDBNKNM =  #����������
#    TradeContext.RCVBNKCO =  #�������к�
#    TradeContext.RCVBNKNM =  #����������
#    TradeContext.TRCDAT =  #ί������ 
#    TradeContext.TRCNO =  #������ˮ��
#    TradeContext.ORTRCCO =  #ԭ���״���
#    TradeContext.ORTRCNO =  #ԭ������ˮ��
#    TradeContext.CUR =  #���ҷ���
#    TradeContext.OCCAMT =  #������
#    TradeContext.CUSCHRG =  #��ؿͻ�������
#    TradeContext.PYRACC =  #�������˺�
#    TradeContext.PYEACC =  #�տ����˺�
    #=====��չ����====
#    TradeContext.PYENAM = #�տ�������
#    TradeContext.AVLBAL   =  #�������
#    TradeContext.ACCBAL   =  #�������
#    TradeContext.BNKBKNO =
    
    AfaLoggerFunc.tradeInfo("TradeContext.AVLBAL<<<<<<" + TradeContext.AVLBAL)
    AfaLoggerFunc.tradeInfo("TradeContext.ACCBAL<<<<<<" + TradeContext.ACCBAL)
                                      
    AfaLoggerFunc.tradeInfo("�����д���(�޸���ˮ,��������,����ǰ����) ����")
        
    return True
     
def SubModuleDoTrd():
    AfaLoggerFunc.tradeInfo("���׺���")
    
    #=====�ж�afe���ؽ��====
    if TradeContext.errorCode == '0000':
        AfaLoggerFunc.tradeInfo('>>>���ͳɹ�')
    else:
        AfaLoggerFunc.tradeInfo('>>>����ʧ��')
        
    AfaLoggerFunc.tradeInfo("TradeContext.BNKBKNO<<<<<<<<<<<"+TradeContext.BNKBKNO)

    AfaLoggerFunc.tradeInfo("���׺��� ����")
    
    AfaLoggerFunc.tradeInfo("'***ũ����ϵͳ��ͨ��ͨ�����˽��ս���.�� ����ѯ[1134] �˳�")
    
    return True  
