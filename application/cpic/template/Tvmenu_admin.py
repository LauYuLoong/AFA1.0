# -*- coding: gbk -*-
################################################################################
# 文件名称：vmenu_admin.py
# 文件标识：
# 摘    要：柜面对账
#
# 当前版本：1.0
# 作    者：胡友
# 完成日期：2011年10月20日
################################################################################
import TradeContext

TradeContext.sysType = 'cron'

import AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaFlowControl,AfaDBFunc,os,time,datetime
from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('******柜面对账['+TradeContext.TemplateCode+']进入******')

    try:

        #=====================初始化返回报文变量================================
        TradeContext.tradeResponse=[]
        
        #=====================获取当前系统时间==================================
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )
        #=====================柜面对账处理======================================
        admin()
        #=============自动打包====================
        AfaFunc.autoPackData()

        #=====================退出模板==========================================
        AfaLoggerFunc.tradeInfo('******柜面对账['+TradeContext.TemplateCode+']退出******')

    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
#==========柜面对账处理==========
def admin( ):

    #1,前台变量校验
    if( (not TradeContext.existVariable( "Appno" )) or (TradeContext.existVariable( "Appno" ) and len(TradeContext.Appno) == 0 ) ):
        return AfaFlowControl.ExitThisFlow( 'A010', '业务编号[Appno]值不存在!' )
    #if( (not TradeContext.existVariable( "Unitno" )) or (TradeContext.existVariable( "Unitno" ) and len(TradeContext.Unitno) == 0 ) ):
    #    return AfaFlowControl.ExitThisFlow( 'A010', '单位编号[Unitno]值不存在!' )
    if( (not TradeContext.existVariable( "ChkDate" )) or (TradeContext.existVariable( "ChkDate" ) and len(TradeContext.ChkDate) == 0 ) ):
        return AfaFlowControl.ExitThisFlow( 'A010', '对账日期[ChkDate]值不存在!' )
    
    #2,业务分支处理：
    ProcName = []
    
    
    #a,非税处理
    if( TradeContext.Appno == 'AG2008' and ( (not TradeContext.existVariable( "Unitno" )) or ( TradeContext.existVariable( "Unitno" ) and len(TradeContext.Unitno) == 0 ) ) ):
        
        #20111028陈浩修改添加 日期偏移量计算
        #begin
        #TrxDate = str(int(TradeContext.ChkDate) - int(TradeContext.workDate))        
         
        AfaLoggerFunc.tradeInfo('对帐日期：' + TradeContext.ChkDate)
        AfaLoggerFunc.tradeInfo('当前日期：' + TradeContext.workDate)
         
        year1  = int(TradeContext.ChkDate[0:4])                        #年
        month1 = int(TradeContext.ChkDate[4:6])                        #月
        day1   = int(TradeContext.ChkDate[6:])                         #日
        
        year2  = int(TradeContext.workDate[:4])
        month2 = int(TradeContext.workDate[4:6])
        day2   = int(TradeContext.workDate[6:])
                 
        d1 = datetime.datetime(year1, month1, day1)  
        d2 = datetime.datetime(year2, month2, day2)
       
        TrxDate = str((d1 - d2).days)                                  #日期偏移量
        AfaLoggerFunc.tradeInfo('日期偏移量：' )
        AfaLoggerFunc.tradeInfo( TrxDate )
                                                                                             
        #end
        
        #对账时间校验
        if( int(TrxDate) > 0 ):
            AfaLoggerFunc.tradeInfo( '对账时间不能超前' )
            return AfaFlowControl.ExitThisFlow( 'A010', '对账时间不能超前' )
         
            
        #20111028陈浩添加修改
        #begin
        #ProcName.append( 'python /home/maps/afa/application/fsyw/trade/AHFS_SCSJ.py '   + TrxDate )   
        #ProcName.append( 'python /home/maps/afa/application/fsyw/trade/AHFS_SCFC60.py ' + TrxDate )   
        
        ProcName.append( 'python /home/maps/afa/application/fsyw/trade/qinfensel.py '  + TrxDate )                # 非税自动清分
        ProcName.append( 'python /home/maps/afa/application/fsyw/trade/8449.py '       + TrxDate )                # 非税自动待查
        ProcName.append( 'python /home/maps/afa/application/fsyw/trade/AHFS_SCSJ.py '  + TradeContext.ChkDate )   # 非税上传数据信息
        
        #end
        
    #b,非非税处理
    elif( (TradeContext.Appno == 'AG2011' or TradeContext.Appno == 'AG2013' or TradeContext.Appno == 'AG2017') and  TradeContext.existVariable( "Unitno" ) ):
        
        #对账时间校验        
        if( int(TradeContext.ChkDate.strip()) > int(TradeContext.workDate.strip()) ):
            AfaLoggerFunc.tradeInfo( '对账时间不能超前' )
            return AfaFlowControl.ExitThisFlow( 'A010', '对账时间不能超前' )
         
        
        sql = ""
        sql = sql + "select procName"
        sql = sql + " from afa_cronAdm"
        sql = sql + " where procName like '%"+ TradeContext.Appno + " " + TradeContext.Unitno +"%'"
        #陈浩添加 20111115
        sql = sql + " and status = '1'"
        
        AfaLoggerFunc.tradeInfo('非非税处理afa_cron表查询sql=' + sql )
        records = AfaDBFunc.SelectSql( sql )
        
        if (records==None):
            AfaLoggerFunc.tradeInfo('数据库异常')
            return AfaFlowControl.ExitThisFlow( 'A010', '数据库异常' )

        if (len(records)==0):
            AfaLoggerFunc.tradeInfo('表afa_cronadm中没有该业务对应单位的对账记录')
            return AfaFlowControl.ExitThisFlow( 'A010', '表afa_cronadm中没有该业务对应单位的对账记录' )
        
        if( len(records) == 1 ):
            AfaLoggerFunc.tradeInfo('表afa_cronadm中该业务对应单位的对账记录信息为'+records[0][0])
            
            #对账程序加上日期
            name = records[0][0].strip() + " " + TradeContext.ChkDate
            ProcName.append( name )
        
        else:
            AfaLoggerFunc.tradeInfo('表afa_cronadm中该业务对应单位的对账记录信息不唯一，有'+str(len(records)))
            return AfaFlowControl.ExitThisFlow( 'A010', '表afa_cronadm中该业务对应单位的对账记录信息不唯一' )
            
    #运行对账程序
    AfaLoggerFunc.tradeInfo( '要运行的对账程序有'+str(ProcName) )
    
    for i in range(0,len(ProcName)):
        
        #20111103 添加
        #begin
        AfaLoggerFunc.tradeInfo(">>>判断此调度是否正在运行...")
        #判断当前系统调度是否正在运行,若正在运行,则不重新调起
        cmd = "ps -ef | grep '" + ProcName[i] + "' | grep -v grep"
        handler = os.popen(cmd,'r')
        handler_line = handler.readline()
        handler.close()
        
        if len(handler_line) > 0:
            #WrtLog( '>>>程序:[ ' + ProcName[i] + ' ]正在运行中' )
            AfaLoggerFunc.tradeInfo( '>>>程序:[ ' + ProcName[i] + ' ]正在运行中' )
            continue
        #end
        
        AfaLoggerFunc.tradeInfo( '运行对账程序'+ProcName[i] )
        
        #os.system(ProcName[i] + ' &')   #后台运行
        os.system(ProcName[i])
        
        #time.sleep(5)
    
    
    TradeContext.errorCode = '0000'
    TradeContext.errorMsg = '交易成功'
    return True
    
