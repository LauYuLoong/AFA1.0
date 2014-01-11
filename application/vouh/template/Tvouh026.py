# -*- coding: gbk -*-
###################################################################
#    文    件:    Tvouh026.py
#    说    明:    凭证管理-->凭证号段调整
#    环    境:    中间业务新平台（AFA）--- UNIX: AIX 5.3
#    作    者:    LLJ
#    公    司:    北京赞同科技
#    创建地址:    安徽
#    创建时间:    2012年7月
#    维护纪录:   
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, AfaFlowControl, AfaDBFunc,VouhHostFunc,HostContext
from types import *

#=============返回错误码,错误信息===================================        
def tradeExit( code, msg ):                                                 
    TradeContext.errorCode, TradeContext.errorMsg=code, msg                 
    if code != '0000':                                                      
        return False                                                        
    return True                                                             

def main( ):
    AfaLoggerFunc.tradeInfo( '凭证号段调整['+TradeContext.TemplateCode+']进入' )

    #=============前台上送数据===================================
    #TradeContext.sBesbNo                                 机构代号
    #TradeContext.sCur                                    货币代码
    #TradeContext.sTellerNo                               柜员号
    #TradeContext.sVouhType                               凭证种类
    #TradeContext.sStartNo                                起始号码
    #TradeContext.sEndNo                                  终止号码
    #TradeContext.sVouhStatus                             凭证状态
    #TradeContext.sDepository                             库箱标志
    #TradeContext.sTellerTailNo                           尾箱号
    #TradeContext.sWSNO                                   终端号
    try:
        #=============初始化返回报文变量========================
        TradeContext.tradeResponse = []
        
        #=============获取当前系统时间==========================
        TradeContext.sLstTrxDay  = AfaUtilTools.GetSysDate( )
        TradeContext.sLstTrxTime = AfaUtilTools.GetSysTime( )
        
        #=============判断输入尾箱号与凭证状态是否符合规则===========                 
        if TradeContext.sTellerTailNo =='000':                                        
            if TradeContext.sVouhStatus not in ('0','1','2'):                         
                AfaLoggerFunc.tradeInfo('输入尾箱号：'+ TradeContext.sTellerTailNo)   
                AfaLoggerFunc.tradeInfo('输入凭证状态：'+ TradeContext.sVouhStatus)   
                tradeExit('A005061', '输入尾箱号与凭证状态不相符!')                   
                raise AfaFlowControl.flowException( )                                 
        	  	                                                                        
        else:                                                                         
            if TradeContext.sVouhStatus not in ('3','4','5','6'):                     
                AfaLoggerFunc.tradeInfo('输入尾箱号：'+ TradeContext.sTellerTailNo)   
                AfaLoggerFunc.tradeInfo('输入凭证状态：'+ TradeContext.sVouhStatus)   
                tradeExit('A005061', '输入尾箱号与凭证状态不相符!')                   
                raise AfaFlowControl.flowException( )
                
        #=============获取机构类型==========================                                   
        HostContext.I1OTSB = TradeContext.sBesbNo         #机构代号                            
        HostContext.I1SBNO = TradeContext.sBesbNo         #机构号                              
        HostContext.I1USID = '999996'                     #柜员号                              
                                                                                               
        if(not VouhHostFunc.CommHost('2001')):                                                 
            tradeExit( TradeContext.errorCode, TradeContext.errorMsg )                         
            raise AfaFlowControl.flowException( )                                              
        if(TradeContext.errorCode == '0000'):                                                  
            SBNO = HostContext.O1SBCH                                                          
            AfaLoggerFunc.tradeInfo( '机构级别:'+ SBNO )
            
        TradeContext.sDepository=''
                                                                                               
        if(SBNO=='33'):                                                                        
                                                                                               
            if (TradeContext.sTellerTailNo<>'000' or TradeContext.sVouhStatus not in('0','1')):
                tradeExit('A005061', '财务机构库管员尾箱号为000，入库状态0，出库状态1')    
                raise AfaFlowControl.flowException( )                                          
                                                                                               
            if TradeContext.sVouhStatus=='0':
                TradeContext.sDepository='1'
            else:                                                                              
                TradeContext.sDepository=''
            
                                                                                               
        elif(SBNO=='31' or SBNO=='40' or SBNO=='32' or SBNO=='41'):                            
                                                                                               
            if TradeContext.sTellerTailNo=='000':                                              
                TradeContext.sDepository='2'                                                  
                TradeContext.sVouhStatus='2'                                                  
            else:                                                                              
                TradeContext.sDepository='4'                                                  
                                                                                               
        elif(SBNO=='50'):                                                                      
                                                                                               
            if TradeContext.sTellerTailNo=='000':                                              
                TradeContext.sDepository='3'                                                  
                TradeContext.sVouhStatus='2'                                                  
            else:                                                                              
                TradeContext.sDepository='4'                                                   
                                                                                               
        else:                                                                                  
            tradeExit('A005061', '该机构级别不在指定范围内')                                   
            raise AfaFlowControl.flowException( )                                              
        
        
        #=============查询数据库中是否存在需要调整的号段==========================                 
        sqlStr = ""                                                                                
        sqlStr = "select TELLERNO,DEPOSITORY,VOUHSTATUS from VOUH_REGISTER WHERE "                 
        sqlStr = sqlStr + "BESBNO ='" + TradeContext.sBesbNo +"'"                                  
        sqlStr = sqlStr + "AND VOUHTYPE ='" + TradeContext.sVouhType +"'"                          
        sqlStr = sqlStr + "AND STARTNO ='" + TradeContext.sStartNo +"'"                            
        sqlStr = sqlStr + "AND ENDNO ='" + TradeContext.sEndNo +"'"                                
                                                                                                   
        AfaLoggerFunc.tradeInfo( sqlStr )                                                          
        records = AfaDBFunc.SelectSql( sqlStr )                                                    
                                                                                                   
        if( records == None ):                                                                     
            tradeExit('A005061', '查询[凭证登记表]操作异常!')                                      
            raise AfaFlowControl.flowException( )                                                  
                                                                                                   
        elif( len( records ) == 0 ):                                                               
            tradeExit('A005067', '凭证库中不存在此条记录!')                                        
                                                                                                   
        else :                                                                                     
            AfaLoggerFunc.tradeInfo( "原记录尾箱号：" + records[0][0] )                            
            AfaLoggerFunc.tradeInfo( "原记录库箱标识：" + records[0][1] )                          
            AfaLoggerFunc.tradeInfo( "原记录凭证状态：" + records[0][2] )                          
                                                                                                   
            #将凭证号段调整至正常状态
            sql1 = ""                                                                
            sql1 = sql1 + "update vouh_register set "
            sql1 = sql1 + "TELLERNO ='" + TradeContext.sTellerTailNo +"',"
            sql1 = sql1 + "DEPOSITORY ='" + TradeContext.sDepository +"'," 
            sql1 = sql1 + "VOUHSTATUS ='" + TradeContext.sVouhStatus +"'"          
            sql1 = sql1 + "where BESBNO ='" + TradeContext.sBesbNo +"'"                    	  
            sql1 = sql1 + " and VOUHTYPE ='" + TradeContext.sVouhType +"'"                
            sql1 = sql1 + " and STARTNO ='" + TradeContext.sStartNo +"'"                      
            sql1 = sql1 + " and ENDNO ='" + TradeContext.sEndNo +"'"                          
                                                                                         
            AfaLoggerFunc.tradeInfo(sql1)                                                
                                                                                         
            if  AfaDBFunc.UpdateSqlCmt(sql1)<0:                                          
                return AfaFlowControl.ExitThisFlow("A005067","凭证号段调整失败！")
            
            TradeContext.tradeResponse.append( ['sLstTrxDay',TradeContext.sLstTrxDay] )
            TradeContext.tradeResponse.append( ['sLstTrxTime',TradeContext.sLstTrxTime] )
            TradeContext.tradeResponse.append( ['sVouhType',TradeContext.sVouhType] )
            TradeContext.tradeResponse.append( ['sStartNo',TradeContext.sStartNo] )      
            TradeContext.tradeResponse.append( ['sEndNo',TradeContext.sEndNo] )
            TradeContext.tradeResponse.append( ['errorCode','0000'] )                        
            TradeContext.tradeResponse.append( ['errorMsg','交易成功'] )             
                

        #自动打包
        AfaFunc.autoPackData()

        #=============程序退出====================
        AfaLoggerFunc.tradeInfo( '凭证号段调整['+TradeContext.TemplateCode+']退出' )
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))

