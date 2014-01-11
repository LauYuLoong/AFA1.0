# -*- coding: gbk -*-
################################################################################
#   ����ҵ��ϵͳ������ҵ���ý���
#===============================================================================
#   �����ļ�:   T001000_8401.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  XZH
#   �޸�ʱ��:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,os,AbdtFunc
from types import *


#=====================����ҵ���ý���==========================================
def TrxMain( ):


    AfaLoggerFunc.tradeInfo('**********����ҵ���ý���(8488)��ʼ**********')


    TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #��������
    TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #����ʱ��


    if ( TradeContext.I1PROCTYPE == '01' ):

        #��ѯ�˻���Ϣ
        if ( not AbdtFunc.VMENU_QueryAccInfo( ) ):
            return False

    else:
        return ExitSubTrade( '9000', '�޴˲�������' )


    AfaLoggerFunc.tradeInfo('**********����ҵ���ý���(8488)����**********')


    #����
    TradeContext.tradeResponse.append(['errorCode', '0000'])
    TradeContext.tradeResponse.append(['errorMsg',  '���׳ɹ�'])
    return True
       
    
    

def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False