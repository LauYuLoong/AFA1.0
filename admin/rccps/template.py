# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ��ϵͳ������.ģ��
#===============================================================================
#   �����ļ�:   template.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ����
#   �޸�ʱ��:   YYYY-MM-DD
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc

if __name__ == '__main__':
    
    try:
        rccpsCronFunc.WrtLog("***ũ����ϵͳ: ϵͳ������.ģ��[template]����***")
        
        
        
        rccpsCronFunc.WrtLog("***ũ����ϵͳ: ϵͳ������.ģ��[template]�˳�***")
    
    except Exception, e:
        #�����쳣

        if not AfaDBFunc.RollbackSql( ):
            rccpsCronFunc.WrtLog( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.WrtLog(">>>Rollback�쳣")
        rccpsCronFunc.WrtLog(">>>Rollback�ɹ�")

        if( not TradeContext.existVariable( "errorCode" ) or str(e) ):
            TradeContext.errorCode = 'A9999'
            TradeContext.errorMsg = 'ϵͳ����['+ str(e) +']'

        if TradeContext.errorCode != '0000' :
            rccpsCronFunc.WrtLog( 'errorCode=['+TradeContext.errorCode+']' )
            rccpsCronFunc.WrtLog( 'errorMsg=['+TradeContext.errorMsg+']' )
            rccpsCronFunc.WrtLog('rccpsHDDZGetFile�����ж�')

        sys.exit(-1)