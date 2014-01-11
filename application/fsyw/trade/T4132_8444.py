# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.�˸�����
#=================================================================
#   �����ļ�:   4102_8444.py
#   �޸�ʱ��:   2007-10-11
##################################################################
import TradeContext, AfaDBFunc, AfaLoggerFunc,AfaFlowControl
from types import *

def SubModuleDoFst():

    AfaLoggerFunc.tradeInfo( '�˸���ʼ' )


    #=====������  20080811  ��������fa15���в�����������,����Ϊ��λ����====
    #sql = "select AAA010 from fs_fa15 where AFA050='" + TradeContext.busiNo + "'"
    sql = "select AAA010 from fs_fa22 where busino='" + TradeContext.busiNo + "'"
    
    #begin 20100629 ���������Ӳ�ѯ����
    sql = sql + " and AFA101 = '" + TradeContext.bankbm + "'"
    AfaLoggerFunc.tradeInfo( sql )
    #end

    ret = AfaDBFunc.SelectSql( sql )
    if ret == None:
        return AfaFlowControl.ExitThisFlow('0001','ͨ����λ������Ҳ�����������ʧ��')
    elif len(ret) <= 0:
        return AfaFlowControl.ExitThisFlow('0001','ͨ����λ������Ҳ�����������������������¼')
    else:
        TradeContext.AAA010  =  ret[0][0]


    TradeContext.__agentEigen__ = '0'   #�ӱ��־

    #���ֶ�ת��Ϊ�˸�������ʹ�õ��ֶ�
    TradeContext.AFC060         =   TradeContext.userNo
    TradeContext.AFA050         =   TradeContext.note1
    TradeContext.AFC064         =   TradeContext.amount
    TradeContext.AFC063         =   TradeContext.accno

    #=====������  20080811  ��������������������====
    #sqlstr                      =   "select flag from fs_fc75 where afc060='" + TradeContext.AFC060 + "'"
    sqlstr                      =   "select flag from fs_fc75 where afc060='" + TradeContext.AFC060 + "'"

    sqlstr = sqlstr + " and AAA010 = '" + TradeContext.AAA010 + "'"

    #===�����������б����ֶ�,�ź��޸�===
    sqlstr = sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

    records                     =   AfaDBFunc.SelectSql( sqlstr )

    AfaLoggerFunc.tradeInfo( '�˸���ѯ' + sqlstr )

    if ( len(records) > 0 ):
        if records[0][0]   ==  '0':
            TradeContext.errorCode,TradeContext.errorMsg  =   '0001','�Ѿ����ҵ����˸���ţ������ٴ��˸�'
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False


        elif records[0][0] != '1':
            TradeContext.errorCode,TradeContext.errorMsg  =   '0002',"�ɿ���״̬λ�쳣"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False

    return True


def SubModuleDoFstMore():

    #��������ʺŻ���
    tmp                         =   TradeContext.accno
    TradeContext.accno          =   TradeContext.__agentAccno__     #�跽
    TradeContext.__agentAccno__ =   tmp
    #begin 20100701 ����������
    TradeContext.Daccno         =   tmp                             #����
    #end
    
    AfaLoggerFunc.tradeInfo("�跽�˺�:" + TradeContext.accno)
    AfaLoggerFunc.tradeInfo("�����˺�:" + TradeContext.__agentAccno__)

    if TradeContext.vouhNo :
        TradeContext.vouhType   =   TradeContext.vouhNo[0:2]
        TradeContext.vouhNo     =   TradeContext.vouhNo[2:]
    else:
        TradeContext.vouhType   =   '99'
    return True


def SubModuledoSnd():

    #���˸���Ϣд���������ݿ�����
    sqlstr  =   "insert into FS_FC75(AAA010,AFC060,AFC041,AFA050,AFC061,AFC062,AFC063,AFC064,FBLRQ,AFA101,BUSINO,TELLER,BRNO,FLAG,DATE,TIME) values("
    FLAG    =   '0'
    sqlstr          =   sqlstr + "'" + TradeContext.AAA010   + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.AFC060   + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.AFC041   + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.AFA050   + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.AFC061   + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.AFC062   + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.AFC063   + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.AFC064   + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.FBLRQ    + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.bankbm   + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.busiNo   + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.teller   + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.brno     + "',"
    sqlstr          =   sqlstr + "'" + FLAG                  + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.workDate + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.workTime + "')"

    TradeContext.errorCode  =   "0000"
    TradeContext.errorMsg   =   "�˸��ɹ�"

    if( AfaDBFunc.InsertSql( sqlstr ) < 1 ):
        AfaDBFunc.RollbackSql( )
        AfaLoggerFunc.tradeInfo( '�����˸���Ϣ��ʧ��' + sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "�˸�ʧ��"
        return False

    AfaDBFunc.CommitSql( )

    AfaLoggerFunc.tradeInfo( '�����˸���Ϣ�����' )


    #��ģ����Ҫ��Ϊ����д��Ʊ����
    if (TradeContext.channelCode =='001' ): #���潻�ײ��Ʒ�Ʊ
        TradeContext.__billSaveCtl__  = '0'
    else:
        TradeContext.__billSaveCtl__  = '1'

    bill    =   []
    bill.append('1')
    bill.append('')
    bill.append('')
    bill.append('')
    bill.append('')
    bill.append('')
    bill.append('')
    bill.append('')

    return bill
