# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ��ϵͳ������.ͨ��ͨ������������ϸ�ļ�����
#===============================================================================
#   �����ļ�:   rccpsTDZJDZImport.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-11-27
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc
import rccpsDBTrcc_tdzjmx,rccpsDBTrcc_mbrifa

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.ͨ��ͨ������������ϸ�ļ�����[rccpsTDZJDZImport]����***")
        
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
        
        #==========ɾ��������ϸ������=================================================
        AfaLoggerFunc.tradeInfo(">>>ɾ��������ϸ������")
        delsql = "delete from rcc_tdzjmx"
        res = AfaDBFunc.DeleteSqlCmt(delsql)
        if(  res==None or res == -1 ):
            AfaLoggerFunc.tradeDebug(">>>������ϸ����������ʧ��,���ݿ���,��������")
            AfaDBFunc.RollbackSql()
            rccpsCronFunc.cronExit( '9000', '������ϸ����������ʧ��,���ݿ���,��������' )  
        else:
            AfaDBFunc.CommitSql()
        
        #==========������ϸ����������=================================================
        AfaLoggerFunc.tradeInfo(">>>������ϸ����������")
        file_name = 'rccpsdz' + NCCWKDAT
        file_path = os.environ['AFAP_HOME'] + "/data/rccps/host/"
        rb = open(file_path + file_name , 'r')
        #��ȡһ��
        lineBuf = rb.readline()
        iLine=0
        while ( len(lineBuf) > 20 ):
            iLine=iLine+1
            sItemBuf = lineBuf.split('|')         
            
            if ( len(sItemBuf) < 16 ):
                rb.close()
                rccpsCronFunc.cronExit( '9000', '�����ļ���ʽ����(' + file_name + ')' )   
                
            tdzjmx_dict = {}
            tdzjmx_dict['NCCWKDAT'] = sItemBuf[2].strip()
            tdzjmx_dict['SCNBBH'] = sItemBuf[1].strip()
            tdzjmx_dict['SCFEDT'] = sItemBuf[3].strip()
            tdzjmx_dict['SCRBSQ'] = sItemBuf[4].strip()
            tdzjmx_dict['SCEYDT'] = sItemBuf[5].strip()
            tdzjmx_dict['SCTLSQ'] = sItemBuf[6].strip()
            tdzjmx_dict['SCRVSB'] = sItemBuf[7].strip()
            tdzjmx_dict['SCCATR'] = sItemBuf[8].strip()
            tdzjmx_dict['SCWLBZ'] = sItemBuf[9].strip()
            tdzjmx_dict['SCTRAM'] = sItemBuf[10].strip()
            if(tdzjmx_dict['SCTRAM'][0] == '-'):
               tdzjmx_dict['SCTRAM'] = tdzjmx_dict['SCTRAM'][1:]
            tdzjmx_dict['SCFLAG'] = sItemBuf[11].strip()
            tdzjmx_dict['SCSTCD'] = sItemBuf[12].strip()
            tdzjmx_dict['SCBYZ1'] = sItemBuf[13].strip()
            tdzjmx_dict['SCBYZ2'] = sItemBuf[14].strip()
            tdzjmx_dict['SCBYZ3'] = sItemBuf[15].strip()
            
            #���(SCRVSB)���˱�־����"1"(8820 ����)����¼��һ��
            if(tdzjmx_dict['SCRVSB'] == '1'):
                tdzjmxcp_dict = {}
                tdzjmxcp_dict = tdzjmx_dict.copy()
                tdzjmxcp_dict['SCRVSB'] = ''
                tdzjmxcp_dict['SCSTCD'] = '1'
                records = rccpsDBTrcc_tdzjmx.insertCmt(tdzjmxcp_dict)      
                if( records == -1):
                    AfaLoggerFunc.tradeDebug(">>>������ϸ����������ʧ��,���ݿ���,��������")
                    AfaDBFunc.RollbackSql()
                    rccpsCronFunc.cronExit( '9000', '������ϸ����������ʧ��,���ݿ���,��������' )  
                else:
                    AfaDBFunc.CommitSql()
            
            res = rccpsDBTrcc_tdzjmx.insertCmt(tdzjmx_dict)      
            if( res == -1):
                AfaLoggerFunc.tradeDebug(">>>������ϸ����������ʧ��,���ݿ���,��������")
                AfaDBFunc.RollbackSql()
                rccpsCronFunc.cronExit( '9000', '������ϸ����������ʧ��,���ݿ���,��������' )  
            else:
                AfaDBFunc.CommitSql()

            lineBuf = rb.readline()
        
        rb.close()
        
        #================�ر�ͨ��ͨ������������ϸ���ļ�����ϵͳ����,��ͨ��ͨ���������˹���ϵͳ����==
        AfaLoggerFunc.tradeInfo(">>>��ʼ�ر�ͨ��ͨ������������ϸ���ļ�����ϵͳ����,��ͨ��ͨ���������˹���ϵͳ����")
        if not rccpsCronFunc.closeCron("00069"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","�ر�ͨ��ͨ�Ҷ�����ϸ���ļ�����ϵͳ�����쳣")
            
        if not rccpsCronFunc.openCron("00070"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","��ͨ��ͨ�Ҷ��˹���ϵͳ�����쳣")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit�쳣")
        AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
        
        AfaLoggerFunc.tradeInfo(">>>�����ر�ͨ��ͨ������������ϸ���ļ�����ϵͳ����,��ͨ��ͨ���������˹���ϵͳ����")
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.ͨ��ͨ������������ϸ�ļ�����[rccpsTDZJDZImport]�˳�***")
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
            AfaLoggerFunc.tradeInfo('***[rccpsTDZJDZImport]�����ж�***')

        sys.exit(-1)