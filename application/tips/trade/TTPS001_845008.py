# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.��˰���к�������.״̬���֪ͨ
#   
#=================================================================
#   �����ļ�:   TTPS001_845008.py
#   �޸�ʱ��:   2008-5-4 10:56
##################################################################
import TradeContext, AfaLoggerFunc,TipsFunc
from types import *

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('״̬���֪ͨ����ǰ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
        if( not TradeContext.existVariable( "nextWorkDate" ) ):
            return TipsFunc.ExitThisFlow( '93002', 'TIPS��������[nextWorkDate]ֵ������!' )
        if(  len(TradeContext.nextWorkDate)!=8 ):
            return TipsFunc.ExitThisFlow( '93001', 'TIPS��������[nextWorkDate]ֵ���Ϸ�!' )
        if( not TradeContext.existVariable( "SysStat" ) ):
            return TipsFunc.ExitThisFlow( '93002', 'TIPS[SysStat]ֵ������!' )
        
        if TradeContext.SysStat=='0':#�ռ�
            #Ӧ������״̬Ϊ������
            if(not TipsFunc.UpdAppStatus('1')):                                  
                return TipsFunc.ExitThisFlow( 'A0001', '�޸�Ӧ������״̬ʧ��!' )
            #�޸�Ӧ�ù�������
            if(not TipsFunc.UpdAppWorkDate(TradeContext.nextWorkDate)):
                return TipsFunc.ExitThisFlow( 'A0001', '�޸�Ӧ�ù�������ʧ��!' )
        if TradeContext.SysStat=='1':#���д���
            #�޸�Ӧ�ù�������
            if(not TipsFunc.UpdAppWorkDate(TradeContext.nextWorkDate)):
                return TipsFunc.ExitThisFlow( 'A0001', '�޸�Ӧ�ù�������ʧ��!' )
        if TradeContext.SysStat=='2':#ϵͳά��״̬
            #Ӧ������״̬Ϊ����ͣ
            if(not TipsFunc.UpdAppStatus('2')):                                  
                return TipsFunc.ExitThisFlow( 'A0001', '�޸�Ӧ������״̬ʧ��!' )

        TradeContext.errorCode = '0000'
        TradeContext.errorMsg = '���׳ɹ�' 
        #=============�Զ����====================
        AfaLoggerFunc.tradeInfo('״̬���֪ͨǰ�������[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        return True
    except Exception, e:
        return TipsFunc.exitMainFlow(str(e))
