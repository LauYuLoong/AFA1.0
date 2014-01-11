# -*- coding: gbk -*-
###################################################################
#    ��    ��:    Tvouh001.py
#    ˵    ��:    ƾ֤�������ݸ���
#    ��    ��:    �м�ҵ����ƽ̨��AFA��--- UNIX: AIX 5.3
#    ��    ��:    ������
#    ��    ˾:    ������ͬ�Ƽ�
#    ������ַ:    ����
#    ����ʱ��:    2011��12��20��
#    ά����¼:
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, AfaFlowControl, AfaDBFunc,AfaHostFunc,HostComm
from types import *
import AfaLoggerFunc,VouhFunc,binascii,HostContext,VouhHostFunc

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
        #===========��ѯ���ݿ��в����Ϲ���Ŀ����־��ƾ֤״̬���==============       
        sql = ""
        sql = "select distinct(BESBNO) from vouh_register where depository = '4' and vouhstatus='2'"
        
        AfaLoggerFunc.tradeInfo('��ѯ���'+ sql)
        
        records = AfaDBFunc.SelectSql( sql )
        
        if records==None:
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"��ѯ���ݿ�ʧ��"
            raise AfaFlowControl.flowException( )
        
        elif(len(records) < 1):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","��������������������"
            return False
        
        else:
            
            record=AfaUtilTools.ListFilterNone( records )          
            total=len( records )
            AfaLoggerFunc.tradeDebug("����������" + str(total))
            
            for i in range(0,total):
                
                AfaLoggerFunc.tradeInfo('������'+ records[i][0])          
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
                    AfaLoggerFunc.tradeInfo( SBNO )
                
                if(SBNO=='33'):
                    update_sql = ""
                    update_sql = update_sql + "update vouh_register set depository = '1'"
                    update_sql = update_sql + " where besbno = '" + records[i][0] + "'"
                    update_sql = update_sql + " and depository = '4' and vouhstatus='2'"
                    AfaLoggerFunc.tradeInfo('�������ݿ����1��'+ update_sql)
                    #���²��ύ����
                    if  AfaDBFunc.UpdateSqlCmt(update_sql)<0:
                        return AfaFlowControl.ExitThisFlow("A999","����ʧ��")
                    
                elif(SBNO=='31' or SBNO=='40' or SBNO=='32' or SBNO=='41'):
                    update_sql = ""
                    update_sql = "update vouh_register set depository = '2'"
                    update_sql = update_sql + " where besbno = '" + records[i][0] + "'"
                    update_sql = update_sql + " and depository = '4' and vouhstatus='2'"
                    AfaLoggerFunc.tradeInfo('�������ݿ����2��'+ update_sql)
                    if  AfaDBFunc.UpdateSqlCmt(update_sql)<0:
                        return AfaFlowControl.ExitThisFlow("A999","����ʧ��")
                        
                elif(SBNO=='50'):
                    update_sql = ""
                    update_sql = "update vouh_register set depository = '3'"
                    update_sql = update_sql + " where besbno = '" + records[i][0] + "'"
                    update_sql = update_sql + " and depository = '4' and vouhstatus='2'"
                    AfaLoggerFunc.tradeInfo('�������ݿ����3��'+ update_sql)
                    if  AfaDBFunc.UpdateSqlCmt(update_sql)<0:
                        return AfaFlowControl.ExitThisFlow("A999","����ʧ��")
                else:
                    VouhFunc.tradeExit('A005061', '�û���������ָ����Χ��')
                    raise AfaFlowControl.flowException( )                
        
                tradeExit('0000', '���³ɹ�')

        
                #=============�����˳�=========================================
        
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return False

#######################################������###########################################
if __name__=='__main__':

    AfaLoggerFunc.tradeInfo('********************�����Ϲ���Ŀ����־��ƾ֤״̬���ת����ʼ********************')
    
    #ת������
    vouh_Pro( )
    
    AfaLoggerFunc.tradeInfo('********************�����Ϲ���Ŀ����־��ƾ֤״̬���ת������********************')