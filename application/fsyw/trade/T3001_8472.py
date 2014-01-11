#-*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.���ղ�ѯ����
#=================================================================
#   �����ļ�:   T3001_8472.py
#   �޸�ʱ��:   2007-10-21
##################################################################
import TradeContext, AfaDBFunc, AfaLoggerFunc
from types import *

def SubModuleMainFst( ):

    TradeContext.__agentEigen__  = '0'   #�ӱ��־

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

    AfaLoggerFunc.tradeInfo( "********************��̨����Ʊ����ˮ��ѯ��ʼ***************" )
    sqlstr          =   "select AFC401,AFC011,AFC001,nofee from fs_fc74 where afc001 like '%" + TradeContext.findNo + "%' and busino='" + TradeContext.busiNo + "' and afc016='" + TradeContext.brno + "' and flag !='*' "

    #===�����������б����ֶ�,�ź��޸�===
    sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

    AfaLoggerFunc.tradeInfo(sqlstr)
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None or len( records)==0 ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "û�в鵽����Ʊ����ˮ��Ϣ"
        AfaLoggerFunc.tradeInfo(sqlstr+AfaDBFunc.sqlErrMsg)
        return False
    else:
        recCnt                  =   len(records)            #��¼����
        TradeContext.RECCNT     =   str ( recCnt )

        #��������
        serNoMap                =   {}          #��ˮ���ֵ䣬������ˮ�������ˮ���ļ�ֵ��
        NoMap                   =   {}          #�ɿ������ֵ䣬����ɿ����źͽɿ�����ļ�ֵ��
        for i in range(recCnt):
            if records[i][0] not in serNoMap :
                serNoMap[records[i][0]] =   records[i][1]

            if records[i][2] not in NoMap :
                NoMap[records[i][2]] =   records[i][3]

        #�ĸ����ڴ�ŷ���ǰ̨����
        AFC401List              =   []
        AFC011List              =   []
        AFC001List              =   []
        NOFEEList               =   []

        #��ȡ��ˮ��������
        for item in serNoMap.keys():
            AFC401List.append(item)
            AFC011List.append(serNoMap[item])

        #��ȡ�ɿ����������
        for item in NoMap.keys():
            AFC001List.append(item)
            NOFEEList.append(NoMap[item])


        AfaLoggerFunc.tradeInfo(serNoMap)
        AfaLoggerFunc.tradeInfo(NoMap)
        #ƴ�ֶη���ǰ̨
        TradeContext.AFC401     =   ':'.join(AFC401List)
        TradeContext.AFC011     =   ':'.join(AFC011List)
        TradeContext.AFC001     =   ':'.join(AFC001List)
        TradeContext.NOFEE      =   ':'.join(NOFEEList)


        #fields                  =   "AFC401,AFC011,AFC001,NOFEE"
        #
        #index                   =   0                       #�ֶ����±�
        #for field  in fields.split(","):
        #    item                =   []
        #    for i in range(recCnt):
        #        if (field == 'AFC401' or field == 'AFC001' or field == 'NOFEE') and ( records[i][index] in item ):           #��ˮ�����кͽɿ��������е���Ŀ������ͬ
        #            #if (field == 'AFC011' or field == 'NOFEE') and ( records[i][index] in item) :
        #            pass
        #        else:
        #             item.append(records[i][index])
        #
        #    AfaLoggerFunc.tradeInfo( item )
        #    if item == None :
        #        TradeContext.errorCode  =   "0000"
        #        TradeContext.errorMsg   =   "��̨����Ʊ����ˮ��ѯ�ɹ�"
        #        return False
        #
        #    value               =   ":".join(item)
        #    setattr(TradeContext,field,value)
        #    index               =   index + 1           #��ʼ��һ���ֶ�
        #
        #    AfaLoggerFunc.tradeInfo( "TradeContext." + field + " = " + value )

        TradeContext.errorCode  =   "0000"
        TradeContext.errorMsg   =   "��̨����Ʊ����ˮ��ѯ�ɹ�"

    AfaLoggerFunc.tradeInfo( "********************��̨����Ʊ����ˮ��ѯ����***************" )
    return True
