# -*- coding: gbk -*-
###############################################################################
# �ļ����ƣ�tjyw_admin.py
# ժ    Ҫ��ȫʡͨ��ҵ�����
# ��ǰ�汾��1.0
# ��    �ߣ�CYG
# ������ڣ�2010��01��06��
###############################################################################
import TradeContext

TradeContext.sysType = 'tjyw'

import ConfigParser, sys, AfaDBFunc, os, AfaAdminFunc,HostContext,YbtFunc,AfaUtilTools
from types import *

###########################################������###########################################
if __name__=='__main__':


    print('**********ȫʡͨ��ҵ�������ʼ**********')

    if ( len(sys.argv) != 4 ):
        print( '�÷�: jtfk_Proc sysid unitno dateoffset')
        sys.exit(-1)

    sSysId      = sys.argv[1]
    sUnitno     = sys.argv[2]
    sOffSet     = sys.argv[3]
    sTrxDate   = AfaAdminFunc.getTimeFromNow(int(sOffSet))

    print '   ϵͳ���� = ' + sSysId
    print '   ��λ���� = ' + sUnitno
    print '   �������� = ' + sTrxDate

    #��ȡ�����ļ�
    if ( not AfaAdminFunc.GetAdminConfig( ) ) :
        sys.exit(-1)

    AfaAdminFunc.WrtLog('>>>����������')
    if not AfaAdminFunc.MatchData(sSysId,sUnitno,sTrxDate):
        sys.exit(-1)

    print '**********ȫʡͨ��ҵ���������**********'

    sys.exit(0)
