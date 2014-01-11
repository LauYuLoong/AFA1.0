# -*- coding: gbk -*-
###############################################################################
# �ļ����ƣ�ahjf_export.py
# �ļ���ʶ��
# ժ    Ҫ�����ս�������������
# ��    �ߣ�����̩
# ������ڣ�2011��03��14��
###############################################################################
import TradeContext
TradeContext.sysType = 'ahjf'
import os,sys,TradeContext,AfaUtilTools,datetime,AfaLoggerFunc,ConfigParser,AfaFtpFunc



######################################������#################################
def MainExp_Proc( ):
    
    if (len(sys.argv)==1):
        TradeContext.workDate = AfaUtilTools.GetSysDate( )   #Ĭ�ϵ�����������
    else:
        TradeContext.workDate = sys.argv[1]                  #����ָ�����ڵ�����
    try:
        config = ConfigParser.ConfigParser( )
        configFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'
        config.readfp( open(configFileName) )
        LDIR           = config.get("AG2017_AHJF_EXPORT","LDIR")
        
        LFileName_AHJF = "ahjf_export_" + TradeContext.workDate + ".txt"
        DFileName_AHJF = LDIR + "/" + "ahjf_export"  + ".txt"
        FileName_AHJF  = "ahjf_export"  + ".txt"

        sql_export     = " db2 \"export to '" + DFileName_AHJF + "' of del select * from afa_maintransdtl where sysid='AG2017' and workdate='" + TradeContext.workDate + "' \""

        os.system( "db2 connect to maps" )
        
        AfaLoggerFunc.tradeInfo(">>>��ʼ������afa_maintransdtl��������䣺" + sql_export)
        os.system( sql_export )

        os.system( "db2 disconnect maps" )
        
        #�ϴ������ļ�
        RFileName_AHJF = LFileName_AHJF

        if not ( AfaFtpFunc.putFile( "AG2017_AHJF_EXPORT",FileName_AHJF,RFileName_AHJF ) ):
            AfaLoggerFunc.tradeInfo( ">>>�ϴ��ļ�[" + LFileName_AHJF + "]ʧ��" )
            return False
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        AfaLoggerFunc.tradeInfo("�����쳣")
        return False
        
    
####################################������############################################    
if __name__ == '__main__':
        
    AfaLoggerFunc.tradeInfo("****************���ս�����ʱ�������ݵ�����ʼ****************")
    
    MainExp_Proc( )
    
    AfaLoggerFunc.tradeInfo("****************���ս�����ʱ�������ݵ�������****************")
