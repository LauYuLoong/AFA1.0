# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.���ղ�ѯ����
#=================================================================
#   �����ļ�:   T3001_8448.py
#   �޸�ʱ��:   2007-10-21
##################################################################
import TradeContext, AfaDBFunc, AfaLoggerFunc,AfaFlowControl
from types import *

def SubModuleMainFst( ):

    #=====������  20080811  ��������fa15���в�����������,����Ϊ��λ����====
    AfaLoggerFunc.tradeInfo( ">>>AFA050=" + TradeContext.busiNo)
    sql = "select AAA010 from fs_fa22 where busino='" + TradeContext.busiNo + "'"

    #begin 20100629 ���������Ӳ�ѯ����
    sql = sql + " and afa101 = '" + TradeContext.bankbm + "'"
    AfaLoggerFunc.tradeInfo( sql )
    #end

    ret = AfaDBFunc.SelectSql( sql )
    if ret == None:
        return AfaFlowControl.ExitThisFlow('0001','ͨ����λ������Ҳ�����������ʧ��')
    elif len(ret) <= 0:
        return AfaFlowControl.ExitThisFlow('0001','ͨ����λ������Ҳ�����������������������¼')
    else:
        TradeContext.AAA010  =  ret[0][0]
        
    TradeContext.__agentEigen__  = '0'   #�ӱ��־
    
    AfaLoggerFunc.tradeInfo( "��̨�������ݿ⿪ʼ" )
        
    #����̨���ݿ��в�ѯ
    #=====������  20080811  ��������������������====
    #sqlstr = "select AFC306,AAA010,AFA050,AFC041,AFC061,AFC062,AFC063,AFC064,AAZ016,AAZ015 from FS_FC06 where AFC060='" + TradeContext.AFC060 + "'"
    
    sqlstr = "select AFC306,AAA010,AFA050,AFC041,AFC061,AFC062,AFC063,AFC064,AAZ016,AAZ015 from FS_FC06 where AFC060='" + TradeContext.AFC060 + "'"
    sqlstr = sqlstr + " AND AAA010 = '" + TradeContext.AAA010 + "'"
    
    AfaLoggerFunc.tradeInfo( sqlstr )
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None or len( records)==0 ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "�����˸���Ϣʧ��"
        AfaLoggerFunc.tradeInfo( "***************��̨�������ݿ����*******************" )
        return False

    elif ( len( records )==1 ):

        #�����ҵ�����Ϣ��ֵ��TradeContext��
        TradeContext.AFC306     =   records[0][0]
        TradeContext.AAA010     =   records[0][1]
        TradeContext.AFA050     =   records[0][2]
        TradeContext.AFC041     =   records[0][3]
        TradeContext.AFC061     =   records[0][4]
        TradeContext.AFC062     =   records[0][5]
        TradeContext.AFC063     =   records[0][6]
        TradeContext.AFC064     =   records[0][7]
        TradeContext.AAZ016     =   records[0][8]
        TradeContext.AAZ015     =   records[0][9]
        
        if not (TradeContext.AAZ015.strip()  == '1') :
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "���˸���Ų����˸�"
            return False 
        
        #���ݲ������������ѯ��������
        
        if TradeContext.AAA010 :
            sqlstr  =   ""
            sqlstr  =   "select aaa012 from fs_aa11 where aaa010='" + TradeContext.AAA010 + "'"
            records = AfaDBFunc.SelectSql( sqlstr )
            if( records == None or len( records)==0 ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "���Ҳ�������ʧ��"
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False
            else:   
                TradeContext.AAA012     =   records[0][0]
        else:
            TradeContext.AAA012         =   ''
            
        #����ִ�յ�λ�����ѯ���յ�λ����
        if TradeContext.AFA050:
            sqlstr  =   ""
            sqlstr  =   "select afa052 from fs_fa15 where afa050='" + TradeContext.AFA050 + "'"
            AfaLoggerFunc.tradeInfo( sqlstr )
            records = AfaDBFunc.SelectSql( sqlstr )
            if( records == None or len( records)==0 ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "����ִ�յ�λ����ʧ��"
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False
            else:   
                TradeContext.AFA052     =   records[0][0]
        else:
            TradeContext.AFA052         =   ''
            
        #�����շ���Ŀ�����ѯ�շ���Ŀ����
        if TradeContext.AFC041 :
            sqlstr  =   ""
            sqlstr  =   "select afa032 from fs_fa13 where afa030='" + TradeContext.AFC041 + "'"
            AfaLoggerFunc.tradeInfo( sqlstr )
            records = AfaDBFunc.SelectSql( sqlstr )
            if( records == None or len( records)==0 ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "������Ŀ��������ʧ��"
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False
            else:   
                TradeContext.AFA032     =   records[0][0]
        else:
            TradeContext.AFA032         =   ''       
        
        TradeContext.errorCode  =   "0000"
        TradeContext.errorMsg   =   "�����˸���Ϣ�ɹ�"
        AfaLoggerFunc.tradeInfo( "********************��̨�������ݿ����***************" )
        return True
        
    else:
        TradeContext.errorCode  =   "9999"
        TradeContext.errorMsg   =   "���ֶ����˸���¼,���ܽ����˸�����(��������)"
        return False
