# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   TTJYW003_8498.py
#   ����˵��:   �ɷ���ϸ��ѯ
#   �޸�ʱ��:   2011-01-06
##################################################################
import TradeContext, AfaLoggerFunc,AfaFlowControl,AfaDBFunc,os
from types import *

def SubModuleDoFst( ):

    try:
        CrtJKMXFile( )
        TradeContext.count = "1"
        AfaLoggerFunc.tradeInfo(TradeContext.count)
        return True
    except  Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        AfaFlowControl.flowException( )

def CrtJKMXFile( ):
    
    try:
        sql = " select workdate,worktime,note3,amount,username,note1 from afa_maintransdtl"
        sql = sql + " where substr(workdate,1,6)='" + TradeContext.month  + "'"                         #�ɿ�����
        sql = sql + " and   sysid='"                + TradeContext.appno  + "'"                         #ҵ����
        sql = sql + " and   unitno='"               + TradeContext.unitno + "'"                         #��λ���
        sql = sql + " and revtranf = '0' and bankstatus = '0' and ChkFlag = '0'"
        
        #20120709�º���� note2 ---busino��λ����
        sql = sql + " and    note2   = '"           + TradeContext.busino +"'"                          #��λ����
        
        AfaLoggerFunc.tradeInfo( "�ɿ���ϸ��ѯsql��" + sql )
        
        results = AfaDBFunc.SelectSql( sql )
        TradeContext.RecAllCount = str(len(results))
        
        if results == None:
            AfaLoggerFunc.tradeInfo( '��ѯ�ɿ���ϸ���ݿ��쳣' )
            return False
        elif len(results) == 0:
            AfaLoggerFunc.tradeInfo( '����û�нɿ���ϸ��¼' )
            TradeContext.errorCode = "E0001"
            TradeContext.errorMsg  = "����û�нɿ���ϸ��¼"
            return False
        else:
            AfaLoggerFunc.tradeInfo( '���ڽɿ���ϸ' )
        
        #����ÿ�½ɿ���ϸ�����ļ�
        mFileName = os.environ['HOME'] + "/afa/data/tjyw/report/P" + TradeContext.brno + "_" + TradeContext.tellerno + "_" + TradeContext.unitno + "_" + TradeContext.month + ".TXT"
        TradeContext.filename = "P" + TradeContext.brno + "_" + TradeContext.tellerno + "_" + TradeContext.unitno + "_" + TradeContext.month + ".TXT"
        AfaLoggerFunc.tradeInfo( '��ʼ���ɽɿ���ϸ�����ļ���' + mFileName )
        AfaLoggerFunc.tradeInfo( TradeContext.filename )
        dfp = open( mFileName,"w" )
        
        tmpStr = "".ljust(116,"-") + "\n"
        #tmpStr = tmpStr + "".ljust(30)  + "�����л����ʽɿ���ϸ" + "\n"
        tmpStr = tmpStr + "".ljust(30)  + "����ɿ���ϸ" + "\n"
        tmpStr = tmpStr + "\n"
        tmpStr = tmpStr + "�ɿ��·ݣ�" + TradeContext.month + "\n"
        tmpStr = tmpStr + "\n"
        tmpStr = tmpStr + "".ljust(116,"-") + "\n"
        tmpStr = tmpStr + "�ɿ�����".ljust(14)
        tmpStr = tmpStr + "�ɿ�ʱ��".ljust(14)
        tmpStr = tmpStr + "���׻�������".ljust(40)
        tmpStr = tmpStr + "���".ljust(14)
        tmpStr = tmpStr + "�ɿ�������".ljust(20)
        tmpStr = tmpStr + "��ϵ�绰".ljust(14) + "\n"
        
        dfp.write( tmpStr )
        
        for i in range( 0,len(results) ):
            tmpStr =          results[i][0].lstrip().rstrip().ljust(14)          #�ɿ�����
            tmpStr = tmpStr + results[i][1].lstrip().rstrip().ljust(14)          #�ɿ�ʱ��
            tmpStr = tmpStr + results[i][2].lstrip().rstrip().ljust(40)          #���׻�������
            tmpStr = tmpStr + results[i][3].lstrip().rstrip().ljust(14)          #���
            tmpStr = tmpStr + results[i][4].lstrip().rstrip().ljust(20)          #�ɿ�������
            tmpStr = tmpStr + results[i][5].lstrip().rstrip().ljust(14)          #��ϵ�绰
            dfp.write( tmpStr + "\n" )
        dfp.close( )
        AfaLoggerFunc.tradeInfo( '���ɽɿ���ϸ�����ļ���' + mFileName + "�ɹ�")
        return True
        
    except  Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        AfaFlowControl.flowException( )
      
