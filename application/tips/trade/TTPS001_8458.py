# -*- coding: gbk -*-
##################################################################
#   ��˰����.����TIPS�ط�������ϸ
#=================================================================
#   �����ļ�:   TTPS001_8458.py
#   �޸�ʱ��:   2007-7-2 15:03
##################################################################
import TradeContext, AfaLoggerFunc
#, UtilTools,TipsFunc
import TipsFunc,AfaAfeFunc
from types import *

def SubModuleMainFst( ):

    AfaLoggerFunc.tradeInfo( '��������TIPS�ط�������ϸ��ѯ[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    sbrno=TradeContext.brno
    try:
        #====�жϻ���״̬=======
        if not TipsFunc.ChkBranchStatus( ):
            return False
        #====��ȡ������Ϣ=======
        if not TipsFunc.ChkLiquidStatus( ):
            return False
        if TradeContext.brno != TradeContext.__mainBrno__:
            return TipsFunc.ExitThisFlow( 'A0002', '��������������������˽���')
        #=============��ȡƽ̨��ˮ��==================== 
        if TipsFunc.GetSerialno( ) == -1 :
            raise TipsFunc.flowException( )
        
        #=============�������ͨѶ====================
        AfaAfeFunc.CommAfe()

        TradeContext.errorCode = '0000'
        TradeContext.errorMsg = '�������������Ժ��ѯ���˽��'
        
        AfaLoggerFunc.tradeInfo( '�˳�����TIPS�ط�������ϸ['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        return True
    except TipsFunc.flowException, e:
        return False
