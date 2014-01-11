# -*- coding: gbk -*-
##################################################################
#   财税库行.自由格式报文查询和发送.柜面发起
#=================================================================
#   程序文件:   TTPS001_8461.py
#   修改时间:   2006-04-05
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools, AfaDBFunc
import TipsFunc,AfaAfeFunc,os
from types import *

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo( '进入自由格式报文查询和发送[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
        #=============获取当前系统时间====================
        TradeContext.workDate=UtilTools.GetSysDate( )
        TradeContext.workTime=UtilTools.GetSysTime( )
        
        
        #============校验公共节点的有效性==================
        # 完整性检查
        if( not TradeContext.existVariable( "operFlag" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '标识[operFlag]值不存在!' )
        
        ##=============获取平台流水号==================== 
        #if TipsFunc.GetSerialno( ) == -1 :
        #    raise TipsFunc.flowException( )
        #
        if TradeContext.operFlag=='0': #查询
            if( not TradeContext.existVariable( "beginDate" ) ):
                return TipsFunc.ExitThisFlow( 'A0001', '起始日[beginDate]值不存在!' )
            if( not TradeContext.existVariable( "endDate" ) ):
                return TipsFunc.ExitThisFlow( 'A0001', '截至日[endDate]值不存在!' )
            
            #=================================
            sql="SELECT * FROM TIPS_NOTE WHERE WORKDATE BETWEEN '"+ TradeContext.beginDate +"' AND '"+TradeContext.endDate+"'" 
            if( TradeContext.existVariable( "srcNodeCode" ) and len(TradeContext.srcNodeCode)>0):
                sql=sql+" AND SRCNODECODE ='"+TradeContext.srcNodeCode     +"'"
            if( TradeContext.existVariable( "desNodeCode" ) and len(TradeContext.desNodeCode)>0):
                sql=sql+" AND DESNODECODE ='"+TradeContext.desNodeCode     +"'"
            sql=sql+" ORDER BY WORKDATE,WORKTIME "
            AfaLoggerFunc.tradeInfo(sql)
            records = AfaDBFunc.SelectSql(sql)
            if( records == None ):
                AfaLoggerFunc.tradeFatal(sql)
                return TipsFunc.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
            elif( len( records )==0 ):
                return TipsFunc.ExitThisFlow( 'A0002', '无满足条件的记录')
            else:
                records=UtilTools.ListFilterNone( records ,'')
                
                mx_file_name = os.environ['AFAP_HOME'] + '/tmp/' + 'AH_' + TradeContext.teller + '.txt'
                TradeContext.tradeResponse.append(['fileName',  'AH_' + TradeContext.teller + '.txt'])
            
                if (os.path.exists(mx_file_name) and os.path.isfile(mx_file_name)):
                    #文件存在,先删除-再创建
                    os.system("rm " + mx_file_name)
            
                sfp = open(mx_file_name, "w")
                AfaLoggerFunc.tradeInfo('明细文件=['+mx_file_name+']')
                i = 0
                while ( i  < len(records) ):
                    A0 = str(records[i][0]).strip()         #WORKDATE
                    A1 = str(records[i][1]).strip()         #WORKTIME
                    A2 = str(records[i][2]).strip()         #SrcNodeCode
                    A3 = str(records[i][3]).strip()         #DesNodeCode
                    A4 = str(records[i][4]).strip()         #SendOrgCode
                    A5 = str(records[i][5]).strip()         #RcvOrgCode 
                    A6 = str(records[i][6]).strip()         #Content    
            
                    sfp.write(A0 +  '|'  +  A1[0:2]+':' +A1[2:4]+':' + A1[4:6] +  '|'  +  A2 +  '|'  +  A3 +  '|'  +  A4 +  '|'  +  A5 +  '|'  +  A6 +  '|'  + '\n')
                    i=i+1
                sfp.close()

        elif TradeContext.operFlag=='1':
            #=============获取平台流水号====================
            if TipsFunc.GetSerialno( ) == -1 :
                WrtLog('>>>处理结果:获取平台流水号异常' )
                sys.exit()
            
            #=============与第三方通讯====================
            AfaAfeFunc.CommAfe()
            if( TradeContext.errorCode != '0000' ):
                return False
            else:
                sql="insert into TIPS_NOTE"
                sql=sql+" values"
                sql=sql+"('"+TradeContext.workDate     +"'"
                sql=sql+",'"+TradeContext.workTime    +"'"
                sql=sql+",'"+TradeContext.srcNodeCode    +"'"
                sql=sql+",'"+TradeContext.desNodeCode    +"'"
                if( TradeContext.existVariable( "sendOrgCode" ) ):
                    sql=sql+",'"+TradeContext.sendOrgCode    +"'"
                else:
                    sql=sql+",''"
                if( TradeContext.existVariable( "rcvOrgCode" ) ):
                    sql=sql+",'"+TradeContext.rcvOrgCode    +"'"
                else:
                    sql=sql+",''"
                sql=sql+",'"+TradeContext.content +"'"
                sql=sql+")"
                AfaLoggerFunc.tradeInfo(sql)
                if( AfaDBFunc.InsertSqlCmt(sql) == -1 ):
                    AfaLoggerFunc.tradeFatal(sql)
                    return TipsFunc.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
        else :
            return TipsFunc.ExitThisFlow( 'A0002', '操作类型错误')
            
        #=============自动打包==================== 
        TradeContext.tradeResponse.append(['errorCode',  '0000'])
        TradeContext.tradeResponse.append(['errorMsg',  '交易成功'])
        #=============程序退出====================
        AfaLoggerFunc.tradeInfo( '退出自由格式报文查询和发送['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        return True
    except TipsFunc.flowException, e:
        return False
    except Exception, e:
        return TipsFunc.ExitThisFlow('A9999','系统异常'+str(e) )
def SubModuleMainSnd():
    return True   
