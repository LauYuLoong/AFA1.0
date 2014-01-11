# -*- coding: gbk -*-
###################################################################
#    ��    ��:    Tvouh001.py
#    ˵    ��:    ƾ֤�������ݸ���
#    ��    ��:    �м�ҵ����ƽ̨��AFA��--- UNIX: AIX 5.3
#    ��    ��:    ������
#    ��    ˾:    ������ͬ�Ƽ�
#    ������ַ:    ����
#    ����ʱ��:    2012��04��09��
#    ά����¼:
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools,  AfaFlowControl, AfaDBFunc
from types import *
import HostContext,VouhHostFunc
#VouhFunc,binascii,AfaFunc,AfaHostFunc,HostComm,

TradeContext.sysType = 'agent' 

#=============���ش�����,������Ϣ===================================
def tradeExit( code, msg ):
    TradeContext.errorCode, TradeContext.errorMsg=code, msg
    if code != '0000':
        return False
    return True

#=========================������==============================================
def vouh_Pro( ):
        
    try: 
        #===========��ѯ���ݿ������л���==============       
        sql = ""
        sql = "select distinct(besbno) from vouh_register where vouhstatus='2'"
        
        AfaLoggerFunc.tradeInfo('��ѯ���'+ sql)
        
        records = AfaDBFunc.SelectSql( sql )
        
        if records==None:
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"��ѯ���ݿ��쳣"
            raise AfaFlowControl.flowException( )
        
        elif(len(records) < 1):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","��������������������"
            return False
        
        else:
            
            record=AfaUtilTools.ListFilterNone( records )          
            total=len( records )
            AfaLoggerFunc.tradeDebug("����ѯ����������" + str(total))
            
            for i in range(0,total):
            
                AfaLoggerFunc.tradeInfo('������:'+ records[i][0])
                          
                #=============��ȡ��������==========================
                HostContext.I1OTSB = records[i][0]                #��������
                HostContext.I1SBNO = '3401010007'                 #������
                HostContext.I1USID = '999996'                     #��Ա��
                #HostContext.I1WSNO = TradeContext.sWSNO          #�ն˺�
                
                if(not VouhHostFunc.CommHost('2001')):
                    tradeExit( TradeContext.errorCode, TradeContext.errorMsg )
                    raise AfaFlowControl.flowException( )
                if(TradeContext.errorCode == '0000'):
                    SBNO = HostContext.O1SBCH
                    AfaLoggerFunc.tradeInfo( '��������:'+ SBNO )
                
                if(SBNO=='33'):
                    continue
                    
                elif(SBNO=='31' or SBNO=='40' or SBNO=='32' or SBNO=='41'):
                    update_sql = ""
                    update_sql = "update vouh_register set depository = '2'"
                    update_sql = update_sql + " where besbno = '" + records[i][0] + "'"
                    update_sql = update_sql + "and vouhstatus='2'"
                    AfaLoggerFunc.tradeInfo('update1��'+ update_sql)
                    if  AfaDBFunc.UpdateSqlCmt(update_sql)<0:
                        return AfaFlowControl.ExitThisFlow("A999","����ʧ��")
                        
                elif(SBNO=='50'):
                    update_sql = ""
                    update_sql = "update vouh_register set depository = '3'"
                    update_sql = update_sql + " where besbno = '" + records[i][0] + "'"
                    update_sql = update_sql + " and vouhstatus='2'"
                    AfaLoggerFunc.tradeInfo('update2��'+ update_sql)
                    if  AfaDBFunc.UpdateSqlCmt(update_sql)<0:
                        return AfaFlowControl.ExitThisFlow("A999","����ʧ��")
                else:
                    tradeExit('A005061', '�û���������ָ����Χ��')
                    raise AfaFlowControl.flowException( )                
        
                tradeExit('0000', '���³ɹ�')

        
                #=============�����˳�=========================================
        
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return False

#######################################������###########################################
if __name__=='__main__':

    AfaLoggerFunc.tradeInfo('********************�����������ͬ����ʼ********************')
    
    #ת������
    vouh_Pro( )
    
    AfaLoggerFunc.tradeInfo('********************�����������ͬ������********************')
