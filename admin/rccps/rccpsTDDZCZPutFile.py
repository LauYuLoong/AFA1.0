# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ��ϵͳ������.ũ����ͨ��ͨ�Ҵ����ļ����ɼ����͵������ƽ̨
#===============================================================================
#   �����ļ�:   rccpsTDDZCZPutFile.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-12-10
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsFtpFunc,rccpsDBFunc,rccpsState,rccpsHostFunc,rccpsUtilTools
import rccpsDBTrcc_mbrifa,rccpsDBTrcc_tddzmx,rccpsDBTrcc_tddzcz

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.ũ����ͨ��ͨ�Ҵ����ļ����ɼ����͵������ƽ̨[rccpsTDDZCZPutFile]����***")
        
        #==========��ȡ��������================================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��ȡǰ���Ĺ�������")
        
        mbrifa_where_dict = {}
        mbrifa_where_dict['OPRTYPNO'] = "30"
        
        mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
        
        if mbrifa_dict == None:
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","��ѯ��ǰ���������쳣")
            
        NCCWKDAT = mbrifa_dict['NOTE1'][:8]                           #��������
        LNCCWKDAT = "('" + mbrifa_dict['NOTE3'].replace(",","','") + "')"
        
        AfaLoggerFunc.tradeInfo(">>>������ȡǰ���Ĺ�������")
        
        #================����ͨ��ͨ�Ҷ�����ϸ�Ǽǲ�,����ͨ��ͨ�Ҳ�����ļ�============
        AfaLoggerFunc.tradeInfo(">>>��ʼ����ͨ��ͨ�Ҳ�����ļ�")
        
        tddzcz_where_sql = "NCCWKDAT in " + LNCCWKDAT
        
        tddzcz_list = rccpsDBTrcc_tddzcz.selectm(1,0,tddzcz_where_sql,"")
        
        if tddzcz_list == None:
            rccpsCronFunc.cronExit("S999","��ѯͨ��ͨ�Ҷ��˴��˵Ǽǲ��쳣")
            
        file_path = os.environ['AFAP_HOME'] + "/data/rccps/errorfile/EXPREQ" + NCCWKDAT + '01.BIN'
        
        fp = open(file_path,"wb")
        
        if fp == None:
            rccpsCronFunc.cronExit("S999","��ͨ��ͨ�Ҷ��˲����ϸ�ļ��쳣")
            
        file_line = ""
        
        if len(tddzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo(">>>ͨ��ͨ�Ҷ�����ϸ�Ǽǲ����޶�Ӧ��¼")
        else:
            for i in xrange(len(tddzcz_list)):
                
                file_line = file_line + tddzcz_list[i]['SNDMBRCO'].ljust(10,' ')   + '|'
                file_line = file_line + tddzcz_list[i]['RCVMBRCO'].ljust(10,' ')   + '|'
                file_line = file_line + tddzcz_list[i]['TRCCO'].ljust(7,' ')       + '|'
                file_line = file_line + tddzcz_list[i]['DCFLG'].ljust(1,' ')       + '|'
                file_line = file_line + tddzcz_list[i]['TRCNO'].ljust(8,' ')       + '|'
                file_line = file_line + tddzcz_list[i]['TRCDAT'].ljust(8,' ')      + '|'
                file_line = file_line + tddzcz_list[i]['NCCWKDAT'].ljust(8,' ')    + '|'
                file_line = file_line + tddzcz_list[i]['PYRACC'].ljust(32,' ')     + '|'
                file_line = file_line + tddzcz_list[i]['PYEACC'].ljust(32,' ')     + '|'
                file_line = file_line + tddzcz_list[i]['CUR'].ljust(3,' ')         + '|'
                file_line = file_line + rccpsUtilTools.FormatMoney(str(tddzcz_list[i]['OCCAMT'])).ljust(15,' ')     + '|'
                file_line = file_line + rccpsUtilTools.FormatMoney(str(tddzcz_list[i]['LOCOCCAMT'])).ljust(15,' ')  + '|'
                file_line = file_line + rccpsUtilTools.FormatMoney(str(tddzcz_list[i]['CUSCHRG'])).ljust(15,' ')    + '|'
                file_line = file_line + rccpsUtilTools.FormatMoney(str(tddzcz_list[i]['LOCCUSCHRG'])).ljust(15,' ') + '|'
                file_line = file_line + tddzcz_list[i]['ORTRCNO'].ljust(8,' ')     + '|'
                file_line = file_line + tddzcz_list[i]['EACTYP'].ljust(2,' ')      + '|'
                file_line = file_line + tddzcz_list[i]['SNDBNKCO'].ljust(10,' ')   + '|'
                file_line = file_line + tddzcz_list[i]['RCVBNKCO'].ljust(10,' ')   + '|'
                file_line = file_line + "\n"
                
        fp.write(file_line)
        
        fp.close()
        
        AfaLoggerFunc.tradeInfo(">>>��������ͨ��ͨ�Ҳ�����ļ�")
        
        #�ر��  20081216  ����ftp�������ƽ̨��ش���
        ##================FTP�ļ�������=========================================
        #dFileName = "RCCPSTDDZCZ"  + NCCWKDAT
        #
        #AfaLoggerFunc.tradeInfo(">>>��ʼFTP�ļ��������ƽ̨")
        #if not rccpsFtpFunc.putERRSYS(dFileName):
        #    rccpsCronFunc.cronExit("S999","FTP�ļ��������ƽ̨�쳣")
        #    
        #AfaLoggerFunc.tradeInfo(">>>����FTP�ļ��������ƽ̨")
        
        #================�ر�ͨ��ͨ�Ҷ��˴����ļ����ɼ����͵������ƽ̨ϵͳ����==========
        AfaLoggerFunc.tradeInfo(">>>��ʼ�ر�ͨ��ͨ�Ҷ��˴����ļ����ɼ����͵������ƽ̨ϵͳ����")
        if not rccpsCronFunc.closeCron("00060"):
            rccpsCronFunc.cronExit("S999","�ر�ͨ��ͨ�Ҷ��˴����ļ����ɼ����͵������ƽ̨�����쳣")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit�쳣")
        AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
        
        AfaLoggerFunc.tradeInfo(">>>�����ر�ͨ��ͨ�Ҷ��˴����ļ����ɼ����͵������ƽ̨ϵͳ����")
        
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.ũ����ͨ��ͨ�Ҵ����ļ����ɼ����͵������ƽ̨[rccpsTDDZCZPutFile]�˳�***")
    
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
            AfaLoggerFunc.tradeInfo('***[rccpsTDDZCZPutFile]�����ж�***')

        sys.exit(-1)
