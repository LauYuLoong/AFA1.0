#  --*--coding: gbk --*--
##################################################################
#   ũ����ϵͳ.����ģ��
#=================================================================
#   �����ļ�:   rccpsConst.py
#   ��    ��:   �ر��
#   �޸�ʱ��:   2008-06-10
##################################################################

PL_BJEDTE         = '20080409'

PL_RCV_CENTER     = '1000000000' #ũ������������
PL_RCV_CENNAM     = 'ũ������������'

PL_BESBNO_BCLRSB  = '3400008889' #ʡ�������Ļ�����
PL_BETELR_AUTO    = '999996'     #�Զ���Ա

PL_BCSTAT_INIT    = '00'    #��ʼ
PL_BCSTAT_SND     = '10'    #����
PL_BCSTAT_ACC     = '20'    #����
PL_BCSTAT_HCAC    = '21'    #Ĩ��
PL_BCSTAT_MFERCV  = '30'    #MFE����
PL_BCSTAT_CONFPAY = '31'    #ȷ�ϸ���
PL_BCSTAT_MFERFE  = '40'    #�ܾ�
PL_BCSTAT_MFEQUE  = '41'    #�Ŷ�
PL_BCSTAT_MFESTL  = '42'    #����
PL_BCSTAT_CAC     = '50'    #����
PL_BCSTAT_BNKRCV  = '60'    #��������
PL_BCSTAT_CONFACC = '61'    #ȷ������
PL_BCSTAT_AUTO    = '70'    #�Զ�����
PL_BCSTAT_HANG    = '71'    #�Զ�����
PL_BCSTAT_AUTOPAY = '72'    #�Զ��ۿ�
PL_BCSTAT_QTR     = '80'    #�˻�
PL_BCSTAT_CANC    = '81'    #����

#=====������ 20081129 �����Զ�����״̬====
PL_BCSTAT_CANCEL  = '82'    #����
#=====�ر�� 20081225 �����ֹ���ת״̬====
PL_BCSTAT_TRAS    = '43'    #�ֹ���ת

#PL_BCSTAT_EMERG  = '90'    #����ֹ��
PL_BCSTAT_LONG    = '91'    #����
PL_BCSTAT_SHORT   = '92'    #�̿�
PL_BCSTAT_DEL     = '93'    #ɾ��

PL_BDWFLG_SUCC    = '1'     #�ɹ�
PL_BDWFLG_FAIL    = '2'     #ʧ��
PL_BDWFLG_WAIT    = '9'     #������

PL_ISDEAL_UNDO    = '0'     #δ�����δ����
PL_ISDEAL_ISDO    = '1'     #�Ѵ�����Ѳ鸴

PL_BRSFLG_SND     = '0'     #����
PL_BRSFLG_RCV     = '1'     #����

PL_MBRTRCST_RCV   = '20'    #��������
PL_MBRTRCST_ACSUC = '21'    #���˳ɹ�
PL_MBRTRCST_ACFAL = '22'    #����ʧ��
PL_MBRTRCST_CNF   = '23'    #��ȷ��
PL_MBRTRCST_CURE  = '24'    #�ѳ���
PL_MBRTRCST_RUSH  = '25'    #�ѳ���
PL_MBRTRCST_REPR  = '26'    #�Ѳ���
PL_MBRTRCST_UNRCV = '27'    #δ�յ�

PL_TRCCO_HD       = '20'    #���
PL_TRCCO_HP       = '21'    #��Ʊ
PL_TRCCO_TCTD     = '30'    #ͨ��ͨ��
PL_TRCCO_QT       = '99'    #����

PL_SEAL_ENC       = 0       #����Ѻ
PL_SEAL_DEC       = 1       #����Ѻ

PL_TYPE_XJHP      = '1'     #�ֽ��Ʊ
PL_TYPE_ZZHP      = '2'     #ת�˻�Ʊ
PL_TYPE_DZHD      = '3'     #�ֽ���

PL_SUBFLG_SUB     = '0'     #������
PL_SUBFLG_AGE     = '1'     #����

PL_DCFLG_DEB      = '1'     #��
PL_DCFLG_CRE      = '2'     #��

PL_BILRS_INN      = '0'     #����ǩ���Ļ�Ʊ
PL_BILRS_OUT      = '1'     #����ǩ���Ļ�Ʊ

PL_HPSTAT_SIGN    = '01'    #ǩ��
PL_HPSTAT_PAYC    = '02'    #�⸶
PL_HPSTAT_CANC    = '03'    #����
PL_HPSTAT_HANG    = '04'    #��ʧ
PL_HPSTAT_RETN    = '05'    #��Ʊ
PL_HPSTAT_DEHG    = '06'    #���
PL_HPSTAT_CLER    = '07'    #����

PL_BILTYP_CASH    = '0'     #�ֽ��Ʊ
PL_BILTYP_TRAN    = '1'     #ת�˻�Ʊ

PL_PAYWAY_CASH    = '0'     #�ֽ�
PL_PAYWAY_TRAN    = '1'     #���ֽ�

#����ժҪ����
PL_RCCSMCD_HPQF   = '610'   #��Ʊǩ��
PL_RCCSMCD_HPJF   = '611'   #��Ʊ�⸶
PL_RCCSMCD_HPCX   = '612'   #��Ʊ����
PL_RCCSMCD_HPTK   = '613'   #��Ʊ�˿�
PL_RCCSMCD_WCX    = '614'   #������
PL_RCCSMCD_JJZF   = '615'   #����ֹ��
PL_RCCSMCD_WCH    = '616'   #�����
PL_RCCSMCD_LTH    = '617'   #���˻�
PL_RCCSMCD_HDWZ   = '618'   #�������
PL_RCCSMCD_HDLZ   = '619'   #�������
PL_RCCSMCD_HPLZ   = '620'   #��Ʊ����
#ͨ��ͨ�����
PL_RCCSMCD_SXF    = '015'   #������
PL_RCCSMCD_XJTCWZ = '630'   #�ֽ�ͨ������
PL_RCCSMCD_XJTDWZ = '631'   #�ֽ�ͨ������
PL_RCCSMCD_XJTCLZ = '621'   #�ֽ�ͨ������
PL_RCCSMCD_XJTDLZ = '622'   #�ֽ�ͨ������
PL_RCCSMCD_BZYWZ  = '623'   #�����˻�ת�������
PL_RCCSMCD_YZBWZ  = '624'   #����˻�ת��������
PL_RCCSMCD_BZYLZ  = '626'   #�����˻�ת�������
PL_RCCSMCD_YZBLZ  = '627'   #����˻�ת��������
PL_RCCSMCD_CX     = '625'   #����
PL_RCCSMCD_CZ     = 'ADJ'   #����
PL_RCCSMCD_DZMZ   = '628'   #���˺�Ĩ��
PL_RCCSMCD_DZBJ   = '629'   #���˺󲹼���


#=====������  20080626 �˺�ǰ��ӱ��ִ��룺01====
PL_ACC_NXYDQSWZ   = '01065100000005'   #ũ��������������
PL_ACC_NXYDQSLZ   = '01065600000005'   #ũ��������������
PL_ACC_NXYDJLS    = '01060300000003'   #ũ����������ʱ����
PL_ACC_NXYDXZ     = '01053700000007'   #ũ����������
PL_ACC_HCHK       = '01053800000001'   #������
#=====������  20080911 ����2621��Ŀ====
PL_ACC_DYKJQ      = '01061200000001'   #�����
#=====�ر��  20081023 ����5111�����ѿ�Ŀ
PL_ACC_TCTDSXF    = '01082000000006'   #ͨ��ͨ��������
#=====�ź�    20091109 ����0651�����ѿ�Ŀ
PL_ACC_HDSXF      = '01082000000002'   #���������
#=====�ر��  20081217  ����1391����Ӧ�տ��Ŀ=====
PL_ACC_QTYSK      = '01032100000013'   #����Ӧ�տ�
#=====�ر��  20081217  ����2621����Ӧ�����Ŀ=====
PL_ACC_QTYFK      = '01061200000001'   #����Ӧ����
#=====�ر��  20081225  ����4601ũ�������˿�Ŀ��4602ũ�������˿�Ŀ=====
PL_ACC_NXYWZ      = '01075100000005'   #ũ��������
PL_ACC_NXYLZ      = '01075600000005'   #ũ��������

#=====�ر��  20080804 ����OPRNO����
PL_HDOPRNO_HD     = '00'       #���
PL_HDOPRNO_WT     = '01'       #ί���տ�(����)
PL_HDOPRNO_TS     = '02'       #���ճи�(����)
PL_HDOPRNO_TY     = '04'       #��Լ���
PL_HDOPRNO_TH     = '09'       #�˻�
PL_HPOPRNO_QF     = '00'       #ǩ��
PL_HPOPRNO_JF     = '01'       #�⸶
PL_HPOPRNO_CX     = '03'       #����
PL_HPOPRNO_GS     = '04'       #��ʧ
PL_HPOPRNO_JG     = '05'       #���
PL_HPOPRNO_TP     = '06'       #��Ʊ
PL_HPOPRNO_CF     = '07'       #���ڸ���
PL_TDOPRNO_TC     = '20'       #�ֽ�ͨ��
PL_TDOPRNO_BZY    = '21'       #�����˻�ת���
PL_TDOPRNO_TD     = '22'       #�ֽ�ͨ��
PL_TDOPRNO_YZB    = '23'       #����˻�ת����
PL_TDOPRNO_CZ     = '24'       #����
PL_TDOPRNO_CX     = '25'       #����
PL_TDOPRNO_BZ     = '26'       #����

#=====�ر��  20081030 ����ϵͳ��������
PL_BPATPE_STR     = '0'        #�ַ�
PL_BPATPE_NUM     = '1'        #����
PL_BPATPE_MON     = '2'        #���

#=====������  20081124 ������������ȡ��ʽ====
PL_CHRG_CASH      = '0'        # �ֽ�
PL_CHRG_TYPE      = '1'        #ת��
PL_CHRG_NONE      = '2'        #���շ�
