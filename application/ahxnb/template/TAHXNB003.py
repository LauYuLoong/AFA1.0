# -*- coding: gbk -*-
################################################################################
#   ����ҵ��.ͨ��ģ��
#===============================================================================
#   ģ���ļ�:   AHXNB001.py
#   �޸�ʱ��:   2010-12-15
################################################################################
import TradeContext

TradeContext.sysType = "ahxnb"

import AfaLoggerFunc,AfaUtilTools,AfaFlowControl,AfaFunc,os

from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('********����ʡ��ũ��.����ģ��['+TradeContext.TemplateCode+']����********')

    try:
    
        #=====================��ʼ�����ر��ı���================================
        TradeContext.tradeResponse=[]

       
        #=====================��ȡϵͳ����ʱ��==================================
        TradeContext.WorkDate=AfaUtilTools.GetSysDate( )
        TradeContext.WorkTime=AfaUtilTools.GetSysTime( )
        
        #=====================�ж�Ӧ��ϵͳ״̬==================================
        if not AfaFunc.ChkSysStatus( ) :
            raise AfaFlowControl.flowException( )


        #=====================��̬���ؽ��׽ű�==================================
        trxModuleName = 'T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode
        try:
            trxModuleHandle=__import__( trxModuleName )

        except Exception, e:
            AfaLoggerFunc.tradeInfo(e)
            raise AfaFlowControl.flowException( 'A0001', '���ؽ��׽ű�ʧ�ܻ��׽ű�������' )


        #=====================������ũ��ҵ����Ի�����==========================
        if not trxModuleHandle.TrxMain( ) :
            raise AfaFlowControl.flowException( TradeContext.errorCode,TradeContext.errorMsg)


        #=====================�Զ����==========================================
        AfaFunc.autoPackData()


        #=====================�˳�ģ��==========================================
        AfaLoggerFunc.tradeInfo('********����ʡ��ũ��.����ģ��['+TradeContext.TemplateCode+']�˳�********')


    except AfaFlowControl.flowException, e:
        #�����쳣
        AfaFlowControl.exitMainFlow( str(e) )

    except AfaFlowControl.accException:
        #�����쳣
        AfaFunc.autoPackData()

    except Exception, e:
        #Ĭ���쳣
        AfaFlowControl.exitMainFlow( str( e ) )
        
if __name__ == '__main__':
    TradeContext.TemplateCode = "AHXNB001"
    TradeContext.TransCode = "8492"
    TradeContext.I1SBNO    ="3401010077"
    TradeContext.sysId     ="AG2015"
    TradeContext.I1USID    ="007905"
    TradeContext.I1AUUS    =""
    TradeContext.I1AUPS    =""
    TradeContext.I1WSNO    =""
    TradeContext.I1APPNO   ="AG1014"
    TradeContext.I1BUSINO  ="34010100770001"
    #TradeContext.I1FTPTYPE ="2"
    #TradeContext.I1FILENAME="yhdkfs_nchz_340122_2.txt"
    TradeContext.I1FTPTYPE ="1"
    TradeContext.I1FILENAME = "daifa.txt"
    TradeContext.I1TOTALNUM="10"
    TradeContext.I1TOTALAMT="120.00"
    TradeContext.I1STARTDATE="20101217"
    TradeContext.I1ENDDATE  ="20101217"
    
    fileCount = os.popen("sed -n '$=' /home/maps/afa/data/ahxnb/yhkhfs_nchz_340122_1.txt").read().strip()
    print fileCount
    
    
    
    main( )

