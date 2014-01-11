# -*- coding: gbk -*-
###############################################################################
# 文件名称：ahjf_export.py
# 文件标识：
# 摘    要：安徽交罚导出表数据
# 作    者：曾照泰
# 完成日期：2011年03月14日
###############################################################################
import TradeContext
TradeContext.sysType = 'ahjf'
import os,sys,TradeContext,AfaUtilTools,datetime,AfaLoggerFunc,ConfigParser,AfaFtpFunc



######################################处理函数#################################
def MainExp_Proc( ):
    
    if (len(sys.argv)==1):
        TradeContext.workDate = AfaUtilTools.GetSysDate( )   #默认导出当天数据
    else:
        TradeContext.workDate = sys.argv[1]                  #导出指定日期的数据
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
        
        AfaLoggerFunc.tradeInfo(">>>开始导出表afa_maintransdtl，导出语句：" + sql_export)
        os.system( sql_export )

        os.system( "db2 disconnect maps" )
        
        #上传导出文件
        RFileName_AHJF = LFileName_AHJF

        if not ( AfaFtpFunc.putFile( "AG2017_AHJF_EXPORT",FileName_AHJF,RFileName_AHJF ) ):
            AfaLoggerFunc.tradeInfo( ">>>上传文件[" + LFileName_AHJF + "]失败" )
            return False
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        AfaLoggerFunc.tradeInfo("操作异常")
        return False
        
    
####################################主函数############################################    
if __name__ == '__main__':
        
    AfaLoggerFunc.tradeInfo("****************安徽交罚定时调度数据导出开始****************")
    
    MainExp_Proc( )
    
    AfaLoggerFunc.tradeInfo("****************安徽交罚定时调度数据导出结束****************")
