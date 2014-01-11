# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.���ղ�ѯ����
#=================================================================
#   �����ļ�:   T3001_8478.py
#   �޸�ʱ��:   2007-10-21
##################################################################
import TradeContext, AfaLoggerFunc, AfaDBFunc
from types import *

def SubModuleMainFst( ):

    TradeContext.__agentEigen__  = '0'   #�ӱ��־

    AfaLoggerFunc.tradeInfo( "��̨��λ������Ϣά����ʼ" )

    #�жϲ�������
    if TradeContext.opType == '1':
        AfaLoggerFunc.tradeInfo( "����" )

        sqlstr  =   "select * from fs_businoinfo where busino='" + TradeContext.busiNo + "'"
        sqlstr  =   sqlstr + " and bankno = '" + TradeContext.bankbm + "'"

        AfaLoggerFunc.tradeInfo('>>>sql=' + sqlstr)

        records = AfaDBFunc.SelectSql( sqlstr )
        if records == None :
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "���ҵ�λ������Ϣ�쳣"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False

        if len(records) >=1 :
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "�Ѿ����ҵ���λ������Ϣ�������ٴ��½�"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False

        #����У�������˻��������Ƿ���ȷ
        #�ź��޸�AG2012
        sqlstr  =   "select accno,businame from abdt_unitinfo where appno ='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "'"
        AfaLoggerFunc.tradeInfo('>>>sql=' + sqlstr)

        records = AfaDBFunc.SelectSql( sqlstr )
        if( records == None or len( records)==0 ):
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "û�в��ҵ���λ�����˻���Ϣ"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False
        else:
            if records[0][0].strip() != TradeContext.accno  or records[0][1].strip() and records[0][1].strip() != TradeContext.name :
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "��λ�����˻���Ϣ����"
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False

        #У���������б�������������Ƿ���ȷ
        sqlstr  =   "select afa102 from fs_fa22 where afa101='" + TradeContext.bankNo + "'"

        AfaLoggerFunc.tradeInfo('>>>sql=' + sqlstr)

        records = AfaDBFunc.SelectSql( sqlstr )
        if( records == None ):
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "���ҵ���λ�����˻���Ϣ�쳣"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False

        if len(records) == 0:
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "���б��벻����"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False
        else:
            #=====������  20080815  �������ڴ������б�����ͬ������¼�Ĵ���====
            for i in range(0,len(records)):
                if records[i][0].strip() != TradeContext.bankName :
                    TradeContext.errorCode = '0011'
                    TradeContext.errorMsg  = '���б������������Ʋ���'
                    AfaLoggerFunc.tradeInfo('>>>��������['+str(records[i][0])+']���Ա������������['+TradeContext.bankName+']����')
                    if int(len(records)-1) == i:
                        return False
                else:
                    AfaLoggerFunc.tradeInfo('>>>��������['+str(records[i][0])+']���Ա������������['+TradeContext.bankName+']���')
                    break

            #if records[0][0].strip() != TradeContext.bankName :
            #    TradeContext.errorCode  =   "0001"
            #    TradeContext.errorMsg   =   "���б������������ֲ���"
            #    AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            #    return False

        #У�����������Ϣ
        sqlstr  =   "select aaa012 from fs_aa11 where aaa010='" + TradeContext.AAA010 + "'"

        AfaLoggerFunc.tradeInfo('>>>sql=' + sqlstr)

        records = AfaDBFunc.SelectSql( sqlstr )
        AfaLoggerFunc.tradeInfo(str(records))
        if( records == None ):
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "���ҵ���λ�������������Ϣ�쳣"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False

        if len(records) == 0:
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "�����������벻����"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False
        else:
            if records[0][0].strip() != TradeContext.AAA012 :
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "������������������������Ʋ���"
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                AfaLoggerFunc.tradeInfo( records[0][0].strip() )
                return False

        #ͨ��У�飬���뵽���ݿ���
        sqlstr  =   "insert into fs_businoinfo ( BUSINO,ACCNO,NAME,AAA010,AAA012,BANKNO,BANKNAME,BANKBRNO,BRNO,TELLER,DATE,TIME,CTRYBANKNO,CTRYBANKNAME ) values("

        sqlstr  =   sqlstr + "'" + TradeContext.busiNo      + "',"
        sqlstr  =   sqlstr + "'" + TradeContext.accno       + "',"
        sqlstr  =   sqlstr + "'" + TradeContext.name        + "',"
        sqlstr  =   sqlstr + "'" + TradeContext.AAA010      + "',"
        sqlstr  =   sqlstr + "'" + TradeContext.AAA012      + "',"
        sqlstr  =   sqlstr + "'" + TradeContext.bankNo      + "',"
        sqlstr  =   sqlstr + "'" + TradeContext.bankName    + "',"
        sqlstr  =   sqlstr + "'" + TradeContext.busiNo[0:10]+ "',"
        sqlstr  =   sqlstr + "'" + TradeContext.brno        + "',"
        sqlstr  =   sqlstr + "'" + TradeContext.teller      + "',"
        sqlstr  =   sqlstr + "'" + TradeContext.workDate    + "',"
        sqlstr  =   sqlstr + "'" + TradeContext.workTime    + "',"
        sqlstr  =   sqlstr + "'',"
        sqlstr  =   sqlstr + "'')"

        AfaLoggerFunc.tradeInfo('>>>sql=' + sqlstr)

        if( AfaDBFunc.InsertSql( sqlstr ) < 1 ):
                AfaDBFunc.RollbackSql( )
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001",'���뵥λ������Ϣ��ʧ��' + sqlstr
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                return False

        AfaDBFunc.CommitSql( )

    #�޸�
    elif TradeContext.opType == '2':
        AfaLoggerFunc.tradeInfo( "�޸�" )

        sqlstr  =   "update fs_businoinfo set accno='" + TradeContext.accno + "',name='" + TradeContext.name + "',"  + \
        "aaa010='" + TradeContext.AAA010 + "',aaa012='" + TradeContext.AAA012 + "',date='" + TradeContext.workDate + "'," + \
        "time='" + TradeContext.workTime + "',brno='" + TradeContext.brno + "',teller='" + TradeContext.teller + "'," + \
        "bankno = '" + TradeContext.bankNo + "' where busino='" + TradeContext.busiNo + "'"
        #=====������ 20080821 �����޸Ĳ���====

        AfaLoggerFunc.tradeInfo('>>>sql=' + sqlstr)

        if( AfaDBFunc.UpdateSql( sqlstr ) < 1 ):
                AfaDBFunc.RollbackSql( )
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001",'���µ�λ������Ϣ��ʧ��' + sqlstr
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                return False

        AfaDBFunc.CommitSql( )

    #ɾ��
    elif TradeContext.opType == '3':
        AfaLoggerFunc.tradeInfo( "ɾ��" )

        sqlstr = "delete from fs_businoinfo where busino='" + TradeContext.busiNo + "'"

        AfaLoggerFunc.tradeInfo('>>>sql=' + sqlstr)

        if( AfaDBFunc.DeleteSql( sqlstr ) < 1 ):
                AfaDBFunc.RollbackSql( )
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001",'ɾ����λ������Ϣ��ʧ��' + sqlstr
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                return False

        AfaDBFunc.CommitSql( )

    TradeContext.errorCode,TradeContext.errorMsg    =   "0000",'������λ������Ϣ��ɹ�'
    AfaLoggerFunc.tradeInfo( "********************��̨��λ������Ϣά������***************" )
    return True
