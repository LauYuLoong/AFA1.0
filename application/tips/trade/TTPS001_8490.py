# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.��˰���к�������.�˹��ط����ж˽ɿ��ִ
#=================================================================
#   �����ļ�:   TPS001_8490.py
#   �޸�ʱ��:   2007-10-23
##################################################################

import TradeContext, AfaFlowControl
#LoggerHandler, UtilTools,  os, AfaLoggerFunc
import AfaAfeFunc,TipsFunc

def SubModuleMainFst( ):

    try:
    
        #=============��ȡƽ̨��ˮ��====================
        if TipsFunc.GetSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )
            
        TradeContext.TaxVouNo = '34234234'
        TradeContext.OriTaxOrgCode = '21100000000'
        TradeContext.OriEntrustDate = '20060623'
        TradeContext.OriTraNo = '00000012'
        TradeContext.TaxDate = '20060623'
        TradeContext.Result = '90000'
        TradeContext.AddWord = '���׳ɹ�'
        
        #=============�������ͨѶ====================
        AfaAfeFunc.CommAfe()
        if( TradeContext.errorCode != '0000' ):
            return False

        TradeContext.errorCode = '0000'
        TradeContext.errorMsg = '���׳ɹ�'

    except AfaFlowControl.flowException, e:
        return False
    except Exception, e:
        return AfaFlowControl.ExitThisFlow('A9999','ϵͳ�쳣'+str(e) )
    return True
 
def SubModuleMainSnd ():
    return True
