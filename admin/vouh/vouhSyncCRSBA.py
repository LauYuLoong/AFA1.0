# -*- coding: gbk -*-
################################################################################
#   ƾ֤����ϵͳ��ϵͳ������.ͬ��������
#===============================================================================
#   �����ļ�:   vouhSyncCRSBA.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2009-09-15
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys,ConfigParser,AfaFtpFunc
from types import *
from rccpsConst import *
import vouhCronFunc


if __name__ == '__main__':

    try:
        vouhCronFunc.WrtLog("***ƾ֤����ϵͳ: ϵͳ������.ͬ��������[vouhSyncCRSBA]����***")
        
        #���������������ļ�
        vouhCronFunc.WrtLog(">>>>��ʼ���������������ļ�")
        #�����ļ�
        LocalFileName = os.environ['AFAP_HOME'] + '/data/vouh/'
        
        ret = AfaFtpFunc.getFile("VOUH_SYNC_CRSBA","crsba","crsba")
        
        if not ret:
           vouhCronFunc.WrtLog(">>>>�������������������ļ�,ʧ��")
           raise Exception,">>>�ļ�����ʧ��"
        else:
           vouhCronFunc.WrtLog(">>>>�������������������ļ�,�ɹ�")
        #ת�������������ļ�
        vouhCronFunc.WrtLog(">>>>��ʼת�������������ļ�")
        #���ø�ʽ:cvt2ascii -T �����ı��ļ� -P �����ļ� -F fld�ļ� [-D ���-��] [-S] [-R]
        CvtProg     = os.environ['AFAP_HOME'] + '/data/cvt/cvt2ascii'
        
        dstFileName = LocalFileName + 'vouh_front_crsba.del'
        srcFileName = LocalFileName + 'crsba'
        fldFileName = os.environ['AFAP_HOME'] + '/data/cvt/crsba.fld'
        
        cmdstr=CvtProg + " -T " + dstFileName + " -P " + srcFileName + " -F " + fldFileName + " -D " + "','"

        os.system(cmdstr)
        
        vouhCronFunc.WrtLog(">>>>����ת�������������ļ�")
        #����ƾ֤����ϵͳ������
        vouhCronFunc.WrtLog(">>>>��ʼ���������������ļ�")

        #���ӵ�DB2 MAPS
        os.system( "db2 connect to maps")
         
        vouhCronFunc.WrtLog( '>>>��ʼ�����' )

        crsba_sql = "import from /home/maps/afa/data/vouh/vouh_front_crsba.del of del commitcount 1000 replace into vouh_front_crsba"
        cmd = "db2 \"" + crsba_sql + "\""
        vouhCronFunc.WrtLog( '>>>����Ϊ:' + cmd )
        os.system( cmd )
        #��������
        os.system( "db2 disconnect maps" )
                
        vouhCronFunc.WrtLog(">>>>�������������������ļ�")
        vouhCronFunc.WrtLog("***ƾ֤����ϵͳ: ϵͳ������.ͬ��������[vouhSyncCRSBA]�˳�***")

       
 
    except Exception, e:  
        vouhCronFunc.WrtLog( e )

    sys.exit(-1)
        
 
