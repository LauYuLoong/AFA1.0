# -*- coding: gbk -*-
################################################################################
# �ļ����ƣ�vmenu_admin.py
# �ļ���ʶ��
# ժ    Ҫ���������
#
# ��ǰ�汾��1.0
# ��    �ߣ�����
# ������ڣ�2011��10��20��
################################################################################
import TradeContext

TradeContext.sysType = 'cron'

import AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaFlowControl,AfaDBFunc,os,time,datetime
from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('******�������['+TradeContext.TemplateCode+']����******')

    try:

        #=====================��ʼ�����ر��ı���================================
        TradeContext.tradeResponse=[]
        
        #=====================��ȡ��ǰϵͳʱ��==================================
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )
        #=====================������˴���======================================
        admin()
        #=============�Զ����====================
        AfaFunc.autoPackData()

        #=====================�˳�ģ��==========================================
        AfaLoggerFunc.tradeInfo('******�������['+TradeContext.TemplateCode+']�˳�******')

    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
#==========������˴���==========
def admin( ):

    #1,ǰ̨����У��
    if( (not TradeContext.existVariable( "Appno" )) or (TradeContext.existVariable( "Appno" ) and len(TradeContext.Appno) == 0 ) ):
        return AfaFlowControl.ExitThisFlow( 'A010', 'ҵ����[Appno]ֵ������!' )
    #if( (not TradeContext.existVariable( "Unitno" )) or (TradeContext.existVariable( "Unitno" ) and len(TradeContext.Unitno) == 0 ) ):
    #    return AfaFlowControl.ExitThisFlow( 'A010', '��λ���[Unitno]ֵ������!' )
    if( (not TradeContext.existVariable( "ChkDate" )) or (TradeContext.existVariable( "ChkDate" ) and len(TradeContext.ChkDate) == 0 ) ):
        return AfaFlowControl.ExitThisFlow( 'A010', '��������[ChkDate]ֵ������!' )
    
    #2,ҵ���֧����
    ProcName = []
    
    
    #a,��˰����
    if( TradeContext.Appno == 'AG2008' and ( (not TradeContext.existVariable( "Unitno" )) or ( TradeContext.existVariable( "Unitno" ) and len(TradeContext.Unitno) == 0 ) ) ):
        
        #20111028�º��޸���� ����ƫ��������
        #begin
        #TrxDate = str(int(TradeContext.ChkDate) - int(TradeContext.workDate))        
         
        AfaLoggerFunc.tradeInfo('�������ڣ�' + TradeContext.ChkDate)
        AfaLoggerFunc.tradeInfo('��ǰ���ڣ�' + TradeContext.workDate)
         
        year1  = int(TradeContext.ChkDate[0:4])                        #��
        month1 = int(TradeContext.ChkDate[4:6])                        #��
        day1   = int(TradeContext.ChkDate[6:])                         #��
        
        year2  = int(TradeContext.workDate[:4])
        month2 = int(TradeContext.workDate[4:6])
        day2   = int(TradeContext.workDate[6:])
                 
        d1 = datetime.datetime(year1, month1, day1)  
        d2 = datetime.datetime(year2, month2, day2)
       
        TrxDate = str((d1 - d2).days)                                  #����ƫ����
        AfaLoggerFunc.tradeInfo('����ƫ������' )
        AfaLoggerFunc.tradeInfo( TrxDate )
                                                                                             
        #end
        
        #����ʱ��У��
        if( int(TrxDate) > 0 ):
            AfaLoggerFunc.tradeInfo( '����ʱ�䲻�ܳ�ǰ' )
            return AfaFlowControl.ExitThisFlow( 'A010', '����ʱ�䲻�ܳ�ǰ' )
         
            
        #20111028�º�����޸�
        #begin
        #ProcName.append( 'python /home/maps/afa/application/fsyw/trade/AHFS_SCSJ.py '   + TrxDate )   
        #ProcName.append( 'python /home/maps/afa/application/fsyw/trade/AHFS_SCFC60.py ' + TrxDate )   
        
        ProcName.append( 'python /home/maps/afa/application/fsyw/trade/qinfensel.py '  + TrxDate )                # ��˰�Զ����
        ProcName.append( 'python /home/maps/afa/application/fsyw/trade/8449.py '       + TrxDate )                # ��˰�Զ�����
        ProcName.append( 'python /home/maps/afa/application/fsyw/trade/AHFS_SCSJ.py '  + TradeContext.ChkDate )   # ��˰�ϴ�������Ϣ
        
        #end
        
    #b,�Ƿ�˰����
    elif( (TradeContext.Appno == 'AG2011' or TradeContext.Appno == 'AG2013' or TradeContext.Appno == 'AG2017') and  TradeContext.existVariable( "Unitno" ) ):
        
        #����ʱ��У��        
        if( int(TradeContext.ChkDate.strip()) > int(TradeContext.workDate.strip()) ):
            AfaLoggerFunc.tradeInfo( '����ʱ�䲻�ܳ�ǰ' )
            return AfaFlowControl.ExitThisFlow( 'A010', '����ʱ�䲻�ܳ�ǰ' )
         
        
        sql = ""
        sql = sql + "select procName"
        sql = sql + " from afa_cronAdm"
        sql = sql + " where procName like '%"+ TradeContext.Appno + " " + TradeContext.Unitno +"%'"
        #�º���� 20111115
        sql = sql + " and status = '1'"
        
        AfaLoggerFunc.tradeInfo('�Ƿ�˰����afa_cron���ѯsql=' + sql )
        records = AfaDBFunc.SelectSql( sql )
        
        if (records==None):
            AfaLoggerFunc.tradeInfo('���ݿ��쳣')
            return AfaFlowControl.ExitThisFlow( 'A010', '���ݿ��쳣' )

        if (len(records)==0):
            AfaLoggerFunc.tradeInfo('��afa_cronadm��û�и�ҵ���Ӧ��λ�Ķ��˼�¼')
            return AfaFlowControl.ExitThisFlow( 'A010', '��afa_cronadm��û�и�ҵ���Ӧ��λ�Ķ��˼�¼' )
        
        if( len(records) == 1 ):
            AfaLoggerFunc.tradeInfo('��afa_cronadm�и�ҵ���Ӧ��λ�Ķ��˼�¼��ϢΪ'+records[0][0])
            
            #���˳����������
            name = records[0][0].strip() + " " + TradeContext.ChkDate
            ProcName.append( name )
        
        else:
            AfaLoggerFunc.tradeInfo('��afa_cronadm�и�ҵ���Ӧ��λ�Ķ��˼�¼��Ϣ��Ψһ����'+str(len(records)))
            return AfaFlowControl.ExitThisFlow( 'A010', '��afa_cronadm�и�ҵ���Ӧ��λ�Ķ��˼�¼��Ϣ��Ψһ' )
            
    #���ж��˳���
    AfaLoggerFunc.tradeInfo( 'Ҫ���еĶ��˳�����'+str(ProcName) )
    
    for i in range(0,len(ProcName)):
        
        #20111103 ���
        #begin
        AfaLoggerFunc.tradeInfo(">>>�жϴ˵����Ƿ���������...")
        #�жϵ�ǰϵͳ�����Ƿ���������,����������,�����µ���
        cmd = "ps -ef | grep '" + ProcName[i] + "' | grep -v grep"
        handler = os.popen(cmd,'r')
        handler_line = handler.readline()
        handler.close()
        
        if len(handler_line) > 0:
            #WrtLog( '>>>����:[ ' + ProcName[i] + ' ]����������' )
            AfaLoggerFunc.tradeInfo( '>>>����:[ ' + ProcName[i] + ' ]����������' )
            continue
        #end
        
        AfaLoggerFunc.tradeInfo( '���ж��˳���'+ProcName[i] )
        
        #os.system(ProcName[i] + ' &')   #��̨����
        os.system(ProcName[i])
        
        #time.sleep(5)
    
    
    TradeContext.errorCode = '0000'
    TradeContext.errorMsg = '���׳ɹ�'
    return True
    
