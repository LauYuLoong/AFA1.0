###############################################################################
# -*- coding: gbk -*-
# �ļ���ʶ��
# ժ    Ҫ����˰ʵʱ�ϴ������Ϣ
#
# ��ǰ�汾��1.0
# ��    �ߣ�WJJ
# ������ڣ�2007��10��15��
###############################################################################
import TradeContext

TradeContext.sysType = 'cron'

import AfaUtilTools, sys, AfaDBFunc, AfaFsFunc
import os, HostContext, HostComm, AfaAfeFunc, AfaLoggerFunc, time
from types import *



def ChkAppStatus():
    sqlstr  =   "select status from abdt_unitinfo where appno='" + TradeContext.appNo + "' and busino ='" + TradeContext.busiNo + "'"
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None or len( records)==0 ):
        AfaLoggerFunc.tradeInfo('����Ӧ��״̬��ʧ��')
        return False
    elif len( records ) == 1:
        if records[0][0].strip() == '1':
            return True
        else:
            AfaLoggerFunc.tradeInfo('Ӧ��״̬û�п���')
            return False
    else:
        AfaLoggerFunc.tradeInfo('Ӧ��ǩԼ�쳣')
        return False
        
###########################################������###########################################
if __name__=='__main__':
    AfaLoggerFunc.tradeInfo('**********���շ�˰ʵʱ�ϴ������Ϣ��ʼ**********')
    
    
    TradeContext.sysId = "AG2008"
    
    #�г����е�λ���е�λ���
    #begin 20100527 �������޸� 
    #sqlstr  = "select distinct busino,accno from abdt_unitinfo where appno='AG2008'"
    #sqlstr  = "select distinct busino,accno,appno from abdt_unitinfo where appno in ('AG2008','AG2012')"
    sqlstr  = " select busino,accno,bankno from fs_businoinfo "
    #end
    
    fsrecords = AfaDBFunc.SelectSql( sqlstr )
    if fsrecords == None or len(fsrecords)==0 :
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","���ҵ�λ��Ϣ���쳣"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        sys.exit(1)
        
    AfaLoggerFunc.tradeInfo( fsrecords ) 
    for item in fsrecords :  
        
        AfaLoggerFunc.tradeInfo( item[0] )
        AfaLoggerFunc.tradeInfo( item[1] )
        AfaLoggerFunc.tradeInfo( item[2] )

        #begin 20100527 �������޸� 
        #TradeContext.appNo          =   'AG2008'
        TradeContext.bankbm         =   item[2].strip()
        
        if( TradeContext.bankbm == '012' ):
            TradeContext.appNo = 'AG2008';
        else:
            TradeContext.appNo = 'AG2012';
        #end
        
        TradeContext.busiNo         =   item[0].strip()
        TradeContext.workDate       =   AfaUtilTools.GetSysDate( )
        TradeContext.workTime       =   AfaUtilTools.GetSysTime( )
        TradeContext.zoneno         =   ""
        TradeContext.brno           =   ""
        TradeContext.teller         =   ""
        TradeContext.authPwd        =   ""
        TradeContext.termId         =   ""
        TradeContext.TransCode      =   "8449"                  #ʵʱ�ϴ������Ϣ
        
        #=============�ж�Ӧ��״̬========================
        if not ChkAppStatus( ) :
            AfaLoggerFunc.tradeInfo('**********���շ�˰��λ���%sӦ��״̬������**********' %TradeContext.busiNo)
            continue
        
        #�������������ѯ�˻����
        HostContext.I1TRCD = '8810'                        #������
        HostContext.I1SBNO = ''                            #���׻�����
        HostContext.I1USID = '999986'                      #���׹�Ա��
        HostContext.I1AUUS = ""                            #��Ȩ��Ա
        HostContext.I1AUPS = ""                            #��Ȩ��Ա����
        HostContext.I1WSNO = ""                            #�ն˺�
        HostContext.I1ACNO = item[1].strip()               #�Թ������ʺ�
        HostContext.I1CYNO = ""                            #����        
        HostContext.I1CFFG = ""                            #����У���־
        HostContext.I1PSWD = ""                            #����        
        HostContext.I1CETY = ""                            #ƾ֤����    
        HostContext.I1CCSQ = ""                            #ƾ֤����    


        HostTradeCode = "8810".ljust(10,' ')
        HostComm.callHostTrade( os.environ['AFAP_HOME'] + '/conf/hostconf/AH8810.map', HostTradeCode, "0002" )
        if( HostContext.host_Error ):
            AfaLoggerFunc.tradeInfo('>>>��������ʧ��=[' + str(HostContext.host_ErrorType) + ']:' +  HostContext.host_ErrorMsg)
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   HostContext.host_ErrorMsg
            continue
            
        else:
            if ( HostContext.O1MGID == "AAAAAAA" ):
                AfaLoggerFunc.tradeInfo('���ؽ��:�˻����     = ' + HostContext.O1ACBL)        #�˻���� 
            else:
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "�������ײ��ɹ�"
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                continue
        
        
        
        #-----------------------���ݵ�λ�������û�ȡ������Ϣ----------------------------
        
        #begin 20100527 �������޸� �������б����ֶΣ�bankno����Ϊsql�Ĳ�ѯ����
        #sqlstr      =   "select aaa010,bankno from fs_businoinfo where busino='" + TradeContext.busiNo + "'"
        sqlstr      =   "select aaa010,bankno from fs_businoinfo where busino='" + TradeContext.busiNo + "'" + " and bankno='" + TradeContext.bankbm + "'"
        #end
        
        AfaLoggerFunc.tradeInfo( sqlstr )
            
        records = AfaDBFunc.SelectSql( sqlstr )
        if records == None or len(records)==0 :
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","���ҵ�λ��Ϣ��ʧ��"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            continue
        
        elif len(records) > 1:
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","��λ��Ϣ���쳣:һ����λ��Ŷ�Ӧ�˶��������Ϣ"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            AfaLoggerFunc.tradeInfo( sqlstr )
            continue

        #ƴ�ɵ���������
        TradeContext.TemplateCode   =   "3001"
        TradeContext.AAA010         =   records[0][0].strip()       #������������
        TradeContext.AFA101         =   records[0][1].strip()       #������������
        #TradeContext.AAA010         =   "0000000000"
        #TradeContext.AFA101         =   "011"
        TradeContext.AFA103         =   item[1].strip()             #�ʺ�
        TradeContext.AFC601         =   HostContext.O1ACBL          #���
        
        
        #=============�������ͨѶͨѶ====================
        TradeContext.__respFlag__='0'
        AfaAfeFunc.CommAfe()
        if( TradeContext.errorCode != '0000' ):
            AfaLoggerFunc.tradeInfo( TradeContext.errorCode + TradeContext.errorMsg )
            continue

    AfaLoggerFunc.tradeInfo('**********���շ�˰ʵʱ�ϴ������Ϣ����**********')
    sys.exit(0)
