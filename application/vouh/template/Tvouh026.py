# -*- coding: gbk -*-
###################################################################
#    ��    ��:    Tvouh026.py
#    ˵    ��:    ƾ֤����-->ƾ֤�Ŷε���
#    ��    ��:    �м�ҵ����ƽ̨��AFA��--- UNIX: AIX 5.3
#    ��    ��:    LLJ
#    ��    ˾:    ������ͬ�Ƽ�
#    ������ַ:    ����
#    ����ʱ��:    2012��7��
#    ά����¼:   
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, AfaFlowControl, AfaDBFunc,VouhHostFunc,HostContext
from types import *

#=============���ش�����,������Ϣ===================================        
def tradeExit( code, msg ):                                                 
    TradeContext.errorCode, TradeContext.errorMsg=code, msg                 
    if code != '0000':                                                      
        return False                                                        
    return True                                                             

def main( ):
    AfaLoggerFunc.tradeInfo( 'ƾ֤�Ŷε���['+TradeContext.TemplateCode+']����' )

    #=============ǰ̨��������===================================
    #TradeContext.sBesbNo                                 ��������
    #TradeContext.sCur                                    ���Ҵ���
    #TradeContext.sTellerNo                               ��Ա��
    #TradeContext.sVouhType                               ƾ֤����
    #TradeContext.sStartNo                                ��ʼ����
    #TradeContext.sEndNo                                  ��ֹ����
    #TradeContext.sVouhStatus                             ƾ֤״̬
    #TradeContext.sDepository                             �����־
    #TradeContext.sTellerTailNo                           β���
    #TradeContext.sWSNO                                   �ն˺�
    try:
        #=============��ʼ�����ر��ı���========================
        TradeContext.tradeResponse = []
        
        #=============��ȡ��ǰϵͳʱ��==========================
        TradeContext.sLstTrxDay  = AfaUtilTools.GetSysDate( )
        TradeContext.sLstTrxTime = AfaUtilTools.GetSysTime( )
        
        #=============�ж�����β�����ƾ֤״̬�Ƿ���Ϲ���===========                 
        if TradeContext.sTellerTailNo =='000':                                        
            if TradeContext.sVouhStatus not in ('0','1','2'):                         
                AfaLoggerFunc.tradeInfo('����β��ţ�'+ TradeContext.sTellerTailNo)   
                AfaLoggerFunc.tradeInfo('����ƾ֤״̬��'+ TradeContext.sVouhStatus)   
                tradeExit('A005061', '����β�����ƾ֤״̬�����!')                   
                raise AfaFlowControl.flowException( )                                 
        	  	                                                                        
        else:                                                                         
            if TradeContext.sVouhStatus not in ('3','4','5','6'):                     
                AfaLoggerFunc.tradeInfo('����β��ţ�'+ TradeContext.sTellerTailNo)   
                AfaLoggerFunc.tradeInfo('����ƾ֤״̬��'+ TradeContext.sVouhStatus)   
                tradeExit('A005061', '����β�����ƾ֤״̬�����!')                   
                raise AfaFlowControl.flowException( )
                
        #=============��ȡ��������==========================                                   
        HostContext.I1OTSB = TradeContext.sBesbNo         #��������                            
        HostContext.I1SBNO = TradeContext.sBesbNo         #������                              
        HostContext.I1USID = '999996'                     #��Ա��                              
                                                                                               
        if(not VouhHostFunc.CommHost('2001')):                                                 
            tradeExit( TradeContext.errorCode, TradeContext.errorMsg )                         
            raise AfaFlowControl.flowException( )                                              
        if(TradeContext.errorCode == '0000'):                                                  
            SBNO = HostContext.O1SBCH                                                          
            AfaLoggerFunc.tradeInfo( '��������:'+ SBNO )
            
        TradeContext.sDepository=''
                                                                                               
        if(SBNO=='33'):                                                                        
                                                                                               
            if (TradeContext.sTellerTailNo<>'000' or TradeContext.sVouhStatus not in('0','1')):
                tradeExit('A005061', '����������Աβ���Ϊ000�����״̬0������״̬1')    
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
            tradeExit('A005061', '�û���������ָ����Χ��')                                   
            raise AfaFlowControl.flowException( )                                              
        
        
        #=============��ѯ���ݿ����Ƿ������Ҫ�����ĺŶ�==========================                 
        sqlStr = ""                                                                                
        sqlStr = "select TELLERNO,DEPOSITORY,VOUHSTATUS from VOUH_REGISTER WHERE "                 
        sqlStr = sqlStr + "BESBNO ='" + TradeContext.sBesbNo +"'"                                  
        sqlStr = sqlStr + "AND VOUHTYPE ='" + TradeContext.sVouhType +"'"                          
        sqlStr = sqlStr + "AND STARTNO ='" + TradeContext.sStartNo +"'"                            
        sqlStr = sqlStr + "AND ENDNO ='" + TradeContext.sEndNo +"'"                                
                                                                                                   
        AfaLoggerFunc.tradeInfo( sqlStr )                                                          
        records = AfaDBFunc.SelectSql( sqlStr )                                                    
                                                                                                   
        if( records == None ):                                                                     
            tradeExit('A005061', '��ѯ[ƾ֤�ǼǱ�]�����쳣!')                                      
            raise AfaFlowControl.flowException( )                                                  
                                                                                                   
        elif( len( records ) == 0 ):                                                               
            tradeExit('A005067', 'ƾ֤���в����ڴ�����¼!')                                        
                                                                                                   
        else :                                                                                     
            AfaLoggerFunc.tradeInfo( "ԭ��¼β��ţ�" + records[0][0] )                            
            AfaLoggerFunc.tradeInfo( "ԭ��¼�����ʶ��" + records[0][1] )                          
            AfaLoggerFunc.tradeInfo( "ԭ��¼ƾ֤״̬��" + records[0][2] )                          
                                                                                                   
            #��ƾ֤�Ŷε���������״̬
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
                return AfaFlowControl.ExitThisFlow("A005067","ƾ֤�Ŷε���ʧ�ܣ�")
            
            TradeContext.tradeResponse.append( ['sLstTrxDay',TradeContext.sLstTrxDay] )
            TradeContext.tradeResponse.append( ['sLstTrxTime',TradeContext.sLstTrxTime] )
            TradeContext.tradeResponse.append( ['sVouhType',TradeContext.sVouhType] )
            TradeContext.tradeResponse.append( ['sStartNo',TradeContext.sStartNo] )      
            TradeContext.tradeResponse.append( ['sEndNo',TradeContext.sEndNo] )
            TradeContext.tradeResponse.append( ['errorCode','0000'] )                        
            TradeContext.tradeResponse.append( ['errorMsg','���׳ɹ�'] )             
                

        #�Զ����
        AfaFunc.autoPackData()

        #=============�����˳�====================
        AfaLoggerFunc.tradeInfo( 'ƾ֤�Ŷε���['+TradeContext.TemplateCode+']�˳�' )
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))

