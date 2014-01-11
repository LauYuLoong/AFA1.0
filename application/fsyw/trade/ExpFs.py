# -*- coding: gbk -*-
###############################################################################
# �ļ����ƣ�ExpFs.py
# �ļ���ʶ��
# ժ    Ҫ����˰����������
# ��    �ߣ�CYG
# ������ڣ�2009��11��09��
###############################################################################
import os,sys,TradeContext,AfaUtilTools,datetime,AfaLoggerFunc,ConfigParser,AfaFtpFunc



######################################������#################################
def MainExp_Proc( ):
    
    if (len(sys.argv)==2):
        TradeContext.workDate = sys.argv[1]
    else:
        #��ȡϵͳ�������� 
        TradeContext.WorkDate = GetYesterday( )
    try:
    
        config = ConfigParser.ConfigParser( )
        configFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'
        config.readfp( open(configFileName) )
        LDIR           = config.get("FS_EXPORT_HE","LDIR")
        
        LFileName_fc74 = "fs_fc74" + TradeContext.WorkDate + ".txt"
        DFileName_fc74 = LDIR + "/" + LFileName_fc74
        
        LFileName_fc75 = "fs_fc75" + TradeContext.WorkDate + ".txt"
        DFileName_fc75 = LDIR + "/" + LFileName_fc75
        
        LFileName_fc76 = "fs_fc76" + TradeContext.WorkDate + ".txt"
        DFileName_fc76 = LDIR + "/" + LFileName_fc76
        
        LFileName_fc84 = "fs_fc84" + TradeContext.WorkDate + ".txt"
        DFileName_fc84 = LDIR + "/" + LFileName_fc84
        
        LFileName_fa15 = "fs_fa15" + TradeContext.WorkDate + ".txt"
        DFileName_fa15 = LDIR + "/" + LFileName_fa15

        sql_fc74 = " db2 \"export to '" + DFileName_fc74 + "' of del select * from fs_fc74 where busino='34010100790001' and date='" + TradeContext.WorkDate + "' and flag!='*' \""
        sql_fc75 = " db2 \"export to '" + DFileName_fc75 + "' of del select * from fs_fc75 where flag='0' and busino='34010100790001' and date='" + TradeContext.WorkDate + "' \""
        sql_fc76 = " db2 \"export to '" + DFileName_fc76 + "' of del select * from fs_fc76 where flag='0' and busino='34010100790001' and date='" + TradeContext.WorkDate + "' \""
        sql_fc84 = " db2 \"export to '" + DFileName_fc84 + "' of del select * from fs_fc84 where busino='34010100790001' and date='" + TradeContext.WorkDate + "' and flag='0' \""
        sql_fa15 = " db2 \"export to '" + DFileName_fa15 + "' of del select * from fs_fa15 where busino='34010100790001' \""

        os.system( "db2 connect to maps" )
        
        AfaLoggerFunc.tradeInfo(">>>��ʼ������fs_fc74��������䣺" + sql_fc74)
        os.system( sql_fc74 )
        AfaLoggerFunc.tradeInfo(">>>��ʼ������fs_fc75��������䣺" + sql_fc75)
        os.system( sql_fc75 )
        AfaLoggerFunc.tradeInfo(">>>��ʼ������fs_fc76��������䣺" + sql_fc76)
        os.system( sql_fc76 )
        AfaLoggerFunc.tradeInfo(">>>��ʼ������fs_fc84��������䣺" + sql_fc84)
        os.system( sql_fc84 )
        AfaLoggerFunc.tradeInfo(">>>��ʼ������fs_fa15��������䣺" + sql_fa15)
        os.system( sql_fa15 )

        os.system( "db2 disconnect maps" )
        
        #�ϴ������ļ�
        RFileName_fc74 = LFileName_fc74
        RFileName_fc75 = LFileName_fc75
        RFileName_fc76 = LFileName_fc76
        RFileName_fc84 = LFileName_fc84
        RFileName_fa15 = LFileName_fa15
        
        if not ( AfaFtpFunc.putFile( "FS_EXPORT_HE",LFileName_fc74,RFileName_fc74 ) ):
            AfaLoggerFunc.tradeInfo( ">>>�ϴ��ļ���" + LFileName_fc74 + "��ʧ��" )
            return False
            
        if not ( AfaFtpFunc.putFile( "FS_EXPORT_HE",LFileName_fc75,RFileName_fc75 ) ):
            AfaLoggerFunc.tradeInfo( ">>>�ϴ��ļ���" + LFileName_fc75 + "��ʧ��" )
            return False
            
        if not ( AfaFtpFunc.putFile( "FS_EXPORT_HE",LFileName_fc76,RFileName_fc76 ) ):
            AfaLoggerFunc.tradeInfo( ">>>�ϴ��ļ���" + LFileName_fc76 + "��ʧ��" )
            return False
            
        if not ( AfaFtpFunc.putFile( "FS_EXPORT_HE",LFileName_fc84,RFileName_fc84 ) ):
            AfaLoggerFunc.tradeInfo( ">>>�ϴ��ļ���" + LFileName_fc84 + "��ʧ��" )
            return False

        if not ( AfaFtpFunc.putFile( "FS_EXPORT_HE",LFileName_fa15,RFileName_fa15 ) ):
            AfaLoggerFunc.tradeInfo( ">>>�ϴ��ļ���" + LFileName_fa15 + "��ʧ��" )
            return False
        
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        AfaLoggerFunc.tradeInfo("�����쳣")
        return False
        
    
#��ȡϵͳ���������
def GetYesterday( ):
    currentDate = datetime.date.today()
    yesterday   = currentDate - datetime.timedelta( days=1 )
    return AfaUtilTools.DateDelSign( str(yesterday) )





####################################������############################################    
if __name__ == '__main__':
        
    AfaLoggerFunc.tradeInfo("****************��˰��ʱ�������ݵ�����ʼ****************")
    
    MainExp_Proc( )
    
    AfaLoggerFunc.tradeInfo("****************��˰��ʱ�������ݵ�������****************")
