# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.����ˮ�Ѳ�ѯ����
#=================================================================
#   �����ļ�:   T4201_8422.py
#   �޸�ʱ��:   2007-06-12
##################################################################

import TradeContext, AfaDBFunc

#��Ҫ���͵������ӿڵ�ǰ̨û�취������,�ٴ˽���ƴ��.�����еĵ�������ѯҲ��Ҫ��ˮ�ŵ�
def SubModuleMainFst( ):
    TradeContext.__agentEigen__  = '0'   #�ӱ��־
    return True
 
def SubModuleMainSnd ():
    if TradeContext.errorCode   ==    "0000":
        TradeContext.errorMsg   =     "��½�ɹ�"
    return True