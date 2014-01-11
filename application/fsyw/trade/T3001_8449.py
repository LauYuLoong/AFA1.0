###############################################################################
# -*- coding: gbk -*-
# �ļ���ʶ��
# ժ    Ҫ�����շ�˰
#
# ��ǰ�汾��1.0
# ��    �ߣ�WJJ
# ������ڣ�2007��10��15��
###############################################################################

#���е�״̬λ 0 �ѹ��Ҵ���  1δ���Ҵ���  *�Ǵ�������
import TradeContext, AfaDBFunc, AfaLoggerFunc, os, sys
from types import *

def SubModuleMainFst( ):

    TradeContext.__agentEigen__  = '0'   #�ӱ��־

    AfaLoggerFunc.tradeInfo( "********************��̨��ֿ�ʼ***************" )

    fileName    =   os.environ['AFAP_HOME'] + "/data/ahfs/" + TradeContext.FileName
    cnt         =   0
    amount      =   0.0

    #-----------------------���ݵ�λ�������û�ȡ������Ϣ----------------------------
    sqlstr      =   "select aaa010,bankno from fs_businoinfo where busino='" + TradeContext.busiNo + "'"
    records = AfaDBFunc.SelectSql( sqlstr )
    if records == None or len(records)==0 :
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","���ҵ�λ��Ϣ���쳣"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        AfaLoggerFunc.tradeInfo( sqlstr )
        sys.exit(1)

    elif len(records) > 1:
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","��λ��Ϣ���쳣:һ����λ��Ŷ�Ӧ�˶��������Ϣ"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        AfaLoggerFunc.tradeInfo( sqlstr )
        sys.exit(1)

    TradeContext.AAA010     =   records[0][0].strip()
    TradeContext.AFA101     =   records[0][1].strip()

    #TradeContext.AAA010     =   "0000000000"
    #TradeContext.AFA101     =   "011"
    try:
        cnt         =   0
        amount      =   0.0
        if ( os.path.exists(fileName) and os.path.isfile(fileName) ):
            fp      =   open(fileName,"r")
            sLine   =   fp.readline()
            while ( sLine ):
                LineItem    =   sLine.split("|")

                #���ҵ�����ˮ���룬�����״̬λ��

                dateTmp     =   TradeContext.serDate[0:4] + '-' + TradeContext.serDate[4:6] + '-' + TradeContext.serDate[6:8]
                if LineItem[0].strip() == '0':
                    TradeContext.errorCode  =   "0002"
                    TradeContext.errorMsg   =   "���������Զ����ɣ�����д�����"
                    #sqlstr  =   "update fs_fc74 set flag ='1',busino='" + TradeContext.busiNo + "',afc016='" + TradeContext.brno + "',teller='" + TradeContext.teller + "',date='" + TradeContext.workDate + "' where afc401='" + LineItem[1].strip() + "' and afc015='" + dateTmp + "' and BUSINO='" + TradeContext.busiNo + "'"
                else:
                    sqlstr  =   "select date from fs_fc74 where afc401='" + LineItem[1].strip() + "' and afc015='" + dateTmp + "' and BUSINO='" + TradeContext.busiNo + "'"

                    #===�����������б����ֶ�,�ź��޸�===
                    sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

                    AfaLoggerFunc.tradeInfo( sqlstr )
                    records =   AfaDBFunc.SelectSql( sqlstr )
                    if( records == None ):
                        TradeContext.errorCode  =   "0001"
                        TradeContext.errorMsg   =   "����������Ϣʧ��"
                        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                        AfaLoggerFunc.tradeInfo( sqlstr + AfaDBFunc.sqlErrMsg )
                        return False
                    date    =   records[0][0]
                    AfaLoggerFunc.tradeInfo( date )
                    if TradeContext.workDate != date:
                        TradeContext.errorCode  =   "0002"
                        TradeContext.errorMsg   =   "�����������ϴ�������ɾ������"
                        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                        return False
                    TradeContext.errorCode  =   "0002"
                    TradeContext.errorMsg   =   "���������Զ����ɣ�����ɾ������"
                    #sqlstr  =   "update fs_fc74 set flag ='*',busino='" + TradeContext.busiNo + "',afc016='" + TradeContext.brno + "',teller='" + TradeContext.teller + "',date='" + '00000000' + "' where afc401='" + LineItem[1].strip() + "' and afc015='" + dateTmp + "' and BUSINO='" + TradeContext.busiNo + "'"
                AfaLoggerFunc.tradeInfo( sqlstr )
                if( AfaDBFunc.UpdateSqlCmt( sqlstr ) < 1 ):
                    AfaLoggerFunc.tradeInfo( '---test----->[' +sqlstr + ']<------------')
                    TradeContext.errorCode, TradeContext.errorMsg='0002', '���������Զ�����,������ˮ��%sʧ��' %( LineItem[1].strip() )
                    #TradeContext.errorCode, TradeContext.errorMsg='0002', '���������Զ����ɣ������޸�')
                    AfaLoggerFunc.tradeInfo( TradeContext.errorMsg + AfaDBFunc.sqlErrMsg )
                    AfaLoggerFunc.tradeInfo(  sqlstr )
                    return False

                cnt     =   cnt + 1
                amount  =   amount + float(LineItem[4].strip())

                sLine   =   fp.readline()

        else:
            AfaLoggerFunc.tradeInfo( "�ļ�" + fileName + "������" )
            TradeContext.errorCode  =   "0002"
            TradeContext.errorMsg   =   "�����ļ�������"
            return False

        AfaLoggerFunc.tradeInfo( "********************��̨��ֽ���***************" )
        TradeContext.errorCode  =   "0000"
        TradeContext.errorMsg   =   "�������´����ɹ�"
        TradeContext.Total      =   str(amount)
        TradeContext.Count      =   str(cnt)
        AfaLoggerFunc.tradeInfo( TradeContext.Count )
        return True

    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        TradeContext.errorCode  =   "0003"
        TradeContext.errorMsg   =   "���������쳣"
        return False
