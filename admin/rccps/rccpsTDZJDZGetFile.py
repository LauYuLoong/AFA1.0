# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ��ϵͳ������.ͨ��ͨ�����������ļ�����
#===============================================================================
#   �����ļ�:   rccpsTDZJDZGetFile.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-11-27
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsHostFunc,rccpsFtpFunc
import rccpsDBTrcc_mbrifa

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.ͨ��ͨ�����������ļ�����[rccpsTDZJDZGetFile]����***")
        
        #==========��ȡ��������================================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��ȡǰ���Ĺ�������")
        
        mbrifa_where_dict = {}
        mbrifa_where_dict['OPRTYPNO'] = "30"
        
        mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
        
        if mbrifa_dict == None:
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","��ѯ��ǰ���������쳣")
            
        NCCWKDAT  = mbrifa_dict['NOTE1'][:8]                  #��������
        NCCWKDAT_LIST = mbrifa_dict['NOTE3'].split(',')       #��Ҫ���˵���������(���������㹤���պ�֮ǰ�ķ����㹤����)
        
        
        
        AfaLoggerFunc.tradeInfo(">>>��ʼע�����������ļ�����")
        
        #==========��������ǰ����==============================================
        TradeContext.HostCode = '8825'                        #���״���
        TradeContext.STRDAT = min( NCCWKDAT_LIST )            #��ʼ����
        TradeContext.ENDDAT = max( NCCWKDAT_LIST )            #��ֹ����
        TradeContext.BESBNO = PL_BESBNO_BCLRSB                #��������
        TradeContext.BETELR = PL_BETELR_AUTO                  #�Զ���Ա
            
        AfaLoggerFunc.tradeInfo("��ʼ���� = [" + TradeContext.STRDAT + "]")
        AfaLoggerFunc.tradeInfo("��ֹ���� = [" + TradeContext.ENDDAT + "]")
        #================����ע�����������ļ�����==========================
        rccpsHostFunc.CommHost( TradeContext.HostCode )
        
        AfaLoggerFunc.tradeInfo("errorCode = [" + TradeContext.errorCode + "]")
        AfaLoggerFunc.tradeInfo("errorMsg  = [" + TradeContext.errorMsg  + "]")
        
        #================�ж�ע���������˷�����Ϣ==============================
        
        if TradeContext.errorCode != '0000':
            rccpsCronFunc.cronExit("S999","ע�����������ļ������쳣")
        else:
            AfaLoggerFunc.tradeInfo("ע�����������ļ����ɳɹ�")
 
        AfaLoggerFunc.tradeInfo(">>>����ע�����������ļ�����")
        
        #================�������������ļ�======================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ�������������ļ�")
        #==========�ļ���===============
        host_path = 'BANKMDS'                                   #����·��
        file_path = 'NXSCA'           #����·��
        
        if( not rccpsFtpFunc.getHost(file_path,host_path)):
            rccpsCronFunc.cronExit('A099', '�������������ļ��쳣')
        AfaLoggerFunc.tradeInfo(">>>�����������������ļ�")
        
        #================���������ļ�ת��======================================
        AfaLoggerFunc.tradeInfo(">>>��ʼת�����������ļ�")
        dFileName = 'rccpsdz' + NCCWKDAT
        sFileName = 'NXSCA'
        fldName = 'nxsca.fld'
        if( not rccpsCronFunc.FormatFile('0', fldName, sFileName, dFileName)):
            rccpsCronFunc.cronExit('A099', 'ת�����������ļ������쳣')
        AfaLoggerFunc.tradeInfo(">>>����ת�����������ļ�")
        
        #================�ر�ͨ��ͨ������������ϸ������ϵͳ����,��ͨ��ͨ�����������ļ�����ϵͳ����==
        AfaLoggerFunc.tradeInfo(">>>��ʼ�ر�ͨ��ͨ������������ϸ������ϵͳ����,��ͨ��ͨ�����������ļ�����ϵͳ����")
        if not rccpsCronFunc.closeCron("00068"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","�ر�ͨ��ͨ�Ҷ�����ϸ������ϵͳ�����쳣")
            
        if not rccpsCronFunc.openCron("00069"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","��ͨ��ͨ�Ҷ����ļ�����ϵͳ�����쳣")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit�쳣")
        AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
        
        AfaLoggerFunc.tradeInfo(">>>�����ر�ͨ��ͨ������������ϸ������ϵͳ����,��ͨ��ͨ�����������ļ�����ϵͳ����")
        
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.ͨ��ͨ�Ҷ�����ϸ�˹���[rccpsTDDZMXCompare]�˳�***")
    
    except Exception, e:
        #�����쳣

        if not AfaDBFunc.RollbackSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeInfo(">>>Rollback�쳣")
        AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")

        if( not TradeContext.existVariable( "errorCode" ) or str(e) ):
            TradeContext.errorCode = 'A9999'
            TradeContext.errorMsg = 'ϵͳ����['+ str(e) +']'

        if TradeContext.errorCode != '0000' :
            AfaLoggerFunc.tradeInfo( 'errorCode=['+TradeContext.errorCode+']' )
            AfaLoggerFunc.tradeInfo( 'errorMsg=['+TradeContext.errorMsg+']' )
            AfaLoggerFunc.tradeInfo('***[rccpsTDZJDZGetFile]�����ж�***')

        sys.exit(-1)
