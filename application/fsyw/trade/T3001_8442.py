# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.���ղ�ѯ����
#=================================================================
#   �����ļ�:   T3001_8442.py
#   �޸�ʱ��:   2007-10-21
##################################################################
import TradeContext, AfaDBFunc, AfaLoggerFunc
from types import *

def SubModuleMainFst( ):

    TradeContext.__agentEigen__  = '0'   #�ӱ��־

    #------------------------���ݸ�ʽת��--------------
    tmpDataList             =   [k for k in TradeContext.AFC001.split(':') if k]     #��ǰ̨�����ֶ�AFC001,����Ϊ 1::::2::::3�����Ľṹ�������д��뽫�յ�ȥ�������ձ��1:2:3�����Ľṹ
    TradeContext.AFC001     =   ':'.join(tmpDataList)

    tmpDataList             =   [k.strip() for k in TradeContext.NOFEE.split(':') if ( k.strip() != '0.00' and k.strip() != '' )]     #��ǰ̨�����ֶ�AFC001,����Ϊ 1::::2::::3�����Ľṹ�������д��뽫�յ�ȥ�������ձ��1:2:3�����Ľṹ
    TradeContext.NOFEE      =   ':'.join(tmpDataList)

    tmpDataList             =   [k for k in TradeContext.AFC401.split(':') if k]     #��ǰ̨�����ֶ�AFC001,����Ϊ 1::::2::::3�����Ľṹ�������д��뽫�յ�ȥ�������ձ��1:2:3�����Ľṹ
    TradeContext.AFC401     =   ':'.join(tmpDataList)

    tmpDataList             =   [k.strip() for k in TradeContext.AFC011.split(':') if ( k.strip() != '0.00' and k.strip() != '' )]     #��ǰ̨�����ֶ�AFC001,����Ϊ 1::::2::::3�����Ľṹ�������д��뽫�յ�ȥ�������ձ��1:2:3�����Ľṹ
    TradeContext.AFC011      =   ':'.join(tmpDataList)

    AfaLoggerFunc.tradeInfo( '�ɿ����ţ�' + TradeContext.AFC001 )
    AfaLoggerFunc.tradeInfo( '�ɿ����' + TradeContext.NOFEE )

    AfaLoggerFunc.tradeInfo( '��ˮ���룺' + TradeContext.AFC401 )
    AfaLoggerFunc.tradeInfo( '��ˮ��' + TradeContext.AFC011 )

    #������������У��������˽���
    sqlstr      =   "select brno from abdt_unitinfo where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "' and brno='" + TradeContext.brno + "'"
    AfaLoggerFunc.tradeInfo(sqlstr)
    records = AfaDBFunc.SelectSql( sqlstr )
    if records == None:
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "�������ݿ��쳣"
        AfaLoggerFunc.tradeInfo(sqlstr+AfaDBFunc.sqlErrMsg)
        return False

    if( len( records)==0 ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "���������У��������˽���"
        AfaLoggerFunc.tradeInfo(sqlstr+AfaDBFunc.sqlErrMsg)
        return False

    #if ( not TradeContext.AFC401 ):
    #    TradeContext.errorCode,TradeContext.errorMsg    =   "0002","��ˮ���벻�ܿ�"
    #    return False

    AfaLoggerFunc.tradeInfo( "********************��̨���Կ�ʼ***************" )

    #---------------------------����֮ǰȷ���Ƿ���ֹ������û����ֹ������������Խ���
    for item in TradeContext.AFC401.split(":"):
        sqlstr  =   "select * from fs_fc74 where afc401 like '%" + item + "%' and flag ='*' and afc015='" + TradeContext.AFC015 + "' and BUSINO='" + TradeContext.busiNo + "'"

        #===�����������б����ֶ�,�ź��޸�===
        sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

        records = AfaDBFunc.SelectSql( sqlstr )
        if records == None:
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "�������ݿ��쳣"
            AfaLoggerFunc.tradeInfo(sqlstr+AfaDBFunc.sqlErrMsg)
            return False

        if( len( records)>0 ):
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "��ˮ��%sû������ֲ��ܹ���" %item
            AfaLoggerFunc.tradeInfo(sqlstr+AfaDBFunc.sqlErrMsg)
            return False

    #----------------------------����֮ǰȷ���Ƿ�ɹ��ѣ�����ɹ��Ѳ�������--------------------
    AfaLoggerFunc.tradeInfo( '�жϽɿ������Ƿ�ɹ���' )
    for item in TradeContext.AFC001.split(":"):
        sqlstr  =   "select flag from fs_fc76 where afc001='" + item + "'"


        #===�����������б����ֶ�,�ź��޸�===
        sqlstr  =   sqlstr + " and afc153 = '" + TradeContext.bankbm + "'"

        records = AfaDBFunc.SelectSql( sqlstr )
        if ( len(records) == 0 ):
            AfaLoggerFunc.tradeInfo( "�ɿ�����û�нɷ�%s���Թ���" %item )
            AfaLoggerFunc.tradeInfo( sqlstr )
        else:
            if records[0][0]   ==  '0':
                TradeContext.errorCode,TradeContext.errorMsg  =   '0001','��������%s�Ѿ��ɷѲ��ܹ���' %item
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False

    #------------------------------��������������½������ȼ����Ƿ񹴶Թ�����ӵ����ݿ���---------------------
    if TradeContext.opType == '1':
        for item in TradeContext.AFC401.split(":"):
            #-----------------�����ˮ�����Ƿ񹴶Թ�--------------------
            sqlstr = "select afc001 from fs_fc74 where afc401 = '" + item + "' and afc015='" + TradeContext.AFC015 + "' and BUSINO='" + TradeContext.busiNo +  "' and length(afc001)=0 and flag!='*'"

            #===�����������б����ֶ�,�ź��޸�===
            sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

            records = AfaDBFunc.SelectSql( sqlstr )

            if( records == None ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "���ݿ��쳣�������"
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False

            if(  len( records)==0 ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "��ˮ����%s�Ѿ����Թ�" %item
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                AfaLoggerFunc.tradeInfo( sqlstr )
                return False

        for payNo in TradeContext.AFC001.split(':'):
            #------------------���ɿ������Ƿ񹴶Թ�--------------------
            sqlstr = "select afc001 from fs_fc74 where afc001 like '%" + payNo + "%' and flag!='*' and BUSINO='" + TradeContext.busiNo +  "'"

            #===�����������б����ֶ�,�ź��޸�===
            sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

            records = AfaDBFunc.SelectSql( sqlstr )

            if( records == None ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "���ݿ��쳣�������"
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False

            if(  len( records)>0 ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "�ɿ�����%s�Ѿ����Թ�" %payNo
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False

        #-------------------��������ӵ����ݿ���------------------------------------
        for item in TradeContext.AFC401.split(":"):
            sqlstr      =   "update fs_fc74 set afc001='" + TradeContext.AFC001  + "',nofee='" + TradeContext.NOFEE + "',flag='0' where afc401='" + item + "' and afc015='" + TradeContext.AFC015 + "' and BUSINO='" + TradeContext.busiNo +  "'"

            #===�����������б����ֶ�,�ź��޸�===
            sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

            AfaLoggerFunc.tradeInfo( sqlstr )
            if( AfaDBFunc.UpdateSql( sqlstr ) < 1 ) :
                AfaDBFunc.RollbackSql()
                TradeContext.errorCode, TradeContext.errorMsg='0001', '���´������ݱ�ʧ��'
                AfaLoggerFunc.tradeInfo( sqlstr+AfaDBFunc.sqlErrMsg )
                return False

            AfaDBFunc.CommitSql( )

    #-------------����������ɾ��----------------
    elif TradeContext.opType == '2':

        #------------------------------ɾ��������е�����---------------------------
        for item in TradeContext.AFC401.split(":"):
            sqlstr      =   "update fs_fc74 set afc001='',nofee='',flag='1' where afc401='" + item + "' and afc015='" + TradeContext.AFC015 + "'"

            #===�����������б����ֶ�,�ź��޸�===
            sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

            AfaLoggerFunc.tradeInfo( sqlstr )
            if( AfaDBFunc.UpdateSql( sqlstr ) < 1 ) :
                AfaDBFunc.RollbackSql()
                TradeContext.errorCode, TradeContext.errorMsg='0001', '���´������ݱ�ʧ��'
                AfaLoggerFunc.tradeInfo( sqlstr+AfaDBFunc.sqlErrMsg )
                return False

            AfaDBFunc.CommitSql( )

        #-----------------------��ʼɾ����¼���е�����-------------------------------
        sqlstr  =   "select afc401,date from fs_fc84 where afc001='"

        for payNo in TradeContext.AFC001.split(':'):
            sqlstr      =   "select afc401,date from fs_fc84 where"
            condition   =    " afc001='" + payNo + "'"

            for serNo in TradeContext.AFC401.split(':'):
                condition  =   condition + " and afc401 like '%" + serNo + "%'"
             
            #begin 20100625 ���������Ӳ�ѯ���� 
            condition   = condition + " and afa101 = '" + TradeContext.bankbm + "'"
            #end
   
            sqlstr      =   sqlstr + condition

            #===�����������б����ֶ�,�ź��޸�===
            #sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

            AfaLoggerFunc.tradeInfo( sqlstr )
            records = AfaDBFunc.SelectSql( sqlstr )
            AfaLoggerFunc.tradeInfo( '���ݿⳤ�ȣ�' + str( len(records) ) )

            if len(records) == 0:
                AfaLoggerFunc.tradeInfo( 'û�в��ҵ���¼��Ϣ����ɾ��' )
                continue

            #---------------------------����ɾ����ǰ�Ѿ��ϴ��Ĳ�¼����---------------------------
            if records[0][1].strip() < TradeContext.workDate :
                TradeContext.errorCode,TradeContext.errorMsg    =   '0001','�������Ѿ��ϴ�����ɾ��'
                return False

            #���ҵ��˲�¼��Ϣ��ɾ����ˮ��
            if( len( records) == 1 ):

                sqlstr  =   "delete from fs_fc84 where " + condition

                #===�����������б����ֶ�,�ź��޸�===
                #sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

                AfaLoggerFunc.tradeInfo( sqlstr )
                if( AfaDBFunc.DeleteSql( sqlstr ) < 1 ) :
                    AfaDBFunc.RollbackSql()
                    TradeContext.errorCode, TradeContext.errorMsg='0001', 'ɾ����¼����ʧ��'
                    AfaLoggerFunc.tradeInfo( sqlstr+AfaDBFunc.sqlErrMsg )
                    return False

                AfaDBFunc.CommitSql( )
                AfaLoggerFunc.tradeInfo( 'ɾ����¼���ݳɹ����ýɿ�����:%s' %payNo )

            #������ҳ����ļ�¼��������1����˵����¼���ݴ���
            elif len( records) > 1 :
                AfaLoggerFunc.tradeInfo( '��¼���ݴ��󣬽ɿ����ţ���ˮ�����Ӧ���������ϼ�¼' )
                AfaLoggerFunc.tradeInfo( '�ɿ�����' + payNo )
                AfaLoggerFunc.tradeInfo( '��ˮ����' + TradeContext.AFC401 )
                TradeContext.errorCode, TradeContext.errorMsg='0000', '����ɾ��ʧ��'
                return False
    else:
        TradeContext.errorCode, TradeContext.errorMsg='0001', '���������쳣'
        AfaLoggerFunc.tradeInfo( sqlstr+AfaDBFunc.sqlErrMsg )
        return False

    TradeContext.errorCode, TradeContext.errorMsg='0000', '�������ݳɹ�'
    AfaLoggerFunc.tradeInfo( "********************��̨���Խ���***************" )
    return True
