# -*- coding: gbk -*-
###################################################################
#    ��    ��:    Tvouh021.py
#    ˵    ��:    ƾ֤����-->��ѯƾ֤״̬
#    ��    ��:    �м�ҵ����ƽ̨��AFA��--- UNIX: AIX 5.3
#    ��    ��:    ���ǽ�
#    ��    ˾:    ������ͬ�Ƽ�
#    ������ַ:    ����
#    ����ʱ��:    2008��6��11�� 
#    ά����¼:
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, AfaFlowControl, AfaDBFunc
from types import *
import VouhFunc,HostContext,VouhHostFunc

#=============���ش�����,������Ϣ===================================
def tradeExit( code, msg ):
    TradeContext.errorCode, TradeContext.errorMsg=code, msg
    if code != '0000':
        return False
    return True

def main( ):
    AfaLoggerFunc.tradeInfo( 'ƾ֤ʹ�ò�ѯ['+TradeContext.TemplateCode+']����' )

    #=============ǰ̨��������===================================
    #TradeContext.sVouhNo                                 ƾ֤����
    #TradeContext.sVouhType                               ƾ֤����
    #TradeContext.sBESBNO                                 ������
    #TradeContext.sTellerNo                               ��Ա��
    #TradeContext.sStartNo                                ��ʼ����
    #TradeContext.sEndNo                                  ��ֹ����
    #TradeContext.sRivTeller                              �Է���Ա
    #TradeContext.sVouhStatus                             ƾ֤״̬
    #TradeContext.sVouhNum                                ƾ֤����
    #TradeContext.sLstTrxDay                              ���������
    #TradeContext.sLstTrxTime                             �����ʱ��
    #TradeContext.sDepository                             �����־
    #TradeContext.sVouhName                               ƾ֤����
    
    try:
        #=============��ʼ�����ر��ı���========================
        TradeContext.tradeResponse = []
        
        #=============��ȡ��ǰϵͳʱ��==========================
        TradeContext.sLstTrxDay  = AfaUtilTools.GetSysDate( )
        TradeContext.sLstTrxTime = AfaUtilTools.GetSysTime( )
        
        #beginƾ֤�Ż�����201109  
        #=============��ȡ��Աβ���===============================
        HostContext.I1SBNO = TradeContext.sBesbNo         #������
        HostContext.I1USID = TradeContext.sTellerNo       #��Ա��
        HostContext.I1WSNO = TradeContext.sWSNO           #�ն˺�
        HostContext.I1EDDT = TradeContext.sLstTrxDay      #��ֹ����
        HostContext.I1TELR = TradeContext.sTellerNo       #��Ա����
        
        if(not VouhHostFunc.CommHost('0104')):
            VouhFunc.tradeExit( TradeContext.errorCode, TradeContext.errorMsg )
            raise AfaFlowControl.flowException( )
        if(TradeContext.errorCode == '0000'):
            TradeContext.sTellerTailNobak = HostContext.O2CABO
            TradeContext.sTellerTailNo    = TradeContext.sTellerTailNobak[0]                 
            AfaLoggerFunc.tradeInfo( '���׹�Աβ��ţ�' + TradeContext.sTellerTailNo ) 
        #end   
        
        #==============�ж�ƾ֤״̬===========================================
        sqlStr = "SELECT VOUHTYPE,VOUHNAME,BESBNO FROM VOUH_PARAMETER WHERE (SUBSTR(BESBNO,1,6) = '"+ (TradeContext.sBesbNo)[:6] +"' \
                    or BESBNO ='3400008887')"
        if (len(TradeContext.sVouhType)!=0 and len(TradeContext.sVouhType)!=0):
            sqlStr = sqlStr + " AND VOUHTYPE = '" + TradeContext.sVouhType + "' AND STATUS = '1'"
        
        AfaLoggerFunc.tradeInfo( 'sqlStr = ' + sqlStr )
        records = AfaDBFunc.SelectSql( sqlStr )
        if( records == None ):
            TradeContext.tradeResponse.append( ['retCount','0'] )
            tradeExit( 'A005052', '��ѯ[ƾ֤����ά����]�����쳣!'  )
            raise AfaFlowControl.flowException( )
        elif( len( records )==0 ):
            TradeContext.tradeResponse.append( ['retCount','0'] )
            tradeExit( 'A005059', '��ѯ[ƾ֤����ά����]������Ϣ������!' )
            raise AfaFlowControl.flowException( )
        
        #===================�ж��Ƿ�Ϊ�����Ŷ�=======================================
        
        sqlStr = "select STARTNO,ENDNO,LSTTRXDAY,LSTTRXTIME,RIVTELLER,TELLERNO \
            from VOUH_REGISTER \
            where VOUHTYPE = '" + TradeContext.sVouhType+ "' \
            and BESBNO = '" + TradeContext.sBesbNo + "'\
            and TELLERNO = '" + TradeContext.sTellerTailNo + "'\
            and VOUHSTATUS = '3' \
            and ( ENDNO >= '" + TradeContext.sEndNo + "' and STARTNO <= '" + TradeContext.sStartNo + "' )"
        records = AfaDBFunc.SelectSql( sqlStr )
        AfaLoggerFunc.tradeDebug(sqlStr)
        if( records == None ):          #��ѯƾ֤�ǼǱ��쳣
            tradeExit('A005061', '��ѯ[ƾ֤�ǼǱ�]�����쳣!')
            raise AfaFlowControl.flowException( )
        elif( len( records ) == 0 ):    #���ƾ֤�ǼǱ����޶�Ӧ��¼
            tradeExit('A005067', 'ƾ֤����ʧ��,ƾ֤���в����ڱ��β�����ƾ֤!')
            raise AfaFlowControl.flowException( )

        TradeContext.sVouhNo=TradeContext.sStartNo


        sqlStr = "select STARTNO,ENDNO from VOUH_REGISTER \
            where TELLERNO = '" + TradeContext.sTellerTailNo + "' \
            and BESBNO = '" + TradeContext.sBesbNo + "'\
            and VOUHTYPE = '" + TradeContext.sVouhType + "'\
            and VOUHSTATUS = '3' \
            and STARTNO = '" + TradeContext.sVouhNo + "'"

        records = AfaDBFunc.SelectSql( sqlStr )
        AfaLoggerFunc.tradeDebug(sqlStr)
        if( records == None ):          #��ѯƾ֤�ǼǱ��쳣
            tradeExit('A005061', '��ѯ[ƾ֤�ǼǱ�]�����쳣!')
            raise AfaFlowControl.flowException( )
        elif( len( records ) == 0 ):    #���ƾ֤�ǼǱ����޶�Ӧ��¼
            tradeExit('A005067', 'ƾ֤����ʧ��,ƾ֤���в����ڱ��β�����ƾ֤!')
            sStatus = '1'
            #raise AfaFlowControl.flowException( )
        else :
            vouhNos = []
            for i in range(len(records)):
                vouhNos.append(int(records[i][0]))
            if(int(TradeContext.sVouhNo)== min(vouhNos)):
                tradeExit('0000', 'ƾ֤����ȷ������')
                sStatus = '0'
            else:
                tradeExit('A005061', 'ƾ֤�������!!')
                sStatus = '1'
                #raise AfaFlowControl.flowException( )

        TradeContext.tradeResponse.append( ['sVouhType',TradeContext.sVouhType] )
        TradeContext.tradeResponse.append( ['sVouhName',''] )
        TradeContext.tradeResponse.append( ['sStartNo',TradeContext.sVouhNo] )
        TradeContext.tradeResponse.append( ['sEndNo',TradeContext.sVouhNo] )
        TradeContext.tradeResponse.append( ['sVouhNum','1'] )
        TradeContext.tradeResponse.append( ['sStatus',sStatus] )
        TradeContext.tradeResponse.append( ['sLstTrxDay',TradeContext.sLstTrxDay] )
        TradeContext.tradeResponse.append( ['sLstTrxTime',TradeContext.sLstTrxTime] )
        TradeContext.tradeResponse.append( ['sNum','1'] )
        TradeContext.tradeResponse.append( ['errorCode','0000'] )
        TradeContext.tradeResponse.append( ['errorMsg','���׳ɹ�'] )
        #�Զ����
        AfaFunc.autoPackData()

        #=============�����˳�=========================================
        AfaLoggerFunc.tradeInfo( 'ƾ֤ʹ�ò�ѯ['+TradeContext.TemplateCode+']�˳�' )
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
