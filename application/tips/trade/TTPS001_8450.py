# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.��˰���к�������.ǰ̨�����½�˳�
#=================================================================
#   �����ļ�:   TTPS001_8450.py
#   �޸�ʱ��:   2008-10-23
##################################################################

import TradeContext, TipsFunc
#LoggerHandler, UtilTools,, os
import AfaAfeFunc,AfaLoggerFunc

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('==========��ʼ��˰����.ǰ̨�����½�˳�[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']==========')
    
    #=============��ȡƽ̨��ˮ��====================
    if TipsFunc.GetSerialno( ) == -1 :
        raise TipsFunc.flowException( )
        
    if TradeContext.OperFlag=='1':  #��½
        #��ѯӦ������״̬
        TipsFunc.SelAppStatus()
        if(TradeContext.flag == '1'):
            AfaLoggerFunc.tradeInfo('>>>Ӧ������״̬Ϊ��½�������ظ���½')
            TradeContext.errorCode = '0001'
            TradeContext.errorMsg = '�ѵ�½'
            return True
        
    elif TradeContext.OperFlag=='2': #�˳�
        #��ѯӦ������״̬
        TipsFunc.SelAppStatus()
        if(TradeContext.flag == '2'):
            AfaLoggerFunc.tradeInfo('>>>Ӧ������״̬Ϊ�˳��������ظ��˳�')
            TradeContext.errorCode = '0001'
            TradeContext.errorMsg = '���˳�'
            return True

    #=============�������ͨѶ====================
    AfaAfeFunc.CommAfe()
    if( TradeContext.errorCode != '0000' ):
        return False
    else:
        if TradeContext.OperFlag=='1':  #��½
            #��ѯӦ������״̬
            #TipsFunc.SelAppStatus()
            #if(TradeContext.flag == '1'):
            #    TradeContext.errorMsg = '�ѵ�½'
            #    return True
            AfaLoggerFunc.tradeInfo('>>>�޸�����״̬Ϊ��½״̬(1-��½,0-�˳�)')
            if (not TipsFunc.UpdAppStatus('1')):
                raise TipsFunc.flowException( )
        elif TradeContext.OperFlag=='2': #�˳�
            AfaLoggerFunc.tradeInfo('>>>�޸�����״̬Ϊ�˳�״̬(1-��½,0-�˳�)')
            if (not TipsFunc.UpdAppStatus('0')):
                raise TipsFunc.flowException( )
        
        #TradeContext.errorMsg = '���׳ɹ�'
        
    AfaLoggerFunc.tradeInfo('==========�˳���˰����.ǰ̨�����½�˳�[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']==========')
    return True
 
def SubModuleMainSnd ():
    return True
