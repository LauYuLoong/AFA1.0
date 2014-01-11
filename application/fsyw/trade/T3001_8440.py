# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.���ղ�ѯ����
#=================================================================
#   �����ļ�:   T3001_8440.py
#   �޸�ʱ��:   2007-10-21
##################################################################
import TradeContext, AfaDBFunc, AfaLoggerFunc,AfaFlowControl
from types import *

def SubModuleMainFst( ):

    TradeContext.__agentEigen__  = '0'   #�ӱ��־

    TradeContext.AFC001         =   TradeContext.userNo

    AfaLoggerFunc.tradeInfo( "��̨�������ݿ⿪ʼ" )

    #fieldList                  =   "AFA031,AFC163,AFC187,AFC183,AFC157,AFC181,AFA040,AFC180,AFA051,AFC166,AFC155,AFC153,AFC154,AFA183,AFA184,AFA185,AFA091,AAA010"

    #����̨���ݿ��в�ѯ
    sqlstr                      =   "select AFA031,AFC181,AFA040,AFC180,   \
                                    AFC163,AFC187,AFC183,AFC157,AFA051,AFC166,AFC155,AFC153,AFC154,  \
                                    AFA183,AFA184,AFA185,AFA091,AAA010 from FS_FC70 where AFC001='" + TradeContext.AFC001 + " ' "
    #�������б����ֶ�,�ź��޸�
    sqlstr = sqlstr + " and afc153 = '" + TradeContext.bankbm + "'"

    AfaLoggerFunc.tradeInfo( sqlstr )
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None or len( records)==0 ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "û�в��ҵ��ɿ�����Ϣ"
        AfaLoggerFunc.tradeInfo( "***************��̨�������ݿ����*******************" )
        return False
    else:
        TradeContext.AFC163     =   records[0][4]
        TradeContext.AFC187     =   records[0][5]
        TradeContext.AFC183     =   records[0][6]
        TradeContext.AFC157     =   records[0][7]
        TradeContext.AFA051     =   records[0][8]
        TradeContext.AFC166     =   records[0][9]
        TradeContext.AFC155     =   records[0][10]
        TradeContext.AFC153     =   records[0][11]
        TradeContext.AFC154     =   records[0][12]
        TradeContext.AFA183     =   records[0][13]
        TradeContext.AFA184     =   records[0][14]
        TradeContext.AFA185     =   records[0][15]
        TradeContext.AFA091     =   records[0][16]
        TradeContext.AAA010     =   records[0][17]


        recCnt                  =   len(records)
        #��Щ�ֶ���Ҫ���ɶ�� AFC181	(	���    ),AFA040	(	������λ),AFC180	(	����    ),AFA031	(	��Ŀ����)
        if recCnt == 1:

            #�����ҵ�����Ϣ��ֵ��TradeContext��
            TradeContext.errorCode  =   "0000"
            TradeContext.errorMsg   =   "���ҽɿ�����Ϣ�ɹ�"

            TradeContext.RECCNT     =   str( len(records) )
            TradeContext.AFA031     =   records[0][0]
            TradeContext.AFC181     =   records[0][1]
            TradeContext.AFA040     =   records[0][2]
            TradeContext.AFC180     =   records[0][3]

            AfaLoggerFunc.tradeInfo( "һ���ɿ����Ӧһ���շ���Ŀ" )

        elif recCnt > 1  and recCnt <= 3 :

            #�����ҵ�����Ϣ��ֵ��TradeContext��
            TradeContext.errorCode  =   "0000"
            TradeContext.errorMsg   =   "���ҽɿ�����Ϣ�ɹ�"
            TradeContext.RECCNT     =   str(len(records))

            fields                  =   "AFA031,AFC181,AFA040,AFC180"

            index                   =   0                   #�ֶ����±�
            for field  in fields.split(","):
                item                =   []
                for i in range(recCnt):
                    item.append(records[i][index])

                if item == None :
                    return False

                value               =   "^".join(item)
                setattr(TradeContext,field,value)
                index               =   index + 1           #��ʼ��һ���ֶ�

                AfaLoggerFunc.tradeInfo( "һ���ɿ����Ӧ����շ���Ŀ" )
                AfaLoggerFunc.tradeInfo( field + "***" + value )

        else:
            AfaLoggerFunc.tradeInfo( "һ�������Ŷ�Ӧ�Ľɷ���Ŀ����������" )
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "���ҽɿ�����Ϣʧ��"
            return False


    AfaLoggerFunc.tradeInfo( ">>>��ʼ��ѯִ�յ�λ����" )
    #��ѯִ�յ�λ����
    sqlstr  =   "select afa052 from fs_fa15 where afa051='" + TradeContext.AFA051 + "' and BUSINO='" + TradeContext.busiNo + "'"
    sqlstr  =   sqlstr + " and aaa010='" + TradeContext.AAA010 + "'"
    #=====������ 20080827 ��ѯִ�յ�λ����ʱ,���Ӳ�������������Ϊ��ѯ����====

    records = AfaDBFunc.SelectSql( sqlstr )
    if ( records == None or len(records) == 0 ):
        AfaLoggerFunc.tradeInfo( sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "û�в��ҵ�ִ�յ�λ����"
        return False

    TradeContext.AFA052         =   records[0][0]               #ִ�յ�λ����
    AfaLoggerFunc.tradeInfo( ">>>ִ�յ�λ����[" + TradeContext.AFA052 + "]")


    AfaLoggerFunc.tradeInfo( ">>>��ʼ��ѯִ����Ŀ����" )
    #��ѯִ����Ŀ����
    sqlstr      =   ""
    value       =   []
    AfaLoggerFunc.tradeInfo(TradeContext.RECCNT )

    for i in range( 0,int(TradeContext.RECCNT) ):
        sqlstr  =   "select afa032,afa030 from fs_fa13 where afa031='" + (TradeContext.AFA031.split("^"))[i]  + "' and BUSINO='" + TradeContext.busiNo + "' order by aaz006 desc"
        AfaLoggerFunc.tradeInfo(sqlstr)

        records = AfaDBFunc.SelectSql( sqlstr )

        AfaLoggerFunc.tradeInfo(str(records))

        if ( records == None or len(records) == 0 ):
            AfaLoggerFunc.tradeInfo( sqlstr )
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "û�в��ҵ�ִ����Ŀ����"
            return False
        AfaLoggerFunc.tradeInfo(str(i))
        value.append(records[0][0])

        TradeContext.AFA032             =   "^".join(value)
        AfaLoggerFunc.tradeInfo( ">>>ִ����Ŀ����[" + TradeContext.AFA032 + "]")

    AfaLoggerFunc.tradeInfo( ">>>��ʼ��ѯ������������" )
    #��ѯ������������
    sqlstr      =   ""
    value       =   []
    sqlstr  =   "select afa102 from fs_fa22 where afa101='" + TradeContext.AFC153 + "' and BUSINO='" + TradeContext.busiNo + "'"
    sqlstr  =   sqlstr + " and aaa010='" + TradeContext.AAA010 + "'"

    records = AfaDBFunc.SelectSql( sqlstr )
    if ( records == None or len(records) == 0 ):
        AfaLoggerFunc.tradeInfo( sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "û�в��ҵ�������������"
        return False

    TradeContext.AFC154         =   records[0][0]               #������������
    AfaLoggerFunc.tradeInfo( ">>>������������[" + TradeContext.AFC154 + "]")

    AfaLoggerFunc.tradeInfo(TradeContext.AFA052 + TradeContext.AFA032 + TradeContext.AFC154 +"AAAAAAAAAA")

    AfaLoggerFunc.tradeInfo( "********************��̨�������ݿ����***************" )
    return True
