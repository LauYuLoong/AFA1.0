###############################################################################
# -*- coding: gbk -*-
# ժ    Ҫ����ũ��������ʱ������ʱ����
# ��ǰ�汾��1.0
# ��    �ߣ�������
# ������ڣ�2010��12��23��
###############################################################################
import TradeContext

TradeContext.sysType = "ahxnb"

import sys, AfaDBFunc,AfaLoggerFunc,AfaAdminFunc

from types import *

if __name__ == '__main__':
    
    AfaLoggerFunc.tradeInfo( '-------------------����ʡ��ũ���������������ʼ-------------------' )
    
    if ( len(sys.argv) != 2 ):
        print ( '�÷�:python procName offsetDays' )
        sys.exit( -1 )
    offsetDays = sys.argv[1]
    DelDate = AfaAdminFunc.getTimeFromNow( int(offsetDays) )
    
    #ɾ��ָ������ǰ����ʱ����
    sql = "delete from ahxnb_swap where workdate <= '" + DelDate + "'"
    
    AfaLoggerFunc.tradeInfo( '��ʱ����sql��' + sql )
    
    ret = AfaDBFunc.DeleteSqlCmt( sql )
    
    if ret < 0:
        AfaLoggerFunc.tradeInfo( '��ʱ��������ʧ��' )
        sys.exit( -1 )
    AfaLoggerFunc.tradeInfo( '�ܹ�����' + str(ret) + "������¼" )
    
    AfaLoggerFunc.tradeInfo( '-------------------����ʡ��ũ�����������������-------------------' )
    
    sys.exit( 0 )
