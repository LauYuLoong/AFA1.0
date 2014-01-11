# -*- coding: gbk -*-
###################################################################
#    文    件:    Tvouh001.py
#    说    明:    凭证管理数据更改
#    环    境:    中间业务新平台（AFA）--- UNIX: AIX 5.3
#    作    者:    李利君
#    公    司:    北京赞同科技
#    创建地址:    安徽
#    创建时间:    2011年12月20日
#    维护纪录:
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, AfaFlowControl, AfaDBFunc,AfaHostFunc,HostComm
from types import *
import AfaLoggerFunc,VouhFunc,binascii,HostContext,VouhHostFunc

TradeContext.sysType = 'agent' 

#=============返回错误码,错误信息===================================
def tradeExit( code, msg ):
    TradeContext.errorCode, TradeContext.errorMsg=code, msg
    if code != '0000':
        return False
    return True

#=========================处理函数==============================================
def vouh_Pro( ):
        
    try: 
        #===========查询数据库中不符合规则的库箱标志和凭证状态组合==============       
        sql = ""
        sql = "select distinct(BESBNO) from vouh_register where depository = '4' and vouhstatus='2'"
        
        AfaLoggerFunc.tradeInfo('查询语句'+ sql)
        
        records = AfaDBFunc.SelectSql( sql )
        
        if records==None:
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"查询数据库失败"
            raise AfaFlowControl.flowException( )
        
        elif(len(records) < 1):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","不存在满足条件的数据"
            return False
        
        else:
            
            record=AfaUtilTools.ListFilterNone( records )          
            total=len( records )
            AfaLoggerFunc.tradeDebug("数据条数：" + str(total))
            
            for i in range(0,total):
                
                AfaLoggerFunc.tradeInfo('机构号'+ records[i][0])          
                #=============获取机构类型==========================
                HostContext.I1OTSB = records[i][0]                #机构代号
                HostContext.I1SBNO = '3401010007'                 #机构号
                HostContext.I1USID = '999996'                     #柜员号
                #HostContext.I1WSNO = TradeContext.sWSNO          #终端号
                
                
                if(not VouhHostFunc.CommHost('2001')):
                    tradeExit( TradeContext.errorCode, TradeContext.errorMsg )
                    raise AfaFlowControl.flowException( )
                if(TradeContext.errorCode == '0000'):
                    SBNO = HostContext.O1SBCH
                    AfaLoggerFunc.tradeInfo( SBNO )
                
                if(SBNO=='33'):
                    update_sql = ""
                    update_sql = update_sql + "update vouh_register set depository = '1'"
                    update_sql = update_sql + " where besbno = '" + records[i][0] + "'"
                    update_sql = update_sql + " and depository = '4' and vouhstatus='2'"
                    AfaLoggerFunc.tradeInfo('更新数据库语句1：'+ update_sql)
                    #更新并提交数据
                    if  AfaDBFunc.UpdateSqlCmt(update_sql)<0:
                        return AfaFlowControl.ExitThisFlow("A999","更新失败")
                    
                elif(SBNO=='31' or SBNO=='40' or SBNO=='32' or SBNO=='41'):
                    update_sql = ""
                    update_sql = "update vouh_register set depository = '2'"
                    update_sql = update_sql + " where besbno = '" + records[i][0] + "'"
                    update_sql = update_sql + " and depository = '4' and vouhstatus='2'"
                    AfaLoggerFunc.tradeInfo('更新数据库语句2：'+ update_sql)
                    if  AfaDBFunc.UpdateSqlCmt(update_sql)<0:
                        return AfaFlowControl.ExitThisFlow("A999","更新失败")
                        
                elif(SBNO=='50'):
                    update_sql = ""
                    update_sql = "update vouh_register set depository = '3'"
                    update_sql = update_sql + " where besbno = '" + records[i][0] + "'"
                    update_sql = update_sql + " and depository = '4' and vouhstatus='2'"
                    AfaLoggerFunc.tradeInfo('更新数据库语句3：'+ update_sql)
                    if  AfaDBFunc.UpdateSqlCmt(update_sql)<0:
                        return AfaFlowControl.ExitThisFlow("A999","更新失败")
                else:
                    VouhFunc.tradeExit('A005061', '该机构级别不在指定范围内')
                    raise AfaFlowControl.flowException( )                
        
                tradeExit('0000', '更新成功')

        
                #=============程序退出=========================================
        
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return False

#######################################主函数###########################################
if __name__=='__main__':

    AfaLoggerFunc.tradeInfo('********************不符合规则的库箱标志和凭证状态组合转化开始********************')
    
    #转换处理
    vouh_Pro( )
    
    AfaLoggerFunc.tradeInfo('********************不符合规则的库箱标志和凭证状态组合转化结束********************')