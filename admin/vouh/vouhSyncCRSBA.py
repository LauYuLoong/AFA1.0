# -*- coding: gbk -*-
################################################################################
#   凭证管理系统：系统调度类.同步机构表
#===============================================================================
#   交易文件:   vouhSyncCRSBA.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2009-09-15
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys,ConfigParser,AfaFtpFunc
from types import *
from rccpsConst import *
import vouhCronFunc


if __name__ == '__main__':

    try:
        vouhCronFunc.WrtLog("***凭证管理系统: 系统调度类.同步机构表[vouhSyncCRSBA]进入***")
        
        #下载主机机构表文件
        vouhCronFunc.WrtLog(">>>>开始下载主机机构表文件")
        #本地文件
        LocalFileName = os.environ['AFAP_HOME'] + '/data/vouh/'
        
        ret = AfaFtpFunc.getFile("VOUH_SYNC_CRSBA","crsba","crsba")
        
        if not ret:
           vouhCronFunc.WrtLog(">>>>结束下载主机机构表文件,失败")
           raise Exception,">>>文件下载失败"
        else:
           vouhCronFunc.WrtLog(">>>>结束下载主机机构表文件,成功")
        #转码主机机构表文件
        vouhCronFunc.WrtLog(">>>>开始转码主机机构表文件")
        #调用格式:cvt2ascii -T 生成文本文件 -P 物理文件 -F fld文件 [-D 间隔-符] [-S] [-R]
        CvtProg     = os.environ['AFAP_HOME'] + '/data/cvt/cvt2ascii'
        
        dstFileName = LocalFileName + 'vouh_front_crsba.del'
        srcFileName = LocalFileName + 'crsba'
        fldFileName = os.environ['AFAP_HOME'] + '/data/cvt/crsba.fld'
        
        cmdstr=CvtProg + " -T " + dstFileName + " -P " + srcFileName + " -F " + fldFileName + " -D " + "','"

        os.system(cmdstr)
        
        vouhCronFunc.WrtLog(">>>>结束转码主机机构表文件")
        #导入凭证管理系统机构表
        vouhCronFunc.WrtLog(">>>>开始导入主机机构表文件")

        #连接到DB2 MAPS
        os.system( "db2 connect to maps")
         
        vouhCronFunc.WrtLog( '>>>开始导入表' )

        crsba_sql = "import from /home/maps/afa/data/vouh/vouh_front_crsba.del of del commitcount 1000 replace into vouh_front_crsba"
        cmd = "db2 \"" + crsba_sql + "\""
        vouhCronFunc.WrtLog( '>>>命令为:' + cmd )
        os.system( cmd )
        #结束连接
        os.system( "db2 disconnect maps" )
                
        vouhCronFunc.WrtLog(">>>>结束导入主机机构表文件")
        vouhCronFunc.WrtLog("***凭证管理系统: 系统调度类.同步机构表[vouhSyncCRSBA]退出***")

       
 
    except Exception, e:  
        vouhCronFunc.WrtLog( e )

    sys.exit(-1)
        
 
