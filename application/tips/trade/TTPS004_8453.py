# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.��˰���к�������.���ж��걨�ɷѽ���
#=================================================================
#   �����ļ�:   TTPS004_8453.py
#   �޸�ʱ��:   2008-5-2 16:02
##################################################################
import TradeContext, AfaLoggerFunc,Party3Context,TipsFunc
from types import *

def SubModuleDoFst( ):
    try:
        AfaLoggerFunc.tradeInfo('����ɷѽ���['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']ǰ����' )
        #TradeContext.tradeType='T' #ת���ཻ��
        #if( not TradeContext.existVariable( "corpTime" ) ):
        #    return TipsFunc.ExitThisFlow( 'A0001', 'ί������[corpTime]ֵ������!' )
        #if( not TradeContext.existVariable( "corpSerno" ) ):
        #    return TipsFunc.ExitThisFlow( 'A0001', '������.������ˮ��[corpSerno]ֵ������!' )
        
        #====�ж�Ӧ��״̬=======
        if not TipsFunc.ChkAppStatus():
            return False
            
        TradeContext.payeeBankNo = '011100000003'
        #====��ȡ������Ϣ=======
        if not TipsFunc.ChkLiquidStatus():
            return False
        #====����Ƿ�ǩԼ��=======
        #if not TipsFunc.ChkCustSign():
        #    return False
        #====�жϻ���״̬=======
        if not TipsFunc.ChkBranchStatus():
            return False
        #====��ȡժҪ����=======
        #if not AfaFlowControl.GetSummaryCode():
        #    return False
        
        #ժҪ����
        TradeContext.summary_code = 'TIP'
        
        #ת�����(��ԪΪ��λ->�Է�Ϊ��λ)
        #AfaLoggerFunc.tradeInfo('ת��ǰ���(��ԪΪ��λ)=' + TradeContext.amount)
        #TradeContext.amount=str(long((float(TradeContext.amount))*100 + 0.1))
        #AfaLoggerFunc.tradeInfo('ת������(�Է�Ϊ��λ)=' + TradeContext.amount)
       
        #��ʼ��
        #TradeContext.catrFlag = '1'         #�ֽ�ת�˱�־
        TradeContext.__agentEigen__ = '0'   #�ӱ��־
        TradeContext.channelCode = '001'
        TradeContext.userno = '12'
        TradeContext.zoneno = '000'
        AfaLoggerFunc.tradeInfo('==========================[' +TradeContext.accno+ ']')
        AfaLoggerFunc.tradeInfo('�˳��ɷѽ���['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']ǰ����' )
        return True
    except Exception, e:
        TipsFunc.exitMainFlow(str(e)) 
def SubModuledoSnd():
    try:
        return Party3Context.dn_detail
    except Exception, e:
        TipsFunc.exitMainFlow(str(e))
        
        
def SubModuledoTrd():
    return True

