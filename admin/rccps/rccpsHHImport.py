# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ��ϵͳ������.�к���Ч����
#===============================================================================
#   �����ļ�:   rccpsHHEffict.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-09-15
################################################################################
import TradeContext
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys,AfaHostFunc
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsState,rccpsDBFunc,rccpsHostFunc,rccpsUtilTools
import rccpsDBTrcc_paybnk

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit("usage: rccpsHHImport.py filename")
        
    try:
        local_file_home = os.environ['AFAP_HOME'] + "/data/rccps/"
        file_path = "filein/" + sys.argv[1]
        
        AfaLoggerFunc.tradeInfo(">>>��ʼ���������кű�ũ�����ʽ�����ϵͳ�����к�")
        
        pfile = open(local_file_home + file_path,"rb")
        file_line = " "
        
        while file_line:
            file_line = AfaUtilTools.trim(pfile.readline())   
            file_line = rccpsUtilTools.replaceRet(file_line)
            
            if file_line == "":
                continue
                
            line_list = file_line.split('|')
            
            paybnk_where_dict = {}
            paybnk_where_dict['BANKBIN'] = line_list[0]
            tmp_paybnk_dict = rccpsDBTrcc_paybnk.selectu(paybnk_where_dict)
            if tmp_paybnk_dict == None:
                if not AfaDBFunc.RollbackSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    AfaLoggerFunc.tradeError(">>>Rollback�쳣")
                AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
                rccpsCronFunc.cronExit("S999","��ѯ���Ǽ��к��Ƿ�����쳣")
            
            paybnk_dict = {}
            paybnk_dict['BANKBIN']      = line_list[0][:10]
            paybnk_dict['BANKSTATUS']   = line_list[1][:1]
            paybnk_dict['BANKATTR']     = line_list[2][:2]
            paybnk_dict['STLBANKBIN']   = line_list[3][:10]
            paybnk_dict['BANKNAM']      = line_list[4][:60]
            paybnk_dict['BANKADDR']     = line_list[5][:60]
            paybnk_dict['BANKPC']       = line_list[6][:6]
            paybnk_dict['BANKTEL']      = line_list[7][:30]
            paybnk_dict['EFCTDAT']      = line_list[8][:8]
            paybnk_dict['INVDAT']       = line_list[9][:8]
            paybnk_dict['ALTTYPE']      = line_list[10][:1]
            paybnk_dict['PRIVILEGE']    = line_list[11][:20]
            paybnk_dict['STRINFO']      = line_list[12][:60]
            
            if len(tmp_paybnk_dict) <= 0:
                #=====�����кű��в����ڴ��к�,�������к�=======================
                ret = rccpsDBTrcc_paybnk.insert(paybnk_dict)
                AfaLoggerFunc.tradeInfo("�������к�")
                if ret <= 0:
                    if not AfaDBFunc.RollbackSql( ):
                        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        AfaLoggerFunc.tradeError(">>>Rollback�쳣")
                    AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
                    rccpsCronFunc.cronExit("S999","�������к��쳣")
                    
            #else:
            #    #=====�����кű��д��ڴ��к�,�����к���Ϣ=======================
            #    ret = rccpsDBTrcc_paybnk.update(paybnk_dict,paybnk_where_dict)
            #    AfaLoggerFunc.tradeInfo("���¾��к�")
            #    if ret <= 0:
            #        if not AfaDBFunc.RollbackSql( ):
            #            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            #            AfaLoggerFunc.tradeError(">>>Rollback�쳣")
            #        AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
            #        rccpsCronFunc.cronExit("S999","���¾��к��쳣")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit�쳣")
        AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
        
        AfaLoggerFunc.tradeInfo(">>>�������������кű�ũ�����ʽ�����ϵͳ�����к�")
        
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
            AfaLoggerFunc.tradeInfo("***[rccpsHHEffict]�����ж�***")

        sys.exit(-1)