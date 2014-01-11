# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.Ӧ�ò��������
#=================================================================
#   �����ļ�:   AppFunc.py
#   �޸�ʱ��:   2006-09-26
##################################################################
from types import *
import ConfigParser, time, Party3Context,AfaLoggerFunc,AfaFlowControl
import exceptions, TradeContext, AfaDBFunc, TradeException, AfaUtilTools
import AfaFunc
import os

#===========================================================================
#   ����������    ���ײ������
#   ����˵��:    ChkCode    8λ
#        ÿһλ��ʾһ�ּ�����ͣ�1��ʾ���,0��ʾ����飻Ŀǰ��������
#        ��1λ����ʾ�Ƿ���Ӧ��ϵͳ״̬
#        ��2λ����ʾ�Ƿ����̻�״̬
#        ��3λ����ʾ�Ƿ���Ӧ��״̬
#        ��4λ����ʾ�Ƿ��齻��״̬
#        ��5λ����ʾ�Ƿ�������״̬
#        ��6λ����ʾ�Ƿ���ɷѽ���״̬
#        ��7λ������
#        ��8λ������
#    ����������ͨ�����������¹ؼ�������
#        TradeContext.sysEName    ϵͳӢ�ļ��
#        TradeContext.sysCName    ϵͳ��������
#        TradeContext.__type__    ϵͳ����
#        TradeContext.__sysMaxAmount__     ���ʽ��׶��
#        TradeContext.__sysTotalamount__   ���ۼƽ��׶��
#        TradeContext.__channelMode__      ��������ģʽ
#        TradeContext.__actnoMode__        �ɷѽ��ʹ���ģʽ
#    
#        TradeContext.unitName     �̻�����
#        TradeContext.unitSName    �̻����
#        TradeContext.__bankMode__    ���н�ɫ
#        TradeContext.__busiMode__    ҵ��ģʽ
#        TradeContext.__accMode__     �˻�ģʽ
#        TradeContext.bankCode        ���б���
#        TradeContext.__agentEigen__  �̻�������
#        TradeContext.__signFlag__    ǩ����־
#        TradeContext.bankUnitno      �����̻����루�̻��ţ�
#        TradeContext.mainZoneno      ������к�
#        TradeContext.mainBrno        ���������
#        
#        TradeContext.subUnitName     �̻���֧��λ����
#        TradeContext.subUnitSName    �̻���֧��λ���
#        
#        TradeContext.__abstract__    ����ժҪ��(note1)
#        TradeContext.__prtAbs__      SASB��ӡժҪ��(note2)
#        
#        TradeContext.__tradeMode__       ����ģʽ
#        TradeContext.__bankReq__         ���з����־
#        TradeContext.__unitReq__         �̻������־
#        TradeContext.__accPwdFlag__      ����У���־
#        TradeContext.__tradePwdFlag__    ��������У���־
#        TradeContext.__channelCode__     ��������
#        TradeContext.__errType__         ����������0��������,1���ط�,2������
#        
#        TradeContext.__agentBrno__        ��Χϵͳ�����
#        TradeContext.__agentTeller__      ��Χϵͳ����Ա��
#        TradeContext.__chanlMaxAmount__   �������ʽ��׶��
#        TradeContext.__chanlTotalAmount__ �������ۼƽ��׶��
#        TradeContext.__billSaveCtl__      ��Ʊ�����־
#        TradeContext.__autoRevTranCtl__   �Զ����ʱ�־
#        TradeContext.__errChkCtl__        �쳣���׼���־
#        TradeContext.__autoChkAcct__      �Զ�����ʻ�����
#        TradeContext.__chkAccPwdCtl__     У���ʻ������־
#        TradeContext.__enpAccPwdCtl__     �ʻ�������ܱ�־
#        TradeContext.__hostType__         ������־

#==========================================================================   
def ChkParam(ChkCode='11111111'):

    if ChkCode[0]=='1':
    	#===============�ж�Ӧ��ϵͳ״̬======================
    	if not AfaFunc.ChkSysStatus( ) :
    		raise AfaFlowControl.flowException( )
    		    
    if ChkCode[1]=='1':
    	#===============�ж��̻�״̬======================
    	if not AfaFunc.ChkUnitStatus( ) :
    		raise AfaFlowControl.flowException( )

    if ChkCode[2]=='1':
        #=============�жϽ���״̬=====================
        if not AfaFunc.ChkTradeStatus( ) :
            raise AfaFlowControl.flowException( )

    if ChkCode[3]=='1':
    	#=============�ж�����״̬====================
    	if not AfaFunc.ChkChannelStatus( ) :
    		raise AfaFlowControl.flowException( )

    if ChkCode[4]=='1':
    	#=============�жϽɷѽ���״̬====================
    	if not AfaFunc.ChkActStatus( ) :
    		raise AfaFlowControl.flowException( )

    return True
